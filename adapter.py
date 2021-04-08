import base64
import urllib.parse
from hashlib import sha256


class Adapter:
    API_URL = 'https://uiservices.ecom.nayax.com/hosted/'

    STATUS_SUCCESS = 'success'
    STATUS_ERROR = 'error'

    def __init__(self, merchant_id, hash_code):
        self.MERCHANT_ID = merchant_id
        self.HASH_CODE = hash_code

    def initiate_payment(self, initiate_payment_request):
        transaction = {
            'merchantID': self.MERCHANT_ID,
            'trans_amount': initiate_payment_request['amount'],
            'trans_currency': initiate_payment_request['currency'],
            'trans_type': 0,  # debit
            'trans_installments': 1,
            'trans_refNum': initiate_payment_request['orderId'],
            'disp_paymentType': 'CC',
            'url_redirect': initiate_payment_request['redirectUrl'],
            'notification_url': initiate_payment_request['notificationUrl'],
        }

        signature_key = 'signature'
        signature = self.create_signature(transaction)
        transaction[signature_key] = signature
        return self.get_redirect_url(transaction)

    def create_signature(self, transaction):
        concatenated_transaction = ''
        concatenated_transaction += str(transaction['merchantID'])
        concatenated_transaction += str(transaction['trans_refNum'])
        concatenated_transaction += str(transaction['trans_installments'])
        concatenated_transaction += str(transaction['trans_amount'])
        concatenated_transaction += str(transaction['trans_currency'])
        concatenated_transaction += str(transaction['trans_type'])
        concatenated_transaction += str(transaction['disp_paymentType'])
        concatenated_transaction += str(transaction['notification_url'])
        concatenated_transaction += str(transaction['url_redirect'])
        concatenated_transaction += str(self.HASH_CODE)

        return urllib.parse.quote_plus(
            base64.b64encode(
                sha256(concatenated_transaction.encode('utf-8')).digest()
            )
        )

    def get_redirect_url(self, transaction):
        redirect_url = self.API_URL
        redirect_url += '?merchantID=' + str(self.MERCHANT_ID)
        redirect_url += '&trans_refNum=' + str(transaction['trans_refNum'])
        redirect_url += '&trans_installments=' + str(transaction['trans_installments'])
        redirect_url += '&trans_amount=' + str(transaction['trans_amount'])
        redirect_url += '&trans_currency=' + str(transaction['trans_currency'])
        redirect_url += '&trans_type=' + str(transaction['trans_type'])
        redirect_url += '&disp_paymentType=' + str(transaction['disp_paymentType'])
        redirect_url += '&notification_url=' + urllib.parse.quote_plus(transaction['notification_url'])
        redirect_url += '&url_redirect=' + urllib.parse.quote_plus(transaction['url_redirect'])
        redirect_url += '&signature=' + transaction['signature']

        return redirect_url

    def handle_notification(self, notification):
        description = notification.get('replyDesc', notification.get('ReplyDesc', ''))
        code = notification.get('code', notification.get('replyCode', ''))
        original_transaction_id = notification.get('trans_refNum', notification.get('Order', ''))

        inner_transaction_id = notification['trans_id']
        amount = notification['trans_amount']
        currency = notification['trans_currency']

        notification_details = {
            'description': description,
            'original_order_id': original_transaction_id,
            'internal_transaction_id': inner_transaction_id,
            'amount': amount,
            'currency': currency,
            'notification': notification
        }

        if code == '000' or code == '000.000.000':
            notification_details['status'] = self.STATUS_SUCCESS
        else:
            notification_details['status'] = self.STATUS_ERROR

        return notification_details
