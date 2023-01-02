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

    def set_default_book(self, ord_id):
        self.change_parameters(self.base_parameters)
        self.update_fields_in_component('AllocationInstructionBlock',
                                        {"OrdAllocList": {"OrdAllocBlock": [{"OrdID": ord_id}]}})
        return self

    def set_amend_book(self, alloc_instr_id, exec_id, exec_qty, exec_price):
        self.change_parameters(self.base_parameters)
        self.update_fields_in_component('AllocationInstructionBlock',
                                        {'ExecAllocList': {'ExecAllocBlock': [{"ExecQty": exec_qty,
                                                                               'ExecID': exec_id,
                                                                               'ExecPrice': exec_price}]},
                                         'AllocInstructionID': alloc_instr_id, 'AllocTransType': 'R', 'AllocType': "P"})

        return self

    def set_ament_book_with_multiply_execution(self, alloc_instr_id, exec_ids: list, exec_qty, exec_price):
        self.change_parameters(self.base_parameters)
        list_of_exec_alloc_block = []
        for exec_id in exec_ids:
            list_of_exec_alloc_block.append({"ExecQty": exec_qty,
                                             'ExecID': exec_id,
                                             'ExecPrice': exec_price})
        self.update_fields_in_component('AllocationInstructionBlock',
                                        {'ExecAllocList': {'ExecAllocBlock': list_of_exec_alloc_block},
                                         'AllocInstructionID': alloc_instr_id, 'AllocTransType': 'R', 'AllocType': "P"})

