class CounterpartsConstants:
    COUNTERPARTS_PAGE_TITLE_XPATH = "//span[@class='entity-title left'][text()='Counterparts ']"
    NAME_FILTER_XPATH = '//input[@class="ag-floating-filter-input"]'
    NAME_VALUE = '//div[@col-id="counterpartName"]//*[@ref="eValue"]'
    NEW_BUTTON = '//button[text()="New"]'
    REFRESH_BUTTON = '//*[@data-name="refresh"]'
    MORE_ACTIONS = '//*[@data-name="more-vertical"]'
    EDIT_AT_MORE_ACTIONS = '//*[@data-name="edit"]'
    CLONE_AT_MORE_ACTIONS = '//*[@data-name="copy"]'
    DELETE_AT_MORE_ACTIONS = '//*[@data-name="trash-2"]'

    # ----------------COUNTERPARTS WIZARD---------------
    NAME_AT_VALUES_TAB = '//*[@id="counterpartName"]'
    CHECK_MARK = '//*[@class="nb-checkmark"]'
    CLOSE_COUNTERPARTS_WIZARD = '//*[@data-name="close"]'
    CLOSE_CHANGES_AT_COUNTERPARTS_TABS = '//*[@class="nb-close"]'
    EDIT_AT_COUNTERPARTS_TABS = '//*[@class="nb-edit"]'
    DELETE_AT_COUNTERPARTS_TABS = '//*[@class="nb-trash"]'
    REVERT_CHANGES_AT_COUNTERPARTS_TAB = '//button[text()="Revert Changes"]'
    SAVE_CHANGES = '//*[text()="Save Changes"]'
    CLEAR_CHANGES = '//button[text()="Clear Changes"]'

    # ----------SUB_COUNTERPARTS_TAB----------
    PLUS_AT_SUB_COUNTERPARTS_TAB = '//nb-accordion//nb-accordion-item[2]//*[@class="nb-plus"]'
    NAME_AT_SUB_COUNTERPARTS_TAB = '//*[@placeholder="Name *"]'
    PARTY_ID_AT_SUB_COUNTERPARTS_TAB = '//*[@placeholder="Party ID *"]'
    EXT_ID_CLIENT_AT_SUB_COUNTERPARTS_TAB = '//*[@placeholder="Ext ID Client *"]'
    PARTY_SUB_ID_TYPE_AT_SUB_COUNTERPARTS_TAB = '//*[@placeholder="Party Sub ID Type *"]'
    # --FILTERS--
    NAME_FILTER_AT_SUB_COUNTERPARTS_TAB = '//*[contains(@class,"subCounterpartName")]//*[@placeholder="Filter"]'
    PARTY_ID_FILTER_AT_SUB_COUNTERPARTS_TAB = '//*[contains(@class,"SubCounterpartID ")]//*[@placeholder="Filter"]'
    EXT_ID_CLIENT_FILTER_AT_SUB_COUNTERPARTS_TAB = '//*[contains(@class,"clientSubCounterpartID ")]//*[@placeholder="Filter"]'
    PARTY_SUB_ID_TYPE_FILTER_AT_SUB_TYPE = '//*[contains(@class,"partySubIDType")]//*[@placeholder="Filter"]'
    # --Values--
    NAME_VALUE_AT_SUB_COUNTERPARTS_TAB = '//*[@class="ng-tns-c93-87 ng-star-inserted"]//*//td[2]//div[@class="ng-star-inserted"]'
    PARTY_ID_VALUE_AT_SUB_COUNTERPARTS_TAB = '//*[@class="ng-tns-c93-87 ng-star-inserted"]//*//td[3]//div[@class="ng-star-inserted"]'
    EXT_ID_VALUE_CLIENT_AT_SUB_COUNTERPARTS_TAB = '//*[@class="ng-tns-c93-87 ng-star-inserted"]//*//td[4]//div[@class="ng-star-inserted"]'
    PARTY_SUB_ID_VALUE_TYPE_AT_SUB_COUNTERPARTS_TAB = '//*[@class="ng-tns-c93-87 ng-star-inserted"]//*//td[5]//div[@class="ng-star-inserted"]'

    # ----------PARTY_ROLES_TAB---------
    PLUS_BUTTON_AT_PARTY_ROLES_TAB = '//nb-accordion//nb-accordion-item[3]//*[@class="nb-plus"]'
    PARTY_ID_SOURCE_AT_PARTY_ROLES_TAB = '//*[@placeholder="Party ID Source *"]'
    VENUE_COUNTERPART_ID_AT_PARTY_ROLES_TAB = '//*[@placeholder="Venue Counterpart ID *"]'
    PARTY_ROLE_AT_PARTY_ROLES_TAB = '//*[@placeholder="Party Role *"]'
    EXT_ID_CLIENT_AT_PARTY_ROLES_TAB = '//*[@placeholder="Ext ID Client *"]'
    PARTY_ROLE_QUALIFIER_AT_PARTY_ROLES_TAB = '//*[@placeholder="Party Role Qualifier *"]'
    VENUE_AT_PARTY_ROLES_TAB = '//*[@placeholder="Venue *"]'
    # --FILTERS--
    PARTY_ID_SOURCE_FILTER_AT_PARTY_ROLES_TAB = '//*[contains(@class,"partyIDSource")]//*[@placeholder="Filter"]'
    VENUE_COUNTERPART_ID_FILTER_AT_PARTY_ROLES_TAB = '//*[contains(@class,"venueCounterpartID")]//*[@placeholder="Filter"]'
    PARTY_ROLE_FILTER_AT_PARTY_ROLES_TAB = '//*[contains(@class,"partyRole ")]//*[@placeholder="Filter"]'
    EXT_ID_CLIENT_FILTER_AT_PARTY_ROLES_TAB = '//*[contains(@class,"clientCounterpartID")]//*[@placeholder="Filter"]'
    PARTY_ROLE_QUALIFIER_FILTER_AT_PARTY_ROLES_TAB = '//*[contains(@class,"partyRoleQualifier")]//*[@placeholder="Filter"]'
    VENUE_FILTER_AT_PARTY_ROLES_TAB = '//*[contains(@class,"venue ")]//*[@placeholder="Filter"]'
    # --Values--
    PARTY_ID_SOURCE_VALUE_AT_PARTY_ROLES_TAB = '//tr[@class="ng2-smart-row ng-star-inserted"]/td[2]//div[@class="ng-star-inserted"]'
    VENUE_COUNTERPART_ID_VALUE_AT_PARTY_ROLES_TAB = '//tr[@class="ng2-smart-row ng-star-inserted"]/td[3]//div[@class="ng-star-inserted"]'
    PARTY_ROLE_VALUE_AT_PARTY_ROLES_TAB = '//tr[@class="ng2-smart-row ng-star-inserted"]/td[4]//div[@class="ng-star-inserted"]'
    EXT_ID_CLIENT_VALUE_AT_PARTY_ROLES_TAB = '//tr[@class="ng2-smart-row ng-star-inserted"]/td[5]//div[@class="ng-star-inserted"]'
    PARTY_ROLE_QUALIFIER_VALUE_AT_PARTY_ROLES_TAB = '//tr[@class="ng2-smart-row ng-star-inserted"]/td[6]//div[@class="ng-star-inserted"]'
    VENUE_VALUE_AT_PARTY_ROLES_TAB = '//*[@class="ng2-smart-row ng-star-inserted"]/td[7]//custom-view-component[@class="ng-star-inserted"]'
