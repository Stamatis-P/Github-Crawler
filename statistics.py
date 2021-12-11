from collections import Counter

import numpy as np
import pandas
import matplotlib.pyplot as plt


def occurrences(lis):
    print(sum(Counter(lis).values()))
    counter = sorted(Counter(lis).items())
    print(counter)
    x = [i for i, k in counter]
    prob = [k for i, k in counter]
    prob = [val / sum(Counter(lis).values()) for val in prob]
    print(prob)
    prob = 1 - np.cumsum(prob)
    print(prob)
    ecdf(x, prob)


def ecdf(x, prob):
    #x = [y for y in x if y < 10000]
    #prob = prob[:len(x)]
    plt.loglog(x, prob)
    plt.grid(True)
    plt.xlabel('size')
    plt.savefig('10000_ecdf_size_loglog.png')


def scatter(lis1, lis2):
    plt.scatter(lis1, lis2)
    plt.xlabel('stars')
    plt.ylabel('size')
    plt.xscale('log')
    plt.yscale('log')
    #plt.xlim([1000, 10000])
    #plt.ylim([0, 50000])
    plt.savefig('1000_stars_size_scatter_loglog.png')

def heatmap(lis1, lis2):
    hmap, xedges, yedges = np.histogram2d(lis1, lis2, bins=(1000, 100))

    plt.clf()
    plt.imshow(hmap.T, origin='lower')
    plt.show()


def get_lists(file):
    column_names = ["Full_Names", "Stars", "Num_Forks", "Num_Commits", "Topics", "Size"]
    df = pandas.read_csv(file, names=column_names)

    full_names = df.Full_Names.to_list()
    stars = df.Stars.to_list()
    num_forks = df.Num_Forks.to_list()
    num_commits = df.Num_Commits.to_list()
    topics = df.Num_Commits.to_list()
    size = df.Size.to_list()

    del full_names[0]
    del stars[0]
    del num_forks[0]
    del num_commits[0]
    del topics[0]
    del size[0]

    stars = [int(star) for star in stars]
    num_forks = [int(num_fork) for num_fork in num_forks]
    num_commits = [int(num_commit) for num_commit in num_commits]
    size = [int(siz) for siz in size]

    #occurrences(size)
    scatter(stars, size)
    #heatmap(stars, num_forks)


if __name__ == '__main__':
    get_lists("1000_stars.csv")
