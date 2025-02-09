import requests
import os
from dotenv import load_dotenv
import base64
import re
import pandas as pd

load_dotenv()
base_url = "https://api.github.com"

def fetch_repo_readme(access_token, owner, repo):
    url = f"{base_url}/repos/{owner}/{repo}/readme"
   
    headers = {
        "Authorization": f"token {access_token}",
        "Accept": "application/vnd.github.v3+json"
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        repo_data = response.json()
        return repo_data
    else:
        return None

def extract_links(markdown_content):
    links = re.findall(r'\[([^\]]+)\]\(([^)]+)\)', markdown_content)
    cleaned_links = [(text.replace('**', '').replace('_', ''), url) for text, url in links]
    return cleaned_links


access_token = os.getenv("GITHUB_ACCESS_TOKEN")
owner = "codecrafters-io"
repo_name = "build-your-own-x"

readme_data = fetch_repo_readme(access_token, owner, repo_name)

if readme_data:
    readme_content = base64.b64decode(readme_data['content']).decode('utf-8')
    links = extract_links(readme_content)
    df = pd.DataFrame(columns=["Text", "URL"])
    i=0
    
    for text, url in links :
        if(not (url[0] =="#")):
            print(f"Text: {text}, URL: {url}")
            df.loc[i]= [text ,  url]
            i+=1
    df.to_csv("links.csv", index=False)   
else:
    print("Failed to fetch the README.")