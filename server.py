#!/usr/bin/env python3
"""
仓库看板 HTTP 服务器
- 静态文件服务（index.html, JS, CSS, images 等）
- GET  /data.json  → 返回已有 JSON 数据（不存在返回 404）
- POST /api/save   → 接收前端 JSON 并写入 data.json
"""
import http.server
import json
import os
from urllib.parse import urlparse

PORT = 8080
DATA_FILE = "data.json"


class Handler(http.server.SimpleHTTPRequestHandler):
    def do_POST(self):
        parsed = urlparse(self.path)
        if parsed.path == "/api/save":
            try:
                content_length = int(self.headers.get("Content-Length", 0))
                body = self.rfile.read(content_length)
                data = json.loads(body.decode("utf-8"))
                with open(DATA_FILE, "w", encoding="utf-8") as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
                self.wfile.write(json.dumps({"ok": True}).encode())
                print(f"[已保存] data.json ({len(data)} 条记录)")
            except Exception as e:
                self.send_response(500)
                self.send_header("Content-Type", "application/json")
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
                self.wfile.write(json.dumps({"error": str(e)}).encode())
        else:
            self.send_error(404)

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_GET(self):
        parsed = urlparse(self.path)
        if parsed.path == "/":
            self.path = "/index.html"
        if parsed.path == "/" + DATA_FILE and not os.path.exists(DATA_FILE):
            self.send_error(404)
            return
        return http.server.SimpleHTTPRequestHandler.do_GET(self)


if __name__ == "__main__":
    print(f"仓库看板服务已启动：http://0.0.0.0:{PORT}/")
    print(f"data.json {'已找到，将自动加载' if os.path.exists(DATA_FILE) else '不存在，请上传 Excel 文件'}")
    http.server.HTTPServer(("0.0.0.0", PORT), Handler).serve_forever()
