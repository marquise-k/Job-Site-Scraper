import urllib2
import csv
from bs4 import BeautifulSoup

# Replace developer by the role you're scraping for
sample_page = "https://www.indeed.com/jobs?q=developer&sort=date&start="

# Create placeholders for your results
titlelist = []
companieslist = []
locationlist = []
datelist = []

# Replace developer by the role you're scraping for
step = 10
last_page = 780
first_page = 0

# Loop through pages of your job scraping site
# Make sure the attributes matches your job's html attributes
# These worked for Indeed's attributes as of May 2020 (subject to change of course)

for num in range(first_page, last_page, step):
  page = sample_page + str(num)
  pagedata = urllib2.urlopen(page)
  pagehtml = BeautifulSoup(pagedata, 'html.parser')
  jobhtml = pagehtml.find_all('div', attrs={'class': 'jobsearch-SerpJobCard'})
  for item in jobhtml:
    job_title = item.find(attrs={'class': 'title'})
    job_location = item.find(attrs={'class': 'location'})
    job_company = item.find(attrs={'class': 'company'})
    job_date = item.find(attrs={'class': 'date'})
    title = job_title.text.strip()

    if job_location == None:
      location = 'N/A'
    else:
      location = job_location.text.strip()
    if job_company == None:
     company = 'N/A'
    else:
      company = job_company.text.strip()
    date = job_date.text.strip()
    titlelist.append(title)
    locationlist.append(location)
    companieslist.append(company)
    datelist.append(date)

# Here we clean the results for non-ascii characters
jobs_ascii = [item.encode('ascii', errors='ignore') for item in titlelist]
companies_ascii = [item.encode('ascii', errors='ignore') for item in companieslist]
locations_ascii = [item.encode('ascii', errors='ignore') for item in locationlist]
dates_ascii = [item.encode('ascii', errors='ignore') for item in datelist]

with open('jobs', 'wb') as myfile:
  wr = csv.writer(myfile)
  wr.writerow(jobs_ascii)

with open('locations', 'wb') as myfile:
  wr = csv.writer(myfile)
  wr.writerow(locations_ascii)

with open('companies', 'wb') as myfile:
  wr = csv.writer(myfile)
  wr.writerow(companies_ascii)

with open('dates', 'wb') as myfile:
  wr = csv.writer(myfile)
  wr.writerow(dates_ascii)