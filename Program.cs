using Microsoft.AspNetCore.HttpOverrides;
using Microsoft.EntityFrameworkCore;
using wt_lab8_8razor_postgresql_kobzeva.Data;

var builder = WebApplication.CreateBuilder(args);

// Строка подключения: локально — ConnectionStrings:DefaultConnection,
// на Render — переменная окружения DATABASE_URL.
var connectionString = builder.Configuration.GetConnectionString("DefaultConnection");
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

if (string.IsNullOrWhiteSpace(connectionString))
{
    throw new InvalidOperationException(
        "Не задана строка подключения. Укажите ConnectionStrings:DefaultConnection " +
        "или переменную окружения DATABASE_URL.");
}

// Регистрация AppDbContext с провайдером PostgreSQL.
builder.Services.AddDbContext<AppDbContext>(options =>
    options.UseNpgsql(connectionString));

builder.Services.AddRazorPages();

// Render и другие reverse-proxy передают реальную схему запроса в X-Forwarded-Proto.
builder.Services.Configure<ForwardedHeadersOptions>(options =>
{
    options.ForwardedHeaders =
        ForwardedHeaders.XForwardedFor | ForwardedHeaders.XForwardedProto;
    options.KnownNetworks.Clear();
    options.KnownProxies.Clear();
});

var app = builder.Build();

// Для учебного проекта миграции применяются автоматически при запуске.
using (var scope = app.Services.CreateScope())
{
    var db = scope.ServiceProvider.GetRequiredService<AppDbContext>();
    db.Database.Migrate();
}

if (!app.Environment.IsDevelopment())
{
    app.UseExceptionHandler("/Error");
    // The default HSTS value is 30 days. You may want to change this for production scenarios, see https://aka.ms/aspnetcore-hsts.
    app.UseHsts();
}

app.UseForwardedHeaders();
app.UseHttpsRedirection();
app.UseStaticFiles();

app.UseRouting();

app.UseAuthorization();

app.MapRazorPages();

var port = Environment.GetEnvironmentVariable("PORT") ?? "10000";
app.Run($"http://0.0.0.0:{port}");
