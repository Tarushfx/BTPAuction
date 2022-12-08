from numpy.random import rand

from components.Bidder import Bidder


class Shiller(Bidder):
    def __init__(self):
        super().__init__()
        self.id = None
        self.L = None
        self.bid_prob_b = 0.1


    def set_bidder_id(self, bidder_id):
        self.id = bidder_id

    def does_bidder_bid(self, time):
        return rand() < self.bid_prob_b

    def get_bid(self, time, highest_bidder_id, second_highest_bid):
        if highest_bidder_id and highest_bidder_id == self.id:
            return None
        if not second_highest_bid:
            return None
        if not self.L:
            return None
        if self.L <= second_highest_bid:
            return None
        if not self.does_bidder_bid(time):
            return None
        c = self.get_c()
        return min(c * second_highest_bid, self.L)

    @staticmethod
    def get_c():
        return 1.5
