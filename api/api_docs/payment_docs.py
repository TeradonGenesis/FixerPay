# flake8: noqa
PAYMENT_DOCS = """API documentation:

Endpoint: http://127.0.0.1:5002
GET /api/merchant/transactions
 
This API run first and is for getting recent transaction information from Merchant before requesting transaction information from Bank.
 
Query parameters table:
custId |string| Send Customer ID to Merchant | required
record |string| Request for the Recent Transaction information using Transaction ID | required
 
Response schema (JSON object):
results | array[object] (Recent Transaction Information Result Object)
Each object in the "results" key has the following schema:
mercTransId | string | required
bankTxnId | string | required
transDt | datetime | optional
mercOrderId | string | optional
paymentAmt | string | optional
paymentCur | string | optional

use custId: 909090135832
use record: latest
========================================================

Endpoint: http://127.0.0.1:5002
GET /api/bank/transaction/status
 
This API run last and is to request transaction information from bank after verifying the customer IC with the Bank.
 
Query parameters table:
bankTxnId | string | Bank Transaction number | required
hash | string | The hash key given by the bank to allow the calls for the bank transaction api | required
 
Response schema (JSON object):
status | string | required

use bankTxnId:999999
use hash:999999

========================================================

Endpoint: http://127.0.0.1:5002
POST /api/bank/transaction/verification
 
This API run 2nd and is sending the customer IC for verification first before requesting the transaction information.
 
Request parameters table:
ic | string |Identification Card Number| required
 
Response schema (JSON object):
hash | string | Hash key returned by the bank to authenticate the next bank api calls | required

Use ic: 909090135832

"""
