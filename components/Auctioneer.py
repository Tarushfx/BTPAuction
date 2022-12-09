from numpy.random import seed, normal


class Auctioneer:
    def __init__(self, marketprice, total_bidders, bidders):
        self.MIN_PRICE = 1
        self.marketprice = marketprice
        self.total_bidders = total_bidders
        self.bidders = bidders



