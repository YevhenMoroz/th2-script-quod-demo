import datetime
import math
from copy import deepcopy
from datetime import time, date, timezone, timedelta
from datetime import datetime as dt
from math import ceil
from decimal import Decimal

from test_framework.data_sets.constants import TradingPhases

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
    def calc_step_for_scaling(pp2_price: float, pp1_price: float, number_of_levels: int) -> float:
        result = (pp2_price - pp1_price) / number_of_levels
        return int(result) if result.is_integer() else round(result, 2)

    @staticmethod
    def get_next_twap_slice(remaining_ord_qty: int, remaining_waves: int, round_lot: int = 1) -> int:
        return math.floor(remaining_ord_qty / remaining_waves/round_lot) * round_lot

    @staticmethod
    def get_all_twap_slices(remaining_ord_qty: int, remaining_waves: int) -> list:
        twap_slices = []
        for i in range(remaining_waves):
            temp = AlgoFormulasManager.get_next_twap_slice(remaining_ord_qty, remaining_waves - i)
            twap_slices.append(temp)
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
    def calculate_shift_for_settl_date_if_it_is_on_weekend(expire_date: dt, delta: int) -> int:
        day = dt.weekday(expire_date)
        shift = delta
        if day == 5:
            shift += 2
        elif day == 6:
            shift += 1
        else:
            shift = delta
        return shift

    @staticmethod
    def make_expire_date_friday_if_it_is_on_weekend(expire_date: dt) -> int:
        day = dt.weekday(expire_date)
        shift = 0
        if day == 5:
            shift += 1
        elif day == 6:
            shift += 2
        else:
            shift = 0
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

    @staticmethod
    def calculate_price_with_currency_conversion(price: float, rate: float, decimal_places: int, offset: float = 0) -> Decimal:
        number = Decimal(math.floor(price / rate * 10 ** decimal_places) / 10 ** decimal_places - offset)
        number = number.quantize(Decimal("1.000"))
        return number

    # @staticmethod
    # def change_datetime_from_epoch_to_normal(datetime_epoch) -> datetime:
    #     return dt.fromtimestamp(int(datetime_epoch)/1000).replace(tzinfo=timezone.utc)
    #
    # @staticmethod
    # def change_time_from_normal_to_epoch(time: datetime) -> int:
    #     return int(time.replace(tzinfo=timezone.utc).timestamp()) * 1000
    #
    # @staticmethod
    # def change_datetime_from_normal_to_epoch(date: dt) -> int:
    #     return int(date.replace(tzinfo=timezone.utc).timestamp()) * 1000
    #
    # @staticmethod
    # def change_time_from_normal_to_epoch_without_milisec(time: datetime) -> int:
    #     return int(time.replace(tzinfo=timezone.utc).timestamp())

    @staticmethod
    def change_datetime_local_to_UTC(local_date: dt):
        copy_local_date = deepcopy(local_date)
        return copy_local_date.replace(tzinfo=datetime.timezone.utc)

    @staticmethod
    def change_datetime_UTC_to_local(utc_dt: dt):
        copy_utc_dt = deepcopy(utc_dt)
        return copy_utc_dt.replace(tzinfo=datetime.timezone.utc).astimezone(tz=None)

    @staticmethod
    def change_datetime_from_epoch_to_normal(datetime_epoch) -> dt:
        return datetime.datetime.fromtimestamp(datetime_epoch).astimezone(tz=timezone.utc)

    @staticmethod
    def change_datetime_from_epoch_to_normal_with_milisec(datetime_epoch) -> dt:
        return datetime.datetime.fromtimestamp(int(datetime_epoch)/1000)


    @staticmethod
    def change_datetime_from_normal_to_epoch(datetime: dt) -> int:
        return int(AlgoFormulasManager.change_datetime_local_to_UTC(datetime).timestamp())

    @staticmethod
    def change_datetime_from_normal_to_epoch_with_milisecs(datetime: dt) -> int:
        return int(datetime.timestamp()) * 1000

    @staticmethod
    def get_timestamps_for_previous_phase(phase: TradingPhases):
        tm = dt.now()
        if phase == TradingPhases.PreOpen:
            pop_start = tm - datetime.timedelta(seconds=tm.second, microseconds=tm.microsecond) + datetime.timedelta(minutes=2)
            opn_start = pop_start + timedelta(minutes=4)
            pcl_start = opn_start + timedelta(minutes=5)
            pcl_end = pcl_start + timedelta(minutes=5)
            clo_start = pcl_end + timedelta(minutes=5)
        elif phase == TradingPhases.PreClosed:
            pcl_start = tm - datetime.timedelta(seconds=tm.second, microseconds=tm.microsecond) + datetime.timedelta(minutes=2)
            opn_start = pcl_start - timedelta(minutes=5)
            pop_start = opn_start - timedelta(minutes=5)
            pcl_end = pcl_start + timedelta(minutes=5)
            clo_start = pcl_end + timedelta(minutes=5)
        return [
            {
                "beginTime": pop_start,
                "endTime": opn_start,
                "submitAllowed": "True",
                "tradingPhase": "POP",
                "standardTradingPhase": "PRE",
            },
            {
                "beginTime": opn_start,
                "endTime": pcl_start,
                "submitAllowed": "True",
                "tradingPhase": "OPN",
                "standardTradingPhase": "OPN",
            },
            {
                "beginTime": pcl_start,
                "endTime": pcl_end,
                "submitAllowed": "True",
                "tradingPhase": "PCL",
                "standardTradingPhase": "PCL",
            },
            {
                "beginTime": pcl_end,
                "endTime": clo_start,
                "submitAllowed": "True",
                "tradingPhase": "TAL",
                "standardTradingPhase": "TAL",
            },
            {
                "beginTime": clo_start,
                "endTime": dt(year=tm.year, month=tm.month, day=tm.day, hour=23, minute=0, second=0, microsecond=0),
                "submitAllowed": "True",
                "tradingPhase": "CLO",
                "standardTradingPhase": "CLO",
            }
        ]

    @staticmethod
    def get_timestamps_for_current_phase(phase: TradingPhases, dateformat="full"):
        tm = dt.now()
        if phase == TradingPhases.PreOpen:
            pop_start = tm - datetime.timedelta(seconds=tm.second, microseconds=tm.microsecond)
            opn_start = pop_start + timedelta(minutes=4)
            pcl_start = opn_start + timedelta(minutes=5)
            pcl_end = pcl_start + timedelta(minutes=5)
            clo_start = pcl_end + timedelta(minutes=5)
            exa_start = dt(year=tm.year, month=tm.month, day=tm.day, hour=10, minute=10, second=0, microsecond=0).replace(tzinfo=timezone.utc)
            exa_end = dt(year=tm.year, month=tm.month, day=tm.day, hour=10, minute=15, second=0, microsecond=0).replace(tzinfo=timezone.utc)
        elif phase == TradingPhases.PreClosed:
            pcl_start = tm - datetime.timedelta(seconds=tm.second, microseconds=tm.microsecond)
            pcl_end = pcl_start + timedelta(minutes=4)
            opn_start = pcl_start - timedelta(minutes=5)
            pop_start = opn_start - timedelta(minutes=5)
            clo_start = pcl_end + timedelta(minutes=5)
            exa_start = dt(year=tm.year, month=tm.month, day=tm.day, hour=10, minute=10, second=0, microsecond=0).replace(tzinfo=timezone.utc)
            exa_end = dt(year=tm.year, month=tm.month, day=tm.day, hour=10, minute=15, second=0, microsecond=0).replace(tzinfo=timezone.utc)
        elif phase == TradingPhases.Open:
            opn_start = tm - datetime.timedelta(seconds=tm.second, microseconds=tm.microsecond)
            pcl_start = opn_start + timedelta(minutes=4)
            pcl_end = pcl_start + timedelta(minutes=5)
            pop_start = opn_start - timedelta(minutes=5)
            clo_start = pcl_end + timedelta(minutes=5)
            exa_start = dt(year=tm.year, month=tm.month, day=tm.day, hour=10, minute=10, second=0, microsecond=0).replace(tzinfo=timezone.utc)
            exa_end = dt(year=tm.year, month=tm.month, day=tm.day, hour=10, minute=15, second=0, microsecond=0).replace(tzinfo=timezone.utc)
        elif phase == TradingPhases.AtLast:
            pcl_end = tm - datetime.timedelta(seconds=tm.second, microseconds=tm.microsecond)
            clo_start = pcl_end + timedelta(minutes=4)
            pcl_start = pcl_end - timedelta(minutes=5)
            opn_start = pcl_start - timedelta(minutes=5)
            pop_start = opn_start - timedelta(minutes=5)
            exa_start = dt(year=tm.year, month=tm.month, day=tm.day, hour=10, minute=10, second=0, microsecond=0).replace(tzinfo=timezone.utc)
            exa_end = dt(year=tm.year, month=tm.month, day=tm.day, hour=10, minute=15, second=0, microsecond=0).replace(tzinfo=timezone.utc)
        elif phase == TradingPhases.Closed:
            clo_start = tm - datetime.timedelta(seconds=tm.second, microseconds=tm.microsecond)
            pcl_end = clo_start - timedelta(minutes=5)
            pcl_start = pcl_end - timedelta(minutes=5)
            opn_start = pcl_start - timedelta(minutes=5)
            pop_start = opn_start - timedelta(minutes=5)
            exa_start = dt(year=tm.year, month=tm.month, day=tm.day, hour=10, minute=10, second=0, microsecond=0).replace(tzinfo=timezone.utc)
            exa_end = dt(year=tm.year, month=tm.month, day=tm.day, hour=10, minute=15, second=0, microsecond=0).replace(tzinfo=timezone.utc)
        elif phase == TradingPhases.Expiry:
            opn_start = tm - datetime.timedelta(minutes=10, seconds=tm.second, microseconds=tm.microsecond)
            pcl_start = opn_start + timedelta(minutes=20)
            pcl_end = pcl_start + timedelta(minutes=5)
            pop_start = opn_start - timedelta(minutes=5)
            clo_start = pcl_end + timedelta(minutes=5)
            exa_start = tm - datetime.timedelta(seconds=tm.second, microseconds=tm.microsecond)
            exa_end = exa_start + timedelta(minutes=5)

        if dateformat == "full":
            return [
                {
                    "beginTime": pop_start,
                    "endTime": opn_start,
                    "submitAllowed": "True",
                    "tradingPhase": "POP",
                    "standardTradingPhase": "PRE",
                },
                {
                    "beginTime": opn_start,
                    "endTime": pcl_start,
                    "submitAllowed": "True",
                    "tradingPhase": "OPN",
                    "standardTradingPhase": "OPN",
                },
                {
                    "beginTime": pcl_start,
                    "endTime": pcl_end,
                    "submitAllowed": "True",
                    "tradingPhase": "PCL",
                    "standardTradingPhase": "PCL",
                },
                {
                    "beginTime": pcl_end,
                    "endTime": clo_start,
                    "submitAllowed": "True",
                    "tradingPhase": "TAL",
                    "standardTradingPhase": "TAL",
                },
                {
                    "beginTime": clo_start,
                    "endTime": dt(year=tm.year, month=tm.month, day=tm.day, hour=23, minute=0, second=0, microsecond=0),
                    "submitAllowed": "True",
                    "tradingPhase": "CLO",
                    "standardTradingPhase": "CLO",
                },
                {
                    "beginTime": exa_start,
                    "endTime": exa_end,
                    "submitAllowed": "True",
                    "tradingPhase": "EXA",
                    "standardTradingPhase": "EXA",
                    "expiryCycle": "EVM",
                }]
        else:
            return [
                {
                    "phaseBeginTime": pop_start.strftime("%H:%M:%S"),
                    "phaseEndTime": opn_start.strftime("%H:%M:%S"),
                    "tradingPhase": "POP",
                    "standardTradingPhase": "PRE",
                },
                {
                    "phaseBeginTime": opn_start.strftime("%H:%M:%S"),
                    "phaseEndTime": pcl_start.strftime("%H:%M:%S"),
                    "tradingPhase": "OPN",
                    "standardTradingPhase": "OPN",
                },
                {
                    "phaseBeginTime": pcl_start.strftime("%H:%M:%S"),
                    "phaseEndTime": pcl_end.strftime("%H:%M:%S"),
                    "tradingPhase": "PCL",
                    "standardTradingPhase": "PCL",
                },
                {
                    "phaseBeginTime": pcl_end.strftime("%H:%M:%S"),
                    "phaseEndTime": clo_start.strftime("%H:%M:%S"),
                    "tradingPhase": "AUC",
                    "standardTradingPhase": "TAL",
                },
                {
                    "phaseBeginTime": clo_start.strftime("%H:%M:%S"),
                    "phaseEndTime": datetime.time(hour=23, minute=0, second=0),
                    "tradingPhase": "CLO",
                    "standardTradingPhase": "CLO",
                },
                {
                    "phaseBeginTime": exa_start.strftime("%H:%M:%S"),
                    "phaseEndTime": exa_end.strftime("%H:%M:%S"),
                    "tradingPhase": "HAL",
                    "standardTradingPhase": "EXA",
                    "expiryCycle": "EVM",
                }
        ]

    @staticmethod
    def get_default_timestamp_for_trading_phase(dateformat="full"):
        tm = dt.now()
        if dateformat == "full":
            return [
                {
                    "beginTime": dt(year=tm.year, month=tm.month, day=tm.day, hour=6, minute=50, second=0, microsecond=0).replace(tzinfo=timezone.utc),
                    "endTime": dt(year=tm.year, month=tm.month, day=tm.day, hour=7, minute=0, second=0, microsecond=0).replace(tzinfo=timezone.utc),
                    "submitAllowed": "True",
                    "tradingPhase": "POP",
                    "standardTradingPhase": "PRE",
                },
                {
                    "beginTime": dt(year=tm.year, month=tm.month, day=tm.day, hour=7, minute=0, second=0, microsecond=0).replace(tzinfo=timezone.utc),
                    "endTime": dt(year=tm.year, month=tm.month, day=tm.day, hour=19, minute=0, second=0, microsecond=0).replace(tzinfo=timezone.utc),
                    "submitAllowed": "True",
                    "tradingPhase": "OPN",
                    "standardTradingPhase": "OPN",
                },
                {
                    "beginTime": dt(year=tm.year, month=tm.month, day=tm.day, hour=19, minute=0, second=0, microsecond=0).replace(tzinfo=timezone.utc),
                    "endTime": dt(year=tm.year, month=tm.month, day=tm.day, hour=19, minute=10, second=0, microsecond=0).replace(tzinfo=timezone.utc),
                    "submitAllowed": "True",
                    "tradingPhase": "PCL",
                    "standardTradingPhase": "PCL",
                },
                {
                    "beginTime": dt(year=tm.year, month=tm.month, day=tm.day, hour=19, minute=10, second=0, microsecond=0).replace(tzinfo=timezone.utc),
                    "endTime": dt(year=tm.year, month=tm.month, day=tm.day, hour=19, minute=20, second=0, microsecond=0).replace(tzinfo=timezone.utc),
                    "submitAllowed": "True",
                    "tradingPhase": "TAL",
                    "standardTradingPhase": "TAL",
                },
                {
                    "beginTime": dt(year=tm.year, month=tm.month, day=tm.day, hour=19, minute=20, second=0, microsecond=0).replace(tzinfo=timezone.utc),
                    "endTime": dt(year=tm.year, month=tm.month, day=tm.day, hour=23, minute=59, second=0, microsecond=0).replace(tzinfo=timezone.utc),
                    "submitAllowed": "True",
                    "tradingPhase": "CLO",
                    "standardTradingPhase": "CLO",
                },
                {
                    "beginTime": dt(year=tm.year, month=tm.month, day=tm.day, hour=10, minute=10, second=0, microsecond=0).replace(tzinfo=timezone.utc),
                    "endTime": dt(year=tm.year, month=tm.month, day=tm.day, hour=10, minute=15, second=0, microsecond=0).replace(tzinfo=timezone.utc),
                    "submitAllowed": "True",
                    "tradingPhase": "EXA",
                    "standardTradingPhase": "EXA",
                    "expiryCycle": "EVM",
                }
            ]
        else:
            tm = datetime.time
            return [
                {
                    "phaseBeginTime": tm(hour=6, minute=50, second=0).replace(tzinfo=timezone.utc),
                    "phaseEndTime": tm(hour=7, minute=0, second=0).replace(tzinfo=timezone.utc),
                    "tradingPhase": "POP",
                    "standardTradingPhase": "PRE",
                },
                {
                    "phaseBeginTime": tm(hour=7, minute=0, second=0).replace(tzinfo=timezone.utc),
                    "phaseEndTime": tm(hour=19, minute=0, second=0).replace(tzinfo=timezone.utc),
                    "tradingPhase": "OPN",
                    "standardTradingPhase": "OPN",
                },
                {
                    "phaseBeginTime": tm(hour=19, minute=0, second=0).replace(tzinfo=timezone.utc),
                    "phaseEndTime": tm(hour=19, minute=10, second=0).replace(tzinfo=timezone.utc),
                    "tradingPhase": "PCL",
                    "standardTradingPhase": "PCL",
                },
                {
                    "phaseBeginTime": tm(hour=19, minute=10, second=0).replace(tzinfo=timezone.utc),
                    "phaseEndTime": tm(hour=19, minute=20, second=0).replace(tzinfo=timezone.utc),
                    "tradingPhase": "AUC",
                    "standardTradingPhase": "TAL",
                },
                {
                    "phaseBeginTime": tm(hour=19, minute=20, second=0).replace(tzinfo=timezone.utc),
                    "phaseEndTime": tm(hour=23, minute=59, second=0).replace(tzinfo=timezone.utc),
                    "tradingPhase": "CLO",
                    "standardTradingPhase": "CLO",
                },
                {
                    "phaseBeginTime": tm(hour=10, minute=10, second=0).replace(tzinfo=timezone.utc),
                    "phaseEndTime": tm(hour=10, minute=15, second=0).replace(tzinfo=timezone.utc),
                    "tradingPhase": "HAL",
                    "standardTradingPhase": "EXA",
                    "expiryCycle": "EVM",
                }
            ]

    @staticmethod
    def get_timestamps_for_next_phase(phase: TradingPhases, dateformat="full"):
        tm = dt.now()
        if phase == TradingPhases.PreOpen:
            pop_start = tm + datetime.timedelta(minutes=3) - datetime.timedelta(seconds=tm.second, microseconds=tm.microsecond)
            opn_start = pop_start + timedelta(minutes=4)
            pcl_start = opn_start + timedelta(minutes=5)
            pcl_end = pcl_start + timedelta(minutes=5)
            clo_start = pcl_end + timedelta(minutes=5)
        elif phase == TradingPhases.PreClosed:
            pcl_start = tm + datetime.timedelta(minutes=3) - datetime.timedelta(seconds=tm.second, microseconds=tm.microsecond)
            pcl_end = pcl_start + timedelta(minutes=4)
            opn_start = pcl_start - timedelta(minutes=5)
            pop_start = opn_start - timedelta(minutes=5)
            clo_start = pcl_end + timedelta(minutes=5)
        elif phase == TradingPhases.Open:
            opn_start = tm + datetime.timedelta(minutes=3) - datetime.timedelta(seconds=tm.second, microseconds=tm.microsecond)
            pcl_start = opn_start + timedelta(minutes=4)
            pcl_end = pcl_start + timedelta(minutes=5)
            pop_start = opn_start - timedelta(minutes=5)
            clo_start = pcl_end + timedelta(minutes=5)
        elif phase == TradingPhases.Expiry:
            opn_start = tm - datetime.timedelta(minutes=10, seconds=tm.second, microseconds=tm.microsecond)
            pcl_start = opn_start + timedelta(minutes=20)
            pcl_end = pcl_start + timedelta(minutes=5)
            pop_start = opn_start - timedelta(minutes=5)
            clo_start = pcl_end + timedelta(minutes=5)
            exa_start = tm - datetime.timedelta(seconds=tm.second, microseconds=tm.microsecond) + timedelta(minutes=2)
            exa_end = exa_start + timedelta(minutes=5)

        if dateformat == "full":
            return [
                {
                    "beginTime": pop_start,
                    "endTime": opn_start,
                    "submitAllowed": "True",
                    "tradingPhase": "POP",
                    "standardTradingPhase": "PRE",
                },
                {
                    "beginTime": opn_start,
                    "endTime": pcl_start,
                    "submitAllowed": "True",
                    "tradingPhase": "OPN",
                    "standardTradingPhase": "OPN",
                },
                {
                    "beginTime": pcl_start,
                    "endTime": pcl_end,
                    "submitAllowed": "True",
                    "tradingPhase": "PCL",
                    "standardTradingPhase": "PCL",
                },
                {
                    "beginTime": pcl_end,
                    "endTime": clo_start,
                    "submitAllowed": "True",
                    "tradingPhase": "TAL",
                    "standardTradingPhase": "TAL",
                },
                {
                    "beginTime": clo_start,
                    "endTime": dt(year=tm.year, month=tm.month, day=tm.day, hour=23, minute=0, second=0, microsecond=0),
                    "submitAllowed": "True",
                    "tradingPhase": "CLO",
                    "standardTradingPhase": "CLO",
                },
                {
                    "beginTime": exa_start,
                    "endTime": exa_end,
                    "submitAllowed": "True",
                    "tradingPhase": "EXA",
                    "standardTradingPhase": "EXA",
                    "expiryCycle": "EVM",
                }
            ]
        else:
            return [
                {
                    "phaseBeginTime": pop_start.strftime("%H:%M:%S"),
                    "phaseEndTime": opn_start.strftime("%H:%M:%S"),
                    "tradingPhase": "POP",
                    "standardTradingPhase": "PRE",
                },
                {
                    "phaseBeginTime": opn_start.strftime("%H:%M:%S"),
                    "phaseEndTime": pcl_start.strftime("%H:%M:%S"),
                    "tradingPhase": "OPN",
                    "standardTradingPhase": "OPN",
                },
                {
                    "phaseBeginTime": pcl_start.strftime("%H:%M:%S"),
                    "phaseEndTime": pcl_end.strftime("%H:%M:%S"),
                    "tradingPhase": "PCL",
                    "standardTradingPhase": "PCL",
                },
                {
                    "phaseBeginTime": pcl_end.strftime("%H:%M:%S"),
                    "phaseEndTime": clo_start.strftime("%H:%M:%S"),
                    "tradingPhase": "AUC",
                    "standardTradingPhase": "TAL",
                },
                {
                    "phaseBeginTime": clo_start.strftime("%H:%M:%S"),
                    "phaseEndTime": datetime.time(hour=23, minute=0, second=0),
                    "tradingPhase": "CLO",
                    "standardTradingPhase": "CLO",
                },
                {
                    "phaseBeginTime": exa_start.strftime("%H:%M:%S"),
                    "phaseEndTime": exa_end.strftime("%H:%M:%S"),
                    "tradingPhase": "HAL",
                    "standardTradingPhase": "EXA",
                    "expiryCycle": "EVM",
                }
            ]

    @staticmethod
    def get_timestamp_from_list(phases, phase: TradingPhases, start_time: bool = True):
        for phase_from_list in phases:
            if phase_from_list['tradingPhase'] == phase.value:
                if start_time:
                    return phase_from_list['beginTime'].timestamp()
                else:
                    return phase_from_list['endTime'].timestamp()

    @staticmethod
    def update_endtime_for_trading_phase_by_phase_name(phase_list: list, phase_name: TradingPhases, end_time: datetime):
        new_phase_list = phase_list
        if phase_name == TradingPhases.PreOpen:
            new_phase_list[0].update(endTime=end_time)
            new_phase_list[1].update(beginTime=end_time, endTime=end_time + timedelta(minutes=5))
            new_phase_list[2].update(beginTime=end_time + timedelta(minutes=5), endTime=end_time + timedelta(minutes=5))
            new_phase_list[3].update(beginTime=end_time + timedelta(minutes=5), endTime=end_time + timedelta(minutes=4))
            new_phase_list[4].update(beginTime=end_time + timedelta(minutes=4), endTime=end_time + timedelta(minutes=5))
            new_phase_list[5].update(beginTime=end_time + timedelta(minutes=10), endTime=end_time + timedelta(minutes=5))
        elif phase_name == TradingPhases.Open:
            new_phase_list[1].update(endTime=end_time)
            new_phase_list[2].update(beginTime=end_time + timedelta(minutes=5), endTime=end_time + timedelta(minutes=5))
            new_phase_list[3].update(beginTime=end_time + timedelta(minutes=5), endTime=end_time + timedelta(minutes=4))
            new_phase_list[4].update(beginTime=end_time + timedelta(minutes=4), endTime=end_time + timedelta(minutes=5))
            new_phase_list[5].update(beginTime=end_time + timedelta(minutes=5), endTime=end_time + timedelta(minutes=5))
        elif phase_name == TradingPhases.PreClosed:
            new_phase_list[2].update(endTime=end_time)
            new_phase_list[3].update(beginTime=end_time + timedelta(minutes=5), endTime=end_time + timedelta(minutes=4))
            new_phase_list[4].update(beginTime=end_time + timedelta(minutes=4), endTime=end_time + timedelta(minutes=5))
            new_phase_list[5].update(beginTime=end_time + timedelta(minutes=5), endTime=end_time + timedelta(minutes=5))
        elif phase_name == TradingPhases.AtLast:
            new_phase_list[3].update(endTime=end_time)
            new_phase_list[4].update(beginTime=end_time + timedelta(minutes=5), endTime=end_time + timedelta(minutes=4))
            new_phase_list[5].update(beginTime=end_time + timedelta(minutes=4), endTime=end_time + timedelta(minutes=5))
        elif phase_name == TradingPhases.Closed:
            new_phase_list[4].update(endTime=end_time)
            new_phase_list[5].update(beginTime=end_time + timedelta(minutes=5), endTime=end_time + timedelta(minutes=5))
        elif phase_name == TradingPhases.Expiry:
            new_phase_list[5].update(endTime=end_time)

        return new_phase_list

    @staticmethod
    def get_litdark_child_price(ord_side: int, bid_price: float, ask_price: float, parent_qty: int, cost_per_trade: float , comm_per_unit: float = 12,
                                    comm_basis_point: float = 16, is_comm_per_unit: bool = False, spread_disc_proportion: int = 0) -> float:
        if ord_side == 1:
            lit_touch = bid_price
        else:
            lit_touch = ask_price
        giveup_cost = cost_per_trade / parent_qty
        if is_comm_per_unit == False:
            commission = comm_basis_point / 10000 * lit_touch
        else:
            commission = comm_per_unit
        custom_adjustment = (ask_price - bid_price) * spread_disc_proportion
        if ord_side == 1:
            return round((lit_touch + giveup_cost + commission + custom_adjustment), 4)
        else:
            return round((lit_touch - giveup_cost - commission - custom_adjustment), 4)

    @staticmethod
    def get_child_qty_for_auction(indicative_volume, percentage, parent_qty):
        child_qty = ceil(indicative_volume * percentage / (100 - percentage))
        return min(child_qty, parent_qty)

    @staticmethod
    def get_child_qty_for_auction_first_child(indicative_volume, percentage, parent_qty, initial_slice_multiplier):
        return ceil(indicative_volume * percentage / (100 - percentage) * (initial_slice_multiplier / 100))

    @staticmethod
    def get_child_qty_for_auction_historical_volume(historical_volume, percentage, parent_qty):
        return ceil(historical_volume * percentage / 100)

    @staticmethod
    def get_bi_lateral_auction_qty(indicative_volume, percentage, tradeable_qty, parent_qty):
        return AlgoFormulasManager.get_child_qty_for_auction((indicative_volume - tradeable_qty), percentage, parent_qty)