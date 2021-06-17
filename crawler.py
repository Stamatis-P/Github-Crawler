from github import Github
import os
import requests
import config
import time

def get_rep(repos):
    for repo in repos:
        directory = repo.name
        # print(directory)

        with open("repository_names.txt", "a") as f:
            f.write(directory + "\n")
        time.sleep(2)

        # parent_directory = "C:\\Users\\stama\\2021_Research\\Crawler"

        # path = os.path.join(parent_directory, directory)
        # os.mkdir(path)

        # contents = repo.get_contents("")

        # for content in contents:
        # current issue I believe comes from when content is a directory, will fix
        # url = content.download_url
        # path = directory + "/" + content.name
        # r = requests.get(url)
        # open(path, "wb").write(r.content)


if __name__ == '__main__':
    g = Github(config.api_key)
    count = 0

    repos = g.search_repositories(query="language:python stars:>300 created:2000-01-01..2012-01-01", sort="stars")
    get_rep(repos)

    repos = g.search_repositories(query="language:python stars:>300 created:2012-01-02..2013-01-01", sort="stars")
    get_rep(repos)
    print("2012-01-02..2013-01-01 Done!")

    repos = g.search_repositories(query="language:python stars:>300 created:2013-01-02..2014-01-01", sort="stars")
    get_rep(repos)
    print("2013-01-02..2014-01-01 Done!")

    repos = g.search_repositories(query="language:python stars:>300 created:2014-01-02..2015-01-01", sort="stars")
    get_rep(repos)
    print("2014-01-02..2015-01-01 Done!")

    repos = g.search_repositories(query="language:python stars:>300 created:2015-01-02..2015-11-01", sort="stars")
    get_rep(repos)
    print("2015-01-02..2015-11-01 Done!")

    repos = g.search_repositories(query="language:python stars:>300 created:2015-11-02..2016-07-01", sort="stars")
    get_rep(repos)
    print("2015-11-02..2016-07-01 Done!")

    repos = g.search_repositories(query="language:python stars:>300 created:2016-07-02..2017-01-01", sort="stars")
    get_rep(repos)
    print("2016-07-02..2017-01-01 Done!")

    repos = g.search_repositories(query="language:python stars:>300 created:2017-01-01..2017-07-01", sort="stars")
    get_rep(repos)
    print("2017-01-01..2017-07-01 Done!")

    repos = g.search_repositories(query="language:python stars:>300 created:2017-07-02..2018-01-01", sort="stars")
    get_rep(repos)
    print("2017-07-02..2018-01-01 Done!")

    repos = g.search_repositories(query="language:python stars:>300 created:2018-01-02..2018-06-01", sort="stars")
    get_rep(repos)
    print("2018-01-02..2018-06-01 Done!")

    repos = g.search_repositories(query="language:python stars:>300 created:2018-06-02..2019-01-01", sort="stars")
    get_rep(repos)
    print("2018-06-02..2019-01-01 Done!")

    repos = g.search_repositories(query="language:python stars:>300 created:2019-01-02..2019-06-01", sort="stars")
    get_rep(repos)
    print("2019-01-02..2019-06-01 Done!")

    repos = g.search_repositories(query="language:python stars:>300 created:2019-06-02..2020-01-01", sort="stars")
    get_rep(repos)
    print("2019-06-02..2020-01-01 Done!")

    repos = g.search_repositories(query="language:python stars:>300 created:2020-01-02..2021-01-01", sort="stars")
    get_rep(repos)
    print("2020-01-02..2021-01-01 Done!")

    repos = g.search_repositories(query="language:python stars:>300 created:>2021-01-01", sort="stars")
    get_rep(repos)
    print(">2021-01-01 Done!")
