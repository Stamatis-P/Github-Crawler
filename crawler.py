from github import Github
import os
import requests
import config

if __name__ == '__main__':
    g = Github(config.api_key)
    count = 0

    repos = g.search_repositories(query = "language:python stars:>1000", sort="stars")
    for repo in repos:
        if count > 10:
            break
        count += 1

        directory = repo.name
        parent_directory = "C:\\Users\\stama\\2021_Research\\Crawler"

        path = os.path.join(parent_directory, directory)
        os.mkdir(path)

        contents = repo.get_contents("")

        for content in contents:
            #current issue I believe comes from when content is a directory, will fix
            url = content.download_url
            path = directory + "/" + content.name
            r = requests.get(url)
            open(path, "wb").write(r.content)
