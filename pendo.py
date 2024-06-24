import requests
import json
from requests import HTTPError

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
            data=json.dumps(body) if body else None,
            headers = headers if headers else self.auth_headers
        )

        try:
            resp.raise_for_status()
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
    

def download_xliffs(search_string, save_folder, api_key):

    client = Pendo(api_key)
    guides = client.list_guides().json()

    guide_items = [(x["id"], x["name"]) for x in guides if search_string in x['name']]

    for id, filename in guide_items:
        
        xliff_content = client.export_guide(id).content
        
        with open(f"{save_folder}/{filename.replace(" ","_")}.xliff", "w") as outfile:
            outfile.write(str(xliff_content, encoding='utf-8'))