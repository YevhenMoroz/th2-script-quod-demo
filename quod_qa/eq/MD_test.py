from custom import basic_custom_actions as bca
from grpc_modules.infra_pb2 import Direction, ConnectionID
from grpc_modules.quod_simulator_pb2 import TemplateQuodSingleExecRule, TemplateNoPartyIDs
from grpc_modules.quod_simulator_pb2 import RequestMDRefID
from stubs import Stubs


timeouts = True


def execute(report_id):
    act = Stubs.fix_act
    verifier = Stubs.verifier
    simulator = Stubs.simulator

    case_name = "QAP-2409"

    symbol = "2320"
    # Create sub-report for case
    case_id = bca.create_event(case_name, report_id)
    MDRefID_1 = simulator.getMDRefIDForConnection(request=RequestMDRefID(
        symbol=symbol,
        connection_id=ConnectionID(session_alias="fix-fh-eq-trqx")
    )).MDRefID


    mdfr_params_1 = {
        'MDReportID': "1",
        'MDReqID': MDRefID_1,
        'Instrument': {
            'Symbol': symbol
        },
        # 'LastUpdateTime': "",
        'NoMDEntries': [
            {
                'MDEntryType': '0',
                'MDEntryPx': '10.7',
                'MDEntrySize': '650'
            },
            {
                'MDEntryType': '1',
                'MDEntryPx': '11',
                'MDEntrySize': '500'
            },
            {
                'MDEntryType': '1',
                'MDEntryPx': '12',
                'MDEntrySize': '600'
            }
        ]
    }

    act.sendMessage(
        request=bca.convert_to_request(
            'Send MarketDataSnapshotFullRefresh',
            "fix-fh-eq-trqx",
            case_id,
            bca.message_to_grpc('MarketDataSnapshotFullRefresh', mdfr_params_1, "fix-fh-eq-trqx")
        )
    )
