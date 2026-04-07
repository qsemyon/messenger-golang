import flet as ft
import asyncio
import websockets
import json

async def main(page: ft.Page):
    page.title = "VibeChat"
    page.theme_mode = "dark"
    page.window_width = 400
    page.window_height = 700
    chat_history = ft.ListView(expand=True, spacing=10, auto_scroll=True)
    state = {"ws": None}

    async def listen_server():
        ws_url = "ws://localhost:8080/ws"
        try:
            async with websockets.connect(ws_url) as websocket:
                state["ws"] = websocket
                while True:
                    message = await websocket.recv()
                    data = json.loads(message)
                    chat_history.controls.append(
                        ft.Row([
                            ft.Container(
                                content=ft.Text(data["content"]),
                                bgcolor="grey800",
                                padding=10,
                                border_radius=10
                            )
                        ], alignment="start")
                    )
                    page.update()
        except Exception as e:
            print(f"WS Connection lost: {e}")
            state["ws"] = None

    async def send_click(e):
        if not message_input.value: return
        ws = state["ws"]
        if ws:
            try:
                await ws.send(json.dumps({"content": message_input.value}))
                message_input.value = ""
                page.update()
            except Exception as ex:
                print(f"Send error: {ex}")
    message_input = ft.TextField(
        hint_text="Сообщение...", 
        expand=True, 
        on_submit=send_click
    )

    send_button = ft.Container(
        content=ft.Icon("send", color="blue400"),
        on_click=send_click,
        width=50, height=50, padding=10, ink=True
    )

    page.add(
        ft.Column([
            chat_history,
            ft.Row([message_input, send_button], vertical_alignment="center")
        ], expand=True)
    )
    
    asyncio.create_task(listen_server())

ft.app(target=main)