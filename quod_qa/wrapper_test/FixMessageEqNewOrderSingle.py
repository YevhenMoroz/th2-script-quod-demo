from quod_qa.wrapper_test.FixMessageEq import FixMessageEq


class FixMessageEqNewOrderSingle(FixMessageEq):

    def __init__(self, parameters: dict):
        super().__init__("NewOrderSingle", parameters)
        instrument = dict(
            Symbol='FR0010436584',
            SecurityID='FR0010436584',
            SecurityIDSource='4',
            SecurityExchange='XPAR'
        )
        super().add_tag(dict(instrument=instrument))
        super().add_tag(dict(ExDestination='XPAR'))
        super().parameters = parameters
