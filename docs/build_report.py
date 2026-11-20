#!/usr/bin/env python3
"""Сборка отчёта по лабораторной работе WT-8 в формате DOCX."""

from pathlib import Path

from docx import Document
from docx.enum.section import WD_SECTION
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_BREAK
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt, RGBColor

ROOT = Path(__file__).resolve().parent.parent
IMG = ROOT / "docs" / "img"
OUT = ROOT / "wt-lab8-kobzeva.docx"

DARK = RGBColor(0x1F, 0x38, 0x64)
MID = RGBColor(0x2E, 0x54, 0x96)
GREY = RGBColor(0x59, 0x59, 0x59)
CODE_BG = "F3F5F8"
HEAD_BG = "DCE6F1"

doc = Document()

# ---------- страница и базовые стили ----------
section = doc.sections[0]
section.page_width = Cm(21)
section.page_height = Cm(29.7)
section.top_margin = Cm(2)
section.bottom_margin = Cm(2)
section.left_margin = Cm(2.5)
section.right_margin = Cm(1.5)

normal = doc.styles["Normal"]
normal.font.name = "Times New Roman"
normal.font.size = Pt(12)
normal.element.rPr.rFonts.set(qn("w:eastAsia"), "Times New Roman")
normal.paragraph_format.line_spacing = 1.15
normal.paragraph_format.space_after = Pt(4)

for name, size, color in (("Heading 1", 16, DARK), ("Heading 2", 13, MID)):
    st = doc.styles[name]
    st.font.name = "Times New Roman"
    st.element.rPr.rFonts.set(qn("w:eastAsia"), "Times New Roman")
    st.font.size = Pt(size)
    st.font.bold = True
    st.font.color.rgb = color
    st.paragraph_format.space_before = Pt(14 if size == 16 else 10)
    st.paragraph_format.space_after = Pt(6)
    st.paragraph_format.keep_with_next = True


def shade(paragraph, fill):
    pPr = paragraph._p.get_or_add_pPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"), fill)
    pPr.append(shd)


def borders(paragraph, color="D0D7E2"):
    pPr = paragraph._p.get_or_add_pPr()
    pBdr = OxmlElement("w:pBdr")
    for edge in ("top", "left", "bottom", "right"):
        el = OxmlElement(f"w:{edge}")
        el.set(qn("w:val"), "single")
        el.set(qn("w:sz"), "6")
        el.set(qn("w:space"), "4")
        el.set(qn("w:color"), color)
        pBdr.append(el)
    pPr.append(pBdr)


def code(text, size=8.6):
    p = doc.add_paragraph()
    pf = p.paragraph_format
    pf.space_before = Pt(2)
    pf.space_after = Pt(8)
    pf.left_indent = Cm(0.25)
    pf.right_indent = Cm(0.1)
    pf.line_spacing = 1.0
    shade(p, CODE_BG)
    borders(p)
    run = p.add_run(text.rstrip())
    run.font.name = "Consolas"
    run._element.rPr.rFonts.set(qn("w:eastAsia"), "Consolas")
    run.font.size = Pt(size)
    return p


def para(text="", bold=False, italic=False, align=None, size=None, color=None,
         space_after=None):
    p = doc.add_paragraph()
    if align is not None:
        p.alignment = align
    if space_after is not None:
        p.paragraph_format.space_after = Pt(space_after)
    run = p.add_run(text)
    run.bold = bold
    run.italic = italic
    if size:
        run.font.size = Pt(size)
    if color:
        run.font.color.rgb = color
    return p


def bullets(items):
    for item in items:
        p = doc.add_paragraph(style="List Bullet")
        p.paragraph_format.space_after = Pt(2)
        p.add_run(item)


def caption(text):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(10)
    run = p.add_run(text)
    run.italic = True
    run.font.size = Pt(9.5)
    run.font.color.rgb = GREY


def image(name, width=15.4, cap=None):
    path = IMG / name
    if not path.exists():
        return False
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(4)
    p.paragraph_format.space_after = Pt(0)
    p.add_run().add_picture(str(path), width=Cm(width))
    if cap:
        caption(cap)
    return True


def table(headers, rows, widths=None, font=10.5):
    t = doc.add_table(rows=1, cols=len(headers))
    t.style = "Table Grid"
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    hdr = t.rows[0].cells
    for i, h in enumerate(headers):
        hdr[i].text = ""
        p = hdr[i].paragraphs[0]
        run = p.add_run(h)
        run.bold = True
        run.font.size = Pt(font)
        shade(p, HEAD_BG)
    for row in rows:
        cells = t.add_row().cells
        for i, value in enumerate(row):
            cells[i].text = ""
            p = cells[i].paragraphs[0]
            run = p.add_run(str(value))
            run.font.size = Pt(font)
    if widths:
        for row in t.rows:
            for i, w in enumerate(widths):
                row.cells[i].width = Cm(w)
    doc.add_paragraph().paragraph_format.space_after = Pt(2)
    return t


