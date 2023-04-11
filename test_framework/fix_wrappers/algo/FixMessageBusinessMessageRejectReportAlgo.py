from test_framework.fix_wrappers.FixMessageBusinessMessageRejectReport import FixMessageBusinessMessageRejectReport


class FixMessageBusinessMessageRejectReportAlgo(FixMessageBusinessMessageRejectReport):

    def __init__(self, parameters: dict = None):
        super().__init__()
        super().change_parameters(parameters)

    def set_params_for_business_message_reject(self):
        temp = dict()
        temp.update(
            RefSeqNum='*',
            Text='*',
            RefMsgType='G',
            BusinessRejectReason='5',
            DefaultApplVerID='*'
        )
        super().change_parameters(temp)
        return self

    def set_params_for_business_message_reject_kepler(self):
        temp = dict()
        temp.update(
            RefSeqNum='*',
            Text='*',
            RefMsgType='G',
            BusinessRejectReason='5',
        )
        super().change_parameters(temp)
        return self
