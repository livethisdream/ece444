# nec_lab, packaged so a whole class can reach one running copy.
#
# The point of this image is the machine that serves the room, not the machine
# a student sits at: a managed Windows PC cannot install Docker, but it can
# open a browser. Run this on a box you control, hand out the address, and the
# barrier at the student's end is a URL.
#
#   docker build -t nec_lab scripts/nec_lab
#   docker run --rm -p 8444:8444 nec_lab
#
# Ubuntu rather than a slim Python base because `nec2c` is packaged here and
# verified at this version; the image carries BOTH engines, so the build can
# check one against the other before it is ever put in front of a class.
FROM ubuntu:24.04

ENV DEBIAN_FRONTEND=noninteractive \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

RUN apt-get update \
 && apt-get install -y --no-install-recommends \
      python3 python3-venv nec2c ca-certificates \
 && rm -rf /var/lib/apt/lists/*

# PEP 668 marks the system Python as externally managed, so PyNEC goes in a
# venv rather than fighting apt for site-packages.
RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Wheel or nothing. PyNEC publishes no ARM wheel, and this image has no
# compiler, so on a Raspberry Pi the source build would fail and take the whole
# image down with it. nec2c is already installed above and is packaged for
# arm64, so an ARM build simply runs on that -- which is also the faster engine
# when several people share one server, because subprocesses use every core
# while PyNEC holds the GIL.
RUN pip install --no-cache-dir --only-binary :all: PyNEC \
 || echo "no PyNEC wheel for this architecture; nec2c will do the solving"


WORKDIR /app
COPY . /app/nec_lab

# The build fails unless both engines run, agree with each other, and still
# reproduce the L7 and L8 numbers. An image that ships is an image that passed.
RUN python -m nec_lab.selftest

RUN useradd --system --create-home --uid 10001 necuser
USER necuser

EXPOSE 8444
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
  CMD python -c "import sys,urllib.request; \
sys.exit(0 if urllib.request.urlopen('http://127.0.0.1:8444/api/engine', timeout=3).status == 200 else 1)"

CMD ["python", "-m", "nec_lab", "serve", \
     "--host", "0.0.0.0", "--port", "8444", "--no-browser"]
