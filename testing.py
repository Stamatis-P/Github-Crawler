from github import Github

if __name__ == '__main__':
    g = Github("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")

    repo = g.get_repo("Stamatis-P/project2")

    contents = repo.get_contents("")

    for content in contents:
        print(content)
        print(content.download_url)

    print(repo.url)
