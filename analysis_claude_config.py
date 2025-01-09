# config.py
import streamlit as st

def setup_page():
    """페이지 기본 설정을 수행하는 함수"""
    # 페이지 설정
    st.set_page_config(page_title="웹페이지 분석 도구", page_icon="📊", layout="wide")

    # 기본 스타일링
    st.markdown("""
        <style>
        .main {
            padding: 20px;
            font-family: 'Nanum Gothic', sans-serif;
        }
        </style>
    """, unsafe_allow_html=True)