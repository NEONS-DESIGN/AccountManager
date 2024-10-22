import uuid
import flet as ft

async def main(page: ft.Page):
	page.title = "PasswordManager"  # タイトル
	page.window.width = 640  # 幅
	page.window.height = 480  # 高さ
	page.theme = ft.Theme(color_scheme_seed="blue", use_material3=False)
	page.window.resizable = False  # ウィンドウサイズ変更可否

	# ---------------------------------
    # 関数定義
    # ---------------------------------
	def search_submit(e):
		print(uuid.uuid5(uuid.NAMESPACE_URL, "ああああ"))
		print(search_filed.value)

	def route_change(e):
		print("Route change:", e.route)

		# ページクリア
		page.views.clear()

		# トップページ（常にviewに追加する）
		top_appbar = ft.AppBar(
			title=ft.Text("検索ページ"),
			actions=[
                ft.IconButton(ft.icons.ADD),
                ft.IconButton(ft.icons.CLOSE),
            ],
		)
		page.views.append(
			ft.View(
				"/",
				[
					top_appbar,
					list_content,
					form_content
				],
			)
		)
		# テストページ（テストページのときだけviewに追加する）
		if page.route == "/detail":
			page.views.append(
				ft.View(
					"/detail",
					[
						ft.AppBar(title=ft.Text("テストページ")),
						ft.Text("これはテストページです"),
					],
				)
			)

		# ページ更新
		page.update()

	# 現在のページを削除して、前のページに戻る
	def view_pop(e):
		print("View pop:", e.view)
		page.views.pop()
		top_view = page.views[-1]
		page.go(top_view.route)

	# テストページへ移動
	def open_detail_page(e):
		page.go("/detail")

	# ---------------------------------
    # コンテンツ定義
    # ---------------------------------
	list_content = ft.ListView(
		controls=[
			ft.CupertinoListTile(
				# notched=True,
				# bgcolor_activated=ft.colors.AMBER_ACCENT,
				# leading=ft.Icon(name=ft.cupertino_icons.GAME_CONTROLLER),
				title=ft.Text("ServiceName"),
				subtitle=ft.Text("Detail"),
				trailing=ft.Icon(name=ft.cupertino_icons.ALARM),
				additional_info=ft.Text("24/10/22"),
				on_click=open_detail_page,
			),
		],
		spacing=10, #gap
		padding=20,
		height=300,
		divider_thickness = 0.5 #区切り線
	)

	search_filed = ft.TextField(hint_text="アプリ・サービス名を入力してください", width=450, height=40, autofocus=True, text_vertical_align=0.9)
	form_content = ft.Column(
			controls=[
				ft.Row(
					[
						search_filed,
						ft.ElevatedButton("検索", on_click=search_submit, icon=ft.icons.SEARCH)
					],
					spacing=20,
					alignment=ft.MainAxisAlignment.CENTER
				)
			],
		)

	# ---------------------------------
	# イベントの登録
	# ---------------------------------
	# ページ遷移イベントが発生したら、ページを更新
	page.on_route_change = route_change
	# AppBarの戻るボタンクリック時、前のページへ戻る
	page.on_view_pop = view_pop

	# ---------------------------------
	# 起動時の処理
	# ---------------------------------
	# ページ遷移を実行
	page.go(page.route)

ft.app(target=main, assets_dir="assets")