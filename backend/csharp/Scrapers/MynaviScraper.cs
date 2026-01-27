using HtmlAgilityPack;
using JobScraperCore.Models;
using JobScraperCore.Utils;

namespace JobScraperCore.Scrapers
{
    public class MynaviScraper : IJobScraper
    {
        public bool CanHandle(string url)
        {
            return url.Contains("mynavi.jp") || url.Contains("mynavi-agent");
        }

        public async Task<ScrapingResult> ScrapeAsync(string url)
        {
            var result = new ScrapingResult
            {
                SiteName = "Mynavi",
                SourceUrl = url
            };

            var html = await HttpClientHelper.GetHtmlAsync(url);
            var doc = new HtmlDocument();
            doc.LoadHtml(html);

            var jobNodes = doc.DocumentNode.SelectNodes("//div[contains(@class, 'cassetteRecruit')]");
            
            if (jobNodes == null)
            {
                jobNodes = doc.DocumentNode.SelectNodes("//div[contains(@class, 'js-jobList-item')]");
            }

            if (jobNodes == null)
            {
                jobNodes = doc.DocumentNode.SelectNodes("//article[contains(@class, 'job-article')]");
            }

            if (jobNodes != null)
            {
                foreach (var node in jobNodes)
                {
                    var job = new JobListing
                    {
                        CompanyName = ExtractText(node, ".//h3[contains(@class, 'cassetteRecruit__name')]|.//div[contains(@class, 'company')]"),
                        JobType = ExtractText(node, ".//h4[contains(@class, 'cassetteRecruit__copy')]|.//h2[contains(@class, 'job-title')]"),
                        EmploymentType = ExtractText(node, ".//li[contains(@class, 'employmentType')]|.//span[contains(@class, 'employment')]"),
                        Salary = ExtractText(node, ".//span[contains(@class, 'salary')]|.//div[contains(@class, 'wage')]"),
                        WorkLocation = ExtractText(node, ".//li[contains(@class, 'location')]|.//p[contains(@class, 'area')]"),
                        JobDescription = ExtractText(node, ".//div[contains(@class, 'tableCondition')]|.//div[contains(@class, 'description')]"),
                        WorkHours = ExtractText(node, ".//th[text()='勤務時間']/following-sibling::td|.//div[contains(@class, 'work-hours')]"),
                        Benefits = ExtractText(node, ".//th[text()='待遇・福利厚生']/following-sibling::td|.//div[contains(@class, 'benefits')]"),
                        Holidays = ExtractText(node, ".//th[text()='休日・休暇']/following-sibling::td|.//div[contains(@class, 'holiday')]"),
                        Requirements = ExtractText(node, ".//th[text()='応募資格']/following-sibling::td|.//div[contains(@class, 'requirements')]"),
                        CompanyLocation = ExtractText(node, ".//th[text()='本社所在地']/following-sibling::td|.//div[contains(@class, 'company-location')]"),
                        IndustryType = ExtractText(node, ".//span[contains(@class, 'industry')]|.//div[contains(@class, 'industryType')]"),
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
