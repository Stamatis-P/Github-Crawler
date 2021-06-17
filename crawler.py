from github import Github
import wget
import config
import time


def get_rep(repos):
    """Given a set of repositories from Github API,
    puts their name in one text file and downloads
    zip files of their default branch to current directory"""

    for repo in repos:
        directory = repo.name
        default_branch = repo.default_branch

        with open("repository_names.txt", "a") as f:
            f.write(directory + "\n")

        # required to avoid Github API rate limits
        time.sleep(2)

        download_url = "https://" + repo.url[12:22] + repo.url[28:] + "/archive/refs/heads/" + default_branch + ".zip"
        print("Downloading: " + download_url)
        wget.download(download_url)


def query(auth_key, query_list):
    """Loop through all queries and perform get_rep"""
    for query in query_list:
        print("Getting repos with query: " + query)
        repos = auth_key.search_repositories(query=query, sort="stars")
        get_rep(repos)


if __name__ == '__main__':

    # create config.py file with attribute api_key that is a string of Github PTA
    g = Github(config.api_key)

    # split the queries by date because Github only returns 1000 search results
    query_list = ["language:python stars:>300 created:2000-01-01..2012-01-01",
                  "language:python stars:>300 created:2012-01-02..2013-01-01",
                  "language:python stars:>300 created:2013-01-02..2014-01-01",
                  "language:python stars:>300 created:2014-01-02..2015-01-01",
                  "language:python stars:>300 created:2015-01-02..2015-11-01",
                  "language:python stars:>300 created:2015-11-02..2016-07-01",
                  "language:python stars:>300 created:2016-07-02..2017-01-01",
                  "language:python stars:>300 created:2017-01-02..2017-07-01",
                  "language:python stars:>300 created:2017-07-02..2018-01-01",
                  "language:python stars:>300 created:2018-01-02..2018-06-01",
                  "language:python stars:>300 created:2018-06-02..2019-01-01",
                  "language:python stars:>300 created:2019-01-02..2019-06-01",
                  "language:python stars:>300 created:2019-06-02..2020-01-01",
                  "language:python stars:>300 created:2020-01-02..2021-01-01",
                  "language:python stars:>300 created:>2021-01-01"]

    query(g, query_list)
