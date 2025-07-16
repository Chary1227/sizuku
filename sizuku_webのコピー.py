import streamlit as st
from PIL import Image
import time

# ページ設定
st.set_page_config(page_title="チャーリーの物理sizuku", layout="centered")

# タイトル
st.title("💧 チャーリーの物理sizuku（Streamlit版）")

# 初期状態
if "drop_count" not in st.session_state:
    st.session_state["drop_count"] = 0

# 画像読み込み（ファイル名は正確に）
try:
    img = Image.open("sizuku_drop.png")
except FileNotFoundError:
    st.error("💥 sizuku_drop.png が見つかりません。ファイル名を確認してください。")
    st.stop()

# ボタンを押したらカウント増加
if st.button("物理sizukuを落とす"):
    st.session_state["drop_count"] += 1

# 落下アニメーション（簡易）
for i in range(st.session_state["drop_count"]):
    placeholder = st.empty()
    for y in range(10):
        placeholder.image(img, width=50)
        time.sleep(0.03)
        placeholder.empty()
    st.image(img, width=50, caption=f"💥 sizuku #{i+1} 着地")
