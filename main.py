import os
import requests as rq
from bs4 import BeautifulSoup as bs
import lxml
import time
import smtplib as sm
import ssl

# Your authentication data.
my_email = os.environ['SENDER_MAIL']
password = os.environ['SENDER_PASSWORD']
to_addy = os.environ['RECEIVER_MAIL']


# Price you want to buy the product.
DEAL_PRICE = # Price you want to deal.


# Function to check price of the item
def check_price():
    # Headers to specify USER AGENT (Software acting onbehalf of a user). Get user agent string for your browser at: https://www.useragentstring.com/pages/Browserlist/
    HEADERS = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36"
    }
    # URL of your product.
    AMAZON_URL = "LINK TO YOUR ITEM"

    response = rq.get(url=AMAZON_URL, headers=HEADERS)  # Using GET method to get response from product url.
    product_web_page = response.text  # Storing response as text.

    # Creating SOUP. Converting text to lxml to access elements.
    soup = bs(product_web_page, "lxml")

    price_string = soup.find("span", class_="a-offscreen")  # Storing price of product. Elements from web-pages may vary. Re-define elements according to your web-page.

    # Return conditions.
    if price_string is None:
        return None
    else:
        price = price_string.getText().strip("₹")  # Cleaning received data -> Removing spaces and symbols.
        # print(price)  # For testing.
        return float(price)  # Return price typecasted to float data type.


get_current_price = check_price()  # Getting price.
loop = True  # Boolean to check price after certain intervals -> To prevent browser from classfying program as bot.
counter = 0  # Counter to define intervals.
mail_msg = f"This is a steal! Order now! Follow Link: https"

while loop is True and counter < 15 and get_current_price is None:  # Maximum 15 attempts.
    # print(get_current_price)  # For testing
    counter += 1  # Increment counter.
    # print(f"Try #{counter}, returned: {get_current_price}")  # For testing number of counts.
    time.sleep(2)  # Pausing execution -> To prevent browser from classfying program as bot.
    get_current_price = check_price()  # Re-check for the price.
else:
    current_price = get_current_price  # Storing into other variable to send mail.
    if current_price is not None:
        if current_price > DEAL_PRICE:
            print("Today isn't the day to buy!")  # To let the programmer know that the product is above expected deal price.
        else:
            # print("sending email")  # For testing.
            # Using SMTP:
            with sm.SMTP_SSL("smtp.gmail.com", port=465, context=ssl.create_default_context()) as connection:
                connection.login(my_email, password)
                connection.sendmail(from_addr=my_email, to_addrs=to_addy,
                                    msg=f"Subject:Santobku Knife! - Amazon Price Watcher\n\nget it now!!")
                
        loop = False  # Breaking loop.
        print(f"Bought at: {DEAL_PRICE}\nCurrent: {current_price}")  # For testing/ reference.
    else:
        print("Sorry, please try again. I couldn't get the current price.")  # Product was not available at deal price.
