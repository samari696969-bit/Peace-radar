# Peace Radar

Стартовый каркас агрегатора публичных официальных региональных предупреждений России.

## Возможности
- Тёмная карта на Leaflet с CARTO Dark basemap на данных OpenStreetMap.
- Региональная сводка и лента публикаций.
- RSS-сборщик с явным allowlist источников.
- SQLite и защита от повторной загрузки одной публикации.
- Минимальный Telegram-бот с командой `/status`.
- Публикация в Telegram через отдельный модуль, выключенный без токенов.

## Запуск локально
```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# Linux/macOS: source .venv/bin/activate
pip install -r requirements.txt
cp sources.json.example sources.json
python app.py
```
Откройте http://127.0.0.1:5000

## Сбор RSS
Заполните `sources.json` реальными HTTPS RSS/Atom-адресами официальных источников.
Для каждого источника укажите название, регион и статус (`info`, `warning`, `all_clear`, `unknown`).
Затем выполните:
```bash
python -m collectors.source_manager
python -m collectors.rss_collector
```
Планировщик запуска RSS-сборщика на Render настраивается отдельно как Cron Job. Не запускайте его внутри web-процесса.

## Telegram
Создайте бота через BotFather и задайте переменные окружения:
- `TELEGRAM_BOT_TOKEN`
- `PUBLIC_BASE_URL`

Запуск:
```bash
python -m bot.telegram_bot
```
Для публикации в канал дополнительно задайте `TELEGRAM_CHANNEL_ID` и используйте `services.publisher.publish()` после проверки сообщения.

## Важно
- Не используйте публичный demo-сервер тайлов OpenStreetMap для массового трафика. Здесь используется CARTO Dark, с атрибуцией OSM и CARTO.
- Соблюдайте условия RSS-источников и ограничения частоты запросов.
- Публикуйте только проверенные сообщения и сохраняйте ссылку на первоисточник.
- Этот каркас показывает региональные статусы, а не точные места происшествий или военные объекты.
- Перед публичным запуском добавьте модерацию, резервное копирование и мониторинг ошибок.
