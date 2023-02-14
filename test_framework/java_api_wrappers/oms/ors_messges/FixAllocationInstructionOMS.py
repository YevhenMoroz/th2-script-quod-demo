from datetime import datetime

from custom import basic_custom_actions
from test_framework.data_sets.base_data_set import BaseDataSet
from test_framework.java_api_wrappers.ors_messages.FixAllocationInstruction import FixAllocationInstruction


class FixAllocationInstructionOMS(FixAllocationInstruction):
    def __init__(self, data_set: BaseDataSet, parameters: dict = None):
        super().__init__()
        self.change_parameters(parameters)
        self.data_set = data_set
        self.base_parameters = {
            'SEND_SUBJECT': 'QUOD.FIX_REPLY.gtwbo',
            # 'REPLY_SUBJECT': 'QUOD.FIX_REPLY.gtwquod4',
            "AllocationInstructionBlock": {
                "OrdAllocList": {
                    "OrdAllocBlock": [{"OrdID": "*"}]},
                "AllocInstructionMiscBlock": {
                    "AllocInstructionMisc0": "BOC1",
                    "AllocInstructionMisc1": "BOC2",
                    "AllocInstructionMisc2": "BOC3",
                    "AllocInstructionMisc3": "BOC4",
                    "AllocInstructionMisc4": "BOC5"},
                "ClientAllocID": basic_custom_actions.client_orderid(9),
                "AllocTransType": "New",
                "AllocType": "Preliminary",
                "Side": "Buy",
                "AvgPrice": "20",
                "TransactTime":datetime.utcnow().isoformat(),
                "PositionEffect":"Open",
                "ExecQty":"100",
                "Currency": data_set.get_currency_by_name("currency_1"),
                "TradeDate": datetime.utcnow().isoformat(),
                "Qty": "100",
                "SettlDate": datetime.utcnow().isoformat(),
                "GrossTradeAmt": "2000",
                "BookingType": "RegularBooking",
                "InstrumentBlock": {"InstrSymbol": "FR0010436584_EUR",
                                    "SecurityID": "FR0010436584",
                                    "SecurityIDSource": "ISIN",
                                    "InstrType": "Equity"},
                "ClientAccountGroupID": data_set.get_client_by_name("client_pt_1"),
                "AllocAccountList": {"AllocAccountBlock": [
                    {"AllocClientAccountID": data_set.get_account_by_name('client_pt_1_acc_1'),
                     "AllocPrice": "20",
                     "AllocAvgPx": "20",
                     "AllocQty": "100",
                     # "AllocNetPrice": "20",
                     # "AllocNetMoney": "100"
                     }]}
            }}

    def set_default_book(self, ord_id):
        self.change_parameters(self.base_parameters)
        self.update_fields_in_component('AllocationInstructionBlock',
                                        {"OrdAllocList": {"OrdAllocBlock": [{"ClOrdID": ord_id}]}})
        return self
