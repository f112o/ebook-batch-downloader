from flask import Flask, request, jsonify, send_file, render_template, Response
from get_books import get_book_urls
import requests
import os
from bs4 import BeautifulSoup
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_links', methods=['POST'])
def get_links():
    data = request.json
    print(data)
    key_words = data.get('key_words', '')
    numbers = int(data.get('numbers', 1))
    book_urls = get_book_urls(key_words, numbers)
    links = []
    from get_books import to_download
    # 只获取PDF直链和文件名，不下载
    base_url = 'https://1lib.sk'
    for book_url in book_urls:
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
                download_name = ' '.join(tag.text.split())
                break
        for tag in soup.find_all('a', href=True):
            if tag['href'].startswith('/dl/'):
                pdf_url = base_url + tag['href']
                # 检查是否为PDF
                r = requests.head(pdf_url, headers=headers, allow_redirects=True)
                content_type = r.headers.get('Content-Type', '')
                if 'pdf' in content_type.lower():
                    links.append({'url': pdf_url, 'name': download_name, 'referer': book_url})
                break
    print(links)
    return jsonify({'links': links})

@app.route('/download_file')
def download_file():
    url = request.args.get('url')
    name = request.args.get('name', 'download')
    print("name:", name)
    referer = request.args.get('referer', '')
    headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36 Edg/136.0.0.0",
            "Cookie": "remix_userkey=10c648ddff70acbaa7be85609a35b6d2; remix_userid=36658551; selectedSiteMode=books; domainsNotWorking=cnlib.icu%2Cquasieconomist.org%2Cknowledgeseeker.site%2Cforthriver.xyz%2Cwesinx.com%2Chomeonet.tech%2Ckeypaperi.top%2Ccymatyx.com; siteLanguage=en; mp_851392464b60e8cc1948a193642f793b_mixpanel=%7B%22distinct_id%22%3A%20%22%24device%3A19716301c235fa-08fe33cdcbe7c18-4c657b58-11cc40-19716301c245fa%22%2C%22%24device_id%22%3A%20%2219716301c235fa-08fe33cdcbe7c18-4c657b58-11cc40-19716301c245fa%22%2C%22%24initial_referrer%22%3A%20%22https%3A%2F%2Flink.zhihu.com%2F%3Ftarget%3Dhttps%253A%2F%2F1lib.sk%2F%22%2C%22%24initial_referring_domain%22%3A%20%22link.zhihu.com%22%7D",
            "Referer": referer
        }
    r = requests.get(url, headers=headers, stream=True)
    content_type = r.headers.get('Content-Type', '')
    if r.status_code == 200 and 'pdf' in content_type.lower():
        return Response(
            r.iter_content(chunk_size=8192),
            content_type=content_type,
            headers={"Content-Disposition": f"attachment; filename={name}.pdf"}
        )
    else:
        return jsonify({"error": "文件获取失败或不是PDF", "content_type": content_type}), 400

if __name__ == '__main__':
    app.run(debug=True)