from test_framework.data_sets.base_data_set import BaseDataSet
from test_framework.java_api_wrappers.ors_messages.DFDManagementBatch import DFDManagementBatch


class DFDManagementBatchOMS(DFDManagementBatch):
    def __init__(self, data_set: BaseDataSet, parameters: dict = None):
        super().__init__()
        self.change_parameters(parameters)
        self.data_set = data_set
        self.base_parameters = {
            'SEND_SUBJECT': 'QUOD.ORS.FE',
            'REPLY_SUBJECT': 'QUOD.FE.ORS',
            'DFDManagementBatchBlock': {
                "DFDOrderList": {"DFDOrderBlock":
                                     [{"OrdID": "*"}]
                                 },
                "SetDoneForDay": "Y"
            }
        }

    def set_default_complete(self, ord_id):
        self.change_parameters(self.base_parameters)
        self.update_fields_in_component('DFDManagementBatchBlock',
                                        {"DFDOrderList": {"DFDOrderBlock":
                                                              [{"OrdID": ord_id}]
                                                          }})
        return self

    def set_default_uncomplete(self, ord_id):
        self.change_parameters(self.base_parameters)
        self.update_fields_in_component('DFDManagementBatchBlock',
                                        {"DFDOrderList": {"DFDOrderBlock":
                                                              [{"OrdID": ord_id}]
                                                          }, "SetDoneForDay": "N"})
        return self
