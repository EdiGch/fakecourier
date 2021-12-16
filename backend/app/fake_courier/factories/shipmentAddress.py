class ShipmentAddressFactory():
    def __init__(self, name: str, shipment: int, countryCode: str, zipcode: str, city: str, streetAndNumber: str,
                 telephone: str, fax: str,
                 notifyGSM: str, notifyEmail: str):
        self.name = name
        self.shipment_id = shipment
        self.country_code = countryCode
        self.zipcode = zipcode
        self.city = city
        self.street_and_number = streetAndNumber
        self.telephone = telephone
        self.fax = fax
        self.notify_gsm = notifyGSM
        self.notify_email = notifyEmail
