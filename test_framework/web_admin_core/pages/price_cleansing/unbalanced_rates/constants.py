class Constants:
    class MainPage:
        PAGE_TITLE = '//span[@class="entity-title left"][normalize-space()="Unbalanced Rates"]'
        GLOBAL_FILTER = '//nb-card-header//*[@placeholder="Filter"]'
        HELP_ICON = '//nb-card-header//*[@nbtooltip="Help"]/a'
        DOWNLOAD_CSV_BUTTON = '//nb-card-header//*[@data-name="download"]'
        FULL_SCREEN_BUTTON = '//nb-card-header//*[@nbtooltip="Full Screen"]/a'
        REFRESH_BUTTON = '//nb-card-header//*[@data-name="refresh"]'
        NEW_BUTTON = '//nb-card-header//*[contains(@class, "new-btn")]'
        OK_BUTTON = '//*[normalize-space()="Ok" or normalize-space()="OK"]'
        CANCEL_BUTTON = '//button[normalize-space()="Cancel"]'
        SEARCHED_ENTITY = '//*[text()="{}"]'
        PINNED_ENTITY = '//*[@ref="eTop"]//*[@col-id="buyingPowerLimitName"]//span[normalize-space()="{}"]'

        class Filters:
            NAME = '(//input[@class="ag-floating-filter-input"])[1]'
            REMOVE_DETECTED_PRICE_UPDATES = '(//select[contains(@class, "boolean-filter")])[1]'
            ENRICH_EMPTY_SIDE_OF_BOOK = '(//select[contains(@class, "boolean-filter")])[2]'
            VENUE = '(//input[@class="ag-floating-filter-input"])[2]'
            LISTING = '(//input[@class="ag-floating-filter-input"])[3]'
            SYMBOL = '(//input[@class="ag-floating-filter-input"])[4]'
            INSTR_TYPE = '(//input[@class="ag-floating-filter-input"])[5]'
            SELECT_OPTION_TRUE = '//select//option[@value="true"]'
            SELECT_OPTION_FALSE = '//select//option[@value="false"]'

        class MoreActions:
            MORE_ACTIONS_BUTTON = '//*[@data-name="more-vertical"]'
            EDIT_BUTTON = '//nb-overlay-container//*[@data-name="edit"]'
            CLONE_BUTTON = '//nb-overlay-container//*[@data-name="copy"]'
            DELETE_BUTTON = '//nb-overlay-container//*[@data-name="trash-2"]'
            DOWNLOAD_PDF_BUTTON = '//nb-overlay-container//*[@data-name="download"]'
            PIN_BUTTON = '//nb-overlay-container//*[@icon="unpinned-outline"]'

    class Wizard:
        HELP_ICON = '//nb-card-header//*[@nbtooltip="Help"]/a'
        DOWNLOAD_PDF_BUTTON = '//nb-card-header//*[@data-name="download"]'
        CLOSE_BUTTON = '//nb-card-header//*[@data-name="close"]'
        CLEAR_CHANGES_BUTTON = '//button[normalize-space()="Clear Changes"]'
        SAVE_CHANGES_BUTTON = '//button[normalize-space()="Save Changes"]'
        OK_BUTTON = '//*[normalize-space()="Ok" or normalize-space()="OK"]'
        CANCEL_BUTTON = '//button[normalize-space()="Cancel"]'
        REVERT_CHANGES = '//button[normalize-space()="Revert Changes"]'
        NO_BUTTON = '//button[normalize-space()="No"]'
        DROP_DOWN_MENU = '//*[@class="option-list"]//span'
        FOOTER_ERROR = '//nb-card-footer//nb-alert//span'

        class ValuesTab:
            NAME = '//*[@formcontrolname="priceCleansingRuleName"]'
            REMOVE_DETECTED_PRICE_UPDATES_CHECKBOX = '//*[normalize-space()="Remove Detected Price Updates"]/preceding-sibling::span'
            ENRICH_EMPTY_SIDE_OF_BOOK_XPATH = '//*[normalize-space()="Enrich Empty Side Of Book"]/preceding-sibling::span'

        class DimensionsTab:
            VENUE = '//*[@id="venue"]'
            LISTING = '//*[@id="listing"]'
            INSTR_TYPE = '//*[@id="instrType"]'
            SYMBOL = '//*[@id="instrSymbol"]'

