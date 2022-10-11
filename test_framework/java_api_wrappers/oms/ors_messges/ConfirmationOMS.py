from datetime import datetime

from test_framework.data_sets.base_data_set import BaseDataSet
from test_framework.java_api_wrappers.ors_messages.Confirmation import Confirmation


class ConfirmationOMS(Confirmation):
    def __init__(self, data_set: BaseDataSet, parameters: dict = None):
        super().__init__()
        self.change_parameters(parameters)
        self.data_set = data_set
        self.base_parameters = {
            'SEND_SUBJECT': 'QUOD.ORS.ALLOC.FE',
            'REPLY_SUBJECT': 'QUOD.FE.ORS',
            "ConfirmationBlock": {
                "ConfirmationID": "0",
                "AllocInstructionID": "*",
                "AllocAccountID": data_set.get_account_by_name('client_pt_1_acc_1'),
                "InstrID": data_set.get_instrument_id_by_name("instrument_1"),
                "ConfirmTransType": "NEW",
                "ConfirmType": "CON",
                "TradeDate": datetime.utcnow().isoformat(),
                "AllocQty": "100",
                "Side": "B",
                "AvgPx": "10",
                "NetMoney": "0",
                "SettlementModelID": "1",
                "SettlLocationID": "2",
            }}

    def set_default_allocation(self, alloc_id):
        self.change_parameters(self.base_parameters)
        self.update_fields_in_component('ConfirmationBlock',
                                        {"AllocInstructionID": alloc_id})
        return self
