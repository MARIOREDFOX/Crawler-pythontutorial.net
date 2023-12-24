import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

url = "https://www.pythontutorial.net/python-oop/"

def remove_classes(soup, class_names):
    for class_name in class_names:
        elements = soup.find_all(class_=class_name)
        for element in elements:
            element.decompose()

def format_class_italic(soup, class_name):
    elements = soup.find_all(class_=class_name)
    for element in elements:
        element.name = 'i'

def scrape_section_content(section_url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    response = requests.get(section_url, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')

        # Remove specific classes
        remove_classes(soup, ["wth-question"])

        # Format specific class as italic
        format_class_italic(soup, "wp-block-code")

        section_content = soup.find('main', {'id': 'primary'})
        if section_content:
            content_text = section_content.get_text(separator='\n')

            # Add separator line
            separator = '-' * 50 + '\n'
            content_text += '\n' + separator
            return content_text
        else:
            print(f"Content not found for section: {section_url}")
            return None
    else:
        print(f"Failed to retrieve the page. Status code: {response.status_code}")
        return None

# Send a GET request to the main URL
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}
main_response = requests.get(url, headers=headers)
if main_response.status_code == 200:
    main_soup = BeautifulSoup(main_response.content, 'html.parser')

    # Find and follow links in each section
    section_links = main_soup.find_all('a', {'href': lambda x: x and '/python-oop/' in x})
    
    # Create a single text file to save all content
    with open("combined_content.txt", 'w', encoding='utf-8') as combined_file:
        for link in section_links:
            section_url = urljoin(url, link.get('href'))
            print(f"\nScraping content for section: {section_url}\n")
            content = scrape_section_content(section_url)
            if content:
                combined_file.write(content)
else:
    print(f"Failed to retrieve the main page. Status code: {main_response.status_code}")

