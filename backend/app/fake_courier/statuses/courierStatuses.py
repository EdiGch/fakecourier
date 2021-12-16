from typing import List, Dict
import random


class CourierStatuses():
    ddef = 8  # odebrano powiadomienie o wysyłce, data dostawy wciąż nieznana
    init = 10  # paczka została zważona i czeka na dalsze rozmieszczenie
    xdly = 132  # przesyłka została zmagazynowana i zostanie dostarczona zgodnie z harmonogramem
    dmgd = 145  # możliwe uszkodzenie wykryte, może być dostarczone w oczekiwaniu na stopień uszkodzenia
    ovsz = 162  # ponadgabarytowa paczka
    lost = 62  # przesyłka zaginęła. Skontaktuje się z Tobą dział obsługi klienta
    nloc = 160  # przesyłka nie jest obecnie zlokalizowana
    rets = 260  # powrót do nadawcy
    tour = 30  # przesyłka została załadowana do samochodu dostawczego
    ddsp = 38  # przesyłka nie została doręczona / odbiorca zamówił zmianę adresu lub przedziału czasowego
    deps = 71  # przesyłka dotarła do naszego lokalnego HUBu w oczekiwaniu na odbiór odbiorcy
    adru = 80  # przesyłka nie została dostarczona z powodu nieznanego/błędnego adresu. Kolejna próba doręczenia
    # nastąpi po otrzymaniu przez nas prawidłowego adresu lub danych. Po 5 dniach przesyłka zostanie zwrócona do nadawcy
    refu = 100  # przesyłka nie została dostarczona, ponieważ odbiorca odmówił jej przyjęcia.
    rcvu = 110  # przesyłka nie została dostarczona, ponieważ nie było zaadresowanego odbiorcy. Kolejna próba
    # doręczenia nastąpi po otrzymaniu prawidłowych danych odbiorcy. Po 5 dniach przesyłka zostanie zwrócona do nadawcy
    abst = 130  # przesyłka nie została dostarczona z powodu nieobecności odbiorcy . Następna próba doręczenia
    # nastąpi po tym, jak odbiorca poprosi/zorganizuje następną próbę. Po 5 dniach przesyłka zostanie zwrócona do nadawcy
    dely = 40  # przesyłka została dostarczona
    cash = 41  # Pieniądze za pobraniem są zbierane
    delr = 134  # przesyłka zwrócona do pierwotnego nadawcy

    def get_all_statuses_list(self) -> List:
        statuses_list_dict = []
        statuses_list = ['ddef', 'init', 'xdly', 'dmgd', 'ovsz', 'lost', 'nloc', 'rets', 'tour', 'ddsp', 'deps', 'adru',
                         'refu', 'rcvu', 'abst', 'dely', 'cash', 'delr']

        for item_list in statuses_list:
            statuses_dict = {'StatusID': self.__getattribute__(item_list), 'StatusName': item_list}
            statuses_list_dict.append(statuses_dict)

        return statuses_list_dict

    def get_all_statuses_dict(self) -> Dict:
        statuses_dict = {
            8: {
                'StatusID': 8,
                'StatusName': 'ddef',
                'StatusDescription': 'odebrano powiadomienie o wysyłce, data dostawy wciąż nieznana',
                'CabrozStatusMapped': 'ApprovedAfterExternalVerification'
            },
            10: {
                'StatusID': 10,
                'StatusName': 'init',
                'StatusDescription': 'paczka została zważona i czeka na dalsze rozmieszczenie',
                'CabrozStatusMapped': 'PendingPickupByCourier'
            },
            132: {
                'StatusID': 132,
                'StatusName': 'xdly',
                'StatusDescription': 'przesyłka została zmagazynowana i zostanie dostarczona zgodnie z harmonogramem',
                'CabrozStatusMapped': 'Sent'
            },
            145: {
                'StatusID': 145,
                'StatusName': 'dmgd',
                'StatusDescription': 'możliwe uszkodzenie wykryte, może być dostarczone w oczekiwaniu na stopień uszkodzenia',
                'CabrozStatusMapped': 'Sent'
            },
            162: {
                'StatusID': 162,
                'StatusName': 'ovsz',
                'StatusDescription': 'ponadgabarytowa paczka',
                'CabrozStatusMapped': 'AwaitingForInstructions'
            },
            62: {
                'StatusID': 62,
                'StatusName': 'lost',
                'StatusDescription': 'przesyłka zaginęła. Skontaktuje się z Tobą dział obsługi klienta',
                'CabrozStatusMapped': 'Lost'
            },
            160: {
                'StatusID': 160,
                'StatusName': 'nloc',
                'StatusDescription': 'przesyłka nie jest obecnie zlokalizowana',
                'CabrozStatusMapped': 'AwaitingForInstructions'
            },
            260: {
                'StatusID': 260,
                'StatusName': 'rets',
                'StatusDescription': 'powrót do nadawcy',
                'CabrozStatusMapped': 'Undelivered'
            },
            30: {
                'StatusID': 30,
                'StatusName': 'tour',
                'StatusDescription': 'przesyłka została załadowana do samochodu dostawczego',
                'CabrozStatusMapped': 'Sent'
            },
            38: {
                'StatusID': 38,
                'StatusName': 'ddsp',
                'StatusDescription': 'przesyłka nie została doręczona / odbiorca zamówił zmianę adresu lub przedziału czasowego',
                'CabrozStatusMapped': 'AwaitingForInstructions'
            },
            71: {
                'StatusID': 71,
                'StatusName': 'deps',
                'StatusDescription': 'przesyłka dotarła do naszego lokalnego HUBu w oczekiwaniu na odbiór odbiorcy',
                'CabrozStatusMapped': 'AwaitingOnAccessPoint'
            },
            80: {
                'StatusID': 80,
                'StatusName': 'adru',
                'StatusDescription': 'przesyłka nie została dostarczona z powodu nieznanego/błędnego adresu. Kolejna próba doręczenia nastąpi po otrzymaniu przez nas prawidłowego adresu lub danych. Po 5 dniach przesyłka zostanie zwrócona do nadawcy',
                'CabrozStatusMapped': 'AwaitingForInstructions'
            },
            100: {
                'StatusID': 100,
                'StatusName': 'refu',
                'StatusDescription': 'przesyłka nie została dostarczona, ponieważ odbiorca odmówił jej przyjęcia.',
                'CabrozStatusMapped': 'AwaitingForInstructions'
            },
            110: {
                'StatusID': 110,
                'StatusName': 'rcvu',
                'StatusDescription': 'przesyłka nie została dostarczona, ponieważ nie było zaadresowanego odbiorcy. Kolejna próba doręczenia nastąpi po otrzymaniu prawidłowych danych odbiorcy. Po 5 dniach przesyłka zostanie zwrócona do nadawcy',
                'CabrozStatusMapped': 'AwaitingForInstructions'
            },
            130: {
                'StatusID': 130,
                'StatusName': 'abst',
                'StatusDescription': 'przesyłka nie została dostarczona z powodu nieobecności odbiorcy. Następna próba doręczenia nastąpi po tym, jak odbiorca poprosi/zorganizuje następną próbę. Po 5 dniach przesyłka zostanie zwrócona do nadawcy',
                'CabrozStatusMapped': 'AwaitingForInstructions'
            },
            40: {
                'StatusID': 40,
                'StatusName': 'dely',
                'StatusDescription': 'przesyłka została dostarczona',
                'CabrozStatusMapped': 'Delivered'
            },
            41: {
                'StatusID': 41,
                'StatusName': 'cash',
                'StatusDescription': 'Pieniądze za pobraniem są zbierane',
                'CabrozStatusMapped': 'Delivered'
            },
            134: {
                'StatusID': 134,
                'StatusName': 'delr',
                'StatusDescription': 'przesyłka zwrócona do pierwotnego nadawcy',
                'CabrozStatusMapped': 'Undelivered'
            },
        }

        return statuses_dict

    def get_by_value_from_list(self, value: int) -> Dict:
        statuses_list_dict = self.get_all_statuses_list()
        status_dict = {}
        for status_dict_key in statuses_list_dict:
            if status_dict_key['StatusID'] == value:
                status_dict = status_dict_key

        return status_dict

    def get_by_value_from_dict(self, value: int) -> Dict:
        statuses_dict = self.get_all_statuses_dict()
        status_dict = {}
        for statuses_dict_key in statuses_dict:
            if statuses_dict_key == value:
                status_dict = statuses_dict[statuses_dict_key]

        return status_dict

    def get_random_status_from_dict(self) -> Dict:
        statuses_list_dict = self.get_all_statuses_list()
        status_list = []
        for status_dict_key in statuses_list_dict:
            status_list.append(status_dict_key['StatusID'])

        # print(status_list[random.randint(0, len(status_list))])
        return self.get_by_value_from_dict(status_list[random.randint(0, len(status_list))])
