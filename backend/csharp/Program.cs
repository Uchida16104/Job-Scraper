using System;
using System.IO;
using System.Text.Json;
using JobScraperCore.Services;
using JobScraperCore.Models;

namespace JobScraperCore
{
    class Program
    {
        static async Task<int> Main(string[] args)
        {
            if (args.Length < 1)
            {
                Console.Error.WriteLine("Error: URL argument required");
                return 1;
            }

            string url = args[0];
            
            try
            {
                var factory = new ScraperFactory();
                var scraper = factory.CreateScraper(url);
                
                if (scraper == null)
                {
                    Console.Error.WriteLine($"Error: Unsupported URL: {url}");
                    return 1;
                }

                var result = await scraper.ScrapeAsync(url);
                
                var jsonOptions = new JsonSerializerOptions
                {
                    WriteIndented = false,
                    PropertyNamingPolicy = JsonNamingPolicy.CamelCase
                };
                
                string jsonResult = JsonSerializer.Serialize(result, jsonOptions);
                Console.WriteLine(jsonResult);
                
                return 0;
            }
            catch (Exception ex)
            {
                Console.Error.WriteLine($"Error: {ex.Message}");
                return 1;
            }
        }
    }
}
