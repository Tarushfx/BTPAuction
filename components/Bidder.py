class Bidder:
    def __init__(self):
        self.TOTAL_AUCTION_TIME = None
        self.last_bid = None

    def set_auction_time(self, time):
        self.TOTAL_AUCTION_TIME = time

    def set_last_bid(self, bid_data):
        pass

    def set_bidder_id(self, bidder_id):
        pass

    def does_bidder_bid(self, time):
        pass

    @staticmethod
    def get_c():
        pass

    def get_bid(self, time, highest_bidder_id, second_highest_bid):
        pass
