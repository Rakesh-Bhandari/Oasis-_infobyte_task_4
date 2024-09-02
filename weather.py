import customtkinter as ctk
from tkinter import *
import requests
from geopy.geocoders import Nominatim
from datetime import datetime, timedelta
from PIL import Image,ImageTk
import random
from tkinter import messagebox

API_KEY = "7bf7479c5aea6c265fca3ba21c6fd1d8"

# Function to get coordinates using geopy
def get_coordinates(location):
    try:
        geolocator = Nominatim(user_agent="weather_app")
        location_data = geolocator.geocode(location)
        if location_data:
            return (location_data.latitude, location_data.longitude)
        else:
            return (None, None)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to get coordinates: {e}")
        return (None, None)

# Function to get weather data 
def get_weather(lat, lon, date, api_key=API_KEY):
    url = f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&units=metric"
    response = requests.get(url)
    return response.json()

# Function to display weather information 
def show_weather():
    location = search_area.get()
    if location:
        lat, lon = get_coordinates(location)
        if lat is not None and lon is not None:
            day = datetime.now()
            weather_data1 = get_weather(lat, lon, day)
            if weather_data1.get('cod') == 200:
                temp = weather_data1['main']['temp']
                feels_like = weather_data1['main']['feels_like']
                temp_max = weather_data1['main']['temp_max']
                condition1 = weather_data1['weather'][0]['description']
                humidity = weather_data1['main']['humidity']
                pressure = weather_data1['main']['pressure']
                wind_speed = weather_data1['wind']['speed']
                icon_id = weather_data1['weather'][0]['icon']
                Day = day.strftime('%A, %d %B %Y')
                time = day.strftime('%I:%M %p')
                update_weather_icon(icon_id)
                change_bg(condition1)
                
            else:
                messagebox.showerror("Error", "Could not retrieve weather data.")

            canvas.itemconfig(Descript,text=f"{condition1.capitalize()}|Feels like {feels_like}")
            canvas.itemconfig(w,text=wind_speed)
            canvas.itemconfig(h,text=humidity)
            canvas.itemconfig(p,text=pressure)
            canvas.itemconfig(day_canvas,text=Day)
            canvas.itemconfig(time_canvas,text=time)
            canvas.itemconfig(max_temp,text=temp_max)
            canvas.itemconfig(temperature, text=f'{temp}°C')

        else:
            messagebox.showerror("Error", "Location not found.")
            
    else:
        messagebox.showwarning("Input Required", "Please enter a location.")

# Function to change background image according to weather if not randomly
def change_bg(condition):
    if condition in image_references_2:
        canvas.itemconfig(back_ground, image=image_references_2[condition])
    else:
        random_codition = random.choice(list(image_references_2.keys()))
        canvas.itemconfig(back_ground, image=image_references_2[random_codition])

# Function to change icon according to weather
def update_weather_icon(condition):
    if condition in image_references:
        canvas.itemconfig(d, image=image_references[condition])

# Setting up the GUI with CustomTkinter
root=ctk.CTk()
root.title("Weather App")
root.geometry("900x500+200+50")
root.resizable(False,False)

root.iconbitmap(False,"icon/logo.ico")

image_references = {}
image_references['01d'] = PhotoImage(file="icon/01d@2x.png")
image_references['01n'] = PhotoImage(file="icon/01n@2x.png")
image_references['02d'] = PhotoImage(file="icon/02d@2x.png")
image_references['02n'] = PhotoImage(file="icon/02n@2x.png")
image_references['03d'] = PhotoImage(file="icon/03d@2x.png")
image_references['04d'] = PhotoImage(file="icon/04d@2x.png")
image_references['04n'] = PhotoImage(file="icon/04n@2x.png")
image_references['09d'] = PhotoImage(file="icon/09d@2x.png")
image_references['10d'] = PhotoImage(file="icon/10d@2x.png")
image_references['10n'] = PhotoImage(file="icon/10n@2x.png")
image_references['11d'] = PhotoImage(file="icon/11d@2x.png")
image_references['11n'] = PhotoImage(file="icon/11n@2x.png")
image_references['13d'] = PhotoImage(file="icon/13d@2x.png")
image_references['13n'] = PhotoImage(file="icon/13n@2x.png")
image_references['50d'] = PhotoImage(file="icon/50d@2x.png")
image_references['50n'] = PhotoImage(file="icon/50n@2x.png")

