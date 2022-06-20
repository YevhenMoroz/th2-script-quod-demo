
class OrderTicketConstants:

    # region OrderTicket label
    ARROW_BACK = '//android.view.View[@content-desc="Order Ticket Security Account Cash Account Quantity Price Order Type Time In Force"]/android.widget.Button[1]'
    # endregion

    # region Side
    SIDE_BUY = '//android.view.View[@content-desc="Buy"]'
    SIDE_SELL = '//android.view.View[@content-desc="Sell"]'
    # endregion

    # region Instrument
    INSTRUMENT_SEARCH_BUTTON = '//android.view.View[@content-desc="Instrument not selected, use search to find it."]'
    INSTRUMENT_SELECTED = ''
    INSTRUMENT_EDIT_ARROW_BACK = '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.View/android.view.View/android.view.View/android.view.View/android.view.View/android.view.View'
    INSTRUMENT_EDIT_TEXT = '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.View/android.view.View/android.view.View/android.view.View/android.view.View/android.widget.EditText'
    INSTRUMENT_EDIT_SYMBOL = '//android.view.View[@content-desc="TCS-IQ[NSE] TCS-IQ"]' # ?
    # endregion

    # region Security Account
    SECURITY_ACCOUNT = '//android.widget.Button[@content-desc="HAKKIM3"]'
    # endregion

    # region Cash Account
    CASH_ACCOUNT_EMPTY = '//android.view.View[@content-desc="Order Ticket Security Account Cash Account Quantity Price Order Type Time In Force"]/android.widget.Button[3]'
    CASH_ACCOUNT_VALUE = '//android.view.View[@content-desc="test_cash_account"]' # ?
    # endregion
