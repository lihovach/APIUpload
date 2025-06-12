import os
import requests
import json
from pathlib import Path

BRIGHT_API_TOKEN = "Your API key"
BRIGHT_PROJECT_ID = "Your projecT ID"
BRIGHT_HOSTNAME = "eu.brightsec.com"
AUTH_OBJECT_ID = "Your AO id"

def find_schema_files():
    """Find API schema files in current directory"""
    return list(Path('.').glob('*.json')) + list(Path('.').glob('*.yaml'))

def upload_schema(file_path):
    """Upload schema to Bright and return file ID"""
    url = f"https://{BRIGHT_HOSTNAME}/api/v1/files"
    headers = {"Authorization": f"Api-Key {BRIGHT_API_TOKEN}"}
    
    with open(file_path, 'rb') as f:
        files = {
            'file': (os.path.basename(file_path), f, 'application/json'),
            'projectId': (None, BRIGHT_PROJECT_ID)
        }
        response = requests.post(url, headers=headers, files=files)
        response.raise_for_status()
        return response.json()['id']  # Return only the file ID

def start_discovery(file_id):
    """Start a new discovery scan using the uploaded file"""
    url = f"https://{BRIGHT_HOSTNAME}/api/v2/projects/{BRIGHT_PROJECT_ID}/discoveries"
    headers = {
        "Authorization": f"Api-Key {BRIGHT_API_TOKEN}",
        "Content-Type": "application/json"
    }

    payload = {
        "config": {
            "name": "Discovery for Booking Journey APIs",
            "discoveryTypes": ["oas"],
            "fileId": file_id,
#            "hostsFilter": [" "], is required if the uploaded schema file does NOT include a 'servers' section (i.e., no host defined).
            "authObjectId": AUTH_OBJECT_ID,
            "optimizedCrawler": True,
            "useCrawlerOdometer": False,
            "maxInteractionsChainLength": 3,
            "subdomainsCrawl": False,
            "poolSize": 10,
            "requestsRateLimit": 300,
            "queuePriority": 0,
            "exclusions": {
                "requests": [
                    {
                        "patterns": [
                            "(?<excluded_file_ext>(\\/\\/[^?#]+\\.)((?<image>jpg|jpeg|png|gif|svg|eps|webp|tif|tiff|bmp|psd|ai|raw|cr|pcx|tga|ico)|(?<video>mp4|avi|3gp|flv|h264|m4v|mkv|mov|mpg|mpeg|vob|wmv)|(?<audio>wav|mp3|ogg|wma|mid|midi|aif)|(?<document>doc|docx|odt|pdf|rtf|ods|xls|xlsx|odp|ppt|pptx)|(?<font>ttf|otf|fnt|fon))(?:$|#|\\?))"
                        ]
                    },
                    {
                        "patterns": ["logout|signout"]
                    },
                    {
                        "patterns": [
                            "(\\/(client_204|csi_204|gen_204|generate_204)\\?)|(&l=dataLayer&cx=c)|(\\.js\\?id=GTM-)|(\\/ns.html\\?id=GTM-)|(:\\/\\/gtm.*\\.js\\?st=)|(:\\/\\/load.*\\.js\\?st=)|.*adservice\\.google\\.|.*googletagmanager.com|.*google-analytics.com|beacon.min.js|(\\/cdn-cgi\\/apps\\/body\\/)|(.*trustarc.com\\/(cap|log)?)|.*trkn.us|(\\/facebook[-_\\/]?(pixel|fbevents|productad).*.js)|(\\/\\?sentry_(key|version)=)|(\\/sentry[-\\/](bundle|browser|logger|tracing).*.js)|(\\/log\\?(action|count|data|documentUrl|event|entry|id|kc|method|ref|sLog|tag|uuid)=)|mathtag.com|scorecardresearch.com|criteo\\.(com|net)"
                        ]
                    }
                ]
            }
        }
    }

    
    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()
    return response.json()

def main():
    print("🔍 Finding API schemas...")
    schema_files = find_schema_files()
    
    if not schema_files:
        print("No schema files found")
        return
    
    for file_path in schema_files:
        print(f"\nUploading {file_path}...")
        try:
            file_id = upload_schema(file_path)
            print(f"Uploaded! File ID: {file_id}")
            
            print("\n Starting discovery scan...")
            discovery = start_discovery(file_id)
            print(f" Discovery started! ID: {discovery.get('id')}")
            print(f"Name: {discovery.get('name')}")
            print(f"Status: {discovery.get('status')}")
            
        except Exception as e:
            print(f" Error: {str(e)}")
            if hasattr(e, 'response'):
                print(f"Response: {e.response.text}")

if __name__ == "__main__":
    main()
