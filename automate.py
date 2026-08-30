import os
import requests
from bs4 import BeautifulSoup

def download_file(url, save_path, link_text=None, prefix=None):

    try:
        res = requests.get(url, timeout=10)

        # uses the link's visible text as the filename, e.g. <a>Booking</a> would use 'Booking'
        base_filename = link_text.strip()

        # make sure it ends in .pdf, e.g. Booking.pdf
        if not base_filename.lower().endswith('.pdf'):
            base_filename += '.pdf'

        # add a prefix for context, e.g. 'Sun 1 Hotel - Booking.pdf'
        if prefix:
            base_filename = f'{prefix} - {base_filename}'

        # strip characters Windows won't allow in filenames
        for char in '\\/*?:"<>|':
            base_filename = base_filename.replace(char, '')

        filepath = os.path.join(save_path, base_filename)

        print(f"Downloading {url} to {filepath}")

        with open(filepath, 'wb') as f:
            f.write(res.content)
            
        print(f"File downloaded to {filepath}")

    except Exception as e:
        print(f"Error: {e}")


def main():
    page_url = ''       # the page to scrape
    CLASS = ''       # class of the (<div>/<span>, etc.) containing the document links
    prefix_class = ''  # class of the tag holding a descriptive prefix (e.g. a <span>)
    site_domain = ''     # e.g. 'https://www.example.com' - used to fix relative links
    sav_dir = ''         #fill in the directory the files should be saved to

    req = requests.get(page_url)
    print(req.status_code)

    soup = BeautifulSoup(req.text, 'html.parser')

    #find the specific content you want to extract
    content = soup.find('div', class_=CLASS)

    #looking for the header
    title_tag = content.find('span', class_=prefix_class)
    PREFIX = title_tag.get_text().strip()
    print(f"Prefix used: {PREFIX}")

    os.makedirs(sav_dir, exist_ok=True)

    for link in content.find_all('a', href=True):
        file_url = link['href']
        if not file_url.startswith('http'):
            #e.g. file_url=f'https://www.example{file_url}'
            file_url = f'{site_domain}{file_url}'

        download_file(file_url, sav_dir, link.get_text(), prefix=PREFIX)

if __name__ == '__main__':
    main()