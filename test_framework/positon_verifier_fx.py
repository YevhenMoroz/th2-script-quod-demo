from custom.verifier import Verifier
from test_framework.data_sets.constants import PosAmtType
from test_framework.fix_wrappers.forex.FixMessagePositionReportFX import FixMessagePositionReportFX
from test_framework.position_calculation_manager import PositionCalculationManager


class PositionVerifier:

    def __init__(self, test_id):
        self.test_id = test_id
        self.verifier = Verifier(test_id)
        self.pos_calc = PositionCalculationManager()

    def check_base_position(self, report, expected_value, text="Check Base Position"):
        amount = self.get_amount(report, PosAmtType.BasePosition)
        self.verifier.set_event_name(text)
        self.verifier.compare_values("Compare Base", expected_value, amount)
        self.verifier.verify()
        self.verifier = Verifier(self.test_id)

    def check_avg_price(self, report, expected_value):
        amount = self.get_amount(report, PosAmtType.AvgPX)
        self.verifier.set_event_name("Check Avg Price")
        self.verifier.compare_values("Compare Avg PX", expected_value, amount)
        self.verifier.verify()
        self.verifier = Verifier(self.test_id)

    def check_quote_position_default(self, report, trade):
        qty = trade.get_exec_qty()
        price = trade.get_exec_price()
        side = trade.get_side()
        expected_value = self.pos_calc.calculate_quote_position(qty, price, side)
        amount = self.get_amount(report, PosAmtType.QuotePosition)
        self.verifier.set_event_name("Check Quote Position")
        self.verifier.compare_values("Compare Quote Position", expected_value, amount)
        self.verifier.verify()
        self.verifier = Verifier(self.test_id)

    def check_backup_after_trade(self, report: FixMessagePositionReportFX, trade_qty, trade_px):
        pass

    def check_system_cur_position(self, report, expected_value):
        amount = self.get_amount(report, PosAmtType.SysCurPosition)
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
        amount = self.get_amount(report, PosAmtType.SysQuotePosition)
        self.verifier.set_event_name("Check SysQuote Position")
        self.verifier.compare_values("Compare SysQuote Position", expected_value, amount)
        self.verifier.verify()
        self.verifier = Verifier(self.test_id)

    def check_mtm_pnl_position(self, report, trade):
        qty = trade.get_exec_qty()
        price = trade.get_exec_price()
        symbol = trade.get_symbol()
        side = trade.get_side()
        expected_value = self.pos_calc.calculate_mtm_pnl(qty, price, symbol, side)
        amount = self.get_amount(report, PosAmtType.MTMPnl)
        self.verifier.set_event_name("Check MTM Pnl Position")
        self.verifier.compare_values("Compare MTM Pnl Position", expected_value, amount)
        self.verifier.verify()
        self.verifier = Verifier(self.test_id)

    def check_system_mtm_pnl_position(self, report, trade):
        qty = trade.get_exec_qty()
        price = trade.get_exec_price()
        symbol = trade.get_symbol()
        side = trade.get_side()
        expected_value = self.pos_calc.calculate_system_mtm_pnl(qty, price, symbol, side)
        amount = self.get_amount(report, PosAmtType.SysMTMPnl)
        self.verifier.set_event_name("Check System MTM Pnl Position")
        self.verifier.compare_values("Compare System MTM Pnl Position", expected_value, amount)
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
        amount = self.get_amount(report, PosAmtType.WorkingPosition)
        self.verifier.set_event_name("Check Working Position")
        self.verifier.compare_values("Compare Position", expected_value, amount)
        self.verifier.verify()
        self.verifier = Verifier(self.test_id)

    # TODO Add new fields to check

    def get_amount(self, report, position_type: PosAmtType):
        pos_amount_date = report[1].get_parameters()
        for item in pos_amount_date["PositionAmountData"]:
            if item.get("PosAmtType") == position_type.value:
                pos_amt = item.get("PosAmt")
                if pos_amt is None:
                    raise Exception("Position Amount is None")
                else:
                    return pos_amt

    def count_position_change(self, old_position, new_position, expected_change, account):
        actual_change = int(new_position) - int(old_position)
        self.verifier.set_event_name("Check Position Change of {}".format(account))
        self.verifier.compare_values("Compare Base", str(expected_change), str(actual_change))
        self.verifier.verify()
        self.verifier = Verifier(self.test_id)
