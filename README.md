# A股行业拥挤度热力图

基于申万一级行业成交额数据，计算各行业的"拥挤度"（60日滚动分位值），并以热力图形式可视化。

## 原理

- 每日计算各行业成交额占全市场总成交额的比例
- 对每个行业，计算当日占比在过去 **60 个交易日**内的分位值（0-100），即为**拥挤度**
- 拥挤度越高，说明该行业近期资金关注度越高，处于相对拥挤状态

## 依赖

- Python 3.11+
- akshare（数据获取）
- pandas（数据处理）
- jinja2（HTML 模板渲染）

## 安装

```bash
python -m venv venv
venv\Scripts\pip install akshare pandas jinja2
```

## 使用

```bash
venv\Scripts\python main.py
```

运行后自动生成两个文件：

- `data.json` — 结构化数据（日期、行业、拥挤度值）
- `index.html` — 独立可打开的 ECharts 热力图页面

## 热力图说明

| 维度 | 内容 |
|------|------|
| 横轴 | 日期（最近 90 个交易日） |
| 纵轴 | 申万一级行业（31 个） |
| 颜色 | 绿（0）→ 黄（50）→ 红（100），越红越拥挤 |
| 交互 | 鼠标悬停查看具体拥挤度数值 |

## 目录结构

```
hotpicture/
├── main.py          # 主入口
├── template.html    # 热力图模板
├── data.json        # 输出数据
├── index.html       # 输出页面
└── README.md
```
