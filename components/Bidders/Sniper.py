from numpy.random import rand

from components.Bidder import Bidder


class Sniper(Bidder):
    def __init__(self):
        super().__init__()
        self.TOTAL_AUCTION_TIME = 500
        self.id = None
        self.L = None
        self.v = None

    def set_priv_limit(self, pl):
        self.L = pl

    def set_bidder_id(self, bidder_id):
        self.id = bidder_id

    def get_bid(self, time, highest_bidder_id, second_highest_bid):
        if highest_bidder_id and highest_bidder_id == self.id:
            return None
        if time < self.TOTAL_AUCTION_TIME - 20:
            return None
        if not self.L:
            return None
        self.v = min(self.L, 2 * second_highest_bid)
        if not self.does_bidder_bid():
            return None
        return self.v

    def does_bidder_bid(self):
        return rand() < self.bid_prob_b
