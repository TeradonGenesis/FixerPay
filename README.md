# FixerPay

### Installation
1. Navigate to the root directory and run  ```pip install -r requirements.txt```

2. Create .env file to set the OPENAI_API_KEY environment variabke in the root folder and modify it as such to use your own api key

```cmd
OPENAI_API_KEY=<Open ai key here>
PINECONE_API_ENV=<Pinecone Environment>
PINECONE_API_KEY=<Pinecone API Key>
```
![image](https://user-images.githubusercontent.com/48543482/235380019-09ab0d93-2f80-43cd-a15f-dd00902f4575.png)

3. In the root directory, run ```python3 app.py```

4. The server should then be up

### Available endpoints

#### Create a book record 

**POST** /api/v1/query

Request
```json
{
    "query": "I want to refund my payment",
}
```

Response
```json
{
    "message": "The payment has been refunded",
}
```
