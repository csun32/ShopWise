#ShopWise.py
#---Import libraries---#
from google.oauth2 import service_account                      #pip install google-auth
from gspread_pandas import Spread,Client                       #pip install gspread_pandas
import pandas as pd                                            #pip install pandas
import streamlit as st                                         #pip install streamlit
from streamlit_option_menu import option_menu
import gspread                                                 #pip install gspread
from st_aggrid import AgGrid, GridUpdateMode, JsCode           #pip install streamlit-aggrid
from st_aggrid.grid_options_builder import GridOptionsBuilder
import plotly.express as px                                     #pip install plotly-express
from datetime import datetime, date


@st.cache_data()
def load_the_spreadsheet(tabname):
    # --- Create a Google Authentication connection objectt --- #
    scope = ['https://spreadsheets.google.com/feeds',
             'https://www.googleapis.com/auth/drive']
    credentials = service_account.Credentials.from_service_account_info(
                    st.secrets["gcp_service_account"], scopes = scope)

    client = Client(scope=scope,creds=credentials)
    spreadsheetname = "ShopWise Food List"                #spreadsheet name
    #spread = Spread(spreadsheetname,client = client)      #load ShopWise Food List google sheet
    # --- Call the spreadshet --- #
    sh = client.open(spreadsheetname)                     #load ShopWise Food List google sheet
    #worksheet_list = sh.worksheets()                      # list of ALL worksheets in the google sheet <Worksheet 'Shopping_List2' id:986753546>...
    worksheet = sh.worksheet(tabname)
    df = pd.DataFrame(worksheet.get_all_records())
    return df
df=load_the_spreadsheet("Pantry")
df_c=df.query('Status == "Completed"')

#get all avaliable food items from master list for drop down features
sheet_id = "1X5ANn3c5UKfpc-P20sMRLJhHggeSaclVfXavdfv-X1c"
fd_list_sheet = "Food_List_Master"
fd_list_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={fd_list_sheet}"
fd_list = pd.read_csv(fd_list_url, usecols = ['Name','Category','CO2_Per_g'])

#Merging df
df_c2= df_c.merge(fd_list,
                  left_on= 'Item',
                  right_on= 'Name',
                  how = 'left')
 
df_c2['Emission']= df_c2['Wasted'] * df_c2['CO2_Per_g']


#st.write(df.dtypes) #to check data type
#df_c2["Purchase_Date"] = pd.to_datetime(df["Purchase_Date"])               #change to datetime
#df_c2["P_Month"] = df_c2["Purchase_Date"].dt.month                            #new column to extract month
#df_c2["p_Year"] = df_c2["Purchase_Date"].dt.year                           #new column to extract month

#year to date parameter
ytd_start_date = date(date.today().year, 1, 1)
ytd_end_date = date.today()
#ytd_flit=(df['Purchase_Date'] > ytd_start_date) & (df['Purchase_Date'] <= ytd_end_date)


# ---- SIDEBAR ----
st.sidebar.header("Please Filter Here:")
status = st.sidebar.multiselect(
    "Select your grocery status:",
    options=df_c2["Status"].unique(),
    default=df_c2["Status"].unique()               #prepopulate all status
)

df_selection = df_c2.query(
    "Status == @status"
)

#adding new columns


st.title(':bar_chart: Here are your grocery stats') #Page Title
st.markdown("##")
total_waste = int(df_selection['Wasted'].sum())
total_emission = int(df_selection['Emission'].sum())
left_column, right_column = st.columns(2)

with left_column:
    st.subheader(f"Total Waste: {total_waste:,} g")
with right_column:
    st.subheader(f"Total Emissions: {total_emission:,} gCO2eq")
    
st.markdown("""---""")

st.dataframe(df_selection)

 #---visualization---#

emis_by_cat = (
    df_selection.groupby(by=["Category"]).sum()[["Emission"]].sort_values(by="Emission")
)
fig_emis_by_cat = px.bar(
    emis_by_cat,
    x="Emission",
    y=emis_by_cat.index,
    orientation="h",
    title="<b>Waste Emission by Category</b>",
    color_discrete_sequence=["#0083B8"] * len(emis_by_cat),
    template="plotly_white",
)
fig_emis_by_cat.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=(dict(showgrid=False))
)
#left_column, right_column = st.columns(2)
#left_column.plotly_chart(fig_emis_by_cat, use_container_width=True)
st.plotly_chart(fig_emis_by_cat, use_container_width=True)
#right_column.plotly_chart(fig_product_sales, use_container_width=True)


