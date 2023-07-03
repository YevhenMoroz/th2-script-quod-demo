import copy

from test_cases.fx.fx_wrapper.common_tools import get_cross_rate


class PositionCalculationManager:
    def __init__(self):
        self.cumulative_quote_pos = 0
        self.cumulative_base_pos = 0
        self.cumulative_daily_quote_pos = 0
        self.call_count = 0

    def get_cumulative_quote_pos(self):
        return self.cumulative_quote_pos

    def update_cumulative_quote_pos(self, quote_pos):
        self.cumulative_quote_pos = quote_pos

    def get_cumulative_base_pos(self):
        return self.cumulative_base_pos

    def update_cumulative_base_pos(self, base_pos):
        self.cumulative_base_pos = base_pos

    def get_cumulative_daily_quote_pos(self):
        return self.cumulative_daily_quote_pos

    def update_cumulative_daily_quote_pos(self, daily_quote_pos):
        self.cumulative_daily_quote_pos = daily_quote_pos

    def calculate_base_position(self, qty, side):
        base_pos = copy.deepcopy(self.get_cumulative_base_pos())
        if side == "B":
            base_pos += float(qty)
        else:
            base_pos += -float(qty)
        self.update_cumulative_base_pos(base_pos)
        return str(base_pos)

    def calculate_quote_position(self, qty, price, side):
        quote_pos = copy.deepcopy(self.get_cumulative_quote_pos())  # Get the cumulative quote position for the symbol

        if side == "B":
            quote_pos += -float(qty) * float(price)
        else:
            quote_pos += float(qty) * float(price)

        self.update_cumulative_quote_pos(quote_pos)

        if str(quote_pos).endswith(".0"):
            return str(quote_pos)[:-2]
        else:
            return str(round(quote_pos, 3))

    def calculate_sys_quote_position(self, qty, price, symbol, side):
        cross_rate = get_cross_rate(symbol)
        quote_pos = copy.deepcopy(self.get_cumulative_quote_pos())  # Get the cumulative quote position for the symbol

        if side == "B":
            quote_pos += -float(qty) * float(price)
        else:
            quote_pos += float(qty) * float(price)

        system_quote_pos = quote_pos / float(cross_rate)
        self.update_cumulative_quote_pos(quote_pos)

        if str(system_quote_pos).endswith(".0"):
            return str(system_quote_pos)[:-2]
        else:
            return str(round(system_quote_pos, 8))

    def calculate_mtm_pnl(self, qty, price, symbol, side):
        cross_rate = get_cross_rate(symbol)
        quote_pos = self.calculate_quote_position(qty, price, side)
        base_position = self.calculate_base_position(qty, side)
        pnl = float(base_position) * float(cross_rate) + float(quote_pos)
        if str(pnl).endswith(".0"):
            return str(pnl)[:-2]
        else:
            return str(round(pnl, 9))

    def calculate_daily_mtm_quote_position(self, qty, price, side):
        daily_quote_pos = copy.deepcopy(self.get_cumulative_daily_quote_pos())
        self.call_count += 1
        if self.call_count == 1:
            return 0
        if side == "B":
            daily_quote_pos += -float(qty) * float(price)
        else:
            daily_quote_pos += float(qty) * float(price)
        self.update_cumulative_daily_quote_pos(daily_quote_pos)
        return daily_quote_pos

    def calculate_daily_mtm_pnl(self, qty, price, symbol, side):
        position = self.calculate_base_position(qty, side)
        cross_rate = get_cross_rate(symbol)
        daily_pnl = float(position) * float(cross_rate) + self.calculate_daily_mtm_quote_position(qty, price, side)
        suffixes = (".0", ".000000001")
        if any(str(daily_pnl).endswith(suffix) for suffix in suffixes):
            return str(daily_pnl).split(".")[0]  # remove the .0 or .000000001
        else:
            return str(round(daily_pnl, 9))

    def calculate_sys_daily_mtm_pnl(self, qty, price, symbol, side):
        position = self.calculate_base_position(qty, side)
        cross_rate = get_cross_rate(symbol)
        daily_pnl = (float(position) * float(cross_rate) +
                     self.calculate_daily_mtm_quote_position(qty, price, side)) / float(cross_rate)
        suffixes = (".0", ".000000001")
        if any(str(daily_pnl).endswith(suffix) for suffix in suffixes):
            return str(daily_pnl).split(".")[0]  # remove the .0 or .000000001
        else:
            return str(round(daily_pnl, 8))

    def calculate_system_mtm_pnl(self, qty, price, symbol, side):
        cross_rate = get_cross_rate(symbol)
        base_position = self.calculate_base_position(qty, side)
        quote_pos = self.calculate_quote_position(qty, price, side)
        pnl = (float(base_position) * float(cross_rate) + float(quote_pos)) / float(cross_rate)
        if str(pnl).endswith(".0"):
            return str(pnl)[:-2]
        else:
            return str(round(pnl, 9))

    def calculate_daily_avg_px(self, qty, price, side):
        daily_quote_pos = self.calculate_daily_mtm_quote_position(qty, price, side)
        base_pos = self.calculate_base_position(qty, side)
        daily_avg_px = float(daily_quote_pos) / float(base_pos)
        return str(round(daily_avg_px, 2))

    @staticmethod
    def calculate_position_buy(position_before: str, order_qty: str) -> str:
        expected_pos = int(position_before.replace(",", "")) + int(order_qty)
        return str(expected_pos)

    @staticmethod
    def calculate_position_sell(position_before: str, order_qty: str) -> str:
        expected_pos = int(position_before.replace(",", "")) - int(order_qty)
        return str(expected_pos)

    # equity position`s formulas
    # cross_rate = 1 if PositCurrency equals TradingCurrency
    @staticmethod
    def calculate_today_gross_pl_buy_side_execution(daily_realized_gross_pl: str, posit_qty: str, exec_qty: str,
                                                    exec_price: str,
                                                    gross_weighted_avg_px: str, cross_rate=1):
        if float(posit_qty) < 0:
            daily_realized_gross_pl = float(daily_realized_gross_pl) - \
                                      (min(-float(posit_qty), float(exec_qty)) * (
                                              float(exec_price) * float(cross_rate) - float(gross_weighted_avg_px)))
            return str(daily_realized_gross_pl)
        else:
            return str(daily_realized_gross_pl)

    @staticmethod
    def calculate_realized_pl_buy_side_execution(posit_qty: str, exec_qty: str,
                                                 exec_price: str,
                                                 net_weighted_avg_px: str, client_commission='0.0', fees='0.0',
                                                 cross_rate=1):
        if float(posit_qty) < 0:
            realized_pl = -(
                    min(-float(posit_qty), float(exec_qty)) * (float(exec_price) - float(net_weighted_avg_px))) - \
                          ((float(client_commission) + float(fees)) * float(cross_rate))
            print(realized_pl)
            print(float(exec_price) - float(net_weighted_avg_px))
            print(-float(posit_qty))
            print(min(-float(posit_qty), float(exec_qty)))
            return str(realized_pl)
        else:
            return '0.0'

    @staticmethod
    def calculate_gross_weighted_avg_px_buy_side_execution(gross_weight_avg_px, posit_qty: str, exec_qty: str,
                                                           exec_price: str,
                                                           cross_rate=1):
        if float(posit_qty) >= float(0):
            gross_weight_avg_px = \
                (float(gross_weight_avg_px) * float(posit_qty) + float(exec_qty) * float(exec_price) * float(
                    cross_rate)) / (
                        float(posit_qty) + float(exec_qty))
            return str(gross_weight_avg_px)
        if float(posit_qty) < float(0):
            if float(exec_qty) < -(float(posit_qty)):
                return str(gross_weight_avg_px)
            if float(exec_qty) > -(float(posit_qty)):
                gross_weight_avg_px = float(exec_price) * float(cross_rate) * float(exec_qty) / float(exec_qty)
                return str(gross_weight_avg_px)
            if float(exec_qty) == -(float(posit_qty)):
                return '0.0'

    @staticmethod
    def calculate_net_weighted_avg_px_buy_side_execution(net_weight_avg_px, posit_qty: str, exec_qty: str,
                                                         exec_price: str,
                                                         commission: str = '0.0', fees: str = '0.0', cross_rate=1):
        if float(posit_qty) >= 0:
            net_weight_avg_px = (float(net_weight_avg_px) * float(posit_qty) + float(exec_qty) * float(
                exec_price) * float(cross_rate) +
                                 (float(commission) + float(fees)) * float(cross_rate)) / (
                                        float(posit_qty) + float(exec_qty))
            return str(net_weight_avg_px)
        if float(posit_qty) < 0:
            if float(exec_qty) < -float(posit_qty):
                return str(net_weight_avg_px)
            if float(exec_qty) > -float(posit_qty):
                net_weight_avg_px = (float(exec_qty) * float(exec_price) + (float(commission) + float(fees)) * float(
                    cross_rate)) / float(exec_qty)
                return str(net_weight_avg_px)
            if float(exec_qty) == -float(posit_qty):
                return '0.0'

    @staticmethod
    def calculate_buy_avg_px_execution_buy_side(posit_qty, exec_qty, exec_price, buy_avg_px, cross_rate='1', fees='0',
                                                client_commission='0'):
        if float(posit_qty) >= 0:
            buy_avg_px = (float(buy_avg_px) * float(posit_qty) + float(exec_qty) * float(exec_price) * float(
                cross_rate) + (float(client_commission) + float(fees)) * float(cross_rate)) / (
                                 float(posit_qty) + float(exec_qty))
            return str(buy_avg_px)
        if float(posit_qty) < 0:
            if float(exec_qty) < -float(posit_qty):
                buy_avg_px = (float(buy_avg_px) * float(posit_qty) + float(exec_qty) * float(exec_price) * float(
                    cross_rate) + (float(client_commission) + float(fees)) * float(cross_rate)) / (
                                     float(posit_qty) + float(exec_qty))
                return str(buy_avg_px)
            if float(exec_qty) > -float(posit_qty):
                buy_avg_px = (float(exec_qty) * float(exec_price) * float(cross_rate) + (
                        float(fees) + float(client_commission)) * float(cross_rate)) / float(exec_qty)
                return str(buy_avg_px)

            if float(exec_qty) == -float(posit_qty):
                return '0.0'
        else:
            return buy_avg_px

    @staticmethod
    def calculate_sell_avg_px_execution_sell_side_net(posit_qty, exec_qty, exec_price, sell_avg_px, cross_rate='1',
                                                      fees='0',
                                                      client_commission='0'):
        if float(posit_qty) <= 0:
            sell_avg_px = (float(sell_avg_px) * (-float(posit_qty)) + (
                    float(exec_qty) * float(exec_price) * float(cross_rate) - (
                    float(fees) + float(client_commission)) * float(cross_rate))) / (
                                  -float(posit_qty) + float(exec_qty))
            return str(sell_avg_px)
        if float(posit_qty) > 0:
            if float(exec_qty) < float(posit_qty):
                sell_avg_px = (float(sell_avg_px) * float(posit_qty) - (
                        float(exec_qty) * float(exec_price) * float(cross_rate) - (
                        float(fees) + float(client_commission)) * float(cross_rate))) / (
                                      float(posit_qty) - float(exec_qty))
                return str(sell_avg_px)
            if float(exec_qty) > float(posit_qty):
                sell_avg_px = (float(exec_qty) * float(exec_price) * float(cross_rate) - (
                        float(fees) + float(client_commission)) * float(cross_rate)) / float(exec_qty)
                return str(sell_avg_px)
            if float(exec_qty) == -float(posit_qty):
                return '0.0'
        else:
            return sell_avg_px

    @staticmethod
    def calculate_net_weighted_avg_px_for_position_transfer_source_acc(posit_qty, qty_to_transfer, net_weighted_avg_px,
                                                                       transfer_price):
        if float(posit_qty) <= 0:
            if float(qty_to_transfer) > 0:
                net_weighted_avg_px = (float(net_weighted_avg_px) * -(float(posit_qty)) +
                                       float(qty_to_transfer) * float(transfer_price)) / (
                                              -(float(posit_qty)) + float(qty_to_transfer))
                return str(net_weighted_avg_px)
            if float(qty_to_transfer) < float(posit_qty):
                net_weighted_avg_px = float(qty_to_transfer) * float(transfer_price) / float(qty_to_transfer)
                return str(net_weighted_avg_px)
            if float(qty_to_transfer) == -float(posit_qty):
                return '0.0'
        if float(posit_qty) > 0:
            if float(qty_to_transfer) < 0:
                net_weighted_avg_px = (float(net_weighted_avg_px) * float(posit_qty) +
                                       (-float(qty_to_transfer) * float(transfer_price))) / (
                                              float(posit_qty) - float(qty_to_transfer))
                return str(net_weighted_avg_px)
            if float(qty_to_transfer) > float(posit_qty):
                net_weighted_avg_px = float(qty_to_transfer) * float(transfer_price) / float(qty_to_transfer)
                return str(net_weighted_avg_px)

            if float(posit_qty) == float(qty_to_transfer):
                return '0.0'
            else:
                return str(net_weighted_avg_px)

    @staticmethod
    def calculate_realized_pl_for_transfer_sell(posit_qty, transfered_qty, transfered_price, net_weighted_avg_px):
        if float(posit_qty) > 0:
            realized_pl = min(float(posit_qty), float(transfered_qty)) * (
                    float(transfered_price) - float(net_weighted_avg_px))
            return str(realized_pl)
        else:
            return '0.0'

    @staticmethod
    def calculate_net_weighted_avg_px_for_position_transfer_destination_acc(posit_qty, qty_to_transfer,
                                                                            net_weighted_avg_px,
                                                                            transfer_price):
        if float(posit_qty) >= 0:
            if float(qty_to_transfer) > 0:
                net_weighted_avg_px = (float(net_weighted_avg_px) * float(posit_qty) + float(qty_to_transfer) * float(
                    transfer_price)) / (float(posit_qty) + float(qty_to_transfer))
                return str(net_weighted_avg_px)
            if float(qty_to_transfer) < -float(posit_qty):
                net_weighted_avg_px = -float(qty_to_transfer) * float(transfer_price) / -float(qty_to_transfer)
                return str(net_weighted_avg_px)
            if float(qty_to_transfer) == -float(posit_qty):
                return '0.0'
            else:
                return str(net_weighted_avg_px)
        if float(posit_qty) < 0:
            if float(qty_to_transfer) < 0:
                net_weighted_avg_px = (float(net_weighted_avg_px) * (-float(posit_qty)) + (
                    -float(qty_to_transfer)) * float(
                    transfer_price)) / (-float(posit_qty) - float(qty_to_transfer))
                return str(net_weighted_avg_px)
            if float(qty_to_transfer) > -float(posit_qty):
                net_weighted_avg_px = float(qty_to_transfer) * float(transfer_price) / float(qty_to_transfer)
                return str(net_weighted_avg_px)
            if float(qty_to_transfer) == -float(posit_qty):
                return '0.0'
            else:
                return str(net_weighted_avg_px)
