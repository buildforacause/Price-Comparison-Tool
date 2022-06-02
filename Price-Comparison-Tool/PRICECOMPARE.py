from tkinter import *
from bs4 import BeautifulSoup
import requests
from tkhtmlview import HTMLLabel

AMAZON = "https://www.amazon.in/s"
FLIPKART = "https://www.flipkart.com/search"
headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/97.0.4692.71 Safari/537.36",
    "accept-language": "en-US,en;q=0.9"
}

RED = 'background-color: red; color: white;'
GREEN = 'background-color: green; color: white;'
YELLOW = 'background-color: yellow; color: black;'
BEST_DEAL = '<img src= "https://giphy.com/embed/u7Lqr8BhhWbvasXFpy" width="10" height="10">'


def search():
    product_name = "+".join(user_input.get().split(" "))
    amz_params = {
        "k": product_name
    }
    fk_params = {
        "q": product_name,
        "otracker": "search"
    }
    amazon = requests.get(AMAZON, headers=headers, params=amz_params)
    flipkart = requests.get(FLIPKART, headers=headers, params=fk_params)
    bsObj_amz = BeautifulSoup(amazon.text, "lxml")
    bsObj_fk = BeautifulSoup(flipkart.text, "lxml")
    amz_result = bsObj_amz.find_all("div", class_="s-result-item")[4:5]
    fk_result = bsObj_fk.find_all("div", class_="col-12-12")[6:]
    amz_link, fk_link = amazon.url, flipkart.url
    amazon_result, flipkart_result = HTMLLabel(window), HTMLLabel(window)
    try:
        amz_price = amz_result[0].find('span', class_='a-offscreen').text
    except:
        amz_price = "₹0,00"
    try:
        fk_price = fk_result[0].find('div', class_='_30jeq3').text
    except:
        fk_price = "₹0,00"
    new_amz_price = int("".join(amz_price[1:].split(",")))
    new_fk_price = int("".join(fk_price[1:].split(",")))
    amz_style, fk_style = "", ""
    if new_amz_price < new_fk_price:
        amz_style += GREEN
        fk_style += RED
        best_deal.place(x=715, y=180)
    else:
        fk_style += GREEN
        amz_style += RED
        best_deal.place(x=690, y=310)
    try:
        fk_product = fk_result[0].find('div', class_='_4rR01T').text
    except:
        try:
            fk_product = fk_result[0].find('a', class_='IRpwTa').text
        except:
            try:
                fk_product = fk_result[0].find('a', class_='s1Q9rs').text
            except:
                fk_product = "Didn't find something relevant"
                fk_price = ""
                fk_style = YELLOW
                best_deal.place_forget()
    try:
        amz_product = amz_result[0].h2.text
    except:
        amz_product = "Didn't find something relevant"
        amz_price = ""
        amz_style = YELLOW
        best_deal.place_forget()

    amz_html = f'''
        <p style='{amz_style}'><a style='{amz_style}' href={amz_link}>Amazon</a>: {amz_product} - {amz_price}</p>
    '''
    fk_html = f'''
        <p style='{fk_style}'><a style='{fk_style};' href={fk_link}>Flipkart</a>: {fk_product} - {fk_price}</p>
    '''
    amazon_result.set_html(amz_html)
    flipkart_result.set_html(fk_html)
    amazon_result.place(x=20, y=190)
    flipkart_result.place(x=20, y=320)
    results.config(text="Comparison Results")


window = Tk()
window.minsize(width=450, height=450)
window.title("Price Comparison Tool")

# Labels
title = Label(text="Price Comparison Tool", fg="black", font=("Courier", 45))
title.grid(row=0, column=0, columnspan=3)

results = Label(text="", fg="black", font=("Courier", 15))
results.place(x=250, y=125)

title1 = Label(text="Product Name: ", fg="black", font=("Courier", 15))
title1.grid(row=2, column=0, sticky="e")

user_input = Entry(width=69)
user_input.grid(row=2, column=1, sticky="w")

button = Button(text="Compare", width=14, command=search, relief="groove")

button.grid(row=2, column=2, sticky="w")

img = PhotoImage(file="giphy_resize.gif")
best_deal = Label(image=img, height=50, width=40)

window.mainloop()
