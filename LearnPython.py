import streamlit as st
import python_weather as pw
import asyncio

st.toast("Bazzingga!!", duration="short", icon="🔥")

async def get_weather():
    keys = ["temp", "humid", "prec", "pres", "ws", "city"]

    for k in keys:
        if k not in st.session_state:
            st.session_state[k] = None

    client = pw.Client()

    st.title("Weather App", anchor=None, help=None, width="stretch", text_alignment="center")
    country = st.text_input("Insert (Country/Cities/...)", max_chars=300, type="default", help="Insert (Country/Cities/...)", placeholder="Country A", value="Jakarta", icon="🌎")

    if st.session_state.city != country:
        st.session_state.temp = None
        st.session_state.humid = None
        st.session_state.prec = None
        st.session_state.pres = None
        st.session_state.ws = None
        st.session_state.city = country

    weather = await client.get(country)

    temp, humid, prec = st.columns(3)
    pres, coor = st.columns(2)

    st.metric("Country", value=weather.country, help="Country", border=True, width="stretch")
    
    pupils, feel = st.columns(2)

    st.metric("Description", value=weather.description, help="Description", border=True, width="stretch")

    ws, uv = st.columns(2)

    st.metric("Wind Direction", value=str(weather.wind_direction), help="Wind Direction", border=True)

    x,y = weather.coordinates

    with temp:
        new_temp = weather.temperature
        old_temp = st.session_state.temp

        delta_t = 0 if old_temp is None else new_temp - old_temp
        st.metric("Temperature (°C)", value=f"{new_temp} °C", delta=f"{delta_t} °C", help="Temperature", border=True)

        st.session_state.temp = new_temp
    with humid:
        new_humid = weather.humidity
        old_humid = st.session_state.humid

        delta_h = 0 if old_humid is None else new_humid - old_humid
        st.metric("Humidity (%)", value=f"{new_humid} %", delta=f"{delta_h} %", help="Humidity", border=True)

        st.session_state.humid = new_humid
    with prec:
        new_prec = weather.precipitation
        old_prec = st.session_state.prec

        delta_p = 0 if old_prec is None else new_prec - old_prec
        st.metric("Precipitation (mm)", value=f"{new_prec} mm", delta=f"{delta_p} mm", help="Precipitation", border=True)
   
        st.session_state.prec = new_prec
    with pres:
        new_pres = weather.pressure
        old_pres = st.session_state.pres

        delta_pr = 0 if old_pres is None else new_pres - old_pres
        st.metric("Pressure (mb/hPa)", value=f"{new_pres} hPa", delta=f"{delta_pr} mb/hPa", help="Pressure", border=True, width=250)
    with coor:
        st.metric("Coordinates (x, y)", value=f"{x}, {y}", help="Coordinates", border=True)
    with pupils:
        st.metric(" Local Population", value=weather.local_population, help="Local Population", border=True)
    with feel:
        st.metric("Feels Like (How Hot/Cold We Feel)", value=weather.feels_like, help="Feels Like", border=True)
    with ws:
        new_ws = weather.wind_speed
        old_ws = st.session_state.ws

        delta_ws = 0 if old_ws is None else new_ws - old_ws
        st.metric("Wind Speed (km/h)", value=f"{new_ws} km/h", delta=f"{delta_ws} km/h", help="Wind Speed", border=True)
    
        st.session_state.ws = new_ws
    with uv:
        st.metric("Ultraviolet", value=str(weather.ultraviolet), help="Ultraviolet", border=True)

    await client.close()


asyncio.run(get_weather())

