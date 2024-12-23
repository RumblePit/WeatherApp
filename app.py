# Instalar geopy, timezonefinder, pytz
# Se necesita Iniciar Sesión y generar una APIKEY de https://home.openweathermap.org/
# En caso de ser necesario también se debe instalar requests para el consumo de API

from tkinter import *
import tkinter as tk
from geopy.geocoders import Nominatim
from tkinter import ttk, messagebox
from timezonefinder import TimezoneFinder
from datetime import datetime
import requests
import pytz

def getWeather():
    '''Se busca la ciudad ingresada, como resultado se mostrará su hora actual
    así como características climatológicas'''
    try:
        ciudad = txtfield.get()

        # Se obtiene la hora de la ciudad seleccionada
        geolocator = Nominatim(user_agent="WeatherApp")
        locacion = geolocator.geocode(ciudad)
        obj = TimezoneFinder()
        resultado = obj.timezone_at(lng=locacion.longitude, lat=locacion.latitude)

        home = pytz.timezone(resultado)
        local_time = datetime.now(home)
        current_time = local_time.strftime("%I:%M %p")
        reloj.config(text=current_time)
        nombre.config(text="TIEMPO ACTUAL")

        # Se consume API que da el CLIMA y sus características
        api_key = "#" # Ingresa tu APIKEY
        api = f"https://api.openweathermap.org/data/2.5/weather?q={ciudad}&appid={api_key}"

        json_data = requests.get(api).json()
        condicion = json_data['weather'][0]['main']
        descripcion = json_data['weather'][0]['description']
        temp = int(json_data['main']['temp'] - 273.15)
        presion = json_data['main']['pressure']
        humedad = json_data['main']['humidity']
        viento = json_data['wind']['speed']

        t.config(text=(temp,"°"))
        c.config(text=(condicion, "|", "SENSACION", "TERMICA", temp, "°"))

        v.config(text=viento)
        h.config(text=humedad)
        p.config(text=presion)
        d.config(text=descripcion)

    except Exception as e:
        # Se abrirá una ventana en caso de no encontrar la ciudad
        messagebox.showerror("Weather App", "Entrada Invalida")


# Ventana de la App
root = Tk()
root.title("Weather App")
root.geometry("900x500+300+200")
root.resizable(False,False)

# Barra de Busqueda
search_img = PhotoImage(file="images/search.png")
search_label = Label(image=search_img)
search_label.place(x=20, y=20)

txtfield = tk.Entry(root, justify="center", width=17, font=("poppins", 25,"bold"), bg="#404040", fg="white")
txtfield.place(x=50, y=40)
txtfield.focus()

# Botón de busqueda
search_icon = PhotoImage(file="images/search_icon.png")
icon_button = Button(image=search_icon, borderwidth=0, cursor="hand2", bg="#404040", command=getWeather)
icon_button.place(x=400, y=34)

# Logo
logo_img = PhotoImage(file="images/logo.png")
logo_label = Label(image=logo_img)
logo_label.place(x=150, y=100)

# Caja de características climáticas
frame_img = PhotoImage(file="images/box.png")
frame_label = Label(image=frame_img)
frame_label.pack(padx=5, pady=5, side=BOTTOM)

#  Hora actual de la ciudad
nombre = Label(root, font=("arial", 15, "bold"))
nombre.place(x=30, y=100)
reloj = Label(root, font=("Helvetica", 20))
reloj.place(x=30, y=140)

# Son las descripciones de cada característica
label1 = Label(root, text="VIENTO", font=("Helvetica", 15, "bold"), fg="white", bg="#1ab5ef")
label1.place(x=120, y=400)

label2 = Label(root, text="HUMEDAD", font=("Helvetica", 15, "bold"), fg="white", bg="#1ab5ef")
label2.place(x=250, y=400)

label3 = Label(root, text="DESCRIPCION", font=("Helvetica", 15, "bold"), fg="white", bg="#1ab5ef")
label3.place(x=430, y=400)

label4 = Label(root, text="PRESION", font=("Helvetica", 15, "bold"), fg="white", bg="#1ab5ef")
label4.place(x=650, y=400)

# Aquí dice la temperatura y condición de la ciudad seleccionada
t = Label(font=("arial", 70, "bold"), fg="#ee666d")
t.place(x=400, y=150)
c = Label(font=("arial", 15, "bold"))
c.place(x=400, y=250)

# Aquí van las características del clima de la ciudad seleccionada
v = Label(text="...", font=("arial", 20, "bold"), bg="#1ab5ef")
v.place(x=120, y=430)
h = Label(text="...", font=("arial", 20, "bold"), bg="#1ab5ef")
h.place(x=250, y=430)
d = Label(text="...", font=("arial", 20, "bold"), bg="#1ab5ef")
d.place(x=430, y=430)
p = Label(text="...", font=("arial", 20, "bold"), bg="#1ab5ef")
p.place(x=650, y=430)

root.mainloop()
