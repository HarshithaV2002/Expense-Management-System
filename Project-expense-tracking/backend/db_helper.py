import mysql.connector
from contextlib import contextmanager
from logging_setup import setup_logger


logger = setup_logger('db_helper')

@contextmanager
def db_connection(commit=False):
    connection = mysql.connector.connect(
        host = "localhost",
        user = "root",
        password = "root123",
        database = "expense_manager"
    )
    cursor = connection.cursor(dictionary=True)

    yield cursor
    if commit:
        connection.commit()

    cursor.close()
    connection.close()

def fetch_all_expense(exp_date):
    logger.info(f"fetch_all_expense called with {exp_date}")
    with db_connection() as cursor:
        cursor.execute("Select * From expenses Where expense_date = %s",(exp_date,))
        expenses = cursor.fetchall()
        return expenses

def insert_expense(exp_date,amount,category,notes):
    logger.info(f"insert_expense called with expense_date:{exp_date},amount:{amount},category:{category},notes:{notes}")
    with db_connection(commit=True) as cursor:
        cursor.execute("Insert into expenses(expense_date,amount,category,notes) values(%s,%s,%s,%s)",(exp_date,amount,category,notes))


def update_for_date_expense(num,exp_date,amount,category,notes):
    logger.info(f"update_for_date_expense called with expense_date:{exp_date}")
    with db_connection(commit=True) as cursor:
        cursor.execute("Update expenses set amount = %s, category = %s, notes = %s where id = %s and expense_date = %s" , (amount,category,notes,num,exp_date,))

def delete_for_date_expense(exp_date):
    logger.info(f"delete_for_date_expense called with {exp_date}")
    with db_connection(commit=True) as cursor:
        cursor.execute("Delete from expenses where expense_date = %s ",(exp_date,))



def delete_individual_expense(num):
    with db_connection(commit=True) as cursor:
        logger.info(f"delete_individual_expense called with expense_id:{num}")
        cursor.execute("Delete from expenses where id = %s" , (num,))


def expense_summary(start_date , end_date):
    with db_connection() as cursor:
        logger.info(f"expense_summary from start_date:{start_date} and end_date:{end_date}")
        cursor.execute(
            "Select category , sum(amount) as total  "
            "From expenses Where expense_date "
            "between %s and %s group by category ",(start_date,end_date,)
        )
        data = cursor.fetchall()
        return data

def monthly_summary():
    with db_connection() as cursor:
        logger.info(f"monthly_summary ")
        cursor.execute("Select  MONTHNAME(expense_date) AS Month,SUM(amount) AS Total "
                       "FROM expenses GROUP BY  MONTHNAME(expense_date) ORDER BY  month")

        data = cursor.fetchall()
        # result = [{"month": row[0], "total": row[1]} for row in data]
        return data



if __name__ == "__main__":
    print(monthly_summary())
    # update_for_date_expense("79","2024-08-28","200","Food","Ate DBC ice cream")


    # delete_individual_expense(66)



#     insert_expense("2025-08-02","30","food","samosa")
#     print(fetch_all_expense("2025-08-02"))
#     delete_expense("2025-08-02")
#     print(fetch_all_expense("2025-08-02"))
