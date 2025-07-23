#config.py | kutubxonalar
import telebot
from telebot.types import *
from config import *
from datetime import datetime, timedelta
from telebot.types import Message , InlineKeyboardMarkup, InlineKeyboardButton , ChatPermissions
from telebot.types import Message
from telebot import types
from rapidfuzz import process, fuzz
import time
from database import *
import os
import requests
# kutubxonalar tugadi

# vaqtinchalik xotira
NEW_SERIAL = {}
CAPTION = {}
FILE_ID = {}
IMGBB_API_KEY = "de55c2e41077612eb0a371e95ac2b170"

# vaqtinchalik xotira tugadi



# Admin o'zgaruvchilari
ADMIN_ID = [5921733345,6325574205 ,1739407678, 6699875416,5760452570,6845147329]
# Admin o'zgaruvchilari tugadi

OWNER_ID = ADMIN_ID[0]

#token
token = "6459135662:AAG4h2rVTkeglOf77aEFWyvI0IbnpIIwcJQ"
bot = telebot.TeleBot(token,parse_mode='html')
#token tugadi

# shorts bo'limi



dub_text=f"""
<b>🛑 Qoidalarni o'qib chqing  🛑

1) Yoshi 16-17 dan oshgan bo'lishi kerak
2) Dublyaj qilish bo'yicha tushunchasi bo'lishi kerak
3) Shevada gapirmasligi kerak
4) Iloji boricha chet tilini bilishi kerak (shart emas)
5) Berilgan topshiriqni vaqtida bajarib o'z ishiga puxta yondashish kerak
6) Boshqa fan dublarda ishlamasligi shart</b>

<blockquote>Qoidalarga rozi bo'lsangiz tugmani bosing</blockquote>"""

dub2_text= f"""<b>
🖊 Endi esa Ismingiz yoshingiz va tajribangiz haqida adminga yozing
</b>
<blockquote>🚫 Muomilasi yoqlar spam bo'ladi</blockquote>"""

admin_text=f"""
👮🏻‍♀️ Adminlik turlari :

1) Kanalga edit va qiziqarli post tashlash,
2) Botga Film yuklash uchun ,
3) Gruhda saavollarga javob berish ,
4) Anime , Dorama , Kino topish uchun
5) Pymovie instgarmi uchun

<blockquote>Bu eng masulyatli ishlar</blockquote>"""

def private_chat_only(func):
  def wrapper(message: Message):
      if message.chat.type == 'private':
          return func(message)
      else:
          bot.reply_to(message, "🙁 Bu funksya faqat @pymovibot chatida ishlaydi\n<blockquote> Botni gruhda ishlatguncha miyyani ishlating 😢</blockquote>")
  return wrapper



# Buttonlar hammasi . . .

def adminga():
  key = InlineKeyboardMarkup()
  key.add(InlineKeyboardButton(text="Admin bo'lmoqchiman", url="t.me/pyfotuz"))
  return key

def dub_btn():
  btn = InlineKeyboardMarkup()
  btn.add(InlineKeyboardButton(text="📝 Yozish", url="http://t.me/pyfotuz?text=🍃Assalomualaykum%20men%20Dublyaj%20gruhga%20qoshilmoqchiman"))
  return btn


def group_btn():
  btn = InlineKeyboardMarkup(row_width=2)
  btn.add(InlineKeyboardButton(text="Pymovie Group", url="t.me/pymovie_group"))
  return btn

def main_btn():
    btn = InlineKeyboardMarkup()
    b1 = InlineKeyboardButton(text="🪼 Kanalimiz",url='t.me/pymoviee')
    b2 = InlineKeyboardButton(text="⌂ Home", callback_data='home')
    btn.row(b1,b2)
    return btn
# start buttonlar

def main_menu():
    btn = InlineKeyboardMarkup(row_width=2)
    b1 = InlineKeyboardButton(text="🧩 Web ilova",url='https://t.me/pymovibot?startapp')
    b2 = InlineKeyboardButton(text="🔍 Film qidirish", switch_inline_query_current_chat="")
    b3 = InlineKeyboardButton(text="📣 E'lonlar", callback_data='news')
    b4 = InlineKeyboardButton(text="ℹ️ Qo'llanma", web_app=types.WebAppInfo(url='https://pult.serv00.net/'))
    b5 = InlineKeyboardButton(text="»»»", callback_data='next_page')
    btn.add(b1, b2)
    btn.add(b3)
    btn.add(b4)
    return btn


# admin panel reply keyboard
def admin_panel():
  key = ReplyKeyboardMarkup(resize_keyboard=True,input_field_placeholder='Admin paneli')
  key.add(
    KeyboardButton("📺 Seriallar"),
    KeyboardButton("➕ Serial qo'shish"))
  key.add(
    KeyboardButton("✉ Oddiy xabar"),
    KeyboardButton("✉ Forward xabar"),
  )
  key.add(
      KeyboardButton("📊 Statistika"),
      KeyboardButton("📣 E'lonlar")
  )
  key.add(
      KeyboardButton("🎴 Kanallarni boshqarish")
  )
  return key

