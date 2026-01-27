using System.Collections.Generic;

namespace JobScraperCore.Models
{
    public class ScrapingResult
    {
        public int JobCount { get; set; }
        public List<JobListing> Jobs { get; set; } = new List<JobListing>();
        public string SiteName { get; set; } = string.Empty;
        public string SourceUrl { get; set; } = string.Empty;
        public string ScrapedAt { get; set; } = DateTime.UtcNow.ToString("o");
    }
}
