import flet as ft

from modules.sqlite import sql_execution

async def main(page: ft.Page):
	page.title = "PasswordManager"  # タイトル
	page.window.width = 640  # 幅
	page.window.min_width = 640
	page.window.height = 480  # 高さ
	page.window.min_height = 480
	page.theme = ft.Theme(color_scheme_seed="Blue")
	page.theme_mode = ft.ThemeMode.LIGHT
	page.window.resizable = True  # ウィンドウサイズ変更可否

	# プログレスバー表示
	progress_bar = ft.ProgressBar(visible=False)
	page.overlay.append(progress_bar)

	# グローバル変数
	global remove_data, edit_data
	remove_data = ""
	edit_data = ""

	# ---------------------------------
    # データベースアクセス関数定義
    # ---------------------------------
	async def get_service_list():
		sql = f"SELECT * FROM serviceList;"
		return await sql_execution(sql)

	async def get_search_service_list(serviceName):
		sql = f"SELECT * FROM serviceList WHERE serviceName = '{serviceName}';"
		return await sql_execution(sql)

	async def get_like_search_service_list(serviceName):
		sql = f"SELECT * FROM serviceList WHERE serviceName LIKE '%{serviceName}%';"
		return await sql_execution(sql)

	async def delete_service(serviceName):
		sql = f"DELETE FROM serviceList WHERE serviceName = '{serviceName}';"
		return await sql_execution(sql)

	async def delete_account(serviceName):
		sql = f"DELETE FROM accountData WHERE serviceName = '{serviceName}';"
		return await sql_execution(sql)

	async def insert_service(serviceName, serviceDetail):
		sql = f"INSERT INTO serviceList (serviceName, serviceDetail) VALUES ('{serviceName}', '{serviceDetail}')"
		return await sql_execution(sql)

	async def update_service(oldServiceName, newServiceName, serviceDetail):
		sql = f"UPDATE serviceList SET serviceDetail = '{serviceDetail}' WHERE serviceName IS '{oldServiceName}'"
		result1 = await sql_execution(sql)
		sql = f"UPDATE serviceList SET serviceName = '{newServiceName}' WHERE serviceName IS '{oldServiceName}'"
		result2 = await sql_execution(sql)
		return result1, result2

	# ---------------------------------
    # 関数定義
    # ---------------------------------
	def window_resize(e):
		search_filed.width = page.width - 160
		search_filed.update()

	async def reset():
		create_form_content.controls[2].controls[0].value = ""

	async def search_submit(e):
		app_list = await get_like_search_service_list(search_filed.value)
		service_list_content.clean()
		for app in app_list:
			service_list_content.controls.append(
				await app_list_controls(app)
			)
		service_list_content.update()

	async def create_submit(e):
		name = create_form_content.controls[0]
		detail = create_form_content.controls[1]
		error_text = create_form_content.controls[2].controls[0]
		# アプリ・サービス名の空を検出
		if not name.value:
			error_text.value = "アプリ・サービス名を入力してください。"
			create_form_content.update()
			return
		# 一致する名前があった場合エラー表示を出し、処理停止
		if await get_search_service_list(name.value):
			error_text.value ="既存のアプリ・サービス名は使用できません"
			create_form_content.update()
			return
		try:
			insert_result = await insert_service(name.value, detail.value)
		except Exception as err:
			print(err)
			error_text.value = "データベースエラーが発生しました。\nもう一度お願いいたします。"
			create_form_content.update()
			return
		await view_pop(e)

	async def edit_submit(e):
		oldName = edit_data.control.data[1]
		oldDetail = edit_data.control.data[2]
		name = create_form_content.controls[0]
		detail = create_form_content.controls[1]
		error_text = create_form_content.controls[2].controls[0]
		# アプリ・サービス名の空を検出
		if not name.value:
			error_text.value = "アプリ・サービス名を入力してください。"
			create_form_content.update()
			return
		# 一致する名前があった場合エラー表示を出し、処理停止
		if oldName == name.value:
			if oldDetail == detail.value:
				if await get_search_service_list(name.value):
					error_text.value ="既存のアプリ・サービス名は使用できません"
					create_form_content.update()
					return
		try:
			edit_result = await update_service(oldName, name.value, detail.value)
		except Exception as err:
			print(err)
			error_text.value = "データベースエラーが発生しました。\nもう一度お願いいたします。"
			create_form_content.update()
			return
		await view_pop(e)

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

		# トップページ
		if page.route == "/":
			appbar.title = ft.Text("アプリ・サービス検索")
			appbar.actions = [
				ft.IconButton(ft.icons.ADD, tooltip="データ追加", on_click=open_create_page),
				toggle_dark_light,
			]
			page.views.append(
				ft.View(
					"/",
					appbar=appbar,
					controls=[
						service_list_content,
						search_form_content
					],
					vertical_alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
					padding = 20
				)
			)
		# アカウントリストページ
		if page.route == "/service":
			appbar.title = ft.Text("アカウントリスト")
			page.views.append(
				ft.View(
					"/service",
					appbar=appbar,
					controls=[
						ft.Text("作成中"),
						ft.FloatingActionButton(icon=ft.icons.ADD, tooltip="アカウント追加", on_click=open_account_add_page),
					],
				)
			)
		# アカウント詳細ページ
		if page.route == "/service/add":
			appbar.title = ft.Text("アカウント詳細")
			page.views.append(
				ft.View(
					"/service/add",
					appbar=appbar,
					controls=[
						ft.Text("作成中"),
					]
				)
			)
		# アプリ・サービス登録ページ
		if page.route == "/create":
			appbar.title = ft.Text("アプリ・サービス登録")
			page.views.append(
				ft.View(
					"/create",
					appbar=appbar,
					controls=[
						create_form_content,
					]
				)
			)
		# アプリ・サービス編集ページ
		if page.route == "/edit":
			appbar.title = ft.Text("アプリ・サービス編集")
			e = edit_data
			create_form_content.controls[0].value = e.control.data[1]
			create_form_content.controls[1].value = e.control.data[2]
			page.views.append(
				ft.View(
					"/edit",
					appbar=appbar,
					controls=[
						create_form_content,
					]
				)
			)
		# ページ更新
		page.update()

	# 現在のページを削除して、前のページに戻る
	async def view_pop(e):
		page.views.pop()
		page.go("/back")
		await reset()

	# 詳細ページへ移動
	async def open_service_page(e):
		page.go("/service")

	# アカウント詳細ページ
	async def open_account_add_page(e):
		page.go("/service/add")

	# アプリ・サービス登録ページ
	async def open_create_page(e):
		page.go("/create")

	# アプリ・サービス編集ページ
	async def open_edit_page(e):
		global edit_data
		edit_data = e
		create_form_content.controls[2].controls[1].on_click = edit_submit
		page.go("/edit")

	# サービスとそれに関連したデータの削除
	async def remove_service(e):
		e = remove_data
		await delete_service(e.control.data)
		await delete_account(e.control.data)
		for check in service_list_content.controls:
			if check.data == e.control.data:
				check.clean()
				page.close(confirmation_dialog)
				return

	# サービスとそれに関連したデータの削除確認ダイアログ
	async def remove_confirmation_dialog(e):
		global remove_data
		remove_data = e
		confirmation_dialog.content = ft.Text(f"「{e.control.data}」を本当に削除しますか？\n一時削除すると、元に戻りません。", color=ft.colors.RED)
		confirmation_dialog.actions = [
			ft.TextButton("はい", on_click=remove_service),
			ft.TextButton("いいえ", on_click=lambda _: page.close(confirmation_dialog)),
		]
		page.open(confirmation_dialog)

	async def app_list_controls(app):
		return 	ft.ListTile(
			title=ft.Text(f"{app[1]}"), #サービス名
			subtitle=ft.Text(f"{app[2]}"), #詳細
			trailing=ft.PopupMenuButton(
				icon=ft.icons.MORE_VERT,
				items=[
					ft.PopupMenuItem(text="編集", icon=ft.icons.EDIT, on_click=open_edit_page, data=app),
					ft.PopupMenuItem(text="削除", icon=ft.icons.DELETE, on_click=remove_confirmation_dialog, data=app[1]),
				],
				tooltip="メニュー",
			),
			# additional_info=ft.Text(f"{app[3]}"), #最終更新日
			on_click=open_service_page,
			data=app[0],
			visual_density=ft.VisualDensity.ADAPTIVE_PLATFORM_DENSITY
		)

	# データ分すべて生成したリストの生成
	async def generate_service_list():
		service_list_content.controls.clear()
		for app in await get_service_list():
			service_list_content.controls.append(
				ft.ListTile(
					title=ft.Text(f"{app[1]}"), #サービス名
					subtitle=ft.Text(f"{app[2]}"), #詳細
					trailing=ft.PopupMenuButton(
						icon=ft.icons.MORE_VERT,
						items=[
							ft.PopupMenuItem(text="編集", icon=ft.icons.EDIT, on_click=open_edit_page, data=app),
							ft.PopupMenuItem(text="削除", icon=ft.icons.DELETE, on_click=remove_confirmation_dialog, data=app[1]),
						],
						tooltip="メニュー",
					),
					# additional_info=ft.Text(f"{app[3]}"), #最終更新日
					on_click=open_service_page,
					data=app[1],
					visual_density=ft.VisualDensity.ADAPTIVE_PLATFORM_DENSITY
				),
			)

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
	service_list_content = ft.ListView(
		controls=[],
		spacing=10, #gap
		padding=10,
		height=page.window.height - 200,
		divider_thickness = 0.5 #区切り線
	)

	search_filed = ft.TextField(
		hint_text="アプリ・サービス名を入力してください",
		width=page.window.width - 170,
		height=40,
		autofocus=True,
		text_vertical_align=0.9,
		on_submit=search_submit
	)

	search_form_content = ft.Column(
			controls=[
				ft.Row(
					[
						search_filed,
						ft.ElevatedButton("検索", on_click=search_submit, icon=ft.icons.SEARCH)
					],
					spacing=20,
					alignment=ft.MainAxisAlignment.SPACE_BETWEEN
				)
			],
		)

	create_form_content = ft.Column(
		controls=[
			ft.TextField(
						label="アプリ・サービス名",
						border=ft.InputBorder.UNDERLINE,
						max_lines=1,
						max_length=50
					),
			ft.TextField(
						label="アプリ・サービスの詳細",
						border=ft.InputBorder.UNDERLINE,
						max_lines=1,
						max_length=100
					),
			ft.Row(
				controls=[
					ft.Text(color=ft.colors.RED),
					ft.ElevatedButton(text="保存", on_click=create_submit)
				],
				alignment=ft.MainAxisAlignment.END,
			)
		],
		spacing=10
	)

	confirmation_dialog = ft.AlertDialog(
		modal=True,
		title=ft.Text("削除確認"),
		actions_alignment=ft.MainAxisAlignment.END,
	)

	# ---------------------------------
	# 初期呼び出し
	# ---------------------------------
	# データ分すべて生成したリストの生成
	await generate_service_list()

	# ---------------------------------
	# イベントの登録
	# ---------------------------------
	# ページ遷移イベントが発生したら、ページを更新
	page.on_route_change = route_change
	# AppBarの戻るボタンクリック時、前のページへ戻る
	page.on_view_pop = view_pop
	# windowのサイズが変更されたら
	page.on_resized = window_resize

	# ---------------------------------
	# 起動時の処理
	# ---------------------------------
	# ページ遷移を実行
	page.views.clear()
	page.go("/")

if __name__ == "__main__":
	ft.app(target=main, assets_dir="assets")