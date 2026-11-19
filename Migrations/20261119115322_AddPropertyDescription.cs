using Microsoft.EntityFrameworkCore.Migrations;

#nullable disable

namespace wt_lab8_8razor_postgresql_kobzeva.Migrations
{
    /// <inheritdoc />
    public partial class AddPropertyDescription : Migration
    {
        /// <inheritdoc />
        protected override void Up(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.AddColumn<string>(
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
                value: "Замок с привидением, рвом и собственным садом");

            migrationBuilder.UpdateData(
                table: "Properties",
                keyColumn: "Id",
                keyValue: 2,
                column: "Description",
                value: "Уютная избушка с печью, рядом остановка ступы");

            migrationBuilder.UpdateData(
                table: "Properties",
                keyColumn: "Id",
                keyValue: 3,
                column: "Description",
                value: "Дворец под водой с видом на коралловый риф");

            migrationBuilder.UpdateData(
                table: "Properties",
                keyColumn: "Id",
                keyValue: 4,
                column: "Description",
                value: "Светлая трёхкомнатная квартира рядом с метро");

            migrationBuilder.UpdateData(
                table: "Properties",
                keyColumn: "Id",
                keyValue: 5,
                column: "Description",
                value: "Офис в бизнес-центре, есть парковка и охрана");

            migrationBuilder.UpdateData(
                table: "Properties",
                keyColumn: "Id",
                keyValue: 6,
                column: "Description",
                value: "Первый жилой дом на Луне, доставка ракетой включена");
        }

        /// <inheritdoc />
        protected override void Down(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.DropColumn(
                name: "Description",
                table: "Properties");
        }
    }
}
