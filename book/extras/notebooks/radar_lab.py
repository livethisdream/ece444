"""radar_lab.py: the ECE 444 radar processing chain, L28 through L31.

The course provides this module complete. Each lab's notebook imports it and
runs it on your saved captures (or the course's recorded data); the lab tasks
change a parameter or a line or two, never a whole function. Python with
numpy and scipy only.

A capture is an .npz file, loaded by load_capture() into a dict:

    iq      complex, n_chirps x n_samples: the summed array, one chirp a row
    iq_ch   (optional) complex, 2 x n_chirps x n_samples: the two subarray
            halves, whose sum is iq; monopulse_angle() needs them
    fs      sample rate, Hz              fc      carrier, Hz
    B       chirp bandwidth, Hz          T_ramp  chirp length, s
    PRI     chirp start to chirp start, s
    f0      the 0 m frequency, Hz, from your L28 calibration

Conventions, the same on every lesson page:
  * Levels are dBFS: a tone of amplitude 1 reads 0 dB, whatever the window,
    because every FFT is divided by the sum of its window.
  * Range is measured from the 0 m frequency: R = c T_ramp (f - f0) / (2 B).
  * Velocity is radial and positive closing (toward the radar), L26's
    convention: a closing target has a positive Doppler shift.
  * A range-Doppler map is indexed [range, velocity].

L28  load_capture, range_axis, range_fft, range_profile, waterfall
L29  range_doppler, mti
L30  cfar_2d
L31  spectrogram, features, train, classify, confusion_matrix,
     alpha_beta, monopulse_angle
"""

import numpy as np
from scipy import signal

C = 3.00e8          # m/s, as on the course pages
D_SUB = 0.056       # m between the two subarray centers, 4 x 14 mm


def _window(name, n):
    """A window of length n by name ("hann", "hamming", "blackman", ...); None is rectangular."""
    return np.ones(n) if name is None else signal.get_window(name, n)


# ----------------------------------------------------------------------- L28
def load_capture(path):
    """Load a capture .npz into a dict, with its scalar settings as floats."""
    with np.load(path) as z:
        cap = {k: z[k] for k in z.files}
    for k in ("fs", "fc", "B", "T_ramp", "PRI", "f0"):
        cap[k] = float(cap[k])
    return cap


def range_axis(cap, n_fft=None):
    """Range in m of each bin of np.fft.fft along a chirp, in that FFT's own order.

    n_fft defaults to the samples in one chirp. Bins below f0 come out as
    negative ranges.
    """
    n = n_fft or cap["iq"].shape[1]
    f = np.fft.fftfreq(n, 1 / cap["fs"])
    k = C * cap["T_ramp"] / (2 * cap["B"])      # meters per hertz of beat
    return (f - cap["f0"]) * k


def range_fft(cap, window="hann", n_fft=None):
    """Complex range FFT of every chirp, n_chirps x n_bins, in range_axis order.

    n_fft > n_samples zero-pads: the same spectrum drawn on a finer grid.
    """
    iq = cap["iq"]
    w = _window(window, iq.shape[1])
    return np.fft.fft(iq * w, n_fft or iq.shape[1], axis=1) / w.sum()


def range_profile(cap, chirp=0, window="hann", n_fft=None):
    """One chirp's range profile: (r, p_db) for the ranges at or beyond 0 m."""
    r = range_axis(cap, n_fft)
    p_db = 20 * np.log10(np.abs(range_fft(cap, window, n_fft)[chirp]) + 1e-12)
    keep = r >= 0
    return r[keep], p_db[keep]


def waterfall(cap, window="hann", n_fft=None):
    """Every chirp's range profile: (r, t, w_db), one row of w_db per chirp."""
    r = range_axis(cap, n_fft)
    w_db = 20 * np.log10(np.abs(range_fft(cap, window, n_fft)) + 1e-12)
    t = np.arange(cap["iq"].shape[0]) * cap["PRI"]
    keep = r >= 0
    return r[keep], t, w_db[:, keep]


# ----------------------------------------------------------------------- L29
def range_doppler(cap, window="hann"):
    """Range-Doppler map: (rd_db, range_m, vel_mps), rd_db indexed [range, velocity].

    A range FFT along each chirp, then a Doppler FFT across the chirps of each
    range bin, both windowed. Ranges at or beyond 0 m only; velocity runs from
    -lambda/(4 PRI) to +lambda/(4 PRI), 0 m/s in the middle.
    """
    rp = range_fft(cap, window)                 # n_chirps x n_bins
    r = range_axis(cap)
    keep = r >= 0
    rp = rp[:, keep]
    m = rp.shape[0]
    wd = _window(window, m)
    rd = np.fft.fftshift(np.fft.fft(rp * wd[:, None], axis=0), axes=0) / wd.sum()
    lam = C / cap["fc"]
    vel = np.fft.fftshift(np.fft.fftfreq(m, cap["PRI"])) * lam / 2
    rd_db = 20 * np.log10(np.abs(rd.T) + 1e-12)
    return rd_db, r[keep], vel


