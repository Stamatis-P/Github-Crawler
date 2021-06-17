from github import Github
import requests
import os
import config

if __name__ == '__main__':
    g = Github(config.api_key)

    repos = g.get_user().get_repos()

    for repo in repos:
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
