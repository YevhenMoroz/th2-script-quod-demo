import math
from datetime import datetime, timedelta
from math import ceil
from functools import wraps


class AlgoFormulasManager:
    # region offset calculation
    @staticmethod
    def calc_ticks_offset_minus(price: float, offset_qty: int, tick: float) -> float:
        result = price - tick * offset_qty
        return int(result) if result.is_integer() else result

    @staticmethod
    def calc_ticks_offset_plus(price: float, offset: int, tick: float) -> float:
        result = price + tick * offset
        return int(result) if result.is_integer() else result

    @staticmethod
    def calc_bps_offset_minus(price: float, offset_qty: int) -> float:
        result = price - price / 10000 * offset_qty
        return int(result) if result.is_integer() else result

    @staticmethod
    def calc_bps_offset_plus(price: float, offset_qty: int) -> float:
        result = price + price / 10000 * offset_qty
        return int(result) if result.is_integer() else result
    # endregion

    @staticmethod
    def get_next_twap_slice(remaining_ord_qty: int, remaining_waves: int) -> int:
        return math.floor(remaining_ord_qty / remaining_waves)

    @staticmethod
    def get_all_twap_slices(remaining_ord_qty: int, remaining_waves: int) -> list:
        used_qty = 0
        twap_slices = []
        for i in range(remaining_waves):
            temp = AlgoFormulasManager.get_next_twap_slice(remaining_ord_qty - used_qty, remaining_waves - i)
            used_qty += temp
            twap_slices.append(used_qty)
        return twap_slices

    @staticmethod
    def get_pov_child_qty(per_vol: float, market_vol: int, ord_qty: int) -> int:
        if (per_vol > 0 and per_vol < 1):
            return min(math.ceil((market_vol * per_vol) / (1 - per_vol)), ord_qty)
        else:
            return min(math.ceil((market_vol * per_vol) / (100 - per_vol)), ord_qty)

    @staticmethod
    def get_twap_nav_child_qty(remaining_ord_qty: int, remaining_waves: int, ats: int, nav_percentage: float = 100) -> int:
        first_reserve = max(5 * ats, math.ceil(remaining_ord_qty * (100 - nav_percentage)))
        reserve = max(first_reserve, AlgoFormulasManager.get_next_twap_slice(remaining_ord_qty, remaining_waves))
        return remaining_ord_qty - reserve

    @staticmethod
    def get_nav_reserve(remaining_ord_qty: int, remaining_waves: int, ats: int, nav_percentage: float = 100) -> int:
        first_reserve = max(5 * ats, math.ceil(remaining_ord_qty * (100 - nav_percentage)))
        reserve = max(first_reserve, AlgoFormulasManager.get_next_twap_slice(remaining_ord_qty, remaining_waves))
        return reserve

    @staticmethod
    def get_child_qty_on_venue_weights(parent_qty: int, minqty: int = None, *venue_weights: int) -> list:
        sum_of_weight = 0
        count_of_venue = 0
        qty_list = []

        for i in venue_weights:
            sum_of_weight += i
            count_of_venue += 1

        if minqty is None:                                                  # for tests without minQty
            one_weight = parent_qty / sum_of_weight
            j = 0
            while j < len(venue_weights):
                qty_list.append(int(one_weight * venue_weights[j]))
                j += 1
            sum_of_qty = 0
            for k in qty_list:
                sum_of_qty += k
            different = parent_qty - sum_of_qty                             # if parent qty not completely divided by venue weights
            if different > 0:
                qty_list[0] += different
        else:                                                               # for tests with minQty
            qty_for_distribution = parent_qty - minqty * count_of_venue
            if parent_qty - minqty < minqty:                                # for tests when parentQty - minQty < minQty (only 1 child)
                one_weight = parent_qty
                qty_list.append(one_weight)
            elif qty_for_distribution <= 0:                                 # for tests when parentQty - minty * countOfVenue <= 0 (qty of each child = minQty)
                count_of_venue = parent_qty / minqty
                one_weight = minqty
                j = 0
                while j < count_of_venue:
                    qty_list.append(ceil(one_weight))
                    j += 1
            else:                                                          # for everyone else
                one_weight = qty_for_distribution / sum_of_weight
                j = 0
                while j < len(venue_weights):
                    qty_list.append(int(one_weight * venue_weights[j] + minqty))
                    j += 1
                sum_of_qty = 0
                for k in qty_list:
                    sum_of_qty += k
                different = parent_qty - sum_of_qty
                if different > 0:
                    qty_list[0] += different
        return qty_list

    @staticmethod
    # Calculating childs qty for Multilisted algo (PostMode=Spraying)
    def get_child_qty_for_spraying(parent_qty: int, *venue_weights: int) -> list:
        sum_of_weight = 0
        count_of_venue = 0
        qty_list = []

        for i in venue_weights:
            sum_of_weight += i
            count_of_venue += 1

        one_weight = parent_qty / sum_of_weight
        j = 0
        while j < len(venue_weights):
            qty_list.append(int(one_weight * venue_weights[j]))
            j += 1
        sum_of_qty = 0
        for k in qty_list:
            sum_of_qty += k
        different = parent_qty - sum_of_qty                                            # if parent qty not completely divided by venue weights
        if different > 0:
            qty_list[0] += different
        return qty_list

    @staticmethod
    def create_string_for_strategy_weight(venues: dict) -> str:
        final_string = str()
        list_len = 0
        for venue in venues:
            final_string += f"{venue}={venues[venue]}"
            list_len += 1
            if list_len < len(venues):
                final_string += "/"
        return final_string

    @staticmethod
    def create_string_for_strategy_venues(*venue: str) -> str:
        final_string = str()
        for idx, v in enumerate(venue):
            final_string += v
            if len(venue) - 1 != idx:
                final_string += "/"
        return final_string

    @staticmethod
    def make_expire_date_next_sunday(day: int) -> int:
        days = [0, 1, 2, 3, 4, 5, 6]
        shift = 6
        res_shift = 0
        for i in days:
            if day == i:
                res_shift = shift
            shift -= 1
        return res_shift

    @staticmethod
    # Need to run test and check ExpireDate if it is not weekend, but weekends between now and ExpireDate. For delta <=2
    def calculate_shift_for_expire_date_if_it_is_on_weekend(expire_date: datetime, delta: int) -> int:
        day = datetime.weekday(expire_date)
        shift = delta
        if day == 5:
            shift += 2
        elif day == 6:
            shift += 1
        else:
            shift = delta
        return shift


    @staticmethod
    def get_pov_child_qty_on_ltq(percentage_vol: float, last_traded_volume: int, ord_qty: int) -> int:
        if (percentage_vol > 0 and percentage_vol < 1):
            return min(math.ceil((last_traded_volume * percentage_vol) / (1 - percentage_vol)), ord_qty)
        # elif (percentage_vol == 100 or percentage_vol == 1):
        #     return min(math.ceil(last_traded_volume * percentage_vol), ord_qty)
        else:
            return min(math.ceil((last_traded_volume * percentage_vol) / (100 - percentage_vol)), ord_qty)

    @staticmethod
    def get_lis_amount_for_order(qty: int, price: float) -> float:
        return qty * price

    @staticmethod
    def convert_pre_trade_lis_amount_for_another_currency(pre_trade_lis_amount: float, rate: float) -> float:
        return pre_trade_lis_amount * rate

    @staticmethod
    def get_pov_child_qty_for_worse_price_behavior(min_part: float, max_part: float, total_traded_volume: int, ord_qty: int, executed_qty: int = 0) -> int:
        return min(math.ceil(((total_traded_volume * ((min_part + max_part) / 2)) / 100) - executed_qty), ord_qty)

    @staticmethod
    def get_pov_child_qty_for_price_improvement(max_part: float, total_traded_volume: int, ord_qty: int, executed_qty: int = 0) -> int:
        return min(math.ceil((total_traded_volume * (max_part / 100)) - executed_qty), ord_qty)

