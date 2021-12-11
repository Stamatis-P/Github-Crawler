from github import Github
import wget
import config
import time
from pandas import DataFrame
import numpy as np

full_names = []
stars = []
contributors_count = []
num_forks = []
# get authors of forks/stars
num_commits = []
topics = []
size = []
# add number of watchers
# add stargazers with dates

def get_rep_info(repos):
    """Given a set of repositories from Github API,
    puts their name in one text file and downloads
    zip files of their default branch to current directory"""

    array_size = repos.totalCount

    for repo in repos:
        # info
        full_names.append(repo.full_name)
        print(repo.full_name)
        stars.append(repo.stargazers_count)
        contributors = repo.get_contributors()
        contributors_count.append(contributors.totalCount)
        # print(contributor[0].login for contributor in contributors)
        num_forks.append(repo.get_forks().totalCount)
        num_commits.append(repo.get_commits().totalCount)
        topics.append(repo.get_topics())
        size.append(repo.size)
        stargazers = repo.get_stargazers_with_dates()

        # download
        default_branch = repo.default_branch
        directory = repo.name

        # required to avoid Github API rate limits
        # time.sleep(1)

        # download_url = "https://" + repo.url[12:22] + repo.url[28:] + "/archive/refs/heads/" + default_branch + ".zip"
        # print("Downloading: " + download_url)
        # path = "C:\\Users\\16507\\2021_Research\\Crawler\\repositories"
        # wget.download(download_url, out=path)


def query(auth_key, query_list):
    """Loop through all queries and perform get_rep"""
    for query in query_list:
        print("Getting repos with query: " + query)
        repos = auth_key.search_repositories(query=query, sort="stars")
        get_rep_info(repos)


if __name__ == '__main__':
    # create config.py file with attribute api_key that is a string of Github PTA
    g = Github(config.api_key)

    # split the queries by date because Github only returns 1000 search results
    query_list = ["language:python stars:>10000 created:2000-01-01..2012-01-01",
                  "language:python stars:>10000 created:2012-01-02..2013-01-01",
                  "language:python stars:>10000 created:2013-01-02..2014-01-01",
                  "language:python stars:>10000 created:2014-01-02..2015-01-01",
                  "language:python stars:>10000 created:2015-01-02..2015-11-01",
                  "language:python stars:>10000 created:2015-11-02..2016-07-01",
                  "language:python stars:>10000 created:2016-07-02..2017-01-01",
                  "language:python stars:>10000 created:2017-01-02..2017-07-01",
                  "language:python stars:>10000 created:2017-07-02..2018-01-01",
                  "language:python stars:>10000 created:2018-01-02..2018-06-01",
                  "language:python stars:>10000 created:2018-06-02..2019-01-01",
                  "language:python stars:>10000 created:2019-01-02..2019-06-01",
                  "language:python stars:>10000 created:2019-06-02..2020-01-01",
                  "language:python stars:>10000 created:2020-01-02..2021-01-01",
                  "language:python stars:>10000 created:>2021-01-01"]

    query(g, query_list)

    print(stars)

    df = DataFrame(
        {'Full_names': full_names, 'Stars': stars, 'Num_Contributors': contributors_count,
         'Num_Forks': num_forks, 'Num_Commits': num_commits, 'Topics': topics, 'Size': size})

    df.to_csv('10000_stars.csv')
