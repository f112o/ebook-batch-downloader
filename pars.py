import argparse 
import requests
from bs4 import BeautifulSoup
from time import sleep
import os
def get_book_urls(key_words,numbers=1):
    url = f'https://1lib.sk/s/{key_words}'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # 提取所有z-bookcard标签的href属性，且以/book开头
    links = []
    base_url = 'https://1lib.sk'
    for card in soup.find_all('z-bookcard', href=True):
        if card['href'].startswith('/book'):
            links.append(base_url + card['href'])

    if not links:
        print("No books found.")
        return []
    return links[:numbers]

def download_book(book_url, download_name, headers=None, save_dir=None):
    if save_dir:
        os.makedirs(save_dir, exist_ok=True)
        download_path = os.path.join(save_dir, download_name)
    else:
        download_path = download_name
    response = requests.get(book_url, headers=headers)
    content_type = response.headers.get('Content-Type')
    if response.status_code == 200 and 'application/pdf' in content_type.lower():
        with open(f"{download_path}.pdf", 'wb') as file:
            file.write(response.content)
        print(f"Downloaded: {download_path}.pdf")
    else:
        print(f"Failed to download {download_name}. Status code: {response.status_code}. Content-Type: {content_type}")


def to_download(book_urls, save_dir=None):
    base_url = 'https://1lib.sk'
    for book_url in book_urls:
        sleep(1)
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36 Edg/136.0.0.0",
            "Cookie": "remix_userkey=10c648ddff70acbaa7be85609a35b6d2; remix_userid=36658551; selectedSiteMode=books; domainsNotWorking=cnlib.icu%2Cquasieconomist.org%2Cknowledgeseeker.site%2Cforthriver.xyz%2Cwesinx.com%2Chomeonet.tech%2Ckeypaperi.top%2Ccymatyx.com; siteLanguage=en; mp_851392464b60e8cc1948a193642f793b_mixpanel=%7B%22distinct_id%22%3A%20%22%24device%3A19716301c235fa-08fe33cdcbe7c18-4c657b58-11cc40-19716301c245fa%22%2C%22%24device_id%22%3A%20%2219716301c235fa-08fe33cdcbe7c18-4c657b58-11cc40-19716301c245fa%22%2C%22%24initial_referrer%22%3A%20%22https%3A%2F%2Flink.zhihu.com%2F%3Ftarget%3Dhttps%253A%2F%2F1lib.sk%2F%22%2C%22%24initial_referring_domain%22%3A%20%22link.zhihu.com%22%7D",
            "Referer": book_url
        }
        res = requests.get(book_url, headers=headers)
        soup = BeautifulSoup(res.text, 'html.parser')
        download_name = None
        for tag in soup.find_all('h1'):
            if 'book-title' in tag.get('class', []):
                download_name = ''.join(tag.text.split())
                print(f"Download name: {download_name}")
                break
        for tag in soup.find_all('a', href=True):
            if tag['href'].startswith('/dl/'):
                book_url = base_url + tag['href']
                id = book_url.split('/')[-1]
                print(book_url)
                download_book(book_url, download_name + '_' + id, headers=headers, save_dir=save_dir)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Download books from 1lib.sk")
    parser.add_argument('--key_words', type=str, help='Keywords to search for books')
    parser.add_argument('--numbers', type=int, default=1, help='Number of books to download')
    parser.add_argument('--save_dir', type=str, default='.', help='Directory to save downloaded books')
    args = parser.parse_args()
    book_urls = get_book_urls(args.key_words, args.numbers)
    to_download(book_urls, save_dir=args.save_dir)