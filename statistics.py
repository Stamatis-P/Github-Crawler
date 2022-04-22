from collections import Counter

import numpy as np
import pandas
import matplotlib.pyplot as plt
from sklearn.cluster import DBSCAN
from sklearn import metrics
from tabulate import tabulate


def occurrences(lis):
    counter = sorted(Counter(lis).items())
    x = [i for i, k in counter]
    prob = [k for i, k in counter]
    prob = [val / sum(Counter(lis).values()) for val in prob]
    prob = 1 - np.cumsum(prob)
    return x, prob


def ecdf(lis):
    """Calculate empiric cumulative density function of list"""
    x, prob = occurrences(lis)
    plt.plot(x, prob)
    plt.xscale('log')
    plt.grid(True)
    plt.xlabel('size')
    plt.savefig('GMH_ecdf_size_log.png')


def scatter(lis1, lis2, loglog):
    """Create scatterplot of two lists"""
    plt.scatter(lis1, lis2)
    plt.title('SGMH forks vs stars loglog')
    plt.xlabel('stars')
    plt.ylabel('forks')
    if loglog:
        plt.xscale('log')
        plt.yscale('log')
    plt.grid()

    plt.show()


def hexbin(lis1, lis2):
    """Create logarithmic heatmap plot of two lists"""
    x = lis1
    y = lis2

    x = nonnegative_test(lis1)
    y = nonnegative_test(lis2)

    hb = plt.hexbin(x, y, gridsize=50, bins="log", xscale='log', yscale='log', cmap='inferno')
    plt.title("forks vs stars")
    plt.xlabel('stars')
    plt.ylabel('forks')
    cb = plt.colorbar(hb, label='log10(N)')
    plt.axhline(y=2500, color='r', linestyle='-')
    plt.axvline(x=600, color='r', linestyle='-')
    plt.axvline(x=2500, color='r', linestyle='-')

    plt.show()
    # plt.savefig('no_log_bin_SGMH_heat_size_vs_stars_loglog.png')


def nonnegative_test(lis1):
    """
    Test for nonnegativity in list
    If all elements are nonnegative, return list
    Else, add 1 to all elements
    """
    dummy = lis1
    for i in lis1:
        if i <= 0:
            dummy = [j + 1 for j in lis1]
            return dummy
    return dummy


def get_lists(file):
    column_names = ["Full_Names", "Stars", "forks", "commits", "Topics", "Size"]
    df = pandas.read_csv(file, names=column_names)

    full_names = df.Full_Names.to_list()
    stars = df.Stars.to_list()
    forks = df.forks.to_list()
    commits = df.commits.to_list()
    topics = df.commits.to_list()
    size = df.Size.to_list()

    del full_names[0]
    del stars[0]
    del forks[0]
    del commits[0]
    del topics[0]
    del size[0]

    stars = [int(star) for star in stars]
    forks = [int(num_fork) for num_fork in forks]
    commits = [int(num_commit) for num_commit in commits]
    size = [int(siz) for siz in size]

    return full_names, stars, forks, commits, topics, size


def histogram1d(lis):
    plt.hist(lis, bins=3000)
    plt.xscale("log")
    plt.yscale("log")
    plt.ylabel("count")
    plt.xlabel("forks")
    plt.title("Forks 1-D Histogram")
    plt.savefig("SGMH_hist1d_forks_loglog.png")


def dbscan2d(full_names, x, y):
    """Perform dbscan on two lists and plot the results"""
    # Preprocess lists
    x = nonnegative_test(x)
    x = np.asarray(x)
    y = nonnegative_test(y)
    y = np.asarray(y)
    x_log = np.log10(x)
    y_log = np.log10(y)

    # Compute DBSCAN
    data = list(zip(x_log, y_log))
    data = np.asarray(data)
    db = DBSCAN(eps=0.15, min_samples=10).fit(data)
    core_samples_mask = np.zeros_like(db.labels_, dtype=bool)
    core_samples_mask[db.core_sample_indices_] = True
    labels = db.labels_

    # write noisy repositories to a file
    noise = []
    for i in range(len(labels)):
        if labels[i] == -1:
            noise.append(full_names[i])

    with open('noisy_reps_forks_stars.txt', 'w') as f:
        for rep in noise:
            f.write(rep)
            f.write('\n')

    # Plot
    # Number of clusters in labels, ignoring noise if present.
    n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)
    n_noise_ = list(labels).count(-1)

    print("Estimated number of clusters: %d" % n_clusters_)
    print("Estimated number of noise points: %d" % n_noise_)

    print("Silhouette Coefficient: %0.3f" % metrics.silhouette_score(data, labels))

    # Plot results
    # Black removed and is used for noise instead.
    unique_labels = set(labels)
    colors = [plt.cm.Spectral(each) for each in np.linspace(0, 1, len(unique_labels))]
    for k, col in zip(unique_labels, colors):
        if k == -1:
            # Black used for noise.
            col = [0, 0, 0, 1]

        class_member_mask = labels == k

        xy = data[class_member_mask & core_samples_mask]
        plt.plot(
            xy[:, 0],
            xy[:, 1],
            "o",
            markerfacecolor=tuple(col),
            markeredgecolor="k",
            markersize=14,
        )

        xy = data[class_member_mask & ~core_samples_mask]
        plt.plot(
            xy[:, 0],
            xy[:, 1],
            "o",
            markerfacecolor=tuple(col),
            markeredgecolor="k",
            markersize=6,
        )

    plt.title("Forks vs Stars")
    plt.xlabel("stars")
    plt.ylabel("forks")
    plt.savefig("SGMH_DBSCAN_forks_stars.png")
    plt.show()


