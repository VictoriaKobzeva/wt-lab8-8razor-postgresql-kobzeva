using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.RazorPages;
using Microsoft.EntityFrameworkCore;
using wt_lab8_8razor_postgresql_kobzeva.Data;
using wt_lab8_8razor_postgresql_kobzeva.Models;

namespace wt_lab8_8razor_postgresql_kobzeva.Pages.Products;

public class EditModel : PageModel
{
    private readonly AppDbContext _context;

    public EditModel(AppDbContext context)
    {
        _context = context;
    }

    [BindProperty]
    public Property Property { get; set; } = new();

    public async Task<IActionResult> OnGetAsync(int? id)
    {
        if (id == null)
        {
            return NotFound();
        }

        var property = await _context.Properties.FindAsync(id);

        if (property == null)
        {
            return NotFound();
        }

        Property = property;
        return Page();
    }

    public async Task<IActionResult> OnPostAsync()
    {
        if (!ModelState.IsValid)
        {
            return Page();
        }

        var existing = await _context.Properties.FindAsync(Property.Id);

        if (existing == null)
        {
            return NotFound();
        }

        existing.Address = Property.Address;
        existing.Type = Property.Type;
        existing.Price = Property.Price;
        existing.Area = Property.Area;
        existing.Rooms = Property.Rooms;
        existing.IsAvailable = Property.IsAvailable;
        existing.Description = Property.Description;

        await _context.SaveChangesAsync();

        return RedirectToPage("./Index");
    }
}
