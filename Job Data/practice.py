import requests
from bs4 import BeautifulSoup
import csv

# Base URL pattern for pagination
base_url = 'https://careers.accor.com/global/en/jobs?q=&options=720,258,&page='

# Number of pages to scrape
num_pages = 13

# List to hold job data
job_data = []

# Function to scrape a single page
def scrape_page(page_number):
    url = base_url + str(page_number)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Find job tiles
    job_tiles = soup.find_all('div', class_='attrax-vacancy-tile')
    
    for job_tile in job_tiles:
        job_info = {}
        # Extract job details
        job_info['Title'] = job_tile.find('a', class_='attrax-vacancy-tile__title').get_text(strip=True) if job_tile.find('a', class_='attrax-vacancy-tile__title') else 'N/A'
        job_info['Location'] = job_tile.find('div', class_='attrax-vacancy-tile__location-freetext').find('p', class_='attrax-vacancy-tile__item-value').get_text(strip=True) if job_tile.find('div', class_='attrax-vacancy-tile__location-freetext') else 'N/A'
        job_info['Experience Level'] = job_tile.find('div', class_='attrax-vacancy-tile__option-experience-level').find('p', class_='attrax-vacancy-tile__item-value').get_text(strip=True) if job_tile.find('div', class_='attrax-vacancy-tile__option-experience-level') else 'N/A'
        job_info['Job Schedule'] = job_tile.find('div', class_='attrax-vacancy-tile__option-job-schedule').find('p', class_='attrax-vacancy-tile__item-value').get_text(strip=True) if job_tile.find('div', class_='attrax-vacancy-tile__option-job-schedule') else 'N/A'
        job_info['Job Type'] = job_tile.find('div', class_='attrax-vacancy-tile__option-job-type').find('p', class_='attrax-vacancy-tile__item-value').get_text(strip=True) if job_tile.find('div', class_='attrax-vacancy-tile__option-job-type') else 'N/A'
        job_info['Brands'] = job_tile.find('div', class_='attrax-vacancy-tile__option-brands').find('p', class_='attrax-vacancy-tile__item-value').get_text(strip=True) if job_tile.find('div', class_='attrax-vacancy-tile__option-brands') else 'N/A'
        job_info['Job Category'] = job_tile.find('div', class_='attrax-vacancy-tile__option-job-category').find('p', class_='attrax-vacancy-tile__item-value').get_text(strip=True) if job_tile.find('div', class_='attrax-vacancy-tile__option-job-category') else 'N/A'
        job_info['Description'] = job_tile.find('div', class_='attrax-vacancy-tile__description').find('p', class_='attrax-vacancy-tile__description-value').get_text(strip=True) if job_tile.find('div', class_='attrax-vacancy-tile__description') else 'N/A'
        job_info['Reference'] = job_tile.find('div', class_='attrax-vacancy-tile__reference').find('p', class_='attrax-vacancy-tile__reference-value').get_text(strip=True) if job_tile.find('div', class_='attrax-vacancy-tile__reference') else 'N/A'
        job_info['Expiry Date'] = job_tile.find('div', class_='attrax-vacancy-tile__expiry').find('p', class_='attrax-vacancy-tile__expiry-value').get_text(strip=True) if job_tile.find('div', class_='attrax-vacancy-tile__expiry') else 'N/A'
        job_data.append(job_info)

# Scrape all pages
for page in range(1, num_pages + 1):
    scrape_page(page)

# Print or save the scraped data
for job in job_data:
    print(job)

# Optionally, save to CSV file
keys = ['Title', 'Location', 'Experience Level', 'Job Schedule', 'Job Type', 'Brands', 'Job Category', 'Description', 'Reference', 'Expiry Date']
with open('job_listings_1.csv', 'w', newline='', encoding='utf-8') as csvfile:
    dict_writer = csv.DictWriter(csvfile, fieldnames=keys)
    dict_writer.writeheader()
    dict_writer.writerows(job_data)
