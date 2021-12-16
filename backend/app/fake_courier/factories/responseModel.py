class ResponseModel():
    def __init__(self, shipment, pickup_time, pickupend_time, delivery_time, deliveryend_time, trace_ID, status, error, validations):
        self.shipmentid = shipment
        self.pickuptime = pickup_time
        self.pickupendtime = pickupend_time
        self.deliverytime = delivery_time
        self.deliveryendtime = deliveryend_time
        self.TraceID = trace_ID
        self.status = status
        self.error = error
        self.validations = validations
