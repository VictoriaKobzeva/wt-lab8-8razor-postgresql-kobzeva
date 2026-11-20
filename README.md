# Лабораторная работа № 8. PostgreSQL и Entity Framework Core в Razor Pages

Проект: **wt-lab8-8razor-postgresql-kobzeva**

Приложение ASP.NET Core Razor Pages для учёта недвижимости. Данные хранятся в
PostgreSQL, доступ выполняется через Entity Framework Core (Code First, миграции).

- **Публичный URL:** <https://wt-lab8-8razor-postgresql-kobzeva.onrender.com>
- **GitHub:** <https://github.com/VictoriaKobzeva/wt-lab8-8razor-postgresql-kobzeva>
- **Отчёт:** [REPORT.md](REPORT.md) · DOCX · PDF
- **Локальная БД:** PostgreSQL 16, `localhost:5432`, база `wt_lab8`, пользователь `postgres`

## Предметная область

Агентство недвижимости. Основная сущность — `Property`:

| Свойство | Тип | Назначение |
|---|---|---|
| `Id` | `int` | Идентификатор |
| `Address` | `string` | Адрес объекта |
| `Type` | `string` | Тип: квартира, дом, офис, замок |
| `Price` | `decimal(18,2)` | Цена |
| `Area` | `double` | Площадь, м² |
| `Rooms` | `int` | Количество комнат |
| `IsAvailable` | `bool` | Доступность |
| `Description` | `string(1000)` | Описание (добавлено миграцией) |

> В шаблоне лабораторной работы используется сущность `Product` и таблица
> `Products`. В проекте сохранена предметная область лабораторных работ № 5–7,
> поэтому сущность называется `Property`, а таблица — `Properties`. Структура
> страниц, маршруты и дизайн WT-5 не изменялись.

## Архитектура

```text
Razor Pages
     ↓
PageModel (IndexModel, CreateModel, EditModel, DetailsModel)
     ↓
AppDbContext
     ↓
Entity Framework Core
     ↓
PostgreSQL
```

## Структура проекта

```text
wt-lab8-8razor-postgresql-kobzeva/
├── Data/
│   └── AppDbContext.cs
├── Models/
│   └── Property.cs
├── Migrations/
│   ├── 20261119115243_InitialCreate.cs
│   ├── 20261119115322_AddPropertyDescription.cs
│   └── AppDbContextModelSnapshot.cs
├── Pages/
│   ├── Products/
│   │   ├── Index.cshtml(.cs)      — список, поиск, удаление
│   │   ├── Create.cshtml(.cs)     — создание
│   │   ├── Edit.cshtml(.cs)       — редактирование
│   │   └── Details.cshtml(.cs)    — просмотр
│   └── Shared/_Layout.cshtml
├── wwwroot/
├── docs/img/                      — скриншоты для отчёта
├── Program.cs
├── appsettings.json
├── Dockerfile
├── render.yaml
└── wt-lab8-8razor-postgresql-kobzeva.csproj
```

## Локальный запуск

1. Создать базу данных PostgreSQL:

```bash
createdb -h localhost -p 5432 -U postgres wt_lab8
```

2. Указать строку подключения в `appsettings.Development.json`:

```json
{
  "ConnectionStrings": {
    "DefaultConnection": "Host=localhost;Port=5432;Database=wt_lab8;Username=postgres;Password=your_password"
  }
}
```

Файл добавлен в `.gitignore`, реальный пароль в репозиторий не попадает.

3. Применить миграции и запустить приложение:

```bash
dotnet restore
dotnet ef database update
dotnet run
```

Приложение слушает порт из переменной `PORT` (по умолчанию `10000`):
<http://localhost:10000/Products>.

При старте приложение автоматически применяет неприменённые миграции
(`db.Database.Migrate()`), поэтому `database update` можно не выполнять отдельно.

## Миграции

```bash
dotnet ef migrations add <Name>
dotnet ef database update
dotnet ef migrations list
```

| Миграция | Назначение |
|---|---|
| `20261119115243_InitialCreate` | Таблицы `Properties` и `__EFMigrationsHistory`, начальные данные |
| `20261119115322_AddPropertyDescription` | Столбец `Description` (`varchar(1000)`) |

## Поиск

Поиск выполняется на стороне PostgreSQL через `EF.Functions.ILike` по адресу,
типу и описанию:

```csharp
var pattern = $"%{Search.Trim()}%";
query = query.Where(p =>
    EF.Functions.ILike(p.Address, pattern) ||
    EF.Functions.ILike(p.Type, pattern) ||
    EF.Functions.ILike(p.Description, pattern));
```

## Docker

```bash
docker build -t wt-lab8-8razor-postgresql .
docker run -p 10000:10000 \
  -e DATABASE_URL="postgres://user:password@host:5432/wt_lab8" \
  wt-lab8-8razor-postgresql
```

Проверка: <http://localhost:10000/Products>

## Render

`Program.cs` поддерживает два источника строки подключения:

- локально — `ConnectionStrings:DefaultConnection`;
- на Render — переменная окружения `DATABASE_URL` (Internal Database URL),
  которая преобразуется в строку подключения Npgsql.

Порт берётся из переменной `PORT` (по умолчанию `10000`), приложение слушает
`http://0.0.0.0:{port}`. Миграции применяются при запуске контейнера.

### Отдельная схема на Render

Бесплатный тариф Render допускает только один активный инстанс PostgreSQL на
аккаунт, поэтому лабораторная работа использует существующий инстанс
`wt-lab7-db-kobzeva`, но работает в отдельной схеме `wt_lab8`. Схема задаётся
переменной окружения `DATABASE_SCHEMA`; в строку подключения добавляется
`Search Path=wt_lab8`, а таблицы `Properties` и `__EFMigrationsHistory`
создаются внутри этой схемы. Данные лабораторной работы № 7 (схема `public`)
не затрагиваются.

```csharp
var databaseSchema = builder.Configuration["DATABASE_SCHEMA"];
connectionString += $";Search Path={databaseSchema}";
```

В каталоге есть `render.yaml` — вариант развёртывания через Blueprint: он создаёт
PostgreSQL и Web Service (Runtime: Docker) и связывает их через `DATABASE_URL`.
В текущем развёртывании использован существующий инстанс PostgreSQL (лимит
Free-тарифа — одна база на аккаунт), а `render.yaml` оставлен как альтернатива.

## Ссылки

- GitHub-репозиторий: <https://github.com/VictoriaKobzeva/wt-lab8-8razor-postgresql-kobzeva>
- Публичный URL Render: <https://wt-lab8-8razor-postgresql-kobzeva.onrender.com>
- Render PostgreSQL: `wt-lab8-db-kobzeva`
- Render Web Service: `wt-lab8-8razor-postgresql-kobzeva` (Docker, free)
