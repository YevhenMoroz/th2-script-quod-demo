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
        InstrSymbol="TASI",
        SecurityID="TASI",
        SecurityIDSource="ExchSymb",
        InstrType="Index",
        SecurityExchange="XNSE"
    )
    instrument_4 = dict(
        InstrSymbol="SPICEJET-IQ[NSE]",
        SecurityID="11564",
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
    # TASI
    instrument_id_3 = "_kRAMqAgQauzyJvU7V6R9w"


class RetCurrency(Enum):
    currency_1 = "INR"
    currency_2 = "SAR"


class RetVenues(Enum):
    venue_1 = "NSE"
    venue_2 = "BSE"


class RetClients(Enum):
    client_1 = "HAKKIM"
    client_2 = "POOJA"
    client_3 = "QAP-4318"
    client_4 = "api_client_rin_desk"
    client_5 = "api_client_test_desk"


class RetAccounts(Enum):
    account_1 = "HAKKIM"
    account_2 = "POOJA"
    account_3 = "FirmTestClient"
    account_4 = "api_account_rin_desk"
    account_5 = "api_account_test_desk"


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


class DirectionEnum(Enum):
    FromQuod = "FIRST"
    ToQuod = "SECOND"
