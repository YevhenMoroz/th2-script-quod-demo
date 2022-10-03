from enum import Enum


class RetTradingApiInstruments(Enum):
    instrument_1 = dict(
        InstrSymbol='T55FD-F[BSE]',
        SecurityID='541794',
        SecurityIDSource='EXC',
        InstrType='Equity',
        SecurityExchange='XBOM'
    )

    instrument_2 = dict(
        InstrSymbol='TCS-IQ[NSE]',
        SecurityID='28612',
        SecurityIDSource='EXC',
        InstrType='Equity',
        SecurityExchange='XNSE'
    )

    instrument_3 = dict(
        InstrSymbol="SBIN-EQ[NSE]",
        SecurityID="3045",
        SecurityIDSource="ExchSymb",
        InstrType="Equity",
        SecurityExchange="XNSE"
    )
    instrument_4 = dict(
        InstrSymbol="VALECHAENG-EQ[NSE]",
        SecurityID="13555",
        SecurityIDSource="ExchSymb",
        InstrType="Equity",
        SecurityExchange="XNSE"
    )


class RetInstruments(Enum):
    instrument_1 = "RELIANCE"
    instrument_2 = "SPICEJET"
    instrument_3 = "TCS"
    instrument_4 = "T55FD"
    instrument_5 = "SBIN"


class RetInstrumentID(Enum):
    # T55FD-F[BSE]
    instrument_id_1 = "mdfW1JW540Y24GIzFiwmeQ"
    # TCS-IQ[NSE]
    instrument_id_2 = "ePKRr68Nr7pDFdVkx6amaQ"
    # SBIN-EQ[NSE]
    instrument_id_3 = "0ihdikxdDxvmz9PFjLsDRw"
    # VALECHAENG-EQ[NSE]
    instrument_id_4 = "gVZuHbpY32wstjJNQ18MvA"


class RetCurrency(Enum):
    currency_1 = "INR"
    currency_2 = "SAR"


class RetSettlCurrency(Enum):
    settl_currency_1 = "INR"
    settl_currency_2 = "SAR"


class RetVenues(Enum):
    venue_1 = "NSE"
    venue_2 = "BSE"


class RetClients(Enum):
    client_1 = "HAKKIM"
    client_2 = "POOJA"
    client_3 = "QAP-4318"
    client_4 = "api_client_rin_desk"
    client_5 = "api_client_test_desk"
    client_6 = "api_client_gross"
    client_7 = "client_test_limit"


class RetAccounts(Enum):
    account_1 = "HAKKIM"
    account_2 = "POOJA"
    account_3 = "FirmTestClient"
    account_4 = "api_account_rin_desk"
    account_5 = "api_account_test_desk"
    account_6 = "api_account_gross"
    account_7 = "account_test_limit"


class RetCashAccounts(Enum):
    cash_account_1 = "api_cash_account_INR"
    cash_account_2 = "api_cash_account_SAR"
    cash_account_3 = "api_cash_account_gross_INR"
    cash_account_4 = "cash_account_test_limit_INR"


class RetCashAccountCounters(Enum):
    # CashAccountID for "api_cash_account_INR"
    cash_account_counter_1 = 1


class RetWashbookAccounts(Enum):
    washbook_account_1 = "CareWB"
    washbook_account_2 = "DMAWashbook"
    washbook_account_3 = "api_washbook_account"


class RetWashBookRules(Enum):
    washbook_rule_1 = "api_washbook_rule"


class RetRecipients(Enum):
    recipient_desk_1 = "RIN-DESK (CL)"
    recipient_desk_2 = "Test_Desk"

    recipient_user_1 = "QA1"
    recipient_user_2 = "QA2"
    recipient_user_3 = "QA3"
    recipient_user_4 = "QA4"
    recipient_user_5 = "QA5"


class RetWebAdminRestApiUsers(Enum):
    # Site Admin
    web_admin_rest_api_user_1 = "adm02"
    # Any hierarchical level
    web_admin_rest_api_user_2 = "adm_rest"


class RetRiskLimitDimensions(Enum):
    risk_limit_dimension_1 = dict(
        clientListID=400008,
        deskID=2,
        venueID="BSE",
        subVenueID=17,
        listingGroupID=1,
        listingID=1209116,
        instrType="EQU",
        standardTradingPhase="OPN",
        routeID=1110,
        executionPolicy="D",
        positionType=["L", "S", "N"],
        posValidity=["TP1", "ITD", "DEL", "TP2", "TP3", "TP4", "TP5", "TP6"],
        settlType=["WK1", "BDA", "DA5", "FUT", "CAS", "IM1", "PHY", "YR1"],
        side="B"
    )


class RetCashTransferTypes(Enum):
    cash_transfer_types_1 = dict(
        cash_loan="CLD",
        cash_loan_withdrawal="CLW",
        collateral_limit="COL",
        deposit="DEP",
        reserved_limit="RES",
        temporary_cash="TCD",
        temporary_cash_withdrawal="TCW",
        withdrawal="WDR"
    )


class RetHierarchicalLevels(Enum):
    hierarchical_level_1 = dict(
        institutionID={'institutionID': 1},
        zoneID={'zoneID': 1},
        locationID={'location': 1},
        deskID={'deskUserRole': [{'deskID': 1}]}
    )
    hierarchical_level_2 = dict(
        institutionID={'institutionID': 3},
        zoneID={'zoneID': 6},
        locationID={'location': 6},
        deskID={'deskUserRole': [{'deskID': 5}]}
    )


class RetFee:
    fees_1 = 5


class RetCommission:
    commission_1 = 3
