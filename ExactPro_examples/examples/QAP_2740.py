from utils.base_test import BaseTest
from utils.order_book_wrappers import Criterion, OrderAnalysisAction, OrderInfo, \
    OrdersDetails
from utils.services import Services
from utils.wrappers import *


class QAP_2740(BaseTest):

    def __init__(self, services: Services, parent_event):
        super().__init__(services)
        self.create_test_event(parent_event,
                               "QAP_2740", "[SORPING] Send SORPING algo order to check PriceCost criteria in "
                                           "Aggressive phase")

    def execute(self):
        call = self.call
        set_base(self._session_id, self._event_id)

        order_book_service = self._services.order_book_service

        venue = "EURONEXT PARIS"
        order_id = "AO1201228154725160001"

        # create criterion
        criterion = Criterion()
        criterion.set_column_name("PriceCost")
        criterion.minimize()

        # create child order
        verify_generated_order_event_action = OrderAnalysisAction.create_verify_generate_order_event(venue, criterion)
        child_order_info = OrderInfo.create(action=verify_generated_order_event_action)
        child_order = OrdersDetails.create(info=child_order_info)

        # create main order
        main_order = OrdersDetails()
        main_order.set_default_params(self.get_base_request())
        main_order.set_filter(["Order ID", order_id])
        main_order.set_extraction_id("TestExtraction")

        main_order_info = OrderInfo()
        main_order_info.set_sub_orders_details(child_order)
        main_order.add_single_order_info(main_order_info)

        call(order_book_service.getOrdersDetails, main_order.request())
