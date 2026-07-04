import base64

# Read SVG and encode as base64
with open('package/lib/map.svg', 'rb') as f:
    b64 = base64.b64encode(f.read()).decode()

with open('package/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Find and replace the object-based loading block
start_marker = '  var objEl = document.createElement("object");'
start_idx = content.find(start_marker)
if start_idx == -1:
    print("ERROR: Could not find objEl start")
    exit(1)

# Find the end of the function
end_marker = '\nfunction floorTip(e, letter, total, occ, crit, low) {'
end_idx = content.find(end_marker, start_idx)
if end_idx == -1:
    print("ERROR: Could not find floorTip marker")
    exit(1)

# New code - use single braces only, clean Unicode escapes
new_code = '''  // SVG以base64存储，用atob解码后通过DOMParser解析（file://完全兼容）
  var svgDataB64 = "''' + b64 + '''";
  var svgText = null;
  try {
    svgText = atob(svgDataB64);
  } catch(e) {
    container.innerHTML = '<div style="color:red;padding:20px;">SVG解码失败</div>';
    return;
  }

  var parser = new DOMParser();
  var svgDoc = parser.parseFromString(svgText, "image/svg+xml");
  var svgEl = svgDoc.documentElement;

  svgEl.setAttribute("class", "floor-plan-svg");
  svgEl.style.width = dispW + "px";
  svgEl.style.height = dispH + "px";

  for (var letter in cfg.shelves) {
    var rect = svgEl.querySelector("#shelf-" + letter);
    if (!rect) continue;

    var fill = getShelfFill(letter);
    var stroke = getShelfBorder(letter);
    var stats = getShelfStats(letter);
    var strokeW = (_focusShelf === letter) ? "5" : "3";
    rect.setAttribute("fill", fill);
    rect.setAttribute("stroke", stroke);
    rect.setAttribute("stroke-width", strokeW);
    if (_focusShelf === letter) {
      rect.classList.add("svg-shelf-focus");
      var curX = parseFloat(rect.getAttribute("x")) || 0;
      var curY = parseFloat(rect.getAttribute("y")) || 0;
      var curW = parseFloat(rect.getAttribute("width")) || 100;
      var curH = parseFloat(rect.getAttribute("height")) || 50;
      var focusRect = document.createElementNS('http://www.w3.org/2000/svg', 'rect');
      focusRect.setAttribute('x', curX);
      focusRect.setAttribute('y', curY);
      focusRect.setAttribute('width', curW);
      focusRect.setAttribute('height', curH);
      focusRect.setAttribute('fill', fill);
      focusRect.setAttribute('fill-opacity', '0.5');
      focusRect.setAttribute('stroke', '#ff9900');
      focusRect.setAttribute('stroke-width', '6');
      focusRect.setAttribute('rx', '8');
      focusRect.classList.add('svg-shelf-focus');
      focusRect.style.pointerEvents = 'none';
      var textGroup = svgEl.querySelector('#shelf-text-group-' + letter);
      if (textGroup && textGroup.parentNode) {
        textGroup.parentNode.insertBefore(focusRect, textGroup);
      } else {
        svgEl.appendChild(focusRect);
      }
    } else {
      rect.classList.remove("svg-shelf-focus");
    }

    rect.addEventListener("click", (function(l) { return function() { showLayers(l); }; })(letter));
    rect.addEventListener("mouseover", (function(l, st) { return function(e) { floorTip(e, l, st.total, st.occ, st.crit, st.low); }; })(letter, stats));
    rect.addEventListener("mouseout", floorHideTip);

    var cellId = rect.closest('g[data-cell-id]');
    if (cellId) {
      cellId.style.cursor = 'pointer';
      cellId.addEventListener('click', (function(l) { return function(e) { e.stopPropagation(); showLayers(l); }; })(letter));
    }
  }

  var wrapper = document.createElement("div");
  wrapper.style.position = "relative";
  wrapper.style.display = "block";
  wrapper.style.width = dispW + "px";
  wrapper.style.height = dispH + "px";
  wrapper.style.overflow = "visible";

  var svgWrap = document.createElement("div");
  svgWrap.style.position = "relative";
  svgWrap.style.display = "inline-block";
  svgWrap.style.overflow = "visible";
  svgWrap.style.width = dispW + "px";
  svgWrap.style.height = dispH + "px";
  svgWrap.appendChild(svgEl);
  wrapper.appendChild(svgWrap);

  var hint = document.createElement("div");
  hint.className = "floor-hint";
  hint.style.cssText = "position:absolute;bottom:8px;left:50%;transform:translateX(-50%);pointer-events:none";
  hint.textContent = "";
  svgWrap.appendChild(hint);

  var northArrow = document.createElement("div");
  northArrow.style.cssText = "position:absolute;top:12px;right:14px;width:48px;height:48px;pointer-events:none;opacity:0.85";
  northArrow.innerHTML = '<svg viewBox="0 0 48 48" xmlns="http://www.w3.org/2000/svg" width="48" height="48">' +
    '<circle cx="24" cy="24" r="22" fill="rgba(232,238,245,0.85)" stroke="#1a3a5c" stroke-width="1.5"/>' +
    '<polygon points="24,6 30,38 24,32 18,38" fill="#e94560" stroke="#c03050" stroke-width="1" stroke-linejoin="round"/>' +
    '<text x="24" y="18" text-anchor="middle" font-size="10" font-weight="bold" fill="#1a3a5c" font-family="sans-serif">N</text>' +
    '<text x="24" y="46" text-anchor="middle" font-size="8" fill="#1a3a5c" font-family="sans-serif">\u5317</text>' +
    '</svg>';
  svgWrap.appendChild(northArrow);

  var tip = document.createElement("div");
  tip.id = "floorTip";
  tip.className = "floor-tip";
  tip.style.cssText = "position:absolute;pointer-events:none";
  svgWrap.appendChild(tip);

  container.innerHTML = "";
  container.appendChild(wrapper);
  container.style.display = "flex";
  var board = document.getElementById("board");
  board.style.display = "none";
  var btn = document.getElementById("viewToggleBtn");
  if (btn) btn.textContent = "\u7bb1 \u8d27\u67b6\u89c6\u56fe";
'''

# Replace
content = content[:start_idx] + new_code + content[end_idx:]

with open('package/index.html', 'w', encoding='utf-8') as f:
    f.write(content)

# Verify
with open('package/index.html', 'r', encoding='utf-8') as f:
    c = f.read()
print(f"DOMParser: {'DOMParser' in c}")
print(f"atob: {'atob' in c}")
print(f"objEl: {'objEl' in c}")
print(f"文件大小: {len(c):,} 字节")
