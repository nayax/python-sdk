import adapter

myAdd = adapter.Adapter('5787743', 'YWVGU8GM4L')

initiate_payment_request = {
    'amount': 1.23,
    'currency': 'ACP',
    'orderId': 123,
    'methodCode': 'visa',
    'redirectUrl': 'http://example.com',
    'notificationUrl': 'http://example.com',
}

redirect_url = myAdd.initiate_payment(initiate_payment_request)
