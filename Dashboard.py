import streamlit as st
import plotly.express as px
import pandas as pd
from PIL import Image
import datetime
import warnings
warnings.filterwarnings('ignore')

st.set_page_config(page_title="Dashboard!!!", page_icon=":bar_chart:", layout="wide")


# reading the data from excel file
df = pd.read_csv("datosa.csv", encoding="ISO-8859-1", sep=";")

st.markdown('<style>div.block-container{padding-top:1rem;}</style>', unsafe_allow_html=True)

print(df.columns)
col1, col2 = st.columns([0.1,0.9])


image = Image.open('terramaz.png')
col1, col2 = st.columns(2) 
with col1:
    st.image(image,width=230)

html_title = """
    <style>
    .title-test {
    font-weight:bold;
    padding:5px;
    border-radius:6px;
    }
    </style>
    <center><h1 class="title-test">Indicadores de la Marca</h1></center>"""
with col2:
    st.markdown(html_title, unsafe_allow_html=True)

col3, col4, col5 = st.columns([0.1,0.45,0.45])
with col3:
    box_date = str(datetime.datetime.now().strftime("%d %B %Y"))
    st.write(f"Última actualización:  \n {box_date}")
# Convierte la primera columna a datetime

df["Año"] = pd.to_datetime(df["Año"], format="%Y")


# Obtén el año mínimo y máximo
año_minimo = df["Año"].min()
año_maximo = df["Año"].max()

# Ordena la lista de años
#años_ordenados = sorted(df["Año"].unique())

st.sidebar.header("Elige tu Filtro: ")
# Create for Region

año = st.sidebar.multiselect("Seleccione el año", df["Año"].unique())
if año is None:
    cultivo = ["Todos"]
else:
    df2 = df.copy()

# Create for State
cultivo = st.sidebar.multiselect("Seleccione el Cultivo", df2["Cultivo"].unique())
if cultivo is None:
    cultivo = ["Todos"]
else:
    df3 = df2.copy()

# Create df3
df3 = df.copy()

# Si año es un valor escalar, conviértelo en una lista de un solo elemento
if isinstance(año, (int, float, str)):
    año = [año]

filtered_df = df[(df["Cultivo"].isin(cultivo)) & (df["Año"].isin(año))]

# Calcular la producción por cultivo
category_df = filtered_df.groupby(by=["Cultivo", "Año"]).agg(Produccion=("Produccion", "sum"))


# Modificar el texto del gráfico para que indique "Produccion(t)" en lugar de "Sales".
category_df = category_df.reset_index()
category_df.columns = ["Cultivo", "Año", "Produccion"]

# Mostrar el gráfico de producción por cultivo
with col1:
    st.subheader("Cultivo vs Produccion (t)")
    ffig = px.bar(category_df, x="Cultivo", y="Produccion", text="Año", template="seaborn")
    st.plotly_chart(ffig, use_container_width=True, height=200)

with col2:
    st.subheader("Año vs Produccion (t)")
    fig = px.pie(filtered_df, values = "Produccion", names = "Año", hole = 0.5)
    fig.update_traces(text = filtered_df["Año"], textposition = "outside")
    st.plotly_chart(fig,use_container_width=True)

_, view1, dwn1, view2, dwn2 = st.columns([0.15,0.20,0.20,0.20,0.20])

with dwn1:
    st.download_button("Get Data", data = category_df.to_csv().encode("utf-8"),
                       file_name="RetailerSales.csv", mime="text/csv")
