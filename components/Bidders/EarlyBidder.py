from numpy.random import rand, uniform, choice

from components.Bidder import Bidder


class EarlyBidder(Bidder):
    def __init__(self):
        super().__init__()
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

        if not self.v:
            self.v = self.L / 10
        L, v = self.L, self.v
        c = self.get_c()

        self.v = min(L, c * v)

        if second_highest_bid and self.v <= second_highest_bid:
            return None

        if not self.does_bidder_bid():
            return None

        return self.v

    def does_bidder_bid(self):
        return rand() < self.bid_prob_b

    @staticmethod
    def get_c():
        return uniform(1.2, 2)
