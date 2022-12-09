import time

import matplotlib.axes
import matplotlib.pyplot as plt
import pandas as pd

from components.Auction import Auction
import seaborn as sns

if __name__ == '__main__':
    start = time.time()
    data = []
    for _ in range(1000):
        auction = Auction(1000, 7, 3)
        results = auction.start()
        if not results:
            continue

        data.append(results)
    df = pd.DataFrame.from_records(data)
    print(df["second_highest_bid"].unique())
    df.to_csv("/home/kittler/Desktop/BTPAuction/results/results.csv")
    end = time.time()
    print(f"Time taken:{end - start}")
    bins = 50
    left, right = 500, 2000
    ax: matplotlib.axes.Axes = sns.histplot(df["second_highest_bid"], kde=True, bins=bins)
    # ax.set_xlim(left, right)
    fig = ax.get_figure()
    fig.savefig("/home/kittler/Desktop/BTPAuction/results/second_highest_bids.png")
    plt.clf()
    ax = sns.histplot(df["highest_bid"], kde=True, bins=bins)
    # ax.set_xlim(left, right)
    fig = ax.get_figure()
    fig.savefig("/home/kittler/Desktop/BTPAuction/results/highest_bids.png")
    plt.clf()

    ax = sns.histplot(df, x="second_highest_bid", kde=True, hue="bidder_type", bins=bins)
    # ax.set_xlim(left, right)
    fig = ax.get_figure()
    fig.savefig("/home/kittler/Desktop/BTPAuction/results/second_highest_bids_hue.png")
    plt.clf()
    ax = sns.histplot(df, x="highest_bid", kde=True, hue="bidder_type", bins=bins)
    # ax.set_xlim(left, right)
    fig = ax.get_figure()
    fig.savefig("/home/kittler/Desktop/BTPAuction/results/highest_bids_hue.png")
    plt.clf()
