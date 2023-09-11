from telegram.ext import  CallbackContext
from telegram import Update, KeyboardButton, ReplyKeyboardMarkup
import requests



async def news_list(update: Update, context: CallbackContext) -> None:
    
    top_stories = get_gnews_top_stories()

    for story in top_stories:
        title = story.get("title", "No title")
        description = story.get("description", "No description")
        url = story.get("url", "No URL")
        await update.callback_query.message.reply_text(f" *{title}*\n{description}\n Read more: {url}", parse_mode='Markdown')
    
API_KEY = "6516b6188b4e17757f813a35c371ad50"

def get_gnews_top_stories():
    url = "https://gnews.io/api/v4/top-headlines"
    
    params = {
        "token": API_KEY,
        "lang": "en",  
        "max": 3,  
    }
    
    response = requests.get(url, params=params)
    data = response.json()
    
    if "articles" in data:
        top_stories = data["articles"]
        return top_stories
    else:
        return []
