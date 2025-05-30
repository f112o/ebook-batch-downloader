import requests
from bs4 import BeautifulSoup
from time import sleep


def download_book(book_url, download_name, headers=None):
    response = requests.get(book_url, headers=headers)
    content_type = response.headers.get('Content-Type')
    #print(response.text)
    if response.status_code == 200 and 'application/pdf' in content_type.lower():
        with open(f"{download_name}.pdf", 'wb') as file:
            file.write(response.content)
        print(f"Downloaded: {download_name}.pdf")
    else:
        print(f"Failed to download {download_name}. Status code: {response.status_code}. Content-Type: {content_type}")
        
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

def to_download(book_urls):
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
                download_book(book_url, download_name + '_' + id, headers=headers)

if __name__ == "__main__":
    books_urls = get_book_urls("mechine learning", 6)
    to_download(books_urls)
