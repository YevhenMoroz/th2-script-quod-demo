from stubs import Stubs
from test_framework.win_gui_wrappers.base_bag_order_book import BaseBagOrderBook
from win_gui_modules.bag_order_ticket import BagOrderTicketDetails, PegsOrdDetails, SubLevelDetails, BagOrderInfo, \
    OrderBagWaveCreationDetails, ExtractionBagFieldsDetails, ExtractionBagOrderAction, \
    GetOrderBagBookDetails, OrderBagCreationDetails, OrderBagCompleteDetails, CreateOrderDetails, \
    ModifySubLevelBagOrderDetails, ExtractWaveTicketValuesRequest, ScenarioDetails


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
        self.order_bag_extraction_call = Stubs.win_act_bag_management_service.orderBagBookExtraction
        self.order_bag_modification_call = Stubs.win_act_bag_management_service.modifyBag
        self.order_bag_cancel_bag_call = Stubs.win_act_bag_management_service.cancelBag
        self.order_bag_dissociate_bag_call = Stubs.win_act_bag_management_service.dissociateBag
        self.order_bag_complete_details = OrderBagCompleteDetails(self.base_request)
        self.order_bag_complete_call = Stubs.win_act_bag_management_service.completeBag
        self.order_bag_uncomplete_call = Stubs.win_act_bag_management_service.uncompleteBag
        self.order_bag_book_call = Stubs.win_act_bag_management_service.bookBagOrder
        self.create_order_call = Stubs.win_act_bag_management_service.createOrder
        self.create_order_details = CreateOrderDetails(self.base_request)
        self.modify_sub_level_order_details = ModifySubLevelBagOrderDetails(self.base_request)
        self.modify_sub_level_order_call = Stubs.win_act_bag_management_service.modifySubOrderFromBag
        self.extract_wave_ticket_values_request = ExtractWaveTicketValuesRequest(self.base_request)
        self.extract_wave_ticket_values_call = Stubs.win_act_bag_management_service.extractFieldsFromWaveTicket
        self.cancel_wave_call = Stubs.win_act_bag_management_service.cancelWave
        self.scanario_details = ScenarioDetails()
