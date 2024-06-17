import requests
import streamlit as st
import shutil
import random
import gtts
import requests
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import urllib.request
import random
from gtts import gTTS
import sqlite3
import logging
import time
from time import strftime
import datetime
import khayyam
import datetime
import time
from IPython.display import HTML
from bs4 import BeautifulSoup
import base64
import os
import phonenumbers
import phonenumbers
from phonenumbers import geocoder, carrier
from deep_translator import GoogleTranslator

conn = sqlite3.connect('chatbot_data.db')


# ایجاد یک cursor
cursor = conn.cursor()
LOG_FILE = 'user_logs.log'
LOG_FORMAT = '%(asctime)s - %(levelname)s - %(message)s'
logging.basicConfig(filename=LOG_FILE, level=logging.INFO, format=LOG_FORMAT)
# ایجاد جدول برای ذخیره پاسخ‌های Chatbot
cursor.execute('''
    CREATE TABLE IF NOT EXISTS chatbot_responses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_input TEXT,
        bot_response TEXT
    )
    
''')
def get_phone_number_info(phone_number):
    try:
      
        parsed_phone_number = phonenumbers.parse(phone_number, "IR")
        
        # دریافت اطلاعات مربوط به موقعیت جغرافیایی
        location = geocoder.description_for_number(parsed_phone_number, "fa")
        
        # دریافت اطلاعات مربوط به اپراتور
        operator = carrier.name_for_number(parsed_phone_number, "fa")
        
        # بازگشت اطلاعات به ترتیب مطلوب
        return (phone_number, parsed_phone_number.country_code, parsed_phone_number.national_number, location, operator)
    except phonenumbers.NumberParseException as e:
        return (phone_number, None, None, None, None)
def fetch_estekhare():
    url = "http://api-free.ir/api/es.php"
    response = requests.get(url)
    data = response.json()
    return data
def get_bmi_category(bmi):
    if bmi < 18.5:
        return "کمبود وزن"
    elif 18.5 <= bmi < 25:
        return "طبیعی"
    elif 25 <= bmi < 30:
        return "اضافه وزن"
    else:
        return "چاقی"
def animate_image(image_link):
    # لینک وب‌سرویس
    url = f'http://api-free.ir/api/enime/?img={image_link}'

    # دریافت نتیجه وب‌سرویس
    response = requests.get(url)
    data = response.json()

    # چک کردن صحت دریافت نتیجه
    if data['ok']:
        # دریافت لینک عکس انیمه شده
        image_url = data['result']
        
        # دریافت عکس و نمایش آن
        image_response = requests.get(image_url)
        image_data = Image.open(BytesIO(image_response.content))
        st.image(image_data, caption='تصویر انیمه شده')
        st.success("تصویر انیمه شده با موفقیت ذخیره شد.")
    else:
        st.error("دریافت نتیجه انیمه شده با مشکل مواجه شده است.")


def chatgpt4(text):
    s = requests.Session()
    
    
    
    chat = s.get(f"http://api-free.ir/api/bard.php?text={text}").json()["result"]
    return chat

    

# اضافه شده
def add_something(text):
    s = requests.Session()
    added_text = s.get(f"http://api-free.ir/api/bard.php?text={text}").json()["text"]
    return added_text
 
def download_logo_and_save(text):
    random_logo_url = fetch_random_logo(text)
    if random_logo_url:
        try:
            response = requests.get(random_logo_url)
            image = Image.open(BytesIO(response.content))
            st.image(image, caption='Generated Logo', use_column_width=True)
            st.success("Logo saved successfully.")
        except Exception as e:
            st.error("Error occurred while saving logo:", e)
    else:
        st.warning("No logos found.")
# def fetch_random_logo(text):
#     url = f"https://api-free.ir/api/Logo-top.php?text={text}&page={str(random.randint(1, 99))}"

#     try:
#         response = requests.get(url)
#         data = response.json()
#         if 'result' in data and data['result']:
#             return random.choice(data['result'])
#         else:
#             st.error("Error: No logos found.")
#             return None
#     except Exception as e:
#         st.error("Error occurred:", e)
#         return None



