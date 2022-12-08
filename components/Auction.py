from bisect import insort
from collections import deque

from numpy.random import normal, choice

from components.Auctioneer import Auctioneer
from components.Bidders.EarlyBidder import EarlyBidder
from components.Bidders.Shiller import Shiller
from components.Bidders.Sniper import Sniper
import matplotlib.pyplot as plt
import seaborn as sns


class Auction:
    bidder_types = {
        "early_bidders": EarlyBidder, "snipers": Sniper, "shillers": Shiller
    }

    def __init__(self, market_price, early_bidders, snipers, shillers=0):
        self.MIN_PRICE = 1
        self.TOTAL_AUCTION_TIME = 500
        self.earlyBidders, self.snipers, self.shillers = early_bidders, snipers, shillers
        self.counts = [early_bidders, snipers, shillers]
        self.market_price = market_price
        self.total_bidders = sum(self.counts)
        self.bidders = []
        self.bidder_count = {i: j for i, j in zip(self.bidder_types, self.counts)}

        for bidder_type in self.bidder_types:
            self.bidders.extend(
                [{"bidder_type": bidder_type,
                  "bidder_class": self.bidder_types[bidder_type](),
                  "bidder_id": len(self.bidders) + _,
                  } for _ in range(self.bidder_count[bidder_type])]
            )
        for bidder_id, bidder in enumerate(self.bidders):
            bidder["bidder_class"].set_bidder_id(bidder_id)
            bidder["bidder_class"].set_auction_time(self.TOTAL_AUCTION_TIME)

        self.auctioneer = Auctioneer(self.market_price, self.bidder_count, self.bidders)

        self.__scoreboard = deque()
        self.visible_scoreboard = deque()
        self.scoreboard_update_time = 0

        self.__bid_history = []
        self.__track_highest_value = []
        # print((vars(self)))
        self.start()
        # self.plot_highest_values()

    def get_status(self, time):
        print(f"{time=}:{self.visible_scoreboard}")

    def start(self):
        for time in range(self.TOTAL_AUCTION_TIME):
            if time == self.scoreboard_update_time:
                self.update_scoreboard()
            self.track_private_scoreboard()
            highest_bidder_id, second_highest_bid = self.get_current_highest_bidder(), self.get_current_second_highest()
            for bidder in self.bidders:
                # make a decision to place a bid

                bid = bidder["bidder_class"].get_bid(time, highest_bidder_id, second_highest_bid)
                if not bid:
                    continue
                self.bid(bidder["bidder_id"], bid, time)
                bidder["bidder_class"].set_last_bid([time, bid])
                # self.get_status(time)

        return self.winner()

    def winner(self):
        res = self.__scoreboard
        if not res:
            return None
        winner_scorecard = {
            "bidder_type": res[0][3],
            "highest_bid": res[0][2],
            "second_highest_bid": res[-1][2]
        }
        return winner_scorecard

    def get_private_highest_bid(self):
        if not self.__scoreboard:
            return None
        return self.__scoreboard[0][2]

    def get_private_second_highest_bid(self):
        if not self.__scoreboard:
            return None
        if len(self.__scoreboard) == 1:
            return self.__scoreboard[0][2]
        return self.__scoreboard[1][2]

    def get_current_highest_bidder(self):
        if not self.visible_scoreboard:
            return None
        return self.visible_scoreboard[0][1]

    def get_current_highest(self):
        if not self.visible_scoreboard:
            return None
        return self.visible_scoreboard[0][2]

    def get_current_second_highest(self):
        if not self.visible_scoreboard: return None
        return self.visible_scoreboard[-1][2]

    def update_scoreboard(self):
        self.visible_scoreboard = self.__scoreboard

    def record_bid(self, bid_data):
        self.__bid_history.append(bid_data)

    def bid(self, bidder_id, bid_value, bid_time):
        bid_data = [bid_time, bidder_id, bid_value, self.bidders[bidder_id]["bidder_type"]]
        self.record_bid(bid_data)
        bid_delay = choice([0, 1, 2])
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

    def plot_highest_values(self):
        plt.plot(self.__track_highest_value)
        plt.ylim(0, 2000)
        plt.show()
        plt.savefig('/home/kittler/Desktop/BTPAuction/results/bid_progression.png')

    def track_private_scoreboard(self):
        self.__track_highest_value.append(self.get_private_second_highest_bid())


if __name__ == "__main__":
    Auction(1000, 7, 3)
