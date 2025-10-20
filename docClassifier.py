import requests

def download_file_from_google_drive(file_id, destination, chunk_size=32768):
    session = requests.Session()
    base_url = "https://docs.google.com/uc?export=download"
    response = session.get(base_url, params={'id': file_id}, stream=True)
    # try to get confirmation token from cookies (for large files)
    token = None
    for key, value in response.cookies.items():
        if key.startswith('download_warning'):
            token = value
            break
    if token:
        response = session.get(base_url, params={'id': file_id, 'confirm': token}, stream=True)
    response.raise_for_status()
    with open(destination, "wb") as f:
        for chunk in response.iter_content(chunk_size):
            if chunk:
                f.write(chunk)
    return destination


file_id = "11lZOc35beVbXjETyXTkiT3Wh3beb_Dby"
dest = "downloaded_csv_payload.csv"
path = download_file_from_google_drive(file_id, dest)
print(f"Saved to: {path}")
# quick sanity check: print first 512 bytes (binary)
with open(path, "rb") as f:
    print(f.read(512))

url = 'https://storage.googleapis.com/bilby-scraper-pdfs-prod/China%2Fbank%2FPeopleBankOfChina2%2Fhttp%253A%252F%252Fwww.pbc.gov.cn%252Fdiaochatongjisi%252F116219%252F116227%252F5629762%252F2025032117120920108.pdf'
import requests
response = requests.get(url)
print(response.content)

with open("sample_pdf.pdf", "wb") as f:
    f.write(response.content)
