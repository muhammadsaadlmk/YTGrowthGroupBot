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

1⃣ */start* – Start the bot.
2⃣ Subscribe to all 3 YouTube channels shown in the first message.
3⃣ Join the group shown in the first message to get full access of the service *Free of Cost*.
4⃣ Use */checkjoin* to confirm you've joined the group.
5⃣ Type */continue* to begin submitting your links.
6⃣ Bot will ask: "How many links (max 5)?" ➡️ Type a number. For example you have 1 youtube video link, then type 1.
7⃣ Then send links using:  */addlink link1 link2 ...* (same number as selected, Put a space between links if you select index number greater then 1, for example if you have add index number 2 then: */addlink https://youtube.com/watch?v=abc123 https://youtube.com/watch?v=xyz456*)
✏️ *To View your links:* - Type */mylist* List will be sent to you with index number 1,2,3...
✏️ *To Edit:* Type */editlink* – This will show your links with index numbers 1,2,3,...
✏️ *To Replace a Link:* Type */replace index new_link* – Replace a specific link by index number, For example you want to change link at index number 2 so you need to type */replace 2 https://www.youtube.com/watch?v=abcdefghijk*.
✏️ *To Delete a Link:* Type */delete index* – Delete a specific link by index number, For example you want to delete link at index number 2 so you need to type */delete 2*.
-> *For Detailed Youtube Video Guide*: [Click Here to Watch the Video](https://msprimetechservicespk.blogspot.com/p/how-to-use-ms-yt-group-bot-and-get.html)
"""

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
app.add_handler(MessageHandler(filters.Regex(r"^/send\\d+$"), send_to_group))
app.add_handler(MessageHandler(filters.Regex(r"^/senduser\\d+$"), send_first_link))

app.run_polling()
