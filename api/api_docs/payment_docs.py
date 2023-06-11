# flake8: noqa
PAYMENT_DOCS = """API documentation:


Endpoint: http://127.0.0.1:5002
GET /api/merchant/transaction/dispute
 
This API is used to query a payment dispute status
 
Request parameters:
custId | string | Customer unique ID | required
 
Response schema (JSON object):
message | string | The status of the payment dispute | required

use custId:5
================================

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

"""
