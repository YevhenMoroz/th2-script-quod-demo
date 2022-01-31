from enum import Enum

from custom.tenor_settlement_date import spo, wk1, wk2, wk3, today, tom


class FxInstruments(Enum):
    instrument_1 = ""
    instrument_2 = ""
    instrument_3 = ""


class FxVenues(Enum):
    venue_1 = "CITI"
    venue_2 = "HSBC"
    venue_3 = "MS"
    venue_4 = "JPM"
    venue_5 = "DB"
    venue_6 = "BARX"
    venue_7 = "EBS"

    venue_rfq_1 = "CITIR"
    venue_rfq_2 = "HSBCR"
    venue_rfq_3 = "MSR"
    venue_rfq_4 = "JPMR"
    venue_rfq_5 = "DBR"
    venue_rfq_6 = "BARR"
    venue_rfq_7 = "EBS"


class FxClients(Enum):
    """Clients for Taker"""
    client_1 = "ASPECT_CITI"
    client_2 = "ASPECT_DB"
    client_3 = "ASPECT_BREAK"
    client_4 = "AH_TEST_CLIENT"
    client_5 = "TH2_Taker"

    """Dummy client"""
    client_dummy = "DUMMY"

    """Internal clients for AH"""
    client_int_1 = "QUOD"
    client_int_2 = "QUOD2"
    client_int_3 = "QUOD3"
    client_int_4 = "QUOD4"
    client_int_5 = "QUOD5"
    client_int_6 = "DEFAULT1"
    client_int_7 = "QUOD_INT"

    """"Clients for maker"""
    client_mm_1 = "Silver1"  # For ESP_MM testing
    client_mm_2 = "Argentina1"  # For MM_RFQ testing - Explicitly Request Swap Points
    client_mm_3 = "Iridium1"  # For MM_RFQ testing
    client_mm_4 = "Palladium1"  # For ESP_MM testing
    client_mm_5 = "Palladium2"  # For ESP_MM testing
    client_mm_6 = "Osmium1"  # For AutoHedger testing
    client_mm_7 = "Argentum1"  # Can be used for MM_Positions testing
    client_mm_8 = "Aurum1"  # For AutoHedger testing


class FxAccounts(Enum):
    """Account for taker"""
    account_1 = "ASPECT_CITI1"
    account_2 = "ASPECT_DB1"
    account_3 = "ASPECT_BREAK1"
    account_4 = "AH_TEST_CLIENT1"
    account_5 = "TH2_Taker_1"

    """Internal accounts for AH and positions"""
    account_int_1 = "QUOD_1"
    account_int_2 = "QUOD2_1"
    account_int_3 = "QUOD3_1"
    account_int_4 = "QUOD4_1"
    account_int_5 = "QUOD5_1"
    account_int_6 = "DEFAULT1_1"
    account_int_7 = "QUOD_INT_1"

    """Accounts for mm clients"""
    account_mm_1 = "Silver1_1"
    account_mm_2 = "Argentina1_1"
    account_mm_3 = "Iridium1_1"
    account_mm_4 = "Palladium1_1"
    account_mm_5 = "Palladium2_2"
    account_mm_6 = "Osmium1_1"
    account_mm_7 = "Argentum1_1"
    account_mm_8 = "Aurum1_1"


class FxClientTiers(Enum):
    client_tier_1 = "Silver"  # For ESP_MM testing
    client_tier_2 = "Argentina"  # For MM_RFQ testing - Explicitly Request Swap Points
    client_tier_3 = "Iridium1"  # For MM_RFQ testing
    client_tier_4 = "Palladium1"  # For ESP_MM testing
    client_tier_5 = "Palladium2"  # For ESP_MM testing
    client_tier_6 = "Osmium"  # For AutoHedger testing
    client_tier_7 = "Argentum"  # For MM_Positions testing
    client_tier_8 = "Aurum"  # For AutoHedger testing


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


class FxTenors(Enum):
    tenor_spot = "Spot"
    tenor_tod = "Today"
    tenor_tom = "Tom"
    tenor_1w = "1W"
    tenor_2w = "2W"
    tenor_3w = "3W"
    tenor_1m = "1M"
    tenor_2m = "2M"
    tenor_1y = "1Y"
    tenor_2y = "2Y"



class FxSettleDates(Enum):
    today = today()
    tomorrow = tom()
    spot = spo()
    wk1 = wk1()
    wk2 = wk2()
    wk3 = wk3()
    # TODO add more settle dates


class FxSymbols(Enum):
    symbol_1 = "EUR/USD"
    symbol_2 = "GBP/USD"
    symbol_3 = "EUR/GBP"
    symbol_4 = "EUR/JPY"
    symbol_5 = "USD/JPY"
    symbol_6 = "EUR/NOK"
    symbol_7 = "EUR/SEK"
    symbol_8 = "USD/SEK"
    symbol_9 = "GBP/AUD"
    symbol_10 = "GBP/NOK"
    symbol_11 = "GBP/SEK"
    symbol_12 = "USD/CAD"

    symbol_ndf_1 = "USD/PHP"
    symbol_ndf_2 = "EUR/PHP"
    symbol_ndf_3 = "AUD/BRL"
    symbol_ndf_4 = "USD/RUB"
    symbol_ndf_5 = "USD/KRW"

    symbol_synth_1 = "NOK/SEK"  # cross through EURtoUSD
    symbol_synth_2 = "CHF/THB"  # cross through USDtoEUR
    symbol_synth_3 = "EUR/CHF"  # cross thought USD
    symbol_synth_4 = "GBP/NOK"  # cross thought USD
    symbol_synth_5 = "GBP/CAD"  # cross thought USD

    symbol_ndf_synth_1 = "SGD/RUB"  # cross thought USD


class FxCurrencies(Enum):
    currency_eur = "EUR"
    currency_usd = "USD"
    currency_gbp = "GBP"
    currency_php = "PHP"
    currency_cad = "CAD"


class FxRecipients(Enum):
    recipient_desk_1 = ""
    recipient_desk_2 = ""
    recipient_desk_3 = ""

    recipient_user_1 = ""
    recipient_user_2 = ""
    recipient_user_3 = ""


class DaysOfWeek(Enum):
    monday = "MON"
    tuesday = "TUE"
    wednesday = "WED"
    thursday = "THU"
    friday = "FRI"
    sunday = "SUN"
    saturday = "SAT"
