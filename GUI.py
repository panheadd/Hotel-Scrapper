import tkinter as tk
from tkinter import ttk
import re
import Scrapping

main_window = tk.Tk()

city = tk.StringVar()
check_in = tk.StringVar()
check_out = tk.StringVar()
currency = tk.StringVar(value='TL')


def run():
    global main_window, city, check_in, check_out, currency
    main_window.title("Search Hotels In Europe")
    main_window.geometry("1200x900")

    tk.Label(text="Select City In Europe:").place(x=300, y=10)

    ttk.Combobox(textvariable=city, values=["Marseille", "Dubrovnik", "Bari", "Zadar", "Barcelona", "Valencia", "Amsterdam", "Madrid", "Heraklion", "Bastia"]).place(x=500, y=7)

    tk.Label(text="Enter Check-in:").place(x=300, y=50)

    tk.Entry(textvariable=check_in).place(x=500, y=47)

    tk.Label(text="(YYYY-MM-DD)").place(x=700, y=50)

    tk.Label(text="Enter Check-out:").place(x=300, y=90)

    tk.Entry(textvariable=check_out).place(x=500, y=87)

    tk.Label(text="(YYYY-MM-DD)").place(x=700, y=90)

    tk.Label(text="Preferred Currency:").place(x=300, y=130)

    tk.Radiobutton(text="Euro", variable=currency, value="Euro").place(x=500, y=132)

    tk.Radiobutton(text="TL", variable=currency, value="TL").place(x=600, y=132)

    tk.Button(text="Search", command=search).place(x=540, y=162)

    main_window.mainloop()


def check_date(date_string):
    if re.match(r'^\d\d\d\d-\d\d-\d\d$', date_string):
        return True
    else:
        return False


def check_date_before_after(check_in_date_string, check_out_date_string):
    year1 = check_in_date_string[:4]
    year2 = check_out_date_string[:4]
    if int(year1) > int(year2):
        return False
    else:
        month1 = check_in_date_string[5:7]
        month2 = check_out_date_string[5:7]
        if int(month1) > int(month2):
            return False
        else:
            day1 = check_in_date_string[8:]
            day2 = check_out_date_string[8:]
            if int(day1) > int(day2):
                return False
            else:
                return True


info_text = tk.Label(text="Please Select City And Enter Dates In (YYYY-MM-DD) Format")
exception_text = tk.Label(text="Something went wrong.")

will_forgot_texts = []


def search():
    global city, main_window, check_in, check_out, currency, will_forgot_texts

    selected_city = city.get()
    check_in_date = check_in.get()
    check_out_date = check_out.get()
    selected_currency = currency.get()

    exception_text.place_forget()
    info_text.place_forget()

    if selected_city == "" or not check_date(check_in_date) or not check_date(check_out_date) or not check_date_before_after(check_in_date, check_out_date):
        info_text.place(x=390, y=200)
    else:
        for text in will_forgot_texts:
            text.place_forget()
        will_forgot_texts.clear()

        tk.Label(text="---Search Results---").place(x=520, y=250)

        tk.Label(text="Name:").place(x=10, y=350)
        tk.Label(text="Address:").place(x=510, y=350)
        tk.Label(text="Distance to center:").place(x=810, y=350)
        tk.Label(text="Rating:").place(x=1010, y=350)
        tk.Label(text="Price:").place(x=1110, y=350)

        try:
            Scrapping.scrap_hotel(selected_city, check_in_date, check_out_date)

        except Exception:
            exception_text.place(x=500, y=200)

        hotel_info_sorted = sorted(Scrapping.hotels_data, key=lambda k: k['Price'])
        hotel_info_sorted = hotel_info_sorted[:5]

        currency_sign = ""
        for hotel in hotel_info_sorted:
            price_int_tr = hotel.get("Price")
            price_int_eu = int(hotel.get("Price") / 30)
            if selected_currency == "TL":
                hotel["Price"] = price_int_tr
                currency_sign = "₺"
            else:
                hotel["Price"] = price_int_eu
                currency_sign = "€"

        y = 0

        for hotel in hotel_info_sorted:
            name_text = tk.Label(text=hotel.get("Name"))
            name_text.place(x=10, y=400 + y)
            will_forgot_texts.append(name_text)

            address_text = tk.Label(text=hotel.get("Address"))
            address_text.place(x=510, y=400 + y)
            will_forgot_texts.append(address_text)

            distance_text = tk.Label(text=hotel.get("Distance"))
            distance_text.place(x=810, y=400 + y)
            will_forgot_texts.append(distance_text)

            rating_text = tk.Label(text=hotel.get("Rating"))
            rating_text.place(x=1010, y=400 + y)
            will_forgot_texts.append(rating_text)

            price_text = tk.Label(text=str(hotel.get("Price"))+currency_sign)
            price_text.place(x=1110, y=400 + y)
            will_forgot_texts.append(price_text)
            y = y + 30
