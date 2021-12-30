from enum import Enum


class RetInstruments(Enum):
    instrument_1 = "RELIANCE"
    instrument_2 = "SPICEJET"
    instrument_3 = "TCS"
    instrument_4 = "T55FD"
    instrument_5 = "SBIN"


class RetVenues(Enum):
    venue_1 = "NSE"
    venue_2 = "BSE"


class RetClients(Enum):
    client_1 = "HAKKIM"
    client_2 = "POOJA"
    client_3 = "QAP-4318"
    client_4 = "test_client"


class RetAccounts(Enum):
    account_1 = "HAKKIM"
    account_2 = "POOJA"
    account_3 = "test_account"


class RetWashbookAccounts(Enum):
    washbook_account_1 = "CareWB"
    washbook_account_2 = "DMAWashbook"


class RetRecipients(Enum):
    recipient_desk_1 = "RIN-DESK (CL)"
    recipient_desk_2 = "Test_Desk"

    recipient_user_1 = "QA1"
    recipient_user_2 = "QA2"
    recipient_user_3 = "QA3"
    recipient_user_4 = "QA4"
    recipient_user_5 = "QA5"
