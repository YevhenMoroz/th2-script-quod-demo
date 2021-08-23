from datetime import datetime

from quod_qa.wrapper_test.FixMessage import FixMessage


class FixMessageEq(FixMessage):

    def __init__(self, message_type: str, parameters: dict = None):
        super().__init__(message_type=message_type)
        super().add_tag(dict(Account='CLIENT1'))
        super().add_tag(dict(HandlInst=0))
        super().add_tag(dict(Side=1))
        super().add_tag(dict(OrderQty=1000))
        super().add_tag(dict(TimeInForce=0))
        super().add_tag(dict(OrdType=2))
        super().add_tag(dict(TransactTime=datetime.utcnow().isoformat()))
        super().add_tag(dict(OrderCapacity='A'))
        super().add_tag(dict(Price=20))
        super().add_tag(dict(Currency='EUR'))
        super().add_tag(dict(ExDestination='XPAR'))
        super().change_parameters(parameters)
