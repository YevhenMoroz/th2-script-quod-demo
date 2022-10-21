class ClientTierConstants:
    CLIENT_TIER_PAGE_TITLE_XPATH = "//span[@class='entity-title left'][text()='Client Tiers ']"
    REFRESH_PAGE_BUTTON_XPATH = "//*[@data-name='refresh']"
    DOWNLOAD_PDF_BUTTON_XPATH = "//*[@data-name='download']"
    SAVE_CHANGES_BUTTON_XPATH = "//*[text()='Save Changes']"
    CLEAR_CHANGES_BUTTON_XPATH = "//*[text()='Clear Changes']"
    CLOSE_WIZARD_XPATH = "//*[@data-name='close']"
    OK_BUTTON_XPATH = '//*[text()="Ok" or text()="OK"]'
    CANCEL_BUTTON_XPATH = '//*[text()="Cancel"]'
    GO_BACK_BUTTON_XPATH = '//button[normalize-space()="Go Back"]'
    REVERT_CHANGES_XPATH = "//*[text()='Revert Changes']"
    SUCH_RECORD_ALREADY_EXISTS_MASSEGE_XPATH = "//*[text()='Such a record already exists']"
    INCORRECT_OR_MISSING_VALUES_XPATH = "//*[text()='Incorrect or missing values']"
    DROP_DOWN_MENU_XPATH = '//*[@class="option-list"]//span'
    DISPLAYED_ENTITY_XPATH = '//*[@class="ct-grid"]//div[@col-id="clientTierName"]//span[text()="{}"]'
    # region ~~~~~~~Client Tiers Block~~~~~~~
    # main page
    CLIENT_TIER_MORE_ACTIONS_XPATH = "//*[@class='ct-grid']//*[@data-name='more-vertical']"
    MAIN_PAGE_CLIENT_TIER_EDIT_XPATH = "//*[@class='cdk-overlay-container']//*[@data-name='edit']"
    MAIN_PAGE_CLIENT_TIER_CLONE_XPATH = "//*[@data-name='copy']"
    MAIN_PAGE_CLIENT_TIER_DELETE_XPATH = "//*[@data-name='trash-2']"
    MAIN_PAGE_CLIENT_TIER_PIN_ROW_XPATH = "//*[@class='cdk-overlay-container']//*[@nbtooltip='Click to Pin Row']"
    MAIN_PAGE_CLIENT_TIER_DOWNLOAD_CSV_XPATH = "//*[@class='ct-grid']//*[@data-name='download']"
    MAIN_PAGE_CLIENT_TIER_DOWNLOAD_PDF_XPATH ="//*[@class='cdk-overlay-container']//*[@data-name='download']"
    MAIN_PAGE_CLIENT_TIER_NEW_BUTTON_XPATH = '//*[normalize-space()="Client Tiers"]//..//*[text()="New"]'
    MAIN_PAGE_CLIENT_TIER_NAME_FILTER_XPATH = "//*[@class='ct-grid']//*[@class='ag-header-container']/div[2]/div[1]//input"
    MAIN_PAGE_CLIENT_TIER_CORE_SPOT_PRICE_STRATEGY_FILTER_XPATH = "//*[@class='ct-grid']//*[@class='ag-header-container']/div[2]/div[2]//input"
    MAIN_PAGE_CLIENT_TIER_ENABLE_SCHEDULE_FILTER_XPATH = "//*[@class='ct-grid']//*[@class='ag-header-container']/div[2]/div[3]//select"
    MAIN_PAGE_CLIENT_TIER_GLOBAL_FILTER_XPATH = '//*[text()="Client Tiers"]/following-sibling::div/input[@placeholder="Filter"]'
    MAIN_PAGE_CLIENT_TIER_EXECUTABLE_XPATH = '//*[normalize-space()="Executable"]//nb-icon'
    MAIN_PAGE_CLIENT_TIER_EXECUTABLE_ENABLE_TOOLTIP = '//*[@id="cdk-overlay-35"]//ancestor::*//*[@nbtooltip="Executable Enabled, Click to Disable"]'
    MAIN_PAGE_CLIENT_TIER_EXECUTABLE_DISABLE_TOOLTIP = '//*[@id="cdk-overlay-33"]//ancestor::*//*[@nbtooltip="Executable Disabled, Click to Enable"]'
    MAIN_PAGE_CLIENT_TIER_PRICING_XPATH = '//*[normalize-space()="Pricing"]//nb-icon'
    MAIN_PAGE_CLIENT_TIER_PRICING_ENABLE_TOOLTIP = '//*[@id="cdk-overlay-25"]//ancestor::*//*[@nbtooltip="Pricing Enabled, Click to Disable"]'
    MAIN_PAGE_CLIENT_TIER_PRICING_DISABLE_TOOLTIP = '//*[@id="cdk-overlay-38"]//ancestor::*//*[@nbtooltip="Pricing Disabled, Click to Enable"]'
    # region wizard
    # values tab
    CLIENT_TIER_VALUES_TAB_NAME_XPATH = '//*[@id="clientTierName"]'
    CLIENT_TIER_VALUES_TAB_CORE_SPOT_PRICE_STRATEGY_XPATH = '//*[@id="pricingMethod"]'
    CLIENT_TIER_VALUES_TAB_CORE_SPOT_PRICE_STRATEGY_DROP_DOWN_MENU_XPATH = "//*[@class='option-list']//span"
    CLIENT_TIER_VALUES_TAB_TOD_END_TIME = '//*[@id="TODEndTime_ext"]'
    CLIENT_TIER_VALUES_TAB_SCHEDULES_MANAGE_BUTTON = '//*[normalize-space()="Schedule"]//following::button[normalize-space()="Manage"]'
    CLIENT_TIER_VALUES_TAB_SCHEDULES_CHECKBOX = '//*[normalize-space()="Schedule"]//..//*[@class="custom-checkbox"]'
    CLIENT_TIER_VALUES_TAB_SCHEDULES = '//*[@id="schedule"]'
    # schedules
    # schedules schedules
    CLIENT_TIER_SCHEDULES_NAME_TAB_NAME_XPATH = '//*[@placeholder="Schedule Name *"]'
    CLIENT_TIER_SCHEDULES_NAME_TAB_NAME_FILTER_XPATH = '//*[normalize-space()="Schedule Name"]//*[@placeholder="Filter"]'
    CLIENT_TIER_SCHEDULES_NAME_TAB_PLUS_BUTTON = '//*[normalize-space()="Schedule Name"]//*//*[@data-name="plus"]'
    CLIENT_TIER_SCHEDULES_NAME_TAB_CHECKMARK_XPATH = '//*[normalize-space()="Schedule Name"]//..//*[@data-name="checkmark"]'
    CLIENT_TIER_SCHEDULES_NAME_TAB_CANCEL_XPATH = '//*[normalize-space()="Schedule Name"]//..//*[@data-name="close"]'
    CLIENT_TIER_SCHEDULES_NAME_TAB_DELETE_XPATH = '//*[normalize-space()="Schedule Name"]//..//*[@data-name="trash-2"]'
    CLIENT_TIER_SCHEDULES_NAME_TAB_EDIT_XPATH = '//*[normalize-space()="Schedule Name"]//..//*[@data-name="edit"]'
    CLIENT_TIER_SCHEDULES_NAME_TAB_SEARCHED_ENTITY_XPATH = '//*[normalize-space()="Schedule Name"]//..//span[normalize-space()="{}"]'

    CLIENT_TIER_SCHEDULES_TAB_PLUS_BUTTON_XPATH = '//*[normalize-space()="Schedules"]//..//*[@data-name="plus"]'
    CLIENT_TIER_SCHEDULES_TAB_CHECKMARK_BUTTON_XPATH = '//*[normalize-space()="Schedules"]//..//*[@data-name="checkmark"]'
    CLIENT_TIER_SCHEDULES_TAB_CLOSE_BUTTON_XPATH = '//*[normalize-space()="Schedules"]//..//*[@data-name="close"]'
    CLIENT_TIER_SCHEDULES_TAB_EDIT_BUTTON_XPATH = '//*[normalize-space()="Schedules"]//..//*[@data-name="edit"]'
    CLIENT_TIER_SCHEDULES_TAB_DELETE_BUTTON_XPATH = '//*[normalize-space()="Schedules"]//..//*[@data-name="trash-2"]'

    CLIENT_TIER_SCHEDULES_TAB_DAY_XPATH = "//*[@class='schedule']//*[@placeholder='Day *']"
    CLIENT_TIER_SCHEDULES_TAB_DAY_FILTER_XPATH = "//*[@class='schedule']//*[@class='ng2-smart-th weekDay ng-star-inserted']//input-filter"
    CLIENT_TIER_SCHEDULES_TAB_FROM_TIME_XPATH = "//*[@class='schedule']//*[@placeholder='From Time *']"
    CLIENT_TIER_SCHEDULES_TAB_FROM_TIME_FILTER_XPATH = "//*[@class='schedule']//*[@class='ng2-smart-th scheduleFromTime ng-star-inserted']//input-filter"
    CLIENT_TIER_SCHEDULES_TAB_TO_TIME_XPATH = "//*[@class='schedule']//*[@placeholder='To Time *']"
    CLIENT_TIER_SCHEDULES_TAB_TO_TIME_FILTER_XPATH = "//*[@class='schedule']//*[@class='ng2-smart-th scheduleToTime ng-star-inserted']//input-filter"

    # schedules exceptions
    CLIENT_TIER_SCHEDULES_EXCEPTIONS_TAB_PLUS_BUTTON_XPATH = "//*[@class='schedule-excep']//*[@data-name='plus']"
    CLIENT_TIER_SCHEDULES_EXCEPTIONS_TAB_CHECKMARK_BUTTON_XPATH = "//*[@class='schedule-excep']//*[@data-name='checkmark']"
    CLIENT_TIER_SCHEDULES_EXCEPTIONS_TAB_CLOSE_BUTTON_XPATH = "//*[@class='schedule-excep']//*[@data-name='close']"

    CLIENT_TIER_SCHEDULES_EXCEPTIONS_TAB_EXCEPTION_DAY_XPATH = "//*[@class='schedule-excep']//*[@placeholder='Exception Date *']"
    CLIENT_TIER_SCHEDULES_EXCEPTIONS_TAB_EXCEPTION_DAY_FILTER_XPATH = "//*[@class='schedule-excep']//*[@class='ng2-smart-th scheduleExceptionDate ng-star-inserted']//input-filter"
    CLIENT_TIER_SCHEDULES_EXCEPTIONS_TAB_FROM_TIME_XPATH = "//*[@class='schedule-excep']//*[@placeholder='From Time *']"
    CLIENT_TIER_SCHEDULES_EXCEPTIONS_TAB_FROM_TIME_FILTER_XPATH = "//*[@class='schedule-excep']//*[@class='ng2-smart-th scheduleFromTime ng-star-inserted']//input-filter"
    CLIENT_TIER_SCHEDULES_EXCEPTIONS_TAB_TO_TIME_XPATH = "//*[@class='schedule-excep']//*[@placeholder='To Time *']"
    CLIENT_TIER_SCHEDULES_EXCEPTIONS_TAB_TO_TIME_FILTER_XPATH = "//*[@class='schedule-excep']//*[@class='ng2-smart-th scheduleToTime ng-star-inserted']//input-filter"
    # endregion
    # endregion

    # region ~~~~~~~Client Tiers Instruments Block~~~~~~~
    CLIENT_TIER_INSTRUMENTS_MORE_ACTIONS_XPATH = "//*[@class='ctis-grid']//*[@data-name='more-vertical']"
    MAIN_PAGE_CLIENT_TIER_INSTRUMENTS_EDIT_XPATH = "//*[@data-name='edit']"
    MAIN_PAGE_CLIENT_TIER_INSTRUMENTS_CLONE_XPATH = "//*[@data-name='copy']"
    MAIN_PAGE_CLIENT_TIER_INSTRUMENTS_DOWNLOAD_PDF_XPATH = "//*[@nbtooltip='Download PDF']//*[@data-name='download']"
    MAIN_PAGE_CLIENT_TIER_INSTRUMENTS_PIN_ROW_XPATH = "//*[@class='cdk-overlay-container']//*[@nbtooltip='Click to Pin Row']"
    MAIN_PAGE_CLIENT_TIER_INSTRUMENTS_DOWNLOAD_CSV_XPATH = "//*[@class='ctis-grid']//*[@data-name='download']"
    MAIN_PAGE_CLIENT_TIER_INSTRUMENTS_NEW_BUTTON_XPATH = "//*[@class='ctis-grid']//*[text()='New']"

    MAIN_PAGE_CLIENT_TIER_INSTRUMENTS_SYMBOL_FILTER_XPATH = "//*[@class='ctis-grid']//*[@class='ag-header-container']/div[2]/div[1]//input"
    MAIN_PAGE_CLIENT_TIER_INSTRUMENTS_RFQ_RESPONSE_STREAM_TTL_FILTER_XPATH = "//*[@class='ctis-grid']//*[@class='ag-header-container']/div[2]/div[2]//input"
    MAIN_PAGE_CLIENT_TIER_INSTRUMENTS_CORE_SPOT_PRICE_STRATEGY_FILTER_XPATH = "//*[@class='ctis-grid']//*[@class='ag-header-container']/div[2]/div[3]//input"
    MAIN_PAGE_CLIENT_TIER_INSTRUMENTS_ENABLED_FILTER_XPATH = "//*[@class='ctis-grid']//*[@class='ag-header-container']/div[2]/div[1]//select"
    MAIN_PAGE_CLIENT_TIER_INSTRUMENTS_ENABLED_DISABLED_BUTTON_XPATH = "//*[@class='ag-pinned-left-cols-container']//span"
    MAIN_PAGE_CLIENT_TIER_INSTRUMENTS_CORE_SPOT_PRICE_STRATEGY_XPATH = "//*[@class='ctis-grid']//*[@col-id='pricingMethod']//span//span[4]"
    MAIN_PAGE_CLIENT_TIER_INSTRUMENTS_ENABLE_DISABLE_ARIA_CHECK_XPATH = "//*[@class='ctis-grid']//*[@class='ag-pinned-left-cols-container']/div[1]//input[@role='switch']"

    # region wizard
    # values tab
    CLIENT_TIER_INSTRUMENTS_VALUES_TAB_SYMBOL_XPATH = '//*[@id="instrSymbol"]'
    CLIENT_TIER_INSTRUMENTS_VALUES_TAB_SYMBOL_LABEL_XPATH = '//*[@for="instrSymbol"]'
    CLIENT_TIER_INSTRUMENTS_VALUES_TAB_RFQ_RESPONSE_TTL_XPATH = '//*[@formcontrolname="quoteTTL"]'
    CLIENT_TIER_INSTRUMENTS_VALUES_TAB_CORE_SPOT_PRICE_STRATEGY_XPATH = '//*[@id="pricingMethod"]'
    # spot venues tab
    CLIENT_TIER_INSTRUMENTS_SPOT_VENUES_TAB_PLUS_BUTTON_XPATH = '//*[text()=" Spot Venues "]/parent::nb-accordion-item//*[@data-name="plus"]'
    CLIENT_TIER_INSTRUMENTS_SPOT_VENUES_TAB_CHECKMARK_BUTTON_XPATH = '//*[text()=" Spot Venues "]/parent::nb-accordion-item//*[@data-name="checkmark"]'
    CLIENT_TIER_INSTRUMENTS_SPOT_VENUES_TAB_CLOSE_BUTTON_XPATH = '//*[text()=" Spot Venues "]/parent::nb-accordion-item//*[@data-name="close"]'
    CLIENT_TIER_INSTRUMENTS_SPOT_VENUES_TAB_EDIT_BUTTON_XPATH = '//*[text()=" Spot Venues "]/parent::nb-accordion-item//*[@data-name="edit"]'
    CLIENT_TIER_INSTRUMENTS_SPOT_VENUES_TAB_DELETE_BUTTON_XPATH = '//*[text()=" Spot Venues "]/parent::nb-accordion-item//*[@data-name="trash-2"]'

    CLIENT_TIER_INSTRUMENTS_SPOT_VENUES_TAB_VENUE_XPATH = '//*[normalize-space()="Spot Venues"]//..//*[@placeholder ="Venue *"]'
    CLIENT_TIER_INSTRUMENTS_SPOT_VENUES_TAB_VENUE_FILTER_XPATH = "//*[@class='ng2-smart-th venue ng-star-inserted']//input"

    CLIENT_TIER_INSTRUMENTS_SPOT_VENUES_TAB_CRITICAL_VENUE_CHECKBOX_XPATH = "//*[@class='ui-table-scrollable-body ng-star-inserted']//td[3]//span"
    CLIENT_TIER_INSTRUMENTS_SPOT_VENUES_TAB_CRITICAL_VENUE_FILTER_XPATH = "//*[@class='criticalVenue ng2-smart-th ng-star-inserted']//input"

    CLIENT_TIER_INSTRUMENTS_SPOT_VENUES_TAB_EXCLUDE_WHEN_UNHEALTHY_CHECKBOX_XPATH = "/html/body/ngx-app/ngx-pages/ngx-one-column-layout/nb-layout/div[1]/div/div/div/div/nb-layout-column/ngx-client-tier/ngx-ctis-wizard/div/nb-card/nb-card-body/div/nb-accordion/nb-accordion-item[2]/nb-accordion-item-body/div/div/ng2-smart-table/table/thead/tr[3]/td[4]/ng2-smart-table-cell/table-cell-edit-mode/div/table-cell-custom-editor/checkbox-custom-editor/form/nb-checkbox/label/span[1]"
    CLIENT_TIER_INSTRUMENTS_SPOT_VENUES_TAB_EXCLUDE_WHEN_UNHEALTHY_FILTER_XPATH = "//*[@class='excludeWhenUnhealthy ng2-smart-th ng-star-inserted']//input"

    CLIENT_TIER_INSTRUMENTS_SPOT_VENUES_TAB_DEFAULT_WEIGHT_XPATH = "//*[@placeholder ='Default Weight']"
    CLIENT_TIER_INSTRUMENTS_SPOT_VENUES_TAB_DEFAULT_WEIGHT_FILTER_XPATH = "//*[@class='defaultWeight ng2-smart-th ng-star-inserted']//input"

    # forward venues tab
    CLIENT_TIER_INSTRUMENTS_FORWARD_VENUES_TAB_PLUS_BUTTON_XPATH = '//*[text()=" Forward Venues "]/parent::nb-accordion-item//*[@data-name="plus"]'
    CLIENT_TIER_INSTRUMENTS_FORWARD_VENUES_TAB_CHECKMARK_BUTTON_XPATH = '//*[text()=" Forward Venues "]/parent::nb-accordion-item//*[@data-name="checkmark"]'
    CLIENT_TIER_INSTRUMENTS_FORWARD_VENUES_TAB_CLOSE_BUTTON_XPATH = '//*[text()=" Forward Venues "]/parent::nb-accordion-item//*[@data-name="close"]'
    CLIENT_TIER_INSTRUMENTS_FORWARD_VENUES_TAB_EDIT_BUTTON_XPATH = '//*[text()=" Forward Venues "]/parent::nb-accordion-item//*[@data-name="edit"]'
    CLIENT_TIER_INSTRUMENTS_FORWARD_VENUES_TAB_DELETE_BUTTON_XPATH = '//*[text()=" Forward Venues "]/parent::nb-accordion-item//*[@data-name="trash-2"]'

    CLIENT_TIER_INSTRUMENTS_FORWARD_VENUES_TAB_VENUE_XPATH = '//*[normalize-space()="Forward Venues"]//..//*[@placeholder ="Venue *"]'
    CLIENT_TIER_INSTRUMENTS_FORWARD_VENUES_TAB_VENUE_FILTER_XPATH = "//*[text()=' Forward Venues ']/parent::nb-accordion-item//*[@class='ng2-smart-th venue ng-star-inserted']//input"
    CLIENT_TIER_INSTRUMENTS_FORWARD_VENUES_TAB_EXCLUDE_WHEN_UNHEALTHY_XPATH = '/html/body/ngx-app/ngx-pages/ngx-one-column-layout/nb-layout/div[1]/div/div/div/div/nb-layout-column/ngx-client-tier/ngx-ctis-wizard/div/nb-card/nb-card-body/div/nb-accordion/nb-accordion-item[3]/nb-accordion-item-body/div/div/ng2-smart-table/table/thead/tr[3]/td[3]/ng2-smart-table-cell/table-cell-edit-mode/div/table-cell-custom-editor/checkbox-custom-editor/form/nb-checkbox/label/span[1]'
    CLIENT_TIER_INSTRUMENTS_FORWARD_VENUES_TAB_EXCLUDE_WHEN_UNHEALTHY_FILTER_XPATH = "//*[text()=' Forward Venues ']/parent::nb-accordion-item//*[@class='excludeWhenUnhealthy ng2-smart-th ng-star-inserted']//input"

    # external clients tab
    CLIENT_TIER_INSTRUMENTS_EXTERNAL_CLIENTS_TAB_PLUS_BUTTON_XPATH = '//*[text()=" External Clients "]/parent::nb-accordion-item//*[@data-name="plus"]'
    CLIENT_TIER_INSTRUMENTS_EXTERNAL_CLIENTS_TAB_CHECKMARK_BUTTON_XPATH = '//*[text()=" External Clients "]/parent::nb-accordion-item//*[@data-name="checkmark"]'
    CLIENT_TIER_INSTRUMENTS_EXTERNAL_CLIENTS_TAB_CLOSE_BUTTON_XPATH = '//*[text()=" External Clients "]/parent::nb-accordion-item//*[@data-name="close"]'
    CLIENT_TIER_INSTRUMENTS_EXTERNAL_CLIENTS_TAB_EDIT_BUTTON_XPATH = '//*[text()=" External Clients "]/parent::nb-accordion-item//*[@data-name="edit"]'
    CLIENT_TIER_INSTRUMENTS_EXTERNAL_CLIENTS_TAB_DELETE_BUTTON_XPATH = '//*[text()=" External Clients "]/parent::nb-accordion-item//*[@data-name="trash-2"]'

    CLIENT_TIER_INSTRUMENTS_EXTERNAL_CLIENTS_TAB_CLIENT_XPATH = '//*[normalize-space()="External Clients"]//..//*[@placeholder ="Client *"]'
    CLIENT_TIER_INSTRUMENTS_EXTERNAL_CLIENTS_TAB_CREATED_CLIENT_XPATH = '//*[text()=" External Clients "]/parent::nb-accordion-item//tbody//span'
    CLIENT_TIER_INSTRUMENTS_EXTERNAL_CLIENTS_TAB_CLIENT_FILTER_XPATH = "//*[text()=' External Clients ']/parent::nb-accordion-item//thead//tr[2]//th[2]//input"
    CLIENT_TIER_INSTRUMENTS_EXTERNAL_CLIENTS_TAB_WARNING_ICON = '//*[normalize-space()="External Clients"]//..//*[@data-name="alert-triangle"]'

    # internal clients tab
    CLIENT_TIER_INSTRUMENTS_INTERNAL_CLIENTS_TAB_PLUS_BUTTON_XPATH = '//*[text()=" Internal Clients "]/parent::nb-accordion-item//*[@data-name="plus"]'
    CLIENT_TIER_INSTRUMENTS_INTERNAL_CLIENTS_TAB_CHECKMARK_BUTTON_XPATH = '//*[text()=" Internal Clients "]/parent::nb-accordion-item//*[@data-name="checkmark"]'
    CLIENT_TIER_INSTRUMENTS_INTERNAL_CLIENTS_TAB_CLOSE_BUTTON_XPATH = '//*[text()=" Internal Clients "]/parent::nb-accordion-item//*[@data-name="close"]'
    CLIENT_TIER_INSTRUMENTS_INTERNAL_CLIENTS_TAB_EDIT_BUTTON_XPATH = '//*[text()=" Internal Clients "]/parent::nb-accordion-item//*[@data-name="edit"]'
    CLIENT_TIER_INSTRUMENTS_INTERNAL_CLIENTS_TAB_DELETE_BUTTON_XPATH = '//*[text()=" Internal Clients "]/parent::nb-accordion-item//*[@data-name="trash-2"]'

    CLIENT_TIER_INSTRUMENTS_INTERNAL_CLIENTS_TAB_CREATED_CLIENT_XPATH = '//*[text()=" Internal Clients "]/parent::nb-accordion-item//tbody//span'
    CLIENT_TIER_INSTRUMENTS_INTERNAL_CLIENTS_TAB_CLIENT_XPATH = '//*[normalize-space()="Internal Clients"]//..//*[@placeholder ="Client *"]'
    CLIENT_TIER_INSTRUMENTS_INTERNAL_CLIENTS_TAB_CLIENT_FILTER_XPATH = "//*[text()=' Internal Clients ']/parent::nb-accordion-item//thead//tr[2]//th[2]//input"
    CLIENT_TIER_INSTRUMENTS_INTERNAL_CLIENTS_TAB_WARNING_ICON = '//*[normalize-space()="Internal Clients"]//..//*[@data-name="alert-triangle"]'

    # sweepable quantities
    CLIENT_TIER_INSTRUMENTS_SWEEPABLE_QUANTITIES_TAB_PLUS_BUTTON_XPATH = '//*[text()=" Sweepable Quantities "]/parent::nb-accordion-item//*[@data-name="plus"]'
    CLIENT_TIER_INSTRUMENTS_SWEEPABLE_QUANTITIES_TAB_CHECKMARK_BUTTON_XPATH = '//*[text()=" Sweepable Quantities "]/parent::nb-accordion-item//*[@data-name="checkmark"]'
    CLIENT_TIER_INSTRUMENTS_SWEEPABLE_QUANTITIES_TAB_CLOSE_BUTTON_XPATH = '//*[text()=" Sweepable Quantities "]/parent::nb-accordion-item//*[@data-name="close"]'
    CLIENT_TIER_INSTRUMENTS_SWEEPABLE_QUANTITIES_TAB_EDIT_BUTTON_XPATH = '//*[text()=" Sweepable Quantities "]/parent::nb-accordion-item//*[@data-name="edit"]'
    CLIENT_TIER_INSTRUMENTS_SWEEPABLE_QUANTITIES_TAB_DELETE_BUTTON_XPATH = '//*[text()=" Sweepable Quantities "]/parent::nb-accordion-item//*[@data-name="trash-2"]'
    CLIENT_TIER_INSTRUMENTS_SWEEPABLE_QUANTITIES_TAB_DELETE_BY_VALUE_BUTTON_XPATH = '//*[normalize-space(text()="Sweepable Quantities")]/parent::nb-accordion-item//span[normalize-space(text())="{}"]/ancestor::tr//*[@data-name="trash-2"]'

    CLIENT_TIER_INSTRUMENTS_SWEEPABLE_QUANTITIES_TAB_QUANTITY_XPATH = '//*[normalize-space()="Sweepable Quantities"]//..//*[@placeholder ="Quantity *"]'
    CLIENT_TIER_INSTRUMENTS_SWEEPABLE_QUANTITIES_TAB_QUANTITY_FILTER_XPATH = '//*[text()=" Sweepable Quantities "]/parent::nb-accordion-item//thead//tr[2]//th[2]//input'

    CLIENT_TIER_INSTRUMENTS_SWEEPABLE_QUANTITIES_TAB_PUBLISHED_XPATH = "//*[text()=' Sweepable Quantities ']/parent::nb-accordion-item//*[@class='custom-checkbox']"
    CLIENT_TIER_INSTRUMENTS_SWEEPABLE_QUANTITIES_TAB_PUBLISHED_FILTER_XPATH = '//*[text()=" Sweepable Quantities "]/parent::nb-accordion-item//*[@class="ng2-smart-th publishPrices ng-star-inserted"]//input'

    # tiered quantities tab
    CLIENT_TIER_INSTRUMENTS_TIERED_QUANTITIES_TAB_PLUS_BUTTON_XPATH = '//*[text()=" Tiered Quantities "]/parent::nb-accordion-item//*[@data-name="plus"]'
    CLIENT_TIER_INSTRUMENTS_TIERED_QUANTITIES_TAB_CHECKMARK_BUTTON_XPATH = '//*[text()=" Tiered Quantities "]/parent::nb-accordion-item//*[@data-name="checkmark"]'
    CLIENT_TIER_INSTRUMENTS_TIERED_QUANTITIES_TAB_CLOSE_BUTTON_XPATH = '//*[text()=" Tiered Quantities "]/parent::nb-accordion-item//*[@data-name="close"]'
    CLIENT_TIER_INSTRUMENTS_TIERED_QUANTITIES_TAB_EDIT_BUTTON_XPATH = '//*[text()=" Tiered Quantities "]/parent::nb-accordion-item//*[@data-name="edit"]'
    CLIENT_TIER_INSTRUMENTS_TIERED_QUANTITIES_TAB_DELETE_BUTTON_XPATH = '//*[text()=" Tiered Quantities "]/parent::nb-accordion-item//*[@data-name="trash-2"]'

    CLIENT_TIER_INSTRUMENTS_TIERED_QUANTITIES_TAB_QUANTITY_XPATH = '//*[normalize-space()="Tiered Quantities"]//..//*[@placeholder ="Quantity *"]'
    CLIENT_TIER_INSTRUMENTS_TIERED_QUANTITIES_TAB_QUANTITY_FILTER_XPATH = '//*[normalize-space()="Tiered Quantities"]//..//*[@placeholder="Filter"]'
    CLIENT_TIER_INSTRUMENTS_TIERED_QUANTITIES_TAB_WARNING_XPATH = '//*[normalize-space()="Tiered Quantities"]//..//*[@class="max-sweep-qty-warning"]'
    # tenors tab
    CLIENT_TIER_INSTRUMENTS_TENORS_TAB_PLUS_BUTTON_XPATH = '//*[text()=" Tenors "]/parent::nb-accordion-item//*[@data-name="plus"]'
    CLIENT_TIER_INSTRUMENTS_TENORS_TAB_CHECKMARK_BUTTON_XPATH = '//*[text()=" Tenors "]/parent::nb-accordion-item//*[@data-name="checkmark"]'
    CLIENT_TIER_INSTRUMENTS_TENORS_TAB_CLOSE_BUTTON_XPATH = '//*[text()=" Tenors "]/parent::nb-accordion-item//*[@data-name="close"]'
    CLIENT_TIER_INSTRUMENTS_TENORS_TAB_EDIT_BUTTON_XPATH = '//*[text()=" Tenors "]/parent::nb-accordion-item//*[@data-name="edit"]'
    CLIENT_TIER_INSTRUMENTS_TENORS_TAB_DELETE_BUTTON_XPATH = '//*[text()=" Tenors "]/parent::nb-accordion-item//*[@data-name="trash-2"]'

    CLIENT_TIER_INSTRUMENTS_TENORS_TAB_CREATED_TENOR_ENTITY_XPATH = '//*[normalize-space()="Tenors"]//..//*[@class="tenor-table-body"]//td//span[normalize-space()="{}"]'

    CLIENT_TIER_INSTRUMENTS_TENORS_TAB_TENOR_XPATH = '//*[@placeholder ="Tenor *"]'
    CLIENT_TIER_INSTRUMENTS_TENORS_TAB_TENOR_FILTER_XPATH = '//*[@class ="tenor-table-body"]//input'
    CLIENT_TIER_INSTRUMENTS_TENORS_TAB_MIN_SPREAD_XPATH = '//*[@formcontrolname ="minSpread"]'
    CLIENT_TIER_INSTRUMENTS_TENORS_TAB_MAX_SPREAD_XPATH = '//*[@formcontrolname ="maxSpread"]'
    CLIENT_TIER_INSTRUMENTS_TENORS_TAB_MARGIN_FORMAT_XPATH = '//*[@id ="marginPriceType"]'
    CLIENT_TIER_INSTRUMENTS_TENORS_TAB_EXECUTABLE_CHECKBOX_XPATH = '//*[text()="Executable"]//parent::span'
    CLIENT_TIER_INSTRUMENTS_TENORS_TAB_PRICING_CHECKBOX_XPATH = '//*[text()="Pricing"]//parent::span'
    CLIENT_TIER_INSTRUMENTS_TENORS_TAB_CLIENT_PRICE_SLIPPAGE_RANGE_CHECKBOX_XPATH = '//*[@formcontrolname ="validatePriceSlippage"]'
    CLIENT_TIER_INSTRUMENTS_TENORS_TAB_CLIENT_PRICE_SLIPPAGE_RANGE_XPATH = '//input[@formcontrolname="priceSlippageRange"]'
    CLIENT_TIER_INSTRUMENTS_TENORS_TAB_MINIMUM_PRICE_CHECKBOX_XPATH = '//*[@formcontrolname ="validateMinPrice"]'
    CLIENT_TIER_INSTRUMENTS_TENORS_TAB_MINIMUM_PRICE_XPATH = '//*[@formcontrolname ="validateMinPrice"]/input'
    CLIENT_TIER_INSTRUMENTS_TENORS_TAB_MAXIMUM_PRICE_CHECKBOX_XPATH = '//*[@formcontrolname ="validateMaxPrice"]'
    CLIENT_TIER_INSTRUMENTS_TENORS_TAB_MAXIMUM_PRICE_XPATH = '//*[@formcontrolname ="validateMaxPrice"]/input'
    CLIENT_TIER_INSTRUMENTS_TENORS_TAB_AUTOMATED_MARGIN_STRATEGIES_ENABLED_CHECKBOX_XPATH = '//*[text()="Automated Margin Strategies Enabled"]//preceding-sibling::span'
    CLIENT_TIER_INSTRUMENTS_TENORS_TAB_POSITION_BASED_MARGINS_CHECKBOX_XPATH = '//*[text()="Position Based Margins"]//preceding-sibling::span'
    CLIENT_TIER_INSTRUMENTS_TENORS_TAB_POSITION_BOOK_XPATH = '//*[@id ="monitoredPosAccountGroup"]'

    # base margins sub tab
    CLIENT_TIER_INSTRUMENTS_BASE_MARGINS_SUB_TAB_EDIT_BUTTON_XPATH = "//*[text()=' Base Margins ']/parent::nb-accordion-item//*[@data-name='edit']"
    CLIENT_TIER_INSTRUMENTS_BASE_MARGINS_SUB_TAB_EDIT_BUTTON_BY_VALUE_XPATH = '//*[normalize-space()="Base Margins"]//..//*[normalize-space()="{}"]//..//*[@nbtooltip="Edit"]'
    CLIENT_TIER_INSTRUMENTS_BASE_MARGINS_SUB_TAB_DELETE_BUTTON_BY_VALUE_XPATH = '//*[normalize-space()="Base Margins"]//..//*[normalize-space()="{}"]//..//*[@data-name="trash-2"]'
    CLIENT_TIER_INSTRUMENTS_BASE_MARGINS_SUB_TAB_CHECKMARK_BUTTON_XPATH = "//*[text()=' Base Margins ']//parent::nb-accordion-item//*[@data-name='checkmark']"
    CLIENT_TIER_INSTRUMENTS_BASE_MARGINS_SUB_TAB_CLOSE_BUTTON_XPATH = "//*[text()=' Base Margins ']//parent::nb-accordion-item//*[@data-name='close']"
    CLIENT_TIER_INSTRUMENTS_BASE_MARGINS_SUB_TAB_QUANTITY_XPATH = '//*[@placeholder="Quantity *"]'
    CLIENT_TIER_INSTRUMENTS_BASE_MARGINS_SUB_TAB_BID_MARGIN_XPATH = '//*[@placeholder ="Bid Margin"]'
    CLIENT_TIER_INSTRUMENTS_BASE_MARGINS_SUB_TAB_OFFER_MARGIN_XPATH = '//*[@placeholder ="Offer Margin"]'
    CLIENT_TIER_INSTRUMENTS_BASE_MARGINS_SUB_TAB_EXECUTABLE_CHECKBOX_XPATH = '(//*[normalize-space()="Base Margins"]//..//*[*[@nbtooltip="Save"]]//..//..//nb-checkbox)[1]'
    CLIENT_TIER_INSTRUMENTS_BASE_MARGINS_SUB_TAB_PRICING_CHECKBOX_XPATH = '(//*[normalize-space()="Base Margins"]//..//*[*[@nbtooltip="Save"]]//..//..//nb-checkbox)[2]'
    CLIENT_TIER_INSTRUMENTS_BASE_MARGINS_SUB_TAB_PUBLISH_PRICES_CHECKBOX_XPATH = '(//*[normalize-space()="Base Margins"]//..//*[*[@nbtooltip="Save"]]//..//..//nb-checkbox)[3]'
    CLIENT_TIER_INSTRUMENTS_BASE_MARGINS_SUB_TAB_QUANTITY_FILTER_XPATH = '//*[text()=" Base Margins "]/parent::nb-accordion-item//thead//tr[2]//th[2]//input'
    CLIENT_TIER_INSTRUMENTS_BASE_MARGINS_SUB_TAB_BID_MARGIN_FILTER_XPATH = '//*[@class= "defaultBidMargin ng2-smart-th ng-star-inserted"]//input'
    CLIENT_TIER_INSTRUMENTS_BASE_MARGINS_SUB_TAB_OFFER_MARGIN_FILTER_XPATH = '//*[@class= "defaultOfferMargin ng2-smart-th ng-star-inserted"]//input'
    CLIENT_TIER_INSTRUMENTS_BASE_MARGINS_SUB_TAB_EXECUTABLE_MARGIN_FILTER_XPATH = '//*[@class= "MDQuoteType ng2-smart-th ng-star-inserted"]//input'
    CLIENT_TIER_INSTRUMENTS_BASE_MARGINS_SUB_TAB_PRICING_FILTER_XPATH = '//*[@class= "activeQuote ng2-smart-th ng-star-inserted"]//input'
    CLIENT_TIER_INSTRUMENTS_BASE_MARGINS_SUB_TAB_PLUS_BUTTON_XPATH = '//*[text()=" Base Margins "]/parent::nb-accordion-item//*[@data-name="plus"]'
    CLIENT_TIER_INSTRUMENTS_BASE_MARGINS_SUB_TAB_QUANTITY_TABLE_ROW_XPATH = '//*[text()=" Base Margins "]//parent::nb-accordion-item//div[@class="ui-table-scrollable-view"]/div[2]//td[2]//span'

    # tenor - tired quantity
    TIRED_QUANTITY_PLUS_BUTTON_AT_TENOR = '//*[normalize-space()="Tenors"]//..//*[normalize-space()="Tiered Quantities"]//..//*[@nbtooltip="Add"]'
    TIRED_QUANTITY_CHECKMARK_BUTTON_AT_TENOR = '//*[normalize-space()="Tenors"]//..//*[normalize-space()="Tiered Quantities"]//..//*[@data-name="checkmark"]'
    TIRED_QUANTITY_CANCEL_BUTTON_AT_TENOR = '//*[normalize-space()="Tenors"]//..//*[normalize-space()="Tiered Quantities"]//..//*[@data-name="close"]'
    TIRED_QUANTITY_EDIT_BUTTON_AT_TENOR = '//*[normalize-space()="Tenors"]//..//*[normalize-space()="Tiered Quantities"]//..//*[@data-name="edit"]'
    TIRED_QUANTITY_DELETE_BUTTON_AT_TENOR = '//*[normalize-space()="Tenors"]//..//*[normalize-space()="Tiered Quantities"]//..//*[@data-name="trash-2"]'
    TIRED_QUANTITY_QUANTITY_INPUT_AT_TENOR = '//*[normalize-space()="Tenors"]//..//*[normalize-space()="Tiered Quantities"]//..//*[@placeholder="Quantity *"]'

    # position levels sub tab
    CLIENT_TIER_INSTRUMENTS_POSITION_LEVELS_TAB_PLUS_BUTTON_XPATH = '//*[normalize-space()="Position Levels"]//..//*[@nbtooltip="Add"]'
    CLIENT_TIER_INSTRUMENTS_POSITION_LEVELS_TAB_CHECKMARK_BUTTON_XPATH = '//*[normalize-space()="Position Levels"]//..//*[@data-name="checkmark"]'
    CLIENT_TIER_INSTRUMENTS_POSITION_LEVELS_TAB_CLOSE_BUTTON_XPATH = '//*[normalize-space()="Position Levels"]//..//*[@data-name="close"]'
    CLIENT_TIER_INSTRUMENTS_POSITION_LEVELS_TAB_EDIT_BUTTON_XPATH = '//*[normalize-space()="Position Levels"]//..//*[@data-name="edit"]'
    CLIENT_TIER_INSTRUMENTS_POSITION_LEVELS_TAB_DELETE_BUTTON_XPATH = '//*[normalize-space()="Position Levels"]//..//*[@data-name="trash-2"]'

    CLIENT_TIER_INSTRUMENTS_POSITION_LEVELS_TAB_POSITION_XPATH = '//*[@placeholder ="Position (EUR) *"]'
    CLIENT_TIER_INSTRUMENTS_POSITION_LEVELS_TAB_POSITION_FILTER_XPATH = '//*[@class="tenors-table-wrapper"]//*[@class="ng2-smart-th sysCurrPositQty ng-star-inserted"]//input'

    CLIENT_TIER_INSTRUMENTS_POSITION_LEVELS_TAB_BID_MARGIN_XPATH = '//*[@placeholder ="Bid Margin"]'
    CLIENT_TIER_INSTRUMENTS_POSITION_LEVELS_TAB_BID_MARGIN_FILTER_XPATH = '//*[@class="tenors-table-wrapper"]//*[@class="bidMargin ng2-smart-th ng-star-inserted"]//input'

    CLIENT_TIER_INSTRUMENTS_POSITION_LEVELS_TAB_OFFER_MARGIN_XPATH = '//*[@placeholder ="Offer Margin"]'
    CLIENT_TIER_INSTRUMENTS_POSITION_LEVELS_TAB_OFFER_MARGIN_FILTER_XPATH = '//*[@class="tenors-table-wrapper"]//*[@class="ng2-smart-th offerMargin ng-star-inserted"]//input'
    # endregion

    # endregion
