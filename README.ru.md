# my_skills

Русская точка входа для репозитория.
Главный источник правил маршрутизации все еще в `AGENTS.md`, а подробный технический статус репозитория остается в `README.md`.

## С чего начать

Если тебе нужно именно пользоваться `gamedev`-флоу, а не разбираться во всей внутренней кухне репозитория:

1. Открой `docs/gamedev-quickstart.ru.md`.
2. Потом прочитай `docs/gamedev-guide.ru.md`.
3. Если уперся в непонятный кейс, открой `docs/gamedev-troubleshooting.ru.md`.
4. Если путаются термины, открой `docs/gamedev-glossary.ru.md`.

Если тебе нужно менять сам skill-репозиторий:

1. Начни с `AGENTS.md`.
2. Потом смотри `docs/gamedev-workflow.md`.
3. Для границ со специализированными наложениями смотри `docs/gamedev-specialist-handoffs.md`.

## Коротко про маршрут

Базовый путь:

`concept -> setup-engine -> map-systems -> design-system -> prototype if risky -> bootstrap-project -> implement-system -> assemble-mvp -> playtest-and-tune`

Если у тебя уже есть рабочий MVP и следующая цель не просто доказать, что игровой цикл существует, а показать вменяемую демо-версию, дальше идет дополнительная ветка:

`prepare-demo -> design-system/implement-system -> assemble-mvp -> playtest-and-tune`

Важно: `prepare-demo` не только про UI. Этот шаг описывает демо целиком: читаемость игрового процесса, первые подсказки, HUD, меню, проигрыш и перезапуск, правила по временным заглушкам, нехватку ассетов и план проверки.

Если у тебя есть только концепция и ты хочешь дойти до первого GDD, смотри:

- `docs/gamedev-guide.ru.md`
- `docs/gamedev-quickstart.ru.md`

## Полезные документы

- `docs/gamedev-guide.ru.md`
- `docs/gamedev-quickstart.ru.md`
- `docs/gamedev-troubleshooting.ru.md`
- `docs/gamedev-glossary.ru.md`
- `docs/gamedev-guide.md`
- `README.md`

## Карта репозитория

- `core/`: общие навыки, которые живут и без `gamedev/`
- `gamedev/`: основной игровой процесс, шаблоны и стандарты
- `docs/`: документы по процессу, инструкции и пояснения
- `templates/`: общие шаблоны вне `gamedev/`
- `standards/`: общие короткие правила
- `evals/` и `fixtures/`: регрессии и подготовленные состояния
