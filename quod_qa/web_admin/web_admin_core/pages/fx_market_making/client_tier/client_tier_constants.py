class ClientTierConstants:
    CLIENT_TIER_PAGE_TITLE_XPATH = "//span[@class='entity-title left'][text()='Client Tier ']"
    REFRESH_PAGE_BUTTON_XPATH = "//*[@data-name='refresh']"
    DOWNLOAD_PDF_BUTTON_XPATH = "//*[@data-name='download']"
    SAVE_CHANGES_BUTTON_XPATH = "//*[text()='Save Changes']"
    CLEAR_CHANGES_BUTTON_XPATH = "//*[text()='Clear Changes']"
    CLOSE_WIZARD_XPATH = "//*[@data-name='close']"
    OK_BUTTON_XPATH = '//*[text()="Ok"]'
    CANCEL_BUTTON_XPATH = '//*[text()="Cancel"]'
    REVERT_CHANGES_XPATH = "//*[text()='Revert Changes']"
    SUCH_RECORD_ALREADY_EXISTS_MASSEGE_XPATH = "//*[text()='Such a record already exists']"
    INCORRECT_OR_MISSING_VALUES_XPATH = "//*[text()='Incorrect or missing values']"
    # region ~~~~~~~Client Tiers Block~~~~~~~
    # main page
    CLIENT_TIER_MORE_ACTIONS_XPATH = "//*[@class='ct-grid']//*[@data-name='more-vertical']"
    MAIN_PAGE_CLIENT_TIER_EDIT_XPATH = "//*[@class='cdk-overlay-container']//*[@data-name='edit']"
    MAIN_PAGE_CLIENT_TIER_CLONE_XPATH = "//*[@class='ct-grid']//*[@data-name='copy']"
    MAIN_PAGE_CLIENT_TIER_DELETE_XPATH = "//*[@class='ct-grid']//*[@data-name='trash-2']"
    MAIN_PAGE_CLIENT_TIER_PIN_ROW_XPATH = "//*[@class='cdk-overlay-container']//*[@nbtooltip='Click to Pin Row']"
    MAIN_PAGE_CLIENT_TIER_DOWNLOAD_CSV_XPATH = "//*[@class='ct-grid']//*[@data-name='download']"
    MAIN_PAGE_CLIENT_TIER_DOWNLOAD_PDF_XPATH ="//*[@class='cdk-overlay-container']//*[@data-name='download']"
    MAIN_PAGE_CLIENT_TIER_NEW_BUTTON_XPATH = "//*[@class='ct-grid']//*[text()='New']"
    MAIN_PAGE_CLIENT_TIER_NAME_FILTER_XPATH = "//*[@class='ct-grid']//*[@class='ag-header-container']/div[2]/div[1]//input"
    MAIN_PAGE_CLIENT_TIER_CORE_SPOT_PRICE_STRATEGY_FILTER_XPATH = "//*[@class='ct-grid']//*[@class='ag-header-container']/div[2]/div[2]//input"
    MAIN_PAGE_CLIENT_TIER_ENABLE_SCHEDULE_FILTER_XPATH = "//*[@class='ct-grid']//*[@class='ag-header-container']/div[2]/div[3]//select"
    # region wizard
    # values tab
    CLIENT_TIER_VALUES_TAB_NAME_XPATH = "//*[text()='Name *']/preceding-sibling::input"
    CLIENT_TIER_VALUES_TAB_CORE_SPOT_PRICE_STRATEGY_XPATH = "//*[text()='Core Spot Price Strategy']/preceding-sibling::input"
    # schedules
    CLIENT_TIER_SCHEDULES_TAB_ENABLE_SCHEDULE_CHECKBOX_XPATH = "//*[text()='Enable Schedule']/preceding-sibling::span"
    # schedules schedules
    CLIENT_TIER_SCHEDULES_TAB_PLUS_BUTTON_XPATH = "//*[@class='schedule']//*[@class='nb-plus']"
    CLIENT_TIER_SCHEDULES_TAB_CHECKMARK_BUTTON_XPATH = "//*[@class='schedule']//*[@class='nb-checkmark']"
    CLIENT_TIER_SCHEDULES_TAB_CLOSE_BUTTON_XPATH = "//*[@class='schedule']//*[@class='nb-close']"
    CLIENT_TIER_SCHEDULES_TAB_EDIT_BUTTON_XPATH = '//*[@class="schedule"]//*[@class="nb-edit"]'
    CLIENT_TIER_SCHEDULES_TAB_DELETE_BUTTON_XPATH = '//*[@class="schedule"]//*[@class="nb-trash"]'

    CLIENT_TIER_SCHEDULES_TAB_DAY_XPATH = "//*[@class='schedule']//*[@placeholder='Day *']"
    CLIENT_TIER_SCHEDULES_TAB_DAY_FILTER_XPATH = "//*[@class='schedule']//*[@class='ng2-smart-th weekDay ng-star-inserted']//input-filter"
    CLIENT_TIER_SCHEDULES_TAB_FROM_TIME_XPATH = "//*[@class='schedule']//*[@placeholder='From Time *']"
    CLIENT_TIER_SCHEDULES_TAB_FROM_TIME_FILTER_XPATH = "//*[@class='schedule']//*[@class='ng2-smart-th scheduleFromTime ng-star-inserted']//input-filter"
    CLIENT_TIER_SCHEDULES_TAB_TO_TIME_XPATH = "//*[@class='schedule']//*[@placeholder='To Time *']"
    CLIENT_TIER_SCHEDULES_TAB_TO_TIME_FILTER_XPATH = "//*[@class='schedule']//*[@class='ng2-smart-th scheduleToTime ng-star-inserted']//input-filter"

    # schedules exceptions
    CLIENT_TIER_SCHEDULES_EXCEPTIONS_TAB_PLUS_BUTTON_XPATH = "//*[@class='schedule-excep']//*[@class='nb-plus']"
    CLIENT_TIER_SCHEDULES_EXCEPTIONS_TAB_CHECKMARK_BUTTON_XPATH = "//*[@class='schedule-excep']//*[@class='nb-checkmark']"
    CLIENT_TIER_SCHEDULES_EXCEPTIONS_TAB_CLOSE_BUTTON_XPATH = "//*[@class='schedule-excep']//*[@class='nb-close']"

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
    MAIN_PAGE_CLIENT_TIER_INSTRUMENTS_DOWNLOAD_PDF_XPATH = "//*[@data-name='download']"
    MAIN_PAGE_CLIENT_TIER_INSTRUMENTS_PIN_ROW_XPATH = "//*[@class='cdk-overlay-container']//*[@nbtooltip='Click to Pin Row']"
    MAIN_PAGE_CLIENT_TIER_INSTRUMENTS_DOWNLOAD_CSV_XPATH = "//*[@class='ctis-grid']//*[@data-name='download']"
    MAIN_PAGE_CLIENT_TIER_INSTRUMENTS_NEW_BUTTON_XPATH = "//*[@class='ctis-grid']//*[text()='New']"

    MAIN_PAGE_CLIENT_TIER_INSTRUMENTS_SYMBOL_FILTER_XPATH = "//*[@class='ctis-grid']//*[@class='ag-header-container']/div[2]/div[1]//input"
    MAIN_PAGE_CLIENT_TIER_INSTRUMENTS_RFQ_RESPONSE_STREAM_TTL_FILTER_XPATH = "//*[@class='ctis-grid']//*[@class='ag-header-container']/div[2]/div[2]//input"
    MAIN_PAGE_CLIENT_TIER_INSTRUMENTS_CORE_SPOT_PRICE_STRATEGY_FILTER_XPATH = "//*[@class='ctis-grid']//*[@class='ag-header-container']/div[2]/div[3]//input"
    MAIN_PAGE_CLIENT_TIER_INSTRUMENTS_ENABLED_FILTER_XPATH = "//*[@class='ctis-grid']//*[@class='ag-header-container']/div[2]/div[1]//select"
    MAIN_PAGE_CLIENT_TIER_INSTRUMENTS_ENABLED_DISABLED_BUTTON_XPATH = "//*[@class='ag-pinned-left-cols-container']//span"

    # region wizard
    # values tab
    CLIENT_TIER_INSTRUMENTS_VALUES_TAB_SYMBOL_XPATH = '//*[@id="instrSymbol"]'
    CLIENT_TIER_INSTRUMENTS_VALUES_TAB_RFQ_RESPONSE_TTL_XPATH = '//*[@formcontrolname="quoteTTL"]'
    CLIENT_TIER_INSTRUMENTS_VALUES_TAB_CORE_SPOT_PRICE_STRATEGY_XPATH = '//*[@id="pricingMethod"]'
    # spot venues tab
    CLIENT_TIER_INSTRUMENTS_SPOT_VENUES_TAB_PLUS_BUTTON_XPATH = '//*[text()=" Spot Venues "]/parent::nb-accordion-item//*[@class="nb-plus"]'
    CLIENT_TIER_INSTRUMENTS_SPOT_VENUES_TAB_CHECKMARK_BUTTON_XPATH = '//*[text()=" Spot Venues "]/parent::nb-accordion-item//*[@class="nb-checkmark"]'
    CLIENT_TIER_INSTRUMENTS_SPOT_VENUES_TAB_CLOSE_BUTTON_XPATH = '//*[text()=" Spot Venues "]/parent::nb-accordion-item//*[@class="nb-close"]'
    CLIENT_TIER_INSTRUMENTS_SPOT_VENUES_TAB_EDIT_BUTTON_XPATH = '//*[text()=" Spot Venues "]/parent::nb-accordion-item//*[@class="nb-edit"]'
    CLIENT_TIER_INSTRUMENTS_SPOT_VENUES_TAB_DELETE_BUTTON_XPATH = '//*[text()=" Spot Venues "]/parent::nb-accordion-item//*[@class="nb-trash"]'

    CLIENT_TIER_INSTRUMENTS_SPOT_VENUES_TAB_VENUE_XPATH = "//*[@placeholder ='Venue *']"
    CLIENT_TIER_INSTRUMENTS_SPOT_VENUES_TAB_VENUE_FILTER_XPATH = "//*[@class='ng2-smart-th venue ng-star-inserted']//input"

    CLIENT_TIER_INSTRUMENTS_SPOT_VENUES_TAB_CRITICAL_VENUE_CHECKBOX_XPATH = "/html/body/ngx-app/ngx-pages/ngx-one-column-layout/nb-layout/div[1]/div/div/div/div/nb-layout-column/ngx-client-tier/ngx-ctis-wizard/div/nb-card/nb-card-body/div/nb-accordion/nb-accordion-item[2]/nb-accordion-item-body/div/div/ng2-smart-table/table/thead/tr[3]/td[3]/ng2-smart-table-cell/table-cell-edit-mode/div/table-cell-custom-editor/checkbox-custom-editor/form/nb-checkbox/label/span[1]"
    CLIENT_TIER_INSTRUMENTS_SPOT_VENUES_TAB_CRITICAL_VENUE_FILTER_XPATH = "//*[@class='criticalVenue ng2-smart-th ng-star-inserted']//input"

    CLIENT_TIER_INSTRUMENTS_SPOT_VENUES_TAB_EXCLUDE_WHEN_UNHEALTHY_CHECKBOX_XPATH = "/html/body/ngx-app/ngx-pages/ngx-one-column-layout/nb-layout/div[1]/div/div/div/div/nb-layout-column/ngx-client-tier/ngx-ctis-wizard/div/nb-card/nb-card-body/div/nb-accordion/nb-accordion-item[2]/nb-accordion-item-body/div/div/ng2-smart-table/table/thead/tr[3]/td[4]/ng2-smart-table-cell/table-cell-edit-mode/div/table-cell-custom-editor/checkbox-custom-editor/form/nb-checkbox/label/span[1]"
    CLIENT_TIER_INSTRUMENTS_SPOT_VENUES_TAB_EXCLUDE_WHEN_UNHEALTHY_FILTER_XPATH = "//*[@class='excludeWhenUnhealthy ng2-smart-th ng-star-inserted']//input"

    CLIENT_TIER_INSTRUMENTS_SPOT_VENUES_TAB_DEFAULT_WEIGHT_XPATH = "//*[@placeholder ='Default Weight']"
    CLIENT_TIER_INSTRUMENTS_SPOT_VENUES_TAB_DEFAULT_WEIGHT_FILTER_XPATH = "//*[@class='defaultWeight ng2-smart-th ng-star-inserted']//input"

    # forward venues tab
    CLIENT_TIER_INSTRUMENTS_FORWARD_VENUES_TAB_PLUS_BUTTON_XPATH = '//*[text()=" Forward Venues "]/parent::nb-accordion-item//*[@class="nb-plus"]'
    CLIENT_TIER_INSTRUMENTS_FORWARD_VENUES_TAB_CHECKMARK_BUTTON_XPATH = '//*[text()=" Forward Venues "]/parent::nb-accordion-item//*[@class="nb-checkmark"]'
    CLIENT_TIER_INSTRUMENTS_FORWARD_VENUES_TAB_CLOSE_BUTTON_XPATH = '//*[text()=" Forward Venues "]/parent::nb-accordion-item//*[@class="nb-close"]'
    CLIENT_TIER_INSTRUMENTS_FORWARD_VENUES_TAB_EDIT_BUTTON_XPATH = '//*[text()=" Forward Venues "]/parent::nb-accordion-item//*[@class="nb-edit"]'
    CLIENT_TIER_INSTRUMENTS_FORWARD_VENUES_TAB_DELETE_BUTTON_XPATH = '//*[text()=" Forward Venues "]/parent::nb-accordion-item//*[@class="nb-trash"]'

    CLIENT_TIER_INSTRUMENTS_FORWARD_VENUES_TAB_VENUE_XPATH = '//*[@placeholder ="Venue *"]'
    CLIENT_TIER_INSTRUMENTS_FORWARD_VENUES_TAB_VENUE_FILTER_XPATH = "//*[text()=' Forward Venues ']/parent::nb-accordion-item//*[@class='ng2-smart-th venue ng-star-inserted']//input"
    CLIENT_TIER_INSTRUMENTS_FORWARD_VENUES_TAB_EXCLUDE_WHEN_UNHEALTHY_XPATH = '/html/body/ngx-app/ngx-pages/ngx-one-column-layout/nb-layout/div[1]/div/div/div/div/nb-layout-column/ngx-client-tier/ngx-ctis-wizard/div/nb-card/nb-card-body/div/nb-accordion/nb-accordion-item[3]/nb-accordion-item-body/div/div/ng2-smart-table/table/thead/tr[3]/td[3]/ng2-smart-table-cell/table-cell-edit-mode/div/table-cell-custom-editor/checkbox-custom-editor/form/nb-checkbox/label/span[1]'
    CLIENT_TIER_INSTRUMENTS_FORWARD_VENUES_TAB_EXCLUDE_WHEN_UNHEALTHY_FILTER_XPATH = "//*[text()=' Forward Venues ']/parent::nb-accordion-item//*[@class='excludeWhenUnhealthy ng2-smart-th ng-star-inserted']//input"

    # external clients tab
    CLIENT_TIER_INSTRUMENTS_EXTERNAL_CLIENTS_TAB_PLUS_BUTTON_XPATH = '//*[text()=" External Clients "]/parent::nb-accordion-item//*[@class="nb-plus"]'
    CLIENT_TIER_INSTRUMENTS_EXTERNAL_CLIENTS_TAB_CHECKMARK_BUTTON_XPATH = '//*[text()=" External Clients "]/parent::nb-accordion-item//*[@class="nb-checkmark"]'
    CLIENT_TIER_INSTRUMENTS_EXTERNAL_CLIENTS_TAB_CLOSE_BUTTON_XPATH = '//*[text()=" External Clients "]/parent::nb-accordion-item//*[@class="nb-close"]'
    CLIENT_TIER_INSTRUMENTS_EXTERNAL_CLIENTS_TAB_EDIT_BUTTON_XPATH = '//*[text()=" External Clients "]/parent::nb-accordion-item//*[@class="nb-edit"]'
    CLIENT_TIER_INSTRUMENTS_EXTERNAL_CLIENTS_TAB_DELETE_BUTTON_XPATH = '//*[text()=" External Clients "]/parent::nb-accordion-item//*[@class="nb-trash"]'

    CLIENT_TIER_INSTRUMENTS_EXTERNAL_CLIENTS_TAB_CLIENT_XPATH = '//*[@placeholder ="Client *"]'
    CLIENT_TIER_INSTRUMENTS_EXTERNAL_CLIENTS_TAB_CLIENT_FILTER_XPATH = "//*[text()=' External Clients ']/parent::nb-accordion-item//*[@class='accountGroup ng2-smart-th ng-star-inserted']//input"

    # internal clients tab
    CLIENT_TIER_INSTRUMENTS_INTERNAL_CLIENTS_TAB_PLUS_BUTTON_XPATH = '//*[text()=" Internal Clients "]/parent::nb-accordion-item//*[@class="nb-plus"]'
    CLIENT_TIER_INSTRUMENTS_INTERNAL_CLIENTS_TAB_CHECKMARK_BUTTON_XPATH = '//*[text()=" Internal Clients "]/parent::nb-accordion-item//*[@class="nb-checkmark"]'
    CLIENT_TIER_INSTRUMENTS_INTERNAL_CLIENTS_TAB_CLOSE_BUTTON_XPATH = '//*[text()=" Internal Clients "]/parent::nb-accordion-item//*[@class="nb-close"]'
    CLIENT_TIER_INSTRUMENTS_INTERNAL_CLIENTS_TAB_EDIT_BUTTON_XPATH = '//*[text()=" Internal Clients "]/parent::nb-accordion-item//*[@class="nb-edit"]'
    CLIENT_TIER_INSTRUMENTS_INTERNAL_CLIENTS_TAB_DELETE_BUTTON_XPATH = '//*[text()=" Internal Clients "]/parent::nb-accordion-item//*[@class="nb-trash"]'

    CLIENT_TIER_INSTRUMENTS_INTERNAL_CLIENTS_TAB_CLIENT_XPATH = '//*[@placeholder ="Client *"]'
    CLIENT_TIER_INSTRUMENTS_INTERNAL_CLIENTS_TAB_CLIENT_FILTER_XPATH = "//*[text()=' Internal Clients ']/parent::nb-accordion-item//*[@class='accountGroup ng2-smart-th ng-star-inserted']//input"

    # sweepable quantities
    CLIENT_TIER_INSTRUMENTS_SWEEPABLE_QUANTITIES_TAB_PLUS_BUTTON_XPATH = '//*[text()=" Sweepable Quantities "]/parent::nb-accordion-item//*[@class="nb-plus"]'
    CLIENT_TIER_INSTRUMENTS_SWEEPABLE_QUANTITIES_TAB_CHECKMARK_BUTTON_XPATH = '//*[text()=" Sweepable Quantities "]/parent::nb-accordion-item//*[@class="nb-checkmark"]'
    CLIENT_TIER_INSTRUMENTS_SWEEPABLE_QUANTITIES_TAB_CLOSE_BUTTON_XPATH = '//*[text()=" Sweepable Quantities "]/parent::nb-accordion-item//*[@class="nb-close"]'
    CLIENT_TIER_INSTRUMENTS_SWEEPABLE_QUANTITIES_TAB_EDIT_BUTTON_XPATH = '//*[text()=" Sweepable Quantities "]/parent::nb-accordion-item//*[@class="nb-edit"]'
    CLIENT_TIER_INSTRUMENTS_SWEEPABLE_QUANTITIES_TAB_DELETE_BUTTON_XPATH = '//*[text()=" Sweepable Quantities "]/parent::nb-accordion-item//*[@class="nb-trash"]'

    CLIENT_TIER_INSTRUMENTS_SWEEPABLE_QUANTITIES_TAB_QUANTITY_XPATH = '//*[@placeholder ="Quantity *"]'
    CLIENT_TIER_INSTRUMENTS_SWEEPABLE_QUANTITIES_TAB_QUANTITY_FILTER_XPATH = '//*[text()=" Sweepable Quantities "]/parent::nb-accordion-item//*[@class="ng2-smart-th upperQty ng-star-inserted"]//input'

    CLIENT_TIER_INSTRUMENTS_SWEEPABLE_QUANTITIES_TAB_PUBLISHED_XPATH = '/html/body/ngx-app/ngx-pages/ngx-one-column-layout/nb-layout/div[1]/div/div/div/div/nb-layout-column/ngx-client-tier/ngx-ctis-wizard/div/nb-card/nb-card-body/div/nb-accordion/nb-accordion-item[6]/nb-accordion-item-body/div/div/ng2-smart-table/table/thead/tr[3]/td[3]/ng2-smart-table-cell/table-cell-edit-mode/div/table-cell-custom-editor/checkbox-custom-editor/form/nb-checkbox/label/span[1]'
    CLIENT_TIER_INSTRUMENTS_SWEEPABLE_QUANTITIES_TAB_PUBLISHED_FILTER_XPATH = '//*[text()=" Sweepable Quantities "]/parent::nb-accordion-item//*[@class="ng2-smart-th publishPrices ng-star-inserted"]//input'

    # tiered quantities tab
    CLIENT_TIER_INSTRUMENTS_TIERED_QUANTITIES_TAB_PLUS_BUTTON_XPATH = '//*[text()=" Tiered Quantities "]/parent::nb-accordion-item//*[@class="nb-plus"]'
    CLIENT_TIER_INSTRUMENTS_TIERED_QUANTITIES_TAB_CHECKMARK_BUTTON_XPATH = '//*[text()=" Tiered Quantities "]/parent::nb-accordion-item//*[@class="nb-checkmark"]'
    CLIENT_TIER_INSTRUMENTS_TIERED_QUANTITIES_TAB_CLOSE_BUTTON_XPATH = '//*[text()=" Tiered Quantities "]/parent::nb-accordion-item//*[@class="nb-close"]'
    CLIENT_TIER_INSTRUMENTS_TIERED_QUANTITIES_TAB_EDIT_BUTTON_XPATH = '//*[text()=" Tiered Quantities "]/parent::nb-accordion-item//*[@class="nb-edit"]'
    CLIENT_TIER_INSTRUMENTS_TIERED_QUANTITIES_TAB_DELETE_BUTTON_XPATH = '//*[text()=" Tiered Quantities "]/parent::nb-accordion-item//*[@class="nb-trash"]'

    CLIENT_TIER_INSTRUMENTS_TIERED_QUANTITIES_TAB_QUANTITY_XPATH = '//*[@placeholder ="Quantity *"]'
    CLIENT_TIER_INSTRUMENTS_TIERED_QUANTITIES_TAB_QUANTITY_FILTER_XPATH = '//*[text()=" Tiered Quantities "]/parent::nb-accordion-item//*[@class="ng2-smart-th upperQty ng-star-inserted"]//input'

    # tenors tab
    CLIENT_TIER_INSTRUMENTS_TENORS_TAB_PLUS_BUTTON_XPATH = '//*[text()=" Tenors "]/parent::nb-accordion-item//*[@class="nb-plus ng2-main-add-btn"]'
    CLIENT_TIER_INSTRUMENTS_TENORS_TAB_CHECKMARK_BUTTON_XPATH = '//*[text()=" Tenors "]/parent::nb-accordion-item//*[@class="nb-checkmark"]'
    CLIENT_TIER_INSTRUMENTS_TENORS_TAB_CLOSE_BUTTON_XPATH = '//*[text()=" Tenors "]/parent::nb-accordion-item//*[@class="nb-close"]'
    CLIENT_TIER_INSTRUMENTS_TENORS_TAB_EDIT_BUTTON_XPATH = '//*[text()=" Tenors "]/parent::nb-accordion-item//*[@class="nb-edit ng2-main-edit-btn"]'
    CLIENT_TIER_INSTRUMENTS_TENORS_TAB_DELETE_BUTTON_XPATH = '//*[text()=" Tenors "]/parent::nb-accordion-item//*[@class="nb-trash"]'

    CLIENT_TIER_INSTRUMENTS_TENORS_TAB_TENOR_XPATH = '//*[@placeholder ="Tenor *"]'
    CLIENT_TIER_INSTRUMENTS_TENORS_TAB_TENOR_FILTER_XPATH = '//*[@class ="tenor-table-body"]//*[@class="form-control ng-pristine ng-valid ng-touched"]'
    CLIENT_TIER_INSTRUMENTS_TENORS_TAB_MIN_SPREAD_XPATH = '//*[@formcontrolname ="minSpread"]'
    CLIENT_TIER_INSTRUMENTS_TENORS_TAB_MAX_SPREAD_XPATH = '//*[@formcontrolname ="maxSpread"]'
    CLIENT_TIER_INSTRUMENTS_TENORS_TAB_MARGIN_FORMAT_XPATH = '//*[@id ="marginPriceType"]'
    CLIENT_TIER_INSTRUMENTS_TENORS_TAB_EXECUTABLE_CHECKBOX_XPATH = '//*[text()="Executable"]//parent::span'
    CLIENT_TIER_INSTRUMENTS_TENORS_TAB_PRICING_CHECKBOX_XPATH = '//*[text()="Pricing"]//parent::span'
    CLIENT_TIER_INSTRUMENTS_TENORS_TAB_CLIENT_PRICE_SLIPPAGE_RANGE_CHECKBOX_XPATH = '//*[@formcontrolname ="validatePriceSlippage"]'
    CLIENT_TIER_INSTRUMENTS_TENORS_TAB_CLIENT_PRICE_SLIPPAGE_RANGE_XPATH = '//*[@formcontrolname ="validatePriceSlippage"]/input'
    CLIENT_TIER_INSTRUMENTS_TENORS_TAB_MINIMUM_PRICE_CHECKBOX_XPATH = '//*[@formcontrolname ="validateMinPrice"]'
    CLIENT_TIER_INSTRUMENTS_TENORS_TAB_MINIMUM_PRICE_XPATH = '//*[@formcontrolname ="validateMinPrice"]/input'
    CLIENT_TIER_INSTRUMENTS_TENORS_TAB_MAXIMUM_PRICE_CHECKBOX_XPATH = '//*[@formcontrolname ="validateMaxPrice"]'
    CLIENT_TIER_INSTRUMENTS_TENORS_TAB_MAXIMUM_PRICE_XPATH = '//*[@formcontrolname ="validateMaxPrice"]/input'
    CLIENT_TIER_INSTRUMENTS_TENORS_TAB_AUTOMATED_MARGIN_STRATEGIES_ENABLED_CHECKBOX_XPATH = '//*[text()="Automated Margin Strategies Enabled"]//parent::span'
    CLIENT_TIER_INSTRUMENTS_TENORS_TAB_POSITION_BASED_MARGINS_CHECKBOX_XPATH = '//*[text()="Position Based Margins"]//parent::span'
    CLIENT_TIER_INSTRUMENTS_TENORS_TAB_POSITION_BOOK_XPATH = '//*[@id ="monitoredPosAccountGroup"]'

    # base margins sub tab
    CLIENT_TIER_INSTRUMENTS_BASE_MARGINS_SUB_TAB_EDIT_BUTTON_XPATH = '//*[text()="Base Margins"]//parent::div//*[@class="nb-edit piloted-table-action"]'
    CLIENT_TIER_INSTRUMENTS_BASE_MARGINS_SUB_TAB_CHECKMARK_BUTTON_XPATH = '//*[text()="Base Margins"]//parent::div//*[@class="nb-checkmark"]'
    CLIENT_TIER_INSTRUMENTS_BASE_MARGINS_SUB_TAB_CLOSE_BUTTON_XPATH = '//*[text()="Base Margins"]//parent::div//*[@class="nb-close"]'
    CLIENT_TIER_INSTRUMENTS_BASE_MARGINS_SUB_TAB_QUANTITY_XPATH = '//*[text()="Base Margins"]//parent::div//*[@class="ng2-smart-row ng-star-inserted"]/td[2]//div//div'
    CLIENT_TIER_INSTRUMENTS_BASE_MARGINS_SUB_TAB_BID_MARGIN_XPATH = '//*[@placeholder ="Bid Margin"]'
    CLIENT_TIER_INSTRUMENTS_BASE_MARGINS_SUB_TAB_OFFER_MARGIN_XPATH = '//*[@placeholder ="Offer Margin"]'
    CLIENT_TIER_INSTRUMENTS_BASE_MARGINS_SUB_TAB_EXECUTABLE_CHECKBOX_XPATH = '/html/body/ngx-app/ngx-pages/ngx-one-column-layout/nb-layout/div[1]/div/div/div/div/nb-layout-column/ngx-client-tier/ngx-ctis-wizard/div/nb-card/nb-card-body/div/nb-accordion/nb-accordion-item[8]/nb-accordion-item-body/div/div/ngx-ctis-tenor-form/div/div[2]/div/div[2]/ng2-smart-table/table/tbody/tr[2]/td[5]/ng2-smart-table-cell/table-cell-edit-mode/div/table-cell-custom-editor/checkbox-custom-editor/form/nb-checkbox/label/input'
    CLIENT_TIER_INSTRUMENTS_BASE_MARGINS_SUB_TAB_PRICING_CHECKBOX_XPATH = '/html/body/ngx-app/ngx-pages/ngx-one-column-layout/nb-layout/div[1]/div/div/div/div/nb-layout-column/ngx-client-tier/ngx-ctis-wizard/div/nb-card/nb-card-body/div/nb-accordion/nb-accordion-item[8]/nb-accordion-item-body/div/div/ngx-ctis-tenor-form/div/div[2]/div/div[2]/ng2-smart-table/table/tbody/tr[2]/td[6]/ng2-smart-table-cell/table-cell-edit-mode/div/table-cell-custom-editor/checkbox-custom-editor/form/nb-checkbox/label/input'
    CLIENT_TIER_INSTRUMENTS_BASE_MARGINS_SUB_TAB_QUANTITY_FILTER_XPATH = '//*[@class="tenors-table-wrapper"]//*[@class= "ng2-smart-th upperQty ng-star-inserted"]//input'
    CLIENT_TIER_INSTRUMENTS_BASE_MARGINS_SUB_TAB_BID_MARGIN_FILTER_XPATH = '//*[@class= "defaultBidMargin ng2-smart-th ng-star-inserted"]//input'
    CLIENT_TIER_INSTRUMENTS_BASE_MARGINS_SUB_TAB_OFFER_MARGIN_FILTER_XPATH = '//*[@class= "defaultOfferMargin ng2-smart-th ng-star-inserted"]//input'
    CLIENT_TIER_INSTRUMENTS_BASE_MARGINS_SUB_TAB_EXECUTABLE_MARGIN_FILTER_XPATH = '//*[@class= "MDQuoteType ng2-smart-th ng-star-inserted"]//input'
    CLIENT_TIER_INSTRUMENTS_BASE_MARGINS_SUB_TAB_PRICING_FILTER_XPATH = '//*[@class= "activeQuote ng2-smart-th ng-star-inserted"]//input'

    # position levels sub tab
    CLIENT_TIER_INSTRUMENTS_POSITION_LEVELS_TAB_PLUS_BUTTON_XPATH = '//*[@class="tenors-table-wrapper"]//*[@class="nb-plus piloted-table-action"]'
    CLIENT_TIER_INSTRUMENTS_POSITION_LEVELS_TAB_CHECKMARK_BUTTON_XPATH = '//*[@class="tenors-table-wrapper"]//*[@class="nb-checkmark"]'
    CLIENT_TIER_INSTRUMENTS_POSITION_LEVELS_TAB_CLOSE_BUTTON_XPATH = '//*[@class="tenors-table-wrapper"]//*[@class="nb-close"]'
    CLIENT_TIER_INSTRUMENTS_POSITION_LEVELS_TAB_EDIT_BUTTON_XPATH = '//*[@class="tenors-table-wrapper"]//*[@class="nb-edit piloted-table-action"]'
    CLIENT_TIER_INSTRUMENTS_POSITION_LEVELS_TAB_DELETE_BUTTON_XPATH = '//*[@class="tenors-table-wrapper"]//*[@class="nb-trash piloted-table-action"]'

    CLIENT_TIER_INSTRUMENTS_POSITION_LEVELS_TAB_POSITION_XPATH = '//*[@placeholder ="Position (EUR) *"]'
    CLIENT_TIER_INSTRUMENTS_POSITION_LEVELS_TAB_POSITION_FILTER_XPATH = '//*[@class="tenors-table-wrapper"]//*[@class="ng2-smart-th sysCurrPositQty ng-star-inserted"]//input'

    CLIENT_TIER_INSTRUMENTS_POSITION_LEVELS_TAB_BID_MARGIN_XPATH = '//*[@placeholder ="Bid Margin"]'
    CLIENT_TIER_INSTRUMENTS_POSITION_LEVELS_TAB_BID_MARGIN_FILTER_XPATH = '//*[@class="tenors-table-wrapper"]//*[@class="bidMargin ng2-smart-th ng-star-inserted"]//input'

    CLIENT_TIER_INSTRUMENTS_POSITION_LEVELS_TAB_OFFER_MARGIN_XPATH = '//*[@placeholder ="Offer Margin"]'
    CLIENT_TIER_INSTRUMENTS_POSITION_LEVELS_TAB_OFFER_MARGIN_FILTER_XPATH = '//*[@class="tenors-table-wrapper"]//*[@class="ng2-smart-th offerMargin ng-star-inserted"]//input'
    # endregion

    # endregion
