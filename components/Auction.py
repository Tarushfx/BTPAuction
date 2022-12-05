from components.Auctioneer import Auctioneer
from components.Bidders.EarlyBidder import EarlyBidder
from components.Bidders.Shiller import Shiller
from components.Bidders.Sniper import Sniper


class Auction:
    bidder_types = {
        "early_bidders": EarlyBidder, "snipers": Sniper, "shillers": Shiller
    }

    def __init__(self, marketprice, early_bidders, snipers, shillers=0):
        self.earlyBidders, self.snipers, self.shillers = early_bidders, snipers, shillers
        self.total_bidders = sum([early_bidders, snipers, shillers])
        self.bidders = []
        for bidder_type in self.bidder_types:
            self.bidders.append(
                self.bidder_types[bidder_type]()
            )
        self.marketprice = marketprice
        self.auctioneer = Auctioneer(marketprice)



Auction(1)
