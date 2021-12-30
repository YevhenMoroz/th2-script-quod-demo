from enum import Enum

from custom.tenor_settlement_date import spo, wk1, wk2, wk3, today, tom


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
    client_2 = "Argentina1"
    client_3 = ""


class FxSecurityTypes(Enum):
    fx_spot = "FXSPOT"
    fx_fwd = "FXFWD"
    fx_swap = "FXSWAP"
    fx_ndf = "FXNDF"
    fx_nds = "FXNDS"


class FxSettleTypes(Enum):
    today = "1"
    tomorrow = "2"
    spot = "0"
    wk1 = "W1"
    wk2 = "W2"
    wk3 = "W3"
    m1 = "M1"
    # TODO add more settle types


class FxSettleDates(Enum):
    today = today()
    tomorrow = tom()
    spot = spo()
    wk1 = wk1()
    wk2 = wk2()
    wk3 = wk3()
    # TODO add more settle dates


class FxSymbols(Enum):
    eur_usd = "EUR/USD"
    gbp_usd = "GBP/USD"
    eur_gbp = "EUR/GBP"
    eur_jpy = "EUR/JPY"
    usd_jpy = "USD/JPY"
    eur_nok = "EUR/NOK"
    eur_sek = "EUR/SEK"
    usd_sek = "USD/SEK"
    nok_sek = "NOK/SEK"
    usd_cad = "USD/CAD"
    usd_php = "USD/PHP"
    eur_php = "EUR/PHP"


class FxAccounts(Enum):
    account_1 = ""
    account_2 = ""
    account_3 = ""


class FxRecipients(Enum):
    recipient_desk_1 = ""
    recipient_desk_2 = ""
    recipient_desk_3 = ""

    recipient_user_1 = ""
    recipient_user_2 = ""
    recipient_user_3 = ""
