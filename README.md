# Travel Expense Tracker API

## 1. Project Description

Travel Expense Tracker is a REST API that helps users manage expenses during a trip.

The API allows users to:

- Create trips
- Add trip members
- Record expenses
- Specify who paid for an expense
- Specify who shared an expense
- Calculate each person's share
- View expenses
- Filter and sort expenses
- View a trip-wise expense summary
- Find who needs to pay and who should receive money

## 2. Technologies Used

- Python
- FastAPI
- Pydantic
- MongoDB
- PyMongo
- Uvicorn

## 3. Project Structure

Expense Tracker/
├── main.py
├── models.py
├── database.py
├── README.md
└── venv/

## 4. Installation

Create a virtual environment:

python -m venv venv

Install the required packages:

pip install fastapi uvicorn pymongo python-dotenv

## 5. MongoDB Setup

The application uses MongoDB.

MongoDB connection:

mongodb://localhost:27017

Database name:

expense_tracker

Collections:

- trips
- expenses

## 6. Running the Application

Start the FastAPI server:

uvicorn main:app --reload

The API runs at:

http://127.0.0.1:8000

Swagger UI is available at:

http://127.0.0.1:8000/docs

Swagger UI can be used to test all API endpoints.

## 7. API Endpoints

### Trip APIs

POST /trips

Create a new trip.

GET /trips/{trip_id}

Get trip details.

### Expense APIs

POST /trips/{trip_id}/expenses

Add an expense.

GET /trips/{trip_id}/expenses

View trip expenses.

GET /expenses/{expense_id}

Get one expense.

PUT /expenses/{expense_id}

Update an expense.

DELETE /expenses/{expense_id}

Delete an expense.

### Summary API

GET /trips/{trip_id}/summary

Get the trip expense summary.

## 8. Example: Create Trip

Request:

{
  "name": "Goa Trip",
  "destination": "Goa",
  "members": [
    "Praveen",
    "Rahul",
    "Suresh"
  ]
}

Response:

{
  "message": "Trip created successfully",
  "trip_id": "6aa395a23f66e611db54ce61"
}

## 9. Example: Create Expense

Request:

{
  "title": "Goa Dinner",
  "amount": 1500,
  "category": "Food",
  "paid_by": "Praveen",
  "shared_by": [
    "Praveen",
    "Rahul",
    "Suresh"
  ],
  "date": "2026-09-11",
  "description": "Dinner at Goa"
}

Expense Calculation:

1500 / 3 = 500

Therefore, each person's share is ₹500.

## 10. Filtering and Sorting

The expense API supports filtering by:

- Category
- Paid by
- Date
- Minimum amount
- Maximum amount

Expenses can be sorted by:

- Amount
- Date

Example:

GET /trips/{trip_id}/expenses?category=Food

Example:

GET /trips/{trip_id}/expenses?sort_by=amount&order=desc

## 11. Trip Summary

The summary API calculates:

- Total expenses
- Amount paid by each member
- Individual share
- Balance
- Amount to receive
- Amount owed

Example:

{
  "trip_id": "6aa395a23f66e611db54ce61",
  "trip_name": "Goa Trip",
  "total_expenses": 3000,
  "members": {
    "Praveen": {
      "paid": 3000,
      "share": 1000,
      "balance": 2000,
      "status": "receive"
    },
    "Rahul": {
      "paid": 0,
      "share": 1000,
      "balance": -1000,
      "status": "owe"
    },
    "Suresh": {
      "paid": 0,
      "share": 1000,
      "balance": -1000,
      "status": "owe"
    }
  }
}

## 12. Validation and Error Handling

The API handles:

- Invalid trip ID
- Invalid expense ID
- Trip not found
- Expense not found
- Invalid expense amount
- Payer not belonging to the trip
- Shared member not belonging to the trip
- Missing required fields

## 13. Testing

The API was tested using FastAPI Swagger UI.

The following features were tested:

- Create trip
- Get trip
- Create expense
- Get expenses
- Get individual expense
- Update expense
- Delete expense
- Filter expenses
- Sort expenses
- Calculate expense shares
- Generate trip summary
- Validation and error handling

## 14. Screenshots

Swagger UI testing screenshots are included in the `screenshots/` folder.

The screenshots demonstrate:

- Create trip
- Get trip
- Create expense and expense calculation
- Filter and sort expenses
- Get individual expense
- Update expense
- Delete expense
- Trip summary
- Validation error
- Error handling
- All API endpoints