def mti(cap, kind="2pulse"):
    """A pulse canceller across chirps; returns a capture, one or two chirps shorter.

    "2pulse": x[m] - x[m-1]; "3pulse": x[m] - 2 x[m-1] + x[m-2]; "none": unchanged.
    """
    def cancel(x):                              # chirps on the second-to-last axis
        if kind == "2pulse":
            return x[..., 1:, :] - x[..., :-1, :]
        if kind == "3pulse":
            return x[..., 2:, :] - 2 * x[..., 1:-1, :] + x[..., :-2, :]
        if kind == "none":
            return x
        raise ValueError(f"kind must be '2pulse', '3pulse', or 'none', not {kind!r}")
    out = {**cap, "iq": cancel(cap["iq"])}
    if "iq_ch" in cap:
        out["iq_ch"] = cancel(cap["iq_ch"])
    return out


# ----------------------------------------------------------------------- L30
def cfar_2d(rd_db, guard, ref, bias_db, axes=None, method="ca"):
    """2D CFAR on a range-Doppler map in dB: (det, hits).

    guard, ref: half-widths in cells, as (range, Doppler) pairs or one int for
    both. Each cell's noise estimate is the mean power of its reference cells,
    the ring between the guard cells and the outer edge; at a range edge it
    averages only the cells that exist, and the Doppler axis wraps around.
    method "ca" averages the whole ring; "go" and "so" average the ring's
    nearer-range and farther-range halves separately and keep the greater or
    the smaller. A cell is a detection when it exceeds its estimate by bias_db.

    det is a boolean map like rd_db. hits lists (range, velocity, snr_db) for
    each detected cell, in meters and m/s when axes=(range_m, vel_mps) is passed,
    in cell indices otherwise.
    """
    gr, gv = (guard, guard) if np.isscalar(guard) else guard
    rr, rv = (ref, ref) if np.isscalar(ref) else ref
    P = 10 ** (np.asarray(rd_db) / 10)          # dB back to power
    nr, nv = gr + rr, gv + rv
    win = np.ones((2 * nr + 1, 2 * nv + 1))
    win[rr:rr + 2 * gr + 1, rv:rv + 2 * gv + 1] = 0     # guard cells and the cell under test

    def pad(a):                                 # wrap Doppler, zeros beyond the range ends
        a = np.pad(a, ((0, 0), (nv, nv)), mode="wrap")
        return np.pad(a, ((nr, nr), (0, 0)))

    def mean_over(kernel):                      # kernel row i is range offset i - nr
        k = kernel[::-1, ::-1]                  # convolution flips; undo it
        total = signal.fftconvolve(pad(P), k, mode="valid")
        count = signal.fftconvolve(pad(np.ones_like(P)), k, mode="valid")
        return np.maximum(total, 1e-30) / np.maximum(count, 1e-9)

    if method == "ca":
        noise = mean_over(win)
    elif method in ("go", "so"):
        near, far = win.copy(), win.copy()
        near[nr:, :] = 0                        # keep the nearer-range rows
        far[:nr + 1, :] = 0                     # keep the farther-range rows
        pick = np.maximum if method == "go" else np.minimum
        noise = pick(mean_over(near), mean_over(far))
    else:
        raise ValueError(f"method must be 'ca', 'go', or 'so', not {method!r}")

    snr_db = 10 * np.log10(P / noise)
    det = snr_db > bias_db
    r_ax, v_ax = axes if axes is not None else (np.arange(P.shape[0]), np.arange(P.shape[1]))
    hits = [(r_ax[i], v_ax[j], snr_db[i, j]) for i, j in zip(*np.nonzero(det))]
    return det, hits


# ----------------------------------------------------------------------- L31
def spectrogram(cap, range_bin, n_win=64, hop=16):
    """Slow-time spectrogram of one range bin, or a slice of bins summed: (t, f, S_db).

    f is the Doppler frequency in Hz (velocity = f * lambda / 2), t the center
    time of each column, and S_db is indexed [f, t] with its peak at 0 dB.
    range_bin indexes range_fft's columns, the range_axis order. A slice of
    bins follows a target that moves in range; it is summed from the
    rectangular-window FFT, because a Hann-windowed tone puts -1/4, +1/2,
    -1/4 in neighboring bins, and those cancel in a sum whenever the target
    sits on a bin center.
    """
    many = not np.isscalar(range_bin)
    x = range_fft(cap, None if many else "hann")[:, range_bin]
    if many:                                    # a slice of bins: sum them
        x = x.sum(axis=1)
    x = x - x.mean()                            # stationary returns out
    w = np.hanning(n_win)
    cols = [np.fft.fftshift(np.fft.fft(x[i:i + n_win] * w))
            for i in range(0, len(x) - n_win + 1, hop)]
    S = 20 * np.log10(np.abs(np.array(cols).T) + 1e-12)
    f = np.fft.fftshift(np.fft.fftfreq(n_win, cap["PRI"]))
    t = (np.arange(S.shape[1]) * hop + n_win / 2) * cap["PRI"]
    return t, f, S - S.max()


