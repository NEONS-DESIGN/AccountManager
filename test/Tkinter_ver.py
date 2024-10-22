import tkinter as tk
from tkinter import ttk

def test(e):
    print(f"{e}が選択されました")
    label["text"] = e

# tkオブジェクトの作成
root = tk.Tk()
root.title("PasswordManager") #ウィンドウのタイトルを設定
root.geometry("640x360") #ウィンドウのサイズを設定
root.resizable(False, False) #ウィンドウサイズの固定

# フレームを作成して配置
topFrame = tk.Frame(root, bg="green")
bottomFrame = tk.Frame(root, borderwidth=1, bg="blue")
topFrame.pack(fill="x")
bottomFrame.pack(side=tk.BOTTOM, fill="x")

# ウィジェットの配置や、イベント処理などを記述
label = ttk.Label(topFrame, text="テキストテキスト")
label.pack()

entry = ttk.Entry(bottomFrame, width=30)
entry.grid(row=1, column=0)

button = ttk.Button(bottomFrame, text="クリック", command=lambda: test("クリック"))
button.grid(row=1, column=1)

# メニューバーの作成
menuBar = tk.Menu(root)
filemenu = tk.Menu(menuBar, tearoff=0)
filemenu.add_command(label="設定", command=lambda: test("設定"))
filemenu.add_separator() #切れ目
filemenu.add_command(label="終了", command=root.quit)
menuBar.add_cascade(label="ファイル", menu=filemenu)

root.config(menu=menuBar)
# メインループの実行
root.mainloop()