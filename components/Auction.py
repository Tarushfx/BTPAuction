from collections import deque

from numpy.random import normal, choice

from components.Auctioneer import Auctioneer
from components.Bidders.EarlyBidder import EarlyBidder
from components.Bidders.Shiller import Shiller
from components.Bidders.Sniper import Sniper


class Auction:
    bidder_types = {
        "early_bidders": EarlyBidder, "snipers": Sniper, "shillers": Shiller
    }

    def __init__(self, marketprice, early_bidders, snipers, shillers=0):
        self.MIN_PRICE = 1
        self.TOTAL_AUCTION_TIME = 500
        self.earlyBidders, self.snipers, self.shillers = early_bidders, snipers, shillers
        self.counts = [early_bidders, snipers, shillers]
        self.marketprice = marketprice
        self.total_bidders = sum(self.counts)
        self.bidders = []
        self.bidder_count = {i: j for i, j in zip(self.bidder_types, self.counts)}

        self.__limit_price_distribution = normal(loc=self.marketprice, scale=self.marketprice / 6,
                                                 size=self.total_bidders)
        self.__limit_price_distribution = [max(self.MIN_PRICE, price) for price in self.__limit_price_distribution]
        for bidder_type in self.bidder_types:
            self.bidders.extend(
                [{"bidder_type": bidder_type,
                  "bidder_class": self.bidder_types[bidder_type](),
                  "bidder_id": len(self.bidders) + _,
                  } for _ in range(self.bidder_count[bidder_type])]
            )
        for bidder, pl in zip(self.bidders, self.__limit_price_distribution):
            bidder["bidder_class"].set_priv_limit(pl)

        self.auctioneer = Auctioneer(self.marketprice, self.bidder_count, self.bidders)

        self.__scoreboard = deque()
        self.visible_scoreboard = deque()
        self.scoreboard_update_time = 0
        print((vars(self)))

    def start(self):

        for t in range(self.TOTAL_AUCTION_TIME):
            if t == self.scoreboard_update_time: self.update_scoreboard()
            for bidder in self.bidders:
                # make a decision to place a bid
                pass

    def get_current_second_highest(self):
        if not self.__scoreboard: return -1
        return self.visible_scoreboard[-1][1]

    def get_current_highest(self):
        if not self.__scoreboard: return -1
        return self.visible_scoreboard[0][1]

    def update_scoreboard(self):
        self.visible_scoreboard = self.__scoreboard

    def bid(self, bidder_id, bid_value, bid_time):
        bid_delay = choice([0, 1, 2])
        bid_data = [bidder_id, bid_value]
        if not self.__scoreboard:
            self.__scoreboard.append(bid_data)
            self.scoreboard_update_time = max(self.scoreboard_update_time, bid_time + bid_delay)
            return
        if len(self.__scoreboard) == 1:
            curr = self.get_current_second_highest()
            if curr >= bid_value:
                self.__scoreboard.append(bid_data)
            else:
                self.__scoreboard.appendleft(bid_data)
            self.scoreboard_update_time = max(self.scoreboard_update_time, bid_time + bid_delay)
            return
        # length==2
        curr_highest = self.get_current_highest()
        curr_second_highest = self.get_current_second_highest()
        if bid_value > curr_highest:
            self.__scoreboard.pop()
            self.__scoreboard.appendleft(bid_data)
        elif curr_highest >= bid_value > curr_second_highest:
            self.__scoreboard.pop()
            self.__scoreboard.append(bid_data)
        self.scoreboard_update_time = max(self.scoreboard_update_time, bid_time + bid_delay)


Auction(100, 1, 1)
