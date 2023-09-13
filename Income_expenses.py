from telegram.ext import  CallbackContext
from telegram import Update, KeyboardButton, ReplyKeyboardMarkup
from datetime import datetime
import main
import json
import os


def save_data(data, filename):
    with open(os.path.join(current_directory, filename), 'w') as file:
        json.dump(data, file)


def load_data(filename):
    try:
        with open(os.path.join(current_directory, filename), 'r') as file:
            data = json.load(file)
        return data
    except FileNotFoundError:
        
        return {}

CATEGORY = ['Food', 'Sport','Hobby','Family','Home']

current_directory = os.path.dirname(os.path.abspath(__file__))

balance_file_path = os.path.join(current_directory, 'balance.txt')

balance = int(open(balance_file_path, 'r').read())
expenses_list = load_data('expenses.json')
incomes_list = load_data('incomes.json')


async def Income_expenses_menu(update: Update, context: CallbackContext) -> None:
    await update.callback_query.message.reply_text(
        f"Hello, I'm your incomes and expenses list\n"
        "With me you can:\n"
        "Adding expense: /add_expense <expense>\n"
        "Adding income: /add_income <income>\n"
        "Get expenses list: /expenses_list\n"
        "Get incomes list: /incomes_list\n"
        "Remove expense: /remove_expense <expense number>\n"
        "Remove income: /remove_income <income number>\n"
        "Clear expenses list : /clear_expenses \n"
        "Clear incomes list : /clear_incomes \n"
        "Get balance: /balance \n"
        "Get category: /get_category \n"
    )


class Income_Expense:
    def __init__(self, amount: str, category: str, time: datetime = None) :
        self.amount = amount
        self.category = category
        self.time = time
    
    def __str__(self):
        if self.time is not None:
            return f"{self.amount} грн | {self.category} | {self.time.strftime('%Y-%m-%d %H:%M:%S')}"
        return f"{self.amount} грн | {self.category}"
    
    def to_dict(self):
        return {
            "amount": self.amount,
            "category": self.category,
            "time": self.time.strftime('%Y-%m-%d %H:%M:%S') if self.time else None,
        }


