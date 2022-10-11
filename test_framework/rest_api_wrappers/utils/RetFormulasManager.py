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

    @staticmethod
    def calc_security_value(test_id, response_wa_security_account):

        try:
            security_value_type_net = 0
            reserved_qty_type_net = 0
            security_value_type_long = 0
            reserved_qty_type_long = 0
            security_value_type_short = 0
            reserved_qty_type_short = 0

            for count in range(len(response_wa_security_account)):
                security_position = response_wa_security_account[count].keys()
                collateral_qty = 0
                reserved_qty = float(response_wa_security_account[count]['reservedQty'])
                average_price = float(response_wa_security_account[count]['grossWeightedAvgPx'])
                if 'collateralQty' in security_position:
                    collateral_qty = float(response_wa_security_account[count]['collateralQty'])
                if response_wa_security_account[count]['positionType'] == 'N':
                    reserved_qty_type_net = float(response_wa_security_account[count]['reservedQty'])
                    security_value_type_net = average_price * (collateral_qty - reserved_qty)
                if response_wa_security_account[count]['positionType'] == 'L':
                    reserved_qty_type_long = float(response_wa_security_account[count]['reservedQty'])
                    security_value_type_long = average_price * (collateral_qty - reserved_qty)
                if response_wa_security_account[count]['positionType'] == 'S':
                    reserved_qty_type_short = float(response_wa_security_account[count]['reservedQty'])
                    security_value_type_short = average_price * (collateral_qty - reserved_qty)
            security_values_sum = security_value_type_net + security_value_type_long + security_value_type_short
            return {
                'securityValueSum': security_values_sum,
                'securityValueNetPosition': security_value_type_net,
                'securityValueLongPosition': security_value_type_long,
                'securityValueShorPosition': security_value_type_short,
                'reservedQtyNet': reserved_qty_type_net,
                'reservedQtyLong': reserved_qty_type_long,
                'reservedQtyShort': reserved_qty_type_short
            }
        except(ValueError, IndexError, TypeError):
            bca.create_event(f'Security Value was not calculated', status='FAILED', parent_id=test_id)
            logging.error("Error parsing", exc_info=True)

    def calc_buying_power(self, test_id, response_wa_cash_account, response_wa_security_account):
        try:
            cash_position = response_wa_cash_account.keys()

            cash_loan = 0
            booked_cash_loan = 0
            temporary_cash = 0
            booked_temporary_cash = 0
            collateral_cash = 0
            booked_collateral_cash = 0
            available_balance = self.calc_available_balance(response_wa_cash_account)
            security_value = self.calc_security_value(test_id, response_wa_security_account)

            if 'cashLoaned' in cash_position:
                cash_loan = float(response_wa_cash_account['cashLoaned'])
            if 'bookedCashLoan' in cash_position:
                booked_cash_loan = float(response_wa_cash_account['bookedCashLoan'])
            if 'temporaryCash' in cash_position:
                temporary_cash = float(response_wa_cash_account['temporaryCash'])
            if 'bookedTempCash' in cash_position:
                booked_temporary_cash = float(response_wa_cash_account['bookedTempCash'])
            if 'collateralCash' in cash_position:
                collateral_cash = float(response_wa_cash_account['collateralCash'])
            if 'bookedCollateralCash' in cash_position:
                booked_collateral_cash = float(response_wa_cash_account['bookedCollateralCash'])

            buying_power = available_balance + (cash_loan - booked_cash_loan) + (temporary_cash - booked_temporary_cash) \
                           + (collateral_cash - booked_collateral_cash) + security_value['securityValueSum']
            return buying_power
        except(ValueError, IndexError, TypeError):
            bca.create_event(f'BuyingPower was not calculated', status='FAILED', parent_id=test_id)
            logging.error("Error parsing", exc_info=True)

    @staticmethod
    def calc_gross_order_value(test_id, response_noss, reference_price=None):
        try:
            if reference_price is not None:
                return float(response_noss['OrdQty']) * float(reference_price)
            else:
                return float(response_noss['OrdQty']) * float(response_noss['Price'])
        except(ValueError, IndexError, TypeError):
            bca.create_event(f'Gross Order Value was not calculated', status='FAILED', parent_id=test_id)
            logging.error("Error parsing", exc_info=True)

    def calc_net_order_value(self, test_id, response_noss, side):
        try:
            gross_order_value = float(self.calc_gross_order_value(test_id, response_noss))
            vat = float(response_noss['BookedVATMiscFeeAmt'])
            commission = float(response_noss['BookedClientCommission'])
            if side == 'Buy':
                return gross_order_value + vat + commission
            elif side == 'Sell':
                return gross_order_value - vat - commission
        except(ValueError, IndexError, TypeError):
            bca.create_event(f'Net Order Value was not calculated', status='FAILED', parent_id=test_id)
            logging.error("Error parsing", exc_info=True)

    def calc_cash_balance(self, test_id, response_noss, side):
        try:
            net_order_value = float(self.calc_net_order_value(test_id, response_noss, side))
            buying_power = float(response_noss['BuyingPowerLimitAmt'])
            if side == 'Buy':
                return buying_power - net_order_value
            elif side == 'Sell':
                return buying_power + net_order_value
        except(ValueError, IndexError, TypeError):
            bca.create_event(f'Cash Balance was not calculated', status='FAILED', parent_id=test_id)
            logging.error("Error parsing", exc_info=True)

    @staticmethod
    def calc_posit_qty(test_id, response_wa_security_position):
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

    def calc_total_posit_qty(self, test_id, response_wa_security_position, order_qty):
        try:

            leaves_sell_qty = float(response_wa_security_position['leavesSellQty'])
            reserved_qty = float(response_wa_security_position['reservedQty'])
            posit_qty = self.calc_posit_qty(test_id, response_wa_security_position)

            total_posit_qty = posit_qty - leaves_sell_qty - reserved_qty - order_qty
            return total_posit_qty
        except(ValueError, IndexError, TypeError):
            bca.create_event(f'Total Posit Qty was not calculated', status='FAILED', parent_id=test_id)
            logging.error("Error parsing", exc_info=True)

    @staticmethod
    def get_cash_component_values(test_id, response_wa_cash_account):

        try:
            cash_position = response_wa_cash_account.keys()

            applicable_components = 0
            booked_amount = 0
            cash_loan = 0
            booked_cash_loan = 0
            temporary_cash = 0
            booked_temporary_cash = 0
            collateral_cash = 0
            booked_collateral_cash = 0

            if 'bookedAmt' in cash_position:
                booked_amount = float(response_wa_cash_account['bookedAmt'])
                applicable_components += 1

            if 'cashLoaned' in cash_position and 'bookedCashLoan' in cash_position:
                cash_loan = float(response_wa_cash_account['cashLoaned'])
                booked_cash_loan = float(response_wa_cash_account['bookedCashLoan'])
                if cash_loan > booked_cash_loan:
                    applicable_components += 1

            if 'temporaryCash' in cash_position and 'bookedTempCash' in cash_position:
                temporary_cash = float(response_wa_cash_account['temporaryCash'])
                booked_temporary_cash = float(response_wa_cash_account['bookedTempCash'])
                if temporary_cash > booked_temporary_cash:
                    applicable_components += 1

            if 'collateralCash' in cash_position and 'bookedCollateralCash' in cash_position:
                collateral_cash = float(response_wa_cash_account['collateralCash'])
                booked_collateral_cash = float(response_wa_cash_account['bookedCollateralCash'])
                if collateral_cash > booked_collateral_cash:
                    applicable_components += 1

            cash_component_values = {
                'bookedAmt': booked_amount,
                'cashLoaned': cash_loan,
                'bookedCashLoan': booked_cash_loan,
                'temporaryCash': temporary_cash,
                'bookedTempCash': booked_temporary_cash,
                'collateralCash': collateral_cash,
                'bookedCollateralCash': booked_collateral_cash,
                'applicableCashComponents': applicable_components
            }

            return cash_component_values
        except(ValueError, IndexError, TypeError):
            bca.create_event(f'Failed to get cache component values', status='FAILED', parent_id=test_id)
            logging.error("Error parsing", exc_info=True)

    def calc_booked_amount_buy_side(self, test_id, response_wa_cash_account, response_wa_security_account, initial_net_order_value,
                                    execution_type, amended_net_order_value=None, position_type='N'):

        try:
            initial_net_order_value = float(initial_net_order_value)
            execution_type = execution_type
            cash_component_values = self.get_cash_component_values(test_id, response_wa_cash_account)
            security_values_dict = self.calc_security_value(test_id, response_wa_security_account)
            booked_amount = cash_component_values['bookedAmt']
            cash_loan = cash_component_values['cashLoaned']
            booked_cash_loan = cash_component_values['bookedCashLoan']
            temporary_cash = cash_component_values['temporaryCash']
            booked_temporary_cash = cash_component_values['bookedTempCash']
            collateral_cash = cash_component_values['collateralCash']
            booked_collateral_cash = cash_component_values['bookedCollateralCash']
            applicable_cash_components = cash_component_values['applicableCashComponents']
            reserved_qty = 0
            security_value = 0

            if position_type == 'N':
                reserved_qty = round(security_values_dict['reservedQtyNet'], 3)
                security_value = security_values_dict['securityValueNetPosition']
            if position_type == 'L':
                reserved_qty = round(security_values_dict['reservedQtyLong'], 3)
                security_value = security_values_dict['securityValueLongPosition']
            if position_type == 'S':
                reserved_qty = round(security_values_dict['reservedQtyShort'], 3)
                security_value = security_values_dict['securityValueShortPosition']

            if security_value - (initial_net_order_value / 5) > 0:
                applicable_cash_components += 1

            if execution_type == 'Open':
                total_booked_amount_value = initial_net_order_value / applicable_cash_components
                booked_amount += total_booked_amount_value
                if cash_loan > booked_cash_loan:
                    booked_cash_loan += total_booked_amount_value
                if temporary_cash > booked_temporary_cash:
                    booked_temporary_cash += total_booked_amount_value
                if collateral_cash > booked_collateral_cash:
                    booked_collateral_cash += total_booked_amount_value
                if applicable_cash_components == 5:
                    reserved_qty += total_booked_amount_value

                return {
                    'bookedAmt': booked_amount,
                    'bookedCashLoan': booked_cash_loan,
                    'bookedTempCash': booked_temporary_cash,
                    'bookedCollateralCash': booked_collateral_cash,
                    'reservedQty': reserved_qty,
                    'totalBookedAmount': total_booked_amount_value
                }

            if execution_type == 'Replaced':
                net_order_value_delta = amended_net_order_value - initial_net_order_value
                buying_power = self.calc_buying_power(test_id, response_wa_cash_account, response_wa_security_account)
                amended_booked_amount_value = net_order_value_delta / applicable_cash_components
                if amended_booked_amount_value > 0 and buying_power >= net_order_value_delta:
                    booked_amount += amended_booked_amount_value
                    if cash_loan > booked_cash_loan:
                        booked_cash_loan += amended_booked_amount_value
                    if temporary_cash > booked_temporary_cash:
                        booked_temporary_cash += amended_booked_amount_value
                    if collateral_cash > booked_collateral_cash:
                        booked_collateral_cash += amended_booked_amount_value
                    if applicable_cash_components == 5:
                        reserved_qty += amended_booked_amount_value
                    return {
                        'bookedAmt': booked_amount,
                        'bookedCashLoan': booked_cash_loan,
                        'bookedTempCash': booked_temporary_cash,
                        'bookedCollateralCash': booked_collateral_cash,
                        'reservedQty': reserved_qty,
                        'amendedBookedAmount': amended_booked_amount_value
                    }
                elif amended_booked_amount_value < 0:
                    booked_amount -= abs(amended_booked_amount_value)
                    if cash_loan > booked_cash_loan:
                        booked_cash_loan -= abs(amended_booked_amount_value)
                    if temporary_cash > booked_temporary_cash:
                        booked_temporary_cash -= abs(amended_booked_amount_value)
                    if collateral_cash > booked_collateral_cash:
                        booked_collateral_cash -= abs(amended_booked_amount_value)
                    if applicable_cash_components == 5:
                        reserved_qty -= abs(amended_booked_amount_value)
                    return {
                        'bookedAmt': booked_amount,
                        'bookedCashLoan': booked_cash_loan,
                        'bookedTempCash': booked_temporary_cash,
                        'bookedCollateralCash': booked_collateral_cash,
                        'reservedQty': reserved_qty,
                        'amendedBookedAmount': amended_booked_amount_value
                    }

            if execution_type == 'Cancelled':
                total_booked_amount_value = initial_net_order_value / applicable_cash_components
                booked_amount -= total_booked_amount_value
                if cash_loan > booked_cash_loan:
                    booked_cash_loan -= total_booked_amount_value
                if temporary_cash > booked_temporary_cash:
                    booked_temporary_cash -= total_booked_amount_value
                if collateral_cash > booked_collateral_cash:
                    booked_collateral_cash -= total_booked_amount_value
                if applicable_cash_components == 5:
                    reserved_qty -= total_booked_amount_value

                return {
                    'bookedAmt': booked_amount,
                    'bookedCashLoan': booked_cash_loan,
                    'bookedTempCash': booked_temporary_cash,
                    'bookedCollateralCash': booked_collateral_cash,
                    'reservedQty': reserved_qty,
                    'totalBookedAmount': total_booked_amount_value
                }

        except(ValueError, IndexError, TypeError, ZeroDivisionError):
            bca.create_event(f'Booked Amount was not calculated. (Side=Buy)', status='FAILED', parent_id=test_id)
            logging.error("Error parsing", exc_info=True)

    def calc_booked_amount_sell_side(self, test_id, response_wa_cash_account, response_wa_security_account, fee,
                                     commission, execution_type, position_type='N'):
        try:
            cash_component_values = self.get_cash_component_values(test_id, response_wa_cash_account)
            security_values_dict = self.calc_security_value(test_id, response_wa_security_account)
            booked_amount = cash_component_values['bookedAmt']
            booked_cash_loan = cash_component_values['bookedCashLoan']
            booked_temporary_cash = cash_component_values['bookedTempCash']
            booked_collateral_cash = cash_component_values['bookedCollateralCash']
            reserved_qty = 0

            if position_type == 'N':
                reserved_qty = round(security_values_dict['reservedQtyNet'], 3)
            if position_type == 'L':
                reserved_qty = round(security_values_dict['reservedQtyLong'], 3)
            if position_type == 'S':
                reserved_qty = round(security_values_dict['reservedQtyShort'], 3)

            if execution_type == 'Open':
                booked_amount += fee + commission
                return {
                    'bookedAmt': booked_amount,
                    'bookedCashLoan': booked_cash_loan,
                    'bookedTempCash': booked_temporary_cash,
                    'bookedCollateralCash': booked_collateral_cash,
                    'reservedQty': reserved_qty
                }
            if execution_type == 'Cancelled':
                booked_amount -= fee + commission
                return {
                    'bookedAmt': booked_amount,
                    'bookedCashLoan': booked_cash_loan,
                    'bookedTempCash': booked_temporary_cash,
                    'bookedCollateralCash': booked_collateral_cash,
                    'reservedQty': reserved_qty
                }

        except(ValueError, IndexError, TypeError):
            bca.create_event(f'Booked Amount was not calculated. (Side=Sell)', status='FAILED', parent_id=test_id)
            logging.error("Error parsing", exc_info=True)
