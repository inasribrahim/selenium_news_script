import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import telebot
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

url = "https://www.selenium.dev/"
## seleniumNewsbot
# Access environment variables
#BOT_TOKEN = os.getenv('BOT_TOKEN')
Bot_token = "7141875368:AAF_ZOHTPnYlfYKLHgm5UDQNqbCTUNKIwZk"
bot = telebot.TeleBot(Bot_token)

text_message = {
    "welcome": "Welcome to Selenium Releases!",
    "saying_good_bye": "Goodbye, {name}!"
}

def get_release_info():
    response = requests.get(url)
    if response.status_code == 200:
        html_content = response.text
        soup = BeautifulSoup(html_content, "html.parser")
        release_divs = soup.find_all("div", class_="card-body")
        selenium_releases = soup.find_all(string=lambda string: "Released" in string)

        release_list = []
        release_dictionary = {}  # Dictionary to store release version and details

        for release in selenium_releases:
            release_list.append(release.strip())

        for div in release_divs:
            release_link = div.find("a", class_="selenium-link")
            if release_link:
                link_href = release_link.get("href")
                link_version = link_href.split('selenium-')[1].split('-released')[0].replace('-', '.')

                for release_item in release_list:
                    if link_version in release_item:
                        release_dictionary[urljoin(url, link_href)] = release_item
                        break

        return release_dictionary

@bot.message_handler(commands=["start", "help"])
def start_bot(message):
    bot.send_message(message.chat.id, text_message["welcome"])

@bot.message_handler(func=lambda message: True)
def reply(message):
   release_info = get_release_info()
   user_name = "Automation Team "
   for link, release in release_info.items():
       fix_link = "https://github.com/SeleniumHQ/selenium/blob/trunk/java/CHANGELOG"
       message_text = f"\n{release}: {link} \nFix: {fix_link}\n\nSent by: {user_name}"
       bot.send_message(message.chat.id, message_text)
       break

# Start the bot
bot.infinity_polling()
