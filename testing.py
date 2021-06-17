from github import Github
import requests
import config
import wget

if __name__ == '__main__':
    OUTPUT_FOLDER = "C:/Users/stama/2021_Research/Crawler/Results/"
    g = Github(config.api_key)

    repo = g.get_repo("donnemartin/system-design-primer")

    directory = repo.name
    clone_url = repo.git_url
    download_url = "https://" + repo.url[12:22] + repo.url[28:] + "/archive/refs/heads/master.zip"
    print(download_url)
    wget.download(download_url)
    # print(clone_url)