def add_page_numbers():
    footer = doc.sections[0].footer
    p = footer.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run()
    fld = OxmlElement("w:fldSimple")
    fld.set(qn("w:instr"), "PAGE")
    run._r.addnext(fld)


# ---------- титульная страница ----------
for _ in range(4):
    doc.add_paragraph()

para("Лабораторная работа WT-8", bold=True, align=WD_ALIGN_PARAGRAPH.CENTER,
     size=16, color=MID, space_after=12)
para("Подключение PostgreSQL к приложению Razor Pages\n"
     "с использованием Entity Framework Core", bold=True,
     align=WD_ALIGN_PARAGRAPH.CENTER, size=24, color=DARK, space_after=24)
para("Дисциплина: Web-технологии", align=WD_ALIGN_PARAGRAPH.CENTER,
     size=13, space_after=2)
para("Проект: wt-lab8-8razor-postgresql-kobzeva", align=WD_ALIGN_PARAGRAPH.CENTER,
     size=13, space_after=2)
para("Выполнила: Кобзева Виктория, группа УИР-1", align=WD_ALIGN_PARAGRAPH.CENTER,
     size=13, space_after=2)
para("Дата: 19.11.2026", align=WD_ALIGN_PARAGRAPH.CENTER, size=13, space_after=2)

for _ in range(6):
    doc.add_paragraph()

para("GitHub:", bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, size=12)
para("https://github.com/VictoriaKobzeva/wt-lab8-8razor-postgresql-kobzeva",
     align=WD_ALIGN_PARAGRAPH.CENTER, size=11, color=MID, space_after=8)
para("Опубликованное приложение:", bold=True,
     align=WD_ALIGN_PARAGRAPH.CENTER, size=12)
para("https://wt-lab8-8razor-postgresql-kobzeva.onrender.com",
     align=WD_ALIGN_PARAGRAPH.CENTER, size=11, color=MID)
doc.add_page_break()

# ---------- цель ----------
doc.add_heading("1. Цель работы", level=1)
para("Подключить приложение Razor Pages, разработанное в лабораторной работе WT-5, "
     "к базе данных PostgreSQL с использованием Entity Framework Core.")
para("В ходе работы необходимо было:")
bullets([
    "подключить PostgreSQL к существующему приложению Razor Pages;",
    "создать AppDbContext и настроить Entity Framework Core;",
    "создать структуру базы данных с помощью миграций;",
    "заменить хранение данных в памяти (PropertyStore) на PostgreSQL;",
    "реализовать CRUD-операции и поиск данных;",
    "изменить модель данных и обновить структуру БД с помощью миграции;",
    "подготовить Dockerfile и опубликовать приложение на Render;",
    "подключить опубликованное приложение к PostgreSQL.",
])

para("Итоговая архитектура приложения:", bold=True)
code("""Razor Pages
     ↓
PageModel
     ↓
AppDbContext
     ↓
Entity Framework Core
     ↓
PostgreSQL""")

# ---------- исходный проект ----------
doc.add_heading("2. Исходный проект и предметная область", level=1)
para("За основу взято приложение из лабораторной работы WT-5 "
     "(wt-lab5-5razor-kobzeva). Создана его копия "
     "wt-lab8-8razor-postgresql-kobzeva. Структура страниц, маршруты и дизайн "
     "приложения сохранены.")
para("Предметная область — агентство недвижимости. В WT-5 данные хранились "
     "в оперативной памяти в статическом классе PropertyStore:")
code("""Razor Pages
    ↓
PropertyStore
    ↓
List<Property>""")
para("В WT-8 источник данных заменён на PostgreSQL:")
code("""Razor Pages
    ↓
AppDbContext
    ↓
Entity Framework Core
    ↓
PostgreSQL""")
para("В шаблоне лабораторной работы используется сущность Product и таблица "
     "Products. В проекте сохранена предметная область лабораторных работ "
     "№ 5–7, поэтому сущность называется Property, а таблица — Properties. "
     "Набор операций и структура базы данных полностью соответствуют заданию.")
para("Файл Data/PropertyStore.cs удалён, все обращения к нему заменены работой "
     "с AppDbContext.")

