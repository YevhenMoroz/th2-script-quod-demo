from enum import Enum

from custom.tenor_settlement_date import spo, wk1, wk2, wk3, today, tom, wk1_ndf, wk2_ndf, spo_ndf, broken_1, broken_2, \
    broken_w1w2, broken_w2w3, spo_ndf, spo_java_api, wk1_java_api, wk2_java_api, today_java_api


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
    venue_8 = "GS"
    venue_9 = "D3"

    venue_rfq_1 = "CITIR"
    venue_rfq_2 = "HSBCR"
    venue_rfq_3 = "MSR"
    venue_rfq_4 = "JPMR"
    venue_rfq_5 = "DBR"
    venue_rfq_6 = "BARR"
    venue_rfq_7 = "EBS"


class FxMarketIDs(Enum):
    market_1 = "CITI-SW"
    market_2 = "HSBC-SW"
    market_3 = "MS-SW"
    market_4 = "JPM-SW"
    market_5 = "DB-SW"
    market_9 = "D3"
    market_10 = "BNP-SW"


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
    client_mm_9 = "SWEDCUST3"
    client_mm_10 = "CLIENT1"  # For Deposit And Loan
    client_mm_11 = "Platinum1"  # For Margin Format testing
    client_mm_12 = "Konstantin1"  # For Java API testing


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


class FxClientTiersID(Enum):
    client_tier_id_1 = "2200009"  # For ESP_MM testing Silver
    client_tier_id_2 = "2600011"  # For MM_RFQ testing - Explicitly Request Swap Points Argentina1
    client_tier_id_3 = "2400009"  # For MM_RFQ testing Iridium1
    client_tier_id_4 = "2000010"  # For ESP_MM testing
    client_tier_id_5 = "2000011"  # For ESP_MM testing
    client_tier_id_6 = "2600010"  # For AutoHedger testing
    client_tier_id_7 = "2600009"  # For MM_Positions testing
    client_tier_id_8 = "2600012"  # For AutoHedger testing
    client_tier_id_11 = "3200016"  # For Margin Format testing
    client_tier_id_12 = "2800013"  # For Margin Format testing


class FxSecurityTypes(Enum):
    fx_spot = "FXSPOT"
    fx_fwd = "FXFWD"
    fx_swap = "FXSWAP"
    fx_ndf = "FXNDF"
    fx_nds = "FXNDS"
    fx_mleg = "MLEG"


class FxInstrTypeWA(Enum):
    fx_spot = "SPO"
    fx_fwd = "FXF"
    fx_swap = "FXS"
    fx_ndf = "NDF"
    fx_nds = "NDS"


class FxInstrTypeJavaAPi(Enum):
    fx_spot = "FXSpot"
    fx_fwd = "FXForward"
    fx_swap = "FXSwap"
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
    broken = "B"
    # TODO add more settle types


class FxSettleTypesJavaAPi(Enum):
    today = "Cash"
    tomorrow = "NextDay"
    spot = "Regular"
    wk1 = "W1"
    wk2 = "W2"
    wk3 = "W3"
    m1 = "M1"
    broken = "BrokenDate"


class FxTenors(Enum):
    tenor_spot = "Spot"
    tenor_tod = "Today"
    tenor_tom = "TOM"
    tenor_1w = "1W"
    tenor_2w = "2W"
    tenor_3w = "3W"
    tenor_1m = "1M"
    tenor_2m = "2M"
    tenor_1y = "1Y"
    tenor_2y = "2Y"
    tenor_sn = "SN"
    tenor_mar_imm = "Mar IMM"


class FxTenorsJavaApi(Enum):
    tenor_spot = "SPO"
    tenor_tod = "CAS"
    tenor_tom = "TOM"
    tenor_1w = "WK1"
    tenor_2w = "WK2"
    tenor_3w = "WK3"
    tenor_1m = "MO1"
    tenor_2m = "MO2"
    tenor_1y = "YR1"
    tenor_2y = "YR2"
    tenor_sn = "SN"
    tenor_mar_imm = "Mar IMM"


