import requests
import os
from dotenv import load_dotenv
import base64
import re
import pandas as pd
import time 
load_dotenv()
base_url = "https://api.github.com"

def fetch_repo_readme(access_token, url):
    url = f"{base_url}/repos/{url}/readme"
   
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


repo_links = [
    "codecrafters-io/build-your-own-x",
    "practical-tutorials/project-based-learning",
    "josephmisiti/awesome-machine-learning",
    "anthropics/courses",
    "lorinpop17/app-ideas",
    "charlax/professional-programming",
    "aishwaryanr/awesome-generative-ai-guide",
    "liuchong/awesome-roadmaps",
    "detailyang/awesome-cheatsheet",
    "cloudcommunity/Free-Certifications",
    "ChristosChristofidis/awesome-deep-learning",
    "docker/awesome-compose",
    "academic/awesome-datascience",
    "freeCodeCamp/freeCodeCamp",
    "EbookFoundation/free-programming-books",
    "A-to-Z-Resources-for-Students",
    "Hack-with-Github/Awesome-Hacking",
    "prakhar1989/awesome-courses",
    "trimstray/the-book-of-secret-knowledge",
    "brexhq/prompt-engineering",
    "mlabonne/llm-course",
    "sindresorhus/awesome",
    "MunGell/awesome-for-beginners",
    "kamranahmedse/developer-roadmap",
    "bradtraversy/50projects50days",
    "mtdvio/every-programmer-should-know",
    "shahednasser/awesome-resources",
    "microsoft/Data-Science-For-Beginners",
    "natnew/Awesome-Data-Science",
    "goabstract/Marketing-for-Engineers"
]

access_token = os.getenv("GITHUB_ACCESS_TOKEN")
owner = "codecrafters-io"
repo_name = "build-your-own-x"

df = pd.DataFrame(columns=["Repo","Text", "URL"])
i=0
for repo in repo_links:
    readme_data = fetch_repo_readme(access_token, repo)
    if readme_data:
        readme_content = base64.b64decode(readme_data['content']).decode('utf-8')
        links = extract_links(readme_content)
        print(f"Repo: {repo}")
        for text, url in links:
            if(not (url[0]=="#") or (url[0]==".") or (url[0]=="/")):
                df.loc[i]= [repo, text ,  url]
                i+=1
    else:
        print(f"Failed to fetch the README for {repo}")
    time.sleep(1)
df.to_csv("dataset.csv", index=False) 
print("Done!")

"""
Failed to fetch the README for A-to-Z-Resources-for-Students
Failed to fetch the README for lorinpop17/app-ideas
"""