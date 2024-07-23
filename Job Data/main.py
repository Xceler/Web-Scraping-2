import requests 
import csv 
from bs4 import BeautifulSoup  

base_url = 'https://careers.accor.com/global/en/jobs?q=&options=720,258,&page='

num_pages = 13 
job_data= [] 

def scrape_page(page_num):
    url = base_url + str(page_num) 
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'

    }
    response = requests.get(url, headers = headers)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')
    job_tiles = soup.find_all('div', class_ = 'attrax-vacancy-tile')

    for job_tile in job_tiles:
        job_info = {}
        job_info['Title'] = job_tile.find('a', class_ = 'attrax-vacancy-tile__title').get_text(strip = True) if job_tile.find('a', class_ = 'attrax-vacancy-tile__title') else 'N/A'
        job_info['Location'] = job_tile.find('div', class_ = 'attrax-vacancy-tile__location-freetext').find('p', class_ = 'attrax-vacancy-tile__item-value').get_text(strip = True) if job_tile.find('div', class_ = 'attrax-vacancy-tile__option-experience-level') else 'N/A'
        job_info['Experience Level'] = job_tile.find('div', class_ = 'attrax-vacancy-tile__option-experience-level').find('p', class_ = 'attrax-vacancy-tile__item-value').get_text(strip = True) if job_tile.find('div', class_ = 'attrax-vacancy-tile__option-experience-level') else 'N/A'
        job_info['Job Schedule'] = job_tile.find('div', class_ = 'attrax-vacancy-tile__option-job-schedule').find('p', class_ = 'attrax-vacancy-tile__item-value').get_text(strip = True) if job_tile.find('div', class_ = 'attrax-vacancy-tile__option-job-schedule') else 'N/A'
        job_info['Job Type'] = job_tile.find('div', class_ = 'attrax-vacancy-tile__option-job-type').find('p', class_ = 'attrax-vacancy-tile__item-value').get_text(strip =True) if job_tile.find('div', class_ = 'attrax-vacancy-tile__option-job-type') else 'N/A'
        job_info['Brands'] = job_tile.find('div', class_ = 'attrax-vacancy-tile__option-brands').find('p', class_ = 'attrax-vacancy-tile__item-value').get_text(strip = True) if job_tile.find('div', class_ = 'attrax-vacancy-tile__option-brands') else 'N/A'
        job_info['Job Category'] = job_tile.find('div', class_ = 'attrax-vacancy-tile__option-job-category').find('p', class_ = 'attrax-vacancy-tile__item-value').get_text(strip =True) if job_tile.find('div', class_ = 'attrax-vacancy-tile__option-job-category') else 'N/A'
        job_info['Description'] = job_tile.find('div', class_ = 'attrax-vacancy-tile__description').find('p', class_ = 'attrax-vacancy-tile__description-value').get_text(strip = True) if job_tile.find('div', class_ = 'attrax-vacancy-tile__description') else 'N/A'
        job_info['Reference'] = job_tile.find('div', class_ = 'attrax-vacancy-tile__reference').find('p', class_ = 'attrax-vacancy-tile__reference-value').get_text(strip = True) if job_tile.find('div', class_ = 'attrax-vacancy-tile__reference') else 'N/A'
        job_info['Expiry Date']= job_tile.find('div', class_ = 'attrax-vacancy-tile__expiry').find('p', class_ = 'attrax-vacancy-tile__expiry-value').get_text(strip = True) if job_tile.find('div', class_ = 'attrax-vacancy-tile__expiry') else 'N/A'
        job_data.append(job_info)
    


for page in range(1, num_pages+ 1):
    scrape_page(page)

for job in job_data:
    print(job)

keys = ['Title', 'Location', 'Experience Level', 'Job Schedule', 'Job Type', 'Brands',
        'Job Category', 'Description', 'Reference', 'Expiry Date']

with open('JOB_Data.csv', 'w', newline = '', encoding = 'utf-8') as fil:
    dict_writer = csv.DictWriter(fil, fieldnames = keys)
    dict_writer.writeheader() 
    dict_writer.writerows(job_data)