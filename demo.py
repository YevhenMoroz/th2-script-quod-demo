from sys import stdout
import logging
from datetime import datetime
from custom import basic_custom_actions as bca
from grpc_modules.event_store_pb2_grpc import EventStoreServiceStub
from grpc_modules.quod_simulator_pb2_grpc import TemplateSimulatorServiceStub
from grpc_modules.simulator_pb2_grpc import ServiceSimulatorStub
from grpc_modules.quod_simulator_pb2 import TemplateQuodDemoRule, TemplateQuodNOSRule, TemplateQuodOCRRule
from grpc_modules.infra_pb2 import ConnectionID
import grpc
from ConfigParser import ParseConfig
from schemas import *


logging.basicConfig(stream=stdout)
logger = logging.getLogger('demo')
logger.setLevel(logging.INFO)
timeouts = False

# TH2 Components addresses retrieval
components = ParseConfig()

logger.debug("Connecting to TH2 components...")
channels = dict()
channels['act'] = grpc.insecure_channel(components['ACT'])
# channels['act_1'] = grpc.insecure_channel(components['ACT_1'])
channels['event-store'] = grpc.insecure_channel(components['EVENTSTORAGE'])
channels['verifier'] = grpc.insecure_channel(components['VERIFIER'])
channels['simulator'] = grpc.insecure_channel(components['SIMULATOR'])

event_store = EventStoreServiceStub(channels['event-store'])


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
            **channels,
            'case_id': bca.create_event_id(),
            'TraderConnectivity': 'gtwquod3',
            'TraderConnectivity2': 'kch-qa-ret-child',
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
            **channels,
            'case_id': bca.create_event_id(),
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
            **channels,
            'case_id': bca.create_event_id(),
            'TraderConnectivity': 'gtwquod3',
            'TraderConnectivity2': 'kch-qa-ret-child',
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
            **channels,
            'case_id': bca.create_event_id(),
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
            **channels,
            'case_id': bca.create_event_id(),
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
            **channels,
            'case_id': bca.create_event_id(),
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
            **channels,
            'case_id': bca.create_event_id(),
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
            **channels,
            'case_id': bca.create_event_id(),
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
            **channels,
            'case_id': bca.create_event_id(),
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
            **channels,
            'case_id': bca.create_event_id(),
            'TraderConnectivity': 'gtwquod5-fx',
            'Account': 'MMCLIENT1',
            'SenderCompID': 'QUODFX_UAT',
            'TargetCompID': 'QUOD5',
        }
    }

    # start rule
    simulator = TemplateSimulatorServiceStub(channels['simulator'])
    DemoRule = simulator.createTemplateQuodDemoRule(
        request=TemplateQuodDemoRule(
            connection_id=ConnectionID(session_alias='kch-qa-ret-child'),
            demo_field1=123,
            demo_field2='KCH_QA_RET_CHILD'
        )
    )
    OCR = simulator.createQuodOCRRule(request=TemplateQuodOCRRule(
        connection_id=ConnectionID(session_alias='kch-qa-ret-child')))
    print(f"Start rules with id's: {DemoRule}, {OCR}")

    # amend_and_trade.execute('QUOD-AMEND-TRADE', report_id, test_cases['QUOD-AMEND-TRADE'])
    # part_trade.execute('QUOD_PART_TRADE', report_id, test_cases['QUOD_PART_TRADE'])
    # QAP_2425_SIM.execute('QAP_2425_SIM', report_id, test_cases['QAP_2425_SIM'])
    # QAP_2462_SIM.execute('QAP_2462_SIM', report_id, test_cases['QAP_2462_SIM'])
    # send_and_amend.execute('QAP-AMEND', report_id, test_cases['QAP-AMEND'])
    # simple_trade2.execute('QUOD-TRADE2', report_id, test_cases['QUOD-TRADE2'])
    simple_trade.execute('QUOD-TRADE', report_id, test_cases['QUOD-TRADE'])
    # QAP_1552_FX.execute('QAP_1552', report_id, test_cases['QAP_1552'])

    # stop rule
    core = ServiceSimulatorStub(channels['simulator'])
    core.removeRule(DemoRule)
    core.removeRule(OCR)

    for channel_name in channels.keys():
        channels[channel_name].close()


if __name__ == '__main__':
    logging.basicConfig()
    test_run()
