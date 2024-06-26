"""
Write me a code in python to scrap the complete website of https://arcprize.org/. 
1. The code should iterate over all the elements in the source code of the homepage and add any internal links (in the domain of https://arcprize.org/) that it finds in a unvisited list. The code should iteratively visit all those pages in the unvisitied list but once it visits and scraps the page, it should remove it from unvisited list and not visit it again. 
2. After visiting a new page and finding all the internal links, the code should scrap the contents to a arc_prize_website.md file. It should only scrap the human readable that is the text content and appropriately put them in the arc_prize_website.md file. The code should mention the URL of the page that it has scraped at the top. 
3. After scraping all the internal pages, the code should go to the top of the arc_prize_website.md file and write the website map in a directory tree format for all the pages that it has scraped. 
4. While running the code should also print the URL that it is currently working on and the list of visited and unvisited URLs. 
5. Use the best programming methodology for writing the code . Try to divide the code in small logically consistent functions. Comment and put docstring wherever it is required. 
6. Ensure that all your variables and functions are typed. 
7. You may split the code across many files if one file is insufficient.

8. Skip the image files or in general every non text file and make sure that they are not downloaded. Make minimal change to the original code. Add comments and docstrings as required.

9. Can you check each paragraph before insertion and if there is an overlap of more than 80% then remove the redundant part marking it for REDUNDANCY. You may put the reference of the paragraph that matches it. Instead of just writing REDUNDANT: Similar to previous paragraph, mention the URL and the paragraph number/numbers with which the redundancy is found.

"""

import requests
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
from typing import List, Set, Tuple
import os
from difflib import SequenceMatcher

BASE_URL = "https://arcprize.org/"
OUTPUT_FILE = "arc_prize_website.md"

class Scraper:
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.visited: Set[str] = set()
        self.to_visit: Set[str] = {base_url}
        self.sitemap: List[str] = []
        self.paragraphs: List[Tuple[str, int, str]] = []  # (paragraph, number, url)
    
    def get_page_links(self, url: str) -> Set[str]:
        """Fetches all internal links from the given URL"""
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        links = set()
        for link in soup.find_all('a', href=True):
            href = link['href']
            full_url = urljoin(self.base_url, href)
            if urlparse(full_url).netloc == urlparse(self.base_url).netloc:
                links.add(full_url)
        return links

    def scrap_page_content(self, url: str) -> str:
        """Scrapes text content from the given URL and formats it for markdown"""
        response = requests.get(url)
        
        # Skip non-text content
        content_type = response.headers.get('Content-Type', '')
        if 'text/html' not in content_type:
            return ""
        
        soup = BeautifulSoup(response.content, 'html.parser')
        texts = soup.find_all(text=True)
        visible_texts = filter(self._tag_visible, texts)
        content = u" ".join(t.strip() for t in visible_texts)
        paragraphs = content.split('\n')
        filtered_paragraphs = [self.check_redundancy(p, i + 1, url) for i, p in enumerate(paragraphs) if p.strip()]

        return "\n".join(filtered_paragraphs)
    
    def _tag_visible(self, element) -> bool:
        """Determines which HTML elements' text should be considered visible"""
        if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
            return False
        if isinstance(element, str):
            return True
        return False

    def check_redundancy(self, paragraph: str, paragraph_number: int, url: str) -> str:
        """Checks if a paragraph is redundant and marks it if so"""
        for existing_paragraph, existing_number, existing_url in self.paragraphs:
            similarity = self.calculate_similarity(paragraph, existing_paragraph)
            if similarity > 0.8:  # 80% similarity threshold
                return f"[REDUNDANT: Similar to paragraph {existing_number} on {existing_url}]\n"
        
        self.paragraphs.append((paragraph, paragraph_number, url))
        return paragraph

    def calculate_similarity(self, a: str, b: str) -> float:
        """Calculates the similarity between two strings"""
        return SequenceMatcher(None, a, b).ratio()

    def write_to_file(self, url: str, content: str):
        """Writes the scrapped content to the markdown file"""
        with open(OUTPUT_FILE, 'a') as f:
            f.write(f'# URL: {url}\n\n')
            f.write(content + '\n\n')
            self.sitemap.append(url)
    
    def write_sitemap(self):
        """Writes the sitemap in a directory tree format at the top of the file"""
        with open(OUTPUT_FILE, 'r') as f:
            content = f.read()
        
        tree = "\n".join(self.format_sitemap_item(url) for url in self.sitemap)
        with open(OUTPUT_FILE, 'w') as f:
            f.write(tree + '\n\n' + content)

    def format_sitemap_item(self, url: str) -> str:
        """Formats a single sitemap item"""
        url_path = urlparse(url).path.strip('/').split('/')
        return ''.join(['    ' * i + '|-- ' + chunk + '\n' for i, chunk in enumerate(url_path)])

    def run(self):
        """Runs the scraping process"""
        if os.path.exists(OUTPUT_FILE):
            os.remove(OUTPUT_FILE)
        
        while self.to_visit:
            current_url = self.to_visit.pop()
            if current_url in self.visited:
                continue
            print(f'Working on: {current_url}')
            content = self.scrap_page_content(current_url)
            if content:
                self.write_to_file(current_url, content)
                links = self.get_page_links(current_url)
                self.to_visit.update(links - self.visited)
            self.visited.add(current_url)
            print(f'Visited: {self.visited}')
            print(f'To visit: {self.to_visit}')
        self.write_sitemap()

if __name__ == '__main__':
    scraper = Scraper(BASE_URL)
    scraper.run()