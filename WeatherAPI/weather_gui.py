import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import requests

# =============================
# API CONFIG
# =============================
API_KEY = "2b6e29cb829f1dafdac1f316dba32d1d"
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"

def get_weather_data(city):
    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric"
    }
    try:
        res = requests.get(BASE_URL, params=params)
        if res.status_code == 200:
            return res.json()
        else:
            return None
    except:
        return None

# =============================
# WEATHER DISPLAY FUNCTION
# =============================
def show_weather():
    city = city_entry.get()
    unit = unit_var.get()

    if not city:
        messagebox.showwarning("Error", "Please enter a city")
        return

    data = get_weather_data(city)

    if not data:
        messagebox.showerror("Error", "City not found")
        return

    temp = data["main"]["temp"]
    feels = data["main"]["feels_like"]
    desc = data["weather"][0]["description"].title()
    humidity = data["main"]["humidity"]
    wind = data["wind"]["speed"]

    if unit == "F":
        temp = (temp * 9/5) + 32
        feels = (feels * 9/5) + 32
        unit_symbol = "°F"
    else:
        unit_symbol = "°C"

    output = (
        f"City: {city}\n"
        f"Weather: {desc}\n"
        f"Temperature: {temp:.1f}{unit_symbol}\n"
        f"Feels like: {feels:.1f}{unit_symbol}\n"
        f"Humidity: {humidity}%\n"
        f"Wind: {wind} m/s"
    )

    output_label.config(text=output)

# =============================
# GUI
# =============================
root = tk.Tk()
root.title("Weather App")
root.geometry("400x400")

# Load background
bg_img = Image.open("background.jpg")
bg_img = bg_img.resize((400, 400))
bg_photo = ImageTk.PhotoImage(bg_img)

bg_label = tk.Label(root, image=bg_photo)
bg_label.place(x=0, y=0, relwidth=1, relheight=1)

# Title
tk.Label(root, text="🌤 Weather App", font=("Arial", 18), bg="white").place(x=120, y=10)

# City input
tk.Label(root, text="Enter City:", bg="white").place(x=40, y=60)
city_entry = tk.Entry(root, width=25)
city_entry.place(x=120, y=60)

# Unit selection
unit_var = tk.StringVar(value="C")
tk.Radiobutton(root, text="Celsius", variable=unit_var, value="C", bg="white").place(x=120, y=95)
tk.Radiobutton(root, text="Fahrenheit", variable=unit_var, value="F", bg="white").place(x=200, y=95)

# Button
tk.Button(root, text="Get Weather", command=show_weather).place(x=150, y=130)

# Output label
output_label = tk.Label(root, text="", bg="white", font=("Arial", 11), justify="left")
output_label.place(x=40, y=180)

root.mainloop()
