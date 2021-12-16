import uuid


class ShipmentFactory():
    def __init__(self, unit_amount, ref1, ref2, delivery_remark, cod_value, commission_type, cod_currency):
        self.tracking_no = uuid.uuid4().hex.upper()[0:12]
        self.unit_amount = unit_amount
        self.ref1 = ref1
        self.ref2 = ref2
        self.delivery_remark = delivery_remark
        self.cod_value = cod_value
        self.commission_type = commission_type
        self.cod_currency = cod_currency
