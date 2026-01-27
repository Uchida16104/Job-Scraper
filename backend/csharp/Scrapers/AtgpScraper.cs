using HtmlAgilityPack;
using JobScraperCore.Models;
using JobScraperCore.Utils;

namespace JobScraperCore.Scrapers
{
    public class AtgpScraper : IJobScraper
    {
        public bool CanHandle(string url)
        {
            return url.Contains("atgp.jp");
        }

        public async Task<ScrapingResult> ScrapeAsync(string url)
        {
            var result = new ScrapingResult
            {
                SiteName = "atgp",
                SourceUrl = url
            };

            var html = await HttpClientHelper.GetHtmlAsync(url);
            var doc = new HtmlDocument();
            doc.LoadHtml(html);

            var jobNodes = doc.DocumentNode.SelectNodes("//div[contains(@class, 'job-item')]");
            
            if (jobNodes == null)
            {
                jobNodes = doc.DocumentNode.SelectNodes("//article[contains(@class, 'job')]");
            }

            if (jobNodes != null)
            {
                foreach (var node in jobNodes)
                {
                    var job = new JobListing
                    {
                        CompanyName = ExtractText(node, ".//h3[contains(@class, 'company')]|.//div[contains(@class, 'company-name')]"),
                        JobType = ExtractText(node, ".//div[contains(@class, 'job-title')]|.//h4[contains(@class, 'title')]"),
                        EmploymentType = ExtractText(node, ".//span[contains(@class, 'employment-type')]|.//div[contains(@class, 'employment')]"),
                        Salary = ExtractText(node, ".//div[contains(@class, 'salary')]|.//span[contains(@class, 'wage')]"),
                        WorkLocation = ExtractText(node, ".//div[contains(@class, 'location')]|.//span[contains(@class, 'area')]"),
                        JobDescription = ExtractText(node, ".//div[contains(@class, 'description')]|.//p[contains(@class, 'detail')]"),
                        WorkHours = ExtractText(node, ".//div[contains(@class, 'work-hours')]|.//span[contains(@class, 'time')]"),
                        Benefits = ExtractText(node, ".//div[contains(@class, 'benefits')]|.//ul[contains(@class, 'welfare')]"),
                        Holidays = ExtractText(node, ".//div[contains(@class, 'holidays')]|.//span[contains(@class, 'holiday')]"),
                        Requirements = ExtractText(node, ".//div[contains(@class, 'requirements')]|.//div[contains(@class, 'qualification')]"),
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
