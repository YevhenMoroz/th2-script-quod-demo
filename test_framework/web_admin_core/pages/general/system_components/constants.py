class Constants:
    class MainPage:
        PAGE_TITLE = '//span[@class="entity-title left"][normalize-space()="System Components"]'
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

        class MoreActions:
            MORE_ACTIONS_BUTTON = '//*[@data-name="more-vertical"]'
            EDIT_BUTTON = '//nb-overlay-container//*[@data-name="edit"]'

            PIN_BUTTON = '//nb-overlay-container//*[@icon="unpinned-outline"]'