async def get_balance(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text(f"Your balance: {balance} грн")    
    
async def add_expens(update: Update, context: CallbackContext) -> None:
    user_id = str(update.message.from_user.id)
    expens_parts = " ".join(context.args).split("|")
    amount = expens_parts[0].strip()
    category = expens_parts[1].strip()

    if category not in CATEGORY:
        await update.message.reply_text("Your category not in category list")   
        return

    if len(expens_parts) > 2:
        try:
            time = datetime.strptime(expens_parts[2].strip(), '%Y-%m-%d %H:%M:%S')
        except ValueError:
            main.logging.error("Invalid deadline format")
            await update.message.reply_text("Your deadline argument is invalid")    
            return
    else:
        time = datetime.now()    
    if not expenses_list.get(user_id):
        expenses_list[user_id] = []

    global balance
    balance -= int(amount)
    open(balance_file_path, 'w').write(str(balance))
    
    expens = Income_Expense(amount, category, time)
    expenses_list[user_id].append({category: expens.to_dict()})
    await update.message.reply_text(f"Expens: {expens} was successfully added!")
    save_data(expenses_list, 'expenses.json')


async def add_income(update: Update, context: CallbackContext) -> None:
    user_id = str(update.message.from_user.id)
    income_parts = " ".join(context.args).split("|")
    amount = income_parts[0].strip()
    category = income_parts[1].strip()


    if len(income_parts) > 2:
        try:
            time = datetime.strptime(income_parts[2].strip(), '%Y-%m-%d %H:%M:%S')
        except ValueError:
            main.logging.error("Invalid deadline format")
            await update.message.reply_text("Your deadline argument is invalid")    
            return
    else:
        time = datetime.now() 

    if not incomes_list.get(user_id):
        incomes_list[user_id] = []

    global balance
    balance += int(amount)
    open(balance_file_path, 'w').write(str(balance))

    income = Income_Expense(amount, category, time)
    incomes_list[user_id].append({category: income.to_dict()})
    await update.message.reply_text(f"Income: {income} was successfully added!")
    save_data(incomes_list, 'incomes.json')


async def get_category(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text('\n'.join(CATEGORY))

async def get_expenses(update: Update, context: CallbackContext) -> None:
    user_id = str(update.message.from_user.id)
    filters = " ".join(context.args).split("|")
    category_filter = filters[0].strip()
    if len(filters) >= 3:
        date_filter = filters[1].strip()

    if not expenses_list.get(user_id):
        await update.message.reply_text("You dont have any expenses")
        return
    
    user_expenses = expenses_list.get(user_id, [])

    if len(filters) == 1:
        # Виводимо всі витрати 
        expenses = [list(expense.values())[0] for expense in user_expenses]
        formatted_expenses = "\n".join([f"{i + 1}. {expense}" for i, expense in enumerate(expenses)])
        await update.message.reply_text(formatted_expenses)
        return
    
    elif len(filters) == 2:
        # Виводимо витрати по категорії 
        filtered_expenses = [expense for expense in user_expenses if list(expense.keys())[0] == category_filter]
        if filtered_expenses:
            formatted_filtered_expenses = "\n".join([f"{i + 1}. {list(expense.values())[0]}" for i, expense in enumerate(filtered_expenses)])
            await update.message.reply_text(formatted_filtered_expenses)
        else:
            await update.message.reply_text(f"No expenses found for category: {category_filter}")
        return

    elif len(filters) == 3:
        # Виводимо витрати по категорії і даті
        formatted_filtered_expenses = []
        for i, expense in enumerate(user_expenses):
            expense_category = list(expense.keys())[0]
            expense_date = list(expense.values())[0]['time']
            expense_data = list(expense.values())[0]
            if expense_category == category_filter and datetime.strptime(expense_date, '%Y-%m-%d %H:%M:%S') >= datetime.strptime(date_filter, '%Y-%m-%d %H:%M:%S'):
                formatted_filtered_expenses.append(f"{i + 1}. Category: {expense_data['category']}, Amount: {expense_data['amount']}, Time: {expense_data['time']}")

        if formatted_filtered_expenses:
            await update.message.reply_text("\n".join(formatted_filtered_expenses))
        else:
            await update.message.reply_text(f"No expenses found for category: {category_filter} after {date_filter}")
        return
    

async def get_incomes(update: Update, context: CallbackContext) -> None:
    user_id = str(update.message.from_user.id)
    filters = " ".join(context.args).split("|")
    category_filter = filters[0].strip()
    if len(filters) >= 3:
        date_filter = filters[1].strip()

    if not incomes_list.get(user_id):
        await update.message.reply_text("You dont have any incomes")
        return
    
    user_incomes = incomes_list.get(user_id, [])

    if len(filters) == 1:
        # Виводимо всі доходи
        incomes = [list(income.values())[0] for income in user_incomes]
        formatted_incomes = "\n".join([f"{i + 1}. {income}" for i, income in enumerate(incomes)])
        await update.message.reply_text(formatted_incomes)
        return
    
    elif len(filters) == 2:
        # Виводимо доходи по категорії
        filtered_incomes = [income for income in user_incomes if list(income.keys())[0] == category_filter]
        if filtered_incomes:
            formatted_filtered_incomes = "\n".join([f"{i + 1}. {list(income.values())[0]}" for i, income in enumerate(filtered_incomes)])
            await update.message.reply_text(formatted_filtered_incomes)
        else:
            await update.message.reply_text(f"No incomes found for category: {category_filter}")
        return

    elif len(filters) == 3:
        # Виводимо доходи по категорії і даті
        formatted_filtered_incomes = []
        for i, income in enumerate(user_incomes):
            income_category = list(income.keys())[0]
            income_date = list(income.values())[0]['time']
            expense_data = list(income.values())[0]
            if income_category == category_filter and datetime.strptime(income_date, '%Y-%m-%d %H:%M:%S') >= datetime.strptime(date_filter, '%Y-%m-%d %H:%M:%S'):
                formatted_filtered_incomes.append(f"{i + 1}. Category: {expense_data['category']}, Amount: {expense_data['amount']}, Time: {expense_data['time']}")

        if formatted_filtered_incomes:
            await update.message.reply_text("\n".join(formatted_filtered_incomes))
        else:
            await update.message.reply_text(f"No incomes found for category: {category_filter} after {date_filter}")
        return

async def remove_expense(update: Update, context: CallbackContext) -> None:
    user_id = str(update.message.from_user.id)
    try:
        expense_number = int(context.args[0]) - 1
    except (ValueError, IndexError):
        await update.message.reply_text("Please provide a valid expense number to remove.")
        return

    user_expenses = expenses_list.get(user_id, [])

    if len(user_expenses) <= expense_number:
        await update.message.reply_text("Expense number not found.")
        return

    # Видаляємо витрату
    removed_expense = user_expenses.pop(expense_number)
    category = list(removed_expense.keys())[0]
    amount = removed_expense[category]["amount"]

    global balance
    balance += int(amount)

    open(balance_file_path, 'w').write(str(balance))

    await update.message.reply_text(f"Expense {expense_number + 1} has been removed. Your balance has been updated.")

    save_data(expenses_list, 'expenses.json')


async def remove_income(update: Update, context: CallbackContext) -> None:
    user_id = str(update.message.from_user.id)
    try:
        income_number = int(context.args[0]) - 1  
    except (ValueError, IndexError):
        await update.message.reply_text("Please provide a valid income number to remove.")
        return

    user_incomes = incomes_list.get(user_id, [])

    if len(user_incomes) <= income_number:
        await update.message.reply_text("Income number not found.")
        return

    # Видаляємо дохід
    removed_income = user_incomes.pop(income_number)
    category = list(removed_income.keys())[0]
    amount = removed_income[category]["amount"]

    global balance
    balance -= int(amount)

    open(balance_file_path, 'w').write(str(balance))

    await update.message.reply_text(f"Income {income_number + 1} has been removed. Your balance has been updated.")

    save_data(incomes_list, 'incomes.json')

async def clear_expenses(update: Update, context: CallbackContext) -> None:
    user_id = str(update.message.from_user.id)
    if user_id in expenses_list:
        expenses_list[user_id] = {}
        await update.message.reply_text("Your expenses list has been cleared.")
        save_data(expenses_list, 'expenses.json')
    else:
        await update.message.reply_text("You don't have any expenses to clear.")

async def clear_incomes(update: Update, context: CallbackContext) -> None:
    user_id = str(update.message.from_user.id)
    if user_id in incomes_list:
        incomes_list[user_id] = {}  # Очищаємо список доходів для користувача
        await update.message.reply_text("Your incomes list has been cleared.")
        save_data(incomes_list, 'income.json')
    else:
        await update.message.reply_text("You don't have any incomes to clear.")