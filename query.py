import os

import github
from github import Github
import wget
import config
import time
from pandas import DataFrame

full_names = []
stars = []
stargazers_users = []
stargazers_login_times = []
contributors_count = []
contributors_users = []
num_contributors = []
num_forks = []

num_commits = []
topics = []
size = []


def get_rep_info(repos):  # 16 requests + 2 * num_stars + 1 * num_contributors
    """Given a set of repositories from Github API,
    puts their name in one text file and downloads
    zip files of their default branch to current directory"""

    for repo in repos:
        # info
        full_name = repo.full_name  # 1 request
        full_names.append(full_name)
        print(full_name)

        stars.append(repo.stargazers_count)  # 1 request
        # stargazers_count, stargazers_user, stargazers_login_time = get_stargazers_list(repo)  # 2 requests + 2 per star
        # stars.append(stargazers_count)
        # stargazers_users.append(stargazers_user)
        # stargazers_login_times.append(stargazers_login_time)

        # num_contributor, contributors_user = get_contributors_list(repo)  # 2 requests + 1 per contributor
        # num_contributors.append(num_contributors)
        # contributors_count.append(num_contributors)
        # contributors_users.append(contributors_user)

        num_forks.append(repo.get_forks().totalCount)  # 2 requests

        num_commits.append(repo.get_commits().totalCount)  # 2 requests

        topics.append(repo.get_topics())  # 1 request

        size.append(repo.size)  # 1 request

        # download
        default_branch = repo.default_branch  # 1 request

        try:
            download_url = "https://" + repo.url[12:22] + repo.url[
                                                          28:] + "/archive/refs/heads/" + default_branch + ".zip"
            path = "C:\\Users\\16507\\2021_Research\\Track2\\repositories1k"
            repo_full_name = repo.owner.login + "--" + repo.name
            os.mkdir(os.path.join(path, repo_full_name))
            dest = "C:\\Users\\16507\\2021_Research\\Track2\\repositories1k" + "\\" + repo_full_name
            print("Downloading: " + download_url)
            wget.download(download_url, out=dest)
        except FileExistsError:
            continue

        df = DataFrame(
            {'Full_names': full_names, 'Stars': stars,
             'Num_Forks': num_forks, 'Num_Commits': num_commits,
             'Topics': topics, 'Size': size})

        df.to_csv('1000_stars_1.csv')


def query(auth_key, query_list):
    """Loop through all queries and perform get_rep"""
    for query in query_list:
        print("Getting repos with query: " + query)
        repos = auth_key.search_repositories(query=query, sort="stars")
        get_rep_info(repos)


def get_stargazers_list(repo):  # 2 requests + 2 per star
    stars_list = repo.get_stargazers_with_dates()  # 1 request
    number_of_stargazers = stars_list.totalCount  # 1 request

    stargazers_user = []
    stargazers_login_time = []

    for i in range(0, number_of_stargazers):
        user = stars_list[i].user.login  # 1 request
        star_time = stars_list[i].starred_at  # 1 request
        stargazers_user.append(user) if user is not None else stargazers_user.append("None")
        stargazers_login_time.append(star_time.strftime("%m/%d/%Y, %H:%M:%S"))

    return number_of_stargazers, stargazers_user, stargazers_login_time


def get_contributors_list(repo):  # 2 requests + 1 per contributor
    contributors_list = repo.get_contributors()  # 1 request
    number_of_contributors = contributors_list.totalCount  # 1 request

    contributors_user = []

    for i in range(0, number_of_contributors):
        login = contributors_list[i].login  # 1 request
        contributors_user.append(login) if login is not None else contributors_user.append("None")

    return number_of_contributors, contributors_user


if __name__ == '__main__':
    # create config.py file with attribute api_key that is a string of Github PTA
    g = Github(config.api_key)

    # split the queries by date because Github only returns 1000 search results
    #"language:python stars:>1000 created:2000-01-01..2012-01-01",
        #"language:python stars:>1000 created:2012-01-02..2013-01-01",
        #"language:python stars:>1000 created:2013-01-02..2014-01-01",
        #"language:python stars:>1000 created:2014-01-02..2015-01-01",
        #"language:python stars:>1000 created:2015-01-02..2015-11-01",
    #"language:python stars:>1000 created:2015-11-02..2016-07-01",
    #"language:python stars:>1000 created:2016-07-02..2017-01-01",
    #"language:python stars:>1000 created:2017-01-02..2017-07-01",
    #        "language:python stars:>1000 created:2017-07-02..2018-01-01",
    #        "language:python stars:>1000 created:2018-01-02..2018-06-01",
   #     "language:python stars:>1000 created:2018-06-02..2019-01-01",
     #   "language:python stars:>1000 created:2019-01-02..2019-06-01",
     #   "language:python stars:>1000 created:2019-06-02..2020-01-01",
    query_list = [

        "language:python stars:>1000 created:2020-01-02..2021-01-01",
        "language:python stars:>1000 created:>2021-01-01"
    ]
    query(g, query_list)
