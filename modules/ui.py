import flet as ft

async def ui():
		def tile_clicked(e):
			add_content = ft.CupertinoListTile(
				title=ft.Text("Title"),
				subtitle=ft.Text("Subtitle"),
				trailing=ft.Icon(name=ft.cupertino_icons.ALARM),
				additional_info=ft.Text("24/10/22"),
				on_click=tile_clicked,
			)
			list_content.controls.append(add_content)
			list_content.update()

		list_content = ft.ListView(
			controls=[
				ft.CupertinoListTile(
					# notched=True,
					# bgcolor_activated=ft.colors.AMBER_ACCENT,
					# leading=ft.Icon(name=ft.cupertino_icons.GAME_CONTROLLER),
					title=ft.Text("Title"),
					subtitle=ft.Text("Subtitle"),
					trailing=ft.Icon(name=ft.cupertino_icons.ALARM),
					additional_info=ft.Text("24/10/22"),
					on_click=tile_clicked,
				),
			],
			spacing=10,
			padding=20,
			height=300,
			divider_thickness = 0.5
		)

		def search_submit(e):
			contents.controls.append(ft.Text(value="Hello, world!", color="green"))
			contents.update()

		input = ft.TextField(hint_text="アプリ・サービス名を入力してください", width=400)

		# 部品を配置する
		contents = ft.Column(
				controls=[
					ft.Row(
						[
							input,
							ft.ElevatedButton("検索", on_click=search_submit, icon=ft.icons.SEARCH)
						]
					)
				],
				tight=True, # 水平方向の隙間をどうするか。デフォルトはFalseですべての要素に余白を与える。
				expand=True, # 利用可能なスペースを埋めるようにするか。
			)

		test = [list_content, contents]

		return test

async def control():
	def search_submit(e):
		contents.controls.append(ft.Text(value="Hello, world!", color="green"))
		contents.update()

	input = ft.TextField(hint_text="アプリ・サービス名を入力してください", width=400)

	# 部品を配置する
	contents = ft.Column(
			controls=[
				ft.Row(
					[
						input,
						ft.ElevatedButton("検索", on_click=search_submit, icon=ft.icons.SEARCH)
					]
				)
			],
			tight=True, # 水平方向の隙間をどうするか。デフォルトはFalseですべての要素に余白を与える。
			expand=True, # 利用可能なスペースを埋めるようにするか。
		)

	return contents