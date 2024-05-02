import requests
import re
import json
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
import os
from selenium import webdriver
from selenium.common.exceptions import TimeoutException

def clean_url(u):
    index = u.find('"')
    if(index!=-1):
        u = u[:index]
    index = u.find("'")
    if(index!=-1):
        u = u[:index]
    index = u.find("<")
    if(index!=-1):
        u = u[:index]
    index = u.find(">")
    if(index!=-1):
        u = u[:index]
    return u

class BruteForce:
    def __init__(self, url, wordlist, output_file):
        self.url = url
        self.wordlist = wordlist
        self.output_file = output_file

    def brute_force_subdomains(self):
        with open(self.wordlist,'r') as f:
            subs = [line.rstrip() for line in f]
        for i in subs:
            sub = 'https://'+i+'.'+self.url
            try:
                req = requests.get(sub)
                res = req.status_code
                self.output_file.write(f'[+] {sub} [{res}] Alive\n')
            except:
                continue

class WebCrawler:
    def __init__(self):
        self.base_url = ""
        self.urls = set()

    def extract_urls(self, page_url, soup):
        parsed_url = urlparse(page_url)
        base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"
        for link in soup.find_all('a', href=True):
            href = link['href']
            if href.startswith('/'):
                url = urljoin(base_url, href)
                self.urls.add(url)
            elif base_url in href:
                self.urls.add(href)

    def crawl_and_save(self):
        if not self.base_url:
            print("Please enter a domain name first.")
            return

        try:
            response = requests.get(self.base_url)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                self.extract_urls(self.base_url, soup)
                self.save_urls()
                print("URLs containing the specified domain saved to output.txt successfully.")
            else:
                print("Failed to retrieve content from the webpage.")
        except Exception as e:
            print(f"An error occurred: {e}")

    def save_urls(self):
        with open("output.txt", "w", encoding="utf-8") as file:
            for url in self.urls:
                file.write(url + '\n')

class SubdomainScreenshotter:
    def __init__(self, subdomains_file):
        self.subdomains_file = subdomains_file
        self.driver = None
    
    def start_browser(self):
        self.driver = webdriver.Chrome()
        self.driver.set_page_load_timeout(30)

    def take_screenshot(self, url, filename):
        try:
            self.driver.get(url)
            self.driver.save_screenshot(filename)
            print(f"Screenshot saved for URL: {url}")
        except TimeoutException:
            print(f"Timeout occurred while accessing URL: {url}")
        except Exception as e:
            print(f"Error occurred while taking screenshot for URL {url}: {str(e)}")

    def close_browser(self):
        if self.driver:
            self.driver.quit()
            print("Browser closed.")

    def take_screenshots(self):
        self.start_browser()

        if not os.path.exists("selenium_output"):
            os.makedirs("selenium_output")

        with open(self.subdomains_file, 'r') as file:
            for subdomain in file:
                url = f"http://{subdomain.strip()}"
                screenshot_path = os.path.join("selenium_output", f"{subdomain.strip()}.png")
                self.take_screenshot(url, screenshot_path)

        self.close_browser()

def main():
    ## Active Reconnsiance 
    domain = input("Enter your domain name (e.g., example.com): ").strip()
    print("-----------------------------------------------------------------\n Active Reconn started")
    with open("output.txt", "w") as output_file:
        spider = WebCrawler()
        spider.base_url = f"https://{domain}"
        spider.crawl_and_save()

    print("------------------------------------------------------------------\n Screenshots started")
    ## Selenuim to take screenshots
    subdomains_file = "subdomains_test.txt"
    screenshotter = SubdomainScreenshotter(subdomains_file)
    screenshotter.take_screenshots()
    
    ## Web Crawling
    print("------------------------------------------------------------------\n Web Crawling started, it takes a long time")    
    brute_force = BruteForce(domain, "subdomains_list.txt", output_file)
    brute_force.brute_force_subdomains()


if __name__ == "__main__":
    main()
