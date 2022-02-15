import time
import traceback
from datetime import timedelta

from test_cases.web_admin.web_admin_core.utils.web_driver_container import WebDriverContainer
from custom import basic_custom_actions as bca
from test_cases.web_admin.web_admin_test_cases.reference_data.QAP_1727 import QAP_1727
from test_cases.web_admin.web_admin_test_cases.reference_data.QAP_1729 import QAP_1729
from test_cases.web_admin.web_admin_test_cases.reference_data.QAP_1731 import QAP_1731
from test_cases.web_admin.web_admin_test_cases.reference_data.QAP_1732 import QAP_1732
from test_cases.web_admin.web_admin_test_cases.reference_data.QAP_1733 import QAP_1733
from test_cases.web_admin.web_admin_test_cases.reference_data.QAP_1736 import QAP_1736
from test_cases.web_admin.web_admin_test_cases.reference_data.QAP_1737 import QAP_1737
from test_cases.web_admin.web_admin_test_cases.reference_data.QAP_2154 import QAP_2154
from test_cases.web_admin.web_admin_test_cases.reference_data.QAP_2302 import QAP_2302
from test_cases.web_admin.web_admin_test_cases.reference_data.QAP_2504 import QAP_2504
from test_cases.web_admin.web_admin_test_cases.reference_data.QAP_2904 import QAP_2904
from test_cases.web_admin.web_admin_test_cases.reference_data.QAP_2905 import QAP_2905
from test_cases.web_admin.web_admin_test_cases.reference_data.QAP_2940 import QAP_2940
from test_cases.web_admin.web_admin_test_cases.reference_data.QAP_2971 import QAP_2971
from test_cases.web_admin.web_admin_test_cases.reference_data.QAP_3136 import QAP_3136
from test_cases.web_admin.web_admin_test_cases.reference_data.QAP_3399 import QAP_3399
from test_cases.web_admin.web_admin_test_cases.reference_data.QAP_4153 import QAP_4153
from test_cases.web_admin.web_admin_test_cases.reference_data.QAP_4709 import QAP_4709
from test_cases.web_admin.web_admin_test_cases.reference_data.QAP_4861 import QAP_4861
from test_cases.web_admin.web_admin_test_cases.reference_data.QAP_4862 import QAP_4862
from test_cases.web_admin.web_admin_test_cases.reference_data.QAP_5815 import QAP_5815
from test_cases.web_admin.web_admin_test_cases.reference_data.QAP_755 import QAP_755
from test_cases.web_admin.web_admin_test_cases.reference_data.QAP_756 import QAP_756
from test_cases.web_admin.web_admin_test_cases.reference_data.QAP_758 import QAP_758
from test_cases.web_admin.web_admin_test_cases.reference_data.QAP_759 import QAP_759
from test_cases.web_admin.web_admin_test_cases.reference_data.QAP_760 import QAP_760
from test_cases.web_admin.web_admin_test_cases.reference_data.QAP_761 import QAP_761
from test_cases.web_admin.web_admin_test_cases.reference_data.QAP_762 import QAP_762
from test_cases.web_admin.web_admin_test_cases.reference_data.QAP_763 import QAP_763
from test_cases.web_admin.web_admin_test_cases.reference_data.QAP_6299 import QAP_6299
from test_cases.web_admin.web_admin_test_cases.reference_data.QAP_6298 import QAP_6298


class ReferenceData:
    def __init__(self, web_driver_container: WebDriverContainer, root_report_id):
        self.folder_name = 'WebAdmin'
        self.first_lvl_id = bca.create_event(self.__class__.__name__, root_report_id)
        self.second_lvl_id = bca.create_event(self.folder_name, self.first_lvl_id)
        self.web_driver_container = web_driver_container

    def execute(self):
        try:
            start_time = time.monotonic()

# TODO: Перепроврить 7** кейсы
            QAP_755(self.web_driver_container, self.second_lvl_id).run()
            QAP_756(self.web_driver_container, self.second_lvl_id).run()
            QAP_758(self.web_driver_container, self.second_lvl_id).run()
            QAP_759(self.web_driver_container, self.second_lvl_id).run()
            QAP_760(self.web_driver_container, self.second_lvl_id).run()
            QAP_761(self.web_driver_container, self.second_lvl_id).run()
            QAP_762(self.web_driver_container, self.second_lvl_id).run()
            QAP_763(self.web_driver_container, self.second_lvl_id).run()