# Barcha buttonlar tugadi . . .

# group funksyasi for text
grmsg = """
 @pymovie_groupga<b> ɢᴀ ǫᴏ'sʜɪʟᴅɪɴɢɪᴢ ✅:

 ▫️ ɢᴜʀᴜʜɢᴀ ʜᴀʀ xɪʟ ʀᴇᴋʟᴀᴍᴀʟᴀʀ ʀᴇғᴇʀᴀʟ ʜᴀᴠᴏʟᴀʟᴀʀ ʏᴜʙᴏʀᴍᴀɴɢ !

 ▫️ ᴏʀᴛɪǫᴄʜᴀ ᴄʜᴀᴛ ǫɪʟᴍᴀɴɢ ғᴀǫᴀᴛ ᴋᴇʀᴀᴋʟɪ ʜᴀʙᴀʀ ʏᴏᴢɪɴɢ !

 ▫️ ʙɪʀ ʙɪʀɪɴɢɪᴢɴɪ ʜᴜʀᴍᴀᴛ ǫʟɪɴɢ !

📛 ʏᴜǫᴏʀɪᴅᴀɢɪ ǫᴏʏᴅᴀʟᴀʀᴅᴀɴ ʙɪʀɪɴɪ ʙᴜᴢsᴀɴɢɪᴢ ʙʟᴏᴋ ʏᴏᴋɪ ᴍᴜᴛᴇ ǫɪʟɪɴᴀsɪᴢ</b>
"""




def new_serial(msg):
    try:
        cid = msg.chat.id
        if msg.text == "Cancel":
            bot.reply_to(msg, "<b>Bekor qilindi!</b>", reply_markup=admin_panel(), parse_mode='HTML')
            return

        try:
            file_id = msg.photo[-1].file_id
            text = msg.caption.replace("'", "’") if msg.caption else "No name"
        except Exception as e:
            bot.reply_to(msg, "⚠️ Rasm yuborishingiz kerak!", parse_mode='HTML')
            return

        # 1. Telegramdan file_path olish
        get_file = bot.get_file(file_id)
        file_path = get_file.file_path

        # 2. Rasmni Telegramdan yuklab olish
        file_url = f"https://api.telegram.org/file/bot{bot.token}/{file_path}"
        local_filename = f"temp_{file_id}.jpg"
        with open(local_filename, 'wb') as f:
            f.write(requests.get(file_url).content)

        # 3. imgbb'ga yuklash
        with open(local_filename, 'rb') as img_file:
            upload = requests.post(
                "https://api.imgbb.com/1/upload",
                data={'key': IMGBB_API_KEY},
                files={'image': img_file}
            )

        data = upload.json()
        if not data.get('success'):
            raise Exception("imgbb yuklashda xatolik")

        photo_url = data['data']['url']
        os.remove(local_filename)  # vaqtincha faylni o‘chirish

        # 4. Ma'lumotlarni databasega yozish
        cursor.execute("INSERT INTO serial(name, file_id, photo_url) VALUES(?, ?, ?)", (text, file_id, photo_url))
        conn.commit()

        # 5. Adminga tasdiq yuborish
        bot.send_photo(cid, file_id, caption=f"<b>✅ Yangi serial qo‘shildi!</b>\n📎 URL: {photo_url}", reply_markup=admin_panel(), parse_mode='HTML')

    except Exception as e:
        print("Xatolik:", e)
        bot.reply_to(msg, f"⚠️ Xatolik yuz berdi:\n{e}", parse_mode='HTML')


# ------ Qidiruv funksyasi --------

def search_series(series_name=None):
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, photo_url FROM serial")
    all_series = cursor.fetchall()

    results = []

    if not series_name:  # Agar foydalanuvchi hech narsa kiritmasa
        for row in all_series[:50]:  # Ko‘pi bilan 50 tasi chiqsin
            results.append({
                'id': row[0],
                'name': row[1],
                'score': 100,
                'photo_url': row[2] or "https://telegra.ph/file/b606eb049d503c5d3d2fc.jpg"
            })
    else:
        series_dict = {row[1]: {'id': row[0], 'photo_url': row[2]} for row in all_series}
        matches = process.extract(series_name, series_dict.keys(), limit=20, scorer=fuzz.partial_ratio)

        for match in matches:
            name = match[0]
            score = match[1]
            if score > 60:
                results.append({
                    'id': series_dict[name]['id'],
                    'name': name,
                    'score': score,
                    'photo_url': series_dict[name]['photo_url'] or "https://telegra.ph/file/b606eb049d503c5d3d2fc.jpg"
                })

    return results if results else [{'id': None, 'name': 'No match found', 'score': 0, 'photo_url': None}]