class FxSettleDates(Enum):
    today = today()
    today_java_api = today_java_api()
    tomorrow = tom()
    spot = spo()
    spot_java_api = spo_java_api()
    wk1_java_api = wk1_java_api()
    wk1 = wk1()
    wk2 = wk2()
    wk2_java_api = wk2_java_api()
    wk3 = wk3()
    spo_ndf = spo_ndf()
    wk1_ndf = wk1_ndf()
    wk2_ndf = wk2_ndf()
    broken_1 = broken_1()
    broken_2 = broken_2()
    broken_w1w2 = broken_w1w2()
    broken_w2w3 = broken_w2w3()
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
    symbol_13 = "EUR/CAD"
    symbol_14 = "NOK/SEK"
    symbol_15 = "USD/NOK"
    symbol_16 = "AUD/USD"
    symbol_17 = "EUR/AUD"
    symbol_18 = "AUD/GBP"
    symbol_19 = "ZAR/MXN"
    symbol_20 = "USD/ZAR"
    symbol_21 = "EUR/MXN"
    symbol_22 = "THB/TWD"
    symbol_23 = "USD/THB"
    symbol_24 = "USD/TWD"

    symbol_ndf_1 = "USD/PHP"
    symbol_ndf_2 = "EUR/PHP"
    symbol_ndf_3 = "AUD/BRL"
    symbol_ndf_4 = "USD/RUB"
    symbol_ndf_5 = "USD/KRW"
    symbol_ndf_6 = "EUR/RUB"

    symbol_synth_1 = "NOK/SEK"  # cross through EURtoUSD
    symbol_synth_2 = "CHF/THB"  # cross through USDtoEUR
    symbol_synth_3 = "EUR/CHF"  # cross thought USD
    symbol_synth_4 = "GBP/NOK"  # cross thought USD
    symbol_synth_5 = "GBP/CAD"  # cross thought USD
    symbol_synth_6 = "USD/CHF"  # mystery symbol

    symbol_ndf_synth_1 = "SGD/RUB"  # cross thought USD


class FxCurrencies(Enum):
    currency_eur = "EUR"
    currency_usd = "USD"
    currency_gbp = "GBP"
    currency_php = "PHP"
    currency_cad = "CAD"
    currency_aud = "AUD"
    currency_sek = "SEK"
    currency_jpy = "JPY"
    currency_nok = "NOK"


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


class FXAutoHedgers(Enum):
    auto_hedger_1 = "OsmiumAH"
    auto_hedger_2 = "AURUM_AH"
    auto_hedger_3 = "DEFAULT"
    auto_hedger_4 = "Internal"
    auto_hedger_5 = "AUTOHEDGER1"
    auto_hedger_6 = "AUTOHEDGER0"
    auto_hedger_7 = "AUTOHEDGER_Int"
    auto_hedger_8 = "OsmiumAH2"


class FXAutoHedgersID(Enum):
    auto_hedger_id_1 = "1400008"
    auto_hedger_id_2 = "1400010"
    auto_hedger_id_3 = "1600010"
    auto_hedger_id_4 = "1400009"
    auto_hedger_id_5 = "1400006"
    auto_hedger_id_6 = "1"
    auto_hedger_id_7 = "1400005"
    auto_hedger_id_8 = "1600011"


class FXAlgoPolicies(Enum):
    algo_policy_1 = "Hedging_Test"
    algo_policy_2 = "test"
    algo_policy_3 = "test_fake"


class FXAlgoPoliciesID(Enum):
    algo_policy_id_1 = "400019"
    algo_policy_id_2 = "200011"
    algo_policy_id_3 = "400024"


class FXListings(Enum):
    eur_usd_spo = "506403761"
    eur_usd_wk1 = "506403765"
    eur_usd_wk2 = "506403766"
    eur_usd_wk3 = "506403767"
    eur_usd_bda = "506403787"
    gbp_usd_spo = "506404433"
    gbp_usd_wk1 = "506404437"
    gbp_usd_wk2 = "506404438"
    #TODO add more listings
