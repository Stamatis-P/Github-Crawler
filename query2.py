
from github import Github
import config2




if __name__ == '__main__':
    # create config.py file with attribute api_key that is a string of Github PTA
    g = Github(config2.api_key)

    repo = g.get_repo("echen102/us-pres-elections-2020")
    print(repo.size)

