from enum import Enum


class MobileUsers(Enum):
    user_1 = "automation_mobile1"
    user_2 = "automation_mobile2"
    user_3 = "automation_mobile3"
    user_4 = "QA4"
    user_5 = "QA5"


class MobilePasswords(Enum):
    password_1 = "QuodNumber1="
    password_2 = "QuodNumber2="
    password_3 = "QuodNumber3="
    password_4 = "QA4"
    password_5 = "QA5"

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
    client1_1 = "mobile_auto1_client1"
    client1_2 = "mobile_auto1_client2"
    client1_3 = "mobile_auto1_client3"
    client2_1 = "mobile_auto2_client1"
    client2_2 = "mobile_auto2_client2"

class MobileAccount(Enum):
    account1_c1_1 = "mobile_auto1_c1_acc1"
    account1_c2_1 = "mobile_auto1_c2_acc1"
    account1_c2_2 = "mobile_auto1_c2_acc2"
    account1_c3_1 = "mobile_auto1_c3_acc1"

class MobileCashAccounts(Enum):
    cash_account1_c1_1 = "mobile_auto1_c1_cash1"
    cash_account1_c2_1 = "mobile_auto1_c2_cash1"
    cash_account1_c3_1 = "mobile_auto1_c3_cash1"
    cash_account1_c3_2 = "mobile_auto1_c3_cash2"

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