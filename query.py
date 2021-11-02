import os

from github import Github
import wget
import config
import time
from pandas import DataFrame

full_names = []
stars = []
stargazers_users = []
stargazers_login_usernames = []
stargazers_login_times = []
contributors_count = []
contributors_users = []
contributors_names = []
num_forks = []

num_commits = []
topics = []
size = []

def get_rep_info(repos):
    """Given a set of repositories from Github API,
    puts their name in one text file and downloads
    zip files of their default branch to current directory"""

    for repo in repos:
        # info
        full_names.append(repo.full_name)
        print(repo.full_name)
        stars.append(repo.stargazers_count)
        stargazers_user, stargazers_login_username, stargazers_login_time = get_stargazers_list(repo)
        stargazers_users.append(stargazers_user)
        stargazers_login_usernames.append(stargazers_login_username)
        stargazers_login_times.append(stargazers_login_time)
        num_contributors, contributors_user, contributors_name = get_contributors_list(repo)
        contributors_count.append(num_contributors)
        contributors_users.append(contributors_user)
        contributors_names.append(contributors_name)
        num_forks.append(repo.get_forks().totalCount)
        num_commits.append(repo.get_commits().totalCount)
        topics.append(repo.get_topics())
        size.append(repo.size)

        # download
        default_branch = repo.default_branch

        # required to avoid Github API rate limits
        time.sleep(1)

        download_url = "https://" + repo.url[12:22] + repo.url[28:] + "/archive/refs/heads/" + default_branch + ".zip"
        print("Downloading: " + download_url)
        path = "C:\\Users\\16507\\2021_Research\\Track2\\repositories300..1000"
        repo_full_name = repo.owner.login + "--" + repo.name
        os.mkdir(os.path.join (path, repo_full_name))
        dest = "C:\\Users\\16507\\2021_Research\\Track2\\repositories300..1000" + "\\" + repo_full_name
        print(dest)
        wget.download(download_url, out=dest)

        df = DataFrame(
            {'Full_names': full_names, 'Stars': stars, 'Stargazers Users': stargazers_users,
             "Stargazers Names": stargazers_login_usernames, "Stargazers Times": stargazers_login_times,
             'Num_Contributors': num_contributors, "Contributors Users": contributors_users,
             "Contributors Names:": contributors_names, 'Num_Forks': num_forks, 'Num_Commits': num_commits,
             'Topics': topics, 'Size': size})

        df.to_csv('300..1000_stars.csv')

def query(auth_key, query_list):
    """Loop through all queries and perform get_rep"""
    for query in query_list:
        print("Getting repos with query: " + query)
        repos = auth_key.search_repositories(query=query, sort="stars")
        get_rep_info(repos)


def get_stargazers_list(repo):
    stars_list = repo.get_stargazers_with_dates()
    stargazers = repo.get_stargazers()
    number_of_stargazers = stars_list.totalCount

    stargazers_user = []
    stargazers_login_username = []
    stargazers_login_time = []

    for i in range(0, number_of_stargazers):
        user = stars_list[i].user.login
        #time.sleep(1)
        star_time = stars_list[i].starred_at
        name = stargazers[i].name
        #time.sleep(1)
        stargazers_user.append(user) if user is not None else stargazers_user.append("None")
        stargazers_login_username.append(name) if name is not None else stargazers_login_username.append("None")
        stargazers_login_time.append(star_time.strftime("%m/%d/%Y, %H:%M:%S"))

    return stargazers_user, stargazers_login_username, stargazers_login_time


def get_contributors_list(repo):
    contributors_list = repo.get_contributors()
    number_of_contributors = contributors_list.totalCount

    contributors_user = []
    contributors_name = []

    for i in range(0, number_of_contributors):
        login = contributors_list[i].login
        #time.sleep(1)
        name = contributors_list[i].name
        #time.sleep(1)
        contributors_user.append(login) if login is not None else contributors_user.append("None")
        contributors_name.append(name) if name is not None else contributors_name.append("None")

    return number_of_contributors, contributors_user, contributors_name


if __name__ == '__main__':
    # create config.py file with attribute api_key that is a string of Github PTA
    g = Github(config.api_key)
    # "language:python stars:300..1000 created:2000-01-01..2012-01-01",
    # "language:python stars:300..1000 created:2012-01-02..2013-01-01",
    # "language:python stars:300..1000 created:2013-01-02..2014-01-01",
    # "language:python stars:300..1000 created:2014-01-02..2015-01-01",
    # "language:python stars:300..1000 created:2015-01-02..2015-11-01",
    # "language:python stars:300..1000 created:2015-11-02..2016-07-01",
    # "language:python stars:300..1000 created:2016-07-02..2017-01-01",
    # "language:python stars:300..1000 created:2017-01-02..2017-07-01",
    # "language:python stars:300..1000 created:2017-07-02..2018-01-01",
    # "language:python stars:300..1000 created:2018-01-02..2018-06-01",
    # "language:python stars:300..1000 created:2018-06-02..2019-01-01",
    # "language:python stars:300..1000 created:2019-01-02..2019-06-01",
    # "language:python stars:300..1000 created:2019-06-02..2020-01-01",
    # "language:python stars:300..1000 created:2020-01-02..2021-01-01",
    # "language:python stars:300..1000 created:>2021-01-01"

    # split the queries by date because Github only returns 1000 search results
    query_list = [
        "language:python stars:300..1000 created:2000-01-01..2012-01-01",
        "language:python stars:300..1000 created:2012-01-02..2013-01-01",
        "language:python stars:300..1000 created:2013-01-02..2014-01-01",
        "language:python stars:300..1000 created:2014-01-02..2015-01-01",
        "language:python stars:300..1000 created:2015-01-02..2015-11-01",
        "language:python stars:300..1000 created:2015-11-02..2016-07-01",
        "language:python stars:300..1000 created:2016-07-02..2017-01-01",
        "language:python stars:300..1000 created:2017-01-02..2017-07-01",
        "language:python stars:300..1000 created:2017-07-02..2018-01-01",
        "language:python stars:300..1000 created:2018-01-02..2018-06-01",
        "language:python stars:300..1000 created:2018-06-02..2019-01-01",
        "language:python stars:300..1000 created:2019-01-02..2019-06-01",
        "language:python stars:300..1000 created:2019-06-02..2020-01-01",
        "language:python stars:300..1000 created:2020-01-02..2021-01-01",
        "language:python stars:300..1000 created:>2021-01-01"
    ]

    query(g, query_list)
