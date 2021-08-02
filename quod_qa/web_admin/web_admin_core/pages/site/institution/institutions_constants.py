class InstitutionsConstants:
    INSTITUTIONS_PAGE_TITLE_XPATH = "//span[@ class ='menu-title ng-tns-c76-89'][text()='site']"

    INSTITUTION_NAME_XPATH = "//*[text()='Institution Name *']/preceding-sibling::input"
    LEI_XPATH = "//*[text()='LEI']/preceding-sibling::input"
    CTM_BIC_XPATH = "//*[text()='CTM BIC']/preceding-sibling::input"
    COUNTERPART_XPATH = "//*[text()='Counterpart']/preceding-sibling::input"
    MANAGE_BUTTON = "//*[text()='Manage']"
    SAVE_CHANGES_BUTTON_XPATH = "//*[text()='Save Changes']"
    REVERT_CHANGES_BUTTON_XPATH = "//*[text()='Revert Changes']"
