from dataclasses import dataclass
from datetime import datetime
from test_framework.java_api_wrappers.ors_messages.MassConfirmation import MassConfirmation


@dataclass
class ConfirmationInstance:
    alloc_account_id: str
    alloc_instruction_id: str
    instrument_id: str
    alloc_qty: str
    net_money: str
    avg_px: str


class MassConfirmationOMS(MassConfirmation):

    def __init__(self, parameters: dict = None):
        super().__init__(parameters)
        super().change_parameters(parameters)
        self.__list_of_main_information_of_confirmation_instance = []
        self.__list_of_full_information_confirmation_instance = []

    def set_instance_of_confirmation_list(self, alloc_instruction_id, alloc_account_id, instrument_id, alloc_qty,
                                          net_money, avg_px):
        self.__list_of_main_information_of_confirmation_instance.append(
            ConfirmationInstance(alloc_account_id, alloc_instruction_id, instrument_id, alloc_qty, net_money, avg_px))

    def set_default_confimations_new(self) -> None:
        for instance in self.__list_of_main_information_of_confirmation_instance:
            self.__list_of_full_information_confirmation_instance.append(
                {"ConfirmationID": "0",
                 "AllocInstructionID": instance.alloc_instruction_id,
                 "AllocAccountID": instance.alloc_account_id,
                 "InstrID": instance.instrument_id,
                 "ConfirmTransType": "NEW",
                 "ConfirmType": "CON",
                 "Side": "Buy",
                 "TradeDate": datetime.utcnow().isoformat(),
                 'AllocQty': instance.alloc_qty,
                 'NetMoney': instance.net_money,
                 'AvgPx': instance.avg_px}
            )
        base_parameters = {
            'SEND_SUBJECT': 'QUOD.ORS.ALLOC.FE',
            'REPLY_SUBJECT': 'QUOD.FE.ORS',
            "MassConfirmationBlock": {
                'ConfirmationList': {'ConfirmationBlock': self.__list_of_full_information_confirmation_instance}}}
        super().change_parameters(base_parameters)
