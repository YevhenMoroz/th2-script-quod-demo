from stubs import Stubs
from test_framework.win_gui_wrappers.base_bag_order_book import BaseBagOrderBook
from win_gui_modules.bag_order_ticket import BagOrderTicketDetails, PegsOrdDetails, SubLevelDetails, BagOrderInfo, \
    GetOrderBagBookDetailsRequest, OrderBagWaveCreationDetails, ExtractionBagFieldsDetails, ExtractionBagOrderAction, \
    GetOrderBagBookDetails, OrderBagCreationDetails


class OMSBagOrderBook(BaseBagOrderBook):
    def __init__(self, case_id, session_id):
        super().__init__(case_id, session_id)
        self.bag_wave_creation = OrderBagWaveCreationDetails(self.base_request)
        self.bag_book_details = BagOrderTicketDetails()
        self.pegs_details = PegsOrdDetails()
        self.sub_level_details = SubLevelDetails()
        self.bag_order_details = GetOrderBagBookDetails()
        self.extraction_bag_fields_details = ExtractionBagFieldsDetails
        self.bag_order_info = BagOrderInfo
        self.extraction_bag_order_action_static = ExtractionBagOrderAction
        self.extraction_bag_order_action = ExtractionBagOrderAction()
        self.get_order_bag_book_details_request = GetOrderBagBookDetails
        self.wave_bag_creation_call = Stubs.win_act_bag_management_service.waveBagCreation
        self.modify_wave_bag_call = Stubs.win_act_bag_management_service.orderBagWaveModification
        self.order_bag_wave_extraction_call = Stubs.win_act_bag_management_service.orderBagWaveExtraction
        self.order_bag_creation_details = OrderBagCreationDetails(self.base_request)
        self.order_bag_creation_call = Stubs.win_act_bag_management_service.splitBagByQtyPriority
        self.order_bag_extraction_call = Stubs.win_act_bag_management_service.orderBagBookExtraction
