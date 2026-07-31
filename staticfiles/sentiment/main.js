document.addEventListener('DOMContentLoaded', function () {

  /* ---------- textarea char counter ---------- */
  var textarea = document.getElementById('review-text');
  var charCount = document.getElementById('char-count');
  function updateCharCount() {
    if (!textarea || !charCount) return;
    var n = textarea.value.length;
    charCount.textContent = n + (n === 1 ? ' character' : ' characters');
  }
  if (textarea) {
    updateCharCount();
    textarea.addEventListener('input', updateCharCount);
  }

  /* ---------- submit button loading state ---------- */
  var form = document.getElementById('analyze-form');
  var runBtn = document.getElementById('run-btn');
  if (form && runBtn) {
    form.addEventListener('submit', function () {
      if (!textarea || !textarea.value.trim()) return;
      runBtn.disabled = true;
      runBtn.innerHTML = '<span class="dot"></span> Analyzing…';
    });
  }

  /* ---------- gauge: ticks + animated arc + number ---------- */
  var ticksGroup = document.getElementById('gauge-ticks');
  if (ticksGroup) {
    var cx = 100, cy = 100, rOuter = 90, rInner = 80;
    for (var i = 0; i <= 10; i++) {
      var angle = Math.PI - (i / 10) * Math.PI; // 180deg -> 0deg
      var x1 = cx + rInner * Math.cos(angle);
      var y1 = cy - rInner * Math.sin(angle);
      var x2 = cx + rOuter * Math.cos(angle);
      var y2 = cy - rOuter * Math.sin(angle);
      var line = document.createElementNS('http://www.w3.org/2000/svg', 'line');
      line.setAttribute('x1', x1.toFixed(1));
      line.setAttribute('y1', y1.toFixed(1));
      line.setAttribute('x2', x2.toFixed(1));
      line.setAttribute('y2', y2.toFixed(1));
      line.setAttribute('stroke', '#D9DBD2');
      line.setAttribute('stroke-width', '2');
      ticksGroup.appendChild(line);
    }
  }

  if (window.__RESULT__) {
    var confidence = Math.max(0, Math.min(100, Number(window.__RESULT__.confidence) || 0));
    var arcLength = 251.3; 
    var fillPath = document.getElementById('gauge-fill');
    var gaugeNumber = document.getElementById('gauge-number');

    requestAnimationFrame(function () {
      if (fillPath) {
        fillPath.style.transition = 'stroke-dashoffset 1.1s cubic-bezier(.2,.8,.2,1)';
        fillPath.setAttribute('stroke-dashoffset', String(arcLength * (1 - confidence / 100)));
      }
    });

    if (gaugeNumber) {
      animateNumber(gaugeNumber, 0, confidence, 1100, function (v) {
        return Math.round(v) + '%';
      });
    }
  }

  /* ---------- probability bars ---------- */
  document.querySelectorAll('.prob-fill').forEach(function (el) {
    var target = parseFloat(el.getAttribute('data-target')) || 0;
    requestAnimationFrame(function () {
      el.style.width = Math.max(0, Math.min(100, target)) + '%';
    });
  });

  /* ---------- stat counters ---------- */
  document.querySelectorAll('.stat-tile .num[data-count]').forEach(function (el) {
    var target = parseFloat(el.getAttribute('data-count')) || 0;
    animateNumber(el, 0, target, 900, function (v) { return Math.round(v); });
  });

  function animateNumber(el, from, to, duration, formatter) {
    var start = null;
    function step(ts) {
      if (start === null) start = ts;
      var progress = Math.min((ts - start) / duration, 1);
      var eased = 1 - Math.pow(1 - progress, 3); 
      var value = from + (to - from) * eased;
      el.textContent = formatter(value);
      if (progress < 1) requestAnimationFrame(step);
    }
    requestAnimationFrame(step);
  }

});

const clearBtn = document.getElementById("clear-btn");

if (clearBtn) {
    clearBtn.addEventListener("click", function () {
        window.location.href = "/";
    });
}
console.log("main.js loaded");