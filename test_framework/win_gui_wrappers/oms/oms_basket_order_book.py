from th2_grpc_act_gui_quod.basket_ticket_pb2 import ImportedFileMappingField

from test_framework.win_gui_wrappers.base_basket_order_book import BaseBasketOrderBook
from stubs import Stubs
from win_gui_modules import basket_order_book_wrappers
from win_gui_modules.basket_order_book_wrappers import ExtractOrderDataDetails, RemoveChildOrderFromBasketDetails, \
    ExtractChildOrderDataDetails, BasketWaveRowDetails, WaveBasketDetails
from win_gui_modules.basket_ticket_wrappers import TemplatesDetails, FileDetails, RowDetails, BasketTicketDetails, \
    ExtractTemplateDetails
from win_gui_modules.common_wrappers import SimpleRequest


class OMSBasketOrderBook(BaseBasketOrderBook):
    # region Base constructor
    def __init__(self, case_id, session_id):
        super().__init__(case_id, session_id)
        self.imported_file_mapping_field_details = ImportedFileMappingField
        self.templates_details = TemplatesDetails()
        self.row_details = RowDetails()
        self.file_details = FileDetails
        self.simple_request = SimpleRequest()
        self.extract_order_data_details = ExtractOrderDataDetails
        self.remove_from_basket_details = RemoveChildOrderFromBasketDetails
        self.extract_basket_data_details = basket_order_book_wrappers.ExtractOrderDataDetails()
        self.extract_basket_order_details = basket_order_book_wrappers.ExtractChildOrderDataDetails
        self.basket_ticket_details = BasketTicketDetails()
        self.extract_template_details = ExtractTemplateDetails()
        self.extract_child_details = ExtractChildOrderDataDetails
        self.manage_templates_call = Stubs.win_act_basket_ticket.manageTemplates
        self.extract_template_data_call = Stubs.win_act_basket_ticket.extractTemplateData
        self.remove_template_call = Stubs.win_act_basket_ticket.removeTemplate
        self.create_basket_via_import_call = Stubs.win_act_basket_ticket.createBasketViaImport
        self.complete_basket_call = Stubs.win_act_basket_order_book.complete
        self.uncomplete_basket_call = Stubs.win_act_basket_order_book.uncomplete
        self.book_basket_call = Stubs.win_act_basket_order_book.book
        self.cancel_basket_call = Stubs.win_act_basket_order_book.cancelBasket
        self.remove_from_basket_call = Stubs.win_act_basket_order_book.removeChildOrderFromBasket
        self.extract_basket_data_call = Stubs.win_act_basket_order_book.extractOrderData
        self.extract_child_order_data_call = Stubs.win_act_basket_order_book.extractChildOrderData
        self.extract_basket_data_details_call = Stubs.win_act_basket_order_book.extractOrderData
        self.extract_basket_order_details_call = Stubs.win_act_basket_order_book.extractChildOrderData
        self.basket_wave_row_details = BasketWaveRowDetails()
        self.wave_basket_details = WaveBasketDetails(self.base_request)
        self.wave_basket_call = Stubs.win_act_basket_order_book.waveBasket
    # endregion