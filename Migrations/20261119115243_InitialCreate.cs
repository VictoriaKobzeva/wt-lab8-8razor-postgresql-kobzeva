using Microsoft.EntityFrameworkCore.Migrations;
using Npgsql.EntityFrameworkCore.PostgreSQL.Metadata;

#nullable disable

#pragma warning disable CA1814 // Prefer jagged arrays over multidimensional

namespace wt_lab8_8razor_postgresql_kobzeva.Migrations
{
    /// <inheritdoc />
    public partial class InitialCreate : Migration
    {
        /// <inheritdoc />
        protected override void Up(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.CreateTable(
                name: "Properties",
                columns: table => new
                {
                    Id = table.Column<int>(type: "integer", nullable: false)
                        .Annotation("Npgsql:ValueGenerationStrategy", NpgsqlValueGenerationStrategy.IdentityByDefaultColumn),
                    Address = table.Column<string>(type: "character varying(200)", maxLength: 200, nullable: false),
                    Type = table.Column<string>(type: "text", nullable: false),
                    Price = table.Column<decimal>(type: "numeric(18,2)", precision: 18, scale: 2, nullable: false),
                    Area = table.Column<double>(type: "double precision", nullable: false),
                    Rooms = table.Column<int>(type: "integer", nullable: false),
                    IsAvailable = table.Column<bool>(type: "boolean", nullable: false)
                },
                constraints: table =>
                {
                    table.PrimaryKey("PK_Properties", x => x.Id);
                });

            migrationBuilder.InsertData(
                table: "Properties",
                columns: new[] { "Id", "Address", "Area", "IsAvailable", "Price", "Rooms", "Type" },
                values: new object[,]
                {
                    { 1, "Тридевятое царство, замок принцессы", 500.0, true, 999999m, 20, "Замок" },
                    { 2, "Тёмный лес, избушка на курьих ножках", 13.0, true, 666000m, 1, "Избушка" },
                    { 3, "Подводное царство, дворец Нептуна", 1200.0, false, 5000000m, 50, "Дворец" },
                    { 4, "Минск, ул. Ленина, 15, кв. 42", 65.5, true, 120000m, 3, "Квартира" },
                    { 5, "Минск, пр. Независимости, 100", 120.0, true, 250000m, 5, "Офис" },
                    { 6, "Космос, лунная база Илона Маска", 250.0, true, 1000000000m, 5, "Космический дом" }
                });
        }

        /// <inheritdoc />
        protected override void Down(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.DropTable(
                name: "Properties");
        }
    }
}
