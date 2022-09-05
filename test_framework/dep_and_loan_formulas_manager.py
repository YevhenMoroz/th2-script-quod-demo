from datetime import datetime

from custom.tenor_settlement_date import spo


class DepAndLoanManager:

    @staticmethod
    def day_difference(near_date: str, far_date):
        """
        Calculates dates difference between given dates and Spot
        and return it
        """
        spot = datetime.strptime(spo(), '%Y%m%d')
        near_date = datetime.strptime(near_date, '%Y%m%d')
        far_date = datetime.strptime(far_date, '%Y%m%d')
        near_diff = (near_date - spot).days
        far_diff = (far_date - spot).days
        day_dif = far_diff - near_diff
        return [near_diff, far_diff, day_dif]

    @staticmethod
    def calc_dep_and_loan_default(near_bid: float, near_offer: float, far_bid: float, far_offer: float,
                                  near_date: str, far_date: str):
        day_diff = DepAndLoanManager.day_difference(near_date, far_date)
        near_mid_price = (near_bid + near_offer) / 2
        far_mid_price = (far_bid + far_offer) / 2
        near_spread = near_offer - near_bid
        far_spread = far_offer - far_bid
        adj_near_leg_mid = 1 + (near_mid_price * day_diff[0] / 360)
        adj_far_leg_mid = 1 + (far_mid_price * day_diff[1] / 360)
        request_mid_rate = ((adj_far_leg_mid / adj_near_leg_mid) - 1) / (day_diff[2] / 360)
        bid = round(request_mid_rate - (far_spread / 2), 11)
        ask = round(request_mid_rate + (far_spread / 2), 11)
        return [bid, ask]

    @staticmethod
    def calc_dep_and_loan_before_spot(near_bid: float, near_offer: float, far_bid: float, far_offer: float,
                                      near_date: str, far_date: str):
        """
        Calculate prises for deposit and loans when near date < Spot using following formula
        """
        day_diff = DepAndLoanManager.day_difference(near_date, far_date)
        bid_price = round((near_bid * abs(day_diff[0]) + far_bid * (day_diff[1])) / day_diff[2], 11)
        offer_price = round((near_offer * abs(day_diff[0]) + far_offer * day_diff[1]) / day_diff[2], 11)
        return [bid_price, offer_price]
