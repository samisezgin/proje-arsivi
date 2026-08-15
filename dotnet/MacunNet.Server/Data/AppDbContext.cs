using MacunNet.Server.Models;
using Microsoft.EntityFrameworkCore;

namespace MacunNet.Server.Data
{
    public class AppDbContext : DbContext
    {
        public AppDbContext(DbContextOptions<AppDbContext> options) : base(options)
        {

        }
        public DbSet<User> users { get; set; }
    }
}
