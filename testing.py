from github import Github
import requests
import config

if __name__ == '__main__':
    g = Github(config.api_key)

    repo = g.get_repo("Stamatis-P/project2")

    contents = repo.get_contents("")

    for content in contents:
        url = content.download_url
        r = requests.get(url)
        open(content.name, "wb").write(r.content)