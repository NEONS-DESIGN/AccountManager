import configparser
import datetime
import os
import flet as ft
import uuid

from dotenv import load_dotenv, set_key
from modules.databaseAccess import *
from modules.cipher import *

# 環境変数読み込み
load_dotenv()

# configファイルの読み込み
config = configparser.ConfigParser()
config.read('./config.ini', 'UTF-8')

async def main(page: ft.Page):
	page.title = "PasswordManager"  # タイトル
	page.window.width = 640  # 幅
	page.window.min_width = 640
	page.window.height = 480  # 高さ
	page.window.min_height = 480
	page.theme = ft.Theme(color_scheme_seed="Blue")
	page.theme_mode = config.get('Settings', 'theme_mode')
	page.window.resizable = True  # ウィンドウサイズ変更可否

	# プログレスバー表示
	progress_bar = ft.ProgressBar(visible=False)
	page.overlay.append(progress_bar)

	# グローバル変数
	global remove_data, edit_data, detail_data, account_uuid
	remove_data = ""
	edit_data = ""
	detail_data = ""
	account_uuid = ""

	# ---------------------------------
    # 関数定義
    # ---------------------------------
	def window_resize(e):
		search_filed.width = page.width - 160
		search_filed.update()

	async def create_form_reset():
		create_form_content.controls[0].value = ""
		create_form_content.controls[1].value = ""
		create_form_content.controls[2].controls[0].value = ""

	async def account_add_form_reset():
		account_add_form_content.controls[0].value = ""
		account_add_form_content.controls[1].controls[0].value = ""
		account_add_form_content.controls[1].controls[1].value = ""
		account_add_form_content.controls[2].value = ""
		account_add_form_content.controls[3].controls[0].value = ""

	async def search_submit(e):
		app_list = await get_like_search_service_list(search_filed.value)
		service_list_content.clean()
		if app_list == []:
			no_data_content.visible = True
			service_list_content.visible = False
		else:
			no_data_content.visible = False
			service_list_content.visible = True
			for app in app_list:
				service_list_content.controls.append(
					await app_list_controls(app)
				)
		page.update()

	async def create_submit(e):
		gen_uuid = uuid.uuid4()
		name = create_form_content.controls[0]
		detail = create_form_content.controls[1]
		error_text = create_form_content.controls[2].controls[0]
		# アプリ・サービス名の空を検出
		if not name.value:
			error_text.value = "アプリ・サービス名を入力してください。"
			create_form_content.update()
			return
		# 詳細が空の場合、Noneを挿入
		if not detail.value:
			detail.value = "None"
		# 一致する名前があった場合エラー表示を出し、処理停止
		if await get_search_service_list(name.value):
			error_text.value ="既存のアプリ・サービス名は使用できません"
			create_form_content.update()
			return
		try:
			insert_result = await insert_service(gen_uuid, name.value, detail.value)
		except Exception as err:
			print(err)
			error_text.value = "データベースエラーが発生しました。\nもう一度お願いいたします。"
			create_form_content.update()
			return
		await search_submit(e)
		await view_pop(e)

	async def add_submit(e):
		uuid = account_uuid
		account_name = account_add_form_content.controls[0].value
		id = account_add_form_content.controls[1].controls[0].value
		password = account_add_form_content.controls[1].controls[1].value
		mail_address = account_add_form_content.controls[2].value
		error_text = account_add_form_content.controls[3].controls[0]
		if not account_name:
			error_text.value = "アカウント名が入力されていません。"
			account_add_form_content.update()
			return
		try:
			secret_key = os.environ['CLIENT_SECRET_KEY']
			tokyo_tz = datetime.timezone(datetime.timedelta(hours=9))
			dt = datetime.datetime.now(tokyo_tz)
			update_time = f"{dt.year}年{dt.month}月{dt.day}日"
			encrypt_password = await encrypt(secret_key, password)
			result = await add_account(uuid, account_name, id, mail_address, encrypt_password, update_time)
		except Exception as err:
			print(err)
			error_text.value = "データベースエラーが発生しました。\nもう一度お願いいたします。"
			account_add_form_content.update()
			return
		await generate_account_list()
		await view_pop(e)

	async def edit_submit(e):
		uuid = edit_data.control.data[0]
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
		# 詳細が空の場合、Noneを挿入
		if not detail.value:
			detail.value = "None"
		# 一致する名前があった場合エラー表示を出し、処理停止
		if oldName == name.value:
			if oldDetail == detail.value:
				if await get_search_service_list(name.value):
					error_text.value ="既存のアプリ・サービス名は使用できません"
					create_form_content.update()
					return
		try:
			edit_result = await update_service(uuid, name.value, detail.value)
		except Exception as err:
			print(err)
			error_text.value = "データベースエラーが発生しました。\nもう一度お願いいたします。"
			create_form_content.update()
			return
		await search_submit(e)
		await view_pop(e)

	async def account_edit_submit(e):
		print(account_add_form_content.data)
		uuid = account_add_form_content.data[0]
		account_name = account_add_form_content.controls[0].value
		old_account_name = account_add_form_content.data[1]
		id = account_add_form_content.controls[1].controls[0].value
		old_id = account_add_form_content.data[2]
		decrypt_password = account_add_form_content.controls[1].controls[1].value
		old_password = account_add_form_content.data[4]
		mail_address = account_add_form_content.controls[2].value
		old_mail_address = account_add_form_content.data[3]

		error_text = account_add_form_content.controls[3].controls[0]

		if account_name == "":
			error_text.value = "アカウント名が入力されていません。"
			account_add_form_content.update()
			return
		if account_name != old_account_name:
			account_list = await get_account_list(uuid)
			for check in account_list:
				if account_name == check[1]:
					error_text.value = "すでに使われているアカウント名です。"
					account_add_form_content.update()
					return
		# error_text = account_add_form_content[3].controls[0]
		# try:
		# 	result = await update_account(uuid, account_name, id, mail_address, password, update_time)
		# except Exception as err:
		# 	print(err)
		# 	error_text.value = "データベースエラーが発生しました。\nもう一度お願いいたします。"
		# 	create_form_content.update()
		# 	return
		# await view_pop(e)

	async def change_theme(e):
		page.theme_mode = "light" if page.theme_mode == "dark" else "dark"
		toggle_dark_light.selected = not toggle_dark_light.selected
		toggle_dark_light.tooltip = f"{'ライト' if toggle_dark_light.selected else 'ダーク'}モードへ切り替え"
		page.update()
		config.set('Settings', 'theme_mode', page.theme_mode)
		with open('config.ini', 'w') as fp:
			config.write(fp)
			fp.close()

	async def route_change(e):
		print("Route change:", e.route)

		appbar = ft.AppBar(
			title=ft.Text(""),
			actions=[],
		)

		# トップページ
		if page.route == "/":
			await data_check()
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
						starter_content,
						no_data_content,
						service_list_content,
						search_form_content
					],
					vertical_alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
					padding = 20,
				)
			)
		# アカウントリストページ
		if page.route == "/accounts":
			await account_add_form_reset()
			appbar.title = ft.Text("アカウントリスト")
			page.views.append(
				ft.View(
					"/accounts",
					appbar=appbar,
					controls=[
						account_list_content,
						ft.FloatingActionButton(icon=ft.icons.ADD, tooltip="アカウント追加", on_click=open_account_add_page),
					],
				)
			)
		# アカウント追加ページ
		if page.route == "/accounts/add":
			appbar.title = ft.Text("アカウント追加")
			page.views.append(
				ft.View(
					"/accounts/add",
					appbar=appbar,
					controls=[
						account_add_form_content,
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
		# アカウント詳細ページ
		if page.route == "/accounts/detail":
			appbar.title = ft.Text("アカウント詳細")
			detail = detail_data.control
			password = detail.data[4]
			decrypt_password = ""
			if password:
				secret_key = os.environ['CLIENT_SECRET_KEY']
				decrypt_password = await decrypt(secret_key, password)
			account_detail_form_content.controls[0].value = detail.data[1]
			account_detail_form_content.controls[0].data = detail.data[1]
			account_detail_form_content.controls[1].controls[0].value = detail.data[2]
			account_detail_form_content.controls[1].controls[0].data = detail.data[2]
			account_detail_form_content.controls[1].controls[1].value = decrypt_password
			account_detail_form_content.controls[1].controls[1].data = decrypt_password
			account_detail_form_content.controls[2].value = detail.data[3]
			account_detail_form_content.controls[2].data = detail.data[3]
			page.views.append(
				ft.View(
					"/accounts/detail",
					appbar=appbar,
					controls=[
						account_detail_form_content,
					]
				)
			)
		# アカウントデータ編集ページ
		if page.route == "/accounts/edit":
			account_name = edit_data.control.data[1]
			id = edit_data.control.data[2]
			mail_address = edit_data.control.data[3]
			password = edit_data.control.data[4]
			decrypt_password = ""
			if password:
				secret_key = os.environ['CLIENT_SECRET_KEY']
				decrypt_password = await decrypt(secret_key, password)
			account_add_form_content.controls[0].value = account_name
			account_add_form_content.controls[1].controls[0].value = id
			account_add_form_content.controls[1].controls[1].value = decrypt_password
			account_add_form_content.controls[2].value = mail_address
			account_add_form_content.controls[3].controls[1].text = "保存"
			account_add_form_content.controls[3].controls[1].icon = ft.icons.SAVE
			account_add_form_content.controls[3].controls[1].on_click = account_edit_submit
			account_add_form_content.data = edit_data.control.data
			appbar.title = ft.Text("アカウントデータ編集")
			page.views.append(
				ft.View(
					"/accounts/edit",
					appbar=appbar,
					controls=[
						account_add_form_content,
					],
				),
			)
		# ページ更新
		page.update()

	# 現在のページを削除して、前のページに戻る
	async def view_pop(e):
		page.views.pop()
		page.go("/back")
		await data_check()
		await create_form_reset()
		await account_add_form_reset()

	# アカウント一覧ページ
	async def open_service_page(e):
		global account_uuid
		account_uuid = e.control.data[0]
		await generate_account_list()
		page.go("/accounts")

	# アカウント追加ページ
	async def open_account_add_page(e):
		print(account_uuid)
		page.go("/accounts/add")

	# アプリ・サービス登録ページ
	async def open_create_page(e):
		create_form_content.controls[2].controls[1].on_click = create_submit
		page.go("/create")

	# アプリ・サービス編集ページ
	async def open_edit_page(e):
		global edit_data
		edit_data = e
		create_form_content.controls[2].controls[1].on_click = edit_submit
		page.go("/edit")

	# アカウント詳細ページ
	async def open_account_detail_page(e):
		global detail_data
		detail_data = e
		page.go("/accounts/detail")

	# アカウント編集ページ
	async def open_account_edit_page(e):
		global edit_data
		edit_data = e
		page.go("/accounts/edit")

	# サービスとそれに関連したデータの削除
	async def remove_service(e):
		e = remove_data
		# データ数を見てどのテーブルか判断する
		if len(e.control.data) == 3: #serviceList
			await delete_service(e.control.data[0])
			await delete_all_account(e.control.data[0])
			for check in service_list_content.controls:
				if check.data[0] == e.control.data[0]:
					await search_submit(e)
					page.close(confirmation_dialog)
					return
		elif len(e.control.data) == 6: #accountData
			await delete_account(e.control.data[0], e.control.data[1])
			for check in account_list_content.controls:
				if check.data[0] == e.control.data[0]:
					await generate_account_list()
					account_list_content.update()
					page.close(confirmation_dialog)
					return

	# サービスとそれに関連したデータの削除確認ダイアログ
	async def remove_confirmation_dialog(e):
		global remove_data
		remove_data = e
		confirmation_dialog.content = ft.Text(f"「{e.control.data[1]}」を本当に削除しますか？\n一時削除すると、元に戻りません。", color=ft.colors.RED)
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
					ft.PopupMenuItem(text="削除", icon=ft.icons.DELETE, on_click=remove_confirmation_dialog, data=app),
				],
				tooltip="メニュー",
			),
			# additional_info=ft.Text(f"{app[3]}"), #最終更新日
			on_click=open_service_page,
			data=app,
			visual_density=ft.VisualDensity.ADAPTIVE_PLATFORM_DENSITY
		)

	# データ分すべて生成したリストの生成
	async def generate_service_list():
		# 一旦リストの中身を空にする
		service_list_content.controls.clear()
		# DBからデータを取得してくる
		service_list = await get_service_list()
		if service_list != []:
			starter_content.visible = False
			# 取ってきたデータを一つづつ取り出し、要素を作成し追加する
			for app in service_list:
				service_list_content.controls.append(
					ft.ListTile(
						title=ft.Text(f"{app[1]}"), #サービス名
						subtitle=ft.Text(f"{app[2]}"), #詳細
						trailing=ft.PopupMenuButton(
							icon=ft.icons.MORE_VERT,
							items=[
								ft.PopupMenuItem(text="編集", icon=ft.icons.EDIT, on_click=open_edit_page, data=app),
								ft.PopupMenuItem(text="削除", icon=ft.icons.DELETE, on_click=remove_confirmation_dialog, data=app),
							],
							tooltip="メニュー",
						),
						on_click=open_service_page,
						data=app,
						visual_density=ft.VisualDensity.ADAPTIVE_PLATFORM_DENSITY
					),
				)
		else:
			# 秘密鍵を生成し、環境変数ファイルへ書き込む
			secret_key = await create_key()
			set_key(".env", "CLIENT_SECRET_KEY", secret_key)
			# 表示の切り替え
			service_list_content.visible = False
			search_form_content.visible = False
			# 画面へ反映
			page.update()

	async def generate_account_list():
		account_list_content.controls.clear()
		account_list = await get_account_list(account_uuid)
		for app in account_list:
			account_list_content.controls.append(
				ft.ListTile(
					title=ft.Text(f"{app[1]}"), #サービス名
					subtitle=ft.Text(f"最終更新: {app[5]}"), #詳細
					trailing=ft.PopupMenuButton(
						icon=ft.icons.MORE_VERT,
						items=[
							ft.PopupMenuItem(text="編集", icon=ft.icons.EDIT, data=app, on_click=open_account_edit_page),
							ft.PopupMenuItem(text="削除", icon=ft.icons.DELETE, data=app, on_click=remove_confirmation_dialog),
						],
						tooltip="メニュー",
					),
					on_click=open_account_detail_page,
					data=app,
					visual_density=ft.VisualDensity.ADAPTIVE_PLATFORM_DENSITY
				),
			)

	# データの有無チェック
	async def data_check():
		service_list = await get_service_list()
		if service_list != []:
			starter_content.visible = False
			no_data_content.visible = False
			service_list_content.visible = True
			search_form_content.visible = True

	# クリップボードへコピー
	async def set_clipboard(e):
		data = e.control.data
		if data:
			page.set_clipboard(data)
			page.overlay.append(ft.SnackBar(ft.Text(f"クリップボードに 「{data}」 をコピーしました。"), open=True)),
		else:
			page.overlay.append(ft.SnackBar(ft.Text(f"データがありません。"), open=True)),
		page.update()

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

	# 初起動時&データなし時表示
	starter_content = ft.Column (
		controls=[
			ft.Row(
				controls=[
					ft.Text("データがありません。", weight=ft.FontWeight.W_900, size=20)
				],
				alignment= ft.MainAxisAlignment.CENTER,
			),
			ft.Row(
				controls=[
					ft.ElevatedButton(text="追加", icon=ft.icons.ADD, icon_color=ft.colors.BLUE, on_click=open_create_page),
					ft.ElevatedButton(text="閉じる", icon=ft.icons.CLOSE, icon_color=ft.colors.RED, on_click=lambda _: page.window.close()),
				],
				spacing=20,
				alignment= ft.MainAxisAlignment.CENTER
			),
		],
		height=page.window.height - 200,
		alignment= ft.MainAxisAlignment.CENTER,
		visible=True,
	)

	no_data_content = ft.Column (
		controls=[
			ft.Row(
				controls=[
					ft.Text("データがありません。", weight=ft.FontWeight.BOLD, size=20)
				],
				alignment= ft.MainAxisAlignment.CENTER,
			),
		],
		height=page.window.height - 200,
		alignment= ft.MainAxisAlignment.CENTER,
		visible=True,
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
		hint_text="アプリ・サービス名で検索",
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
						label="アプリ・サービス名 (必須)",
						border=ft.InputBorder.UNDERLINE,
						max_lines=1,
						max_length=50,
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
					ft.ElevatedButton(text="保存", icon=ft.icons.SAVE)
				],
				alignment=ft.MainAxisAlignment.END,
			)
		],
		spacing=10,
	)

	account_add_form_content = ft.ListView(
		controls=[
			ft.TextField(
						label="アカウント名 (必須)",
						border=ft.InputBorder.UNDERLINE,
						max_lines=1,
						max_length=50,
						prefix_icon=ft.icons.LABEL,
					),
			ft.Row(
				controls=[
					ft.TextField(
						label="ID",
						border=ft.InputBorder.UNDERLINE,
						max_lines=1,
						max_length=200,
						width=(page.window.width / 2) - 50,
						prefix_icon=ft.icons.BADGE,
					),
					ft.TextField(
						label="パスワード",
						border=ft.InputBorder.UNDERLINE,
						max_lines=1,
						max_length=100,
						width=(page.window.width / 2) - 50,
						prefix_icon=ft.icons.PASSWORD,
						password=True,
						can_reveal_password=True
					),
				],
				alignment=ft.MainAxisAlignment.SPACE_BETWEEN
			),
			ft.TextField(
						label="メールアドレス",
						border=ft.InputBorder.UNDERLINE,
						max_lines=1,
						max_length=200,
						prefix_icon=ft.icons.MAIL,
					),
			ft.Row(
				controls=[
					ft.Text(color=ft.colors.RED),
					ft.ElevatedButton(
						text="追加",
						icon=ft.icons.ADD,
						on_click=add_submit,
					)
				],
				alignment=ft.MainAxisAlignment.END,
			)
		],
		spacing=10,
		padding=20,
	)

	account_detail_form_content = ft.ListView(
		controls=[
			ft.TextField(
						label="アカウント名",
						border=ft.InputBorder.UNDERLINE,
						max_lines=1,
						prefix_icon=ft.icons.LABEL,
						read_only=True,
						on_focus=set_clipboard,
					),
			ft.Row(
				controls=[
					ft.TextField(
						label="ID",
						border=ft.InputBorder.UNDERLINE,
						max_lines=1,
						width=(page.window.width / 2) - 50,
						prefix_icon=ft.icons.BADGE,
						read_only=True,
						on_focus=set_clipboard,
					),
					ft.TextField(
						label="パスワード",
						border=ft.InputBorder.UNDERLINE,
						max_lines=1,
						width=(page.window.width / 2) - 50,
						prefix_icon=ft.icons.PASSWORD,
						read_only=True,
						on_focus=set_clipboard,
						password=True,
						can_reveal_password=True,
					),
				],
				alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
			),
			ft.TextField(
						label="メールアドレス",
						border=ft.InputBorder.UNDERLINE,
						max_lines=1,
						prefix_icon=ft.icons.MAIL,
						read_only=True,
						on_focus=set_clipboard,
					),
		],
		spacing=20,
		padding=20,
	)

	confirmation_dialog = ft.AlertDialog(
		modal=True,
		title=ft.Text("削除確認"),
		actions_alignment=ft.MainAxisAlignment.END,
	)

	account_list_content = ft.ListView(
		controls=[],
		spacing=10, #gap
		padding=10,
		height=page.window.height - 200,
		divider_thickness = 0.5, #区切り線
	)

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
	# テーマモードの切替
	if page.theme_mode == "dark":
		toggle_dark_light.selected = not toggle_dark_light.selected
	toggle_dark_light.tooltip = f"{'ライト' if toggle_dark_light.selected else 'ダーク'}モードへ切り替え"
	# データ分すべて生成したリストの生成
	await generate_service_list()
	# ページ遷移を実行
	page.views.clear()
	page.go("/")

if __name__ == "__main__":
	ft.app(target=main, assets_dir="assets")