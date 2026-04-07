## Технологический стек

- **Backend:** [Golang 1.26](https://go.dev) - обработка WebSocket соединений и бизнес-логика
- **Frontend:** [Python 3.14.3](https://python.org) + [Flet 0.84.0](https://flet.dev) - адаптивный интерфейс с поддержкой тёмной темы
- **Database:** [PostgreSQL 15](https://postgresql.org) - надёжное хранение истории сообщений
- **Infrastructure:** [Docker](https://docker.com) & Docker Compose - полная контейнеризация проекта
- **Communication:** WebSockets (через `gorilla/websocket`) для мгновенного обмена данными

## Основные возможности
- **Real-time сообщения:** Мгновенная доставка через сокеты
- **Умное выравнивание:** Свои сообщения отображаются справа (синие), чужие - слева (серые)
- **История чата:** Все сообщения сохраняются в БД и подгружаются при входе
- **Авто-перенос текста:** Длинные сообщения не ломают интерфейс
- **Docker-ready:** Запуск всей инфраструктуры одной командой
## Как запустить проект
1. Должен быть скачен Python 3.14.3 или выше
```text
https://www.python.org/
```
2. Должна быть скачена программа Docker Desktop
```text
https://docs.docker.com/get-started/get-docker/
```
3. Клонирование репозитория
```Powershell
git clone https://github.com/qsemyon/messenger-golang
cd messenger-golang
```

4. Настройка клиента
```Powershell
pip install flet==0.84.0 websockets
```

5. Запуск инфраструктуры
```Powershell
docker-compose up --build
```

6. Запуск мессенджера
- Запустить первое окно чата
```Powershell
python main.py
```
- Запустить второе окно чата
```Powershell
python main.py
```