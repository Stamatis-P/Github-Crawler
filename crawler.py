from github import Github

import config

if __name__ == '__main__':
    g = Github(config.api_key)
    count = 0

    repos = g.search_repositories(query = "language:python stars:>1000", sort="stars")
    for repo in repos:
        if count > 10:
            break
        print(repo.url)
        count += 1
