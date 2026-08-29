import os
import requests
from bs4 import BeautifulSoup

def download_file(url, save_path, link_text=None, prefix=None):

    try:
        """
        'stream' downloads file in chunks instead of loading the whole thing into memory at once...
        imporant for big files like PDFs
        """
        res = requests.get(url, stream=True, timeout=10)
        res.raise_for_status()

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
            #write the file to disk in small pieces instead of holding the whole thing in memory
            for chunk in res.iter_content(chunk_size=8192):
                f.write(chunk)
        print(f"File downloaded to {filepath}")

    except Exception as e:
        print(f"Error: {e}")


def main():
    PAGE_URL = ''       # the page to scrape
    DIV_CLASS = ''       # class of the (<div>/<span>, etc.) containing the document links
    PREFIX_TAG_CLASS = ''  # class of the tag holding a descriptive prefix (e.g. a <span>)
    SITE_DOMAIN = ''     # e.g. 'https://www.example.com' - used to fix relative links
    SAVE_DIR = ''         #fill in the directory the files should be saved to

    req = requests.get(PAGE_URL)
    print(req.status_code)

    soup = BeautifulSoup(req.text, 'html.parser')

    #find the specific content you want to extract
    content = soup.find('div', class_=DIV_CLASS)

    #looking for the header
    title_tag = content.find('span', class_=PREFIX_TAG_CLASS)
    PREFIX = title_tag.get_text().strip()
    print(f"Prefix used: {PREFIX}")

    os.makedirs(SAVE_DIR, exist_ok=True)

    for link in content.find_all('a', href=True):
        file_url = link['href']
        if not file_url.startswith('http'):
            #e.g. file_url=f'https://www.example{file_url}'
            file_url = f'{SITE_DOMAIN}{file_url}'

        download_file(file_url, SAVE_DIR, link.get_text(), prefix=PREFIX)

if __name__ == '__main__':
    main()