def features(t, f, S, lam, floor_db=-15):
    """Three features of a spectrogram: [mean |centroid| m/s, mean spread m/s, periodicity].

    Each column's power above floor_db (relative to that column's peak) gives
    a Doppler centroid and spread. Periodicity is the largest normalized
    autocorrelation of the spectrogram over lags of 0.25 to 2 s: near 1 for a
    steady repeating motion such as a stride or a wave, near 0 for none.
    """
    S = S - S.max(axis=0, keepdims=True)        # each column's peak at 0 dB
    P = np.where(S > floor_db, 10 ** (S / 10), 0.0)
    fc = (f[:, None] * P).sum(0) / P.sum(0)     # centroid, each column
    sd = np.sqrt(((f[:, None] - fc) ** 2 * P).sum(0) / P.sum(0))
    D = np.maximum(S, floor_db)
    D = np.array([np.convolve(row, np.ones(12) / 12, "valid") for row in D])
    D = D - D.mean(axis=1, keepdims=True)
    dt = t[1] - t[0]
    lags = range(max(1, int(0.25 / dt)), min(int(2.0 / dt), D.shape[1] - 1))
    r = [np.sum(D[:, :-n] * D[:, n:]) / np.sum(D ** 2) for n in lags]
    return np.array([abs(fc.mean()) * lam / 2, sd.mean() * lam / 2, max(r, default=0.0)])


def train(X, y):
    """A nearest-centroid classifier. X: one row of features per trial; y: each trial's class."""
    X, y = np.asarray(X, float), np.asarray(y)
    mu, sd = X.mean(0), X.std(0)
    sd = np.where(sd > 0, sd, 1.0)
    cents = {c: ((X[y == c] - mu) / sd).mean(0) for c in sorted(set(y))}
    return mu, sd, cents


def classify(x, model):
    """The class whose centroid is nearest to feature vector x, in standardized units."""
    mu, sd, cents = model
    z = (np.asarray(x, float) - mu) / sd
    return min(cents, key=lambda c: np.sum((z - cents[c]) ** 2))


def confusion_matrix(y_true, y_pred, labels):
    """Counts, rows the true class and columns the called class, in labels' order."""
    idx = {c: i for i, c in enumerate(labels)}
    M = np.zeros((len(labels), len(labels)), dtype=int)
    for a, b in zip(y_true, y_pred):
        M[idx[a], idx[b]] += 1
    return M


def alpha_beta(track_meas, alpha, beta, dt):
    """Alpha-beta track from one measurement per frame (NaN for a missed frame).

    Returns an array of (position, velocity) rows, one per frame, after each
    frame's update. Works for range in m or angle in degrees alike.
    """
    meas = np.asarray(track_meas, float)
    first = meas[~np.isnan(meas)][0]
    x, v = first, 0.0
    out = []
    for z in meas:
        x = x + v * dt                          # predict
        if not np.isnan(z):
            e = z - x                           # residual
            x, v = x + alpha * e, v + beta / dt * e
        out.append((x, v))
    return np.array(out)


def monopulse_angle(cap, range_bin, window="hann"):
    """Phase-comparison monopulse angle in degrees, one per chirp, from iq_ch.

    The two subarray centers sit D_SUB apart, so a target at angle theta puts
    a phase 2 pi D_SUB sin(theta) / lambda between the channels. The phase is
    known only within +/-180 deg, so the angle is unambiguous within
    +/-arcsin(lambda / (2 D_SUB)), +/-15.5 deg at 10 GHz. Which side of
    broadside reads positive depends on the kit's channel order; check it
    against a target placed to one side.
    """
    lam = C / cap["fc"]
    many = not np.isscalar(range_bin)           # a slice: rectangular, as in spectrogram()
    w = _window(None if many else window, cap["iq_ch"].shape[-1])
    X = np.fft.fft(cap["iq_ch"] * w, axis=-1)[..., range_bin]
    if many:
        X = X.sum(axis=-1)
    dphi = np.angle(X[1] * np.conj(X[0]))
    s = np.clip(dphi * lam / (2 * np.pi * D_SUB), -1, 1)
    return np.degrees(np.arcsin(s))
