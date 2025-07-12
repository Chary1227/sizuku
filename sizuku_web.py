import tkinter as tk
from PIL import Image, ImageTk

def drop_sizuku():
    global drop_img, drop_id
    canvas.delete("all")
    # サイズと位置を初期化して画像生成
    drop_id = canvas.create_image(200, 0, image=drop_img)
    animate_fall()

def animate_fall():
    coords = canvas.coords(drop_id)
    if coords[1] < 200:
        canvas.move(drop_id, 0, 5)  # 下に5pxずつ移動
        canvas.after(30, animate_fall)
    else:
        print("物理sizuku、着地。")

# GUI準備
root = tk.Tk()
root.title("チャーリーの物理sizuku")
root.geometry("400x300")
root.configure(bg="white")

canvas = tk.Canvas(root, width=400, height=250, bg="white", highlightthickness=0)
canvas.pack(pady=(10, 0))

# Pillowで画像読み込み → Tk形式に変換
drop_img_pil = Image.open("sizuku_real.png")
drop_img = ImageTk.PhotoImage(drop_img_pil)

btn = tk.Button(root, text="物理sizukuを落とす", command=drop_sizuku, font=("Arial", 14))
btn.pack(pady=10)

root.mainloop()
