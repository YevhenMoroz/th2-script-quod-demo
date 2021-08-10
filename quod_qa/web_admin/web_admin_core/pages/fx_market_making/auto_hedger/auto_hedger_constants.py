class AutoHedgerConstants:
    AUTO_HEDGER_PAGE_TITLE_XPATH = "//span[@class='entity-title left'][text()='Auto Hedger ']"

    REFRESH_PAGE_BUTTON_XPATH = "//*[@data-name='refresh']"
    DOWNLOAD_PDF_BUTTON_XPATH = "//*[@data-name='download']"
    SAVE_CHANGES_BUTTON_XPATH = "//*[text()='Save Changes']"
    CLEAR_CHANGES_BUTTON_XPATH = "//*[text()='Clear Changes']"
    CLOSE_WIZARD_XPATH = "//*[@data-name='close']"
    OK_BUTTON_XPATH = '//*[text()="Ok"]'
    CANCEL_BUTTON_XPATH = '//*[text()="Cancel"]'
    REVERT_CHANGES_XPATH = "//*[text()='Revert Changes']"

    # Values tab
    VALUES_TAB_NAME_FIELD_XPATH = '//*[text()= "Name *"]'
    VALUES_TAB_POSITION_BOOK_FIELD_XPATH = '//*[text()= "Position Book"]'

    # Schedules tab

    SCHEDULES_TAB_ENABLE_SCHEDULE_CHECKBOX_XPATH = "//*[text()='Enable Schedule']/preceding-sibling::span"
    # schedules schedules
    SCHEDULES_TAB_PLUS_BUTTON_XPATH = "//*[@class='schedule']//*[@class='nb-plus']"
    SCHEDULES_TAB_CHECKMARK_BUTTON_XPATH = "//*[@class='schedule']//*[@class='nb-checkmark']"
    SCHEDULES_TAB_CLOSE_BUTTON_XPATH = "//*[@class='schedule']//*[@class='nb-close']"
    SCHEDULES_TAB_EDIT_BUTTON_XPATH = '//*[@class="schedule"]//*[@class="nb-edit"]'
    SCHEDULES_TAB_DELETE_BUTTON_XPATH = '//*[@class="schedule"]//*[@class="nb-trash"]'

    SCHEDULES_TAB_DAY_XPATH = "//*[@class='schedule']//*[@placeholder='Day *']"
    SCHEDULES_TAB_DAY_FILTER_XPATH = "//*[@class='schedule']//*[@class='ng2-smart-th weekDay ng-star-inserted']//input-filter"
    SCHEDULES_TAB_FROM_TIME_XPATH = "//*[@class='schedule']//*[@placeholder='From Time *']"
    SCHEDULES_TAB_FROM_TIME_FILTER_XPATH = "//*[@class='schedule']//*[@class='ng2-smart-th scheduleFromTime ng-star-inserted']//input-filter"
    SCHEDULES_TAB_TO_TIME_XPATH = "//*[@class='schedule']//*[@placeholder='To Time *']"
    SCHEDULES_TAB_TO_TIME_FILTER_XPATH = "//*[@class='schedule']//*[@class='ng2-smart-th scheduleToTime ng-star-inserted']//input-filter"

    # schedules exceptions
    SCHEDULES_EXCEPTIONS_TAB_PLUS_BUTTON_XPATH = "//*[@class='schedule-excep']//*[@class='nb-plus']"
    SCHEDULES_EXCEPTIONS_TAB_CHECKMARK_BUTTON_XPATH = "//*[@class='schedule-excep']//*[@class='nb-checkmark']"
    SCHEDULES_EXCEPTIONS_TAB_CLOSE_BUTTON_XPATH = "//*[@class='schedule-excep']//*[@class='nb-close']"

    SCHEDULES_EXCEPTIONS_TAB_EXCEPTION_DAY_XPATH = "//*[@class='schedule-excep']//*[@placeholder='Exception Date *']"
    SCHEDULES_EXCEPTIONS_TAB_EXCEPTION_DAY_FILTER_XPATH = "//*[@class='schedule-excep']//*[@class='ng2-smart-th scheduleExceptionDate ng-star-inserted']//input-filter"
    SCHEDULES_EXCEPTIONS_TAB_FROM_TIME_XPATH = "//*[@class='schedule-excep']//*[@placeholder='From Time *']"
    SCHEDULES_EXCEPTIONS_TAB_FROM_TIME_FILTER_XPATH = "//*[@class='schedule-excep']//*[@class='ng2-smart-th scheduleFromTime ng-star-inserted']//input-filter"
    SCHEDULES_EXCEPTIONS_TAB_TO_TIME_XPATH = "//*[@class='schedule-excep']//*[@placeholder='To Time *']"
    SCHEDULES_EXCEPTIONS_TAB_TO_TIME_FILTER_XPATH = "//*[@class='schedule-excep']//*[@class='ng2-smart-th scheduleToTime ng-star-inserted']//input-filter"

    # External clients tab
    EXTERNAL_CLIENTS_TAB_CLIENT_GROUP_FIELD_XPATH = '//*[text()="Client Group"]'
    EXTERNAL_CLIENTS_TAB_PLUS_BUTTON_XPATH = '//*[text()=" External Clients "]/parent::nb-accordion-item//*[@class="nb-plus"]'
    EXTERNAL_CLIENTS_TAB_CANCEL_BUTTON_XPATH = '//*[text()=" External Clients "]/parent::nb-accordion-item//*[@class="nb-close"]'
    EXTERNAL_CLIENTS_TAB_CHECKMARK_BUTTON_XPATH = '//*[text()=" External Clients "]/parent::nb-accordion-item//*[@class="nb-checkmark"]'
    EXTERNAL_CLIENTS_TAB_EDIT_BUTTON_XPATH = '//*[text()=" External Clients "]/parent::nb-accordion-item//*[@class="nb-edit"]'
    EXTERNAL_CLIENTS_TAB_DELETE_BUTTON_XPATH = '//*[text()=" External Clients "]/parent::nb-accordion-item//*[@class="nb-trash"]'
    EXTERNAL_CLIENTS_TAB_CLIENT_FIELD_XPATH = '//*[text()=" External Clients "]/parent::nb-accordion-item//*[@placeholder="Client *"]'
    EXTERNAL_CLIENTS_TAB_CLIENT_FILTER_XPATH = '//*[text()=" External Clients "]/parent::nb-accordion-item//*[@class="accountGroup ng2-smart-th ng-star-inserted"]//input'

    # Internal clients tab
    INTERNAL_CLIENTS_TAB_PLUS_BUTTON_XPATH = '//*[text()=" Internal Clients "]/parent::nb-accordion-item//*[@class="nb-plus"]'
    INTERNAL_CLIENTS_TAB_CANCEL_BUTTON_XPATH = '//*[text()=" Internal Clients "]/parent::nb-accordion-item//*[@class="nb-close"]'
    INTERNAL_CLIENTS_TAB_CHECKMARK_BUTTON_XPATH = '//*[text()=" Internal Clients "]/parent::nb-accordion-item//*[@class="nb-checkmark"]'
    INTERNAL_CLIENTS_TAB_EDIT_BUTTON_XPATH = '//*[text()=" Internal Clients "]/parent::nb-accordion-item//*[@class="nb-edit"]'
    INTERNAL_CLIENTS_TAB_DELETE_BUTTON_XPATH = '//*[text()=" Internal Clients "]/parent::nb-accordion-item//*[@class="nb-trash"]'
    INTERNAL_CLIENTS_TAB_CLIENT_FIELD_XPATH = '//*[text()=" Internal Clients "]/parent::nb-accordion-item//*[@placeholder="Client *"]'
    INTERNAL_CLIENTS_TAB_CLIENT_FILTER_XPATH = '//*[text()=" Internal Clients "]/parent::nb-accordion-item//*[@class="accountGroup ng2-smart-th ng-star-inserted"]//input'

    # Instruments tab

    INSTRUMENTS_TAB_PLUS_BUTTON_XPATH = '//*[text()=" Instruments "]/parent::nb-accordion-item//*[@class="nb-plus ng2-main-add-btn"]'
    INSTRUMENTS_TAB_CHECKMARK_BUTTON_XPATH = '//*[text()=" Instruments "]/parent::nb-accordion-item//*[@class="nb-checkmark"]'
    INSTRUMENTS_TAB_CANCEL_BUTTON_XPATH = '//*[text()=" Instruments "]/parent::nb-accordion-item//*[@class="nb-close ng2-main-cancel-btn"]'
    INSTRUMENTS_TAB_DELETE_BUTTON_XPATH = '//*[text()=" Instruments "]/parent::nb-accordion-item//*[@class="nb-trash"]'
    INSTRUMENTS_TAB_EDIT_BUTTON_XPATH = '//*[text()=" Instruments "]/parent::nb-accordion-item//*[@class="nb-edit ng2-main-edit-btn"]'
    INSTRUMENTS_TAB_SYMBOL_FILTER_XPATH = '/*[text()=" Instruments "]/parent::nb-accordion-item//*[@class="instrSymbol ng2-smart-th ng-star-inserted"]//input'
    INSTRUMENTS_TAB_SYMBOL_FIELD_XPATH = '/*[@placeholder="Symbol *"]'
    INSTRUMENTS_TAB_HEDGING_STRATEGY_FIELD_XPATH = '//*[text()="Hedging Strategy *"]'
    INSTRUMENTS_TAB_LONG_THRESHOLD_QTY_FIELD_XPATH = '//*[text()="Long Threshold Qty (EUR)"]'
    INSTRUMENTS_TAB_LONG_RESIDUAL_QTY_FIELD_XPATH = '//*[text()="Long Residual Qty (EUR)"]'
    INSTRUMENTS_TAB_SHORT_THRESHOLD_QTY_FIELD_XPATH = '//*[text()="Short Threshold Qty (EUR)"]'
    INSTRUMENTS_TAB_SHORT_RESIDUAL_QTY_FIELD_XPATH = '//*[text()="Short Residual Qty (EUR)"]'
    # checkboxes
    INSTRUMENTS_TAB_USE_LONG_QUANTITIES_AS_BOTH_LONG_AND_SHORT_CHECKBOX_XPATH = '//*[text()="Use Long Quantities as Both Long and Short"]'
    INSTRUMENTS_TAB_MAINTAIN_HEDGE_POSITIONS_CHECKBOX_XPATH = '//*[text()="Maintain Hedge Positions"]'
    INSTRUMENTS_TAB_SEND_HEDGE_ORDER_FIELD_XPATH = '//*[@id ="hedgeOrderDestination"]'
    INSTRUMENTS_TAB_SEND_HEDGE_ORDER_CHECKBOX_XPATH = '/html/body/ngx-app/ngx-pages/ngx-one-column-layout/nb-layout/div[1]/div/div/div/div/nb-layout-column/ngx-auto-hedger/ngx-ah-wizard/div/nb-card/nb-card-body/div/nb-accordion/nb-accordion-item[5]/nb-accordion-item-body/div/div/ngx-ah-instrument-form/div/div[2]/form/div[3]/div[3]/div/div[1]/nb-checkbox/label/span[1]'
    INSTRUMENTS_TAB_SYNTHETIC_COMBINATION_TO_AUTO_HEDGE_FIELD_XPATH = '//*[text()="Synthetic Combination to Auto-Hedge"]'
    INSTRUMENTS_TAB_HEDGING_EXECUTION_STRATEGY_FIELD_XPATH = '//*[text()= "Hedging Execution Strategy"]'
    INSTRUMENTS_TAB_HEDGING_EXECUTION_STRATEGY_TIF_FIELD_XPATH = '//*[text()= "Hedging Execution Strategy TIF"]'
    INSTRUMENTS_TAB_HEDGING_EXECUTION_STRATEGY_MAX_DURATION_FIELD_XPATH = '//*[text()= "Hedging Execution Strategy Max Duration (sec)"]'
