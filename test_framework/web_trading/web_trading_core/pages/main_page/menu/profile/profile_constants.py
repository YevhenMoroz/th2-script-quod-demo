class ProfileConstants:
    # region Profile
    CANCEL_BUTTON_XPATH = '//*[@class="button-style-cancel"]'
    SAVE_BUTTON_XPATH = '//*[@class="button-style"]'
    CLOSE_BUTTON_XPATH = '//*[@class="icon-close"]'
    # endregion

    # region - Personal Details
    PERSONAL_DETAILS_BUTTON_XPATH = '//*[@class="nav"]/span[1]'
    PREFERENCE_BUTTON_XPATH = '//*[@class="nav"]/span[2]'
    SECURITY_BUTTON_XPATH = '//*[text()="Security"]'
    TERMS_AND_CONDITION_BUTTON_XPATH = '//*[@class="nav"]/span[4]'
    FIRST_NAME_FIELD_XPATH = '//*[@name="firstName"]'
    LAST_NAME_FIELD_XPATH = '//*[@name="lastName"]'
    MOBILE_NO_FIELD_XPATH = '//*[@name="mobile"]'
    EMAIL_FIELD_XPATH = '//*[@name="email"]'
    COUNTRY_FIELD_XPATH = '//*[@name="country"]'
    ADDRESS_FIELD_XPATH = '//*[@name="address"]'
    DATA_OF_BIRTH_FIELD_XPATH = '//*[@name="dob"]'
    # endregion

    # region - Preference
    ORDER_NOTIFICATIONS_SHOW_RADIO_BUTTON_XPATH = '//*[@id="igx-radio-66"]'
    ORDER_NOTIFICATIONS_HIDE_RADIO_BUTTON_XPATH = '//*[@id="igx-radio-67"]'
    EXECUTION_NOTIFICATIONS_SHOW_RADIO_BATTON_XPATH = '//*[@id="igx-radio-68"]'
    EXECUTION_NOTIFICATIONS_HIDE_RADIO_BATTON_XPATH = '//*[@id="igx-radio-69"]'
    OTHER_NOTIFICATIONS_SHOW_RADIO_BUTTON_XPATH = '//*[@id="igx-radio-70"]'
    OTHER_NOTIFICATIONS_HIDE_RADIO_BUTTON_XPATH = '//*[@id="igx-radio-71"]'
    DEFAULT_CLIENT_SELECT_MENU_XPATH = '//*[@id="default-client"]'
    LIST_OF_DEFAULT_CLIENTS_XPATH = '//*[@id="default-client-list"]//span[text()="{}"]'
    # endregion

    # region - Security
    OLD_PASSWORD_FIELD_XPATH = '//*[@name="oldPassword" and @type="password"]'
    NEW_PASSWORD_FIELD_XPATH = '//*[@name="newPassword" and @type="password"]'
    CONFIRM_PASSWORD_FIELD_XPATH = '//*[@name="confirmPassword" and @type="password"]'
    # endregion

    # region - Terms and Condition
    TAC_CLOSE_BUTTON_XPATH = '//*[@class="icon-close"]'
    # endregion
