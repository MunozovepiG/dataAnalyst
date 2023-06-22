import pandas as pd
import streamlit as st 
import plotly.express as px 
from PIL import Image

dataset= pd.read_excel('egg.xlsx', sheet_name="Sheet1", usecols='A:C',
                        header=1)

dataSegment = pd.read_excel('egg.xlsx', sheet_name="Sheet1", usecols='E:F',
                        header=2)

st.set_page_config(page_title='Start', layout='wide')

dataSegment.dropna(inplace=True)

st.dataframe(dataset)
st.dataframe(dataSegment)

pie_chart = px.pie(dataSegment, title='Happy', values='Par', names='Dep')

image = Image.open('images/download.jpeg')

st.plotly_chart(pie_chart)

st.image(image, caption="Image captured", use_column_width=True)


## strealit selection 

department = dataset["Dept"].unique().tolist()
ages = dataset["Ag"].unique().tolist()

age_selection = st.slider('Age:', min_value=min(ages), max_value=max(ages), value=(min(ages), max(ages)) )

depatment_selection = st.multiselect('Dept:', department, default=department )


###the filter 

mask = (dataset['Ag'].between(*age_selection)) & (dataset['Dept'].isin(depatment_selection))
number_of_result = dataset[mask].shape[0]

st.markdown(f'*Avilable Results: {number_of_result}*')

## group the dataframe

dataset_grouped = dataset[mask].groupby(by=['Rate ']).count()[['Ag']]
dataset_grouped = dataset_grouped.rename(columns={'Rate': 'Ag'})
dataset_grouped = dataset_grouped.reset_index()


# -- plot bar chart 

bar_chart = px.bar(dataset_grouped,
                   x='Rate ',
                   y='Ag',
                   color_discrete_sequence= ['#f63366']*len(dataset_grouped),
                   template='plotly_white')

st.plotly_chart(bar_chart)
