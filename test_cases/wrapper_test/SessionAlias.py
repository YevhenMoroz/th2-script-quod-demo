from quod_qa.wrapper_test.DataSet import Connectivity


class SessionAliasOMS:
    def __init__(self):
        self.bs_connectivity = Connectivity.Ganymede_317_bs.value
        self.ss_connectivity = Connectivity.Ganymede_317_ss.value
        self.dc_connectivity = Connectivity.Ganymede_317_dc.value

