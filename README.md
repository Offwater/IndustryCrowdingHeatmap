# A股行业拥挤度热力图

基于申万一级行业成交额数据，计算各行业的"拥挤度"（60日滚动分位值），以 ECharts 热力图形式可视化。

## 原理

- 每日计算各行业成交额占全市场总成交额的比例
- 对每个行业，计算当日占比在过去 **60 个交易日**内的滚动分位值（0-100），即为**拥挤度**
- 拥挤度越高，说明该行业近期资金关注度越高，处于相对拥挤状态

## 依赖

- Python 3.11+
- [akshare](https://github.com/akfamily/akshare) — A股行情数据获取
- [pandas](https://pandas.pydata.org/) — 数据处理与滚动分位计算
- [jinja2](https://jinja.palletsprojects.com/) — HTML 模板渲染

## 安装

```bash
# 1. 克隆项目后进入目录
cd hotpicture

# 2. 创建虚拟环境
python -m venv venv

# 3. 激活虚拟环境
# Windows:
venv\Scripts\activate
# macOS / Linux:
source venv/bin/activate

# 4. 安装依赖
pip install -r requirements.txt
```

## 初始化与使用

```bash
# 确保虚拟环境已激活，然后运行主脚本：
python main.py
```

脚本执行流程：

1. 通过 akshare 获取申万一级行业列表（31 个行业）
2. 批量拉取每个行业近 150 个交易日的行情数据
3. 计算每日各行业成交额占比，再做 60 日滚动分位排名得到拥挤度
4. 输出 `data.json`（结构化数据）和 `index.html`（ECharts 热力图页面）

直接用浏览器打开 `index.html` 即可查看热力图。

## 热力图功能

| 功能 | 说明 |
|------|------|
| 横轴 | 日期（最近 90 个交易日），日期标签旋转 45° 显示 |
| 纵轴 | 申万一级行业（31 个），按最新拥挤度升序排列 |
| 颜色映射 | 深绿(0) → 浅绿 → 黄(50) → 橙 → 深红(100)，越红越拥挤 |
| 悬浮提示 | 鼠标悬停色块显示：行业名称、日期、拥挤度分位值 |
| DataZoom | 底部滑块缩放条，默认聚焦最近三个月；支持鼠标滚轮缩放和拖拽平移 |
| 自适应 | 图表填满浏览器全屏，窗口大小变化时自动重绘 |

## 目录结构

```
hotpicture/
├── main.py          # 主入口：数据获取 → 计算 → 输出
├── template.html    # ECharts 热力图 Jinja2 模板
├── requirements.txt # Python 依赖清单
├── data.json        # 输出：结构化数据
├── index.html       # 输出：独立可打开的 ECharts 页面
└── README.md
```

## 数据更新

每次运行 `python main.py` 都会重新拉取最新行情数据并覆盖 `data.json` 和 `index.html`。如需定期更新，可配置 cron（Linux/macOS）或任务计划程序（Windows）定时执行。