# ---------- структура проекта ----------
doc.add_heading("3. Структура проекта", level=1)
code("""wt-lab8-8razor-postgresql-kobzeva/
│
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
│   │   ├── Index.cshtml / Index.cshtml.cs
│   │   ├── Create.cshtml / Create.cshtml.cs
│   │   ├── Edit.cshtml / Edit.cshtml.cs
│   │   └── Details.cshtml / Details.cshtml.cs
│   └── Shared/_Layout.cshtml
├── wwwroot/
├── docs/img/                  — скриншоты для отчёта
├── Program.cs
├── appsettings.json
├── Dockerfile
├── render.yaml
└── wt-lab8-8razor-postgresql-kobzeva.csproj""")

# ---------- модель ----------
doc.add_heading("4. Модель данных Property", level=1)
para("Исходная модель WT-5 дополнена свойством Description (см. раздел 11). "
     "Итоговая модель:")
code("""using System.ComponentModel.DataAnnotations;

namespace wt_lab8_8razor_postgresql_kobzeva.Models;

public class Property
{
    public int Id { get; set; }

    [Required(ErrorMessage = "Адрес обязателен")]
    [StringLength(200, ErrorMessage = "Адрес не должен превышать 200 символов")]
    public string Address { get; set; } = string.Empty;

    [Required(ErrorMessage = "Тип обязателен")]
    public string Type { get; set; } = string.Empty;

    [Range(0.01, 1_000_000_000, ErrorMessage = "Цена должна быть от 0.01 до 1 млрд")]
    public decimal Price { get; set; }

    [Range(0.1, 100000, ErrorMessage = "Площадь должна быть от 0.1 до 100000")]
    public double Area { get; set; }

    [Range(1, 1000, ErrorMessage = "Количество комнат от 1 до 1000")]
    public int Rooms { get; set; }

    public bool IsAvailable { get; set; }

    [StringLength(1000, ErrorMessage = "Описание не должно превышать 1000 символов")]
    public string Description { get; set; } = string.Empty;
}""")
table(["Свойство", "Тип C#", "Тип PostgreSQL", "Назначение"],
      [["Id", "int", "integer, identity", "Первичный ключ"],
       ["Address", "string", "varchar(200)", "Адрес объекта"],
       ["Type", "string", "text", "Тип объекта"],
       ["Price", "decimal", "numeric(18,2)", "Цена"],
       ["Area", "double", "double precision", "Площадь, м²"],
       ["Rooms", "int", "integer", "Количество комнат"],
       ["IsAvailable", "bool", "boolean", "Доступность"],
       ["Description", "string", "varchar(1000)", "Описание"]],
      widths=[3.2, 3.0, 4.4, 5.2])

# ---------- AppDbContext ----------
doc.add_heading("5. AppDbContext", level=1)
para("Создан файл Data/AppDbContext.cs. Контекст обеспечивает доступ к таблице "
     "Properties и содержит начальные данные, перенесённые из PropertyStore:")
code("""using Microsoft.EntityFrameworkCore;
using wt_lab8_8razor_postgresql_kobzeva.Models;

namespace wt_lab8_8razor_postgresql_kobzeva.Data;

public class AppDbContext : DbContext
{
    public AppDbContext(DbContextOptions<AppDbContext> options)
        : base(options)
    {
    }

    public DbSet<Property> Properties => Set<Property>();

    protected override void OnModelCreating(ModelBuilder modelBuilder)
    {
        base.OnModelCreating(modelBuilder);

        modelBuilder.Entity<Property>(entity =>
        {
            // Денежные значения хранятся в PostgreSQL как numeric(18, 2).
            entity.Property(p => p.Price).HasPrecision(18, 2);

            // Начальные данные, перенесённые из PropertyStore (WT-5).
            entity.HasData(
                new Property { Id = 1, Address = "Тридевятое царство, замок принцессы",
                    Type = "Замок", Price = 999999m, Area = 500, Rooms = 20,
                    IsAvailable = true,
                    Description = "Замок с привидением, рвом и собственным садом" },
                // ... всего шесть объектов
            );
        });
    }
}""")
para("DbSet<Property> Properties представляет набор сущностей Property, "
     "с которым выполняются операции чтения, добавления, изменения и удаления. "
     "Конфигурация HasPrecision задаёт точный тип numeric(18,2) для цены.")

# ---------- подключение ----------
doc.add_heading("6. Подключение PostgreSQL и строка подключения", level=1)
para("Установлены пакеты:")
code("""dotnet add package Npgsql.EntityFrameworkCore.PostgreSQL --version 8.0.11
dotnet add package Microsoft.EntityFrameworkCore.Design --version 8.0.11
dotnet tool update --global dotnet-ef""")
para("Проверка инструмента dotnet-ef:")
code("""Entity Framework Core .NET Command-line Tools
8.0.11""")
para("Создана база данных wt_lab8. Параметры локального подключения:")
table(["Параметр", "Значение"],
      [["Host", "localhost"],
       ["Port", "5432"],
       ["Database", "wt_lab8"],
       ["Username", "postgres"],
       ["Password", "не указывается в отчёте и в Git (хранится в appsettings.Development.json)"]],
      widths=[4.0, 11.8])
