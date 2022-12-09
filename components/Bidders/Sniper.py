from numpy.random import rand, normal

from components.Bidder import Bidder


class Sniper(Bidder):
    def __init__(self):
        super().__init__()
        self.TOTAL_AUCTION_TIME = 500
        self.bid_prob_b = 1
        self.id = None
        price = 2000
        self.L = normal(loc=price, scale=price/3, size=1)[0]
        self.v = None
        self.watch_probability = 0.15

    def set_bidder_id(self, bidder_id):
        self.id = bidder_id

    def get_bid(self, time, highest_bidder_id, second_highest_bid):
        if highest_bidder_id and highest_bidder_id == self.id:
            return None
        if time < self.TOTAL_AUCTION_TIME - 20:
            return None
        if not self.L:
            return None
        if not self.is_bidder_watching():
            return None
        c = self.get_c()
        self.v = min(self.L, c * second_highest_bid)
        if not self.does_bidder_bid(time):
            return None
        return self.v

    def does_bidder_bid(self, time):
        return rand() < self.bid_prob_b

    def is_bidder_watching(self):
        return rand() < self.watch_probability

    @staticmethod
    def get_c():
        return 2
