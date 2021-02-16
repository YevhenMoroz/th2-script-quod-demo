from custom import basic_custom_actions as bca


class FixMessage:

    def __init__(self, parameters=''):
        self.parameters = parameters

    def get_ClOrdID(self):
        return self.parameters['parameters']

    def get_parameters(self):
        return self.parameters

    def add_tag(self, parameter):
        self.parameters.update(parameter)

    def remove_tag(self, parameter_name):
        self.parameters.popitem(parameter_name)

    def get_ClOrdID(self):
        return self.parameters['ClOrdID']

    def add_random_ClOrdID(self):
        self.parameters.update({'ClOrdID': bca.client_orderid(9)})

