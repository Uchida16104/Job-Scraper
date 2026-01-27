using JobScraperCore.Models;

namespace JobScraperCore.Scrapers
{
    public interface IJobScraper
    {
        Task<ScrapingResult> ScrapeAsync(string url);
        bool CanHandle(string url);
    }
}
