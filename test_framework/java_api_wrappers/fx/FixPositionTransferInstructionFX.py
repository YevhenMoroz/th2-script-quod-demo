from test_framework.data_sets.base_data_set import BaseDataSet
from test_framework.data_sets.fx_data_set.fx_data_set import FxDataSet
from test_framework.data_sets.message_types import ORSMessageType
from test_framework.java_api_wrappers.JavaApiMessage import JavaApiMessage
from custom import basic_custom_actions as bca


class FixPositionTransferInstructionFX(JavaApiMessage):
    def __init__(self, parameters: dict = None, data_set: BaseDataSet = FxDataSet()):
        super().__init__(message_type=ORSMessageType.FixPositionTransferInstruction.value, data_set=data_set)
        super().change_parameters(parameters)

    def set_default_params(self, source_acc, destination_acc):
        base_parameters = {
            "SEND_SUBJECT": "QUOD.ORS.FIX",
            "REPLY_SUBJECT": "QUOD.FIX.ORS",
            "PositionTransferInstructionBlock": {
                "PartiesList": {
                    "PartiesBlock": [
                        {"PartyID": source_acc,  # need set account like CLIENT1_1
                         "PartyIDSource": "Proprietary",
                         "PartyRole": "PositionAccount"}
                    ]},
                "TargetPartiesList": {
                    "TargetPartiesBlock": [
                        {"TargetPartyID": destination_acc,  # need set account like CLIENT1_1
                         "TargetPartyIDSource": "Proprietary",
                         "TargetPartyRole": "PositionAccount"}
                    ]},
                "InstrumentBlock": {
                    "InstrSymbol": self.get_data_set().get_symbol_by_name("symbol_1"),
                    "InstrType": self.get_data_set().get_fx_instr_type_ja("fx_spot")
                },
                "ExternalTransferID": bca.client_orderid(12),
                "TransferTransType": "NEW",
                "PositionType": "N",
                "QtyToTransfer": "1000000",
                "SettlDate": self.get_data_set().get_settle_date_by_name("spot_java_api"),

            }
        }
        super().change_parameters(base_parameters)
        return self

    def change_instrument(self, instrument):
        self.update_fields_in_component("PositionTransferInstructionBlock", {"InstrumentBlock": instrument})
        return self

    def change_symbol(self, symbol):
        instr_block = self.get_parameter("PositionTransferInstructionBlock")["InstrumentBlock"]
        instr_block["InstrSymbol"] = symbol
        return self

    def change_qty(self, qty):
        self.update_fields_in_component("PositionTransferInstructionBlock", {"QtyToTransfer": qty})
        return self

    def change_type_to_short(self):
        self.update_fields_in_component("PositionTransferInstructionBlock", {"PositionType": "S"})
        return self

    def change_date(self, date):
        self.update_fields_in_component("PositionTransferInstructionBlock", {"SettlDate": date})
        return self
