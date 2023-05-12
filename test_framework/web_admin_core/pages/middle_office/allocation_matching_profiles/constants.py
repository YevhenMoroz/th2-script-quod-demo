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
        DOWNLOAD_PDF_BUTTON = '//*[@nbtooltip="Download PDF"]//*[@data-name="download"]'
        OK_BUTTON = '//*[text()="Ok"]'
        CANCEL_BUTTON = '//*[text()="Cancel"]'
        INCORRECT_OR_MISSING_VALUES = "//*[text()='Incorrect or missing values']"

    class ValuesTab:
        NAME = '//*[@formcontrolname="blockMatchingProfileName"]'

    class MatchingFieldsTab:
        AVG_PRICE_PRECISION = '//*[@formcontrolname="avgPxPrecision"]'
        GROSS_TOLERANCE = '//*[@formcontrolname="grossTradeAmtTolerance"]'
        TOLERANCE_CURRENCY = '//*[@id="grossTradeAmtToleranceCurr"]'
        NET_TOLERANCE = '//*[@formcontrolname="netMoneyTolerance"]'
        NET_TOLERANCE_CURRENCY = '//*[@id="netMoneyToleranceCurr"]'

        GROSS_AMOUNT_CHECKBOX = '//*[normalize-space()="Gross Amount"]/preceding-sibling::span'
        NET_AMOUNT_CHECKBOX = '//*[normalize-space()="Net Amount"]/preceding-sibling::span'
        SETTL_AMOUNT_CHECKBOX = '//*[normalize-space()="Settl Amount"]/preceding-sibling::span'
        CLIENT_LEI_CHECKBOX = '//*[normalize-space()="Client LEI"]/preceding-sibling::span'
        SETTL_DATE_CHECKBOX = '//*[normalize-space()="Settl Date"]/preceding-sibling::span'
        CLIENT_BIC_CHECKBOX = '//*[normalize-space()="Client BIC"]/preceding-sibling::span'
        CLIENT_COMMISSION_CHECKBOX = '//*[normalize-space()="Client Commission"]/preceding-sibling::span'
        TRADE_DATE_CHECKBOX = '//*[normalize-space()="Trade Date"]/preceding-sibling::span'















