from test_framework.data_sets.base_data_set import BaseDataSet
from test_framework.data_sets.oms_data_set.oms_const_enum import OmsVenues, OmsClients, OmsAccounts, \
    OmsWashbookAccounts, OmsRecipients, OmsFixInstruments, OmsDbListing, OmsDbInstrument, OmsMic, OmsCurrency, \
    OmsVenueClientNames, OmsRoutes, OmsLookupForVenues, OMSCommissionProfiles, OMSFeeType, OMSExecScope, OMSFee, \
    OMSCommission


class OmsDataSet(BaseDataSet):
    """
    Product line dataset class that overrides attributes from BaseDataSet parent class.
    """
    fix_instruments = OmsFixInstruments
    venues = OmsVenues
    clients = OmsClients
    accounts = OmsAccounts
    washbook_accounts = OmsWashbookAccounts
    recipients = OmsRecipients
    db_listing = OmsDbListing
    db_instrument = OmsDbInstrument
    mic = OmsMic
    currency = OmsCurrency
    venue_client_names = OmsVenueClientNames
    routes = OmsRoutes
    lookups = OmsLookupForVenues
    commission_profiles = OMSCommissionProfiles
    misc_fee_type = OMSFeeType
    fee_exec_scope = OMSExecScope
    fee = OMSFee
    commission = OMSCommission
