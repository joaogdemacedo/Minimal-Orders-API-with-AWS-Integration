# 🧾 Minimal Orders API with AWS Integration

This project is a minimal backend API to manage orders. Built with **FastAPI**, deployed to **AWS Lambda**, and defined via **AWS CDK**, it fulfills all core requirements of the backend challenge – and includes several extras.

---

## 📋 Feature Coverage

| 📌 Requirements                                      | ✅ Implemented                                                                 |
|---------------------------------------------------------------------|----------------------------------------------------------------------------------------|
| **POST /orders/create** – Create a new order                               | FastAPI route to create order, stored in DynamoDB                                      |
| **GET /orders/{id}** – Fetch a specific order                       | Lookup by `id` with error handling for not found                                       |
| **GET /orders** – List all orders                                   | Returns paginated list with encoded cursor support                                     |
| **DELETE /orders/{id}** – Cancel/delete an order                    | Marks order as `cancelled` in DynamoDB                                                 |
| Use a **lightweight setup**                                               | Used **FastAPI** with Pydantic models and JWT support                                  |
| Store data in **AWS (DynamoDB, S3, etc.)**                          | Used **DynamoDB** for persistence                                                      |
| Use AWS **Lambda**, Express, or lightweight setup                   | Deployed with **AWS Lambda + API Gateway** using `Mangum`                              |
| Add a **README** with local/deploy instructions                     | ✅ You're looking at it 😉 Includes local run, test, and deploy info                   |

---

## 💡 Bonus

| 🌟 Bonus or 🚀 Extra Bonus | ✅ Delivered |
|-------------------|-------------|
| 🌟 Implement **authentication**                    | Implemented **JWT OAuth2** with `/login` and FastAPI `Depends` integration               |
| 🌟 Add **tests**                                                       | Added `pytest`-based tests for all endpoints, incl. edge cases                         |
| 🌟 Use **Infrastructure-as-Code**              | Defined infrastructure using **AWS CDK (Python)**                                      |
| 🚀 **Pagination** on `/orders` | ✅ Cursor-based with `next_key` |
| 🚀 **Field-level input validation** | ✅ Regex + type constraints |
| 🚀 **Swagger UI locally** | ✅ Available at `/docs` |
| 🚀 **Swagger in Lambda** | ⚠️ Not working due to CORS (Postman used) |
| 🚀 **Postman testing support** | ✅ Auth + endpoints tested via Postman |
| 🚀 **Centralized logging for debugging** | ✅ Added clean log statements to routes, services, and auth for CloudWatch & local visibility |
| 🚀 **Custom exception handling** | ✅ Defined and used custom exceptions (e.g. `OrderNotFoundException`, `InvalidStartKeyException`) for cleaner error logic |
| 🚀 **Security-conscious input validation** | ✅ Prevented invalid strings & XSS |
---

## 📁 Project Structure

```text
Minimal-Orders-API-with-AWS-Integration/
├── orders_api/                  # FastAPI application
│   ├── app/
│   │   ├── routes/              # Routes for orders and auth
│   │   ├── models/              # Pydantic models
│   │   ├── services/            # Business logic
│   │   ├── db/                  # DynamoDB integration
│   │   ├── exceptions/          # Custom error classes
│   │   └── main.py              # Main app (local dev)
│   │   └── main_lambda.py       # Entry point for AWS Lambda
│   ├── tests/                   # Pytest test cases
│   └── requirements.txt         # App dependencies
│
├── infra/                       # AWS CDK infrastructure
│   ├── infra/                   # CDK stack definition
│   ├── app.py                   # CDK entry point
│   ├── cdk.json                 # CDK config
│   └── requirements.txt         # Infra dependencies
│
├── Orders-API.postman_collection.json    # Postman collection
│
├── README.md
└── LICENSE
```

## ⚙️ Requirements

To run this project locally or deploy to AWS, you must have:

- Python 3.11+
- AWS CLI installed
- Docker installed & running (for Lambda packaging via CDK)
- AWS credentials configured (`aws configure`) with necessary permissions

> ⚠️ You must have valid AWS credentials and a default region set to run or deploy this app.
---


## ⚙️ Local Setup

```bash
git clone https://github.com/your-username/orders-api.git
cd orders_api
pip install -r requirements.txt
export PYTHONPATH=./app
```

---

## ▶️ Run Locally

```bash
uvicorn app.main:app --reload
```

Open Swagger UI at: [http://localhost:8000/docs](http://localhost:8000/docs)

---

## ☁️ Deploy via AWS CDK

```bash
cd infra
pip install -r requirements.txt
cdk deploy
> ⚠️ **Note**: Make sure Docker is running. CDK uses Docker to bundle the Lambda function using the correct architecture for AWS.
```

Your API will be available at the printed endpoint (e.g. `https://xyz.execute-api.eu-west-2.amazonaws.com/prod/`).

---

## 📦 Postman Collection

A Postman collection is available to test the API endpoints.

- File: `Orders-API.postman_collection.json`
- Format: Postman 2.1
- Includes login, JWT-protected routes, and pagination

---

## 🔐 Auth Flow

- `POST /login` – Accepts hardcoded credentials and returns a JWT
- JWT must be passed as Bearer token to access `/orders` endpoints
- Tokens expire in 1 year

---

## 🧪 Running Tests

```bash
export PYTHONPATH=./app
pytest
```

Tests include:
- Creating and listing orders
- Token protection
- Invalid payloads
- Pagination edge cases

---

## 📝 Notes

- Swagger is fully functional in local dev
- Due to CORS, Swagger UI is not functional on deployed Lambda → use Postman
- Infrastructure defined and deployed using CDK v2
- CDK handles: DynamoDB, Lambda, API Gateway

---

## 🙌 Final Thoughts

This project showcases a production-ready FastAPI app with:
- Secure JWT authentication
- AWS-native persistence and deployment
- Clean modular codebase
- Test coverage and validation