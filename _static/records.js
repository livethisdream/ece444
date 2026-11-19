/* Lab records: type a lab's Part 2 values on the lab page as you go, then
 * write them into the lab packet PDF.
 *
 * Markup (raw HTML in a lab page, outside any present block so it shows in
 * read mode only):
 *
 *   <div class="rec" data-lab="L17">
 *   <label>Ping result <input data-field="b.ping"></label>
 *   </div>
 *
 *   <div class="rec-summary" data-lab="L17"
 *        data-pdf="../../labs/ECE444_Lab_L17_Hardware_blank.pdf"
 *        data-file="ECE444_L17_Lab"></div>
 *
 * data-field is the name of an AcroForm field in the blank packet: the
 * faculty LaTeX writes \kv[b.ping]{...}, and the blank build turns that cell
 * into a field of that name. The page knows only the names, never the
 * answers. scripts/verify/check_records.py checks that every name here exists
 * in the PDF.
 *
 * Entries live in this browser's localStorage, one key per lab, and never
 * leave the laptop. The summary frame lists them all, writes them into the
 * blank packet (or into a copy the cadet has already worked in) with pdf-lib,
 * flattens the form so every viewer and Gradescope shows the values, and
 * offers an export file as a backup.
 */
(function () {
    'use strict';

    var scriptSrc = (document.currentScript && document.currentScript.src) || '';
    var staticBase = scriptSrc.replace(/records\.js(\?.*)?$/, '');
    var PDFLIB = staticBase + 'vendor/pdf-lib-1.17.1.min.js';

    function storeKey(lab) { return 'ece444.records.' + lab; }

    function load(lab) {
        try { return JSON.parse(localStorage.getItem(storeKey(lab)) || '{}') || {}; }
        catch (e) { return {}; }
    }

    function save(lab, data) {
        try { localStorage.setItem(storeKey(lab), JSON.stringify(data)); return true; }
        catch (e) { return false; }
    }

    // pdf-lib's standard font is WinAnsi: map the usual typographic
    // characters to plain ones and drop anything else it cannot draw, rather
    // than have one character abort the whole packet.
    function clean(v) {
        return String(v)
            .replace(/[−–—]/g, '-')
            .replace(/[‘’]/g, "'")
            .replace(/[“”]/g, '"')
            .replace(/…/g, '...')
            .replace(/[^\x20-\x7e\xa0-\xff]/g, '');
    }

    function loadPdfLib() {
        if (window.PDFLib) return Promise.resolve(window.PDFLib);
        return new Promise(function (resolve, reject) {
            var s = document.createElement('script');
            s.src = PDFLIB;
            s.onload = function () { resolve(window.PDFLib); };
            s.onerror = function () { reject(new Error('could not load ' + PDFLIB)); };
            document.head.appendChild(s);
        });
    }

    function download(bytes, name, type) {
        var blob = new Blob([bytes], { type: type });
        var url = URL.createObjectURL(blob);
        var a = document.createElement('a');
        a.href = url;
        a.download = name;
        document.body.appendChild(a);
        a.click();
        a.remove();
        setTimeout(function () { URL.revokeObjectURL(url); }, 10000);
    }

    function Lab(name) {
        this.name = name;
        this.data = load(name);
        this.inputs = [];      // every input bound to this lab, steps and summary
        this.fields = [];      // unique field names, page order
        this.labels = {};      // field -> label text from its first occurrence
        this.summaries = [];
    }

    Lab.prototype.bind = function (input) {
        var self = this;
        var f = input.getAttribute('data-field');
        if (!f) return;
        if (this.fields.indexOf(f) < 0) {
            this.fields.push(f);
            var lab = input.closest('label');
            var text = input.getAttribute('data-label') ||
                (lab ? lab.textContent.trim() : f);
            this.labels[f] = text;
        }
        if (this.data[f] !== undefined) input.value = this.data[f];
        input.setAttribute('autocomplete', 'off');
        input.setAttribute('spellcheck', 'false');
        input.addEventListener('input', function () {
            self.data[f] = input.value;
            save(self.name, self.data);
            self.inputs.forEach(function (other) {
                if (other !== input && other.getAttribute('data-field') === f) other.value = input.value;
            });
            self.refresh();
        });
        this.inputs.push(input);
    };

    Lab.prototype.count = function () {
        var d = this.data;
        return this.fields.filter(function (f) { return d[f] && String(d[f]).trim(); }).length;
    };

    Lab.prototype.refresh = function () {
        var n = this.count(), total = this.fields.length;
        this.summaries.forEach(function (s) {
            var st = s.querySelector('.rec-status');
            if (st) st.textContent = n + ' of ' + total + ' entries filled.';
        });
    };

    Lab.prototype.fill = function (bytes, fileBase, summary) {
        var self = this;
        var msg = summary.querySelector('.rec-message');
        msg.textContent = 'Writing your entries into the packet...';
        return loadPdfLib().then(function (PDFLib) {
            return PDFLib.PDFDocument.load(bytes).then(function (doc) {
                var form = doc.getForm();
                if (form.getFields().length === 0) {
                    throw new Error('This PDF has no fillable fields left. It may already have been ' +
                        'downloaded from this page once; start from the blank packet or your own working copy.');
                }
                var missing = [];
                self.fields.forEach(function (f) {
                    var v = self.data[f];
                    if (v === undefined || v === '') return;
                    try { form.getTextField(f).setText(clean(v)); }
                    catch (e) { missing.push(f); }
                });
                form.flatten();
                return doc.save().then(function (out) {
                    var kit = (self.data['b.kit'] || '').trim().replace(/[^A-Za-z0-9-]/g, '');
                    var name = fileBase + (kit ? '_kit' + kit : '') + '.pdf';
                    download(out, name, 'application/pdf');
                    msg.textContent = 'Saved ' + name + '.' + (missing.length
                        ? ' These entries had no place in this PDF: ' + missing.join(', ') + '.'
                        : ' Upload it to Gradescope.');
                });
            });
        }).catch(function (e) {
            msg.textContent = 'Could not write the packet: ' + e.message;
        });
    };

    Lab.prototype.buildSummary = function (box) {
        var self = this;
        var pdf = box.getAttribute('data-pdf');
        var fileBase = box.getAttribute('data-file') || ('ECE444_' + this.name + '_Lab');
        box.innerHTML = '';

        var table = document.createElement('div');
        table.className = 'rec rec-table';
        this.fields.forEach(function (f) {
            var lab = document.createElement('label');
            lab.appendChild(document.createTextNode(self.labels[f] + ' '));
            var input = document.createElement('input');
            input.setAttribute('data-field', f);
            lab.appendChild(input);
            table.appendChild(lab);
        });
        box.appendChild(table);

        var status = document.createElement('p');
        status.className = 'rec-status';
        box.appendChild(status);

        var bar = document.createElement('div');
        bar.className = 'rec-actions';
        function button(text, onclick) {
            var b = document.createElement('button');
            b.type = 'button';
            b.textContent = text;
            b.addEventListener('click', onclick);
            bar.appendChild(b);
            return b;
        }
        function picker(accept, onfile) {
            var i = document.createElement('input');
            i.type = 'file';
            i.accept = accept;
            i.hidden = true;
            i.addEventListener('change', function () {
                if (i.files && i.files[0]) onfile(i.files[0]);
                i.value = '';
            });
            bar.appendChild(i);
            return i;
        }

        var copyPicker = picker('application/pdf,.pdf', function (file) {
            file.arrayBuffer().then(function (buf) { self.fill(buf, fileBase, box); });
        });
        var importPicker = picker('application/json,.json', function (file) {
            file.text().then(function (txt) {
                var got = JSON.parse(txt);
                Object.keys(got).forEach(function (k) { if (self.fields.indexOf(k) >= 0) self.data[k] = String(got[k]); });
                save(self.name, self.data);
                self.inputs.forEach(function (i) {
                    var f = i.getAttribute('data-field');
                    i.value = self.data[f] !== undefined ? self.data[f] : '';
                });
                self.refresh();
                msg.textContent = 'Entries restored from ' + file.name + '.';
            }).catch(function () { msg.textContent = 'That file is not an entries backup from this page.'; });
        });

        button('Download my packet', function () {
            fetch(pdf).then(function (r) {
                if (!r.ok) throw new Error('HTTP ' + r.status);
                return r.arrayBuffer();
            }).then(function (buf) { return self.fill(buf, fileBase, box); })
              .catch(function (e) { msg.textContent = 'Could not fetch the blank packet: ' + e.message; });
        });
        button('Fill my own copy...', function () { copyPicker.click(); });
        button('Export entries', function () {
            download(JSON.stringify(self.data, null, 1), fileBase + '_entries.json', 'application/json');
        });
        button('Import entries...', function () { importPicker.click(); });
        button('Clear', function () {
            if (!window.confirm('Clear every ' + self.name + ' Lab entry in this browser?')) return;
            self.data = {};
            save(self.name, self.data);
            self.inputs.forEach(function (i) { i.value = ''; });
            self.refresh();
        });
        box.appendChild(bar);

        var msg = document.createElement('p');
        msg.className = 'rec-message';
        msg.setAttribute('role', 'status');
        box.appendChild(msg);
        if (!save(this.name, this.data)) {
            msg.textContent = 'This browser is not saving entries (private window or blocked storage): ' +
                'download the packet or export your entries before you close the page.';
        }

        this.summaries.push(box);
        table.querySelectorAll('input[data-field]').forEach(function (i) { self.bind(i); });
    };

    function init() {
        var labs = {};
        function lab(name) { return labs[name] || (labs[name] = new Lab(name)); }
        document.querySelectorAll('.rec[data-lab] input[data-field]').forEach(function (input) {
            lab(input.closest('.rec').getAttribute('data-lab')).bind(input);
        });
        document.querySelectorAll('.rec-summary[data-lab]').forEach(function (box) {
            lab(box.getAttribute('data-lab')).buildSummary(box);
        });
        Object.keys(labs).forEach(function (k) { labs[k].refresh(); });
    }

    if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
    else init();
})();