para("Строка подключения находится в appsettings.Development.json, который "
     "добавлен в .gitignore:")
code("""{
  "ConnectionStrings": {
    "DefaultConnection": "Host=localhost;Port=5432;Database=wt_lab8;Username=postgres;Password=your_password"
  }
}""")
para("В Program.cs зарегистрированы AppDbContext и провайдер Npgsql:")
code("""var connectionString = builder.Configuration.GetConnectionString("DefaultConnection");
var databaseUrl = builder.Configuration["DATABASE_URL"];

if (!string.IsNullOrWhiteSpace(databaseUrl))
{
    var uri = new Uri(databaseUrl);
    var userInfo = uri.UserInfo.Split(':', 2);
    var dbPort = uri.Port > 0 ? uri.Port : 5432;
    // Render: внутреннее подключение (host без домена) не использует TLS,
    // внешнее подключение (host с доменом) требует SSL.
    var sslMode = uri.Host.Contains('.') ? "Require" : "Disable";

    connectionString =
        $"Host={uri.Host};" +
        $"Port={dbPort};" +
        $"Database={uri.AbsolutePath.TrimStart('/')};" +
        $"Username={Uri.UnescapeDataString(userInfo[0])};" +
        $"Password={Uri.UnescapeDataString(userInfo[1])};" +
        $"SSL Mode={sslMode}";
}

builder.Services.AddDbContext<AppDbContext>(options =>
    options.UseNpgsql(connectionString));

builder.Services.AddRazorPages();""")

# ---------- миграции ----------
doc.add_heading("7. Миграции и создание структуры базы данных", level=1)
para("Первая миграция создана командой:")
code("""dotnet ef migrations add InitialCreate
dotnet ef database update""")
para("В каталоге Migrations появились файлы InitialCreate, а в базе данных — "
     "таблицы Properties и __EFMigrationsHistory. Результат выполнения "
     "database update:")
code("""Build started...
Build succeeded.
Applying migration '20261119115243_InitialCreate'.
Done.""")
para("После изменения модели (добавления Description) создана вторая миграция:")
code("""dotnet ef migrations add AddPropertyDescription
dotnet ef database update

Applying migration '20261119115322_AddPropertyDescription'.
Done.""")
table(["Миграция", "Назначение"],
      [["20261119115243_InitialCreate",
        "Создание таблиц Properties и __EFMigrationsHistory, начальные данные"],
       ["20261119115322_AddPropertyDescription",
        "Добавление столбца Description (varchar(1000)) без потери данных"]],
      widths=[7.3, 8.5])
para("При запуске приложение автоматически применяет неприменённые миграции:")
code("""using (var scope = app.Services.CreateScope())
{
    var db = scope.ServiceProvider.GetRequiredService<AppDbContext>();
    db.Database.Migrate();
}""")

# ---------- структура БД ----------
doc.add_heading("8. Структура таблицы Properties", level=1)
para("Структура таблицы после применения обеих миграций (pgAdmin 4, база wt_lab8):")
image("09-db-structure.jpeg", 16.4,
      "Рис. 1. Структура таблицы Properties в pgAdmin 4")
para("Таблица содержит первичный ключ PK_Properties, поля Address, Type, Price "
     "(numeric(18,2)), Area, Rooms, IsAvailable и добавленное поле Description. "
     "Структура соответствует модели Property.")
para("История применённых миграций хранится в таблице __EFMigrationsHistory:")
image("10-migrations-history.jpeg", 16.0,
      "Рис. 2. Содержимое таблицы __EFMigrationsHistory в pgAdmin 4")
table(["MigrationId", "ProductVersion"],
      [["20261119115243_InitialCreate", "8.0.11"],
       ["20261119115322_AddPropertyDescription", "8.0.11"]],
      widths=[9.4, 4.0])

# ---------- интеграция ----------
doc.add_heading("9. Подключение Razor Pages к Entity Framework Core", level=1)
para("Файл Data/PropertyStore.cs удалён. Страницы Products получают данные из "
     "PostgreSQL через внедрённый AppDbContext. PageModel списка товаров:")
