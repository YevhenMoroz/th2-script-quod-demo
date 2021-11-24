from custom import basic_custom_actions
from test_framework.fix_wrappers.FixMessageNewOrderSingle import FixMessageNewOrderSingle
from test_framework.fix_wrappers.FixMessageOrderCancelReplaceRequest import FixMessageOrderCancelReplaceRequest


class FixMessageOrderCancelReplaceRequestAlgo(FixMessageOrderCancelReplaceRequest):

    def __init__(self, parameters: dict = None):
        super().__init__()
        super().change_parameters(parameters)

    def set_amend_params(self, new_order_single: FixMessageNewOrderSingle = None):
        amend_params = dict()
        for param in new_order_single.get_parameters():
            amend_params.update(param)
        amend_params.update(dict(OrigClOrdID=new_order_single.get_parameter("ClOrdID")))
        amend_params.update(ClOrdID=basic_custom_actions.client_orderid(9))
        return self
