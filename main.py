from fastapi import FastAPI, HTTPException
from models import TripCreate,ExpenseCreate
from database import trips_collection, expenses_collection
from bson import ObjectId

app = FastAPI()


@app.get("/")
def home():
    return {
        "message": "Travel Expense Tracker API is running"
    }


@app.post("/trips")
def create_trip(trip: TripCreate):
    trip_data = trip.model_dump()

    result = trips_collection.insert_one(trip_data)

    return {
        "message": "Trip created successfully",
        "trip_id": str(result.inserted_id)
    }
@app.get("/trips/{trip_id}")
def get_trip(trip_id: str):

    if not ObjectId.is_valid(trip_id):
        raise HTTPException(
            status_code=400,
            detail="Invalid trip ID"
        )

    trip = trips_collection.find_one({
        "_id": ObjectId(trip_id)
    })

    if not trip:
        raise HTTPException(
            status_code=404,
            detail="Trip not found"
        )

    trip["_id"] = str(trip["_id"])

    return trip


@app.post("/trips/{trip_id}/expenses")
def create_expense(trip_id: str, expense: ExpenseCreate):

    if not ObjectId.is_valid(trip_id):
        raise HTTPException(
            status_code=400,
            detail="Invalid trip ID"
        )

    trip = trips_collection.find_one({
        "_id": ObjectId(trip_id)
    })

    if not trip:
        raise HTTPException(
            status_code=404,
            detail="Trip not found"
        )

    if expense.paid_by not in trip["members"]:
        raise HTTPException(
            status_code=400,
            detail="Payer must be a member of the trip"
        )

    if not all(member in trip["members"] for member in expense.shared_by):
        raise HTTPException(
            status_code=400,
            detail="All shared members must belong to the trip"
        )

    expense_data = expense.model_dump()

    expense_data["trip_id"] = trip_id

    expense_data["date"] = expense.date.isoformat()

    share = expense.amount / len(expense.shared_by)

    expense_data["share_per_person"] = share

    result = expenses_collection.insert_one(expense_data)

    return {
        "message": "Expense created successfully",
        "expense_id": str(result.inserted_id),
        "share_per_person": share
    }
@app.get("/trips/{trip_id}/expenses")
def get_expenses(
    trip_id: str,
    category: str | None = None,
    paid_by: str | None = None,
    date: str | None = None,
    min_amount: float | None = None,
    max_amount: float | None = None,
    sort_by: str | None = None,
    order: str = "asc"
):

    if not ObjectId.is_valid(trip_id):
        raise HTTPException(
            status_code=400,
            detail="Invalid trip ID"
        )

    trip = trips_collection.find_one(
        {"_id": ObjectId(trip_id)}
    )

    if not trip:
        raise HTTPException(
            status_code=404,
            detail="Trip not found"
        )

    # Start with the trip ID
    query = {"trip_id": trip_id}

    # Filters
    if category:
        query["category"] = category

    if paid_by:
        query["paid_by"] = paid_by

    if date:
        query["date"] = date

    if min_amount is not None:
        query["amount"] = {"$gte": min_amount}

    if max_amount is not None:
        if "amount" in query:
            query["amount"]["$lte"] = max_amount
        else:
            query["amount"] = {"$lte": max_amount}

    # Sorting
    sort_field = None

    if sort_by == "amount":
        sort_field = "amount"

    elif sort_by == "date":
        sort_field = "date"

    if sort_field:
        sort_order = 1 if order == "asc" else -1
        expenses = list(
            expenses_collection.find(query).sort(
                sort_field,
                sort_order
            )
        )
    else:
        expenses = list(
            expenses_collection.find(query)
        )

    for expense in expenses:
        expense["_id"] = str(expense["_id"])

    return expenses

