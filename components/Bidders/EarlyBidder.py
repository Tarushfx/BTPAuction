from components.Bidder import Bidder


class EarlyBidder(Bidder):
    def __init__(self):
        self.L = None
        self.v = None

    def set_priv_limit(self,pl):
        self.L=pl

    def get_bid(self, scoreboard):
        pass
