class Constants:
    class MainPage:
        MAIN_PAGE_TITLE = '//span[@class="entity-title left"][normalize-space()="Allocation Matching Profiles"]'
    
        REFRESH_PAGE_BUTTON = "//*[@data-name='refresh']"
        DOWNLOAD_PDF_BUTTON = "//*[@data-name='download']"
        
        OK_BUTTON = '//*[normalize-space()="Ok"]'
        CANCEL_BUTTON = '//*[normalize-space()="Cancel"]'
        
        MORE_ACTIONS_BUTTON = "//*[@data-name = 'more-vertical']"
        EDIT_BUTTON = "//*[@data-name = 'edit']"
        CLONE_BUTTON = "//*[@data-name = 'copy']"
        DELETE_BUTTON = "//*[@data-name = 'trash-2']"
        PIN_ROW_BUTTON = "//*[@nbtooltip ='Click to Pin Row']"
        NEW_BUTTON = '//*[normalize-space()="Allocation Matching Profiles"]//..//*[text()="New"]'
        DOWNLOAD_CSV_BUTTON = '//*[@data-name="download"]'
        DISPLAYED_ENTITY = "//*[text()='{}']"

        NAME_FILTER = '//*[@style="width: 200px; left: 0px;"]//input[@ref="eFloatingFilterText"]'

        INSTRUMENT_COLUMN = '//*[@col-id="matchListingID"]'
        CLIENT_COLUMN = '//*[@col-id="matchAccountGroupID"]'
        QUANTITY_COLUMN = '//*[@col-id="matchQty"]'
        AVG_PRICE_COLUMN = '//*[@col-id="matchAvgPx"]'
        CURRENCY_COLUMN = '//*[@col-id="matchCurrency"]'
        SIDE_COLUMN = '//*[@col-id="matchSide"]'

    class Wizard:
        SAVE_CHANGES_BUTTON = "//*[text()='Save Changes']"
        CLEAR_CHANGES_BUTTON = "//*[text()='Clear Changes']"
        CLOSE_WIZARD = "//*[@data-name='close']"
        REVERT_CHANGES = "//*[text()='Revert Changes']"
        OK_BUTTON = '//*[text()="Ok"]'
        CANCEL_BUTTON = '//*[text()="Cancel"]'
        INCORRECT_OR_MISSING_VALUES = "//*[text()='Incorrect or missing values']"
    # Wizard

    WIZARD_FIX_MATCHING_PROFILE_NAME = '//*[@formcontrolname="blockMatchingProfileName"]'
    WIZARD_AVG_PRICE_PRECISION  = '//*[@formcontrolname="avgPxPrecision"]'
    WIZARD_GROSS_TOLERANCE  = '//*[@formcontrolname="grossTradeAmtTolerance"]'
    WIZARD_NET_TOLERANCE  = '//*[@formcontrolname="netMoneyTolerance"]'
    WIZARD_TOLERANCE_CURRENCY  = '//*[@id="grossTradeAmtToleranceCurr"]'
    WIZARD_NET_TOLERANCE_CURRENCY  = '//*[@id="netMoneyToleranceCurr"]'


    WIZARD_GROSS_AMOUNT_CHECKBOX = '//*[text()="Gross Amount"]/preceding-sibling::span'
    WIZARD_NET_AMOUNT_CHECKBOX = '//*[text()="Net Amount"]/preceding-sibling::span'
    WIZARD_SETTL_AMOUNT_CHECKBOX = '//*[text()="Settl Amount"]/preceding-sibling::span'
    WIZARD_CLIENT_LEI_CHECKBOX = '//*[text()="Client LEI"]/preceding-sibling::span'
    WIZARD_SETTL_DATE_CHECKBOX = '//*[text()="Settl Date"]/preceding-sibling::span'
    WIZARD_CLIENT_BIC_CHECKBOX = '//*[text()="Client BIC"]/preceding-sibling::span'
    WIZARD_CLIENT_COMMISSION_CHECKBOX = '//*[text()="Client Commission"]/preceding-sibling::span'
    WIZARD_TRADE_DATE_CHECKBOX = '//*[text()="Trade Date"]/preceding-sibling::span'















