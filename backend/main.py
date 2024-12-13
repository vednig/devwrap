from flask import Flask, jsonify, request
import requests
import datetime
import sys
import requests
from bs4 import BeautifulSoup
import time
import json
import redis
from flask_cors import CORS

r = redis.Redis(
  host='concise-earwig-24885.upstash.io',
  port=6379,
  password='AWE1AAIjcDEyM2YxNDU4OWY2ZTI0Y2I1YWU1MWZmZTIxMDg5M2UyYnAxMA',
  ssl=True
)


app = Flask(__name__)
CORS(app)

# # GitHub configuration
# GITHUB_USERNAME = 'vednig'

# # Stack Overflow configuration
# STACK_OVERFLOW_USER_ID = '13935716'
def generate_commits_stats(username):
    url = f"https://github-readme-stats.vercel.app/api?username={username}"

    header = {
        "Content-Type":
            "application/json",
            "User-Agent":
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36"
    }

    response = requests.get(url, headers=header)
    html_content = response.text

    soup = BeautifulSoup(html_content, "html.parser")

    title = soup.title.text.strip()
    description = soup.desc.text.strip()

    metrics = description.split(',')

    description_dict = {}

    for metric in metrics:
        key, value = metric.split(':')
        key = key.strip()
        value = int(value.strip())
        description_dict[key] = value

    description_dict_keys = list(description_dict.keys())

#     github_stats_json = f"""
# ```json
# {{
#     "{title}": {{
#         "{description_dict_keys[0]}": "{description_dict[description_dict_keys[0]]} ⭐️",
#         "{description_dict_keys[1]}": "{description_dict[description_dict_keys[1]]} 🔥",
#         "{description_dict_keys[2]}": "{description_dict[description_dict_keys[2]]} 🚀",
#         "{description_dict_keys[3]}": "{description_dict[description_dict_keys[3]]} 📬",
#         "{description_dict_keys[4]}": "{description_dict[description_dict_keys[4]]} 🤝"
#     }}
# }}
# ```
# """
    return description_dict[description_dict_keys[1]]
def generate_ghoc_stats(username,repo):
    url= f"http://localhost:8080/{username}/{repo}"
    response = requests.get(url)
    # print(response.text)
    if response.status_code == 200:
            resloc = json.loads(response.text)
            # print(resloc)
            return resloc['loc']
    else:
        return 0


def get_commit_data(url):
    headers = {
                 'Authorization': f'token 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',
        'Accept': 'application/vnd.github.v3+json',
        # 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Encoding': 'gzip, deflate, br, zstd',
        'Accept-Language': 'en-US,en;q=0.9',
        'Cache-Control': 'max-age=0',
        'Priority': 'u=0, i',
        'Sec-CH-UA': '"Microsoft Edge";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
        'Sec-CH-UA-Mobile': '?0',
        'Sec-CH-UA-Platform': '"Windows"',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0'
    }
    commits = []
    
    # Handle pagination and empty repositories
    # while url:
    response = requests.get(url, headers=headers)
    
    # Check if the repository is empty
    if response.status_code == 409 and "Git Repository is empty" in response.text:
        return []  # Return empty list if repository has no commits

    # Check rate limit
    remaining_requests = int(response.headers.get('X-RateLimit-Remaining', 0))
    if remaining_requests == 0:
        reset_time = int(response.headers.get('X-RateLimit-Reset', 0))
        reset_timestamp = datetime.datetime.utcfromtimestamp(reset_time)
        raise Exception("GitHub rate limit exceeded.")
    
    # Check for other errors
    if response.status_code != 200:
        response.raise_for_status()
    
    # Accumulate commits
    data = response.json()
    commits.extend(data)
    
    # Check for next page of commits (pagination)
    url = response.links.get('next', {}).get('url')

    return commits