code("""public class IndexModel : PageModel
{
    private readonly AppDbContext _context;

    public IndexModel(AppDbContext context)
    {
        _context = context;
    }

    public List<Property> Properties { get; set; } = new();

    [BindProperty(SupportsGet = true)]
    public string? Search { get; set; }

    public async Task OnGetAsync()
    {
        var query = _context.Properties.AsQueryable();

        if (!string.IsNullOrWhiteSpace(Search))
        {
            var pattern = $"%{Search.Trim()}%";
            query = query.Where(p =>
                EF.Functions.ILike(p.Address, pattern) ||
                EF.Functions.ILike(p.Type, pattern) ||
                EF.Functions.ILike(p.Description, pattern));
        }

        Properties = await query
            .OrderBy(p => p.Address)
            .ToListAsync();
    }
}""")
para("Список объектов, загруженный из PostgreSQL:")
image("01-products-list.jpeg", 10.8,
      "Рис. 3. Список объектов недвижимости из PostgreSQL")

# ---------- CRUD ----------
doc.add_heading("10. Реализация CRUD-операций", level=1)

doc.add_heading("10.1. Create — создание объекта", level=2)
code("""[BindProperty]
public Property Property { get; set; } = new();

public async Task<IActionResult> OnPostAsync()
{
    if (!ModelState.IsValid)
    {
        return Page();
    }

    _context.Properties.Add(Property);
    await _context.SaveChangesAsync();

    return RedirectToPage("./Index");
}""")
para("Через веб-интерфейс добавлен объект «Гомель, ул. Советская, 7, кв. 15»:")
image("02-product-create-form.jpeg", 13.2,
      "Рис. 4. Форма создания объекта")
image("03-product-created.jpeg", 10.8,
      "Рис. 5. Новый объект сохранён в PostgreSQL (Id = 7)")

doc.add_heading("10.2. Read — чтение данных", level=2)
para("Список получается методом ToListAsync(), отдельная запись — FindAsync():")
code("""public async Task<IActionResult> OnGetAsync(int? id)
{
    if (id == null)
    {
        return NotFound();
    }

    Property = await _context.Properties.FindAsync(id);

    if (Property == null)
    {
        return NotFound();
    }

    return Page();
}""")
image("07-details.jpeg", 12.6,
      "Рис. 6. Страница просмотра объекта (Read)")

doc.add_heading("10.3. Update — редактирование объекта", level=2)
code("""public async Task<IActionResult> OnGetAsync(int? id)
{
    if (id == null) return NotFound();

    var property = await _context.Properties.FindAsync(id);
    if (property == null) return NotFound();

    Property = property;
    return Page();
}

public async Task<IActionResult> OnPostAsync()
{
    if (!ModelState.IsValid) return Page();

    var existing = await _context.Properties.FindAsync(Property.Id);
    if (existing == null) return NotFound();

    existing.Address = Property.Address;
    existing.Type = Property.Type;
    existing.Price = Property.Price;
    existing.Area = Property.Area;
    existing.Rooms = Property.Rooms;
    existing.IsAvailable = Property.IsAvailable;
    existing.Description = Property.Description;

    await _context.SaveChangesAsync();

    return RedirectToPage("./Index");
}""")
image("04-product-edit-form.jpeg", 13.2,
      "Рис. 7. Форма редактирования объекта")
image("05-product-edited.jpeg", 10.8,
      "Рис. 8. Изменения сохранены: цена 85 000 → 79 900 BYN")

doc.add_heading("10.4. Delete — удаление объекта", level=2)
code("""public async Task<IActionResult> OnPostDeleteAsync(int id)
{
    var property = await _context.Properties.FindAsync(id);

    if (property != null)
    {
        _context.Properties.Remove(property);
        await _context.SaveChangesAsync();
    }

    return RedirectToPage("./Index");
}""")
para("После удаления тестового объекта в таблице осталось шесть записей:")
image("08-product-deleted.jpeg", 10.8,
      "Рис. 9. Объект удалён из PostgreSQL")

# ---------- поиск ----------
doc.add_heading("11. Поиск данных", level=1)
para("Добавлено свойство Search с поддержкой GET-параметра и поле поиска на "
     "странице списка:")
code("""[BindProperty(SupportsGet = true)]
public string? Search { get; set; }

var pattern = $"%{Search.Trim()}%";
query = query.Where(p =>
    EF.Functions.ILike(p.Address, pattern) ||
    EF.Functions.ILike(p.Type, pattern) ||
    EF.Functions.ILike(p.Description, pattern));""")
para("Поиск выполняется на стороне PostgreSQL без учёта регистра. "
     "Результат поиска по запросу «Минск» — два объекта:")
image("06-search.jpeg", 14.2,
      "Рис. 10. Поиск по адресу, типу и описанию")
