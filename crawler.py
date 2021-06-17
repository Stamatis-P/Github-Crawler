from github import Github
import os
import requests
import config
import time

if __name__ == '__main__':
    g = Github(config.api_key)
    count = 0

    repos = g.search_repositories(query = "language:python stars:>300", sort="stars")
    for repo in repos:
        count += 1
        if count > 10000:
            break

        directory = repo.name
        print(str(count) + ": " + directory)

        with open("repository_names.txt", "a") as f:
            f.write(str(count) + ": " + directory + "\n")
        time.sleep(4)
        #parent_directory = "C:\\Users\\stama\\2021_Research\\Crawler"

        #path = os.path.join(parent_directory, directory)
        #os.mkdir(path)

        #contents = repo.get_contents("")

        #for content in contents:
            #current issue I believe comes from when content is a directory, will fix
            #url = content.download_url
            #path = directory + "/" + content.name
            #r = requests.get(url)
            #open(path, "wb").write(r.content)
