# flake8: noqa
PAYMENT_DOCS = """API documentation:
Endpoint: https://listen-api.listennotes.com/api/v2
GET /search

This API is for searching podcasts or episodes.

Query parameters table:
q | string | Search term, e.g., person, place, topic... You can use double quotes to do verbatim match, e.g., "game of thrones". Otherwise, it's fuzzy search. | required
type | string | What type of contents do you want to search for? Available values: episode, podcast, curated. default: episode | optional
page_size | integer | The maximum number of search results per page. A valid value should be an integer between 1 and 10 (inclusive). default: 3 | optional
language | string | Limit search results to a specific language, e.g., English, Chinese ... If not specified, it'll be any language. It works only when type is episode or podcast. | optional
region | string | Limit search results to a specific region (e.g., us, gb, in...). If not specified, it'll be any region. It works only when type is episode or podcast. | optional
len_min | integer | Minimum audio length in minutes. Applicable only when type parameter is episode or podcast. If type parameter is episode, it's for audio length of an episode. If type parameter is podcast, it's for average audio length of all episodes in a podcast. | optional
len_max | integer | Maximum audio length in minutes. Applicable only when type parameter is episode or podcast. If type parameter is episode, it's for audio length of an episode. If type parameter is podcast, it's for average audio length of all episodes in a podcast. | optional

Response schema (JSON object):
next_offset | integer | optional
total | integer | optional
results | array[object] (Episode / Podcast List Result Object)

Each object in the "results" key has the following schema:
listennotes_url | string | optional
id | integer | optional
title_highlighted | string | optional

Use page_size: 3


========================================================

Endpoint: https://127.0.0.1:5000
GET /api/merchant/transactions/
 
This API is for getting recent transaction information from Merchant
 
Query parameters table:
custId | string | Request for the Recent Transaction information of Customer| required
transId |string| Request for the Recent Transaction information using Transaction ID | optional
merchantId | string | Request for the Recent Transaction information using Merchant Order ID | optional
 
Response schema (JSON object):
results | array[object] (Recent Transaction Information Result Object)
Each object in the "results" key has the following schema:
transId | string | required
transDt | datetime | optional
merchantId | string | optional
paymentAmt | string | optional
paymentCur | string | optional

Use custId: 5

========================================================

Endpoint: https://127.0.0.1:5000
POST /api/bank/request
 
This API is to request transaction information from bank
 
Query parameters table:
query | string |I would like to check a transaction status| required
 
Response schema (JSON object):
message | string | required

========================================================

Endpoint: https://127.0.0.1:5000
POST /api/bank/verification
 
This API respond to Bank verification requirements
 
Query parameters table:
queryIc | string |Identification Card Number| required
 
Response schema (JSON object):
message | string | required

Use queryIc: 909090135832

========================================================

Endpoint: https://127.0.0.1:5000
POST /api/bank/transaction
 
This API send to Bank the transaction ID
 
Query parameters table:
queryTransId | string |Transaction ID| required
 
Response schema (JSON object):
message | string | required
"""
