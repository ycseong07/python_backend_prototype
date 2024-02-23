import streamlit as st
import pandas as pd
from datetime import datetime
import requests

st.title('암호화폐 대시보드 프로토타입')

# 로그아웃
logout_button_html = '<a href="http://localhost:8000/logout" target="_self">Logout</a>'

# 유저 정보 확인
user_info = st.query_params.get_all('user_info')

if user_info:
    st.session_state['user_info'] = user_info[0]

# 로그인 상태
if 'user_info' in st.session_state:
    st.success(f'Logged in as {st.session_state["user_info"]}')
    st.markdown(logout_button_html, unsafe_allow_html=True)
        
    # 사용자 행위 로그 API
    def log_user_action(user_id, action_type):
        response = requests.post("http://localhost:8000/user-action/", json={"user_id": user_id, "action_type": action_type})
        if response.status_code != 200:
            print("사용자 행위 정보를 가져오는 데 실패했습니다")
        
    if 'price_data' not in st.session_state:
        st.session_state.price_data = pd.DataFrame(columns=['market', 'trade_date', 'trade_timestamp', 'high_price', 'low_price', 'trade_price'])
    if 'latest_price' not in st.session_state:
        st.session_state.latest_price = pd.DataFrame()

    # 현재 시세 확인
    if st.button('현재 시세 확인'):
        log_user_action(user_id=st.session_state["user_info"], action_type="현재 시세 확인")
        response = requests.get("http://localhost:8000/market/coin-prices")
        if response.status_code == 200:
            data = response.json()
            price_data = pd.DataFrame(data)
            st.session_state.latest_price = price_data[['market', 'trade_date', 'trade_timestamp', 'high_price', 'low_price', 'trade_price']]
        else:
            st.session_state.latest_price = pd.DataFrame()
            st.error("가격 정보를 가져오는 데 실패했습니다.")

    # 현재 시세 확인 테이블
    st.header("암호화폐 시세")
    if not st.session_state.latest_price.empty:
        st.table(st.session_state.latest_price)

    st.header("비트코인 가격 기록")

    # BTC 정보 기록
    if st.button('BTC 정보 기록'):
        log_user_action(user_id=st.session_state["user_info"], action_type="BTC 정보 기록")
        if not st.session_state.latest_price.empty:
            btc_data = st.session_state.latest_price[st.session_state.latest_price['market'] == 'KRW-BTC']
            if not btc_data.empty:
                st.session_state.price_data = pd.concat([st.session_state.price_data, btc_data], ignore_index=True)
            else:
                st.error("KRW-BTC 정보가 없습니다.")
        else:
            st.error("현재 시세를 먼저 확인하세요.")

    # BTC 정보 기록 테이블
    st.table(st.session_state.price_data)

# 비 로그인 상태
else:
    login_button_html = '<a href="http://localhost:8000/login" target="_blank">Login with Google</a>'
    st.markdown(login_button_html, unsafe_allow_html=True)
    if not user_info:
        st.error('Not logged in or logged out')
