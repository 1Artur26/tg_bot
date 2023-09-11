from telegram.ext import  CallbackContext, ApplicationBuilder, CommandHandler
from telegram import Update
from datetime import datetime, timedelta
import main

user_data = dict()

class Task:
    def __init__(self, title: str, deadline: datetime = None) :
        self.title = title
        self.deadline = deadline
        self.completed = False
    
    def __str__(self):
        completed = "✅" if self.completed else "☑️"
        if self.deadline:
            return f"{completed} {self.title} | {self.deadline.strftime('%Y-%m-%d %H:%M:%S')}"
        return f"{completed} {self.title}"
    
async def todo_list_menu(update: Update, context: CallbackContext) -> None:
    await update.callback_query.message.reply_text(
        f"Hello, I'm your To Do list\n"
        "With me you can:\n"
        "Adding tasks: /add <task>\n"
        "Get tasks list: /list\n"
        "Remove tasks: /remove <task number>\n"
        "Clear tasks list : /clear \n"
        "Completed task: /comleted <task number>\n"
        "Chek Deadlines: /deadlines \n"
    )



async def add_task(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    task_parts = " ".join(context.args).split("|")
    task_title = task_parts[0].strip()
    deadline = None

    if len(task_parts) > 1:
        try:
            deadline = datetime.strptime(task_parts[1].strip(), '%Y-%m-%d %H:%M:%S')
        except ValueError:
            main.logging.error("Invalid deadline format")
            await update.message.reply_text("Your deadline argument is invalid")    
            return
        
    if not user_data.get(user_id):
        user_data[user_id] = []
    
    task = Task(task_title, deadline)
    user_data[user_id].append(task)
    await update.message.reply_text(f"Task: {task} was successfully added!")

async def list_task(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id

    if not user_data.get(user_id):
        await update.message.reply_text("You dont have any tasks")
        return 
    result = "\n".join([f"{i + 1}. {t}" for i, t in enumerate(user_data[user_id])])
    await update.message.reply_text(result)


async def remove_task(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id

    if not user_data.get(user_id):
        await update.message.reply_text("You dont have any tasks to remove")
        return 
    
    try:
        removed_idx = int(context.args[0]) - 1
        task = user_data[user_id].pop(removed_idx)
        await update.message.reply_text(f"Task: {task} successfully removed")
    except (ValueError, ImportError):
        await update.message.reply_text("You entered invalid index")

    
async def clear(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    user_data[user_id] = []
    await update.message.reply_text("Cleared successfully")
        

async def mark_completed(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id

    if not user_data.get(user_id):
        await update.message.reply_text("You dont have any tasks to completed")
        return 
    
    try:
        completed_idx = int(context.args[0]) - 1
        task = user_data[user_id][completed_idx]
        task.completed = True
        await update.message.reply_text(f"Task: {task} successfully completed")
    except (ValueError, ImportError):
        await update.message.reply_text("You entered invalid index")


async def get_dedlines(update: Update, contex: CallbackContext) -> None:
    user_id = update.message.from_user.id

    if not user_data.get(user_id):
        await update.message.reply_text("You dont have any task")
        return 
    
    now = datetime.now
    upcoming_deadlines = []
    for task in user_data[user_id]:
        if task.deadline and task.deadline <= (now - timedelta(days=1)):
            upcoming_deadlines.append(task)
    
    if upcoming_deadlines:
        await update.message.reply_text(
            'Upcoming task:'
            f"\n{' '.join(upcoming_deadlines)}"
        )
        return
    await update.message.reply_text("You dont have any deadlines")
    