# -*- coding: utf-8 -*-
# 自动生成 index.html 到 E:\VScode\HTML\index.html
import os

output_path = r"E:\VScode\HTML\index.html"

html_content = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>仓库库位看板</title>
  <style>
    *{margin:0;padding:0;box-sizing:border-box}
    body{background:#0a0e1a;font-family:Microsoft YaHei,PingFang SC,sans-serif;height:100vh;display:flex;flex-direction:column;overflow:hidden;user-select:none}
    header{background:#0d1525;border-bottom:2px solid #1a3a5c;padding:12px 24px;display:flex;align-items:center;justify-content:space-between;flex-shrink:0}
    h1{font-size:18px;color:#4cc9f0;font-weight:900}
    .stats{display:flex;gap:20px;font-size:13px;color:#666}
    .stats span{color:#4cc9f0;font-weight:bold}
    .btn{background:#e94560;color:#fff;border:none;padding:7px 18px;border-radius:8px;cursor:pointer;font-size:13px;font-weight:bold}
    .btn:hover{background:#ff6b8a}
    .main{flex:1;display:flex;overflow:hidden}
    .board{flex:1;display:flex;flex-direction:column;align-items:center;justify-content:center;padding:20px;gap:12px;overflow:auto}
    .shelf{background:linear-gradient(180deg,#0d1f38,#0a1830);border:2px solid #4cc9f0;border-radius:12px;padding:16px 20px;cursor:pointer;transition:all .2s;display:flex;flex-direction:column;align-items:center;gap:6px;min-width:300px}
    .shelf:hover{border-color:#e94560;background:linear-gradient(180deg,#1a0a28,#150a20);transform:scale(1.02);box-shadow:0 8px 24px rgba(233,69,96,.2)}
    .shelf-title{font-size:20px;font-weight:900;color:#4cc9f0;letter-spacing:2px}
    .shelf-sub{font-size:12px;color:#4a6080}
    .shelf-layers{font-size:11px;color:#2a4a6a;margin-top:4px}
    .layer-row{display:flex;gap:6px;flex-wrap:wrap;justify-content:center}
    .mini-slot{width:28px;height:20px;border-radius:3px;border:1px solid;display:flex;align-items:center;justify-content:center;font-size:8px}
    .ms-occ{border-color:#4cc9f0;background:#0a2040;color:#4cc9f0}
    .ms-empty{border-color:#1e2d3d;background:#111827;color:#334}
    .ms-low{border-color:#f4d03f;background:#2a2200;color:#f4d03f}
    .ms-crit{border-color:#e74c3c;background:#2a0000;color:#e74c3c;animation:pulse 1.5s infinite}
    @keyframes pulse{0%,100%{box-shadow:0 0 0 rgba(231,76,60,0)}50%{box-shadow:0 0 8px rgba(231,76,60,.4)}}
    .panel{width:360px;background:#0d1f38;border-left:2px solid #1a3a5c;padding:20px;overflow-y:auto;flex-shrink:0;display:flex;flex-direction:column}
    .panel-title{font-size:15px;color:#4cc9f0;font-weight:900;padding-bottom:12px;border-bottom:1px solid #1a3a5c;margin-bottom:16px}
    .panel-hint{flex:1;display:flex;flex-direction:column;align-items:center;justify-content:center;color:#2a3a5a;font-size:14px;gap:10px;text-align:center}
    .panel-hint-icon{font-size:48px;opacity:.3}
    .layer-list{display:flex;flex-direction:column;gap:8px}
    .layer-card{background:#0a1830;border:1px solid #1a3a5c;border-radius:10px;padding:12px 14px;cursor:pointer;transition:all .2s;margin-bottom:8px}
    .layer-card:hover{border-color:#4cc9f0;background:#0a2040}
    .modal-overlay{position:fixed;inset:0;background:rgba(0,0,0,.7);backdrop-filter:blur(4px);z-index:500;display:none;align-items:center;justify-content:center}
    .modal-overlay.show{display:flex}
    .modal{background:linear-gradient(135deg,#0d1f38,#0a1628);border:2px solid #4cc9f0;border-radius:16px;width:460px;max-width:90vw;box-shadow:0 20px 60px rgba(0,0,0,.6);overflow:hidden}
    .modal-header{background:#0a2040;padding:14px 20px;display:flex;align-items:center;justify-content:space-between;border-bottom:1px solid #1a3a5c}
    .modal-header h2{font-size:16px;color:#4cc9f0;font-weight:900}
    .modal-close{background:none;border:none;color:#888;font-size:22px;cursor:pointer;padding:0;line-height:1}
    .modal-close:hover{color:#e94560}
    .modal-body{padding:18px;display:flex;flex-direction:column;gap:12px}
    .modal-img{width:100%;height:140px;background:#050810;border:1px solid #1a3a5c;border-radius:8px;display:flex;align-items:center;justify-content:center}
    .modal-img img{max-width:100%;max-height:130px;object-fit:contain}
    .modal-img .no-img{color:#2a3a5a;font-size:13px}
    .modal-row{display:flex;gap:12px}
    .modal-label{font-size:11px;color:#4a6080;text-transform:uppercase;letter-spacing:1px;width:56px;flex-shrink:0;padding-top:2px}
    .modal-value{font-size:14px;color:#e0e0e0;font-weight:700;flex:1}
    .modal-value.highlight{color:#4cc9f0;font-size:18px}
    .modal-badge{display:inline-block;padding:3px 12px;border-radius:20px;font-size:12px;font-weight:900}
    .badge-occ{background:#0a2040;color:#4cc9f0;border:1px solid #4cc9f0}
    .badge-empty{background:#1a1a1a;color:#444;border:1px solid #333}
    .badge-low{background:#2a2000;color:#f4d03f;border:1px solid #f4d03f}
    .badge-critical{background:#2a0000;color:#e74c3c;border:1px solid #e74c3c;animation:badge-blink 1.5s infinite}
    @keyframes badge-blink{0%,100%{opacity:1}50%{opacity:.6}}
    .modal-divider{height:1px;background:#0f3460}
    .toast{position:fixed;bottom:24px;left:50%;transform:translateX(-50%) translateY(80px);background:#0d1f38;border:2px solid #4cc9f0;color:#4cc9f0;padding:8px 22px;border-radius:10px;font-size:13px;opacity:0;transition:all .35s;pointer-events:none;z-index:9999}
    .toast.show{transform:translateX(-50%) translateY(0);opacity:1}
    .tip{text-align:center;font-size:11px;color:#2a3a5a;padding:8px}
  </style>
</head>
<body>
<header>
  <h1>&#128230; 仓库库位看板</h1>
  <div class="stats">总库位 <span id="s-total">0</span> · 已占用 <span id="s-occ" style="color:#27ae60">0</span> · 告警 <span id="s-alert" style="color:#e74c3c">0</span></div>
  <button class="btn" onclick="loadData()">&#128260; 刷新数据</button>
</header>
<div class="main">
  <div class="board" id="board">
    <div class="tip">&#128070; 点击货架 → 选择层数 → 点击货位查看详情</div>
    <div class="shelf" id="shelf-a" onclick="showLayers('A')">
      <div class="shelf-title">&#9670; A 区货架</div>
      <div class="shelf-sub">4层 · 每层6个货位</div>
      <div class="shelf-layers">点击进入</div>
      <div class="layer-row" id="shelf-a-preview"></div>
    </div>
  </div>
  <div class="panel">
    <div class="panel-title" id="panelTitle">&#128203; 库位详情</div>
    <div class="panel-hint" id="panelHint"><div class="panel-hint-icon">&#128070;</div><div>点击左侧货架<br>查看层数和货位</div></div>
    <div class="layer-list" id="layerList"></div>
  </div>
</div>
<div class="modal-overlay" id="modalOverlay" onclick="closeModal(event)">
  <div class="modal" onclick="event.stopPropagation()">
    <div class="modal-header">
      <h2 id="modalTitle">&#128230; 货位详情</h2>
      <button class="modal-close" onclick="closeModal()">&#215;</button>
    </div>
    <div class="modal-body">
      <div class="modal-img" id="modalImg"><div class="no-img">暂无图片</div></div>
      <div class="modal-row"><div class="modal-label">库位</div><div class="modal-value highlight" id="m-code">-</div></div>
      <div class="modal-row"><div class="modal-label">物料</div><div class="modal-value" id="m-name">-</div></div>
      <div class="modal-row"><div class="modal-label">规格</div><div class="modal-value" id="m-spec">-</div></div>
      <div class="modal-row"><div class="modal-label">数量</div><div class="modal-value" id="m-qty">-</div></div>
      <div class="modal-row"><div class="modal-label">状态</div><div class="modal-value"><span class="modal-badge" id="m-badge">-</span></div></div>
      <div class="modal-divider"></div>
      <div class="modal-row"><div class="modal-label">备注</div><div class="modal-value" id="m-note" style="font-size:12px;color:#6a8aaa">-</div></div>
    </div>
  </div>
</div>
<div class="toast" id="toast"></div>
<script>
var KC = "\u5EAB\u4F4D\u7F16\u7801";
var KN = "\u7269\u6599\u540D\u79F0";
var KQ = "\u6570\u91CF";
var KS = "\u89C4\u683C\u578B\u53F7";
var KU = "\u5355\u4F4D";
var KI = "\u7269\u6599\u56FE\u7247\u8DEF\u5F84";
var KZ = "\u5907\u6CE8";
var DATA = {};

function loadData() {
  var x = new XMLHttpRequest();
  x.open("GET", "data.json?t=" + Date.now(), true);
  x.onload = function() {
    if (x.status === 200) {
      try {
        var j = JSON.parse(x.responseText);
        DATA = {};
        for (var i = 0; i < j.length; i++) DATA[j[i][KC]] = j[i];
        updateStats();
        renderPreviews();
        showToast("\u2705 \u52A0\u8F7D\u5B8C\u6210\uFF0C\u5171 " + j.length + " \u6761");
      } catch(e) { showToast("\u274C JSON\u89E3\u6790\u9519\u8BEF"); }
    }
  };
  x.onerror = function() { showToast("\u274C \u52A0\u8F7D\u5931\u8D25"); };
  x.send();
}

function getLayerItems(shelf, layer) {
  var p = shelf + "-L" + layer + "-";
  var r = [];
  for (var k in DATA) { if (k.indexOf(p) === 0) r.push(DATA[k]); }
  return r;
}

function calcStats(items) {
  var occ = 0, crit = 0, low = 0;
  for (var i = 0; i < items.length; i++) {
    var q = parseFloat(items[i][KQ]) || 0;
    var n = items[i][KN] || "";
    if (n && q > 0) occ++;
    if (n && q > 0 && q <= 10) crit++;
    if (n && q > 10 && q <= 50) low++;
  }
  return { occ: occ, crit: crit, low: low };
}

function renderPreviews() {
  var el = document.getElementById("shelf-a-preview");
  if (!el) return;
  el.innerHTML = "";
  for (var L = 1; L <= 4; L++) {
    var its = getLayerItems("A", L);
    var st = calcStats(its);
    var cls = st.crit > 0 ? "ms-crit" : st.low > 0 ? "ms-low" : st.occ > 0 ? "ms-occ" : "ms-empty";
    var d = document.createElement("div");
    d.className = "mini-slot " + cls;
    d.textContent = "L" + L;
    d.title = "\u7B2C" + L + "\u5C42\uFF1A" + st.occ + "/" + its.length + " \u5DF2\u5360\u7528";
    el.appendChild(d);
  }
}

function showLayers(shelf) {
  document.getElementById("panelHint").style.display = "none";
  var list = document.getElementById("layerList");
  list.innerHTML = "";
  document.getElementById("panelTitle").textContent = "\uD83D\uDCCB " + shelf + " \u533A\u8D27\u67DC \u00B7 \u9009\u62E9\u5C42\u6570";

  for (var L = 1; L <= 4; L++) {
    var its = getLayerItems(shelf, L);
    if (its.length === 0) {
      // 即使没有数据也显示空层
      its = [];
      for (var pi = 1; pi <= 6; pi++) {
        var c = shelf + "-L" + L + "-P" + (pi < 10 ? "00" + pi : "0" + pi);
        its.push({});
      }
    }
    var st = calcStats(its);

    var card = document.createElement("div");
    card.className = "layer-card";
    card._shelf = shelf;
    card._layer = L;
    card._items = its;
    card._stats = st;

    // 标题
    var titleRow = document.createElement("div");
    titleRow.style.cssText = "display:flex;align-items:center;justify-content:space-between;font-size:13px;font-weight:900;color:#4cc9f0;margin-bottom:8px";

    var titleSp = document.createElement("span");
    titleSp.textContent = "\u7B2C " + L + " \u5C42";

    var cntSp = document.createElement("span");
    cntSp.style.cssText = "font-size:11px;color:#888";
    cntSp.innerHTML = "<span style='color:#27ae60'>" + st.occ + "</span>/" + its.length +
      (st.crit > 0 ? " <span style='color:#e74c3c'>\u26A0\uFE0F" + st.crit + "</span>" : "") +
      (st.low > 0 ? " <span style='color:#f39c12'>\u26A1" + st.low + "</span>" : "");

    titleRow.appendChild(titleSp);
    titleRow.appendChild(cntSp);
    card.appendChild(titleRow);

    // 货位网格
    var grid = document.createElement("div");
    grid.style.cssText = "display:none;flex-wrap:wrap;gap:5px;margin-top:8px";
    card._grid = grid;

    for (var p = 0; p < its.length; p++) {
      var pnum = p + 1;
      var code = shelf + "-L" + L + "-P" + (pnum < 10 ? "00" + pnum : "0" + pnum);
      var item = DATA[code] || its[p];
      var qty = parseFloat(item[KQ]) || 0;
      var name = item[KN] || "";
      var empty = !name || qty === 0;
      var cls = empty ? "ms-empty" : qty <= 10 ? "ms-crit" : qty <= 50 ? "ms-low" : "ms-occ";

      var dot = document.createElement("div");
      dot.style.cssText = "width:26px;height:26px;border-radius:5px;border:1px solid;display:flex;align-items:center;justify-content:center;font-size:8px;cursor:pointer;transition:transform .15s;";
      if (cls === "ms-empty") dot.style.cssText += "border-color:#1e2d3d;background:#111827;color:#334;";
      else if (cls === "ms-crit") dot.style.cssText += "border-color:#e74c3c;background:#2a0000;color:#e74c3c;";
      else if (cls === "ms-low") dot.style.cssText += "border-color:#f4d03f;background:#2a2200;color:#f4d03f;";
      else dot.style.cssText += "border-color:#4cc9f0;background:#0a2040;color:#4cc9f0;";
      dot.textContent = (pnum < 10 ? "0" : "") + pnum;
      dot.title = empty ? code + " \u7A7A" : code + " " + name + " x" + qty;

      dot.onclick = (function(it) {
        return function(e) {
          e.stopPropagation();
          showModal(it);
        };
      })(item);

      dot.onmouseover = function() { this.style.transform = "scale(1.15)"; };
      dot.onmouseout = function() { this.style.transform = "scale(1)"; };

      grid.appendChild(dot);
    }

    card.appendChild(grid);

    card.onclick = function() {
      var g = this._grid;
      g.style.display = g.style.display === "none" ? "flex" : "none";
    };

    list.appendChild(card);
  }
}

function showModal(item) {
  var qty = parseFloat(item[KQ]) || 0;
  var name = item[KN] || "";
  var empty = !name || qty === 0;
  document.getElementById("modalTitle").textContent = "\uD83D\uDCE6 " + (item[KC] || "-");
  document.getElementById("m-code").textContent = item[KC] || "-";
  document.getElementById("m-name").textContent = empty ? "(\u7A7A\u5E93\u4F4D)" : name;
  document.getElementById("m-spec").textContent = item[KS] || "-";
  document.getElementById("m-qty").textContent = empty ? "-" : qty + " " + (item[KU] || "");
  document.getElementById("m-note").textContent = item[KZ] || "\u65E0";
  var badge = document.getElementById("m-badge");
  if (empty) { badge.textContent = "\u7A7A\u5E93\u4F4D"; badge.className = "modal-badge badge-empty"; }
  else if (qty <= 10) { badge.textContent = "\u26A0\uFE0F \u4E25\u91CD\u544A\u8B66"; badge.className = "modal-badge badge-critical"; }
  else if (qty <= 50) { badge.textContent = "\u26A1 \u5E93\u5B58\u4E0D\u8DB3"; badge.className = "modal-badge badge-low"; }
  else { badge.textContent = "\u2705 \u5DF2\u5360\u7528"; badge.className = "modal-badge badge-occ"; }
  var imgPath = item[KI] || "";
  document.getElementById("modalImg").innerHTML = imgPath ? "<img src='" + imgPath + "' />" : "<div class='no-img'>\u6682\u65E0\u56FE\u7247</div>";
  document.getElementById("modalOverlay").classList.add("show");
}

function closeModal(e) {
  if (e && e.target !== e.currentTarget) return;
  document.getElementById("modalOverlay").classList.remove("show");
}

function updateStats() {
  var all = [];
  for (var k in DATA) all.push(DATA[k]);
  var occ = 0, alert = 0;
  for (var i = 0; i < all.length; i++) {
    var q = parseFloat(all[i][KQ]) || 0;
    var n = all[i][KN] || "";
    if (n && q > 0) occ++;
    if (n && q > 0 && q <= 50) alert++;
  }
  document.getElementById("s-total").textContent = all.length;
  document.getElementById("s-occ").textContent = occ;
  document.getElementById("s-alert").textContent = alert;
}

function showToast(msg) {
  var t = document.getElementById("toast");
  t.textContent = msg;
  t.classList.add("show");
  setTimeout(function() { t.classList.remove("show"); }, 3000);
}

document.addEventListener("keydown", function(e) {
  if (e.key === "Escape") closeModal();
});

loadData();
</script>
</body>
</html>
"""

with open(output_path, "w", encoding="utf-8") as f:
    f.write(html_content)

print("OK: " + output_path)
input("\n按回车键退出...")
