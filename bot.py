
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from sqlalchemy.orm import sessionmaker
from app import Session, User, ReferredUser

TOKEN = '7173391462:AAFHjNM_fpIglqtM6MnE_erCl3HvfdBHz00'
WEB_APP_URL = 'https://e720-88-237-65-36.ngrok-free.app'

session = Session()

REFERRAL_REWARD = 10
DAILY_PERCENTAGE = 0.1

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    username = update.message.from_user.username
    args = context.args
    
    if username is None:
        await update.message.reply_text('You must have a username to use this bot.')
        return
    
    ref_id = None
    if args and args[0].startswith("id"):
        try:
            ref_id = int(args[0].split('id')[1])
        except (IndexError, ValueError):
            ref_id = None
    
    user = session.query(User).filter_by(id=user_id).first()
    if not user:
        user = User(id=user_id, username=username, referral_link=f'https://t.me/PhonexCoinbot?start=id{user_id}')
        session.add(user)
        session.commit()
        
        if ref_id:
            referrer = session.query(User).filter_by(id=ref_id).first()
            if referrer and referrer.id != user.id:
                referrer.referred_count += 1
                referrer.coins += REFERRAL_REWARD
                user.coins += REFERRAL_REWARD
                referred_user = ReferredUser(username=username, referrer_id=referrer.id, coins=user.coins)
                session.add(referred_user)
                session.commit()

    url = f'{WEB_APP_URL}?user_id={user.id}&username={user.username}'
    keyboard = [
        [InlineKeyboardButton("Open Web App", web_app=WebAppInfo(url=url))]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('Click the button below to open the web app:', reply_markup=reply_markup)

async def distribute_daily_income():
    users = session.query(User).all()
    for user in users:
        referred_users = session.query(ReferredUser).filter_by(referrer_id=user.id).all()
        daily_income = 0
        for referred_user in referred_users:
            contribution = referred_user.coins * DAILY_PERCENTAGE
            user.coins += contribution
            user.total_contributed_to_referrer += contribution
            daily_income += contribution
        session.commit()
    print("Daily income distributed to referrers.")

if __name__ == '__main__':
    application = ApplicationBuilder().token(TOKEN).build()
    application.add_handler(CommandHandler('start', start))

    application.run_polling()
