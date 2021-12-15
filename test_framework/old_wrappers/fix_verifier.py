from th2_grpc_check1.check1_pb2 import PreFilter
from custom import basic_custom_actions as bca
from stubs import Stubs
from th2_grpc_common.common_pb2 import Direction, ValueFilter, MessageFilter, FilterOperation



class FixVerifier:

    def __init__(self, TraderConnectivity, case_id):
        self.verifier = Stubs.verifier
        self.TraderConnectivity = TraderConnectivity
        self.case_id = case_id

    def CheckExecutionReport(self, parameters, response, key_parameters=['ClOrdID', 'OrdStatus'],
                             message_name='Check ExecutionReport', direction='FIRST', case=None):
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
    def CheckExecutionReportFIXStandard(self, parameters, response, key_parameters=['ClOrdID', 'OrdStatus'],
                             message_name='Check ExecutionReport', direction='FIRST', case=None):
        if case == None:
            case = self.case_id

        self.verifier.submitCheckRule(
            bca.create_check_rule(
                message_name,
                bca.filter_to_grpc_fix_standard("ExecutionReport", parameters, key_parameters),
                response.checkpoint_id,
                self.TraderConnectivity,
                case,
                Direction.Value(direction)
            )
        )

    def CheckAllocationInstruction(self, parameters, response, key_parameters=['ClOrdID', 'OrdStatus'],
                                   message_name='Check AllocationInstruction', direction='FIRST', case=None):
        if case == None:
            case = self.case_id

        self.verifier.submitCheckRule(
            bca.create_check_rule(
                message_name,
                bca.filter_to_grpc("AllocationInstruction", parameters, key_parameters),
                response.checkpoint_id,
                self.TraderConnectivity,
                case,
                Direction.Value(direction)
            )
        )

    def CheckAllocationInstructionFIXStandard(self, parameters, response, key_parameters=['ClOrdID', 'OrdStatus'],
                                   message_name='Check AllocationInstruction', direction='FIRST', case=None):
        if case == None:
            case = self.case_id

        self.verifier.submitCheckRule(
            bca.create_check_rule(
                message_name,
                bca.filter_to_grpc_fix_standard("AllocationInstruction", parameters, key_parameters),
                response.checkpoint_id,
                self.TraderConnectivity,
                case,
                Direction.Value(direction)
            )
        )

    def CheckConfirmation(self, parameters, response, key_parameters=['ClOrdID', 'OrdStatus'],
                          message_name='Check Confirmation', direction='FIRST', case=None):
        if case == None:
            case = self.case_id

        self.verifier.submitCheckRule(
            bca.create_check_rule(
                message_name,
                bca.filter_to_grpc("Confirmation", parameters, key_parameters),
                response.checkpoint_id,
                self.TraderConnectivity,
                case,
                Direction.Value(direction)
            )
        )

    def CheckConfirmationFIXStandard(self, parameters, response, key_parameters=['ClOrdID', 'OrdStatus'],
                          message_name='Check Confirmation', direction='FIRST', case=None):
        if case == None:
            case = self.case_id

        self.verifier.submitCheckRule(
            bca.create_check_rule(
                message_name,
                bca.filter_to_grpc_fix_standard("Confirmation", parameters, key_parameters),
                response.checkpoint_id,
                self.TraderConnectivity,
                case,
                Direction.Value(direction)
            )
        )

    def CheckBusinessMessageReject(self, parameters, response, key_parameters=['Text', 'RefMsgType'],
                                   message_name='Check BusinessMessageReject', direction='FIRST', case=None):
        if case == None:
            case = self.case_id

        self.verifier.submitCheckRule(
            bca.create_check_rule(
                message_name,
                bca.filter_to_grpc("BusinessMessageReject", parameters, key_parameters),
                response.checkpoint_id,
                self.TraderConnectivity,
                case,
                Direction.Value(direction)
            )
        )

    def CheckBusinessMessageRejectFIXStandard(self, parameters, response, key_parameters=['Text', 'RefMsgType'],
                                   message_name='Check BusinessMessageReject', direction='FIRST', case=None):
        if case == None:
            case = self.case_id

        self.verifier.submitCheckRule(
            bca.create_check_rule(
                message_name,
                bca.filter_to_grpc_fix_standard("BusinessMessageReject", parameters, key_parameters),
                response.checkpoint_id,
                self.TraderConnectivity,
                case,
                Direction.Value(direction)
            )
        )

    def CheckOrderCancelRequest(self, parameters, response, key_parameters=['ClOrdID', 'OrigClOrdID'],
                                direction='FIRST', message_name='Check OrderCancelRequest', case=None):
        if case == None:
            case = self.case_id

        self.verifier.submitCheckRule(
            bca.create_check_rule(
                message_name,
                bca.filter_to_grpc_fix_standard("OrderCancelRequest", parameters, key_parameters),
                response.checkpoint_id,
                self.TraderConnectivity,
                case,
                Direction.Value(direction)
            )
        )

    def CheckOrderCancelRequestFIXStandard(self, parameters, response, key_parameters=['ClOrdID', 'OrigClOrdID'],
                                direction='FIRST', message_name='Check OrderCancelRequest', case=None):
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

    def CheckListStatusFIXStandard(self, parameters, response, key_parameters=['ListID', 'ListOrderStatus'],
                                   direction='FIRST', message_name='Check ListStatus', case=None):
        if case == None:
            case = self.case_id

        self.verifier.submitCheckRule(
            bca.create_check_rule(
                message_name,
                bca.filter_to_grpc_fix_standard("ListStatus", parameters, key_parameters),
                response.checkpoint_id,
                self.TraderConnectivity,
                case,
                Direction.Value(direction)
            )
        )

    def CheckExecutionReportSequence(self, parameters, response, key_parameters=['ClOrdID', 'OrdStatus'],
                                     message_name='Check ExecutionReport', direction='FIRST', case=None):
        if case == None:
            case = self.case_id

        pre_filter = PreFilter(
            fields={
                'header': ValueFilter(
                    message_filter=MessageFilter(
                        fields={
                            'MsgType': ValueFilter(simple_filter='0', operation=FilterOperation.NOT_EQUAL)
                        }
                    )
                )
            }
        )

        message_sequence = list()
        for param in parameters:
            message_sequence.append(bca.filter_to_grpc("ExecutionReport", param, key_parameters))

        self.verifier.submitCheckSequenceRule(
            bca.create_check_sequence_rule(
                message_name,
                pre_filter,
                message_sequence,
                response.checkpoint_id,
                self.TraderConnectivity,
                case,
                Direction.Value(direction)
            )
        )

    def CheckReject(self, parameters, response, key_parameters=['ClOrdID', 'OrdStatus'], message_name='Check Reject'):
        self.verifier.submitCheckRule(
            bca.create_check_rule(
                message_name,
                bca.filter_to_grpc("Reject", parameters, key_parameters),
                response.checkpoint_id,
                self.TraderConnectivity,
                self.case_id
            )
        )
    def CheckRejectFIXStandard(self, parameters, response, key_parameters=['ClOrdID', 'OrdStatus'], message_name='Check Reject'):
        self.verifier.submitCheckRule(
            bca.create_check_rule(
                message_name,
                bca.filter_to_grpc_fix_standard("Reject", parameters, key_parameters),
                response.checkpoint_id,
                self.TraderConnectivity,
                self.case_id
            )
        )



    def CheckCancelReject(self, parameters, response, key_parameters=['ClOrdID', 'OrdStatus'],
                        message_name='Check Reject'):
            self.verifier.submitCheckRule(
                bca.create_check_rule(
                    message_name,
                    bca.filter_to_grpc("OrderCancelReject", parameters, key_parameters),
                    response.checkpoint_id,
                    self.TraderConnectivity,
                    self.case_id
                )
            )

    def CheckCancelRejectFIXStandard(self, parameters, response, key_parameters=['ClOrdID', 'OrdStatus'],
                          message_name='Check Reject'):
        self.verifier.submitCheckRule(
            bca.create_check_rule(
                message_name,
                bca.filter_to_grpc_fix_standard("OrderCancelReject", parameters, key_parameters),
                response.checkpoint_id,
                self.TraderConnectivity,
                self.case_id
            )
        )
    def CheckNewOrderSingle(self, parameters, response, key_parameters=['ClOrdID'], message_name='Check NewOrderSingle',
                            direction='FIRST', case=None):
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
    def CheckNewOrderSingleFIXStandard(self, parameters, response, key_parameters=['ClOrdID'], message_name='Check NewOrderSingle',
                            direction='FIRST', case=None):
        if case == None:
            case = self.case_id

        self.verifier.submitCheckRule(
            bca.create_check_rule(
                message_name,
                bca.filter_to_grpc_fix_standard("NewOrderSingle", parameters, key_parameters),
                response.checkpoint_id,
                self.TraderConnectivity,
                case,
                Direction.Value(direction)
            )
        )

    def CheckOrderCancelReplaceRequest(self, parameters, response, key_parameters=['OrigClOrdID'], direction='FIRST',
                                       message_name='Check OrderCancelReplaceRequest', case=None):
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
    def CheckOrderCancelReplaceRequestFIXStandard(self, parameters, response, key_parameters=['OrigClOrdID'], direction='FIRST',
                                       message_name='Check OrderCancelReplaceRequest', case=None):
        if case == None:
            case = self.case_id

        self.verifier.submitCheckRule(
            bca.create_check_rule(
                message_name,
                bca.filter_to_grpc_fix_standard("OrderCancelReplaceRequest", parameters, key_parameters),
                response.checkpoint_id,
                self.TraderConnectivity,
                case,
                Direction.Value(direction)
            )
        )
