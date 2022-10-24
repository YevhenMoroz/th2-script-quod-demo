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

    instrument_12 = dict(
        Symbol='QUODTESTQA01',
        SecurityID='TESTQA01',
        SecurityIDSource='8',
        SecurityExchange='QDL4',
        SecurityType='CS'
    )

    instrument_13 = dict(
        Symbol='QUODTESTQA02',
        SecurityID='TESTQA02',
        SecurityIDSource='8',
        SecurityExchange='QDL6',
        SecurityType='CS'
    )

    instrument_14 = dict(
        Symbol='FR0000031577',
        SecurityID='FR0000031577',
        SecurityIDSource='4',
        SecurityExchange='XPAR',
        SecurityType='CS'
    )

    instrument_15 = dict(
        Symbol='QUODTESTQA03',
        SecurityID='TESTQA03',
        SecurityIDSource='8',
        SecurityExchange='QDL8',
        SecurityType='CS'
    )

    instrument_16 = dict(
        Symbol='QUODTESTQA04',
        SecurityID='TESTQA04',
        SecurityIDSource='8',
        SecurityExchange='QDL8',
        SecurityType='CS'
    )

    instrument_17 = dict(
        Symbol='QUODTESTQA05',
        SecurityID='TESTQA05',
        SecurityIDSource='8',
        SecurityExchange='QDL11',
        SecurityType='CS'
    )

    instrument_18 = dict(
        Symbol='FR0000121329',
        SecurityID='FR0000121329',
        SecurityIDSource='4',
        SecurityExchange='XPAR',
        SecurityType='CS'
    )

    instrument_19 = dict(
        Symbol='IE00B5BMR087',
        SecurityID='IE00B5BMR087',
        SecurityIDSource='4',
        SecurityExchange='XAMS',
        SecurityType='CS'
    )

    instrument_20 = dict(
        Symbol='SE0006288015',
        SecurityID='SE0006288015',
        SecurityIDSource='4',
        SecurityExchange='XSTO',
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
    client_5 = "BATSDARK_KEPLER"
    client_6 = "CHIXDELTA_KEPLER"


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
    account_11 = "TRQX_KEPLER"
    account_12 = "BATS_KEPLER"
    account_13 = "CHIX_KEPLER"
    account_14 = "XAMS_KEPLER"


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
    mic_13 = "TRQL" # TURQUOISE LIS
    mic_14 = "QDD1" # QUODDKP1
    mic_15 = "QDD2" # QUODDKP2
    mic_16 = "QDL4"  # QUODLIT4
    mic_17 = "QDL5"  # QUODLIT5
    mic_18 = "QDL6"  # QUODLIT6
    mic_19 = "QDL7"  # QUODLIT7
    mic_20 = "TQLIS"  # TQLIS
    mic_21 = "CHIXLIS"  # CHIXLIS
    mic_22 = "JSSI"  # JANESTREET
    mic_23 = "CCEU"  # CITADEL
    mic_24 = "QDL8"  # QUODLIT8
    mic_25 = "QDL9"  # QUODLIT9
    mic_26 = "QDL10"  # QUODLIT10
    mic_27 = "BATE"  # BATS UK
    mic_28 = "QDL11"  # QUODLIT11
    mic_29 = "QDL12"  # QUODLIT12
    mic_30 = "CHIX"   # CHIX
    mic_31 = "XAMS"   # Euronext Amsterdam


class AlgoListingId(Enum):
    listing_1 = "1015"
    listing_2 = "734"
    listing_3 = "3416"
    listing_4 = "107617192" # QUODLIT1 for QUODTESTQA00
    listing_5 = "107617193" # QUODLIT2 for QUODTESTQA00
    listing_6 = "1805006" # Euronext Paris for FR0010411884
    listing_7 = "1804844" # Euronext Paris for FR0011550177
    listing_8 = "1803699" # Euronext Paris for FR0000133308
    listing_9 = "525020503" # QUODLIT4 for QUODTESTQA01
    listing_10 = "525020504" # QUODLIT5 for QUODTESTQA01
    listing_11 = "625020503" # QUODLIT6 for QUODTESTQA02
    listing_12 = "625020504" # QUODLIT7 for QUODTESTQA02
    listing_13 = "125917202" # JANESTREET for FR0000031577
    listing_14 = "181116477" # CITADEL for FR0000031577
    listing_15 = "897588209" # TRQX for FR0010411884
    listing_16 = "116017192"  # QUODLIT3 for QUODTESTQA00
    listing_17 = "825020507"  # QUODLIT8 for QUODTESTQA03
    listing_18 = "825020508"  # QUODLIT9 for QUODTESTQA03
    listing_19 = "825020509"  # QUODLIT10 for QUODTESTQA03
    listing_20 = "925020507"  # QUODLIT8 for QUODTESTQA04
    listing_21 = "925020508"  # QUODLIT9 for QUODTESTQA04
    listing_22 = "925020509"  # QUODLIT10 for QUODTESTQA04
    listing_23 = "897587663"  # TRQX for FR0000133308
    listing_24 = "1803699"    # Euronext Paris for FR0000133308
    listing_25 = "1872430"    # BATS UK for FR0000133308
    listing_26 = "768319009"    # CHIX UK for FR0000133308
    listing_27 = "1225020507"    # QUODLIT11 for QUODTESTQA05
    listing_28 = "1225020508"    # QUODLIT12 for QUODTESTQA05
    listing_29 = "1803729"       # Euronext Paris for FR0000121329
    listing_30 = "1325020507"    # Euronext Amsterdam for IE00B5BMR087
    listing_31 = "1863318"       # CHIX for IE00B5BMR087
    listing_32 = "1874187"       # BATS for FR0010411884
    listing_33 = "1863556"       # CHIX for FR0010411884
    listing_34 = "125911519"       # JANESTREET for FR0010411884
    listing_35 = "1803739"       # Euronext Paris for FR0000121220
    listing_36 = "555"       # Euronext Paris for BUI / FR0000062788


class AlgoCurrency(Enum):
    currency_1 = "EUR"
    currency_2 = "GBP"
    currency_3 = "GBp"
    currency_4 = "USD"
    currency_5 = "UAH"
    currency_6 = "SEK"


class AlgoVerifierKeyParameters(Enum):
    verifier_key_parameters_1 = ['ClOrdID', 'OrdStatus', 'ExecType', 'OrderQty', 'Price']
    verifier_key_parameters_2 = ['OrdStatus', 'ExecType', 'OrderQty', 'Price', 'TimeInForce']
    verifier_key_parameters_3 = ['OrdStatus', 'ExecType', 'OrderQty']
    verifier_key_parameters_4 = ['OrdStatus', 'ExecType', 'OrderQty', 'OrdType']
    verifier_key_parameters_5 = ['ExDestination', 'OrdStatus', 'ExecType', 'OrderQty', 'Price', 'TimeInForce', 'OrdType', 'Account']
    verifier_key_parameters_NOS_child = ['ExDestination', 'OrderQty', 'Price', 'TimeInForce']
    verifier_key_parameters_NOS_child_with_minqty = ['ExDestination', 'OrderQty', 'Price', 'TimeInForce', 'MinQty']
    verifier_key_parameters_NOS_child_with_stoppx = ['ExDestination', 'OrderQty', 'Price', 'TimeInForce', 'StopPx']
    verifier_key_parameters_ER_child = ['ExDestination', 'OrdStatus', 'ExecType', 'OrderQty', 'Price', 'TimeInForce', "OrdType"]
    verifier_key_parameters_ER_2_child = ['ExDestination', 'OrdStatus', 'ExecType']
    verifier_key_parameters_ER_Reject_Eliminate_child = ['Account', 'OrdStatus', 'ExecType', 'OrderQty', 'Price', 'TimeInForce']
    verifier_key_parameters_ER_2_Eliminate_child = ['OrdStatus', 'ExecType', 'TimeInForce']
    verifier_key_parameters_ER_cancel_reject_child = ['Account', 'OrdStatus']
    verifier_key_parameters_ER_cancel_reject_parent = ['ClOrdID', 'OrdStatus']
    verifier_key_parameters_NOS_parent = ['ClOrdID']
    verifier_key_parameters_ER_Partially_Fill_Parent = ['ClOrdID', 'OrdStatus', 'ExecType', 'OrderQty', 'Price', 'LeavesQty']
    verifier_key_parameters_ER_RFQ = ['OrdStatus', 'ExecType', 'AlgoCst01', "OrdType", "ExDestination"]
    verifier_key_parameters_NOS_RFQ = ['ExDestination', 'OrderQty', 'Price', 'TimeInForce', 'OrdType', 'AlgoCst01']
    verifier_key_parameters_RFQ_canceled = ['ExDestination', 'OrderQty', 'Price', 'TimeInForce', 'OrdType', 'DeliverToCompID']
    verifier_key_parameters_with_text = ['ExDestination', 'OrdStatus', 'ExecType', 'Text']
    verifier_key_parameters_er_fill = ['OrdStatus', 'ExecType']
    verifier_key_parameters_er_replace_display_qty_parent = ['ClOrdID', 'OrdStatus', 'ExecType', 'OrderQty', 'Price', 'DisplayQty']
    key_params_read_log_check_updating_status = ['OldStatus', 'NewStatus']
    key_params_read_log_check_cancel_child = ['OrderId', 'QtyCancelingChilds']
    key_params_read_log_check_primary_listing = ['OrderId', 'PrimaryListingID']
    key_params_read_log_check_party_info = ['PartyID', 'OrdrMisc6', 'ClOrdID']
    key_params_read_log_check_tags_5052_and_207_mapping = ['SecurityExchange', 'ClOrdID', 'ExternalStrategyName']
    key_params_read_log_check_that_venue_was_suspended = ['OrderID', 'VenueName']
    key_params_log_319_check_that_lis_phase_is_skipping = ['OrderID', 'Text']
    key_params_log_319_check_the_currency_rate = ['Currency', 'Rate']
    key_params_log_319_check_the_lis_amount = ['Amount1', 'Amount2', 'Venue']
    key_params_log_319_check_party_info_more_than_one_group = ['GroupNumber']
    key_params_log_319_check_that_is_no_suitablle_liquidity = ['ClOrdrId']


class AlgoPreFilter(Enum):
    pre_filer_equal_F = {
                'header': {
                    'MsgType': ('F', "EQUAL")
                }}
    pre_filer_equal_D = {
        'header': {
            'MsgType': ('D', "EQUAL")
        }}

    pre_filer_equal_G = {
        'header': {
            'MsgType': ('G', "EQUAL")
        }}

    pre_filer_equal_ER_canceled = {
                'header': {
                    'MsgType': ('8', "EQUAL")
                },
                'ExecType': ('4', "EQUAL")
                }
    pre_filer_equal_order_cancel_reject = {
                'header': {
                    'MsgType': ('9', "EQUAL")
                }
                }

    pre_filer_equal_ER_fill = {
        'header': {
            'MsgType': ('8', "EQUAL")
        },
        'ExecType': ('F', "EQUAL")
    }

    pre_filter_primary_listing_id = {
        'PrimaryListingID': ('*', "EQUAL")
    }

    pre_filter_primary_status_of_transaction = {
        'NewStatus': ('*', "EQUAL")
    }

    pre_filter_suitable_liquidity = {
        'ClOrdrId': ('*', "EQUAL"),
        'Text': ('*', "EQUAL")
    }

    pre_filer_equal_ER_pending_new = {
        'header': {
            'MsgType': ('8', 'EQUAL')
        },
        'ExecType': ('A', 'EQUAL'),
        'OrdStatus': ('A', 'EQUAL')
    }

    pre_filer_equal_ER_new = {
        'header': {
            'MsgType': ('8', 'EQUAL')
        },
        'ExecType': ('0', 'EQUAL'),
        'OrdStatus': ('0', 'EQUAL')
    }

    pre_filer_equal_ER_eliminate = {
        'header': {
            'MsgType': ('8', 'EQUAL')
        },
        'ExecType': ('4', 'EQUAL'),
        'OrdStatus': ('4', 'EQUAL')
    }