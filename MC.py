# -*- coding: utf-8 -*-
"""
Created on Thu Feb 19 15:58:18 2026
@author: BusRmutt
"""

import pickle
from streamlit_option_menu import option_menu
import streamlit as st

# โหลดโมเดล
used_car_model = pickle.load(open('Used_cars_model.sav','rb'))
riding_model = pickle.load(open('RidingMowers_model.sav','rb'))
bmi_model = pickle.load(open('bmi_model.sav','rb'))

# ================== MAP ==================

fuel_map = {
    'Diesel': 0,
    'Electric': 1,
    'Petrol': 2
}

engine_map = {
    '800': 0,
    '1000': 1,
    '1200': 2,
    '1500': 3,
    '1800': 4,
    '2000': 5,
    '2500': 6,
    '3000': 7,
    '4000': 8,
    '5000': 9
}

brand_map = {
    'BMW': 0,
    'Chevrolet': 1,
    'Ford': 2,
    'Honda': 3,
    'Hyundai': 4,
    'Kia': 5,
    'Nissan': 6,
    'Tesla': 7,
    'Toyota': 8,
    'Volkswagen': 9
}

transmission_map = {
    'Automatic': 0,
    'Manual': 1
}

# ================== MENU ==================

with st.sidebar:
    selected = option_menu(
        'Menu',
        ['BMI', 'Ridingmower', 'Used_cars']
    )

# ================== BMI ==================

if selected == 'BMI':
    st.title('BMI Classification')

    Income = st.text_input('Income')
    LotSize = st.text_input('LotSize')

    if st.button('Predict BMI'):
        try:
            prediction = bmi_model.predict([[float(Income), float(LotSize)]])
            if prediction[0] == 1:
                result = 'Owner'
            else:
                result = 'Non Owner'
            st.success(result)
        except:
            st.error("กรุณากรอกตัวเลขให้ครบ")

# ================== RIDING MOWER ==================

elif selected == 'Ridingmower':
    st.title('Riding Mower Classification')

    Income = st.text_input('Income')
    LotSize = st.text_input('LotSize')

    if st.button('Predict Riding'):
        try:
            prediction = riding_model.predict([[float(Income), float(LotSize)]])
            if prediction[0] == 1:
                result = 'Owner'
            else:
                result = 'Non Owner'
            st.success(result)
        except:
            st.error("กรุณากรอกตัวเลขให้ครบ")

# ================== USED CARS ==================

elif selected == 'Used_cars':
    st.title('ประเมินราคารถมือ 2')

    make_year = st.text_input('ปีที่ผลิต')
    mileage_kmpl = st.text_input('กินน้ำมันกี่ KM/L')
    engine_cc = st.selectbox('ขนาดเครื่องยนต์ (CC)', list(engine_map.keys()))
    fuel_type = st.selectbox('ประเภทน้ำมัน', list(fuel_map.keys()))
    owner_count = st.text_input('จำนวนเจ้าของเดิม')
    brand = st.selectbox('ยี่ห้อรถ', list(brand_map.keys()))
    transmission = st.selectbox('ประเภทเกียร์', list(transmission_map.keys()))
    accidents_reported = st.text_input('จำนวนอุบัติเหตุที่เคยเกิด')

    if st.button('Predict Price'):
        try:
            prediction = used_car_model.predict([[
                float(make_year),
                float(mileage_kmpl),
                engine_map[engine_cc],
                fuel_map[fuel_type],
                float(owner_count),
                brand_map[brand],
                transmission_map[transmission],
                float(accidents_reported)
            ]])

            price = round(prediction[0], 2)
            st.success(f"ราคาประเมิน: {price:,.2f} บาท")

        except:
            st.error("กรุณากรอกข้อมูลให้ถูกต้อง")



