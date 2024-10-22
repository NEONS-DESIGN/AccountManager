import flet as ft


def main(page: ft.Page):
    example = "初期テキスト"
    def test(e):
        global example
        example = "改変テキスト"
        t2.value = example
        t2.update()
        print(example)

    page.title = "PasswordManager"  # タイトル
    page.window.width = 640  # 幅
    page.window.height = 480  # 高さ
    page.theme = ft.Theme(color_scheme_seed="blue", use_material3=False)
    page.window.resizable = False  # ウィンドウサイズ変更可否

    # 部品を配置する
    
    mainPage = ft.Column(
            [
                ft.Row(
                    [
                        ft.Text("ここは2行目"),
                        ft.TextField(hint_text="文字を入力してください"),
                    ],
                    tight=True,
                ),
                ft.Row(
                    [
                        ft.ElevatedButton("検索", on_click=test, icon=ft.icons.SEARCH),
                        ft.ElevatedButton("クリア", icon=ft.icons.DELETE)
                    ]
                )
            ],
            tight=True, # 水平方向の隙間をどうするか。デフォルトはFalseですべての要素に余白を与える。
            expand=True, # 利用可能なスペースを埋めるようにするか。
        )
    t2 = ft.Text(f"{example}")
    page.add(t2, mainPage)


ft.app(target=main)