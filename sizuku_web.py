import streamlit as st
from PIL import Image
import time
import pandas as pd
from datetime import datetime
import io
import matplotlib.pyplot as plt
import os

# JS埋め込みに必要
import streamlit.components.v1 as components

# GitHub上の音ファイル（MP3）
DROP_SOUND_URL = "https://raw.githubusercontent.com/Chary1227/sizuku/main/sizuku_oto.mp3"

# ページ設定とタイトル
st.set_page_config(page_title="チャーリーのWebしずく", layout="centered")
st.title("💧 チャーリーのWebしずく（JS音対応）")

# 初期状態
if "drop_count" not in st.session_state:
    st.session_state["drop_count"] = 0
if "drop_log" not in st.session_state:
    st.session_state["drop_log"] = []

# 画像読み込み
try:
    img = Image.open("sizuku_drop.png")
except FileNotFoundError:
    st.error("💥 sizuku_drop.png が見つかりません。")
    st.stop()

# ボタン処理
if st.button("しずくを落とす"):
    st.session_state["drop_count"] += 1

    # JavaScriptで音を鳴らす（キャッシュ回避で毎回timestamp付加）
    components.html(f"""
        <script>
            var audio = new Audio("{DROP_SOUND_URL}?t={datetime.now().timestamp()}");
            audio.play();
        </script>
    """, height=0)

    # アニメーション
    placeholder = st.empty()
    for y in range(10):
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
df = None
if os.path.exists(csv_path):
    df = pd.read_csv(csv_path)
if st.session_state["drop_log"]:
    df = pd.DataFrame(st.session_state["drop_log"])

# グラフ描画
if df is not None and not df.empty:
    fig, ax = plt.subplots()
    ax.plot(df["timestamp"], df["drop_number"], marker="o", linestyle="-", color="blue")
    ax.set_xlabel("時刻")
    ax.set_ylabel("しずく番号")
    ax.set_title("💧 時間とともに落ちたしずく")
    ax.tick_params(axis='x', rotation=45)
    st.pyplot(fig)

    # PNGダウンロードボタン
    img_buffer = io.BytesIO()
    fig.savefig(img_buffer, format="png")
    img_buffer.seek(0)
    st.download_button(
        label="📷 グラフをPNGでダウンロード",
        data=img_buffer,
        file_name="sizuku_chart.png",
        mime="image/png"
    )
else:
    st.info("まだログがないようです。まずは1滴落としてみよう💧")

# ログの表示とCSVダウンロード
if df is not None and not df.empty:
    st.subheader("📄 しずくログ")
    st.dataframe(df)

    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="📥 しずくログをダウンロード",
        data=csv,
        file_name="sizuku_log.csv",
        mime="text/csv"
    )
