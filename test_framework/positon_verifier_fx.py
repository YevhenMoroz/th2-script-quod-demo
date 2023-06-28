from custom.verifier import Verifier
from test_framework.position_calculation_manager import PositionCalculationManager


class PositionVerifier:

    def __init__(self, test_id):
        self.test_id = test_id
        self.verifier = Verifier(test_id)
        self.pos_calc = PositionCalculationManager()

    def check_base_position(self, report, expected_value, text="Check Base Position"):
        pos_amount_date = report[1].get_parameters()["PositionAmountData"][0]
        amount = pos_amount_date["PosAmt"]
        self.verifier.set_event_name(text)
        self.verifier.compare_values("Compare Base", expected_value, amount)
        self.verifier.verify()
        self.verifier = Verifier(self.test_id)

    def check_avg_price(self, report, expected_value):
        pos_amount_date = report[1].get_parameters()["PositionAmountData"][6]
        amount = pos_amount_date["PosAmt"]
        self.verifier.set_event_name("Check Avg Price")
        self.verifier.compare_values("Compare Avg PX", expected_value, amount)
        self.verifier.verify()
        self.verifier = Verifier(self.test_id)

    def check_quote_position_default(self, report, trade):
        qty = trade.get_exec_qty()
        price = trade.get_exec_price()
        expected_value = self.pos_calc.calculate_quote_position(qty, price)
        pos_amount_date = report[1].get_parameters()["PositionAmountData"][29]
        amount = pos_amount_date["PosAmt"]
        self.verifier.set_event_name("Check Quote Position")
        self.verifier.compare_values("Compare Quote Position", expected_value, amount)
        self.verifier.verify()
        self.verifier = Verifier(self.test_id)

    def check_backup_after_trade(self, report, trade_qty, trade_px):
        pass

    def check_system_cur_position(self, report, expected_value):
        pos_amount_date = report[1].get_parameters()["PositionAmountData"][8]
        amount = pos_amount_date["PosAmt"]
        self.verifier.set_event_name("Check System Currency Position")
        self.verifier.compare_values("Compare Position", expected_value, amount)
        self.verifier.verify()
        self.verifier = Verifier(self.test_id)

    def check_system_quote_position(self, report, trade):
        qty = trade.get_exec_qty()
        price = trade.get_exec_price()
        symbol = trade.get_symbol()
        side = trade.get_side()
        expected_value = self.pos_calc.calculate_sys_quote_position(qty, price, symbol, side)
        pos_amount_date = report[1].get_parameters()["PositionAmountData"][7]
        amount = pos_amount_date["PosAmt"]
        self.verifier.set_event_name("Check SysQuote Position")
        self.verifier.compare_values("Compare SysQuote Position", expected_value, amount)
        self.verifier.verify()
        self.verifier = Verifier(self.test_id)

    def check_transact_time(self, report, expected_value):
        transact_time = report[1].get_parameters()["TransactTime"]
        transact_time = transact_time[0:19]
        expected_value = expected_value[0:19]
        self.verifier.set_event_name("Check Transact time")
        self.verifier.compare_values("Compare time", expected_value, transact_time)
        self.verifier.verify()
        self.verifier = Verifier(self.test_id)

    def check_working_positions(self, report, expected_value):
        working_positions = report[1].get_parameters()["PositionAmountData"][9]
        position = working_positions["PosAmt"]
        self.verifier.set_event_name("Check Working Position")
        self.verifier.compare_values("Compare Position", expected_value, position)
        self.verifier.verify()
        self.verifier = Verifier(self.test_id)

    # TODO Add new fields to check
