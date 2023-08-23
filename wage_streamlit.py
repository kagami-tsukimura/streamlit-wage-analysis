import pandas as pd
import plotly.express as px
import pydeck as pdk
import streamlit as st
from util.file_read import FileReader

# クラスのインスタンスを作成
file_reader = FileReader()

st.title("日本の賃金データのダッシュボード")


st.header("■2019年 : 一人当たり平均賃金ヒートマップ")

# プロパティを通じて属性にアクセス
jp_lat_lon = file_reader.jp_lat_lon.rename(columns={"pref_name": "都道府県名"})
df_pref_ind = file_reader.df_pref_ind[
    (file_reader.df_pref_ind["年齢"] == "年齢計") & (file_reader.df_pref_ind["集計年"] == 2019)
]
df_pref_map = pd.merge(df_pref_ind, jp_lat_lon, on="都道府県名")
df_pref_map["一人当たり賃金（相対値）"] = (
    df_pref_map["一人当たり賃金（万円）"] - df_pref_map["一人当たり賃金（万円）"].min()
) / (df_pref_map["一人当たり賃金（万円）"].max() - df_pref_map["一人当たり賃金（万円）"].min())

view = pdk.ViewState(longitude=139.691648, latitude=35.689185, zoom=4, pitch=40.5)
layer = pdk.Layer(
    "HeatmapLayer",
    data=df_pref_map,
    opacity=0.4,
    get_position=["lon", "lat"],
    threshold=0.3,
    get_weight="一人当たり賃金（相対値）",
)
layer_map = pdk.Deck(layers=layer, initial_view_state=view)
st.pydeck_chart(layer_map)
if st.checkbox("Show DataFrame"):
    st.sidebar.header("■2019年 : 一人当たり平均賃金ヒートマップ")
    st.sidebar.write(df_pref_map)

st.header("■集計年別の一人あたり賃金（万円）の推移")

df_ts_mean = file_reader.df_jp_ind[(file_reader.df_jp_ind["年齢"] == "年齢計")]
df_ts_mean = df_ts_mean.rename(columns={"一人当たり賃金（万円）": "全国_一人当たり賃金（万円）"})

df_pref_mean = file_reader.df_pref_ind[(file_reader.df_pref_ind["年齢"] == "年齢計")]
prefs = df_pref_mean["都道府県名"].unique()
option_pref = st.selectbox("都道府県", prefs)
df_pref_mean = df_pref_mean[(df_pref_mean["都道府県名"] == option_pref)]

df_mean_line = pd.merge(df_ts_mean, df_pref_mean, on="集計年")
df_mean_line = df_mean_line[["集計年", "全国_一人当たり賃金（万円）", "一人当たり賃金（万円）"]]
df_mean_line = df_mean_line.set_index("集計年")
st.line_chart(df_mean_line)

st.header("■年齢階級別の全国一人あたり平均賃金（万円）")

df_mean_bubble = file_reader.df_jp_ind[file_reader.df_jp_ind["年齢"] != "年齢計"]
fig = px.scatter(
    df_mean_bubble,
    x="一人当たり賃金（万円）",
    y="年間賞与その他特別給与額（万円）",
    range_x=[150, 700],
    range_y=[0, 150],
    size="所定内給与額（万円）",
    size_max=38,
    color="年齢",
    animation_frame="集計年",
    animation_group="年齢",
)
st.plotly_chart(fig)

st.header("■産業別の賃金推移")

years = file_reader.df_jp_category["集計年"].unique()
option_year = st.selectbox("集計年", years)
wages = ["一人当たり賃金（万円）", "所定内給与額（万円）", "年間賞与その他特別給与額（万円）"]
option_wage = st.selectbox("賃金の種類", wages)

df_mean_category = file_reader.df_jp_category[
    file_reader.df_jp_category["集計年"] == option_year
]
max_x = df_mean_category[option_wage].max() + 50

fig = px.bar(
    df_mean_category,
    x=option_wage,
    y="産業大分類名",
    color="産業大分類名",
    animation_frame="年齢",
    range_x=[0, max_x],
    orientation="h",
    width=800,
    height=500,
)

st.plotly_chart(fig)

st.text("出典: RESAS（地域経済分析システム）")
st.text("本結果はRESAS（地域経済分析システム）を加工して作成")
