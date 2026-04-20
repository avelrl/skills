# Gamedev V2 Roadmap

Рабочий документ со следующими кандидатами для развития `gamedev/`.

Статус этого файла:

- это не канонический workflow
- это не обязательный план работ
- это shortlist хороших следующих улучшений после стабилизации текущего MVP -> demo path

Связанные документы:

- `docs/gamedev-workflow.md`
- `docs/gamedev-specialist-handoffs.md`
- `docs/gamedev-guide.md`
- `docs/gamedev-guide.ru.md`

## Контекст

Текущий `gamedev/` уже хорошо работает как orchestration layer:

- routing по шагам
- prerequisite discipline
- artifact-driven workflow
- handoff между generic `gamedev` и specialist overlays
- честная логика evidence, closure и doc sync

Самые заметные следующие улучшения уже лежат не в раннем MVP, а в зоне:

- onboarding
- content planning
- gameplay readability
- packaging
- demo/release honesty
- portability between runtime stacks

## Обязательно

### 1. `release-readiness`

Зачем:
- нужен честный go/no-go шаг для milestone уровня `demo candidate` или `release candidate`
- сейчас есть хорошая сборка MVP и demo-path, но не хватает отдельного closure шага перед релизным решением

Что должен делать:
- писать `reports/release-readiness.md`
- фиксировать ready / blocked / risky
- перечислять blockers, acceptable defects и must-fix before release

Почему это важно:
- снижает самообман на поздних стадиях
- не дает путать `почти работает` и `можно выпускать`

### 2. `first-session-onboarding`

Зачем:
- очень много проблем demo и retention живет в первых 3-5 минутах
- это отдельная задача, которая плохо помещается в общий tuning

Что должен делать:
- проверять first-time player path
- фиксировать start flow, initial objective, controls hinting, first fail/restart clarity
- определять, что именно игрок должен понять за первые минуты

Почему это важно:
- полезно и для Web, и для Unity
- напрямую влияет на качество demo

### 3. `content-slice-planning`

Зачем:
- systems уже могут существовать, а играть все равно не во что
- очень частая проблема: код есть, но нет минимального контентного среза

Что должен делать:
- определять минимально достаточный набор encounter/content units для MVP или demo
- фиксировать enemy sets, rooms, waves, pickups, mission beats или equivalent
- отделять must-have content от nice-to-have content

Почему это важно:
- закрывает дыру между system-complete и play-complete

### 4. `feedback-readability-pass`

Зачем:
- плохая читаемость почти всегда убивает ощущение качества раньше, чем отсутствие контента

Что должен делать:
- проходить по hit feedback, damage feedback, pickups, objective change, fail state, recovery state
- фиксировать, где игрок не понимает, что произошло

Почему это важно:
- напрямую повышает качество demo
- не сводится только к UI, это именно player feedback layer

### 5. `qa-triage`

Зачем:
- playtest findings без triage быстро превращаются в шум

Что должен делать:
- превращать результаты playtest/smoke/manual review в action queue
- сортировать по severity, subsystem, reproduction clarity, owner hint

Почему это важно:
- делает `reports/playtest-report.md` реально операционным документом

## Полезно

### 6. `controls-input-pass`

Зачем:
- input-поведение почти всегда всплывает слишком поздно

Что должен делать:
- проверять keyboard/mouse/gamepad/touch expectations
- фиксировать prompt consistency, pause/input gating, remap expectations

### 7. `save-session-state`

Зачем:
- save/load/checkpoint/settings/resume почти всегда вылезают позже, чем надо

Что должен делать:
- задавать единый контракт для session continuity
- отделять MVP-minimum от later-state complexity

### 8. `copy-and-microtext-pass`

Зачем:
- localization и copy quality это не одно и то же

Что должен делать:
- улучшать player-facing wording
- проверять consistency кнопок, HUD labels, prompts, objective text, short error states

### 9. `package-demo`

Зачем:
- нужен отдельный шаг для подготовки demo-артефакта к передаче людям

Что должен делать:
- определять, что именно отдается тестеру или партнеру
- фиксировать build label, package contents, run instructions, version note, evidence set

### 10. `portability-plan`

Зачем:
- особенно полезно под модель `Web + Unity`
- переносимость лучше закладывать заранее, а не после первого прототипа

Что должен делать:
- отделять engine-agnostic core от runtime glue
- фиксировать data-driven seams, platform glue, port blockers и desired abstractions

### 11. `performance-budget-pass`

Зачем:
- бюджеты можно выбрать рано, но сверять их с реальностью нужно отдельным шагом

Что должен делать:
- сравнивать реальный проект с target budgets
- поднимать scene, draw-call, load-time, memory и asset-size gaps

## Вкусовщина, но годная

### 12. `accessibility-pass`

Зачем:
- часто не первый приоритет, но быстро повышает качество проекта

Что должен делать:
- проверять contrast, readable HUD scale, redundant signaling, reduced motion, subtitle policy

### 13. `audio-surface-pass`

Зачем:
- даже сырой demo резко оживает, когда звук и audio cues собраны осмысленно

Что должен делать:
- картировать UI, reward, danger, impact и fail-state audio cues
- отделять must-have sound surface от later polish

### 14. `art-direction-lite`

Зачем:
- не всегда нужен большой art bible, но нужен короткий visual contract

Что должен делать:
- задавать palette, material language, UI tone, asset acceptance rules, placeholder replacement logic

### 15. `telemetry-lite`

Зачем:
- когда demo начинают гонять внешние люди, полезно видеть хотя бы минимальный funnel

Что должен делать:
- определять небольшой набор signal events
- фиксировать где игроки умирают, отваливаются или теряют понимание цели

## Что не стоит добавлять сейчас

### Не добавлять generic micro-skills вроде:

- `hud-skill`
- `menu-skill`
- `pause-skill`

Почему:
- это лучше выражать как systems внутри `design-system` и `implement-system`
- иначе библиотека быстро расползется в мелкие несвязанные куски

### Не добавлять абстрактный `polish-skill`

Почему:
- это почти всегда мусорная корзина без четкого контракта
- лучше иметь узкие production-facing passes с понятным output

### Не добавлять Unity/Unreal-specific skills заранее

Почему:
- пока нет достаточного числа повторяемых кейсов
- лучше сначала закрепить generic contract, а потом делать engine overlays

## Топ-5 кандидатов на следующую волну

Если выбирать только 5 следующих additions, то лучший порядок сейчас такой:

1. `release-readiness`
2. `first-session-onboarding`
3. `content-slice-planning`
4. `feedback-readability-pass`
5. `portability-plan`

## Practical Recommendation

Лучший следующий принцип:

- не расширять `gamedev/` в ширину хаотично
- добавлять только те steps, у которых есть:
  - понятный trigger
  - понятный output artifact
  - понятное место в flow
  - явная граница со specialist overlays

Если идти по порядку, то логичный следующий кандидат после текущего состояния репозитория:

1. `release-readiness`, если нужна честная поздняя milestone closure
2. `first-session-onboarding`, если цель — повысить качество demo
3. `portability-plan`, если хочется заранее проектировать мост между Web и Unity
