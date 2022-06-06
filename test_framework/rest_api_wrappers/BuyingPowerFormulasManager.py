class BuyingPowerFormulasManager:

    @staticmethod
    def calc_buying_power(response_wa, response_trd, collateral_qty=5):

        available_balance = float(response_trd['AvailableCash'])
        cash_loan = float(response_wa['cashLoaned'])
        temporary_cash = float(response_wa['temporaryCash'])
        collateral_cash = float(response_wa['collateralCash'])
        security_value = float(response_trd['AvgPrice']) * collateral_qty
        buying_power = available_balance + cash_loan + temporary_cash + collateral_cash + security_value
        return buying_power

    @staticmethod
    def calc_gross_order_value(response, reference_price=None):
        if reference_price is not None:
            return float(response['OrdQty']) * float(reference_price)
        else:
            return float(response['OrdQty']) * float(response['Price'])

    def calc_net_order_value(self, response, side):
        gross_order_value = float(self.calc_gross_order_value(response))
        vat = float(response['BookedVATMiscFeeAmt'])
        commission = float(response['BookedClientCommission'])
        if side == 'Buy':
            return gross_order_value + vat + commission
        elif side == 'Sell':
            return gross_order_value - vat - commission

    def calc_cash_balance(self, response, side):
        net_order_value = float(self.calc_net_order_value(response, side))
        buying_power = float(response['BuyingPowerLimitAmt'])
        if side == 'Buy':
            return buying_power - net_order_value
        elif side == 'Sell':
            return buying_power + net_order_value

    @staticmethod
    def calc_total_posit_qty(response, order_qty):

        initial_qty = float(response['initialQty'])
        cum_buy_qty = float(response['cumBuyQty'])
        cum_sell_qty = float(response['cumSellQty'])
        transferred_in_qty = float(response['transferredInQty'])
        transferred_out_qty = float(response['transferredOutQty'])
        exercised_qty = float(response['exercisedQty'])
        leaves_sell_qty = float(response['leavesSellQty'])
        reserved_qty = float(response['reservedQty'])

        posit_qty = initial_qty + cum_buy_qty - cum_sell_qty + transferred_in_qty - transferred_out_qty - exercised_qty
        total_posit_qty = posit_qty - leaves_sell_qty - reserved_qty - order_qty
        return total_posit_qty

