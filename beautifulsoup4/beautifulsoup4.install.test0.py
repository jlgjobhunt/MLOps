# ./MLOps/beautifulsoup4/beautifulsoup4.install.test0.py


import requests
from bs4 import BeautifulSoup
import csv
import markdownify
import os

def scrape_ionos_urls(url="https://www.ionos.com/"):
    """
    Scrapes unique URLs from ionos.com and exports them to CSV,
    Markdown, and HTML.
    """

    try:
        response = requests.get(url)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, "html.parser")

        unique_urls = set()

        for a_tag in soup.find_all("a", href=True):
            href = a_tag.get("href")

            if href:
                absolute_url = urljoin(url, href)
                unique_urls.add(absolute_url)

        return list(unique_urls)
    
    except requests.exceptions.RequestException as e:
        print(f"Error fetching URL: {e}")
        return None
    
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
    

def export_to_csv(urls, filename="ionos_urls.csv"):
    """
    Exports URLs to a CSV file.
    """
    try:
        with open(filename, "w", newline="", encoding="utf-8") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["URL"])
            for url in urls:
                writer.writerow([url])
        print(f"URLs exported to {filename}")

    except Exception as e:
        print(f"Error exporting to CSV: {e}")
    

def export_to_markdown(urls, filename="ionos_urls.md"):
    """
    Exports URLs to a Markdown file.
    """
    try:
        with open(filename, "w", encoding="utf-8") as mdfile:
            mdfile.write("# Unique URLs from ionos.com \n\n")
            for url in urls:
                mdfile.write(f"- [{url}]({url})\n")
        print(f"URLs exported to {filename}")
    except Exception as e:
        print(f"Error exporting to Markdown: {e}")


def export_to_html(urls, filename="ionos_urls.html"):
    """
    Exports URLs to an HTML file.
    """
    try:
        with open(filename, "w", encoding="utf-8") as htmlfile:
            htmlfile.write("<!DOCTYPE html>\n<html>\n<head><title>Unique URLs from from ionos.com</title></head>\n<body>\n")
            htmlfile.write("<h1>Unique URLs from ionos.com</h1>\n<ul>\n")
            for url in urls:
                htmlfile.write(f"<li><a href='{url}'>{url}</a></li>\n")
            htmlfile.write("</ul>\n</body>\n</html>\n")
        print(f"URLs exported to {filename}")
    except Exception as e:
        print(f"Error exporting to HTML. {e}")

if __name__ == "__main__":
    from urllib.parse import urljoin
    urls = scrape_ionos_urls()

    if urls:
        export_to_csv(urls)
        export_to_markdown(urls)
        export_to_html(urls)