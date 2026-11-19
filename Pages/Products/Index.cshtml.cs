using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.RazorPages;
using Microsoft.EntityFrameworkCore;
using wt_lab8_8razor_postgresql_kobzeva.Data;
using wt_lab8_8razor_postgresql_kobzeva.Models;

namespace wt_lab8_8razor_postgresql_kobzeva.Pages.Products;

public class IndexModel : PageModel
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

    public async Task<IActionResult> OnPostDeleteAsync(int id)
    {
        var property = await _context.Properties.FindAsync(id);

        if (property != null)
        {
            _context.Properties.Remove(property);
            await _context.SaveChangesAsync();
        }

        return RedirectToPage("./Index");
    }
}
