using JobScraperCore.Scrapers;

namespace JobScraperCore.Services
{
    public class ScraperFactory
    {
        private readonly List<IJobScraper> _scrapers;

        public ScraperFactory()
        {
            _scrapers = new List<IJobScraper>
            {
                new AtgpScraper(),
                new LitalicoScraper(),
                new MynaviScraper()
            };
        }

        public IJobScraper? CreateScraper(string url)
        {
            foreach (var scraper in _scrapers)
            {
                if (scraper.CanHandle(url))
                {
                    return scraper;
                }
            }
            return null;
        }
    }
}
