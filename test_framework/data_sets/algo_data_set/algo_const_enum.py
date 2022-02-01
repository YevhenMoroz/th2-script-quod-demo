from enum import Enum


class AlgoFixInstruments(Enum):
    instrument_1 = dict(
        Symbol='BUI',
        SecurityID='FR0000062788',
        SecurityIDSource='4',
        SecurityExchange='XPAR',
        SecurityType='CS'
    )

    instrument_2 = dict(
        Symbol='PAR',
        SecurityID='FR0010263202',
        SecurityIDSource='4',
        SecurityExchange='XPAR',
        SecurityType='CS'
    )
    instrument_3 = dict(
        Symbol='FR0010436584',
        SecurityID='FR0010436584',
        SecurityIDSource='4',
        SecurityExchange='XPAR',
        SecurityType='CS',
        SecurityDesc='DREAMNEX'
    )


class AlgoVenues(Enum):
    venue_1 = ""
    venue_2 = ""
    venue_3 = ""


class AlgoClients(Enum):
    client_1 = "CLIENT1"
    client_2 = "CLIENT2"
    client_3 = "CLIENT3"


class AlgoAccounts(Enum):
    account_1 = ""
    account_2 = ""
    account_3 = ""


class AlgoWashbookAccounts(Enum):
    washbook_account_1 = ""
    washbook_account_2 = ""
    washbook_account_3 = ""


class AlgoRecipients(Enum):
    recipient_desk_1 = ""
    recipient_desk_2 = ""
    recipient_desk_3 = ""

    recipient_user_1 = ""
    recipient_user_2 = ""
    recipient_user_3 = ""

class AlgoMic(Enum):
    mic_1 = "XPAR"
    mic_2 = "TRQX"
    mic_3 = "XLON"

class AlgoListingId(Enum):
    listing_1 = "1015"

class AlgoCurrency(Enum):
    currency_1 = "EUR"
    currency_2 = "GBP"
    currency_3 = "GBp"
    currency_4 = "USD"
    currency_5 = "UAH"