from datetime import datetime

from test_framework.data_sets.base_data_set import BaseDataSet
from test_framework.java_api_wrappers.ors_messages.AllocationInstruction import AllocationInstruction


class AllocationInstructionOMS(AllocationInstruction):
    def __init__(self, data_set: BaseDataSet, parameters: dict = None):
        super().__init__()
        self.change_parameters(parameters)
        self.data_set = data_set
        self.base_parameters = {
            'SEND_SUBJECT': 'QUOD.ORS.ALLOC.FE',
            'REPLY_SUBJECT': 'QUOD.FE.ORS',
            "AllocationInstructionBlock": {
                "OrdAllocList": {
                    "OrdAllocBlock": [{"OrdID": "*"}]},
                "AllocInstructionMiscBlock": {
                    "AllocInstructionMisc0": "BOC1",
                    "AllocInstructionMisc1": "BOC2",
                    "AllocInstructionMisc2": "BOC3",
                    "AllocInstructionMisc3": "BOC4",
                    "AllocInstructionMisc4": "BOC5"},
                "AllocInstructionID": "0",
                "AllocTransType": "New",
                "AllocType": "ReadyToBook",
                "Side": "Buy",
                "Currency": data_set.get_currency_by_name("currency_1"),
                "TradeDate": datetime.utcnow().isoformat(),
                "Qty": "100",
                "SettlDate": datetime.utcnow().isoformat(),
                "GrossTradeAmt": "1000",
                "BookingType": "RegularBooking",
                "InstrID": data_set.get_instrument_id_by_name("instrument_1"),
                "AvgPx": "10",
                "AccountGroupID": data_set.get_client_by_name("client_pt_1"),
                "ErroneousTrade": "No",
                "NetGrossInd": "Gross",
                "SettlCurrAmt": "1000",
                "RecomputeInSettlCurrency": "No",
                "ComputeFeesCommissions": "No"
            }}

    def set_default_book(self, ord_id, ord_id_second=None):
        self.change_parameters(self.base_parameters)
        if ord_id_second:
            list_of_orders = [{"OrdID": ord_id}, {"OrdID": ord_id_second}]
        else:
            list_of_orders = [{"OrdID": ord_id}]
        self.update_fields_in_component('AllocationInstructionBlock',
                                        {"OrdAllocList": {"OrdAllocBlock": list_of_orders}})
        return self
