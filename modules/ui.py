import flet as ft


async def app_list_controls(app, open_service_page):
    return 	ft.ListTile(
		title=ft.Text(f"{app[1]}"), #サービス名
		subtitle=ft.Text(f"{app[2]}"), #詳細
		trailing=ft.PopupMenuButton(
			icon=ft.icons.MORE_VERT,
			items=[
				ft.PopupMenuItem(text="編集", icon=ft.icons.EDIT),
				ft.PopupMenuItem(text="削除", icon=ft.icons.DELETE),
			],
			tooltip="メニュー",
        ),
		# additional_info=ft.Text(f"{app[3]}"), #最終更新日
		on_click=open_service_page,
		data=app[0],
		visual_density=ft.VisualDensity.ADAPTIVE_PLATFORM_DENSITY
	)
