from custom.verifier import Verifier


class PositionVerifier:

    def __init__(self, test_id):
        self.test_id = test_id
        self.verifier = Verifier(test_id)

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
        expected_value = self.calculate_quote_position(qty, price)
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

    def calculate_quote_position(self, qty, price):
        quote_pos = float(qty) * float(price)
        if str(quote_pos).endswith(".0"):
            return str(quote_pos)[:-2]
        else:
            return str(round(quote_pos, 3))

    def calculate_quote_after_trade(self, qty, trade_px, trade_qty, avg_px):
        leaves_qty = float(qty) - float(trade_qty)
        pos = self.calculate_quote_position(qty, trade_px)
        quote_pos = float(pos) - float(trade_qty) * float(avg_px) - leaves_qty * float(trade_px)
        if str(quote_pos).endswith(".0"):
            return str(quote_pos)[:-2]
        else:
            return str(round(quote_pos, 3))

    def find_position_report_by_type(self, report, type):
        position_report_list = report.get_parameter('PositionAmountData')
        for position_report in position_report_list:
            if position_report["PosAmtType"] == type:
                return position_report.get("PosAmt")
            print("Position report with type {} not found".format(type))
            return None

    def count_position_change(self, old_position, new_position, expected_change, account):
        actual_change = int(new_position) - int(old_position)
        self.verifier.set_event_name("Check Position Change of {}".format(account))
        self.verifier.compare_values("Compare Base", str(expected_change), str(actual_change))
        self.verifier.verify()
        self.verifier = Verifier(self.test_id)


