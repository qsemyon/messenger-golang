import flet as ft

def main(page: ft.Page):
    page.title = "VibeChat"
    page.theme_mode = "dark"
    page.window_width = 400
    page.window_height = 700
    
    chat_history = ft.ListView(
        expand=True,
        spacing=10,
        auto_scroll=True,
        controls=[ft.Text("Чат запущен...", color="grey")]
    )

    def send_click(e):
        if not message_input.value: return
        chat_history.controls.append(
            ft.Row([
                ft.Container(
                    content=ft.Text(message_input.value),
                    bgcolor="blue700",
                    padding=10,
                    border_radius=10
                )
            ], alignment="end")
        )
        message_input.value = ""
        page.update()

    message_input = ft.TextField(
        hint_text="Сообщение...", 
        expand=True, 
        on_submit=send_click
    )

    # Заменяем заглушку на реальную кнопку
    # В 0.8.4 пишем строго icon="send" (строкой)
    # Делаем кнопку вручную через Container
    # Ограничиваем кнопку фиксированным размером
    send_button = ft.Container(
        content=ft.Icon("send", color="blue400"),
        on_click=send_click,
        padding=10,
        ink=True,
        border_radius=10,
        # Жестко задаем размеры, чтобы не распирало
        width=50,
        height=50, 
    )

    page.add(
        ft.Column([
            chat_history,
            # Добавляем vertical_alignment, чтобы кнопка не тянулась вверх-вниз
            ft.Row([
                message_input, 
                send_button
            ], vertical_alignment="center") 
        ], expand=True)
    )


    
    page.update()

ft.app(target=main)