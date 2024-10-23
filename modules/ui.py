import flet as ft


async def app_list_controls(app, open_service_page):
    return ft.CupertinoListTile(
	    title=ft.Text(f"{app[1]}"), #サービス名
	    subtitle=ft.Text(f"{app[2]}"), #詳細
        trailing=ft.Icon(name=ft.cupertino_icons.ALARM), #アイコン
	    additional_info=ft.Text(f"{app[3]}"), #最終更新日
		on_click=open_service_page,
	)