def get_repo_data(url):
    headers = {
         'Authorization': f'token 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',
        'Accept': 'application/vnd.github.v3+json',
        # 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Encoding': 'gzip, deflate, br, zstd',
        'Accept-Language': 'en-US,en;q=0.9',
        'Cache-Control': 'max-age=0',
        'Priority': 'u=0, i',
        'Sec-CH-UA': '"Microsoft Edge";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
        'Sec-CH-UA-Mobile': '?0',
        'Sec-CH-UA-Platform': '"Windows"',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0'
    }
    response = requests.get(url,headers=headers)
    # print(response.json())
    if response.status_code==200:
        return response.json()
    else:
        return {}

# Utility function to get StackOverflow data
def get_stackoverflow_data(url):
    response = requests.get(url)
    response.raise_for_status()
    return response.json()


@app.route('/developer-stats', methods=['GET'])
def get_developer_stats():
    GITHUB_USERNAME = request.args.get('github_username') 
    STACK_OVERFLOW_USER_ID = request.args.get('stackid') 
    cache_stats = r.get(str(GITHUB_USERNAME+STACK_OVERFLOW_USER_ID))
    # cache_stats=None
    if cache_stats==None:
        current_year = datetime.datetime.now().year
        repos_url = f'http://api.github.com/users/{GITHUB_USERNAME}/repos?since=2024-01-01T00:00:00Z'
        repos = get_repo_data(repos_url)
        # print(repos_url)
        total_linesize_of_code = 0
        total_lines_of_code_read = 0
        commits_with_bug = 0
        project_categories = {"big": 0, "medium": 0, "small": 0}
        total_contributions = 0

        for repo in repos:
            # print(repo)
            # Get repository's commit history
            commits_url = f'https://api.github.com/repos/{GITHUB_USERNAME}/{repo["name"]}/commits?since={current_year}-01-01T00:00:00Z&author={GITHUB_USERNAME}'
            commits = get_commit_data(commits_url)
            # Count commits containing "bug" in their message
            for commit in commits:
                if 'bug' in commit['commit']['message'].lower():
                    commits_with_bug += 1
                elif 'fix' in commit['commit']['message'].lower():
                    commits_with_bug += 1
                elif 'error' in commit['commit']['message'].lower():
                    commits_with_bug += 1
            
            # Count lines of code (just an approximation using repo size)
            total_linesize_of_code += repo['size']/12 # Estimation in MB

            # Categorize projects by size
            if repo['size']/1024 > 10:
                project_categories["big"] += 1
            elif repo['size']/1024 > 5:
                project_categories["medium"] += 1
            else:
                project_categories["small"] += 1

            # Count contributions (each commit is a contribution)
            total_contributions += len(commits)
            total_lines_of_code_read += generate_ghoc_stats(GITHUB_USERNAME,repo['name'])
            # print(total_lines_of_code_read)
        total_commits = generate_commits_stats(GITHUB_USERNAME)
        # Stack Overflow: Get user statistics
        stackoverflow_url = f'https://api.stackexchange.com/2.3/users/{STACK_OVERFLOW_USER_ID}/questions?site=stackoverflow'
        questions = get_stackoverflow_data(stackoverflow_url)
        total_stack_contributions = len(questions['items'])

        stats = {
            "total_linesize_of_code": int(total_linesize_of_code),
            "total_lines_of_code_read": total_lines_of_code_read,
            "total_commits_with_bug": commits_with_bug,
            "project_categories": project_categories,
            "total_contributions": total_contributions,
            "total_commits":total_commits,
            "total_stackoverflow_contributions": total_stack_contributions,
            # "repos":repos
        }
        r.set(str(GITHUB_USERNAME+STACK_OVERFLOW_USER_ID),stats.__str__())
    else:
        stats = eval(cache_stats)
        
    return jsonify(stats)

@app.route('/', methods=['GET'])
def home():
    return {"Hello":"World"}

if __name__ == '__main__':
    app.run(debug=True)
