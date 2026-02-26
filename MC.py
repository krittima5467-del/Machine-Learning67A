# -*- coding: utf-8 -*-
"""
Created on Thu Feb 19 15:58:18 2026
@author: BusRmutt
"""

import pickle
from streamlit_option_menu import option_menu
import streamlit as st

# ================== LOAD MODELS ==================
used_car_model = pickle.load(open('Used_cars_model.sav','rb'))
riding_model = pickle.load(open('RidingMowers_model.sav','rb'))
bmi_model = pickle.load(open('bmi_model.sav','rb'))

# ================== MAPPING ==================
fuel_map = {'Diesel': 0, 'Electric': 1, 'Petrol': 2}
engine_map = {'800': 0, '1000': 1, '1200': 2, '1500': 3, '1800': 4, '2000': 5, '2500': 6, '3000': 7, '4000': 8, '5000': 9}
brand_map = {'BMW': 0, 'Chevrolet': 1, 'Ford': 2, 'Honda': 3, 'Hyundai': 4, 'Kia': 5, 'Nissan': 6, 'Tesla': 7, 'Toyota': 8, 'Volkswagen': 9}
transmission_map = {'Automatic': 0, 'Manual': 1}
gender_map = {'Male': 0, 'Female': 1}

# ================== BMI DETAILS ==================
bmi_index_details = {
    0: "Extremely Weak (ผอมมาก)",
    1: "Weak (ผอม/น้ำหนักน้อย)",
    2: "Normal (น้ำหนักปกติ)",
    3: "Overweight (น้ำหนักเกิน)",
    4: "Obesity (โรคอ้วน)",
    5: "Extreme Obesity (โรคอ้วนอันตราย)"
}

bmi_advice = {
    0: "ควรเพิ่มโปรตีนและพลังงาน เช่น ไข่ นม ถั่ว และออกกำลังกายแบบเวทเทรนนิ่ง",
    1: "ควรรับประทานอาหารให้ครบ 5 หมู่ และเพิ่มมื้ออาหาร",
    2: "รักษาสมดุลอาหาร ออกกำลังกายสม่ำเสมอ และพักผ่อนให้เพียงพอ",
    3: "ควรลดของหวาน ของมัน เพิ่มผักผลไม้ และออกกำลังกาย 3-5 วัน/สัปดาห์",
    4: "ควรควบคุมอาหารอย่างจริงจัง และปรึกษาแพทย์หรือนักโภชนาการ",
    5: "ควรพบแพทย์เพื่อตรวจสุขภาพและวางแผนลดน้ำหนักอย่างปลอดภัย"
}

# ================== SIDEBAR ==================
with st.sidebar:
    selected = option_menu('Prediction', ['Ridingmower', 'Used_cars', 'bmi'])

# ================== BMI SECTION ==================
if selected == 'bmi':
    st.title('BMI Prediction')

    gender = st.selectbox('เลือกเพศ', list(gender_map.keys()))
    height = st.text_input('ส่วนสูง (cm)')
    weight = st.text_input('น้ำหนัก (kg)')

    if st.button('ทำนายผล BMI'):
        try:
            prediction = bmi_model.predict([[
                gender_map[gender],
                float(height),
                float(weight)
            ]])

            result_index = int(prediction[0])
            description = bmi_index_details.get(result_index, "ไม่ทราบผลลัพธ์")
            advice = bmi_advice.get(result_index, "")

            # --------- กำหนดสีตามระดับความเสี่ยง ---------
            if result_index == 2:
                st.success(f'ผลการวิเคราะห์: {description}')
            elif result_index in [3]:
                st.warning(f'ผลการวิเคราะห์: {description}')
            elif result_index in [0,1]:
                st.warning(f'ผลการวิเคราะห์: {description}')
            else:
                st.error(f'ผลการวิเคราะห์: {description}')

            st.info(f'คำแนะนำ: {advice}')

        except:
            st.error("กรุณากรอกข้อมูลให้ถูกต้อง")

# ================== RIDING MOWER ==================
if selected == 'Ridingmower':
    st.title('Riding Mower Classification')
    Income = st.text_input('รายได้ (Income)')
    LotSize = st.text_input('ขนาดพื้นที่ (LotSize)')
    if st.button('ทำนายผล'):
        prediction = riding_model.predict([[float(Income), float(LotSize)]])
        res_text = 'เป็นเจ้าของ (Owner)' if prediction[0] == 1 else 'ไม่ได้เป็นเจ้าของ (Non Owner)'
        st.success(f'ผลลัพธ์: {res_text}')

# ================== USED CARS ==================
if selected == 'Used_cars':
    st.title('ประเมินราคารถมือ 2')

    make_year = st.text_input('ปีที่ผลิต')
    mileage_kmpl = st.text_input('อัตราสิ้นเปลือง (KM/L)')
    engine_cc = st.selectbox('ขนาดเครื่องยนต์ (CC)', list(engine_map.keys()))
    fuel_type = st.selectbox('ประเภทน้ำมัน', list(fuel_map.keys()))
    owner_count = st.text_input('จำนวนเจ้าของเดิม')
    brand = st.selectbox('ยี่ห้อรถ', list(brand_map.keys()))
    transmission = st.selectbox('ประเภทเกียร์', list(transmission_map.keys()))
    accidents_reported = st.text_input('จำนวนอุบัติเหตุ')

    if st.button('ประเมินราคา'):
        price = used_car_model.predict([[
            float(make_year), float(mileage_kmpl),
            engine_map[engine_cc],
            fuel_map[fuel_type],
            float(owner_count),
            brand_map[brand],
            transmission_map[transmission],
            float(accidents_reported)
        ]])

        st.success(f'ราคาประเมินคือ: {round(price[0], 2)} บาท')
 