para("Для поиска использован метод ILike провайдера Npgsql. Это важно: "
     "функция lower() в PostgreSQL зависит от локали базы данных, поэтому "
     "для корректной работы с кириллицей база создана с кодировкой UTF8 и "
     "локалью en_US.UTF-8.")

# ---------- изменение модели ----------
doc.add_heading("12. Изменение модели и новая миграция", level=1)
para("В модель Property добавлено свойство:")
code("""public string Description { get; set; } = "";""")
para("Создана и применена миграция AddPropertyDescription:")
code("""dotnet ef migrations add AddPropertyDescription
dotnet ef database update""")
para("Сгенерированная миграция добавляет столбец и заполняет описания для "
     "существующих записей:")
code("""migrationBuilder.AddColumn<string>(
    name: "Description",
    table: "Properties",
    type: "character varying(1000)",
    maxLength: 1000,
    nullable: false,
    defaultValue: "");

migrationBuilder.UpdateData(
    table: "Properties",
    keyColumn: "Id",
    keyValue: 1,
    column: "Description",
    value: "Замок с привидением, рвом и собственным садом");""")
para("После миграции в таблице появился столбец Description, а ранее созданные "
     "записи сохранились. Обновлённая структура таблицы показана на рис. 1 "
     "(раздел 8). Данные в таблице:")
image("11-db-data.jpeg", 16.0,
      "Рис. 11. Данные таблицы Properties после миграции (pgAdmin 4)")
para("На страницах создания, редактирования, просмотра и в карточке списка "
     "добавлено отображение описания. Поиск также учитывает Description.")

# ---------- проверка сохранности ----------
doc.add_heading("13. Проверка сохранности данных", level=1)
para("Приложение остановлено и запущено повторно командой dotnet run. "
     "После перезапуска все шесть объектов, созданных и изменённых через "
     "веб-интерфейс, остались в базе данных. Это подтверждает, что данные "
     "хранятся в PostgreSQL, а не в памяти приложения.")
code("""$ curl http://localhost:10000/Products
Количество объектов: 6

$ psql -U postgres -d wt_lab8 -c 'SELECT count(*) FROM "Properties";'
 count
-------
     6
(1 row)""")

# ---------- Docker ----------
doc.add_heading("14. Docker", level=1)
para("Создан Dockerfile с многоэтапной сборкой:")
code("""FROM mcr.microsoft.com/dotnet/sdk:8.0 AS build
WORKDIR /src
COPY . .
RUN dotnet restore
RUN dotnet publish -c Release -o /app/publish /p:UseAppHost=false

FROM mcr.microsoft.com/dotnet/aspnet:8.0 AS final
WORKDIR /app
COPY --from=build /app/publish .
ENV ASPNETCORE_ENVIRONMENT=Production
EXPOSE 10000
ENTRYPOINT ["dotnet", "wt-lab8-8razor-postgresql-kobzeva.dll"]""")
para("Приложение читает порт из переменной окружения PORT:")
code("""var port = Environment.GetEnvironmentVariable("PORT") ?? "10000";
app.Run($"http://0.0.0.0:{port}");""")
para("Команды локального запуска контейнера:")
code("""docker build -t wt-lab8-8razor-postgresql .
docker run -p 10000:10000 \\
  -e DATABASE_URL="postgres://user:password@host:5432/wt_lab8" \\
  wt-lab8-8razor-postgresql""")
para("Тот же Dockerfile используется на Render (Runtime: Docker), поэтому "
     "опубликованное приложение собирается и запускается в контейнере. "
     "Переменная DATABASE_URL передаётся в контейнер через настройки "
     "Web Service и не хранится в исходном коде.")

# ---------- GitHub ----------
doc.add_heading("15. GitHub-репозиторий", level=1)
para("Проект опубликован в GitHub:")
para("https://github.com/VictoriaKobzeva/wt-lab8-8razor-postgresql-kobzeva",
     bold=True, color=MID)
image("12-github-repo.jpeg", 15.0, "Рис. 12. Репозиторий проекта на GitHub")
para("В репозитории размещены исходный код, модель, AppDbContext, миграции, "
     "Dockerfile, render.yaml, README и отчёт. Файл appsettings.Development.json "
     "с локальным паролем добавлен в .gitignore и в GitHub не попадает. "
     "История коммитов:")
code("""a559a14 Подключение PostgreSQL и Entity Framework Core""")

# ---------- Render ----------
doc.add_heading("16. Публикация на Render", level=1)
para("На Render создан Web Service (Runtime: Docker), подключённый к "
     "GitHub-репозиторию. Строка подключения к PostgreSQL передаётся "
     "в приложение через переменную окружения DATABASE_URL (Internal Database URL), "
     "а имя схемы — через DATABASE_SCHEMA.")
