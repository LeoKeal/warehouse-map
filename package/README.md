# 仓库库位看板

基于浏览器的仓库库位可视化看板，支持 Excel 数据导入、货架可视化、平面图视图、库存告警等功能。

## 快速启动

### 方式一：使用 server.py（推荐）

需要 Python 3，已测试 Python 3.14。

```bash
cd /path/to/warehouse-map/package
python server.py
```

然后浏览器打开 http://localhost:9090/

### 方式二：使用 http.server

```bash
cd /path/to/warehouse-map/package
python -m http.server 9090 --bind 0.0.0.0
```

**注意**：方式二无法保存 data.json 到服务器，仅适合临时查看。

## 数据导入

打开网页后，点击"上传 Excel 文件"，选择 .xlsx 或 .xls 格式的库存数据文件。

**Excel 表头要求（大小写不敏感）：**

| 列名 | 说明 | 必填 |
|------|------|------|
| 库位编码 | 格式如 A-1L-P1（货架-层-位） | ✅ |
| 料号 | 物料编号 | ✅ |
| 物料名称 | 物料名称 | 建议 |
| 规格型号 | 规格 | 建议 |
| 可用量 | 当前库存数量 | ✅ |
| 单位 | PCS/KG 等 | 建议 |
| 安全库存 | 低于此数量时告警 | 选填 |
| 备注 | 备注信息 | 选填 |

## 任务计划程序配置（Windows）

将服务设为开机自启动，避免服务器重启后手动启动。

### 创建任务

1. 打开"任务计划程序"（taskschd.msc）
2. 创建基本任务
3. 任务名称：如 `仓库看板服务`
4. 触发器：选择"计算机启动时"
5. 操作：选择"启动程序"

### 任务参数

| 设置项 | 值 |
|--------|-----|
| **程序或脚本** | `C:\Users\Administrator\AppData\Local\Programs\Python\Python314\python.exe` |
| **添加参数(可选)** | `server.py` |
| **起始位置(可选)** | `F:\HTML\package`（server.py 所在目录） |

### 完整配置示例

```
程序或脚本: C:\Users\Administrator\AppData\Local\Programs\Python\Python314\python.exe
添加参数: server.py
起始位置: F:\HTML\package
```

### 注意事项

- 确认 Python 安装路径正确（路径因安装位置不同可能有差异）
- 确保任务以有权限访问目标文件夹的账户运行（如 Administrator）
- 可在"常规"标签页勾选"使用最高权限运行"
- 端口默认为 9090，如需修改请编辑 server.py 中的 `PORT` 变量

## 文件说明

```
package/
├── server.py          # HTTP 服务器（必选）
├── index.html         # 主页面
├── map.svg            # 仓库平面图
├── lib/
│   └── xlsx.full.min.js   # Excel 解析库
├── uploads/           # 服务器本地 Excel 文件存放目录
├── data.json          # 自动生成，保存解析后的数据
└── package/           # 独立部署包（静态文件）
    ├── index.html
    ├── map.svg
    └── images/        # 物料图片目录
```

## 浏览器兼容性

推荐使用 Chrome、Edge、Firefox 等现代浏览器。
