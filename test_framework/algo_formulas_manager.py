import math
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
        return math.ceil(remaining_ord_qty / remaining_waves)

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
        return max(math.ceil((market_vol * per_vol) / (100 - per_vol)), ord_qty)

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
    def prohibit_float_arguments(func):
        @wraps(func)
        def wrapper(*args):
            for val in args:
                if type(val) == float:
                    raise ValueError('Float arguments are prohibited')
                if type(val) == str:
                    raise ValueError('String arguments are prohibited')
                if val < 0:
                    raise ValueError('Negative arguments are prohibited')
            return func(*args)
        return wrapper

    # @staticmethod
    # # @prohibit_float_arguments
    # def get_child_qty_on_venue_weights(parent_qty: int, minqty: int = None, *venue_weights: list) -> list:
    #     sum_of_weight = 0
    #     count_of_venue = 0
    #     qty_list = []
    #
    #     for i in venue_weights:
    #         sum_of_weight += i
    #         count_of_venue += 1
    #
    #     if minqty is None:
    #         one_weight = parent_qty / sum_of_weight
    #         j = 0
    #         while j < len(venue_weights):
    #             qty_list.append(one_weight * venue_weights[j])
    #             j += 1
    #     else:
    #         qty_for_distribution = parent_qty - minqty * count_of_venue
    #         one_weight = qty_for_distribution / sum_of_weight
    #         j = 0
    #         while j < len(venue_weights):
    #             qty_list.append(one_weight * venue_weights[j] + minqty)
    #             j += 1
    #
    #     return qty_list

    @staticmethod
    def get_child_qty_on_venue_weights(parent_qty: int, *venue_weights: list) -> list:
        sum_of_weight = 0
        for i in venue_weights:
            sum_of_weight += i

        one_weight = parent_qty / sum_of_weight

        qty_list = []
        for k in venue_weights:
            qty_list.append(int(one_weight * k))

        return qty_list

    @staticmethod
    def get_child_qty_on_venue_weights_with_min_qty(parent_qty, min_qty, *venue_weights):
        sum_of_weight = 0
        count_of_venue = 0
        for i in venue_weights:
            sum_of_weight += i
            count_of_venue += 1

        qty_for_distribution = parent_qty - min_qty * count_of_venue

        one_weight = qty_for_distribution / sum_of_weight

        qty_list = []
        for k in venue_weights:
            qty_list.append(int(one_weight * k + min_qty))

        return qty_list






