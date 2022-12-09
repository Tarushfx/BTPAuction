from numpy.random import rand, uniform, choice, normal

from components.Bidder import Bidder


class EarlyBidder(Bidder):
    def __init__(self):
        super().__init__()
        self.id = None
        self.bid_prob_b = 0.3
        self.watch_probability = 0.05
        price = 1500
        self.L = normal(loc=price, scale=price / 3, size=1)[0]
        self.v = normal(loc=price / 5, scale=price / 15, size=1)[0]

    def get_bidding_probabilty(self, time):
        return 1 - (time / self.TOTAL_AUCTION_TIME)

    def set_bidder_id(self, bidder_id):
        self.id = bidder_id

    def get_bid(self, time, highest_bidder_id, second_highest_bid):
        if highest_bidder_id and highest_bidder_id == self.id:
            return None

        if not self.v:
            self.v = self.L / 1000
        if not self.is_bidder_watching():
            return None
        L, v = self.L, self.v
        c = self.get_c()

        self.v = min(L, c * v)

        if second_highest_bid and self.v <= second_highest_bid:
            return None

        if not self.does_bidder_bid(time):
            return None

        return self.v

    def does_bidder_bid(self, time):
        return rand() < self.get_bidding_probabilty(time)

    def is_bidder_watching(self):
        return rand() < self.watch_probability

    @staticmethod
    def get_c():
        return uniform(1.2, 2)
