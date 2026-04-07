import flet as ft

def main(page: ft.Page):
    page.title = "VibeChat"
    page.theme_mode = "dark"
    
    # Принудительно задаем размеры для стабильности в 0.8.4
    page.window_width = 400
    page.window_height = 700
    
    # История чата (ListView заберет все свободное место)
    chat_history = ft.ListView(
        expand=True,
        spacing=10,
        auto_scroll=True,
        controls=[ft.Text("Чат запущен...", color="grey")]
    )

    def send_click(e):
        if not message_input.value: return
        # Добавляем контейнер с текстом, чтобы Row не был пустым
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

    # Поле ввода с обработкой Enter (on_submit)
    message_input = ft.TextField(
        hint_text="Сообщение...", 
        expand=True, 
        on_submit=send_click
    )

    # Заглушка вместо кнопки (пустое место шириной 50px)
    button_placeholder = ft.Container(width=50)

    # Собираем интерфейс
    page.add(
        ft.Column([
            chat_history,
            ft.Row([
                message_input, 
                button_placeholder
            ])
        ], expand=True)
    )
    
    page.update()

# Запуск через ft.app (наиболее стабильный для 0.8.4)
ft.app(target=main)