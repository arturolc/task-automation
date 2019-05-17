from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup

filename = "jobs.csv"
f = open(filename, "w")

headers = "job_title, company, location, date, url"

f.write(headers + "\n")
# go_next = True	
# while go_next:
my_url = 'https://www.indeed.com/jobs?q=software+engineer+intern&l=Utah&limit=50&radius=25&start=0'

uClient = uReq(my_url)
page_html = uClient.read()
uClient.close()	

page_soup = soup(page_html, "html.parser")
# gets the job containers
containers = page_soup.findAll("div", {"class":"jobsearch-SerpJobCard"})

for container in containers:
	# gets the job title
	job_title = container.div.a.text.strip()
	# get the company container and extract the name
	company_container = container.findAll("div", {"class" : "sjcl"})
	company = company_container[0].div.span.text.strip()

	try:
		# get the location
		location = company_container[0].findAll("div", {"class" : "location"})[0].text.strip()
	except IndexError:
		location = company_container[0].findAll("span", {"class" : "location"})[0].text.strip()

	try:
		# get the date
		date = container.findAll("span", {"class" : "date"})[0].text.strip()
	except IndexError:
		date = "undefined"

	# get the url to apply
	url = container.div.a['href']

	if url.startswith("/rc/clk?jk"):
		url = "https://www.indeed.com/viewjob?" + url.split('?')[1]
		uClient = uReq(url)
		job_html = uClient.read()
		uClient.close()
		temp = soup(job_html, "html.parser")

		try:
			posting_url = temp.findAll("div", {"class" : "jobsearch-ViewJobButtons-container"})[0].div.div.div.a['href']
		except AttributeError:
			posting_url = temp.findAll("div", {"class" : "jobsearch-ViewJobButtons-container"})[0].div.div.a['href']
		except TypeError:
			posting_url = url
	else:
		posting_url = my_url

	print("job title: " + job_title)
	print("company: " + company)
	print("location: " + location)
	print("date: " + date)
	print("url: " + posting_url + "\n")

	f.write(job_title.replace(",", " ") + "," + company.replace(",", " ") + "," + location.replace(",", " ") + "," + date + "," + posting_url + "\n")
f.close()
	# next_page = page_soup.findAll("span", {"class" : "np"})

	# if len(next_page) == 2:
	# 	if next_page[0] == "Next" or next_page[1] == "Next":
	# 		go_next = True
	# 		n += 10
	# 	else:
	# 		go_next = False
	# 		f.close()
	# elif len(next_page) == 1:
	# 	if next_page[0] == "Previous":
	# 		go_next = False
	# 		f.close()
	# 	else:
	# 		go_next = True
	# 		n += 10