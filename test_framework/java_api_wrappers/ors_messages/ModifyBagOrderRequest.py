from test_framework.data_sets.message_types import ORSMessageType
from test_framework.java_api_wrappers.JavaApiMessage import JavaApiMessage


class ModifyBagOrderRequest(JavaApiMessage):

    def __init__(self, parameters: dict = None):
        super().__init__(message_type=ORSMessageType.OrderBagModificationRequest.value)
        super().change_parameters(parameters)

    def set_default(self, order_bag_id, price: str, bag_name: str) -> None:
        base_parameters = {
            'SEND_SUBJECT': 'QUOD.ORS.FE',
            'REPLY_SUBJECT': 'QUOD.FE.ORS',
            'OrderBagModificationRequestBlock': {
                'OrderBagOrderList': {
                    'OrderBagOrderBlock': [

                    ]
                },
                'OrderBagID': order_bag_id,
                'Price': price,
                'OrderBagName': bag_name
            }
        }
        super().change_parameters(base_parameters)

    def add_components_into_repeating_group(self, component_name: str, name_of_repeating_group: str,
                                            name_of_component_into_repeating_group: str,
                                            values_of_repeating_group: list):
        parameters = self.get_parameters()
        for keys_of_component in parameters.keys():
            if type(parameters[keys_of_component]) is dict:
                for value in range(len(values_of_repeating_group)):
                    if parameters[keys_of_component][component_name][name_of_repeating_group] is None:
                        parameters[keys_of_component][component_name][name_of_repeating_group] = []
                    parameters[keys_of_component][component_name][name_of_repeating_group].append({name_of_component_into_repeating_group:values_of_repeating_group[value]})
        super().change_parameters(parameters)
