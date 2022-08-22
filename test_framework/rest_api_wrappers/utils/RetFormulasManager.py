import logging
from custom import basic_custom_actions as bca


class RetFormulasManager:

    @staticmethod
    def calc_available_balance(response_wa_cash_account):
        cash_position = response_wa_cash_account.keys()

        initial_balance = 0
        sell_amount = 0
        buy_amount = 0
        cash_deposited = 0
        cash_withdrawn = 0
        booked_amount = 0
        reserved_amount = 0

        if 'initialBalance' in cash_position:
            initial_balance = float(response_wa_cash_account['initialBalance'])
        if 'amountSoldIn' in cash_position:
            sell_amount = float(response_wa_cash_account['amountSoldIn'])
        if 'amountBought' in cash_position:
            buy_amount = float(response_wa_cash_account['amountBought'])
        if 'cashDeposited' in cash_position:
            cash_deposited = float(response_wa_cash_account['cashDeposited'])
        if 'cashWithdrawn' in cash_position:
            cash_withdrawn = float(response_wa_cash_account['cashWithdrawn'])
        if 'bookedAmt' in cash_position:
            booked_amount = float(response_wa_cash_account['bookedAmt'])
        if 'reservedAmt' in cash_position:
            reserved_amount = float(response_wa_cash_account['reservedAmt'])

        return initial_balance + sell_amount - buy_amount + cash_deposited - cash_withdrawn - booked_amount - reserved_amount

    def calc_buying_power(self, response_wa_cash_account, response_wa_security_account):
        cash_position = response_wa_cash_account.keys()
        security_position = response_wa_security_account.keys()

        cash_loan = 0
        temporary_cash = 0
        collateral_cash = 0
        collateral_qty = 0
        available_balance = self.calc_available_balance(response_wa_cash_account)
        reserved_qty = float(response_wa_security_account['reservedQty'])
        average_price = float(response_wa_security_account['avgPx'])

        if 'cashLoaned' in cash_position:
            cash_loan = float(response_wa_cash_account['cashLoaned'])
        if 'temporaryCash' in cash_position:
            temporary_cash = float(response_wa_cash_account['temporaryCash'])
        if 'collateralCash' in cash_position:
            collateral_cash = float(response_wa_cash_account['collateralCash'])
        if 'collateralQty' in security_position:
            collateral_qty = float(response_wa_security_account['collateralQty'])

        security_value = average_price * (collateral_qty - reserved_qty)

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
    def calc_posit_qty(response_wa_security_position, test_id):
        try:
            initial_qty = float(response_wa_security_position['initialQty'])
            cum_buy_qty = float(response_wa_security_position['cumBuyQty'])
            cum_sell_qty = float(response_wa_security_position['cumSellQty'])
            transferred_in_qty = float(response_wa_security_position['transferredInQty'])
            transferred_out_qty = float(response_wa_security_position['transferredOutQty'])
            exercised_qty = float(response_wa_security_position['exercisedQty'])

            posit_qty = initial_qty + cum_buy_qty - cum_sell_qty + transferred_in_qty - transferred_out_qty - exercised_qty
            return posit_qty
        except(ValueError, IndexError, TypeError):
            bca.create_event(f'Posit Qty was not calculated', status='FAILED', parent_id=test_id)
            logging.error("Error parsing", exc_info=True)

    def calc_total_posit_qty(self, response_wa_security_position, order_qty, test_id):
        try:
            leaves_sell_qty = float(response_wa_security_position['leavesSellQty'])
            reserved_qty = float(response_wa_security_position['reservedQty'])
            posit_qty = self.calc_posit_qty(response_wa_security_position, test_id)

            total_posit_qty = posit_qty - leaves_sell_qty - reserved_qty - order_qty
            return total_posit_qty
        except(ValueError, IndexError, TypeError):
            bca.create_event(f'Total Posit Qty was not calculated', status='FAILED', parent_id=test_id)
            logging.error("Error parsing", exc_info=True)

