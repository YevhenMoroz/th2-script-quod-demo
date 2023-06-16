class Constants:
    class MainPage:
        PAGE_TITLE = "//span[@class='entity-title left'][normalize-space()='User Sessions']"
        USER_NAME_FILTER = '//div[@style="width: 200px; left: 0px;"]//input[@ref="eFloatingFilterText"]'
        ACTIVE_BUTTON = '//div[@class="action-cell"]//*[@nbtooltip="Active"]'
        OK_BUTTON = '//button[normalize-space()="Ok"]'
        CANCEL_BUTTON = '//button[normalize-space()="Cancel"]'