def dbscan_all(full_names, stars, forks, commits, size):
    """Perform dbscan on all four lists"""
    full_names = np.asarray(full_names)
    stars = nonnegative_test(stars)
    stars = np.asarray(stars)
    forks = nonnegative_test(forks)
    forks = np.asarray(forks)
    commits = nonnegative_test(commits)
    commits = np.asarray(commits)
    size = nonnegative_test(size)
    size = np.asarray(size)

    stars_log = np.log10(stars)
    forks_log = np.log10(forks)
    commits_log = np.log10(commits)
    size_log = np.log10(size)

    data = list(zip(stars_log, forks_log, commits_log, size_log))
    data = np.asarray(data)

    db = DBSCAN(eps=0.55, min_samples=10).fit(data)
    core_samples_mask = np.zeros_like(db.labels_, dtype=bool)
    core_samples_mask[db.core_sample_indices_] = True
    labels = db.labels_

    # Number of clusters in labels, ignoring noise if present.
    n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)
    n_noise_ = list(labels).count(-1)

    print("Estimated number of clusters: %d" % n_clusters_)
    print("Estimated number of noise points: %d" % n_noise_)

    outlier_reps = np.sort(full_names[labels == -1])

    with open('noisy_reps.txt', 'w') as f:
        for rep in outlier_reps:
            f.write(rep)
            f.write('\n')

    return data, labels, n_clusters_


def analyze_dbscan_all(data, labels, n_clusters):
    """Analyze results of DBSCAN on four lists"""
    data = np.power(10, data)  # undo log_10 in data
    undo_minus = np.array([0, 1, 0, 1])  # forks and size at index 1 and 3 of the array are log(x+1), undo the +1

    # separates each cluster in the data (including outliers) and subtracts the one from forks and size
    clusters = [data[labels == i] - undo_minus for i in range(n_clusters)]
    outliers = data[labels == -1] - undo_minus
    clusters.append(outliers)

    mean = [np.mean(cluster, axis=0) for cluster in clusters]
    med = [np.median(cluster, axis=0) for cluster in clusters]
    std = [np.std(cluster, axis=0) for cluster in clusters]
    min = [np.amin(cluster, axis=0) for cluster in clusters]
    max = [np.amax(cluster, axis=0) for cluster in clusters]

    print(tabulate(mean, headers=["Index", "Stars", "Forks", "Commits", "Size"], showindex='always'))


def repositories_to_string(repository_names, x, y, x_range, y_range):
    """
    count = 0
    string = "{count} index: {i} Full Name: {full_name} Stars: {stars} Number of Forks: {forks} Number of " \
             "Commits: {commits} Topics: {topics} Size: {size} "

    for i in range(len(stars)):
        if 2500 > stars[i] > 600 and forks[i] > 2500:
            count += 1
            print(string.format(count=count, i=i, full_name=full_names[i], stars=stars[i], forks=forks[i],
                                commits=commits[i], topics=topics[i], size=size[i]))
            print(full_names[i])

    """


def preprocess(*csvs):
    full_names = []
    stars = []
    forks = []
    commits = []
    topics = []
    size = []
    for csv in csvs:
        full_names_add, stars_add, forks_add, commits_add, topics_add, size_add = get_lists(csv)
        full_names += full_names_add
        stars += stars_add
        forks += forks_add
        commits += commits_add
        topics += topics_add
        size += size_add

    return full_names, stars, forks, commits, topics, size


if __name__ == '__main__':
    # preprocess("70..79_stars.csv", "80..89_stars.csv", "90..100_stars.csv", "100..149_stars.csv", "150..199_stars.csv",
    #            "200..299_stars.csv", "300..1000_stars.csv", "1000_stars.csv")

    full_names1, stars1, forks1, commits1, topics1, size1 = get_lists("300..1000_stars.csv")
    full_names2, stars2, forks2, commits2, topics2, size2 = get_lists("1000_stars.csv")
    full_names3, stars3, forks3, commits3, topics3, size3 = get_lists("200..299_stars.csv")
    full_names4, stars4, forks4, commits4, topics4, size4 = get_lists("150..199_stars.csv")
    full_names5, stars5, forks5, commits5, topics5, size5 = get_lists("100..149_stars.csv")
    full_names6, stars6, forks6, commits6, topics6, size6 = get_lists("90..100_stars.csv")
    full_names7, stars7, forks7, commits7, topics7, size7 = get_lists("80..89_stars.csv")
    full_names8, stars8, forks8, commits8, topics8, size8 = get_lists("70..79_stars.csv")

    count = 0
    for i in range(len(stars6)):
        if stars6[i] == 100:
            del full_names6[i - count]
            del forks6[i - count]
            del commits6[i - count]
            del topics6[i - count]
            del size6[i - count]
            count += 1

    stars6 = [value for value in stars6 if value != 100]

    full_names = full_names1 + full_names2 + full_names3 + full_names4 + full_names5 + full_names6 + full_names7 + full_names8
    stars = stars1 + stars2 + stars3 + stars4 + stars5 + stars6 + stars7 + stars8
    forks = forks1 + forks2 + forks3 + forks4 + forks5 + forks6 + forks7 + forks8
    commits = commits1 + commits2 + commits3 + commits4 + commits5 + commits6 + commits7 + commits8
    topics = topics1 + topics2 + topics3 + topics4 + topics5 + topics6 + topics7 + topics8
    size = size1 + size2 + size3 + size4 + size5 + size6 + size7 + size8

    data, labels, nclusters = dbscan_all(full_names, stars, forks, commits, size)
    analyze_dbscan_all(data, labels, nclusters)
