import streamlit as st
from PIL import Image
import time
import pandas as pd
from datetime import datetime
import io
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import os
import matplotlib.font_manager as fm
import streamlit.components.v1 as components

# GitHub上の音ファイル（MP3）
DROP_SOUND_URL = "https://raw.githubusercontent.com/Chary1227/sizuku/main/sizuku_oto.mp3"

st.set_page_config(page_title="チャーリーのWebしずく", layout="centered")
st.title("💧 チャーリーのWebしずく（JS音対応）")

# セッション状態の初期化
if "drop_log" not in st.session_state:
    st.session_state["drop_log"] = []
    st.session_state["drop_count"] = 0

# sizuku_log.csv を削除（セッション単位）
if os.path.exists("sizuku_log.csv"):
    os.remove("sizuku_log.csv")

# 画像読み込み
try:
    img = Image.open("sizuku_drop.png")
except FileNotFoundError:
    st.error("💥 sizuku_drop.png が見つかりません。")
    st.stop()

# ボタンでしずくを落とす
if st.button("しずくを落とす"):
    st.session_state["drop_count"] += 1

    # JavaScript音声
    components.html(f"""
        <script>
            var audio = new Audio("{DROP_SOUND_URL}?t={datetime.now().timestamp()}");
            audio.play();
        </script>
    """, height=0)

    # アニメーション
    placeholder = st.empty()
    for _ in range(10):
        placeholder.image(img, width=50)
        time.sleep(0.03)
        placeholder.empty()
    st.image(img, width=50, caption=f"💥 sizuku #{st.session_state['drop_count']} 着地")

    # ログ記録
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    st.session_state["drop_log"].append({
        "timestamp": now,
        "drop_number": st.session_state["drop_count"]
    })
# DataFrame定義
csv_path = "sizuku_log.csv"
df = None  # ← これを必ず先に入れておく！

if os.path.exists(csv_path):
    df = pd.read_csv(csv_path)

if st.session_state["drop_log"]:
    df = pd.DataFrame(st.session_state["drop_log"])
    
# グラフ描画（ログが存在する場合）
if df is not None and not df.empty:
    df["timestamp"] = pd.to_datetime(df["timestamp"])

    # フォント設定（日本語対応）
    font_path = "/System/Library/Fonts/ヒラギノ角ゴシック W3.ttc"
    font_prop = fm.FontProperties(fname=font_path)

    # グラフ作成
    fig, ax = plt.subplots()
    ax.plot(df["timestamp"], df["drop_number"], marker="o", linestyle="-", color="blue")
    ax.set_xlabel("時刻", fontproperties=font_prop)
    ax.set_ylabel("しずく番号", fontproperties=font_prop)
    ax.set_title("💧 時間とともに落ちたしずく", fontproperties=font_prop)
    ax.tick_params(axis='x', rotation=45)

    # 表示
    st.pyplot(fig)

    # PNGダウンロード用に保存
    img_buffer = io.BytesIO()
    fig.savefig(img_buffer, format="png", bbox_inches="tight")
    img_buffer.seek(0)
    st.download_button(
        label="📷 グラフをPNGでダウンロード",
        data=img_buffer,
        file_name="sizuku_chart.png",
        mime="image/png"
    )


    # ログとCSVダウンロード
    st.subheader("📄 しずくログ")
    st.dataframe(df)

    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="📥 しずくログをダウンロード",
        data=csv,
        file_name="sizuku_log.csv",
        mime="text/csv"
    )
else:
    st.info("まだログがないようです。まずは1滴落としてみよう💧")
