class VenueListsConstants:
    class MainPage:
        TITLE_XPATH = '//span[@class="entity-title left"][text()="Venue Lists "]'
        GLOBAL_FILTER = '//nb-card-header//input[@placeholder="Filter"]'
        DOWNLOAD_CSV_BUTTON_XPATH = '//*[@data-name="download"]'
        REFRESH_PAGE_BUTTON_XPATH = '//*[@data-name="refresh"]'
        FULL_SCREEN_BUTTON_XPATH = '//*[@nbtooltip="Full Screen"]'
        NEW_BUTTON_XPATH = '//*[text()="New"]'
        NAME_FILTER_XPATH = '//*[text()="Name"]//following::input[2]'
        DESCRIPTION_FILTER_XPATH = '//*[text()="Description"]//following::input[2]'
        MORE_ACTIONS_BUTTON_XPATH = '//*[@title="More Actions"]'
        EDIT_BUTTON_XPATH = '//*[@nbtooltip="Edit"]'
        DELETE_BUTTON_XPATH = '//*[@nbtooltip="Delete"]'
        OK_BUTTON_XPATH = '//*[text()="Ok"]'
        CANCEL_BUTTON_XPATH = '//*[text()="Cancel"]'
        DOWNLOAD_PDF_BUTTON_XPATH = '//*[@nbtooltip="Download PDF"]'
        PIN_ROW_BUTTON_XPATH = '//*[@nbtooltip ="Click to Pin Row"]'
        USER_ICON_AT_RIGHT_CORNER = '//*[@class="control-item icon-btn context-menu-host"]'
        LOGOUT_BUTTON_XPATH = '//*[text()="Logout"]'
        DISPLAYED_VENUE_LIST_XPATH = "//*[text()='{}']"

    class Wizard:
        DOWNLOAD_PDF_BUTTON_XPATH = '//*[@nbtooltip="Download PDF"]'
        CLOSE_BUTTON_XPATH = '//*[@data-name="close"]'
        NAME_XPATH = '//*[@id="venueListName"]'
        DESCRIPTION_XPATH = '//*[@id="venueListDescription"]'
        VENUE_LIST_XPATH = '//*[@id="venueListVenue"]//button'
        CLEAR_CHANGES_BUTTON_XPATH = '//button[text()="Clear Changes"]'
        SAVE_CHANGES_BUTTON_XPATH = '//button[text()="Save Changes"]'
        FOOTER_ERROR_MESSAGE_XPATH = "//*[@outline='danger']"
        ERROR_MESSAGE_XPATH = '//nb-toast[contains(@class, "danger")]'
