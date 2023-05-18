class Constants:
    class MainPage:
        PAGE_TITLE = '//span[@class="entity-title left"][normalize-space()="System Components"]'
        SITE_HEADER = '//*[@class="fixed"]'
        GLOBAL_FILTER = '//nb-card-header//*[@placeholder="Filter"]'
        HELP_ICON = '//nb-card-header//*[@nbtooltip="Help"]/a'
        DOWNLOAD_CSV_BUTTON = '//nb-card-header//*[@data-name="download"]'
        FULL_SCREEN_BUTTON = '//nb-card-header//*[@nbtooltip="Full Screen"]/a'
        REFRESH_BUTTON = '//nb-card-header//*[@data-name="refresh"]'

        INSTANCE_ID_FILTER = '(//input[@class="ag-floating-filter-input"])[1]'
        SHORT_NAME_FILTER = '(//input[@class="ag-floating-filter-input"])[2]'
        LONG_NAME_FILTER = '(//input[@class="ag-floating-filter-input"])[3]'
        VERSION_FILTER = '(//input[@class="ag-floating-filter-input"])[4]'
        ACTIVE_FILTER = '(//input[@class="ag-floating-filter-input"])[5]'

        SEARCHED_ENTITY = '//*[text()="{}"]'
        PINNED_ENTITY = '//*[@ref="eTop"]//*[@col-id="componentInstanceID"]//span[normalize-space()="{}"]'
        ACTIVE_STATUS_ICON = '//*[@class="action-cell"]//*[@nbtooltip="Active"]'

        MORE_ACTIONS_BUTTON = '//*[@data-name="more-vertical"]'
        EDIT_BUTTON = '//nb-overlay-container//*[@data-name="edit"]'
        CLONE_BUTTON = '//nb-overlay-container//*[@data-name="copy"]'
        DELETE_BUTTON = '//nb-overlay-container//*[@data-name="trash-2"]'
        DOWNLOAD_PDF_BUTTON = '//nb-overlay-container//*[@nbtooltip="Download PDF"]'
        PIN_BUTTON = '//nb-overlay-container//*[@icon="unpinned-outline" or @icon="pinned-outline"]'
        NEW_BUTTON = '//*[normalize-space()="New"]'

    class Wizard:
        REVERT_CHANGES_BUTTON = '//button[normalize-space()="Revert Changes"]'
        SAVE_CHANGES_BUTTON = '//button[normalize-space()="Save Changes"]'
        HELP_ICON = '//*[@data-name="menu-arrow-circle"]'
        PAGE_HEADER_LINK = '//nb-card-header//a//span'
        DOWNLOAD_LOCAL_FILE_BUTTON = '//*[@data-name="download"]'
        CLOSE_WIZARD_BUTTON = '//*[@data-name="close"]'

    class ValuesTab:
        SHORT_NAME = '//*[@formcontrolname="componentShortName"]'
        LONG_NAME = '//*[@formcontrolname="componentLongName"]'
        VERSION = '//*[@formcontrolname="componentRevision"]'