para("Схема подключения:")
code("""Application
      ↓
Environment Variables (DATABASE_URL, DATABASE_SCHEMA)
      ↓
PostgreSQL (схема wt_lab8)""")
para("Параметры Render:")
table(["Ресурс", "Значение"],
      [["PostgreSQL", "инстанс wt-lab7-db-kobzeva, Frankfurt, Free"],
       ["Схема лабораторной работы", "wt_lab8 (переменная DATABASE_SCHEMA)"],
       ["Web Service", "wt-lab8-8razor-postgresql-kobzeva, Docker, Free"],
       ["Переменные окружения", "DATABASE_URL, DATABASE_SCHEMA"],
       ["Публичный URL", "https://wt-lab8-8razor-postgresql-kobzeva.onrender.com"]],
      widths=[5.2, 10.6])
para("Бесплатный тариф Render разрешает только один активный инстанс PostgreSQL "
     "на аккаунт, поэтому приложение использует существующий инстанс "
     "лабораторной работы № 7, но работает в отдельной схеме wt_lab8. "
     "Переменная DATABASE_SCHEMA добавляет в строку подключения Search Path, "
     "а история миграций и таблица Properties создаются внутри этой схемы. "
     "Схема public с данными WT-7 не изменяется.")
para("При запуске контейнера выполняется db.Database.Migrate(), поэтому "
     "структура удалённой базы создаётся автоматически.")
if IMG.joinpath("13-render-app.jpeg").exists():
    image("13-render-app.jpeg", 15.0,
          "Рис. 13. Опубликованное приложение на Render")
    if IMG.joinpath("14-render-logs.jpeg").exists():
        image("14-render-logs.jpeg", 15.0,
              "Рис. 14. Логи Render: применение миграций и запросы EF Core")
else:
    para("[Скриншот опубликованного приложения добавляется после деплоя.]",
         italic=True, color=GREY)

# ---------- результаты ----------
doc.add_heading("17. Результаты проверки работоспособности", level=1)
table(["Операция", "Где проверено", "Результат"],
      [["Открытие главной страницы", "/", "200 OK"],
       ["Список объектов", "/Products", "6 объектов из PostgreSQL"],
       ["Создание", "/Products/Create", "Объект добавлен, Id = 7"],
       ["Просмотр", "/Products/Details?id=4", "Данные объекта отображаются"],
       ["Редактирование", "/Products/Edit?id=7", "Цена 85 000 → 79 900 BYN"],
       ["Удаление", "Кнопка «Удалить»", "Объект удалён, осталось 6"],
       ["Поиск «Минск»", "/Products?Search=Минск", "Найдено 2 объекта"],
       ["Перезапуск приложения", "dotnet run", "Все 6 записей сохранились"],
       ["Таблица Properties", "pgAdmin 4", "8 столбцов, PK_Properties"],
       ["__EFMigrationsHistory", "pgAdmin 4", "2 применённые миграции"],
       ["Публикация на Render", "/Products (onrender.com)", "200 OK, 6 объектов, схема wt_lab8"]],
      widths=[4.8, 5.4, 5.6], font=10)

# ---------- вывод ----------
doc.add_heading("18. Вывод", level=1)
para("В ходе работы приложение Razor Pages из WT-5 подключено к PostgreSQL "
     "через Entity Framework Core. Хранилище PropertyStore заменено на "
     "AppDbContext, созданы две миграции, реализованы операции создания, "
     "чтения, редактирования, удаления и поиска. Проверено, что данные "
     "сохраняются после перезапуска приложения, а изменение модели приводит "
     "к обновлению структуры базы без потери существующих записей.")
para("Приложение подготовлено к работе в Docker и опубликовано на Render, "
     "где используется удалённая база PostgreSQL. Параметры подключения "
     "хранятся в переменных окружения и не попадают в GitHub.")

