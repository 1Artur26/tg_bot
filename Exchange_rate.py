from telegram.ext import filters
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ApplicationBuilder, CallbackContext, CommandHandler, Updater, MessageHandler, ConversationHandler
import requests
import main



async def exchange_rate_menu(update: Update, context: CallbackContext) -> None:
    custom_keyboard = [
        [InlineKeyboardButton('Exchange rate 💰', callback_data="ex_exchange_rate")],
        [InlineKeyboardButton('Cryptocurrency course 📈', callback_data="ex_cryptocurrency_course")],
        [InlineKeyboardButton('Return to the main menu 🏠', callback_data="ex_return_to_the_main_menu")]
    ]
    reply_markup = InlineKeyboardMarkup(custom_keyboard)
    
    await update.callback_query.message.reply_text(
        f"Оберіть функцію з меню:", 
        reply_markup=reply_markup
    )  

async def ex_main_menu(update: Update, context: CallbackContext) -> None:
    custom_keyboard = [
        [InlineKeyboardButton('Income and Expenses 💵', callback_data="mn_income_and_expenses")],
        [InlineKeyboardButton('Weather 🌤', callback_data="mn_weather")],
        [InlineKeyboardButton('Exchange rate 🏦', callback_data="mn_exchange_rate")],
        [InlineKeyboardButton('To-do list 🗒', callback_data="mn_to_do_list")],
        [InlineKeyboardButton('News 🌍', callback_data="mn_news")]
    ]
    reply_markup = InlineKeyboardMarkup(custom_keyboard)
    await update.callback_query.message.reply_text("Виберіть опцію з меню:", reply_markup=reply_markup)

async def exchange_rate_func(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query_data = query.data
    
    if query_data == "ex_exchange_rate":
        await exchange(update, context)
    elif query_data == "ex_cryptocurrency_course":
        await crypto(update, context)
    elif query_data == "ex_return_to_the_main_menu":
        await ex_main_menu(update, context)

    


async def crypto(update: Update, context: CallbackContext):
    top_crypto_data = get_top_crypto_data()

    for coin in top_crypto_data:
        await update.callback_query.message.reply_text(f"Name: {coin['name']}, Current Price: {coin['current_price']} USD")



def get_top_crypto_data():
    url = "https://api.coingecko.com/api/v3/coins/markets"
    
    params = {
        "vs_currency": "usd",  # Змінити валюту, якщо потрібно
        "order": "market_cap_desc",
        "per_page": 10,
        "page": 1,
    }
    
    response = requests.get(url, params=params)
    data = response.json()
    
    crypto_data = []
    for coin in data:
        name = coin["name"]
        current_price = coin["current_price"]
        crypto_data.append({"name": name, "current_price": current_price})
    
    return crypto_data


async def exchange(update: Update, context: CallbackContext):
    url = "http://api.exchangeratesapi.io/latest"
    API_KEY = "ee396e7f51558d4328d4bbd17bbe8852"
    popular_currencies = ["USD", "EUR", "GBP", "CAD", "AUD", "JPY", "CNY", "CHF", "RUB", "MXN"]
    
    params = {
        "base": "EUR",  # Змінити валюту, якщо потрібно
        "symbols": ",".join(popular_currencies),
        "access_key": API_KEY,
    }
    
    response = requests.get(url, params=params)
    data = response.json()
    
    rates = data["rates"]
    messages = []
    
    for currency in popular_currencies:
        exchange_rate = rates.get(currency)
        messages.append(f"{currency} - {exchange_rate:.2f} EUR")
    
    for message in messages:
        await update.callback_query.message.reply_text(message)
