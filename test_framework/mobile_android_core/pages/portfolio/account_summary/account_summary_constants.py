class AccountSummaryConstants:
    # region account_summary
    # ACCOUNT_SUMMARY_TITLE = '//android.view.View[@content-desc*="Account Summary"]'
    ACCOUNT_SUMMARY_TITLE = "//android.view.View[contains(@content-desc, 'Account Summary')]"
    CASH_ACCOUNT_START = "//android.view.View[contains(@content-desc, '"
    CASH_ACCOUNT_END ="')]"
    # endregion

    # region cash_withdrawal
    CASH_WITHDRAWAL_BUTTON = '//android.widget.ImageView[@content-desc="Cash Withdrawal"]'
    # endregion

    # region statement
    STATEMENT_BUTTON = '//android.widget.ImageView[@content-desc="Statement"]'
    STATEMENT_GO_BACK = '//android.view.View[1][@clickable="true"]'
    STATEMENT_TITLE = '//android.view.View[@content-desc="Cash Balance Statement"]'
    FROM_DATE = "//*[contains(@text, ', From Date')]"
    TO_DATE = "//*[contains(@text, ', To Date')]"
    PDF_RADIOBUTTON = "//android.view.View/android.widget.RadioButton[1]"
    CSV_RADIOBUTTON = "//android.view.View/android.widget.RadioButton[2]"
    STATEMENT_RETRIEVE = '//android.widget.Button[@content-desc="Retrieve"]'
    # endregion
