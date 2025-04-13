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

## ⚙️ Local Setup

```bash
git clone https://github.com/your-username/orders-api.git
cd orders_api
python3 -m venv venv
source venv/bin/activate
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
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cdk deploy
> ⚠️ **Note**: Make sure Docker is running. CDK uses Docker to bundle the Lambda function using the correct architecture for AWS.
```

Your API will be available at the printed endpoint (e.g. `https://xyz.execute-api.eu-west-2.amazonaws.com/prod/`).

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