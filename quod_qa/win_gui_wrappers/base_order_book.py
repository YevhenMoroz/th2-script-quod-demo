from quod_qa.win_gui_wrappers.base_window import BaseWindow
from stubs import Stubs
from win_gui_modules.order_book_wrappers import ExtractionDetail, ExtractionAction, OrderInfo, \
    OrdersDetails
from win_gui_modules.utils import call


class BaseOrderBook(BaseWindow):
    def __init__(self, case_id, base_request):
        super().__init__(case_id, base_request)
        # Need to override
        self.order_details = None
        self.order_info = None
        self.grpc_call = None

    def set_order_details(self):
        self.order_details.set_extraction_id(self.extraction_id)
        self.order_details.set_default_params(base_request=self.base_request)

    def set_filter(self, filter_list: list):
        """
        Receives list as an argument, where the elements
        are in order - key, value, key, value, ...
        For example ["Qty", "123456", "Owner", "QA1", etc]
        """
        self.order_details.set_filter(filter_list)
        return self

    def check_order_filled(self, expected_sts, expected_exec_sts):
        sts = ExtractionDetail("orderBook.Sts", "Sts")
        exec_sts = ExtractionDetail("orderBook.ExecSts", "ExecSts")
        self.order_details.add_single_order_info(
            self.order_info.create(
                action=ExtractionAction.create_extraction_action(extraction_details=[sts, exec_sts])
            )
        )
        response = call(self.grpc_call, self.order_details.request())
        self.verifier.set_event_name("Check Order Book")
        self.verifier.compare_values("Status", expected_sts, response[sts.name])
        self.verifier.compare_values("Exec Status", expected_exec_sts, response[exec_sts.name])
        self.verifier.verify()
