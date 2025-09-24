from backend import db_helper

def test_fetch_all_expense_for_aug_15():
    expense = db_helper.fetch_all_expense("2024-08-15")

    assert len(expense)== 1
    assert expense[0]['amount'] == 10.0
    assert expense[0]['category'] == "Shopping"
    assert expense[0]['notes'] == "Bought potatoes"




def test_fetch_all_expense_for_invalid_date():
    expense = db_helper.fetch_all_expense("9999-08-15")

    assert len(expense)== 0

def test_expense_summary():
    summary = db_helper.expense_summary("2099-01-01","2099-12-31")
    assert len(summary) == 0