def download_logo(logo_url):
    try:
        response = requests.get(logo_url)
        image = Image.open(BytesIO(response.content))
        st.image(image, caption='Generated Logo', use_column_width=True)
        st.success("Logo saved successfully.")
    except Exception as e:
        st.error("Error occurred while saving logo:", e)

# اضافه کردن پاسخ Chatbot به جدول
def insert_chatbot_response(user_input, bot_response):
    cursor.execute('INSERT INTO chatbot_responses (user_input, bot_response) VALUES (?, ?)', (user_input, bot_response))
    conn.commit()
# تنظیمات صفحه را سفارشی کنید
st.set_page_config(
    page_title="ChatGPT",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
    

)

def fetch_random_logo(text):
    page = random.randint(1, 99)
    url = f"https://api-free.ir/api/Logo-top.php?text={text}&page={page}"

    try:
        response = requests.get(url)
        data = response.json()
        if 'result' in data and data['result']:
            # انتخاب یک لینک تصادفی از لیست لینک‌های لوگوها
            random_logo_url = random.choice(data['result'])
            return random_logo_url
        else:
            st.error("Error: No logos found.")
            return None
    except Exception as e:
        st.error("Error occurred:", e)
        return None


def download_and_save_music(file_path, music_link):
    response = requests.get(music_link)
    if response.status_code == 200:
        with open(file_path, "wb") as file:
            file.write(response.content)

# https://chatgpt.ai/

def save_to_file(filename, content):
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(content)

def download_image(img_data, folder):
    img_data = img_data.split(',')[1]  # جدا کردن بخش اطلاعاتی از داده‌های تصویر
    img_binary = base64.b64decode(img_data)  # رمزگشایی داده‌های باینری تصویر
    with open(os.path.join(folder, f'image_{len(os.listdir(folder)) + 1}.png'), 'wb') as file:
        file.write(img_binary)
def get_random_music_link():
    api_url = "https://api-free.ir/api/music/"
    response = requests.get(api_url)
    if response.status_code == 200:
        data = response.json()
        if data.get("ok") and data.get("result") and data["result"].get("song"):
            return data["result"]["song"]
    return None

st.image('ai.jpg', width=100)
st.title('ChatGPT')
st.subheader('Free-GPT-Chat')

inp = st.chat_input('درخواست خود را وارد کنید')

