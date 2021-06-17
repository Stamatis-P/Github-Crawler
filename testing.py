from github import Github
import requests
import config

if __name__ == '__main__':
    g = Github(config.api_key)

    repo = g.get_repo("Stamatis-P/project2")

    directory = repo.name
    download_url = repo.url + "/zipball/main"
    print(download_url)
    requests.get(download_url, allow_redirects=True)
    r = requests.get(download_url, allow_redirects=True)
    print(r)

    requests.get("https://api.github.com/repos/hadley/devtools/zipball/master")
