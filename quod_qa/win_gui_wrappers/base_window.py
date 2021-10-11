from custom import basic_custom_actions as bca
from custom.verifier import Verifier


class BaseWindow:
    def __init__(self, case_id, base_request):
        self.case_id = case_id
        self.base_request = base_request
        self.extraction_id = bca.client_orderid(4)
        self.verifier = Verifier(self.case_id)