# ------ Oddiy xabar yuborish funksiyasi --------
def oddiy_xabar(msg):
    success = 0
    error = 0
    
    # Ma'lumotlar bazasidan foydalanuvchilar ro'yxatini olish
    stat = cursor.execute("SELECT chat_id FROM users").fetchall()
    
    for user in stat:
        chat_id = user[0]
        try:
            # Xabarni nusxalab yuborish
            bot.copy_message(chat_id=chat_id, from_chat_id=msg.chat.id, message_id=msg.message_id)
            success += 1
            
            # Flood limitni oldini olish uchun kutish
            time.sleep(0.5)  # Har xabar orasida yarim soniya kutish
        except Exception as e:
            print(f"Xatolik {chat_id} ga yuborishda: {e}")
            error += 1
            
            # Retry (qayta urinish) qilishga harakat
            time.sleep(2)
            try:
                bot.copy_message(chat_id=chat_id, from_chat_id=msg.chat.id, message_id=msg.message_id)
                success += 1
                error -= 1  # Xatoni tuzatilgan deb hisoblash
            except Exception as retry_error:
                print(f"Qayta urinish muvaffaqiyatsiz {chat_id} uchun: {retry_error}")
    
    # Adminlarga natijalarni yuborish
    for admin_id in ADMIN_ID:
        bot.send_message(
            admin_id,
            f"<b>Xabar yuborildi!</b>\n\n✅ Yuborildi: {success}\n❌ Yuborilmadi: {error}",
            parse_mode='HTML'
        )


# ------ Forward xabar yuborish funksiyasi --------

def forward_xabar(msg):
  success = 0
  error = 0
  stat = cursor.execute("SELECT chat_id FROM users").fetchall()
  for i in stat:
    print(i[0])
    try:
      success+=1
      bot.forward_message(i[0], ADMIN_ID, msg.message_id)
    except:
      error+=1
  for chat_id in ADMIN_ID:
    bot.send_message(chat_id, f"<b>Xabar yuborildi!\n\n✅Yuborildi: {success}\n❌ Yuborilmadi: {error}</b>", reply_markup=admin_panel())



# ------ Admin kanal qo'shish  --------
def generate_admin_panel():
    keyboard = InlineKeyboardMarkup(row_width=1)
    channels = get_channels()
    if channels:
        for channel in channels:
            keyboard.add(InlineKeyboardButton(f"{channel[1]} ({channel[2]})", callback_data="no_action"))
    else:
        keyboard.add(InlineKeyboardButton("❌ Kanallar mavjud emas.", callback_data="no_action"))
    keyboard.add(
        InlineKeyboardButton("➕ Kanal qo'shish", callback_data="add_channel"),
        InlineKeyboardButton("❌ Kanal o'chirish", callback_data="delete_channel")
    )
    return keyboard

def generate_delete_buttons():
    keyboard = InlineKeyboardMarkup(row_width=1)
    channels = get_channels()
    for channel in channels:
        keyboard.add(InlineKeyboardButton(channel[1], callback_data=f"delete_{channel[0]}"))
    keyboard.add(InlineKeyboardButton("🔙 Ortga", callback_data="back_to_admin"))
    return keyboard


def generate_join_key():
    keyboard = InlineKeyboardMarkup(row_width=1)
    channels = get_channels()  # Kanallarni databasedan olish
    for channel in channels:
        # Kanallar ma'lumotlarini to'g'ri indekslar bilan foydalanish
        keyboard.add(InlineKeyboardButton(channel[1], url=channel[2]))
    keyboard.add(InlineKeyboardButton('✅ Tasdiqlash', callback_data="member"))
    return keyboard
 

def join(user_id):
    channels = get_channels()  # Kanallar ro'yxati
    for channel in channels:
        try:
            channel_url = channel[2]  # Kanal URL'si https://t.me/cosmos_for formatida
            channel_username = channel_url.split('/')[-1]  # username: cosmos_for
            if not channel_username.startswith('@'):
                channel_username = '@' + channel_username  # @cosmos_for formatiga o'tkazish

            print(f"Kanal username: {channel_username}")

            member = bot.get_chat_member(channel_username, user_id)

            if member.status not in ['member', 'creator', 'administrator']:
                # Foydalanuvchi a'zo emas
                bot.send_message(
                    user_id,
                    "👋 <b>Assalomu alaykum!</b>\n\n"
                    "Botdan foydalanish uchun quyidagi kanallarga a'zo bo'ling va "
                    "'✅ Tasdiqlash' tugmasini bosing.",
                    parse_mode='HTML',
                    reply_markup=generate_join_key()  # Inline tugmalarni jo'natish
                )
                return False
        except Exception as e:
            # Xatolikni chop etish
            bot.send_message(
                OWNER_ID,
                f"Kanaldagi a'zolikni tekshirishda xatolik: {str(e)}. Iltimos, administrator bilan bog'laning."
            )
            return False

    # Foydalanuvchi barcha kanallarga a'zo
    return True
