from components.Bidder import Bidder


class Shiller(Bidder):
    def __init__(self):
        self.L = None

    def set_priv_limit(self, pl):
        self.L = pl

    def set_bidder_id(self, bidder_id):
        self.id = bidder_id

    def get_bid(self, time, highest_bidder_id, second_highest_bid):
        pass
