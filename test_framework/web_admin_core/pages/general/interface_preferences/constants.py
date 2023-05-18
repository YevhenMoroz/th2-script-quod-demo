class Constants:
    class MainPage:
        PAGE_TITLE = '//span[@class="entity-title left"][normalize-space()="Interface Preferences"]'
        SEARCHED_ENTITY = '//*[text()="{}"]'

        HELP_ICON = '//nb-card-header//*[@nbtooltip="Help"]/a'
        DOWNLOAD_CSV_BUTTON = '//nb-card-header//*[@data-name="download"]'
        FULL_SCREEN_BUTTON = '//nb-card-header//*[@nbtooltip="Full Screen"]/a'
        REFRESH_BUTTON = '//nb-card-header//*[@data-name="refresh"]'

        INTERFACE_ID_FILTER = '(//thead//input[@placeholder="Filter"])[1]'
        NAME_FILTER = '(//thead//input[@placeholder="Filter"])[2]'

        INTERFACE_ID = '//*[@placeholder="Interface ID *"]'
        NAME = '//*[@placeholder="Name *"]'
        UPDATE_PREFERENCE_LINK = '//p-celleditor//a[normalize-space()="Update"]'
        DEFAULT_CHECKBOX = '//p-celleditor//span[@class="custom-checkbox"]'

        PLUS_BUTTON = '//button[@nbtooltip="Add"]'
        SAVE_CHECKMARK_BUTTON = '//*[@data-name="checkmark"]'
        CANCEL_BUTTON = '//*[@data-name="close"]'
        EDIT_BUTTON = '//*[@data-name="edit"]'
        DELETE_BUTTON = '//*[@data-name="trash-2"]'

        CLEAR_CHANGES_BUTTON = '//button[normalize-space()="Clear Changes"]'
        SAVE_CHANGES_BUTTON = '//button[normalize-space()="Save Changes"]'

