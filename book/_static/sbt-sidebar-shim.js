// ECE 215/S — sidebar chevron-toggle shim. Ported from ECE 495.
//
// We use Sphinx's built-in globaltoc.html in html_sidebars to render the
// full global TOC on every page (sphinx-book-theme's default scoped
// sidebar truncates books with many parts). globaltoc emits flat
// <ul>/<li> markup. This shim post-processes that markup to insert the
// <details>/<summary> chevron toggles that match ECE-315's look.
//
// Branches containing the current page open by default. The companion
// CSS in custom.css styles the result so it renders like the default
// sphinx-book-theme sidebar.

(function () {
  function findGlobalToc() {
    // globaltoc.html renders inside .bd-sidebar-primary > div.sidebar-primary-item
    // The TOC is the last sidebar-primary-item that contains <p class="caption">.
    var sidebar = document.querySelector(".bd-sidebar-primary");
    if (!sidebar) return null;
    var items = sidebar.querySelectorAll(".sidebar-primary-item");
    for (var i = items.length - 1; i >= 0; i--) {
      if (items[i].querySelector("p.caption")) return items[i];
    }
    return null;
  }

  function shimSidebar() {
    var nav = findGlobalToc();
    if (!nav) return;

    // Tag the host with a known class so our CSS can target it.
    nav.classList.add("sy-globaltoc");

    // Repurpose the "Table of Contents" heading globaltoc.html emits at
    // the top of the nav into a clickable Home link. The element is an
    // <h3><a href=".../intro.html">Table of Contents</a></h3>; we
    // rename the link text to "Home", tag it as the active link if we're
    // currently on the home page, and let CSS handle styling.
    var homeHeading = nav.querySelector("h3");
    if (homeHeading) {
      var homeLink = homeHeading.querySelector("a");
      if (homeLink) {
        homeLink.textContent = "Home";
        // Mark active when we're on the home page (intro.html with no path).
        var path = window.location.pathname;
        if (path.endsWith("/intro.html") ||
            path.endsWith("/index.html") ||
            path.endsWith("/")) {
          homeLink.classList.add("current");
          homeHeading.classList.add("current");
        }
      }
      homeHeading.classList.add("sy-globaltoc-home");
    }

    // For every <li class="toctree-l1"> that has a child <ul>, add the
    // ECE-315-style <details>/<summary> chevron wrapper.
    var items = nav.querySelectorAll("li.toctree-l1");
    items.forEach(function (li) {
      // Skip if already shimmed.
      if (li.classList.contains("has-children") ||
          li.querySelector(":scope > details")) {
        return;
      }

      // Direct child <ul>?
      var ul = null;
      for (var i = 0; i < li.children.length; i++) {
        if (li.children[i].tagName === "UL") { ul = li.children[i]; break; }
      }
      if (!ul) return;  // leaf node — no toggle needed

      var details = document.createElement("details");
      // Branches containing the current page open by default.
      if (li.classList.contains("current") ||
          li.classList.contains("active") ||
          ul.querySelector(".current")) {
        details.open = true;
      }

      var summary = document.createElement("summary");
      summary.innerHTML =
        '<span class="toctree-toggle" role="presentation">' +
          '<i class="fa-solid fa-chevron-down"></i>' +
        '</span>';

      // Move the <ul> into the <details>; append <summary> first so the
      // chevron sits BEFORE the moved-in <ul>.
      details.appendChild(summary);
      details.appendChild(ul);
      li.appendChild(details);
      li.classList.add("has-children");
    });

    // Tag the active branch so styling matches sphinx-book-theme.
    var activeLink = nav.querySelector("a.current");
    if (activeLink) {
      var activeLi = activeLink.closest("li.toctree-l1");
      if (activeLi) activeLi.classList.add("current", "active");
    }

    // Classify each l2 link by title and prepend an inline SVG glyph
    // sized to inherit currentColor. Read, Flashcards, and Demo each
    // get a distinct shape; everything else is left bare.
    var ICONS = {
      reading:    '<svg class="sy-icon" viewBox="0 0 14 14" aria-hidden="true">' +
                    '<path d="M2 2.5 H6 A1.5 1.5 0 0 1 7 4 V12 H2.5 A.5 .5 0 0 1 2 11.5 Z" ' +
                    'fill="none" stroke="currentColor" stroke-width="1.2"/>' +
                    '<path d="M12 2.5 H8 A1.5 1.5 0 0 0 7 4 V12 H11.5 A.5 .5 0 0 0 12 11.5 Z" ' +
                    'fill="none" stroke="currentColor" stroke-width="1.2"/>' +
                  '</svg>',
      flashcards: '<svg class="sy-icon" viewBox="0 0 14 14" aria-hidden="true">' +
                    '<rect x="3" y="4" width="8" height="7" rx="1" ' +
                    'fill="none" stroke="currentColor" stroke-width="1.2"/>' +
                    '<rect x="4.5" y="2.5" width="8" height="7" rx="1" ' +
                    'fill="none" stroke="currentColor" stroke-width="1.2"/>' +
                  '</svg>',
      slides:     '<svg class="sy-icon" viewBox="0 0 14 14" aria-hidden="true">' +
                    '<rect x="2" y="3" width="10" height="7" rx="1" ' +
                    'fill="none" stroke="currentColor" stroke-width="1.2"/>' +
                    '<path d="M5.5 12 H8.5" stroke="currentColor" ' +
                    'stroke-width="1.2" stroke-linecap="round"/>' +
                    '<path d="M7 10 V12" stroke="currentColor" stroke-width="1.2"/>' +
                  '</svg>',
      practice:   '<svg class="sy-icon" viewBox="0 0 14 14" aria-hidden="true">' +
                    '<path d="M3 2.5 H9 L11 4.5 V11.5 A.5 .5 0 0 1 10.5 12 H3 ' +
                    'A.5 .5 0 0 1 2.5 11.5 V3 A.5 .5 0 0 1 3 2.5 Z" ' +
                    'fill="none" stroke="currentColor" stroke-width="1.2"/>' +
                    '<path d="M5 7.5 L6.5 9 L9 6" fill="none" stroke="currentColor" ' +
                    'stroke-width="1.2" stroke-linecap="round" stroke-linejoin="round"/>' +
                  '</svg>',
    };
    // ECE 215 lesson pages are Reading / Flashcards / Slides / Practice Problems.
    // (The upstream ECE 495 shim classified Demo and Pre-flight instead; this
    // course has neither.)
    function classifyKind(text) {
      var t = text.trim();
      if (/^Reading\b/i.test(t))            return "reading";
      if (/^Flashcards\b/i.test(t))         return "flashcards";
      if (/^Slides\b/i.test(t))             return "slides";
      if (/^Practice\b/i.test(t))           return "practice";
      return null;
    }
    nav.querySelectorAll("li.toctree-l2").forEach(function (li) {
      var a = li.querySelector(":scope > a");
      if (!a) return;
      if (a.querySelector(".sy-icon")) return;  // already iconed
      var kind = classifyKind(a.textContent);
      if (!kind) return;
      a.insertAdjacentHTML("afterbegin", ICONS[kind]);
      li.classList.add("sy-l2-" + kind);
    });
  }

  // Inject a "Block N · Page" breadcrumb above the article H1 on every
  // interior page. Derives the labels from the active TOC node so the
  // sidebar and breadcrumb stay in sync without a per-page front-matter.
  function injectBreadcrumb() {
    var nav = document.querySelector(".sy-globaltoc");
    if (!nav) return;

    var article = document.querySelector(".bd-article");
    if (!article) return;

    // Don't double-inject if the shim runs twice (defensive).
    if (article.querySelector(":scope > .sy-breadcrumb")) return;

    var path = window.location.pathname;
    // Skip the home page (intro.html / index at the book root).
    if (path.endsWith("/intro.html") || path.endsWith("/index.html") ||
        path.endsWith("/")) {
      return;
    }

    var activeLink = nav.querySelector("a.current");
    if (!activeLink) return;
    var pageTitle = activeLink.textContent.trim();

    // Part caption ("Block 1", "Project", ...): the previous
    // <p class="caption"> sibling of the closest UL above this LI.
    var partName = null;
    var l1 = activeLink.closest("li.toctree-l1");
    if (l1) {
      var ul = l1.parentElement;  // <ul>
      var sib = ul && ul.previousElementSibling;
      while (sib && !(sib.tagName === "P" && sib.classList.contains("caption"))) {
        sib = sib.previousElementSibling;
      }
      if (sib) partName = sib.textContent.trim();
    }

    if (!partName) return;

    // If the link IS the part overview ("Block N overview"), the
    // breadcrumb would just repeat the part name twice. Collapse it.
    var crumb = document.createElement("p");
    crumb.className = "sy-breadcrumb";
    if (pageTitle.toLowerCase() === partName.toLowerCase() + " overview" ||
        pageTitle.toLowerCase() === partName.toLowerCase()) {
      crumb.textContent = partName;
    } else {
      crumb.innerHTML = partName +
        ' <span class="sep">·</span> ' +
        pageTitle.replace(/^Demo:\s*/, "Demo · ");
    }

    // Insert before the first child so it sits above the H1.
    article.insertBefore(crumb, article.firstChild);
  }

  // Remove the dark-mode toggle button entirely so users cannot switch
  // even if the CSS hide rule loses to a higher-specificity rule.
  function removeThemeSwitchButton() {
    document.querySelectorAll(
      'button.theme-switch-button, .theme-switch-button'
    ).forEach(function (el) {
      el.parentNode && el.parentNode.removeChild(el);
    });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", function () {
      removeThemeSwitchButton();
      shimSidebar();
      injectBreadcrumb();
    });
  } else {
    removeThemeSwitchButton();
    shimSidebar();
    injectBreadcrumb();
  }
})();
