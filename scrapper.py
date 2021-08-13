import requests
from bs4 import BeautifulSoup

#headers = {"User-Agent": "Chrome 92"}


def get_last_page(url):
    f_result = requests.get(url)
    soup = BeautifulSoup(f_result.text, "html.parser")
    pages = soup.find("div", {"class": "s-pagination"}).find_all("a")
    last_page = pages[-2].text.strip()
    return int(last_page)


def extract_job(html):
    title = html.find("h2").find("a")["title"]
    company = html.find("h3").find("span").get_text(strip=True)
    location = html.find("h3").find("span", {
        "class": "fc-black-500"
    }).get_text(strip=True)
    comp_info = html["data-jobid"]
    return {
        "title": title,
        "company": company,
        "location": location,
        "link": f"https://stackoverflow.com/jobs/{comp_info}"
    }


def extract_jobs(last_page, url):
    jobs = []
    for page in range(last_page):
      print(f"Scarpping SO Page: {page}")
      result = requests.get(f"{url}&pg={page}")
      soup = BeautifulSoup(result.text, "html.parser")
      results = soup.find_all("div", {"class": "-job"})
      for result in results:
        job = extract_job(result)
        jobs.append(job)
    return jobs


def get_jobs(word):
    url = f"https://stackoverflow.com/jobs?q={word}"
    last_page = get_last_page(url)
    jobs = extract_jobs(last_page, url)
    return jobs