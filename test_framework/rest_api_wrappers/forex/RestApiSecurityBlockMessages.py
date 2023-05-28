from test_framework.data_sets.message_types import ResAPIMessageType
from test_framework.rest_api_wrappers.RestApiMessages import RestApiMessages


class RestApiSecurityBlockMessages(RestApiMessages):

    def find_security_block(self, instr_id):
        self.clear_message_params()
        self.message_type = 'FindSecurityBlock'
        self.parameters = {
            'URI':
                {
                    'queryID': instr_id
                }
        }
        return self

    def manage_security_block(self):
        self.message_type = ResAPIMessageType.ManageSecurityBlock.value
        return self
