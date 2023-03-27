from enum import Enum


class MobileUsers(Enum):
    user_1 = "a_MobileQA1"
    user_2 = "a_MobileQA2"
    user_3 = "a_MobileQA3"
    user_4 = "a_MobileQA4"
    user_5 = "a_MobileQA5"


class MobilePasswords(Enum):
    password_1 = "a_MobileQA1!"
    password_2 = "a_MobileQA1!"
    password_3 = "a_MobileQA3!"
    password_4 = "a_MobileQA4!"
    password_5 = "a_MobileQA5!"

class UserPersonalDetails(Enum):
    user_1 = {
        "FirstName":"FName",
        "LastName":"LName",
        "DateOfBirth":"2001-03-02",
        "Address":"Highway",
        "Country":"Ukraine",
        "PreferredCommunicationMethod":"Email",
        "E-mail":"mail@quodfinancial.com",
        "Mobile":"123456789",
        "PasswordExpiration":"2027-11-03",
    }

class MobileClients(Enum):
    desk1_client1 = "a_mobile1_client1"

class MobileAccount(Enum):
    desk1_client1_acc1 = "a_mobile1_client1_acc1"

class MobileCashAccounts(Enum):
    desk1_client1_cash1 = "a_mobile1_client1_cash1_INR"

class MobileInstrument(Enum):
    instrument_1 = "TCS-IQ"
    instrument_2 = "SBIN-IQ"
    instrument_3 = "SPICEJET-IQ"

class MobileOrderType(Enum):
    order_type_1 = "Limit"
    order_type_2 = "Market"
    order_type_3 = "Stop"
    order_type_4 = "StopLimit"

class MobileTimeInForce(Enum):
    time_in_force_1 = "Day"
    time_in_force_2 = "GoodTillCancel"
    time_in_force_3 = "GoodTillDate"
    time_in_force_4 = "FillOrKill"
    time_in_force_5 = "ImmediateOrCancel"