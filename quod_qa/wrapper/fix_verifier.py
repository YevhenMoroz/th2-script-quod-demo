from custom import basic_custom_actions as bca
from stubs import Stubs
from th2_grpc_common.common_pb2 import Direction

class FixVerifier:

    def __init__(self, trader_connectivity, case_id):
        self.verifier = Stubs.verifier
        self.trader_connectivity = trader_connectivity,
        self.case_id = case_id


    def CheckExecutionReport(self, parameters, checkpoint, key_parameters = ['ClOrdID', 'OrdStatus'], message_name='Check ExecutionReport', direction = Direction.Value("FIRST")):
        self.verifier.submitCheckRule(
            bca.create_check_rule(
                message_name,
                bca.filter_to_grpc("ExecutionReport", parameters, key_parameters),
                checkpoint,
                self.trader_connectivity,
                self.case_id,
                direction
            )
        )