import flet as ft
import asyncio
import websockets
import json
import uuid

async def main(page: ft.Page):
    my_id = str(uuid.uuid4())
    
    page.title = "Messenger"
    page.window_width = 400
    page.window_height = 700
    
    chat_history = ft.ListView(expand=True, spacing=10, auto_scroll=True)
    state = {"ws": None}

    async def listen_server():
        try:
            async with websockets.connect("ws://localhost:8080/ws") as websocket:
                state["ws"] = websocket
                while True:
                    message = await websocket.recv()
                    data = json.loads(message)
                    
                    is_own = data.get("sender_id") == my_id
                    
                    chat_history.controls.append(
                        ft.Row([
                            ft.Container(
                                content=ft.Text(data["content"], color="white"),
                                bgcolor="blue700" if is_own else "grey800",
                                padding=12,
                                border_radius=15,
                                width=280, 
                            )
                        ], alignment="end" if is_own else "start")
                    )
                    page.update()
        except: pass

    async def send_click(e):
        if not message_input.value or not state["ws"]: return
        
        await state["ws"].send(json.dumps({
            "content": message_input.value,
            "sender_id": my_id
        }))
        message_input.value = ""
        page.update()

    message_input = ft.TextField(expand=True, on_submit=send_click, hint_text="Напиши что-нибудь...")
    
    send_button = ft.Container(
        content=ft.Icon("send", color="blue400"),
        on_click=send_click,
        width=50, height=50, ink=True
    )

    page.add(
        ft.Column([
            chat_history,
            ft.Row([message_input, send_button], vertical_alignment="center")
        ], expand=True)
    )
    
    asyncio.create_task(listen_server())

ft.app(target=main)