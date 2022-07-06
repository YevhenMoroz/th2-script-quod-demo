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

    instrument_4 = dict(
        Symbol='PAR',
        SecurityID='FR0000121121',
        SecurityIDSource='4',
        SecurityExchange='XPAR',
        SecurityType='CS'
    )

    instrument_5 = dict(
        Symbol='FR0000121121_EUR',
        SecurityID='FR0000121121',
        SecurityIDSource='4',
        SecurityExchange='XPAR',
        SecurityType='CS'
    )

    instrument_6 = dict(
        Symbol='FR0000121220', # SWp
        SecurityID='FR0000121220',
        SecurityIDSource='4',
        SecurityExchange='XPAR',
        SecurityType='CS'
    )

    instrument_7 = dict(
        Symbol='FR0000120321', # ORp
        SecurityID='FR0000120321',
        SecurityIDSource='4',
        SecurityExchange='XPAR',
        SecurityType='CS'
    )

    instrument_8 = dict(
        Symbol='QUODTESTQA00',
        SecurityID='TESTQA00',
        SecurityIDSource='8',
        SecurityExchange='QDL1',
        SecurityType='CS'
    )

    instrument_9 = dict(
        Symbol='FR0010411884',
        SecurityID='FR0010411884',
        SecurityIDSource='4',
        SecurityExchange='XPAR',
        SecurityType='CS'
    )

    instrument_10 = dict(
        Symbol='FR0011550177',
        SecurityID='FR0011550177',
        SecurityIDSource='4',
        SecurityExchange='XPAR',
        SecurityType='CS'
    )

    instrument_11 = dict(
        Symbol='FR0000133308',
        SecurityID='FR0000133308',
        SecurityIDSource='4',
        SecurityExchange='XPAR',
        SecurityType='CS'
    )


class AlgoVenues(Enum):
    venue_1 = ""
    venue_2 = ""
    venue_3 = ""


class AlgoClients(Enum):
    client_1 = "CLIENT1"
    client_2 = "CLIENT2"
    client_3 = "CLIENT3"
    client_4 = "KEPLER"


class AlgoAccounts(Enum):
    account_1 = "XPAR_CLIENT1"
    account_2 = "XPAR_CLIENT2"
    account_3 = "XPAR_CLIENT3"
    account_4 = "TRQX_CLIENT1"
    account_5 = "TRQX_CLIENT2"
    account_6 = "TRQX_CLIENT3"
    account_7 = "BATSDARK_KEPLER"
    account_8 = "CHIXDELTA_KEPLER"
    account_9 = "KEPLER"
    account_10 = "TQDARK_KEPLER"


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
    mic_4 = "BATD" # BATS DARKPOOL UK
    mic_5 = "CHID" # CHIX DARKPOOL UK
    mic_6 = "CEUD"  # CBOE DARKPOOL EU
    mic_7 = "XPOS" # ITG
    mic_8 = "TQEM" # TURQUOISE DARKPOOL EU
    mic_9 = "TRQM" # TURQUIOSE DARKPOOL UK
    mic_10 = "QDL1" # QUODLIT1
    mic_11 = "QDL2" # QUODLIT2
    mic_12 = "LISX" # CHIX LIS UK
    mic_13 = "TRQL" # URQUOISE LIS
    mic_14 = "QDD1" # QUODDKP1
    mic_15 = "QDD2" # QUODDKP2



class AlgoListingId(Enum):
    listing_1 = "1015"
    listing_2 = "734"
    listing_3 = "3416"
    listing_4 = "107617192" # QUODLIT1 for QUODTESTQA00
    listing_5 = "107617193" # QUODLIT2 for QUODTESTQA00
    listing_6 = "1805006" # Euronext Paris for FR0010411884
    listing_7 = "1804844 " # Euronext Paris for FR0011550177
    listing_8 = "1803699" # Euronext Paris for FR0000133308

class AlgoCurrency(Enum):
    currency_1 = "EUR"
    currency_2 = "GBP"
    currency_3 = "GBp"
    currency_4 = "USD"
    currency_5 = "UAH"

class AlgoVerifierKeyParameters(Enum):
    verifier_key_parameters_1 = ['ClOrdID', 'OrdStatus', 'ExecType', 'OrderQty', 'Price']
    verifier_key_parameters_2 = ['OrdStatus', 'ExecType', 'OrderQty', 'Price', 'TimeInForce']
    verifier_key_parameters_NOS_child = ['ExDestination', 'OrderQty', 'Price', 'TimeInForce']
    verifier_key_parameters_ER_child = ['ExDestination', 'OrdStatus', 'ExecType', 'OrderQty', 'Price', 'TimeInForce']
    verifier_key_parameters_ER_2_child = ['ExDestination', 'OrdStatus', 'ExecType']
    verifier_key_parameters_ER_Reject_Eliminate_child = ['Account', 'OrdStatus', 'ExecType', 'OrderQty', 'Price', 'TimeInForce']
    verifier_key_parameters_ER_2_Eliminate_child = ['OrdStatus', 'ExecType', 'TimeInForce']
    verifier_key_parameters_ER_cancel_reject_child = ['Account', 'OrdStatus']
    verifier_key_parameters_ER_cancel_reject_parent = ['ClOrdID', 'OrdStatus']
    verifier_key_parameters_NOS_parent = ['ClOrdID']
    verifier_key_parameters_ER_Partially_Fill_Parent = ['ClOrdID', 'OrdStatus', 'ExecType', 'OrderQty', 'Price', 'LeavesQty']

