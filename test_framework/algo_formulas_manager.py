import math


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
    def get_twap_nav_child_qty(remaining_ord_qty: int, remaining_waves: int, ats: int, nav_percentage: float) -> int:
        first_reserve = max(5 * ats, math.ceil(remaining_ord_qty * (100 - nav_percentage)))
        reserve = max(first_reserve, AlgoFormulasManager.get_next_twap_slice(remaining_ord_qty, remaining_waves))
        return remaining_ord_qty - reserve

print(AlgoFormulasManager.calc_ticks_offset_plus(20,1,0.05))