import logging

from telegram import Update, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CallbackContext, CommandHandler, CallbackQueryHandler
import Exchange_rate
import Income_expenses
import News
import Todo_list
import Weather
TOKEN_BOT = '6390673168:AAHU0tXxTy7QsSMcPZSaFeqi1o9iDIwi1yQ'

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


async def start(update: Update, context: CallbackContext) -> None:
    logging.info("User pressed the Start button")
    user_name = update.message.from_user.first_name
    custom_keyboard = [
        [InlineKeyboardButton('Income and Expenses 💵', callback_data="mn_income_and_expenses")],
        [InlineKeyboardButton('Weather 🌤', callback_data="mn_weather")],
        [InlineKeyboardButton('Exchange rate 🏦', callback_data="mn_exchange_rate")],
        [InlineKeyboardButton('To-do list 🗒', callback_data="mn_to_do_list")],
        [InlineKeyboardButton('News 🌍', callback_data="mn_news")]
    ]
    reply_markup = InlineKeyboardMarkup(custom_keyboard)
    await update.message.reply_text(f"Вітаю, {user_name}! Виберіть опцію з меню:", reply_markup=reply_markup)




async def main_menu(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query_data = query.data
    
    if query_data == "mn_income_and_expenses":
        await Income_expenses.Income_expenses_menu(update, context)
    elif query_data == "mn_weather":
        await Weather.get_weather(update, context)
    elif query_data == "mn_exchange_rate":
        await Exchange_rate.exchange_rate_menu(update, context)
    elif query_data == "mn_to_do_list":
        await Todo_list.todo_list_menu(update, context)
    elif query_data == "mn_news":
        await News.news_list(update, context)



def run():
    app = ApplicationBuilder().token(TOKEN_BOT).build()

    app.add_handler(CommandHandler("start", start))
  
    app.add_handler(CallbackQueryHandler(main_menu, pattern='^mn_*'))

    app.add_handler(CallbackQueryHandler(Exchange_rate.exchange_rate_func, pattern='^ex_*'))

    app.add_handler(CommandHandler("help", Todo_list.todo_list_menu))
    app.add_handler(CommandHandler("add", Todo_list.add_task))
    app.add_handler(CommandHandler("list", Todo_list.list_task))
    app.add_handler(CommandHandler("remove", Todo_list.remove_task))
    app.add_handler(CommandHandler("clear", Todo_list.clear))
    app.add_handler(CommandHandler("deadlines", Todo_list.get_dedlines))
    app.add_handler(CommandHandler("comleted", Todo_list.mark_completed))

    app.add_handler(CommandHandler("help_list", Income_expenses.Income_expenses_menu))
    app.add_handler(CommandHandler("add_expense", Income_expenses.add_expens))
    app.add_handler(CommandHandler("add_income", Income_expenses.add_income))
    app.add_handler(CommandHandler("expenses_list", Income_expenses.get_expenses))
    app.add_handler(CommandHandler("incomes_list", Income_expenses.get_incomes))
    app.add_handler(CommandHandler("remove_expense", Income_expenses.remove_expense))
    app.add_handler(CommandHandler("remove_income", Income_expenses.remove_income))
    app.add_handler(CommandHandler("clear_expenses", Income_expenses.clear_expenses))
    app.add_handler(CommandHandler("clear_incomes", Income_expenses.clear_incomes))
    app.add_handler(CommandHandler("balance", Income_expenses.get_balance))
    app.add_handler(CommandHandler("get_category", Income_expenses.get_category))

    app.run_polling()

if __name__ == "__main__":
    run()
