/* ==========================================================================
   DevCarnival — hero frame-sequence scrubber + page chrome
   Vanilla JS. No modules, no imports, no build step.

   The hero is a 350vh scroll track with a position:sticky canvas stage.
   Scroll progress through that track maps linearly onto the frame index;
   a requestAnimationFrame loop eases the drawn index toward the scroll
   target so scrubbing never snaps.
   ========================================================================== */

(function () {
  'use strict';

  /* --- config ----------------------------------------------------------- */

  // Frame count + base paths come from data attributes on the hero so Hugo owns
  // them (relURL keeps this working under a subpath baseURL). Regenerate the
  // sequence with tools/build-frames.py if the count changes.
  var FRAME_COUNT = 260;
  var PATH_FULL = 'frames/dc-';
  var PATH_SMALL = 'frames-sm/dc-';
  var EXT = '.webp';

  var EASE = 0.16;          // index lerp per frame — lower is smoother/laggier
  var CONCURRENCY = 8;      // parallel decodes
  var MAX_BACKING_PX = 1600; // frames are 1280px wide; no point drawing bigger

  // The renderer stamped a badge into the lower right of every footage frame.
  // Re-rendering 520 files to drop it isn't worth it, so the brand tile covers
  // it instead. This is the badge's box as a fraction of the source frame —
  // measured off the averaged sequence, and identical in both frame sets.
  var BUG_BOX = { u0: 0.8875, u1: 0.9250, v0: 0.8000, v1: 0.8667 };
  var BUG_PAD = 10;         // css px of cover around the box
  var BUG_MIN = 68;         // floor: below this the monogram stops reading
  var BUG_IN_END = 0.018;   // slide-in lands here — see placeBug()

  /* --- dom -------------------------------------------------------------- */

  var hero = document.querySelector('[data-dc-hero]');
  var nav = document.querySelector('[data-dc-nav]');

  bindNav();
  bindForm();
  bindTheme();

  if (!hero) return;

  FRAME_COUNT = parseInt(hero.getAttribute('data-count'), 10) || FRAME_COUNT;
  PATH_FULL = hero.getAttribute('data-frames') || PATH_FULL;
  PATH_SMALL = hero.getAttribute('data-frames-sm') || PATH_SMALL;

  var canvas = hero.querySelector('[data-dc-canvas]');
  var poster = hero.querySelector('[data-dc-poster]');
  var bug = hero.querySelector('[data-dc-bug]');
  var loader = hero.querySelector('[data-dc-loader]');
  var bar = hero.querySelector('[data-dc-progress-bar]');
  var cue = hero.querySelector('[data-dc-cue]');
  var beats = [].slice.call(hero.querySelectorAll('[data-dc-beat]')).map(function (el) {
    var start = parseFloat(el.getAttribute('data-start')) || 0;
    var end = parseFloat(el.getAttribute('data-end'));
    return {
      el: el,
      start: start,
      end: isNaN(end) ? 1 : end,
      // hold the first/last beat open at the extremes instead of fading to nothing
      holdIn: start <= 0.001,
      holdOut: (isNaN(end) ? 1 : end) >= 0.999,
      shown: -1
    };
  });

  /* --- reduced motion: bypass the scrub entirely ------------------------ */

  var reduceQuery = window.matchMedia('(prefers-reduced-motion: reduce)');
  var running = false;

  function goStatic() {
    running = false;
    hero.classList.add('dc-hero--static');
    if (poster && !poster.getAttribute('src')) {
      poster.setAttribute('src', poster.getAttribute('data-src'));
    }
    if (loader) loader.hidden = true;
    beats.forEach(function (b) {
      b.el.classList.add('is-on');
      b.el.style.opacity = '';
    });
  }

  if (reduceQuery.matches) {
    goStatic();
  } else {
    start();
  }

  // honour a mid-session preference flip
  if (reduceQuery.addEventListener) {
    reduceQuery.addEventListener('change', function (e) {
      if (e.matches) goStatic();
    });
  }

  /* ===================================================================== */

  function start() {
    // The markup ships in the static/no-JS state; take over the hero here.
    hero.classList.remove('dc-hero--static');

    var ctx = canvas.getContext('2d', { alpha: false });
    var base = pickFrameSet();
    var frames = new Array(FRAME_COUNT);
    var loadedCount = 0;
    var firstPainted = false;

    var current = 0;
    var target = 0;
    var lastDrawn = -1;
    var lastProgress = -1;

    var frameRatio = 16 / 9;  // refined off the first frame that lands
    var bugHide = 0;          // px of translate that parks the tile off-stage

    running = true;
    sizeCanvas();
    preload();
    requestAnimationFrame(tick);

    window.addEventListener('resize', onResize, { passive: true });
    window.addEventListener('orientationchange', onResize, { passive: true });

    /* --- asset loading ------------------------------------------------- */

    function pickFrameSet() {
      var dpr = window.devicePixelRatio || 1;
      var need = Math.min(window.innerWidth, window.innerHeight * (16 / 9)) * dpr;
      // narrow/low-dpr viewports get the 768px set (~6.5MB instead of ~12MB)
      return need > 900 ? PATH_FULL : PATH_SMALL;
    }

    function srcFor(i) {
      return base + pad(i + 1) + EXT;
    }

    function pad(n) {
      return n < 10 ? '000' + n : n < 100 ? '00' + n : n < 1000 ? '0' + n : '' + n;
    }

    // Load order: coarse strided passes first, so the whole runway is
    // scrubbable (at low temporal resolution) long before every frame lands.
    function loadOrder() {
      var order = [];
      var seen = new Uint8Array(FRAME_COUNT);
      [16, 8, 4, 2, 1].forEach(function (step) {
        for (var i = 0; i < FRAME_COUNT; i += step) {
          if (!seen[i]) { seen[i] = 1; order.push(i); }
        }
      });
      return order;
    }

    function preload() {
      var queue = loadOrder();

      // Browsers restore scroll position on reload, so the visitor may start
      // anywhere in the runway. Paint where they actually are first, then let
      // the coarse-to-fine passes fill in the rest of the sequence.
      var here = Math.round(progress() * (FRAME_COUNT - 1));
      if (here > 0) {
        var local = [];
        for (var d = 0; d <= 6; d++) {
          if (here - d >= 0) local.push(here - d);
          if (d && here + d < FRAME_COUNT) local.push(here + d);
        }
        queue = local.concat(queue.filter(function (i) {
          return local.indexOf(i) === -1;
        }));
      }

      var cursor = 0;

      function next() {
        if (cursor >= queue.length) return;
        var i = queue[cursor++];
        decodeFrame(srcFor(i))
          .then(function (img) {
            frames[i] = img;
            loadedCount++;
            report();
            if (!firstPainted) { firstPainted = true; lastDrawn = -1; }
          })
          .catch(function () { /* a dropped frame just falls back to a neighbour */ })
          .then(next);
      }

      for (var w = 0; w < CONCURRENCY; w++) next();
    }

    // Decoding happens off the main thread: HTMLImageElement.decode() hands the
    // work to the browser's decoder and resolves when the bitmap is ready to
    // draw, while letting the UA own eviction (260 retained ImageBitmaps would
    // be ~1GB of pixels).
    function decodeFrame(src) {
      return new Promise(function (resolve, reject) {
        var img = new Image();
        img.decoding = 'async';
        img.src = src;

        if (img.decode) {
          img.decode().then(function () { resolve(img); }, function () {
            // Safari can reject decode() on a perfectly good image; fall back.
            if (img.complete && img.naturalWidth) resolve(img);
            else reject(new Error(src));
          });
        } else {
          img.onload = function () { resolve(img); };
          img.onerror = function () { reject(new Error(src)); };
        }
      });
    }

    function report() {
      if (!loader) return;
      var pct = Math.round((loadedCount / FRAME_COUNT) * 100);
      loader.textContent = 'Lighting up the grounds · ' + pct + '%';
      if (pct >= 100) {
        loader.style.opacity = '0';
        window.setTimeout(function () { loader.hidden = true; }, 450);
      }
    }

    /* --- geometry ------------------------------------------------------ */

    function sizeCanvas() {
      var rect = canvas.getBoundingClientRect();
      var dpr = Math.min(window.devicePixelRatio || 1, 2);
      var w = Math.min(Math.round(rect.width * dpr), MAX_BACKING_PX);
      var h = Math.round(w * (rect.height / Math.max(rect.width, 1)));
      if (canvas.width !== w || canvas.height !== h) {
        canvas.width = w;
        canvas.height = h;
        lastDrawn = -1;
      }
      placeBug();
    }

    // Put the brand tile on the badge. drawCover() crops the source's long axis
    // symmetrically about the centre, so one normalised axis maps straight
    // through and the other scales about .5 by the aspect mismatch — invert that
    // and the tile tracks the badge at every viewport. Because the crop only
    // ever pushes the badge further out of frame, never inward, a tile sized off
    // the same maths cannot end up short of it.
    function placeBug() {
      if (!bug) return;
      var rect = canvas.getBoundingClientRect();
      var w = rect.width;
      var h = rect.height;
      if (!w || !h) return;

      var view = w / h;
      var kx = frameRatio > view ? frameRatio / view : 1;
      var ky = frameRatio > view ? 1 : view / frameRatio;

      var x0 = (0.5 + (BUG_BOX.u0 - 0.5) * kx) * w;
      var x1 = (0.5 + (BUG_BOX.u1 - 0.5) * kx) * w;
      var y0 = (0.5 + (BUG_BOX.v0 - 0.5) * ky) * h;
      var y1 = (0.5 + (BUG_BOX.v1 - 0.5) * ky) * h;

      // A tall viewport (phones, tablets in portrait) crops the badge clean off
      // the frame. Nothing to cover, and a tile stranded in the corner behind
      // the stacked copy just reads as an artifact — so sit it out.
      if (x0 >= w || y0 >= h) {
        bug.style.visibility = 'hidden';
        return;
      }
      bug.style.visibility = '';

      var side = Math.round(Math.max(x1 - x0, y1 - y0, BUG_MIN - BUG_PAD * 2) + BUG_PAD * 2);

      // Partly off-frame is still partly visible, so clamp the tile into the
      // stage rather than letting it hang over the edge. It is wider than the
      // badge, so the clamp can never slide it off what it is covering.
      var left = clamp(Math.round((x0 + x1 - side) / 2), 0, Math.round(w - side));
      var top = clamp(Math.round((y0 + y1 - side) / 2), 0, Math.round(h - side));

      bug.style.width = bug.style.height = side + 'px';
      bug.style.left = left + 'px';
      bug.style.top = top + 'px';
      bugHide = Math.ceil(w - left) + 2;   // clears the stage's overflow edge
      slideBug(progress());
    }

    // Scroll-driven slide from the right. It has to land early: frames 1-20 are
    // the synthetic lead-in that cross-dissolves into the footage, so the badge
    // is still under ~10% opacity when the tile arrives, and fully covered
    // before the footage reads at all.
    function slideBug(p) {
      if (!bug || !bugHide) return;
      var t = clamp(p / BUG_IN_END, 0, 1);
      var eased = 1 - Math.pow(1 - t, 3);
      bug.style.transform =
        'translate3d(' + ((1 - eased) * bugHide).toFixed(1) + 'px, 0, 0)';
    }

    var resizeTimer;
    function onResize() {
      window.clearTimeout(resizeTimer);
      resizeTimer = window.setTimeout(function () {
        sizeCanvas();
      }, 120);
    }

    /* --- the loop ------------------------------------------------------ */

    function progress() {
      var rect = hero.getBoundingClientRect();
      var travel = hero.offsetHeight - window.innerHeight;
      if (travel <= 0) return 0;
      return clamp(-rect.top / travel, 0, 1);
    }

    function tick() {
      if (!running) return;

      var p = progress();
      target = p * (FRAME_COUNT - 1);

      // ease toward the scroll target, then settle exactly on it
      current += (target - current) * EASE;
      if (Math.abs(target - current) < 0.02) current = target;

      var idx = Math.round(current);
      if (idx !== lastDrawn) {
        var img = nearestLoaded(idx);
        if (img) {
          drawCover(img);
          lastDrawn = idx;
        }
      }

      if (p !== lastProgress) {
        paintChrome(p);
        lastProgress = p;
      }

      requestAnimationFrame(tick);
    }

    // Never leave the canvas empty: fall back to the closest frame that has
    // landed, however far away it is.
    function nearestLoaded(idx) {
      if (frames[idx]) return frames[idx];
      for (var d = 1; d < FRAME_COUNT; d++) {
        if (idx - d >= 0 && frames[idx - d]) return frames[idx - d];
        if (idx + d < FRAME_COUNT && frames[idx + d]) return frames[idx + d];
      }
      return null;
    }

    function drawCover(img) {
      var cw = canvas.width;
      var ch = canvas.height;
      if (!cw || !ch) return;

      var iw = img.naturalWidth || img.width;
      var ih = img.naturalHeight || img.height;
      var canvasRatio = cw / ch;

      // the tile's placement depends on the source aspect — trust the pixels
      // over the assumed 16:9 once a frame has actually landed
      if (iw && ih && Math.abs(iw / ih - frameRatio) > 0.001) {
        frameRatio = iw / ih;
        placeBug();
      }

      var sw, sh, sx, sy;

      if (iw / ih > canvasRatio) {
        sh = ih;
        sw = sh * canvasRatio;
        sx = (iw - sw) / 2;
        sy = 0;
      } else {
        sw = iw;
        sh = sw / canvasRatio;
        sx = 0;
        sy = (ih - sh) / 2;
      }
      ctx.drawImage(img, sx, sy, sw, sh, 0, 0, cw, ch);
    }

    /* --- overlays + progress hairline ---------------------------------- */

    function paintChrome(p) {
      if (bar) bar.style.width = (p * 100).toFixed(2) + '%';
      if (cue) cue.classList.toggle('is-gone', p > 0.02);
      slideBug(p);

      for (var i = 0; i < beats.length; i++) {
        var b = beats[i];
        var fade = 0.035;
        var into = b.holdIn ? 1 : (p - b.start) / fade;
        var outOf = b.holdOut ? 1 : (b.end - p) / fade;
        var op = clamp(Math.min(into, outOf), 0, 1);

        var rounded = Math.round(op * 50); // avoid churning style on every frame
        if (rounded !== b.shown) {
          b.el.style.opacity = op;
          b.el.classList.toggle('is-on', op > 0.02);
          b.el.setAttribute('aria-hidden', op > 0.02 ? 'false' : 'true');
          b.shown = rounded;
        }
      }
    }
  }

  /* --- page chrome ------------------------------------------------------ */

  function bindNav() {
    if (!nav) return;
    // solid + neon hairline once the hero is behind us
    var threshold = function () {
      return hero ? Math.max(hero.offsetHeight - window.innerHeight * 0.9, 80) : 80;
    };
    var stuck = false;

    function onScroll() {
      var should = window.pageYOffset > threshold();
      if (should !== stuck) {
        stuck = should;
        nav.classList.toggle('is-stuck', stuck);
      }
    }
    window.addEventListener('scroll', onScroll, { passive: true });
    onScroll();
  }

  function bindForm() {
    var form = document.querySelector('[data-dc-form]');
    if (!form) return;
    var notice = form.querySelector('[data-dc-notice]');
    form.addEventListener('submit', function (e) {
      // No endpoint is wired yet — see the comment in layouts/index.html.
      if (!form.getAttribute('action')) {
        e.preventDefault();
        if (notice) {
          notice.hidden = false;
          notice.focus();
        }
      }
    });
  }

  function bindTheme() {
    var toggle = document.querySelector('[data-dc-theme-toggle]');
    if (!toggle) return;

    var root = document.documentElement;
    var metaColor = document.querySelector('meta[name="theme-color"]');

    function reflect(theme) {
      var light = theme === 'light';
      toggle.setAttribute('aria-pressed', String(light));
      toggle.setAttribute('aria-label', light ? 'Switch to dark theme' : 'Switch to light theme');
      if (metaColor) metaColor.setAttribute('content', light ? '#f7f7f9' : '#121214');
    }

    reflect(root.getAttribute('data-bs-theme'));

    toggle.addEventListener('click', function () {
      var next = root.getAttribute('data-bs-theme') === 'light' ? 'dark' : 'light';
      root.setAttribute('data-bs-theme', next);
      reflect(next);
      try { localStorage.setItem('dc-theme', next); } catch (e) { /* privacy mode */ }
    });

    // honour a mid-session OS preference flip, same as prefers-reduced-motion
    // above — but only until the visitor makes an explicit choice of their own
    var schemeQuery = window.matchMedia('(prefers-color-scheme: light)');
    if (schemeQuery.addEventListener) {
      schemeQuery.addEventListener('change', function (e) {
        var stored;
        try { stored = localStorage.getItem('dc-theme'); } catch (err) { /* privacy mode */ }
        if (stored) return;
        var next = e.matches ? 'light' : 'dark';
        root.setAttribute('data-bs-theme', next);
        reflect(next);
      });
    }
  }

  function clamp(v, lo, hi) {
    return v < lo ? lo : v > hi ? hi : v;
  }
}());
