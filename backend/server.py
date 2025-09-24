from fastapi import FastAPI , HTTPException
from datetime import date

from openpyxl.styles.builtins import percent

import db_helper
from typing import List
from pydantic import BaseModel
from typing import Optional



app = FastAPI()

class Expense(BaseModel):
    id : Optional[int] = None
    amount : float
    category : str
    notes : str
    expense_date : Optional[date] = None


class DateRange(BaseModel):
    start_date : date
    end_date : date




@app.get("/expense/{exp_date}",response_model=List[Expense])
def get_expenses(exp_date : date):
    expenses = db_helper.fetch_all_expense(exp_date)
    if expenses is None:
        raise HTTPException(status_code=500, detail="Failed to retrieve expenses from the database")
    return expenses


@app.post("/expense/{exp_date}")
def add_expenses(exp_date:date ,expenses:List[Expense]):
    for expense in expenses:
        db_helper.insert_expense(exp_date,expense.amount,expense.category,expense.notes)

    return {"message": "Expense added successfully "}


@app.post("/expense/{exp_date}/{exp_id}")
def update_expense(exp_date:date ,exp_id:int, expenses: Expense):
    # db_helper.delete_expense(exp_date)

    db_helper.update_for_date_expense(exp_id,exp_date,expenses.amount,expenses.category,expenses.notes)

    return {"message":"Expense Updated Successfully"}


@app.delete("/expense/{exp_date}")
def delete_expense(exp_date:date):
    db_helper.delete_for_date_expense(exp_date)
    return {"message":"All expenses deleted successfully"}

@app.delete("/expense/{exp_date}/{exp_id}")
def delete_for_id_expense(exp_date:date ,exp_id:int):
    db_helper.delete_individual_expense(exp_id)
    return {"message":"expense deleted successfully"}

@app.post("/analytics/")
def get_analytics(date_range: DateRange):
    data = db_helper.expense_summary(date_range.start_date , date_range.end_date)

    if data is None:
        raise HTTPException(status_code=500, detail="Failed to return expense summary from the database")

    total = sum([row['total'] for row in data])
    breakdown = {}
    for row in data:
        percentage = (row['total']/total)*100 if total != 0 else 0
        breakdown[row['category']] = {
            "total": row['total'],
            "percentage": percentage
        }
    return breakdown

@app.get("/analytics/")
def monthly_analytics():
    data = db_helper.monthly_summary()
    if data is None:
        raise HTTPException(status_code=500, detail="Failed to return monthly expense summary from the database")


    return data