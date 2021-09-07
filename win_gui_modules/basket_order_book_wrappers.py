from th2_grpc_act_gui_quod import basket_book_pb2


class ExtractOrderDataDetails:
    def __init__(self):
        self._request = basket_book_pb2.ExtractOrderDataDetails()

    def set_default_params(self, base_request):
        self._request.base.CopyFrom(base_request)

    def set_filter(self, filter: dict):
        self._request.filter.update(filter)

    def set_column_name(self, column_names: list):
        for name in column_names:
            self._request.basketOrderBookColumnName.append(name)

    def build(self):
        return self._request

 # enum value:
    #
    #   ID
    #   EXEC_POLICY
    #   STATUS
    #   EXEC_STATUS
    #   LIST_EXEC_INST_TYPE
    #   CREAT_DAY
    #   CREAT_HOUR
    #   TERMINATION_TIME
    #   CL_ORD_LIST_ID
    #   OWNER
    #   LIST_QTY
    #   ORD_TYPE
    #   TIME_IN_FORCE
    #   DELTA_PRICE
    #   DELTA_UNIT
    #   PRICE_REFERENCE
    #   DELTA_STOP_PRICE
    #   DELTA_STOP_UNIT
    #   STOP_PRICE_REFERENCE
    #   BASKET_NAME
    #   BASKET_TMPL_NAME
    #   BASKET_TMPL_DESC
    #   EXEC_TMPL_NAME
    #   ACCOUNT_ALLOC
    #   PROGRESS
    #
    #   example : BasketOrderBookColumnName.ID