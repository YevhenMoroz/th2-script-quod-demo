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



