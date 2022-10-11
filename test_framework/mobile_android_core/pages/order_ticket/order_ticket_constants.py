
class OrderTicketConstants:

    # region OrderTicket label
    ARROW_BACK = '//android.widget.Button[1]'
    ORDER_TICKET_TITLE = '//android.view.View[contains(@content-desc, "Order Ticket")]'

    # region Side
    SIDE_BUY = '//android.view.View[@content-desc="Buy"]'
    SIDE_SELL = '//android.view.View[@content-desc="Sell"]'
    # endregion

    # region Instrument
    INSTRUMENT_SEARCH_BUTTON = ''
    INSTRUMENT_SELECTED = ''
    INSTRUMENT_EDIT_ARROW_BACK = ''
    INSTRUMENT_EDIT_TEXT = ''
    INSTRUMENT_EDIT_SYMBOL = ''
    # endregion

    # region Security Account
    SECURITY_ACCOUNT = '//android.widget.Button[@content-desc="HAKKIM3"]'
    # endregion

    # region Cash Account
    CASH_ACCOUNT_EMPTY = '//android.view.View[@content-desc="Order Ticket Security Account Cash Account Quantity Price Order Type Time In Force"]/android.widget.Button[3]'
    CASH_ACCOUNT_VALUE = '//android.view.View[@content-desc="test_cash_account"]' # ?
    # endregion
