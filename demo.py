from __future__ import print_function
import sys
import logging
import time
from datetime import datetime
from custom import basic_custom_actions as bca
from grpc_modules import act_fix_pb2_grpc, event_store_pb2_grpc, verifier_pb2_grpc
import grpc
from ConfigParser import ParseConfig
from schemas import simple_trade2, QAP_2462_SIM, amend_and_trade, part_trade, send_and_amend, QAP_2425_SIM, simple_trade, QAP_1552_FX


logging.basicConfig(stream=sys.stdout)
logger = logging.getLogger('demo')
logger.setLevel(logging.INFO)
timeouts = False

# TH2 Components addresses retrieval
components = ParseConfig()

logger.debug("Connecting to TH2 components...")
act = act_fix_pb2_grpc.ActStub(grpc.insecure_channel(components['ACT_1']))
event_store = event_store_pb2_grpc.EventStoreServiceStub(grpc.insecure_channel(components['EVENTSTORAGE']))
verifier = verifier_pb2_grpc.VerifierStub(grpc.insecure_channel(components['VERIFIER']))


def test_run():
    # Generation id and time for test run
    report_id = bca.create_event_id()
    bca.create_event(
        event_store,
        '__quod_demo_1 ' + datetime.now().strftime('%Y%m%d-%H:%M:%S'),
        report_id
    )
    logger.info("Root event was created (report id = {})".format(report_id))
    # Reference data for test cases

    instrument = {
        'Symbol': 'FR0010263202_EUR',
        'SecurityID': 'FR0010263202',
        'SecurityIDSource': '4',
        'SecurityExchange': 'XPAR'

    }

    instrument_2 = {
        'Symbol': 'SE0000818569_SEK',
        'SecurityID': 'SE0000818569',
        'SecurityIDSource': '4',
        'SecurityExchange': 'XSTO'
    }
    instrument_3 = {
        'Symbol': 'FR0010263202_EUR',
        'SecurityID': 'FR0010263202',
        'SecurityIDSource': '4',
        'SecurityExchange': 'XPAR'
    }
    # Specific data for test case test
    test_cases = {
        'QAP_2425_SIM': {
            'case_id': bca.create_event_id(),
            'act_box': act,
            'event_store_box': event_store,
            'verifier_box': verifier,
            'TraderConnectivity': 'gtwquod3',
            'TraderConnectivity2': 'kch-qa-ret-child',
            'TraderConnectivity3': 'kch-qa-ret-child_out',
            'SenderCompID': 'QUODFX_UAT',
            'TargetCompID': 'QUOD3',
            'SenderCompID2': 'KCH_QA_RET_CHILD',
            'TargetCompID2': 'QUOD_QA_RET_CHILD',
            'Account': 'KEPLER',
            'HandlInst': '2',
            'Side': '2',
            'OrderQty': '600',
            'OrdType': '2',
            'Price': '20',
            'TimeInForce': '0',
            'ExDestination': 'XPAR',
            'DeliverToCompID': 'PARIS',
            'Instrument': instrument_3
        },
        'QAP-2425': {
            'case_id': bca.create_event_id(),
            'act_box': act,
            'event_store_box': event_store,
            'verifier_box': verifier,
            'TraderConnectivity': 'gtwquod3',
            'Account': 'KEPLER',
            'HandlInst': '2',
            'Side': '1',
            'SenderCompID': 'QUODFX_UAT',
            'TargetCompID': 'QUOD3',
            'OrderQty': '500',
            'OrdType': '2',
            'Price': '20',
            'TimeInForce': '0',
            'Instrument': instrument_3
        },
        'QAP_2462_SIM': {
            'case_id': bca.create_event_id(),
            'act_box': act,
            'event_store_box': event_store,
            'verifier_box': verifier,
            'TraderConnectivity': 'gtwquod3',
            'TraderConnectivity2': 'kch-qa-ret-child',
            'TraderConnectivity3': 'kch-qa-ret-child_out',
            'SenderCompID': 'QUODFX_UAT',
            'TargetCompID': 'QUOD3',
            'SenderCompID2': 'KCH_QA_RET_CHILD',
            'TargetCompID2': 'QUOD_QA_RET_CHILD',
            'Account': 'KEPLER',
            'HandlInst': '2',
            'Side': '2',
            'OrderQty': '500',
            'OrdType': '2',
            'Price': '20',
            'TimeInForce': '0',
            'ExDestination': 'XPAR',
            'DeliverToCompID': 'PARIS',
            'Instrument': instrument_3
        },
        'QAP-2422': {
            'case_id': bca.create_event_id(),
            'act_box': act,
            'event_store_box': event_store,
            'verifier_box': verifier,
            'TraderConnectivity': 'gtwquod3',
            'SenderCompID': 'QUODFX_UAT',
            'TargetCompID': 'QUOD3',
            'Account': 'KEPLER',
            'HandlInst': '2',
            'Side': '1',
            'OrderQty': '400',
            'OrdType': '2',
            'Price': '20',
            'TimeInForce': '0',
            'Instrument': instrument_2
        },
        'QAP-AMEND': {
            'case_id': bca.create_event_id(),
            'act_box': act,
            'event_store_box': event_store,
            'verifier_box': verifier,
            'TraderConnectivity': 'gtwquod3',
            'SenderCompID': 'QUODFX_UAT',
            'TargetCompID': 'QUOD3',
            'Account': 'KEPLER',
            'HandlInst': '2',
            'Side': '1',
            'OrderQty': '400',
            'newOrderQty': '500',
            'OrdType': '2',
            'Price': '20',
            'newPrice': '19',
            'TimeInForce': '0',
            'Instrument': instrument_3
        },
        'QUOD-TRADE': {
            'case_id': bca.create_event_id(),
            'act_box': act,
            'event_store_box': event_store,
            'verifier_box': verifier,
            'TraderConnectivity': 'gtwquod3',
            'SenderCompID': 'QUODFX_UAT',
            'Account': 'KEPLER',
            'HandlInst': '2',
            'OrderQty': '500',
            'OrdType': '2',
            'Price': '20',
            'TimeInForce': '0',
            'TargetCompID': 'QUOD3',
            'Instrument': instrument_2
        },
        'QUOD-TRADE2': {
            'case_id': bca.create_event_id(),
            'act_box': act,
            'event_store_box': event_store,
            'verifier_box': verifier,
            'TraderConnectivity': 'gtwquod3',
            'SenderCompID': 'QUODFX_UAT',
            'Account': 'KEPLER',
            'HandlInst': '1',
            'OrderQty_ord1': '200',
            'OrderQty_ord2': '100',
            'OrdType': '2',
            'Price': '20',
            'TimeInForce': '0',
            'TargetCompID': 'QUOD3',
            'Instrument': instrument_2
        },
        'QUOD-AMEND-TRADE': {
            'case_id': bca.create_event_id(),
            'act_box': act,
            'event_store_box': event_store,
            'verifier_box': verifier,
            'TraderConnectivity': 'gtwquod3',
            'SenderCompID': 'QUODFX_UAT',
            'Account': 'KEPLER',
            'HandlInst': '2',
            'OrderQty': '500',
            'OrdType': '2',
            'Price1': '20',
            'Price2': '23',
            'TimeInForce': '0',
            'TargetCompID': 'QUOD3',
            'Instrument': instrument_2
        },
        'QUOD_PART_TRADE': {
            'case_id': bca.create_event_id(),
            'act_box': act,
            'event_store_box': event_store,
            'verifier_box': verifier,
            'TraderConnectivity': 'gtwquod3',
            'SenderCompID': 'QUODFX_UAT',
            'Account': 'KEPLER',
            'HandlInst': '2',
            'OrderQty1': '500',
            'OrderQty2': '800',
            'OrdType': '2',
            'Price': '20',
            'TimeInForce': '0',
            'TargetCompID': 'QUOD3',
            'Instrument': instrument_2
         },

        'QAP_1552': {
            'case_id': bca.create_event_id(),
            'act_box': act,
            'event_store_box': event_store,
            'verifier_box': verifier,
            'TraderConnectivity': 'gtwquod5-fx',
            'Account': 'MMCLIENT1',
            'SenderCompID': 'QUODFX_UAT',
            'TargetCompID': 'QUOD5',

        }
    }
    # amend_and_trade.execute('QUOD-AMEND-TRADE', report_id, test_cases['QUOD-AMEND-TRADE'])
    # part_trade.execute('QUOD_PART_TRADE', report_id, test_cases['QUOD_PART_TRADE'])
    # QAP_2425_SIM.execute('QAP_2425_SIM', report_id, test_cases['QAP_2425_SIM'])
    # QAP_2462_SIM.execute('QAP_2462_SIM', report_id, test_cases['QAP_2462_SIM'])
    # send_and_amend.execute('QAP-AMEND', report_id, test_cases['QAP-AMEND'])
    # simple_trade2.execute('QUOD-TRADE2', report_id, test_cases['QUOD-TRADE2'])
    # simple_trade.execute('QUOD-TRADE', report_id, test_cases['QUOD-TRADE'])
    QAP_1552_FX.execute('QAP_1552', report_id, test_cases['QAP_1552'])

    grpc.insecure_channel(components['ACT_1']).close()
    grpc.insecure_channel(components['EVENTSTORAGE']).close()
    grpc.insecure_channel(components['VERIFIER']).close()

if __name__ == '__main__':
    logging.basicConfig()
    test_run()
