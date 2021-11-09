from quod_qa.win_gui_wrappers.base_window import BaseWindow
from stubs import Stubs
from win_gui_modules.middle_office_wrappers import ModifyTicketDetails
from win_gui_modules.utils import call


class BaseMiddleOfficeBook(BaseWindow):
    # region Base constructor
    def __init__(self, case_id, base_request):
        super().__init__(case_id, base_request)
        # Need to override
        self.order_info = None
        self.order_details = None
        self.modify_ticket_details = None #ModifyTicketDetails()
        self.book_order_call = None #Stubs.win_act_middle_office_service.bookOrder

    # endregion
    # region Get
    def check_booking_toggle_manual(self):
        modify_request = self.modify_ticket_details.set_default_params(self.base_request)
        modify_request.add_commissions_details()
        extraction_details = modify_request.add_extraction_details()
        extraction_details.set_extraction_id("BookExtractionId")
        extraction_details.extract_manual_checkbox_state("book.manualCheckboxState")
        return call(self.book_order_call, modify_request.build())

    # endregion
    # region Set
    def set_modify_ticket_details(self, client=None, trade_date=None, agreed_price=None, net_gross_ind=None,
                                  give_up_broker=None, selected_row_count=None, comm_basis=None, comm_rate=None,
                                  remove_comm=False,fee_type=None, fee_basis=None, fee_rate=None, fee_category=None,
                                  remove_fee=False,settl_type=None, settl_date=None, settl_amount=None,
                                  settl_currency=None, misc_trade_date=None, bo_fields: list = None):
        if selected_row_count is not None:
            self.modify_ticket_details.set_selected_row_count(selected_row_count)
        ticket_details = self.modify_ticket_details.add_ticket_details()
        if client is not None:
            ticket_details.set_client(client)
        if trade_date is not None:
            ticket_details.set_trade_date(trade_date)
        if agreed_price is not None:
            ticket_details.set_agreed_price(agreed_price)
        if net_gross_ind is not None:
            ticket_details.set_net_gross_ind(net_gross_ind)
        if give_up_broker is not None:
            ticket_details.set_give_up_broker(give_up_broker)
        commission_details = self.modify_ticket_details.add_commissions_details()
        if comm_basis or comm_rate is not None:
            response = self.check_booking_toggle_manual()
            if response['book.manualCheckboxState'] == 'unchecked':
                commission_details.toggle_manual()
            commission_details.add_commission(comm_basis, comm_rate)
        if remove_comm:
            commission_details.remove_commissions()
        fees_details = self.modify_ticket_details.add_fees_details()
        if fee_type or fee_basis or fee_rate or fee_category is not None:
            fees_details.add_fees(fee_type, fee_basis, fee_rate, category=fee_category)
        if remove_fee:
            fees_details.remove_fees()
        settlement_details = self.modify_ticket_details.add_settlement_details()
        if settl_type is not None:
            settlement_details.set_settlement_type(settl_type)
        if settl_date is not None:
            settlement_details.set_settlement_date(settl_date)
        if settl_amount is not None:
            settlement_details.set_settlement_amount(settl_amount)
        if settl_currency is not None:
            settlement_details.set_settlement_currency(settl_currency)
        if misc_trade_date or bo_fields is not None:
            misc_details = self.modify_ticket_details.add_misc_details()
            if misc_trade_date is not None:
                misc_details.set_trade_type(misc_trade_date)
            if bo_fields is not None:
                i = 0
                for field in bo_fields:
                    i += 1
                    getattr(misc_details, "set_bo_field_" + str(i))(field)

    # endregion
    # region Action
    # endregion
