from custom import basic_custom_actions as bca
from stubs import Stubs
from th2_grpc_common.common_pb2 import Direction

class FixVerifier:

    def __init__(self, TraderConnectivity, case_id):
        self.verifier = Stubs.verifier
        self.TraderConnectivity = TraderConnectivity
        self.case_id = case_id

    def CheckExecutionReport(self, parameters, response, key_parameters = ['ClOrdID', 'OrdStatus'], message_name='Check ExecutionReport', direction='FIRST', case = None):
        if case == None:
            case = self.case_id

        self.verifier.submitCheckRule(
            bca.create_check_rule(
                message_name,
                bca.filter_to_grpc("ExecutionReport", parameters, key_parameters),
                response.checkpoint_id,
                self.TraderConnectivity,
                case,
                Direction.Value(direction)
            )
        )

    def CheckReject(self, parameters, response, key_parameters = ['ClOrdID', 'OrdStatus'], message_name='Check Reject'):
        self.verifier.submitCheckRule(
            bca.create_check_rule(
                message_name,
                bca.filter_to_grpc("Reject", parameters, key_parameters),
                response.checkpoint_id,
                self.TraderConnectivity,
                self.case_id
            )
        )

    def CheckNewOrderSingle(self, parameters, response, key_parameters = ['ClOrdID'], message_name='Check NewOrderSingle', direction='FIRST', case = None):
        if case == None:
            case = self.case_id

        self.verifier.submitCheckRule(
            bca.create_check_rule(
                message_name,
                bca.filter_to_grpc("NewOrderSingle", parameters, key_parameters),
                response.checkpoint_id,
                self.TraderConnectivity,
                case,
                Direction.Value(direction)
            )
        )

    def CheckOrderCancelReplaceRequest(self, parameters, response, key_parameters = ['OrigClOrdID'], direction='FIRST', message_name='Check OrderCancelReplaceRequest', case = None):
        if case == None:
                case = self.case_id

        self.verifier.submitCheckRule(
            bca.create_check_rule(
                message_name,
                bca.filter_to_grpc("OrderCancelReplaceRequest", parameters, key_parameters),
                response.checkpoint_id,
                self.TraderConnectivity,
                case,
                Direction.Value(direction)
            )
        )


    
    def CheckOrderCancelRequest(self, parameters, response, key_parameters = ['ClOrdID', 'OrigClOrdID'], direction='FIRST', message_name='Check OrderCancelRequest', case = None):
        if case == None:
                case = self.case_id

        self.verifier.submitCheckRule(
            bca.create_check_rule(
                message_name,
                bca.filter_to_grpc("OrderCancelRequest", parameters, key_parameters),
                response.checkpoint_id,
                self.TraderConnectivity,
                case,
                Direction.Value(direction)
            )
        )
