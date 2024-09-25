import requests
import json
from requests import HTTPError
from copy import deepcopy
from os.path import join
from os import listdir

class Pendo():
    def __init__(self, api_key):
        self.auth_headers = {
            "x-pendo-integration-key":api_key,
            "x-content-type": "application/json"
        }
        self.base_url="https://app.pendo.io"
        
    def api(self, url, method, params=None, body=None, headers=None):

        resp = requests.request(
            method=method,
            url = self.base_url + url,
            params=params,
            data=body,
            headers = headers if headers else self.auth_headers
        )

        try:
            resp.raise_for_status()
            print(resp.content)
        except HTTPError as e:
            print(e.response.content)
            raise e
        
        return resp
    
    def list_guides(self):
        url="/api/v1/guide"

        return self.api(url, "GET")
    
    def export_guide(self, guide_id):
        url="/api/v1/guide/localization/export"

        return self.api(url, "GET", params={"guideids": guide_id})
    
    def import_guide(self, file_body):
        url = "/api/v1/guide/localization/import"

        headers = deepcopy(self.auth_headers)
        headers["Content-type"] = "application/xml; charset=UTF-8"
        headers.pop("x-content-type")

        return self.api(url, "POST", body=str(file_body), headers=headers)
    
def upload_xliffs(target_folder, api_key):
    
    client = Pendo(api_key)
    files = listdir(target_folder)

    for target_file in files:

        if target_file == ".DS_Store":
            continue
        
        file_path = join(target_folder, target_file)

        print(file_path)

        file_body = open(file_path, "r").read().encode('utf-8').decode()

        resp = client.import_guide(file_body)



def download_xliffs(search_string, save_folder, api_key):

    client = Pendo(api_key)
    guides = client.list_guides().json()

    guide_items = [(x["id"], x["name"]) for x in guides if search_string in x['name']]

    for id, filename in guide_items:
        
        xliff_content = client.export_guide(id).content
        
        with open(f"{save_folder}/{filename.replace(" ","_")}.xliff", "w") as outfile:
            outfile.write(str(xliff_content, encoding='utf-8'))