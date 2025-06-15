from telegram import Update
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler,
    ContextTypes, filters
)
import json, os

# === CONFIGURATION ===
TOKEN = "7848662149:AAHJN54IL2xbbqc2qJLTSZf36TVUI4EHVGU"
OWNER_USERNAME = "muhammadsaadlmk"
GROUP_USERNAME = "@ytgrowthgroup"
DATA_FILE = "user_links.json"
ADMIN_UNLOCKED_USERS = set()

# === LOAD USER DATA ===
if os.path.exists(DATA_FILE):
    with open(DATA_FILE, "r") as f:
        user_links = json.load(f)
else:
    user_links = {}

def save_links():
    with open(DATA_FILE, "w") as f:
        json.dump(user_links, f)

user_states = {}

# === USER SIDE ===
TRUSTED_LINKS = """
🤗 Welcome to YT Growth Group Bot by Muhammad Saad.
Subscribe to these channels first:
1. https://www.youtube.com/@MSPrimeTechServices
2. https://www.youtube.com/@makkahtv.blogspot9062
3. https://www.youtube.com/@MarbRush

📢 Then join our group: [Join Group](https://t.me/ytgrowthgroup)

After joining, use /checkjoin to continue.
"""

USER_COMMANDS = """
🔧 User Commands:
/howtouse – Show guide
/checkjoin – Verify group join
/continue – Start submission
/addlink – Add links (max 5)
/mylist – View your links
/editlink – Show link list
/replace index newlink – Replace one link
/delete index – Delete a link

✏️ *Detailed Guide:*
📋 *How to Use the Bot:*

1️⃣ */start* – Start the bot.
2️⃣ Subscribe to all 3 YouTube channels shown in the first message.
3️⃣ Join the group shown in the first message to get full access of the service *Free of Cost*.
4️⃣ Use */checkjoin* to confirm you've joined the group.
5️⃣ Type */continue* to begin submitting your links.
6️⃣ Bot will ask: "How many links (max 5)?" ➡️ Type a number. For example you have 1 youtube video link, then type 1.
7️⃣ Then send links using:  */addlink link1 link2 ...* (same number as selected, Put a space between links if you select index number greater then 1, for example if you have add index number 2 then: */addlink https://youtube.com/watch?v=abc123 https://youtube.com/watch?v=xyz456*)
✏️ *To View your links:* - Type */mylist* List will be sent to you with index number 1,2,3...
✏️ *To Edit:* Type */editlink* – This will show your links with index numbers 1,2,3,...
✏️ *To Replace a Link:* Type */replace index new_link* – Replace a specific link by index number, For example you want to change link at index number 2 so you need to type */replace 2 https://www.youtube.com/watch?v=abcdefghijk*.
✏️ *To Delete a Link:* Type */delete index* – Delete a specific link by index number, For example you want to delete link at index number 2 so you need to type */delete 2*.
-> *For Detailed Youtube Video Guide*: [Click Here to Watch the Video](https://msprimetechservicespk.blogspot.com/p/how-to-use-ms-yt-group-bot-and-get.html)
"""

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(TRUSTED_LINKS, parse_mode="Markdown")
    await update.message.reply_text(USER_COMMANDS, parse_mode="Markdown")

