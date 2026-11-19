using Microsoft.EntityFrameworkCore;
using wt_lab8_8razor_postgresql_kobzeva.Models;

namespace wt_lab8_8razor_postgresql_kobzeva.Data;

/// <summary>
/// Контекст базы данных приложения.
/// Обеспечивает доступ к таблице Properties через Entity Framework Core.
/// </summary>
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
                new Property
                {
                    Id = 1,
                    Address = "Тридевятое царство, замок принцессы",
                    Type = "Замок",
                    Price = 999999m,
                    Area = 500,
                    Rooms = 20,
                    IsAvailable = true,
                    Description = "Замок с привидением, рвом и собственным садом"
                },
                new Property
                {
                    Id = 2,
                    Address = "Тёмный лес, избушка на курьих ножках",
                    Type = "Избушка",
                    Price = 666000m,
                    Area = 13,
                    Rooms = 1,
                    IsAvailable = true,
                    Description = "Уютная избушка с печью, рядом остановка ступы"
                },
                new Property
                {
                    Id = 3,
                    Address = "Подводное царство, дворец Нептуна",
                    Type = "Дворец",
                    Price = 5000000m,
                    Area = 1200,
                    Rooms = 50,
                    IsAvailable = false,
                    Description = "Дворец под водой с видом на коралловый риф"
                },
                new Property
                {
                    Id = 4,
                    Address = "Минск, ул. Ленина, 15, кв. 42",
                    Type = "Квартира",
                    Price = 120000m,
                    Area = 65.5,
                    Rooms = 3,
                    IsAvailable = true,
                    Description = "Светлая трёхкомнатная квартира рядом с метро"
                },
                new Property
                {
                    Id = 5,
                    Address = "Минск, пр. Независимости, 100",
                    Type = "Офис",
                    Price = 250000m,
                    Area = 120,
                    Rooms = 5,
                    IsAvailable = true,
                    Description = "Офис в бизнес-центре, есть парковка и охрана"
                },
                new Property
                {
                    Id = 6,
                    Address = "Космос, лунная база Илона Маска",
                    Type = "Космический дом",
                    Price = 1000000000m,
                    Area = 250,
                    Rooms = 5,
                    IsAvailable = true,
                    Description = "Первый жилой дом на Луне, доставка ракетой включена"
                });
        });
    }
}
