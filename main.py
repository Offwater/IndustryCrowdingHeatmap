import json
from pathlib import Path

import akshare as ak
import pandas as pd
from jinja2 import Template

DIR = Path(__file__).parent
LOOKBACK = 150  # 取150个交易日，前60天用于计算分位
WINDOW = 60
DISPLAY = 90  # 热力图展示最近90天

# 1. 获取申万一级行业列表
industries = ak.sw_index_first_info()[["行业代码", "行业名称"]]
industries.columns = ["code", "name"]
codes = industries["code"].str.replace(".SI", "", regex=False).tolist()
names = industries["name"].tolist()

# 2. 批量拉取行情，计算每日各行业成交额占比
dfs = []
for code, name in zip(codes, names):
    df = ak.index_hist_sw(symbol=code, period="day")
    df = df[["日期", "成交额"]].copy()
    df["code"] = code
    df["name"] = name
    dfs.append(df)

raw = pd.concat(dfs, ignore_index=True)
raw["日期"] = pd.to_datetime(raw["日期"])
raw = raw.sort_values(["code", "日期"]).groupby("code").tail(LOOKBACK)  # 每个行业取最后 N 个交易日

daily_total = raw.groupby("日期")["成交额"].transform("sum")
raw["pct"] = raw["成交额"] / daily_total * 100

# 3. 计算每个行业 60 日滚动分位
raw = raw.sort_values(["code", "日期"])
raw["crowding"] = (
    raw.groupby("code")["pct"]
    .transform(lambda x: x.rolling(WINDOW, min_periods=WINDOW).rank(pct=True) * 100)
)

# 取最后 DISPLAY 个交易日
dates = sorted(raw["日期"].unique())[-DISPLAY:]
display_dates = [d.strftime("%Y-%m-%d") for d in dates]
mask = raw["日期"].isin(dates)
data = raw[mask][["name", "日期", "crowding", "pct"]].copy()
data["日期"] = data["日期"].dt.strftime("%Y-%m-%d")

# 按最后一天的拥挤度降序排列行业
last_day = display_dates[-1]
last_crowding = data[data["日期"] == last_day].set_index("name")["crowding"].sort_values(ascending=True)
name_list = last_crowding.index.tolist()

# 转成 ECharts heatmap 格式: [[x_idx, y_idx, value], ...]
heat_data = []
for _, row in data.iterrows():
    x = display_dates.index(row["日期"])
    y = name_list.index(row["name"])
    heat_data.append([x, y, round(row["crowding"], 2)])

# 输出 JSON
out = {
    "dates": display_dates,
    "industries": name_list,
    "data": heat_data,
}
with open(DIR / "data.json", "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False)

# 4. 渲染 HTML
template = Template(Path(DIR / "template.html").read_text(encoding="utf-8"))
html = template.render(dates_json=json.dumps(display_dates, ensure_ascii=False),
                       industries_json=json.dumps(name_list, ensure_ascii=False),
                       data_json=json.dumps(heat_data))

with open(DIR / "index.html", "w", encoding="utf-8") as f:
    f.write(html)

print(f"Done. {len(display_dates)} days, {len(name_list)} industries, {len(heat_data)} data points.")
