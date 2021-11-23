class RoutesConstants:
    ROUTES_PAGE_TITLE_XPATH = "//span[@class='entity-title left'][text()='Routes ']"
    #   -----Main page-----
    NAME_FILTER_XPATH = '//*[@class="ag-header-container"]//div[2]/div[1]//*[@class="ag-input-old_wrappers"]//input'
    DESCRIPTION_FILTER_XPATH = '//*[@class="ag-header-container"]//div[2]/div[2]//*[@class="ag-input-old_wrappers"]//input'
    ES_INSTANCE_FILTER_XPATH = '//*[@class="ag-header-container"]//div[2]/div[3]//*[@class="ag-input-old_wrappers"]//input'
    CLIENT_ID_FILTER_XPATH = '//*[@class="ag-header-container"]//div[2]/div[4]//*[@class="ag-input-old_wrappers"]//input'
    DEFAULT_STRATEGY_TYPE_FILTER_XPATH = '//*[@class="ag-header-container"]//div[2]/div[5]//*[@class="ag-input-old_wrappers"]//input'
    COUNTERPART_FILTER_XPATH = '//*[@class="ag-header-container"]//div[2]/div[6]//*[@class="ag-input-old_wrappers"]//input'
    SUPPORT_CONTRA_FIRM_COMMISSION_FILTER_XPATH = '//*[@class="ag-header-container"]//div[2]/div[7]//select'

    NAME_VALUE_XPATH = '//*[@class="ag-center-cols-container"]//*[@row-index="0"]//*[@col-id="routeName"]//*[@ref="eValue"]'
    DESCRIPTION_VALUE_XPATH = '//*[@class="ag-center-cols-container"]//*[@row-index="0"]//*[@col-id="routeDescription"]//*[@ref="eValue"]'
    ES_INSTANCE_VALUE_XPATH = '//*[@class="ag-center-cols-container"]//*[@row-index="0"]//*[@col-id="ESInstanceID"]//*[@ref="eValue"]'
    CLIENT_ID_VALUE_XPATH = '//*[@class="ag-center-cols-container"]//*[@row-index="0"]//*[@col-id="clientRouteID"]//*[@ref="eValue"]'
    DEFAULT_STRATEGY_TYPE_VALUE_XPATH = '//*[@class="ag-center-cols-container"]//*[@row-index="0"]//*[@col-id="defaultScenario.scenarioName"]//*[@ref="eValue"]'
    COUNTERPART_VALUE_XPATH = '//*[@class="ag-center-cols-container"]//*[@row-index="0"]//*[@col-id="counterpart.counterpartName"]//*[@ref="eValue"]'
    SUPPORT_CONTRA_FIRM_COMMISSION_VALUE_XPATH = '//*[@class="ag-center-cols-container"]//*[@row-index="0"]//*[@col-id="supportContraFirmCommission"]//input'

    # -at more actions-
    NEW_BUTTON_XPATH = '//button[text()="New"]'
    REFRESH_PAGE_XPATH = '//*[@data-name="refresh"]'
    MORE_ACTIONS_XPATH = '//*[@data-name="more-vertical"]'
    EDIT_AT_MORE_ACTIONS_XPATH = '//*[@data-name="edit"]'
    CLONE_AT_MORE_ACTIONS_XPATH = '//*[@data-name="copy"]'
    DELETE_AT_MORE_ACTIONS_XPATH = '//*[@nbtooltip="Delete"]'
    DOWNLOAD_PDF_XPATH = '//*[@class="nb-overlay-left"]//*[@data-name="download"]'
    PIN_ROW_AT_MORE_ACTIONS_XPATH = '//*[@nbtooltip = "Click to Pin Row"]'
    OK_BUTTON_AT_MORE_ACTIONS_XPATH = '//*[text()="Ok"]'
    CANCEL_BUTTON_AT_MORE_ACTIONS_XPATH ='//*[text()="Cancel"]'
    # ------Edit------

    # --Values tab--
    VENUE_FILTER_AT_VALUES_TAB_XPATH  ='//*[@class="ng2-smart-th venue ng-star-inserted"]//*[@placeholder="Filter"]'
    DOWNLOAD_PDF_AT_ROUTES_WIZARD = '//*[@data-name="download"]'
    CLOSE_PAGE_AT_ROUTES_WIZARD = '//*[@data-name="close"]'
    SAVE_CHANGES_AT_VALUES_TAB_XPATH = '//*[text()="Save Changes"]'
    REVERT_CHANGES_AT_VALUES_TAB_XPATH = '//*[text()="Revert Changes"]'
    NAME_AT_VALUES_TAB_XPATH = '//*[@formcontrolname="routeName"]'
    CLIENT_ID_AT_VALUES_TAB_XPATH = '//*[@formcontrolname="clientRouteID"]'
    ES_INSTANCE_AT_VALUES_TAB_XPATH = '//*[@formcontrolname="ESInstanceID"]'
    DESCRIPTION_AT_VALUES_TAB_XPATH = '//*[@id="routeDescription"]'
    COUNTERPART_AT_VALUES_TAB_XPATH = '//*[@id="counterpart"]'
    SUPPORT_CONTRA_FIRM_COMMISSION_AT_VALUES_TAB_XPATH ='//*[text()="Support Contra Firm Commission"]/parent::label'
    MANAGE_AT_VALUES_TAB_XPATH ='//*[text()="Manage"]'
    EXPECTED_ERROR_FOR_VALUE_FIELD_AT_VALUES_TAB_XPATH = "//*[text()='Incorrect or missing values']"
    #-Counterpart tab-
    NEW_BUTTON_AT_COUNTERPARTS_TAB_XPATH = '//*[text()="New"]'
    REFRESH_PAGE_AT_COUNTERPARTS_TAB_XPATH ='//*[@data-name="refresh"]'
    DOWNLOAD_CSV_AT_COUNTERPARTS_TAB_XPATH='//*[@data-name="download"]'
    NAME_FILTER_AT_COUNTERPARTS_TAB_XPATH = '//*[@class="ag-floating-filter-input"]'
    GO_BACK_BUTTON_AT_COUNTERPARTS_TAB_XPATH = '//*[text()="Go Back"]'

    # --Venues tab--
    EXISTING_VENUE_AT_VENUES_TAB = '//*[@class="venue-table-body"]//td[@class="ng-star-inserted"]'
    CHECK_MARK_AT_VENUES_TAB ='//*[@class="venue-table-body"]//*[@class="nb-checkmark"]'
    VENUE_AT_VENUES_TAB_XPATH = '//*[@placeholder="Venue *"]'
    PLUS_BUTTON_AT_VENUES_TAB_XPATH = '//*[@class="nb-plus ng2-main-add-btn"]'
    EDIT_VENUE_AT_VENUES_TAB_XPATH = '//*[@class="ng2-smart-action ng2-smart-action-edit-edit ng-star-inserted"]//*[@class= "nb-edit ng2-main-edit-btn" ][1]'
    DELETE_VENUE_AT_VENUES_TAB_XPATH = '//*[@class="ng2-smart-row selected ng-star-inserted"]//*[@class= "nb-trash" ][1]'
    VENUE_FILTER_AT_VENUES_TAB_XPATH = '//*[@class="venue-table-body"]//*[@placeholder="Filter"]'
    # -Venues edit/new wizard-

    ROUTE_VENUE_NAME_AT_VENUE_WIZARD_XPATH = '//*[text()="Route Venue Name"]/preceding-sibling::input[@formcontrolname="routeVenueName"]'
    MAIN_SECURITY_ID_SOURCE_VALUE_AT_VENUE_WIZARD_XPATH = '//*[@id="mainSecurityIDSource"]'
    ORD_ID_FORMAT_AT_VENUE_WIZARD_XPATH = '//*[@id="clOrdIDFormat"]'
    MIC_AT_VENUE_WIZARD_XPATH = '//*[@id="MIC"]'
    OUT_BOUND_CURRENCY1_AT_VENUE_WIZARD_XPATH = '//*[@id="outboundCurrency1"]'
    OUT_BOUND_CURRENCY2_AT_VENUE_WIZARD_XPATH = '//*[@id="outboundCurrency2"]'
    OUT_BOUND_CURRENCY3_AT_VENUE_WIZARD_XPATH = '//*[@id="outboundCurrency3"]'
    OUT_BOUND_CURRENCY4_AT_VENUE_WIZARD_XPATH = '//*[@id="outboundCurrency4"]'
    OUT_BOUND_CURRENCY5_AT_VENUE_WIZARD_XPATH = '//*[@id="outboundCurrency5"]'
    MAX_ORD_AMT_CURRENCY_AT_VENUE_WIZARD_XPATH = '//*[@id="maxOrdAmtCurrency"]'
    CURRENCY_DIFFERENT_THAN_AT_VENUE_WIZARD_XPATH ='//*[@id="currencyDifferentThan"]'
    MAX_ORD_AMT_AT_VENUE_WIZARD_XPATH ='//*[@id="maxOrdAmt"]'
    MAX_ORD_QTY_AT_VENUE_WIZARD_XPATH = '//*[@id="maxOrdQty"]'
    DISPLAY_QTY_MAX_PCT_OF_ORD_QTY = '//*[@id="displayQtyMaxPctOfOrdQty"]'
    #CHECKBOXES
    NATIVE_CHECKBOX_AT_VENUE_WIZARD_XPATH ='//*[text()="Native"]/parent::label'
    VENUE_MASS_CANCEL_AT_VENUE_WIZARD_XPATH ='//*[text()="Venue MassCancel"]/parent::label'
    LISTING_GROUP_MASS_CANCEL_CHECKBOX_AT_VENUE_WIZARD_XPATH = '//*[text()="ListingGroup MassCancel"]/parent::label'
    INDIVIDUAL_EXEC_UPDATE_TRANSAC_AT_VENUE_WIZARD_XPATH ='//*[text()="Individual Exec Update Transac"]/parent::label'
    SKIP_MD_VALIDATIONS_AT_VENUE_WIZARD_XPATH = '//*[text()="Skip MD Validations"]/parent::label'
    SUBVENUE_MASS_CANCEL_AT_VENUE_WIZARD_XPATH ='//*[text()="SubVenue MassCancel"]/parent::label'
    INSTR_TYPE_MASS_CANCEL_AT_VENUE_WIZARD_XPATH ='//*[text()="InstrType MassCancel"]/parent::label'
    SUPPORT_TRADING_PHASE_AT_VENUE_WIZARD_XPATH ='//*[text()="Support Trading Phase"]/parent::label'
    MASS_CANCEL_CHECKBOX_AT_VENUE_WIZARD_XPATH ='//*[text()="MassCancel"]/parent::label'
    LISTING_MASS_CANCEL_AT_VENUE_WIZARD_XPATH= '//*[text()="Listing MassCancel"]/parent::label'
    INSTR_SUB_TYPE_MASS_CANCEL_AT_VENUE_WIZARD_XPATH = '//*[text()="InstrSubType MassCancel"]/parent::label'
    ORD_AMT_LESS_THAN_STD_MKT_SIZE_AT_VENUE_WIZARD_XPATH = '//*[text()="Ord Amt Less Than Std Mkt Size"]/parent::label'
    PLUS_BUTTON_AT_VENUE_WIZARD_XPATH ='//*[@class="venue-form-body hidden-form-div"]//*[@class="nb-plus piloted-table-action"]'
    #-------Trading phase wizard
    TRADING_PHASE_VALUE_AT_VENUE_SUB_WIZARD_XPATH ='//*[@placeholder="Trading Phase *"]'
    ORD_TYPE_VALUE_AT_VENUE_SUB_WIZARD_XPATH = '//*[@placeholder="Ord Type *"]'
    OUTPUT_ORD_TYPE_VALUE_AT_VENUE_SUB_WIZARD_XPATH = '//*[@placeholder="Output Ord Type *"]'
    TRADING_PHASE_FILTER_AT_VENUE_SUB_WIZARD_XPATH = '//*[@class="ng2-smart-th tradingPhase ng-star-inserted"]//input'
    ORD_TYPE_FILTER_AT_VENUE_SUB_WIZARD_XPATH = '//*[@class="ng2-smart-th ordType ng-star-inserted"]//input'
    OUTPUT_ORD_TYPE_FILTER_AT_VENUE_SUB_WIZARD_XPATH = '//*[@class="ng2-smart-th outputOrdType ng-star-inserted"]//input'
    CHECK_MARK_BUTTON_AT_VENUE_SUB_WIZARD_XPATH = '//*[@class="tenors-table-old_wrappers"]//*[@class="nb-checkmark"]'
    CLOSE_AT_VENUE_SUB_WIZARD_XPATH ='//*[@class="tenors-table-old_wrappers"]//*[@class="nb-close piloted-table-action"]'
    EDIT_BUTTON_AT_VENUE_SUB_WIZARD_XPATH ='//*[@class="tenors-table-old_wrappers"]//*[@class="nb-edit piloted-table-action"]'
    DELETE_BUTTON_AT_VENUE_SUB_WIZARD_XPATH ='//*[@class="tenors-table-old_wrappers"]//*[@class="nb-trash piloted-table-action"]'

    MANAGE_TYPE_TIF_BUTTON_AT_VENUE_SUB_WIZARD_XPATH ='//*[text()=" Manage Type TIF "]/parent::button-custom-editor[@class="ng-star-inserted"]'
    #Manage type tif wizard
    PLUS_BUTTON_AT_MANAGE_TYPE_TIF_WIZARD_XPATH = '//*[@class="rvptt-form"]//*[@class="nb-plus"]'
    EDIT_BUTTON_AT_MANAGE_TYPE_TIF_WIZARD_XPATH ='//*[@class="rvptt-form"]//*[@class="nb-edit"]'
    DELETE_BUTTON_AT_MANAGE_TYPE_TIF_WIZARD_XPATH ='//*[@class="rvptt-form"]//*[@class="nb-trash"]'
    CHECK_MARK_BUTTON_AT_MANAGE_TYPE_TIF_WIZARD_XPATH = '//*[@class="rvptt-form"]//*[@class="nb-checkmark"]'
    CLOSE_AT_MANAGE_TYPE_TIF_WIZARD_XPATH = '//*[@class="rvptt-form"]//*[@class="nb-close"]'

    TIME_IN_FORCE_AT_MANAGE_TYPE_TIF_WIZARD_XPATH = '//*[@placeholder = "Time In Force *"]'
    ORD_TYPE_AT_MANAGE_TYPE_TIF_WIZARD_XPATH = '//*[@class="rvptt-form"]//*[@placeholder = "Ord Type *"]'
    SUPPORT_DISPLAY_QUANTITY_CHECKBOX_AT_MANAGE_TYPE_TIF_WIZARD_XPATH ='//*[@class="rvptt-form"]//*[@class ="custom-checkbox"]'
    TIME_IN_FORCE_FILTER_AT_MANAGE_TYPE_TIF_WIZARD_XPATH ='//*[@class="ng2-smart-th timeInForce ng-star-inserted"]//input'
    ORD_TYPE_AT_FILTER_MANAGE_TYPE_TIF_WIZARD_XPATH ='//*[@class="ng2-smart-th ordType ng-star-inserted"]//input'
    SUPPORT_DISPLAY_QUANTITY_FILTER_AT_MANAGE_TYPE_TIF_WIZARD_XPATH  ='//*[@class="ng2-smart-th supportDisplayQty ng-star-inserted"]//input'
    OK_AT_MANAGE_TYPE_TIF_WIZARD_XPATH = '//*[text()="OK"]'

    TIME_IN_FORCE_VALUE_AT_MANAGE_TYPE_TIF_WIZARD_XPATH = '//*[@class="ng2-smart-row ng-star-inserted"]//td[2]//div[@class="ng-star-inserted"]'
    ORD_TYPE_VALUE_AT_MANAGE_TYPE_TIF_WIZARD_XPATH ='//*[@class="ng2-smart-row ng-star-inserted"]//td[3]//div[@class="ng-star-inserted"]'
    SUPPORT_DISPLAY_QUANTITY_VALUE_AT_MANAGE_TYPE_TIF_WIZARD_XPATH = '//*[@class="ng2-smart-row ng-star-inserted"]//td[4]//div[@class="ng-star-inserted"]'

    # --Instr Symbols--
    PLUS_BUTTON_AT_INSTR_SYMBOLS_TAB_XPATH ='//*[@class ="ng-tns-c93-67 ng-star-inserted"]//*[@class="nb-plus"]'
    CHECK_MARK_BUTTON_AT_INSTR_SYMBOLS_TAB_XPATH ='//*[@class ="ng-tns-c93-67 ng-star-inserted"]//*[@class="nb-checkmark"]'
    CLOSE_BUTTON_AT_INSTR_SYMBOLS_TAB_XPATH ='//*[@class ="ng-tns-c93-67 ng-star-inserted"]//*[@class="nb-close"]'
    EDIT_BUTTON_AT_INSTR_SYMBOLS_TAB_XPATH ='//*[@class ="ng-tns-c93-67 ng-star-inserted"]//*[@class="nb-edit"]'
    DELETE_BUTTON_AT_INSTR_SYMBOLS_TAB_XPATH ='//*[@class ="ng-tns-c93-67 ng-star-inserted"]//*[@class="nb-trash"]'
    INSTR_SYMBOL_AT_INSTR_SYMBOLS_TAB_XPATH ='//*[@placeholder="Instr Symbol *"]'
    PRICE_MULTIPLIER_AT_INSTR_SYMBOLS_TAB_XPATH ='//*[@placeholder="Price Multiplier"]'
    INSTR_SYMBOL_FILTER_AT_INSTR_SYMBOLS_TAB_XPATH='//*[@class="instrSymbol ng2-smart-th ng-star-inserted"]//input'
    PRICE_MULTIPLIER_FILTER_AT_INSTR_SYMBOLS_TAB_XPATH='//*[@class="ng2-smart-th priceMultiplier ng-star-inserted"]//input'
    INSTR_SYMBOL_VALUE_AT_INSTR_SYMBOLS_TAB_XPATH ='//*[@class="ng-tns-c93-1533 ng-star-inserted"]//*[@class="ng2-smart-row ng-star-inserted selected"]//td[2]//div[@class="ng-star-inserted"]'
    PRICE_MULTIPLIER_VALUE_AT_INSTR_SYMBOLS_TAB_XPATH = '//*[@class="ng-tns-c93-1533 ng-star-inserted"]//*[@class="ng2-smart-row ng-star-inserted selected"]//td[3]//div[@class="ng-star-inserted"]'

    # --Strategy Type--
    STRATEGY_TYPE_AT_STRATEGY_TYPE_TAB_XPATH = '//*[@formcontrolname ="routeScenario"]//button'
    DEFAULT_SCENARIO_AT_STRATEGY_TYPE_TAB_XPATH = '//*[text()="Default Scenario"]/preceding-sibling::input'
    CHECKBOX_LIST_AT_STRATEGY_TYPE_TAB_XPATH ='//*[@class="cdk-overlay-pane"]//*[text()="{}"]'

















































