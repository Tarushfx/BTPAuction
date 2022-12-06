from components.Bidder import Bidder


class Sniper(Bidder):
    def __init__(self):
        self.L = None

    def set_priv_limit(self, pl):
        self.L = pl

    def get_bid(self, scoreboard):
        pass
