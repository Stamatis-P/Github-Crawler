from github import Github

if __name__ == '__main__':
    g = Github("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")
    count = 0

    repos = g.search_repositories(query = "language:python stars:>1000", sort="stars")
    for repo in repos:
        if count > 10:
            break
        print(repo.url)
        count += 1
