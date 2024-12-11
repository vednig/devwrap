import os

from flask import (Flask, redirect, render_template, request,
                   send_from_directory, url_for,jsonify)
import requests
import datetime

app = Flask(__name__)


@app.route('/')
def index():
   print('Request for index page received')
   return render_template('index.html')

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/hello', methods=['POST'])
def hello():
   name = request.form.get('name')

   if name:
       print('Request for hello page received with name=%s' % name)
       return render_template('hello.html', name = name)
   else:
       print('Request for hello page received with no name or blank name -- redirecting')
       return redirect(url_for('index'))


# GitHub configuration
GITHUB_USERNAME = 'vednig'

# Stack Overflow configuration
STACK_OVERFLOW_USER_ID = '13935716'

def get_github_data(url):
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
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
    while url:
        response = requests.get(url, headers=headers)
        
        # Check if the repository is empty
        if response.status_code == 409 and "Git Repository is empty" in response.text:
            return []  # Return empty list if repository has no commits

        # # Check rate limit
        # remaining_requests = int(response.headers.get('X-RateLimit-Remaining', 0))
        # if remaining_requests == 0:
        #     reset_time = int(response.headers.get('X-RateLimit-Reset', 0))
        #     reset_timestamp = datetime.datetime.utcfromtimestamp(reset_time)
        #     raise Exception("GitHub rate limit exceeded.")
        
        # Check for other errors
        if response.status_code != 200:
            response.raise_for_status()
        
        # Accumulate commits
        data = response.json()
        commits.extend(data)
        
        # Check for next page of commits (pagination)
        url = response.links.get('next', {}).get('url')

    return commits


# Utility function to get StackOverflow data
def get_stackoverflow_data(url):
    response = requests.get(url)
    response.raise_for_status()
    return response.json()


@app.route('/developer-stats', methods=['GET'])
def get_developer_stats():
    # GitHub: Total lines of code written this year
    current_year = datetime.datetime.now().year
    repos_url = f'https://api.github.com/users/{GITHUB_USERNAME}/repos?per_page=100'
    repos = get_github_data(repos_url)
    
    total_lines_of_code = 0
    commits_with_bug = 0
    project_categories = {"big": 0, "medium": 0, "small": 0}
    total_contributions = 0

    # for repo in repos:
    #     # Get repository's commit history
    #     commits_url = f'https://api.github.com/repos/{GITHUB_USERNAME}/{repo["name"]}/commits?since={current_year}-01-01T00:00:00Z'
    #     commits = get_github_data(commits_url)
        
    #     # Count commits containing "bug" in their message
    #     for commit in commits:
    #         if 'bug' in commit['commit']['message'].lower():
    #             commits_with_bug += 1
        
    #     # Count lines of code (just an approximation using repo size)
    #     total_lines_of_code += repo['size'] * 10  # Estimation

    #     # Categorize projects by size
    #     if repo['size'] > 1000:
    #         project_categories["big"] += 1
    #     elif repo['size'] > 500:
    #         project_categories["medium"] += 1
    #     else:
    #         project_categories["small"] += 1

    #     # Count contributions (each commit is a contribution)
    #     total_contributions += len(commits)

    # Stack Overflow: Get user statistics
    stackoverflow_url = f'https://api.stackexchange.com/2.3/users/{STACK_OVERFLOW_USER_ID}/questions?site=stackoverflow'
    questions = get_stackoverflow_data(stackoverflow_url)
    total_stack_contributions = len(questions['items'])

    stats = {
        'total_lines_of_code': total_lines_of_code,
        'total_commits_with_bug': commits_with_bug,
        'project_categories': project_categories,
        'total_contributions': total_contributions,
        'total_stackoverflow_contributions': total_stack_contributions
    }

    return jsonify(stats)

if __name__ == '__main__':
   app.run()
