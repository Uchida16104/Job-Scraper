namespace JobScraperCore.Models
{
    public class JobListing
    {
        public string CompanyName { get; set; } = string.Empty;
        public string IndustryType { get; set; } = string.Empty;
        public string JobType { get; set; } = string.Empty;
        public string EmploymentType { get; set; } = string.Empty;
        public string WorkHours { get; set; } = string.Empty;
        public string JobDescription { get; set; } = string.Empty;
        public string Salary { get; set; } = string.Empty;
        public string CompanyLocation { get; set; } = string.Empty;
        public string WorkLocation { get; set; } = string.Empty;
        public string Benefits { get; set; } = string.Empty;
        public string Holidays { get; set; } = string.Empty;
        public string Requirements { get; set; } = string.Empty;
        public string JobUrl { get; set; } = string.Empty;
    }
}