async def howtouse(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(USER_COMMANDS, parse_mode="Markdown")

async def check_join(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    try:
        member = await context.bot.get_chat_member(GROUP_USERNAME, user.id)
        if member.status in ["member", "administrator", "creator"]:
            await update.message.reply_text("✅ You have joined the group. Use /continue.")
        else:
            await update.message.reply_text("❌ Please subscribe and join the group first.")
    except:
        await update.message.reply_text("❌ Bot must be admin in a public group.")

async def continue_process(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    user_states[user_id] = {"step": "awaiting_count"}
    await update.message.reply_text("📌 How many YouTube links (max 5)? Send a number.")

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    state = user_states.get(user_id)
    if state and state["step"] == "awaiting_count":
        try:
            count = int(update.message.text)
            if 1 <= count <= 5:
                state["count"] = count
                state["step"] = "awaiting_links"
                await update.message.reply_text("✅ Now send your links using:\n/addlink link1 link2 ...")
            else:
                await update.message.reply_text("⚠ Enter a number between 1 and 5.")
        except:
            await update.message.reply_text("❌ Please enter a valid number.")

async def addlink(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    username = update.effective_user.username or "NoUsername"
    state = user_states.get(user_id)

    if not state or state.get("step") != "awaiting_links":
        return await update.message.reply_text("❗ Please use /continue first.")

    links = context.args
    if len(links) != state["count"]:
        return await update.message.reply_text(f"❌ Please submit exactly {state['count']} links.")

    user_links[user_id] = {"username": username, "links": links}
    save_links()
    user_states[user_id]["step"] = "done"
    await update.message.reply_text("✅ Your links have been saved.")

async def mylist(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    data = user_links.get(user_id)
    if not data:
        return await update.message.reply_text("ℹ You have not submitted any links.")
    text = "\n".join([f"{i+1}. {link}" for i, link in enumerate(data["links"])])
    await update.message.reply_text(f"👤 @{data['username']}:\n{text}")

async def editlink(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await mylist(update, context)

async def replace(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        user_id = str(update.effective_user.id)
        data = user_links[user_id]
        index = int(context.args[0]) - 1
        new_link = context.args[1]
        data["links"][index] = new_link
        save_links()
        await update.message.reply_text("✅ Link replaced.")
    except:
        await update.message.reply_text("❌ Usage: /replace index new_link")

async def delete(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        user_id = str(update.effective_user.id)
        index = int(context.args[0]) - 1
        removed = user_links[user_id]["links"].pop(index)
        save_links()
        await update.message.reply_text(f"🗑 Deleted: {removed}")
    except:
        await update.message.reply_text("❌ Usage: /delete index")

# === ADMIN PANEL ===
async def mslmk(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.username == OWNER_USERNAME:
        ADMIN_UNLOCKED_USERS.add(update.effective_user.id)
        await update.message.reply_text("""
🛠 Admin Commands:
/adminlist  
/viewuser <index>   
/deleteuserlink <user_index> <link_index>
/deleteuser <user_index>  
/edituserlink <user_index> <link_index> <new_link>  
/send<index>  
/senduser<index>  
/addusrlink <user_index> <new_link>  
/adduserlinks <user_index> <link1> <link2> ...  /lockadmin
""")
    else:
        await update.message.reply_text("⛔ Access denied.")

def is_admin(user):
    return user.id in ADMIN_UNLOCKED_USERS

async def adminlist(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update.effective_user): return
    text = "\n".join([f"{i+1}. @{d['username']}" for i, d in enumerate(user_links.values())])
    await update.message.reply_text(text or "❌ No users yet.")

async def viewuser(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update.effective_user): return
    try:
        index = int(context.args[0]) - 1
        uid = list(user_links.keys())[index]
        data = user_links[uid]
        links = "\n".join([f"{i+1}. {l}" for i, l in enumerate(data["links"])])
        await update.message.reply_text(f"👤 @{data['username']}:\n{links}")
    except:
        await update.message.reply_text("❌ Usage: /viewuser <index>")

async def deleteuserlink(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update.effective_user): return
    try:
        uindex = int(context.args[0]) - 1
        lindex = int(context.args[1]) - 1
        uid = list(user_links.keys())[uindex]
        removed = user_links[uid]["links"].pop(lindex)
        save_links()
        await update.message.reply_text(f"🗑 Removed: {removed}")
    except:
        await update.message.reply_text("❌ Usage: /deleteuserlink <user_index> <link_index>")

async def deleteuser(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update.effective_user): return
    try:
        index = int(context.args[0]) - 1
        uid = list(user_links.keys())[index]
        del user_links[uid]
        save_links()
        await update.message.reply_text("✅ User data deleted.")
    except:
        await update.message.reply_text("❌ Usage: /deleteuser <index>")

async def edituserlink(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update.effective_user): return
    try:
        uindex = int(context.args[0]) - 1
        lindex = int(context.args[1]) - 1
        new = context.args[2]
        uid = list(user_links.keys())[uindex]
        user_links[uid]["links"][lindex] = new
        save_links()
        await update.message.reply_text("✅ Link updated.")
    except:
        await update.message.reply_text("❌ Usage: /edituserlink <user_index> <link_index> <new_link>")

async def addusrlink(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update.effective_user): return
    try:
        uindex = int(context.args[0]) - 1
        newlink = context.args[1]
        uid = list(user_links.keys())[uindex]
        user_links[uid]["links"].append(newlink)
        save_links()
        await update.message.reply_text("✅ Link added to user.")
    except:
        await update.message.reply_text("❌ Usage: /addusrlink <user_index> <new_link>")

async def adduserlinks(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update.effective_user): 
        return await update.message.reply_text("⛔ Admin access required.")
    try:
        uindex = int(context.args[0]) - 1
        new_links = context.args[1:]
        uid = list(user_links.keys())[uindex]
        user_links[uid]["links"].extend(new_links)
        save_links()
        await update.message.reply_text(f"✅ Added {len(new_links)} links to user @{user_links[uid]['username']}.")
    except:
        await update.message.reply_text("❌ Usage: /adduserlinks <user_index> <link1> <link2> ...")

async def send_to_group(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update.effective_user): return
    try:
        index = int(update.message.text.replace("/send", "")) - 1
        uid = list(user_links.keys())[index]
        data = user_links[uid]
        text = f"📢 @{data['username']}:\n" + "\n".join([f"{i+1}. {l}" for i, l in enumerate(data["links"])])
        await context.bot.send_message(chat_id=GROUP_USERNAME, text=text)
        await update.message.reply_text("✅ Links sent to group!")
    except:
        await update.message.reply_text("❌ Invalid index.")

async def send_first_link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update.effective_user): return
    try:
        index = int(update.message.text.replace("/senduser", "")) - 1
        uid = list(user_links.keys())[index]
        data = user_links[uid]
        await context.bot.send_message(chat_id=GROUP_USERNAME, text=f"📢 @{data['username']}:\n{data['links'][0]}")
        await update.message.reply_text("✅ Link sent to group!")
    except:
        await update.message.reply_text("❌ Invalid index.")

async def lockadmin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    ADMIN_UNLOCKED_USERS.clear()
    await update.message.reply_text("🔒 Admin access locked.")

# === RUN BOT ===
app = ApplicationBuilder().token(TOKEN).build()

# User Commands
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("howtouse", howtouse))
app.add_handler(CommandHandler("checkjoin", check_join))
app.add_handler(CommandHandler("continue", continue_process))
app.add_handler(CommandHandler("addlink", addlink))
app.add_handler(CommandHandler("mylist", mylist))
app.add_handler(CommandHandler("editlink", editlink))
app.add_handler(CommandHandler("replace", replace))
app.add_handler(CommandHandler("delete", delete))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))

# Admin Commands
app.add_handler(CommandHandler("mslmk", mslmk))
app.add_handler(CommandHandler("adminlist", adminlist))
app.add_handler(CommandHandler("viewuser", viewuser))
app.add_handler(CommandHandler("deleteuserlink", deleteuserlink))
app.add_handler(CommandHandler("deleteuser", deleteuser))
app.add_handler(CommandHandler("edituserlink", edituserlink))
app.add_handler(CommandHandler("addusrlink", addusrlink))
app.add_handler(CommandHandler("adduserlinks", adduserlinks))
app.add_handler(CommandHandler("lockadmin", lockadmin))
app.add_handler(MessageHandler(filters.Regex(r"^/send\d+$"), send_to_group))
app.add_handler(MessageHandler(filters.Regex(r"^/senduser\d+$"), send_first_link))

app.run_polling()
