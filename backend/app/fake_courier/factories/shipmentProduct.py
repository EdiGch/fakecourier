

class ShipmentProductFactory():
    def __init__(self, item_code, amount, shipment: int):
        self.item_code = item_code
        self.quantity = amount
        self.shipment_id = shipment
