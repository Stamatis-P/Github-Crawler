from github import Github
import config
import wget

if __name__ == '__main__':
    OUTPUT_FOLDER = "C:/Users/stama/2021_Research/Crawler/Results/"
    g = Github(config.api_key)

    repo = g.get_repo("donnemartin/system-design-primer")

    directory = repo.name
    default_branch = repo.default_branch
    print(default_branch)
    download_url = "https://" + repo.url[12:22] + repo.url[28:] + "/archive/refs/heads/" + default_branch + ".zip"
    print(download_url)
    # wget.download(download_url)
