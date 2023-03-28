class PositionCalculationManager:
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
    def calculate_today_gross_pl_buy_side(daily_realized_gross_pl: str, posit_qty: str, exec_qty: str, exec_price: str,
                                          gross_weighted_avg_px: str, cross_rate=1):
        if float(posit_qty) < 0:
            daily_realized_gross_pl = float(daily_realized_gross_pl) - \
                                      (min(float(posit_qty), float(exec_qty)) * (
                                                  float(exec_price) * float(cross_rate) - float(gross_weighted_avg_px)))
            return daily_realized_gross_pl
        else:
            return daily_realized_gross_pl

    @staticmethod
    def calculate_today_net_pl_buy_side(daily_realized_net_pl: str, posit_qty: str, exec_qty: str, exec_price: str,
                                        net_weighted_avg_px: str, client_commission=None, fees=None, cross_rate=1):
        if float(posit_qty) < 0:
            daily_realized_net_pl_after = float(daily_realized_net_pl) - (
                    min(abs(float(posit_qty)), float(exec_qty)) * (
                    float(exec_price * cross_rate) - float(net_weighted_avg_px)))
            if client_commission:
                daily_realized_net_pl_after = daily_realized_net_pl_after - (float(client_commission) * cross_rate)
            if fees:
                daily_realized_net_pl_after = daily_realized_net_pl_after - (float(fees) * cross_rate)
            return str(daily_realized_net_pl_after)
        else:
            return daily_realized_net_pl

    @staticmethod
    def calculate_gross_weighted_avg_px_buy_side(gross_weight_avg_px, posit_qty: str, exec_qty: str, exec_price: str,
                                                 cross_rate=1):
        if float(posit_qty) >= float(0):
            gross_weight_avg_px = \
                (float(gross_weight_avg_px) * float(posit_qty) + float(exec_qty) * float(exec_price) * float(
                    cross_rate)) / (
                        float(posit_qty) + float(exec_qty))
            return str(gross_weight_avg_px)
        if float(posit_qty) < float(0):
            if float(exec_qty) < abs(float(posit_qty)):
                return gross_weight_avg_px
            if float(exec_qty) > abs(float(posit_qty)):
                gross_weight_avg_px = float(exec_price) * float(cross_rate) * float(exec_qty) / float(exec_qty)
                return str(gross_weight_avg_px)
            if float(exec_qty) == abs(float(posit_qty)):
                return 0

    @staticmethod
    def calculate_net_weighted_avg_px(net_weight_avg_px, posit_qty: str, exec_qty: str, exec_price: str,
                                      commission: str = None, fees: str = None, cross_rate=1):
        if float(posit_qty) < 0:
            if float(exec_qty) > abs(float(posit_qty)):
                net_weight_avg_px_after = float(exec_qty) * float(exec_price) * cross_rate
                if commission:
                    net_weight_avg_px_after = net_weight_avg_px_after + float(commission) * cross_rate
                if fees:
                    net_weight_avg_px_after = net_weight_avg_px_after + float(fees) * cross_rate
                return str(net_weight_avg_px_after / float(exec_qty))
            if float(exec_qty) < abs(float(posit_qty)):
                return net_weight_avg_px
            if float(exec_qty) == abs(float(posit_qty)):
                return '0'

    @staticmethod
    def calculate_buy_avg_px(posit_qty, exec_qty, exec_price, buy_avg_px, cross_rate='1', fees='0',
                             client_commission='0'):
        if float(posit_qty) >= 0 or (float(posit_qty) < 0 and float(exec_qty) < abs(float(posit_qty))):
            buy_avg_px = (float(buy_avg_px) * float(posit_qty) + float(exec_qty) * float(cross_rate) *
                          float(exec_price) + float(fees) *
                          float(cross_rate) + float(client_commission) * float(cross_rate)) / \
                         (float(posit_qty) + float(exec_qty))
        elif float(posit_qty) < 0:
            if float(exec_qty) > abs(float(posit_qty)):
                buy_avg_px = (float(exec_qty) * float(cross_rate) *
                              float(exec_price) + float(fees) *
                              float(cross_rate) + float(client_commission) * float(cross_rate)) / \
                             (float(exec_qty))
            elif float(exec_qty) == abs(float(posit_qty)):
                buy_avg_px = 0

        return buy_avg_px



