class CounterpartsConstants:
    OTHERS_PAGE_XPATH = '//*[text()="Others"]'
    COUNTERPARTS_PAGE_TITLE_XPATH = "//*[text()='Counterparts']"
    NAME_FILTER_XPATH = '//input[@class="ag-floating-filter-input"]'
    NAME_VALUE_XPATH = '//div[@col-id="counterpartName"]//*[@ref="eValue"]'
    NEW_BUTTON_XPATH = '//button[text()="New"]'
    REFRESH_BUTTON_XPATH = '//*[@data-name="refresh"]'
    MORE_ACTIONS_XPATH = '//*[@data-name="more-vertical"]'
    EDIT_AT_MORE_ACTIONS_XPATH = '//*[@data-name="edit"]'
    CLONE_AT_MORE_ACTIONS_XPATH = '//*[@data-name="copy"]'
    DELETE_AT_MORE_ACTIONS_XPATH = '//*[@data-name="trash-2"]'
    CANCEL_BUTTON_XPATH = '//*[text()="Cancel"]'
    OK_BUTTON_XPATH = '//*[text()="Ok"]'

    # ----------------COUNTERPARTS WIZARD---------------
    NAME_AT_VALUES_TAB_XPATH = '//input[@id="counterpartName"]'
    CHECK_MARK_XPATH = '//*[@data-name="checkmark"]'
    CLOSE_COUNTERPARTS_WIZARD_XPATH = '//*[@data-name="close"]'
    CLOSE_CHANGES_AT_COUNTERPARTS_TABS_XPATH = '//*[@class="nb-close"]'
    EDIT_AT_SUB_COUNTERPARTS_TAB_XPATH = '//div[@class="counterpart-detail-settings"]//nb-accordion-item[2]//*[@data-name="edit"]'
    EDIT_AT_PARTY_ROLES_TAB_XPATH = '//div[@class="counterpart-detail-settings"]//nb-accordion-item[3]//*[@data-name="edit"]'
    DELETE_AT_COUNTERPARTS_TABS_XPATH = '//div[@class="counterpart-detail-settings"]//nb-accordion-item[2]//*[@data-name="trash-2"]'
    DELETE_AT_PARTY_ROLES_TABS_XPATH = '//div[@class="counterpart-detail-settings"]//nb-accordion-item[3]//*[@data-name="trash-2"]'
    REVERT_CHANGES_AT_COUNTERPARTS_TAB_XPATH = '//button[text()="Revert Changes"]'
    SAVE_CHANGES_XPATH = '//*[text()="Save Changes"]'
    CLEAR_CHANGES_XPATH = '//button[text()="Clear Changes"]'
    DOWNLOAD_PDF_XPATH = '//*[@class="nb-overlay-left"]//*[@data-name="download"]'
    DOWNLOAD_PDF_IN_EDIT_WIZARD_XPATH = "//nb-icon[@icon='download-outline']//*[@data-name='download']"

    # ----------SUB_COUNTERPARTS_TAB----------
    PLUS_AT_SUB_COUNTERPARTS_TAB_XPATH = '//nb-accordion//nb-accordion-item[2]//*[@data-name="plus"]'
    NAME_AT_SUB_COUNTERPARTS_TAB_XPATH = '//*[@placeholder="Name *"]'
    PARTY_ID_AT_SUB_COUNTERPARTS_TAB_XPATH = '//*[@placeholder="Party ID"]'
    EXT_ID_CLIENT_AT_SUB_COUNTERPARTS_TAB_XPATH = '//*[@placeholder="Ext ID Client"]'
    PARTY_SUB_ID_TYPE_AT_SUB_COUNTERPARTS_TAB_XPATH = '//*[@placeholder="Party Sub ID Type *"]'
    # --FILTERS--
    NAME_FILTER_AT_SUB_COUNTERPARTS_TAB_XPATH = '//*[contains(@class,"subCounterpartName")]//*[@placeholder="Filter"]'
    PARTY_ID_FILTER_AT_SUB_COUNTERPARTS_TAB_XPATH = '//*[contains(@class,"SubCounterpartID ")]//*[@placeholder="Filter"]'
    EXT_ID_CLIENT_FILTER_AT_SUB_COUNTERPARTS_TAB_XPATH = '//*[contains(@class,"clientSubCounterpartID ")]//*[@placeholder="Filter"]'
    PARTY_SUB_ID_TYPE_FILTER_AT_SUB_TYPE_XPATH = '//*[contains(@class,"partySubIDType")]//*[@placeholder="Filter"]'
    # --Values--
    NAME_VALUE_AT_SUB_COUNTERPARTS_TAB_XPATH = '//*[text()=" Sub counterparts "]/parent::*[@class="expanded"]//td[2]//span[@class="ng-star-inserted"]'
    PARTY_ID_VALUE_AT_SUB_COUNTERPARTS_TAB_XPATH = '//*[text()=" Sub counterparts "]/parent::*[@class="expanded"]//td[3]//span[@class="ng-star-inserted"]'
    EXT_ID_VALUE_CLIENT_AT_SUB_COUNTERPARTS_TAB_XPATH = '//*[text()=" Sub counterparts "]/parent::*[@class="expanded"]//td[4]//span[@class="ng-star-inserted"]'
    PARTY_SUB_ID_VALUE_TYPE_AT_SUB_COUNTERPARTS_TAB_XPATH = '//*[text()=" Sub counterparts "]/parent::*[@class="expanded"]//td[5]//span[@class="ng-star-inserted"]'

    # ----------PARTY_ROLES_TAB---------
    PLUS_BUTTON_AT_PARTY_ROLES_TAB_XPATH = '//nb-accordion//nb-accordion-item[3]//*[@data-name="plus"]'
    PARTY_ID_SOURCE_AT_PARTY_ROLES_TAB_XPATH = '//*[@placeholder="Party ID Source *"]'
    VENUE_COUNTERPART_ID_AT_PARTY_ROLES_TAB_XPATH = '//*[@placeholder="Venue Counterpart ID *"]'
    PARTY_ROLE_AT_PARTY_ROLES_TAB_XPATH = '//*[@placeholder="Party Role *"]'
    EXT_ID_CLIENT_AT_PARTY_ROLES_TAB_XPATH = '//*[@placeholder="Ext ID Client *"]'
    PARTY_ROLE_QUALIFIER_AT_PARTY_ROLES_TAB_XPATH = '//*[@placeholder="Party Role Qualifier"]'
    VENUE_AT_PARTY_ROLES_TAB_XPATH = '//*[@placeholder="Venue"]'
    # --FILTERS--
    PARTY_ID_SOURCE_FILTER_AT_PARTY_ROLES_TAB_XPATH = '//*[contains(@class,"partyIDSource")]//*[@placeholder="Filter"]'
    VENUE_COUNTERPART_ID_FILTER_AT_PARTY_ROLES_TAB_XPATH = '//*[contains(@class,"venueCounterpartID")]//*[@placeholder="Filter"]'
    PARTY_ROLE_FILTER_AT_PARTY_ROLES_TAB_XPATH = '//*[contains(@class,"partyRole ")]//*[@placeholder="Filter"]'
    EXT_ID_CLIENT_FILTER_AT_PARTY_ROLES_TAB_XPATH = '//*[contains(@class,"clientCounterpartID")]//*[@placeholder="Filter"]'
    PARTY_ROLE_QUALIFIER_FILTER_AT_PARTY_ROLES_TAB_XPATH = '//*[contains(@class,"partyRoleQualifier")]//*[@placeholder="Filter"]'
    VENUE_FILTER_AT_PARTY_ROLES_TAB_XPATH = '//*[contains(@class,"venue ")]//*[@placeholder="Filter"]'
    # --Values--
    PARTY_ID_SOURCE_VALUE_AT_PARTY_ROLES_TAB_XPATH = '//*[text()=" Party roles "]/parent::*[@class="expanded"]//td[2]//span[@class="ng-star-inserted"]'
    VENUE_COUNTERPART_ID_VALUE_AT_PARTY_ROLES_TAB_XPATH = '//*[text()=" Party roles "]/parent::*[@class="expanded"]//td[3]//span[@class="ng-star-inserted"]'
    PARTY_ROLE_VALUE_AT_PARTY_ROLES_TAB_XPATH = '//*[text()=" Party roles "]/parent::*[@class="expanded"]//td[4]//span[@class="ng-star-inserted"]'
    EXT_ID_CLIENT_VALUE_AT_PARTY_ROLES_TAB_XPATH = '//*[text()=" Party roles "]/parent::*[@class="expanded"]//td[5]//span[@class="ng-star-inserted"]'
    PARTY_ROLE_QUALIFIER_VALUE_AT_PARTY_ROLES_TAB_XPATH = '//*[text()=" Party roles "]/parent::*[@class="expanded"]//td[6]//span[@class="ng-star-inserted"]'
    VENUE_VALUE_AT_PARTY_ROLES_TAB_XPATH = '//*[text()=" Party roles "]/parent::*[@class="expanded"]//td[7]//*[@class="ng-star-inserted"]'
