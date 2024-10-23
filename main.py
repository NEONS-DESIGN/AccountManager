import flet as ft
import hashlib
import uuid

from modules.ui import *
from modules.sqlite import sql_execution

async def main(page: ft.Page):
	page.title = "PasswordManager"  # タイトル
	page.window.width = 640  # 幅
	page.window.height = 480  # 高さ
	page.theme = ft.Theme(color_scheme_seed="Blue")
	page.theme_mode = ft.ThemeMode.LIGHT
	page.window.resizable = False  # ウィンドウサイズ変更可否

	# プログレスバー表示
	progress_bar = ft.ProgressBar(visible=False)
	page.overlay.append(progress_bar)

	# 初期値取得
	sql = f"SELECT * FROM serviceList"
	app_list = await sql_execution(sql)

	# ---------------------------------
    # 関数定義
    # ---------------------------------
	async def search_submit(e):
		# print(uuid.uuid5(uuid.NAMESPACE_URL, search_filed.value))
		sql = f"SELECT * FROM serviceList WHERE serviceName LIKE '%{search_filed.value}%'"
		app_list = await sql_execution(sql)
		list_content.clean()
		for app in app_list:
			list_content.controls.append(
				await app_list_controls(app, open_service_page)
			)
		list_content.update()

	async def change_theme(e):
		page.theme_mode = "light" if page.theme_mode == "dark" else "dark"
		toggle_dark_light.selected = not toggle_dark_light.selected
		toggle_dark_light.tooltip = f"{'ライト' if toggle_dark_light.selected else 'ダーク'}モードへ切り替え"
		page.update()

	async def route_change(e):
		print("Route change:", e.route)

		appbar = ft.AppBar(
			title=ft.Text(""),
			actions=[],
		)

		# トップページ（常にviewに追加する）
		if page.route == "/":
			appbar.title = ft.Text("アプリ・サービス検索")
			appbar.actions = [
				ft.IconButton(ft.icons.ADD, tooltip="データ追加"),
				toggle_dark_light,
			]
			page.views.append(
				ft.View(
					"/",
					[
						appbar,
						list_content,
						form_content
					],
				)
			)
		# アカウントリストページ（アカウントリストページのときだけviewに追加する）
		if page.route == "/service":
			appbar.title = ft.Text("アカウントリスト")
			page.views.append(
				ft.View(
					"/service",
					[
						appbar,
						ft.Text("これはテストページです"),
						ft.FloatingActionButton(icon=ft.icons.ADD, tooltip="アカウント追加", on_click=open_profile_add_page),
					],
				)
			)
		# アカウント詳細ページ（アカウント詳細ページのときだけviewに追加する)
		if page.route == "/service/add":
			appbar.title = ft.Text("アカウント詳細")
			page.views.append(
				ft.View(
					"/service/add",
					[
						appbar,
						ft.Text("これはテストページです"),
					]
				)
			)
		# ページ更新
		page.update()

	# 現在のページを削除して、前のページに戻る
	async def view_pop(e):
		print(f"\nPop: {page.views.pop()}")
		page.go("/back")

	# 詳細ページへ移動
	def open_service_page(e):
		page.go("/service")
		print(f"\n\n\n\n{e.data}---------")

	async def open_profile_add_page(e):
		page.go("/service/add")

	# ---------------------------------
    # コンテンツ定義
    # ---------------------------------
	toggle_dark_light = ft.IconButton(
		# ToolTipの表示文言
		tooltip=f"ダークモードへ切り替え",
		# アイコンクリック時に実行する処理
		on_click=change_theme,
		icon=ft.icons.LIGHT_MODE,
		icon_color=ft.colors.ORANGE_300,
		selected_icon=ft.icons.DARK_MODE,
		selected_icon_color=ft.colors.YELLOW,
	)

	# リスト用意
	list_content = ft.ListView(
		controls=[],
		spacing=10, #gap
		padding=20,
		height=300,
		divider_thickness = 0.5 #区切り線
	)
	# データ分すべて生成したリストへ生成
	for app in app_list:
		list_content.controls.append(
			ft.CupertinoListTile(
				title=ft.Text(f"{app[1]}"), #サービス名
				subtitle=ft.Text(f"{app[2]}"), #詳細
				trailing=ft.Icon(name=ft.cupertino_icons.ALARM), #アイコン
				additional_info=ft.Text(f"{app[3]}"), #最終更新日
				data=app[0],
				on_click=lambda e=page.data: open_service_page(e),
			)
		)

	search_filed = ft.TextField(
		hint_text="アプリ・サービス名を入力してください",
		width=450,
		height=40,
		autofocus=True,
		text_vertical_align=0.9
	)

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
	page.views.clear()
	page.go("/")

if __name__ == "__main__":
	ft.app(target=main, assets_dir="assets")