if inp:
    if inp.startswith("تصویر"):
        st.text('در حال بارگیری...')
        image = inp.replace("تصویر","").strip()
        try :
            
            response = requests.get(f"http://api-free.ir/api/img.php?text={image}&v=3.5")
            response.raise_for_status()
                
            data = response.json()
            result = data["result"]
            
            # انتخاب یک عنصر تصادفی از لیست result
            random_link = random.choice(result)
            
            response = requests.get(random_link, stream=True)
            response.raise_for_status()
            
            with open("downloaded_image.jpg", "wb") as out_file:
                
                shutil.copyfileobj(response.raw, out_file)
                st.image("downloaded_image.jpg") 
                
                    
        
          
        except requests.exceptions.RequestException as e:
            st.error(f"خطا در دریافت تصویر: {e}")  
    elif inp.startswith("مونث"):
        
        text = inp.replace("مونث", "").strip()
        st.text('در حال پردازش ویس')
       
        
        
        # تبدیل متن به صدا
        try:
            response = requests.get(f"https://api-free.ir/api/voice.php?text={text}&mod=DilaraNeural")
            response.raise_for_status()  # بررسی موفقیت درخواست
                
            result_url = response.json()["result"]
            voice_response = requests.get(result_url)
            
            voice_response.raise_for_status()
        
            
            with open('voice_bot.mp3', "wb") as f:
                
                f.write(voice_response.content)
                st.audio("voice_bot.mp3", format='audio/mp3')
        except requests.exceptions.RequestException as mz:
            
            
            st.error(f"erorr:\n{mz}")        
        
            
            # 
       
    elif inp.startswith("مذکر"):
        text_man = inp.replace("مذکر", "").strip()  
        st.text('در حال پردازش ویس')
        response = requests.get(f"https://api-free.ir/api/voice.php?text={text_man}&mod=FaridNeural")
        response.raise_for_status()  # بررسی موفقیت درخواست
            
        result_url = response.json()["result"]
        voice_response = requests.get(result_url)
        try:

        
            voice_response.raise_for_status()
            with open('voice_bot_man.mp3', "wb") as f:
                
                
                f.write(voice_response.content)
                st.audio("voice_bot_man.mp3", format='audio/mp3')
        except requests.exceptions.RequestException as m:
            st.error(f"erorr:\n{m}")
    elif inp.startswith("voice"):
        
        
        text = inp.replace("voice", "").strip()
        
        st.text('در حال پردازش ویس')
        
        tts = gTTS(text)
        tts.save("responsee.mp3")
        st.audio("responsee.mp3", format='audio/mp3')
        
        
            
        # پخش صدا
        # os.system("start response.mp3")
    
    elif inp =="اهنگ"or inp =="music":
        st.text("منتظربمانید که اهگ اماده بشه")
        random_music_link = get_random_music_link()
        try:
            if random_music_link:
                music_file_name = "random_music.mp3"
                download_and_save_music(music_file_name, random_music_link)
                with open(music_file_name, 'rb') as music_file:
                    st.audio('random_music.mp3',format='audio/mp3')
        except Exception as m:
            st.error(f"erorr:\n {m}")
    elif inp=="bg" or inp =="بگراند":
        st.text("منتظربمانید که  بگراند ارسال شه")
        # لیست مدل‌ها
        model_list = [
            "animals",
            "stock-images",
            "travel",
            "nature",
            "military",
            "hi-tech",
            "games",
            "celebrities",
            "art",
            "architecture",
            "abstract",
            
        ]

        # URL وب‌سرویس
        url_template = "https://api-free.ir/api/background2.php?page=1&text={}"

        # تولید لینک برای یک مدل تصادفی
        random_model = random.choice(model_list)
        url = url_template.format(random_model)

        # ارسال درخواست و دریافت پاسخ
        response = requests.get(url)

        # تبدیل پاسخ به دیکشنری
        data = response.json()

        # استخراج لینک‌های عکس از پاسخ
        image_links = data.get('result', [])

        # انتخاب تصویر تصادفی
        random_image_link = random.choice(image_links)

        # دانلود تصویر
        image_response = requests.get(random_image_link)
        image = Image.open(BytesIO(image_response.content))

        # نمایش تصویر


        # ذخیره تصویر با نام خاص
        image_name = "random_image.jpg"
        image.save(image_name)
        st.image("random_image.jpg")
   
    
    elif inp.startswith("عکس"):
        
        st.text('در حال بارگیری...')
        
        image = inp.replace("عکس","").strip()
        try :
            
            response = requests.get(f"http://api-free.ir/api/img.php?text={image}&v=4")
            response.raise_for_status()
                
            data = response.json()
            result = data["result"]
            
            # انتخاب یک عنصر تصادفی از لیست result
            random_link = random.choice(result)
            
            response = requests.get(random_link, stream=True)
            response.raise_for_status()
            
            with open("downloaded_image.jpg", "wb") as out_file:
                
                shutil.copyfileobj(response.raw, out_file)
                st.image("downloaded_image.jpg", use_column_width=True) 
                
                    
        
          
        except requests.exceptions.RequestException as e:
            st.error(f"خطا در دریافت تصویر: {e}") 
    elif inp.startswith("موزیک"):
        st.text("منتظرسرچ موزیک وارسال آن باشید")
        query = inp.replace("موزیک","")
        url = f"https://api-free.ir/api/sr-music/?text={query}"
        response = requests.get(url)   
        
        
        if response.status_code == 200:
            data = response.json()
            
    
    # دریافت لینک فایل صوتی از دیکشنری result
            song_url = data["result"]["song"]
            
            
            # دانلود فایل صوتی
            urllib.request.urlretrieve(song_url, "music_plyar.mp3") 
            
            with open("music_plyar.mp3","rb") as m:
                st.audio('music_plyar.mp3',format='audio/mp3')
            
                m.close()
    elif inp.startswith("font"):
        st.text("درحال ساخت فونت ")
        a =inp.replace("font","")
        fonts = requests.get(f'http://api-free.ir/api/font.php?en={a}').json()["result"]
        formatted_fonts = "\n".join([f"{index + 1}. {font}" for index, font in enumerate(fonts)])
        try:
        
            st.text_area("Chatbot's Response", value=f"فونت‌های شما:\n{formatted_fonts}"  , height=400)
            # font_to_database(fonts)
            
         
        except Exception as f:
            
            st.text_area("Chatbot's Response", value=f"erorr:\n{f}"  , height=400)
    elif inp.startswith("فونت"):
        st.text("درحال ساخت فونت ")
        a =inp.replace("font","")
        fonts = requests.get(f'http://api-free.ir/api/font.php?fa={a}').json()["result"]
        formatted_fonts = "\n".join([f"{index + 1}. {font}" for index, font in enumerate(fonts)])
        try:
        
            st.text_area("Chatbot's Response", value=f"فونت‌های شما:\n{formatted_fonts}"  , height=400)
            # font_to_database(fonts)
            
         
        except Exception as f:
            st.error(f"erorr:\n{f}")
            
            
            # st.text_area("Chatbot's Response", value=f"erorr:\n{f}"  , height=400)
    
    elif inp == "چنل" or inp == "کانال":
        
        st.markdown("[Python Channel](https://t.me/pythonsource1384)")
    
    
    
        
    elif inp.startswith("logo"):
        text = inp.replace("logo","").strip()
        a=download_logo_and_save(text)
    elif inp.startswith("anime"):
        
        st.text('در حال انیمه کردن')
        image_link = inp.replace("anime", "").strip()
        
        try:
            response = requests.get(f"http://api-free.ir/api/enime/?img={image_link}")
            response.raise_for_status()
            data = response.json()
            
            if data.get('ok'):
                image_url = data['result']
                image_response = requests.get(image_url)
                image_data = Image.open(BytesIO(image_response.content))
                st.image(image_data, caption='تصویر انیمه شده', use_column_width=False)
                st.success("تصویر انیمه شده با موفقیت ذخیره شد.")
            else:
                st.error("خطا در انیمه کردن تصویر.")
        except requests.exceptions.RequestException as e:
            st.error(f"خطا در دریافت تصویر: {e}")
    elif inp.startswith("انیمه"):
        
            
        st.text('در حال انیمه کردن')
        image_link = inp.replace("انیمه", "").strip()
        
        try:
            response = requests.get(f"http://api-free.ir/api/enime/?img={image_link}")
            response.raise_for_status()
            data = response.json()
            
            if data.get('ok'):
                image_url = data['result']
                image_response = requests.get(image_url)
                image_data = Image.open(BytesIO(image_response.content))
                st.image(image_data, caption='تصویر انیمه شده', use_column_width=False)
                st.success("تصویر انیمه شده با موفقیت ذخیره شد.")
            else:
                st.error("خطا در انیمه کردن تصویر.")
        except requests.exceptions.RequestException as e:
            st.error(f"خطا در دریافت تصویر: {e}")
            
            
    
    elif inp =="استخاره":
        
        
        
        estekhare_data = fetch_estekhare()
        
        
        
        if estekhare_data["ok"]:
            # Display result
            st.subheader("نتیجه استخاره:")
            st.write(f"سوره: {estekhare_data['result']['soreh']}")
            st.write(f"آیه: {estekhare_data['result']['ayeh']}")
            st.write(f"نتیجه: {estekhare_data['result']['natijeh']}")
            st.write(f"نتیجه کلی: {estekhare_data['result']['natijeh_kolli']}")
            st.write(f"نتیجه ازدواج: {estekhare_data['result']['natijeh_ezdevaj']}")
            st.write(f"نتیجه معامله: {estekhare_data['result']['natijeh_moameleh']}")

            # Display image
            st.subheader("تصویر مرتبط:")
            image_url = estekhare_data["result"]["image"]
            image_response = requests.get(image_url)
            image = Image.open(BytesIO(image_response.content))
            st.image(image, caption='تصویر استخاره', use_column_width=True)
        else:
            st.error("خطا در دریافت اطلاعات استخاره")
    elif inp =="time" or inp =="تایم":
        current_time = time.strftime("%H:%M:%S")
        
        st.text_area("Chatbot's Response", value=f"تایم کنونی :{   current_time}"  , height=400)
    elif inp =="تاریخ":
        tariq =khayyam.JalaliDatetime.today().strftime("%A %D %B %Y")
        st.text_area("Chatbot's Response", value=f"تاریخ شما:\n{tariq}"  , height=400)
    
    elif inp.startswith("سورس"):
        
        url = inp.replace("سورس", "")
        response = requests.get(url)
        if response.status_code == 200:
            st.text("در حال دریافت قالب وب‌سایت...")
            
            soup = BeautifulSoup(response.content, 'html.parser')

            # استخراج قالب وب‌سایت
            website_template = soup.prettify()

            # استخراج کدهای CSS
            css_code = '\n'.join([style.get_text() for style in soup.find_all('style')])

            # استخراج کدهای JavaScript
            js_code = '\n'.join([script.get_text() for script in soup.find_all('script') if script.get('src') is None])

            # نمایش قالب وب‌سایت
            st.write("قالب وب‌سایت:")
            st.code(website_template, language='html')

            # نمایش کدهای CSS
            st.write("کدهای CSS:")
            st.code(css_code, language='css')

            # نمایش کدهای JavaScript
            st.write("کدهای JavaScript:")
            st.code(js_code, language='javascript')

            # نمایش تصاویر
            st.write("تصاویر:")
            for img in soup.find_all('img'):
                img_url = img.get('src')
                if img_url:
                    st.image(img_url)

        else:
            st.error(f"خطا: {response.status_code}")
    elif inp.startswith("info:"):
        st.text("منتظربمانید برای به دست اوردن اطلاعات شماره")
        phone_number =inp.replace("info:","")
        phone_number_info = get_phone_number_info(phone_number)
        st.write("شماره موبایل:", phone_number_info[0])
        st.write("کد کشور:", phone_number_info[1])
        st.write("شماره ملی:", phone_number_info[2])
        st.write("موقعیت جغرافیایی:", phone_number_info[3])
        st.write("اپراتور:", phone_number_info[4])
    
    elif inp.startswith("bmi:"):
        st.write("درحال به دست اوردن محاسبه توده بدنی")
        t=inp.replace("bmi:","")
        if ',h' in t:
            
            
            try:
                weight, height = list(map(float, inp.split('w')[1].split(',h')[0])), float(inp.split(',h')[1])
                weight = weight[0]  # چون map به لیست تبدیل شده است، باید مقدار مورد نیاز را استخراج کنیم
                bmi = weight / ((height / 100) ** 2)
                bmi_category = get_bmi_category(bmi)
                st.write(f"BMI شما: {bmi:.2f}\nدر دسته‌بندی BMI: {bmi_category}")
            except ValueError:
                st.error("مقادیر رادرست وارد کنید")
    elif inp=="چنل":
        st.write("بفرما چنل ما :\n@Python_Source_1403 \n@sokhon_yar")
    
    elif inp.startswith("ترجمه"):
        translit =inp.replace("ترجمه","")
        
        r =GoogleTranslator(source='auto',target='fa').translate(translit)
        st.write(f"ترجمه شده :\n{r}")
    
    
        
        
        
    
                





        
            
        
        
        
        
    
    
    
  
   
    
        
    
    
    
    
    
    
        
    

    
    
    
        
        
    
        
        

    
   
 
            
    else:
        st.text(' منتظربمانید برای پاسخ')
        try:
           
            chat =chatgpt4(inp)
            
             
            
            st.text_area("Chatbot's Response", value=chat  , height=400)
            insert_chatbot_response(inp, chat)
            
            a=logging.info(f"User input: {inp}, Chatbot response: {chat}")
            with open(LOG_FILE, 'r') as file:
                print(file.read())
                 
    
            
            
            
            
   
           
        except Exception as e:
            st.text_area("Error", value=f"An error occurred: {e}", height=200)
