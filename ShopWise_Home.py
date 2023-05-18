# ShopWise.py
#---Import libraries---#
from collections import namedtuple
from streamlit_option_menu import option_menu
import altair as alt
import math
import pandas as pd
import streamlit as st
from PIL import Image
from st_aggrid import AgGrid, JsCode
from st_aggrid.grid_options_builder import GridOptionsBuilder
import streamlit as st


#---Page setup---#
st.set_page_config(page_title='ShopWise', page_icon=':bar_chart:', layout='centered')
st.title('Welcome to ShopWise')
#---------------#

st.write("Made by Group 4")
st.write("Welcome to ShopWise, your one-stop-shop for all things green and sustainable! Our app is designed to make eco-friendly shopping easier and more accessible than ever before, by wisely recommending a sustainable ammount to purchase. We understand that it can be overwhelming to navigate the world of green shopping, which is why we've curated a selection of products that meet our high standards for sustainability. With ShopWise, you can trust that every purchase you make is making a positive impact on the environment. We believe that small choices can make a big difference, and we're excited to help you make those choices every day. So join us in our mission to create a healthier planet, one shopping trip at a time. Download ShopWise today and start shopping with purpose!")

#------Start- OF video-----#
video_file = open('ShopWise Introduction.mp4', 'rb')
video_bytes = video_file.read()

st.video(video_bytes)
#-------End-------#
st.title('Guide on how to use ShopWise')

st.write("Guide for Shopping List  [link](https://scribehow.com/shared/ShopWise_shopping_list__Q-qGouGYQxSeTSAqA_okuA)")
