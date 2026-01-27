using HtmlAgilityPack;
using JobScraperCore.Models;
using JobScraperCore.Utils;

namespace JobScraperCore.Scrapers
{
    public class LitalicoScraper : IJobScraper
    {
        public bool CanHandle(string url)
        {
            return url.Contains("snabi.jp") || url.Contains("litalico");
        }

        public async Task<ScrapingResult> ScrapeAsync(string url)
        {
            var result = new ScrapingResult
            {
                SiteName = "LITALICO",
                SourceUrl = url
            };

            var html = await HttpClientHelper.GetHtmlAsync(url);
            var doc = new HtmlDocument();
            doc.LoadHtml(html);

            var jobNodes = doc.DocumentNode.SelectNodes("//div[contains(@class, 'searchResultList__item')]");
            
            if (jobNodes == null)
            {
                jobNodes = doc.DocumentNode.SelectNodes("//li[contains(@class, 'job-list-item')]");
            }

            if (jobNodes != null)
            {
                foreach (var node in jobNodes)
                {
                    var job = new JobListing
                    {
                        CompanyName = ExtractText(node, ".//p[contains(@class, 'company-name')]|.//h3[contains(@class, 'companyName')]"),
                        JobType = ExtractText(node, ".//h2[contains(@class, 'job-title')]|.//div[contains(@class, 'jobTitle')]"),
                        EmploymentType = ExtractText(node, ".//dd[contains(@class, 'employment')]|.//span[contains(@class, 'employmentStatus')]"),
                        Salary = ExtractText(node, ".//dd[contains(@class, 'salary')]|.//div[contains(@class, 'wage')]"),
                        WorkLocation = ExtractText(node, ".//dd[contains(@class, 'location')]|.//p[contains(@class, 'workLocation')]"),
                        JobDescription = ExtractText(node, ".//div[contains(@class, 'job-description')]|.//p[contains(@class, 'description')]"),
                        WorkHours = ExtractText(node, ".//dd[contains(@class, 'workingHours')]|.//div[contains(@class, 'work-time')]"),
                        Benefits = ExtractText(node, ".//dd[contains(@class, 'welfare')]|.//ul[contains(@class, 'benefits')]"),
                        Holidays = ExtractText(node, ".//dd[contains(@class, 'holiday')]|.//div[contains(@class, 'holidays')]"),
                        Requirements = ExtractText(node, ".//dd[contains(@class, 'qualification')]|.//div[contains(@class, 'requirements')]"),
                        CompanyLocation = ExtractText(node, ".//dd[contains(@class, 'companyLocation')]|.//p[contains(@class, 'company-address')]"),
                        IndustryType = ExtractText(node, ".//dd[contains(@class, 'industry')]|.//span[contains(@class, 'industryType')]"),
                        JobUrl = ExtractUrl(node, url)
                    };

                    result.Jobs.Add(job);
                }
            }

            result.JobCount = result.Jobs.Count;
            return result;
        }

        private string ExtractText(HtmlNode node, string xpath)
        {
            var targetNode = node.SelectSingleNode(xpath);
            return targetNode?.InnerText.Trim() ?? string.Empty;
        }

        private string ExtractUrl(HtmlNode node, string baseUrl)
        {
            var linkNode = node.SelectSingleNode(".//a[@href]");
            if (linkNode != null)
            {
                var href = linkNode.GetAttributeValue("href", string.Empty);
                if (!string.IsNullOrEmpty(href))
                {
                    if (href.StartsWith("http"))
                    {
                        return href;
                    }
                    else
                    {
                        var uri = new Uri(new Uri(baseUrl), href);
                        return uri.ToString();
                    }
                }
            }
            return string.Empty;
        }
    }
}
