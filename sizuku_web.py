import streamlit as st
from PIL import Image
import time

# ページ設定
st.set_page_config(page_title="チャーリーの物理sizuku", layout="centered")

# タイトル
st.title("💧 チャーリーの物理sizuku（Web音付き）")

# 初期状態
if "drop_count" not in st.session_state:
    st.session_state["drop_count"] = 0

# 音ファイルURL（GitHub raw）
DROP_SOUND_URL = "https://raw.githubusercontent.com/Chary1227/sizuku/main/sizuku_oto.mp3"

# 画像読み込み
try:
    img = Image.open("sizuku_drop.png")
except FileNotFoundError:
    st.error("💥 sizuku_drop.png が見つかりません。ファイル名を確認してください。")
    st.stop()

# ボタンを押したらカウント増加 + 音再生
if st.button("物理sizukuを落とす"):
    st.session_state["drop_count"] += 1

    # 🔊 音をHTMLで再生（ブラウザ上）
    st.markdown(
        f"""
        <audio autoplay>
            <source src="{DROP_SOUND_URL}" type="audio/mpeg">
        </audio>
        """,
        unsafe_allow_html=True
    )
# ========================
# CSVに履歴を保存する
# ========================

csv_path = "sizuku_log.csv"

# 今の情報を記録
now = datetime.now()
timestamp = now.strftime("%Y-%m-%d %H:%M:%S")
drop_number = st.session_state["drop_count"]

# データ行を辞書形式で
new_row = {"timestamp": timestamp, "drop_number": drop_number}

# ファイルがなければ新規作成、あれば追記
if os.path.exists(csv_path):
    df = pd.read_csv(csv_path)
    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
else:
    df = pd.DataFrame([new_row])

df.to_csv(csv_path, index=False)


# 落下アニメーション
for i in range(st.session_state["drop_count"]):
    placeholder = st.empty()
    for y in range(10):
        placeholder.image(img, width=50)
        time.sleep(0.03)
        placeholder.empty()
    st.image(img, width=50, caption=f"💥 sizuku #{i+1} 着地")