image_references_2={}
image_references_2['broken clouds'] = PhotoImage(file="weather/broken cloud.png")
image_references_2['clear sky'] = PhotoImage(file="weather/Clear_sky.png")
image_references_2['dust'] = PhotoImage(file="weather/Dust.png")
image_references_2['few clouds'] = PhotoImage(file="weather/few clouds.png")
image_references_2['fog'] = PhotoImage(file="weather/Fog.png")
image_references_2['haze'] = PhotoImage(file="weather/Haze.png")
image_references_2['heavy rain'] = PhotoImage(file="weather/heavy rain.png")
image_references_2['heavy snow'] = PhotoImage(file="weather/heavy Snow.png")
image_references_2['mist'] = PhotoImage(file="weather/Mist.png")
image_references_2['overcast clouds'] = PhotoImage(file="weather/Overcast cloud.png")
image_references_2['Rain'] = PhotoImage(file="weather/Rain.png")
image_references_2['scattered clouds'] = PhotoImage(file="weather/Scattered_Clouds.png")
image_references_2['Snow'] = PhotoImage(file="weather/snow.png")
image_references_2['Thunderstorm'] = PhotoImage(file="weather/ThunderStrome.png")
 
canvas=Canvas(root)
back_ground = canvas.create_image(0,0,image=image_references_2["clear sky"],anchor='nw')
canvas.pack(fill='both',expand=True)

search_image = ImageTk.PhotoImage(Image.open('icon/search_frame.png'),size=(475,77)) 
canvas.create_image(300,55,image=search_image)   
search_area = ctk.CTkEntry(root,justify='left',width=300,font=("poppins",25,"bold"),text_color="#fff",fg_color="#404040",border_width=0,bg_color="#404040",placeholder_text="Enter location")
search_area.place(x=110,y=40)
search_area.focus_set()
s_icon = ctk.CTkImage(light_image=Image.open("icon/search_icon.png"),size=(39,38))
search_button = ctk.CTkButton(root,image=s_icon,text="",fg_color="transparent",width=40,height=40,bg_color="#404040",cursor="hand2",corner_radius=0,hover=0,command=show_weather)
search_button.place(x=460,y=32)

day_canvas = canvas.create_text(80,100,text="Sunday",font=("helvetica",20,'bold'),fill='#000',anchor='w')
time_canvas = canvas.create_text(80,130,text="00:00 Am",font=("helvetica",20,'bold'),fill='#000',anchor='w')

logo_img = ImageTk.PhotoImage(Image.open('icon/logo.png'),size=(254,242)) 
canvas.create_image(180,250,image=logo_img)   

frame_box = ImageTk.PhotoImage(Image.open('icon/bottom_Frame.png'),size=(787,112))
frame_res = canvas.create_image(450,430,image=frame_box)

label1 = canvas.create_text(150,410,text="WIND",font=("helvetica",15,"bold"),fill="#000",anchor='w')
label2 = canvas.create_text(280,410,text="HUMIDITY",font=("helvetica",15,"bold"),fill="#000",anchor='w')
label3 = canvas.create_text(410,410,text="Pressure",font=("helvetica",15,"bold"),fill="#000",anchor='w')
label4 = canvas.create_text(580,410,text="Icon",font=("helvetica",15,"bold"),fill="#000",anchor='w')
label5 = canvas.create_text(700,410,text="Max_Temp",font=("helvetica",15,"bold"),fill="#000",anchor='w')

temperature = canvas.create_text(320,230,text="--°C",font=("arial",80,"bold"),fill='red',anchor='w')
Descript = canvas.create_text(320,300,text="     |Feels like",font=("arial",25,"bold"),fill='red',anchor='w')
w = canvas.create_text(150,450,text="-----",font=("helvetica",20,"bold"),fill="#000",anchor='w')
h = canvas.create_text(280,450,text="-----",font=("helvetica",20,"bold"),fill="#000",anchor='w')
p = canvas.create_text(410,450,text="-----",font=("helvetica",20,"bold"),fill="#000",anchor='w')
d = canvas.create_image(600,450,image=image_references['02d'])
max_temp = canvas.create_text(700,450,text="-----",font=("helvetica",20,"bold"),fill="#000",anchor='w')

root.mainloop()