@app.get("/expenses/{expense_id}")
def get_expense(expense_id: str):
    if not ObjectId.is_valid(expense_id):
        raise HTTPException(
            status_code=400,
            detail="Invalid expense ID"
        )
    expense = expenses_collection.find_one({
        "_id" : ObjectId(expense_id)
    })
    if not expense:
        raise HTTPException(
            status_code=404,
            detail="Expense not found"
        )
    expense["_id"] = str(expense["_id"])

    return expense
@app.put("/expenses/{expense_id}")
def update_expense(expense_id: str, expense: ExpenseCreate):

    if not ObjectId.is_valid(expense_id):
        raise HTTPException(status_code=400, detail="Invalid expense ID")

    existing_expense = expenses_collection.find_one(
        {"_id": ObjectId(expense_id)}
    )

    if not existing_expense:
        raise HTTPException(status_code=404, detail="Expense not found")

    trip = trips_collection.find_one(
        {"_id": ObjectId(existing_expense["trip_id"])}
    )

    if not trip:
        raise HTTPException(status_code=404, detail="Trip not found")

    if expense.paid_by not in trip["members"]:
        raise HTTPException(
            status_code=400,
            detail="Payer must be a member of the trip"
        )

    if not all(member in trip["members"] for member in expense.shared_by):
        raise HTTPException(
            status_code=400,
            detail="All shared members must belong to the trip"
        )

    expense_data = expense.model_dump()

    # Convert Python date to string for MongoDB
    expense_data["date"] = expense.date.isoformat()

    # Keep the original trip ID
    expense_data["trip_id"] = existing_expense["trip_id"]

    # Calculate new share
    share = expense.amount / len(expense.shared_by)

    expense_data["share_per_person"] = share

    expenses_collection.update_one(
        {"_id": ObjectId(expense_id)},
        {"$set": expense_data}
    )

    return {
        "message": "Expense updated successfully",
        "expense_id": expense_id,
        "share_per_person": share
    }

@app.delete("/expenses/{expense_id}")
def delete_expense(expense_id: str):

    if not ObjectId.is_valid(expense_id):
        raise HTTPException(
            status_code=400,
            detail="Invalid expense ID"
        )
    result = expenses_collection.delete_one(
        {"_id": ObjectId(expense_id)}
    )

    if result.deleted_count == 0:
        raise HTTPException(
            status_code=404,detail="Expense not Found"
        )
    return{
        "message": "Expense deleted successfully",
        "expense_id": expense_id
    }
@app.get("/trips/{trip_id}/summary")
def get_trip_summary(trip_id: str):
    if not ObjectId.is_valid(trip_id):
        raise HTTPException(
            status_code=400,
            detail="Invalid trip ID"
        )

    trip = trips_collection.find_one(
        {"_id":ObjectId(trip_id)}
    )

    if not trip:
        raise HTTPException(
            status_code=404,
            detail="Trip not found"
        )
    expenses = list(
        expenses_collection.find(
            {"trip_id":trip_id}
        )
    )

    total_result = list(
        expenses_collection.aggregate([
            {"$match": {"trip_id": trip_id}},
            {"$group":{"_id":None, "total":{"$sum": "$amount"}}}
        ])
    )
    total_expenses = total_result[0]["total"] if total_result else 0

    paid = {}
    share = {}

    for member in trip["members"]:
        paid[member] = 0
        share[member] = 0

    for expense in expenses:
        payer = expense["paid_by"]
        paid[payer] += expense["amount"]

        shared_members = expense["shared_by"]
        individual_share = expense["amount"] / len(shared_members)

        for member in shared_members:
            share[member] += individual_share
    balances ={}

    for member in trip["members"]:
        balance = paid[member] - share[member]

        if balance > 0:
            status = "receive"
        elif balance < 0:
            status = "owe"
        else:
            status = "settled"
        balances[member] = {
            "paid" : round(paid[member], 2),
            "share" : round(share[member], 2),
            "balance" : round(balance, 2),
            "status" : status
        }
    return {
        "trip_id": trip_id,
        "trip_name": trip["name"],
        "total_expenses": round(total_expenses, 2),
        "members": balances
    }