# Не совсем актуальный АТ. Нет проверки степа 3 из ТК. В самом степе ER отличается от AR, получаем другое содерждмое сообщения
# Мануально - фейл, авто ОК. Новый Профиль не создается.
            QAP_1727(self.web_driver_container, self.second_lvl_id).run() #// добавь проверку на 3 степ

# Не совсем актуальный АТ. Нет проверки степа 3 из ТК. В самом степе ER отличается от AR, получаем другое содерждмое сообщения
# Мануально - фейл, авто ОК. Новый Профиль не создается.
            QAP_1729(self.web_driver_container, self.second_lvl_id).run() #//добавь проверку на 3 степ

            QAP_1731(self.web_driver_container, self.second_lvl_id).run()

# Не увидел проверку из степа 2 на "InstSymbol is greyout"
# // set в поле МДМАХСплит. Добавить чек на актив/неактив элемента
            QAP_1732(self.web_driver_container, self.second_lvl_id).run()

# Не пойму почему в верифаере AR и ER = True вместо проверки успешного сообщения
# // После удаления сделать проверку, что элемента нет. (Можно ч-з поиск в фильре → Мор экшн)
            QAP_1733(self.web_driver_container, self.second_lvl_id).run()

            QAP_1736(self.web_driver_container, self.second_lvl_id).run()

# В ТК не упоминается об проверки ПДФ выгрузки. Мне кажется кейс не совсем актуален.
# // Сделать вместо проверки ПДФ, сделать через эдит
            QAP_1737(self.web_driver_container, self.second_lvl_id).run()

# В атвтотестне не увидел проверки на то, что кнопка действительно была выкл или вкл. И проверки в листинге.
# // Добавит ьпроверку на енейбл/дизейбл и на чекбокс
            QAP_2154(self.web_driver_container, self.second_lvl_id).run()

# В ТК не упоминается об заполнение set_cum_trading_limit_percentage
# // убрать лишнее
            QAP_2302(self.web_driver_container, self.second_lvl_id).run()

# Я бы убрал заполнения полей которые не используются в тесте.
# // Тогда не будет работать поиск по листингу.
            QAP_2504(self.web_driver_container, self.second_lvl_id).run()

# Проверить скорость обработки через парсинг и матч.
            QAP_2904(self.web_driver_container, self.second_lvl_id).run()

# авто-тест не проверяет степ 11: "Verify that FeedSource field is not editable."
# //Добавить проверку
            QAP_2905(self.web_driver_container, self.second_lvl_id).run()

# авто-тест не проверяет степ 14: "FeedSource field is not editable."
# //Добавить проверку
            QAP_2940(self.web_driver_container, self.second_lvl_id).run()

# не увидел проверки на реквайред поля
# //Добавить проверки. Заявязаться на реквайред в теге
            QAP_2971(self.web_driver_container, self.second_lvl_id).run()

# Не увидел проверу степа 10. profiles.set_routing_param_group(self.name_at_routing_param_groups) - не выполняет мач.
# // Доделать
            QAP_3136(self.web_driver_container, self.second_lvl_id).run()
#
            QAP_3399(self.web_driver_container, self.second_lvl_id).run()
            QAP_4153(self.web_driver_container, self.second_lvl_id).run()

# В авто-тесте не выполнен степ 4 из ТК
# //Реализовать степ 4
            QAP_4709(self.web_driver_container, self.second_lvl_id).run()

# не совсем понятно для чего в авто-тесте строки 63-69
# // Проверить .clear(), или же send_keys. (clear_enter_field)
            QAP_4861(self.web_driver_container, self.second_lvl_id).run()

# не совсем понятно для чего в авто-тесте строки 55-61
# // Проверить .clear(), или же send_keys. (clear_enter_field)
            QAP_4862(self.web_driver_container, self.second_lvl_id).run()

            QAP_5815(self.web_driver_container, self.second_lvl_id).run()

            QAP_6299(self.web_driver_container, self.second_lvl_id).run()
            QAP_6298(self.web_driver_container, self.second_lvl_id).run()

            end_time = time.monotonic()
            print("Reference data ~execution time~ = " + str(timedelta(seconds=end_time - start_time)))

        except Exception:
            print(traceback.format_exc() + " Execute ERROR !->  " + self.__class__.__name__)




