using System.Text.RegularExpressions;
using JobScraperCore.Models;

namespace JobScraperCore.Services
{
    public static class DataNormalizer
    {
        public static void NormalizeJobListing(JobListing job)
        {
            job.CompanyName = CleanText(job.CompanyName);
            job.JobType = CleanText(job.JobType);
            job.EmploymentType = NormalizeEmploymentType(job.EmploymentType);
            job.Salary = NormalizeSalary(job.Salary);
            job.WorkLocation = CleanText(job.WorkLocation);
            job.JobDescription = CleanText(job.JobDescription);
            job.WorkHours = CleanText(job.WorkHours);
            job.Benefits = CleanText(job.Benefits);
            job.Holidays = CleanText(job.Holidays);
            job.Requirements = CleanText(job.Requirements);
        }

        private static string CleanText(string text)
        {
            if (string.IsNullOrWhiteSpace(text))
                return string.Empty;

            text = Regex.Replace(text, @"\s+", " ");
            text = text.Trim();
            return text;
        }

        private static string NormalizeEmploymentType(string employmentType)
        {
            employmentType = CleanText(employmentType);
            
            if (string.IsNullOrEmpty(employmentType))
                return string.Empty;

            var normalized = employmentType.ToLower();
            
            if (normalized.Contains("正社員") || normalized.Contains("regular"))
                return "正社員";
            if (normalized.Contains("契約社員") || normalized.Contains("contract"))
                return "契約社員";
            if (normalized.Contains("派遣") || normalized.Contains("temporary"))
                return "派遣社員";
            if (normalized.Contains("パート") || normalized.Contains("part-time"))
                return "パート";
            if (normalized.Contains("アルバイト") || normalized.Contains("arbeit"))
                return "アルバイト";
            if (normalized.Contains("業務委託") || normalized.Contains("freelance"))
                return "業務委託";
            
            return employmentType;
        }

        private static string NormalizeSalary(string salary)
        {
            salary = CleanText(salary);
            
            if (string.IsNullOrEmpty(salary))
                return string.Empty;

            salary = Regex.Replace(salary, @"[,、]", "");
            salary = Regex.Replace(salary, @"(\d)円", "$1円 ");
            
            return salary.Trim();
        }
    }
}
