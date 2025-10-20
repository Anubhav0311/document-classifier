# This class contains functions to download files from 
# Google Drive and blob storage and clean it.

import requests
import csv
class FileDownloader:
    def __init__(self,opDir):
        self.opDir = opDir
        self.dataFile = None
    def download_file_from_google_drive(self, file_id, destination, chunk_size=32768):
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
        with open(self.opDir+'/'+destination, "wb") as f:
            for chunk in response.iter_content(chunk_size):
                if chunk:
                    f.write(chunk)
        self.dataFile = self.opDir+'/'+destination
        return self.opDir+'/'+destination

    def download_blob_file(self, url, destination):
        response = requests.get(url)
        response.raise_for_status()
        with open(self.opDir+'/'+destination, "wb") as f:
            f.write(response.content)
        return self.opDir+'/'+destination

    def clean_file(self):
        file_path = self.dataFile
        # Implement any cleaning logic if needed
        

        with open(file_path, mode='r') as file:
            csv_reader = csv.reader(file)
            count = 0
            # print(csv_reader[1])
            list_urls = []
            for row in csv_reader:
                count += 1
                # if count == 3:
                # print(row[0])
                # print(row[0].replace('[','').replace(']','').replace('"','').split(','))
                list_urls.extend(row[0].replace('[','').replace(']','').replace('"','').split(','))
        list_urls = list(set(list_urls))
        for idx, url in enumerate(list_urls):
            print(idx,url)
            
file_id = "11lZOc35beVbXjETyXTkiT3Wh3beb_Dby"
dataFileName = "downloaded_csv_payload_current.csv"
dir = "anubhav"
downloader = FileDownloader(dir)
path = downloader.download_file_from_google_drive(file_id, dataFileName)
print(f"Saved to: {path}")
downloader.clean_file()
 
# clean_file should give CSV in the dir.
# to read clean file into a list , iterate over it and download from the blob
#return the sample file
