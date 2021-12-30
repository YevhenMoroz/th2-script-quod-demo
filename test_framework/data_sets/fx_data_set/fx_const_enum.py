from enum import Enum


class FxInstruments(Enum):
    instrument_1 = ""
    instrument_2 = ""
    instrument_3 = ""


class FxVenues(Enum):
    venue_1 = "CITI"
    venue_2 = ""
    venue_3 = ""


class FxClients(Enum):
    client_1 = "ASPECT_CITI"
    client_2 = ""
    client_3 = ""


class FxAccounts(Enum):
    account_1 = "Argentina1"
    account_2 = ""
    account_3 = ""


class FxRecipients(Enum):
    recipient_desk_1 = ""
    recipient_desk_2 = ""
    recipient_desk_3 = ""

    recipient_user_1 = ""
    recipient_user_2 = ""
    recipient_user_3 = ""
