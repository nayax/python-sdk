# Nayax API Python SDK

## min python version: 3

## main.py has example on how to use

```python
merchant_id = '{{ your merchant id}}'
hash_code = '{{ your hash code}}'

nayax_adapter = nayax.Adapter(merchant_id, hash_code)

initiate_payment_request = {
    'amount': 1.23,
    'currency': 'ACP',
    'orderId': 123,
    'methodCode': 'visa',
    'redirectUrl': 'http://example.com',
    'notificationUrl': 'http://example.com',
}

# to get redirect url
redirect_url = nayax_adapter.initiate_payment(initiate_payment_request)
```