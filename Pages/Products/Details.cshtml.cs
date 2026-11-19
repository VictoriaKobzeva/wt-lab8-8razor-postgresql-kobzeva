using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.RazorPages;
using wt_lab8_8razor_postgresql_kobzeva.Data;
using wt_lab8_8razor_postgresql_kobzeva.Models;

namespace wt_lab8_8razor_postgresql_kobzeva.Pages.Products;

public class DetailsModel : PageModel
{
    private readonly AppDbContext _context;

    public DetailsModel(AppDbContext context)
    {
        _context = context;
    }

    public Property? Property { get; set; }

    public async Task<IActionResult> OnGetAsync(int? id)
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
    }
}
