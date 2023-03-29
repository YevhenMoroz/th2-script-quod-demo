from test_framework.data_sets.base_data_set import BaseDataSet
from test_framework.java_api_wrappers.ors_messages.PositionTransferInstruction import PositionTransferInstruction


class PositionTransferInstructionOMS(PositionTransferInstruction):
    def __init__(self, data_set: BaseDataSet, parameters: dict = None):
        super().__init__(parameters)
        self.data_set = data_set
        self.base_parameters: dict = {
            'SEND_SUBJECT': 'QUOD.ORS.FE',
            'REPLY_SUBJECT': 'QUOD.FE.ORS',
        }

    def set_default_transfer(self, source_account, destination_account, qty_to_transfer,
                             clearing_trade_price=None) -> None:
        if clearing_trade_price is None:
            clearing_trade_price = '20'
        base_parameters = {
            'PositionTransferInstructionBlock': {
                'TransferTransType': 'NEW',
                'InstrID': self.data_set.get_instrument_id_by_name('instrument_2'),
                'PositionType': 'N',
                'SourceAccountID': source_account,
                'DestinationAccountID': destination_account,
                'QtyToTransfer': qty_to_transfer,
                'ClearingTradePrice': clearing_trade_price
            }
        }
        base_parameters.update(self.base_parameters)
        super().change_parameters(base_parameters)

    def set_default_amend_transfer(self, source_account, destination_account, trans_id, qty_to_transfer,
                                   clearing_trade_price=None):
        if clearing_trade_price is None:
            clearing_trade_price = '20'
        base_parameters = {
            'PositionTransferInstructionBlock': {
                'TransferTransType': 'REP',
                'InstrID': self.data_set.get_instrument_id_by_name('instrument_2'),
                'PositionType': 'N',
                'SourceAccountID': source_account,
                'PositionTransferID': trans_id,
                'DestinationAccountID': destination_account,
                'QtyToTransfer': qty_to_transfer,
                'ClearingTradePrice': clearing_trade_price
            }
        }
        base_parameters.update(self.base_parameters)
        super().change_parameters(base_parameters)
