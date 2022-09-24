class MarketConstants:

    MENU_BUTTON = '//android.widget.FrameLayout/android.view.View/android.view.View/android.view.View/android.view.View/android.view.View[1]/android.view.View'

    MARKET_TITLE = '(//*[@content-desc = "Market"])[1]'
    MARKET_PLUS_BUTTON_X = 315
    MARKET_PLUS_BUTTON_Y = 135
    WATCHLIST_NAME_START='//*[contains(@content-desc, "'
    WATCHLIST_NAME_END = '")]'
    NO_WATCHLISTS = '//*[contains(@content-desc,"No Watchlists") and contains(@content-desc, "Add your favourite stocks and check here easily")]'
    MARKET_SEARCH_FIELD = "//android.widget.EditText[contains(@text, 'Search')]"

    # Search
    SEARCH_FIELD = "//*[contains(@text, 'Search ex: info base, nifty fut')]"
    SEARCH_CLEAR_BUTTON = "//android.view.View[1]/android.widget.EditText"
    SEARCH_BACK_BUTTON = "//android.view.View[1]/android.view.View"
    INSTRUMENT_START = '//*[contains(@content-desc, "'
    INSTRUMENT_END = '")]'
    # endregion