# ---------- приложение ----------
doc.add_page_break()
doc.add_heading("Приложение А. Контрольные вопросы", level=1)
qa = [
    ("Что такое ORM?",
     "Object-Relational Mapping — технология сопоставления объектов языка "
     "программирования таблицам реляционной базы данных."),
    ("Для чего используется Entity Framework Core?",
     "Это ORM для .NET: позволяет работать с базой через C#-классы и LINQ "
     "без написания SQL вручную."),
    ("Какую задачу выполняет DbContext?",
     "Представляет сессию работы с базой: отслеживает изменения сущностей, "
     "формирует запросы и сохраняет данные."),
    ("Что такое DbSet?",
     "Набор сущностей одного типа, через который выполняются запросы и "
     "операции добавления/удаления."),
    ("Для чего используется Npgsql.EntityFrameworkCore.PostgreSQL?",
     "Это провайдер EF Core для PostgreSQL: переводит LINQ в SQL диалекта "
     "PostgreSQL и управляет подключением."),
    ("Что такое Code First?",
     "Подход, при котором структура базы создаётся по C#-моделям и миграциям, "
     "а не наоборот."),
    ("Что такое миграция EF Core?",
     "Файл с инструкциями изменения схемы базы данных, созданный по разнице "
     "между моделью и предыдущим состоянием."),
    ("Для чего используется dotnet ef migrations add?",
     "Создаёт новую миграцию на основе изменений модели."),
    ("Для чего используется dotnet ef database update?",
     "Применяет неприменённые миграции к базе данных."),
    ("Что такое __EFMigrationsHistory?",
     "Служебная таблица с идентификаторами уже применённых миграций."),
    ("Как EF Core определяет структуру таблицы?",
     "По классам модели, атрибутам и конфигурации в OnModelCreating."),
    ("Как класс Property связан с таблицей Properties?",
     "Через DbSet<Property> и соглашение об имени: имя DbSet используется "
     "как имя таблицы."),
    ("Для чего используется SaveChangesAsync()?",
     "Сохраняет накопленные изменения сущностей в базе данных асинхронно."),
    ("Чем Add() отличается от Remove()?",
     "Add() помечает сущность для вставки, Remove() — для удаления."),
    ("Для чего используется FindAsync()?",
     "Ищет сущность по первичному ключу, сначала в кэше контекста, затем в базе."),
    ("Что такое CRUD?",
     "Create, Read, Update, Delete — четыре базовые операции с данными."),
    ("Как реализуется операция Create?",
     "Создать объект, вызвать DbSet.Add() и SaveChangesAsync()."),
    ("Как реализуется операция Read?",
     "Запросить данные через DbSet с помощью LINQ, ToListAsync() или FindAsync()."),
    ("Как реализуется операция Update?",
     "Получить сущность, изменить её свойства и вызвать SaveChangesAsync()."),
    ("Как реализуется операция Delete?",
     "Получить сущность, вызвать DbSet.Remove() и SaveChangesAsync()."),
    ("Для чего используется LINQ?",
     "Для типизированных запросов к коллекциям и базам данных прямо в C#."),
    ("Что делает метод Where()?",
     "Фильтрует последовательность по заданному условию."),
    ("Что делает метод OrderBy()?",
     "Сортирует последовательность по возрастанию указанного ключа."),
    ("Для чего используется ToListAsync()?",
     "Асинхронно выполняет запрос и возвращает список результатов."),
    ("Как реализовать поиск с использованием LINQ?",
     "Добавить в запрос Where() с условием Contains/ILike по нужным полям."),
    ("Что происходит при изменении модели после создания базы?",
     "Модель и схема базы расходятся; EF Core требует новую миграцию."),
    ("Зачем после изменения модели создавать новую миграцию?",
     "Чтобы применить изменение схемы к базе без потери данных."),
    ("Что происходит с существующими данными при применении миграции?",
     "Они сохраняются, если миграция не удаляет столбцы и не меняет типы "
     "несовместимым образом."),
    ("Что такое Dockerfile?",
     "Файл с инструкциями сборки Docker-образа приложения."),
    ("Для чего используется переменная PORT?",
     "Указывает порт, на котором приложение слушает входящие подключения; "
     "хостинг задаёт её автоматически."),
    ("Зачем приложение должно принимать подключения на 0.0.0.0?",
     "Чтобы контейнер принимал подключения извне, а не только с localhost."),
    ("Для чего используется Render?",
     "Облачная платформа для публикации веб-приложений и баз данных."),
    ("Где должны храниться параметры подключения к удалённой базе?",
     "В переменных окружения или секретах хостинга, а не в коде."),
    ("Почему пароль PostgreSQL нельзя хранить в GitHub?",
     "Репозиторий могут увидеть посторонние; пароль даёт доступ к базе данных."),
    ("Как проверить, что опубликованное приложение использует PostgreSQL?",
     "Создать/изменить запись на сайте, перезапустить сервис и убедиться, что "
     "данные сохранились, а также проверить их запросом к базе."),
]
table(["Вопрос", "Ответ"], qa, widths=[6.2, 9.6], font=9.5)

add_page_numbers()
doc.core_properties.title = "Лабораторная работа WT-8"
doc.core_properties.author = "Кобзева Виктория"
doc.core_properties.subject = "Razor Pages + Entity Framework Core + PostgreSQL"

doc.save(OUT)
print(f"Сохранено: {OUT}")
