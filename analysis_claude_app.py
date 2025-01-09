import streamlit as st
from anthropic import Anthropic
import requests
from bs4 import BeautifulSoup
import os

st.set_page_config(page_title="웹페이지 분석 도구", page_icon="📊", layout="wide")

# CSS 스타일 적용
st.markdown("""
    <style>
    .main {
        padding: 20px;
        font-family: 'Nanum Gothic', sans-serif;
    }
    .result-container {
        line-height: 1.8;
        padding: 20px;
        background-color: white;
        border-radius: 10px;
        margin: 20px 0;
    }
    .stButton > button {
        width: 100%;
        margin-top: 10px;
    }
    </style>
""", unsafe_allow_html=True)

def analyze_webpage(url):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()  # Raises an HTTPError for bad responses
        soup = BeautifulSoup(response.text, 'html.parser')
        
        title = soup.title.string if soup.title else "제목 없음"
        paragraphs = soup.find_all('p')
        content = ' '.join([p.text for p in paragraphs])
        
        if len(content) > 1500:
            content = content[:1500] + "..."
            
        return True, title, content
    except Exception as e:
        return False, None, f"에러 발생: {str(e)}"

def summarize_text(api_key, text):
    try:
        # Anthropic 클라이언트 초기화 - 기본 설정 사용
        anthropic = Anthropic(
            api_key=api_key,
            base_url="https://api.anthropic.com",
        )
        
        message = anthropic.messages.create(
            model="claude-3-5-sonnet-20240620",
            max_tokens=1000,
            temperature=0.7,
            messages=[{
                "role": "user",
                "content": f"다음 웹 페이지 내용을 분석하고 아래 형식으로 요약해주세요:\n\n{text}\n\n"
                          f"1. CodeAI Studio Pro 소개와 주요 특징\n"
                          f"2. 지원하는 프레임워크와 기술 스택\n"
                          f"3. 핵심 기능과 개발 워크플로우\n"
                          f"4. AI 모델 통합과 지원\n"
                          f"5. 가격 정책과 제공 플랜"
            }]
        )
        return True, message.content
    except Exception as e:
        return False, f"요약 중 에러 발생: {str(e)}"

def format_result(content):
    return f"""
    <div class="result-container">
        <h1 style="text-align: center; margin-bottom: 30px;">
            📊 분석 결과 📊
        </h1>
        
        <div style="margin-bottom: 20px;">
            🎯 ★★내용 요약 (핵심 포인트 5개):★★
        </div>
        
        <ol style="list-style-type: none; padding-left: 0;">
            <li style="margin-bottom: 15px;">
                1. 🚀 ★★CodeAI Studio Pro 소개★★: {content}
            </li>
        </ol>
    </div>
    """

def main():
    st.title("웹페이지 분석 및 요약 도구")
    
    with st.container():
        # API 키 입력
        api_key = st.text_input("Anthropic API 키를 입력하세요", type="password")
        
        # 입력 방식 선택
        input_method = st.radio("입력 방식 선택:", ["URL", "텍스트"])
        
        url = None
        text = None
        
        if input_method == "URL":
            url = st.text_input("분석할 웹페이지 URL을 입력하세요")
        else:
            text = st.text_area("분석할 텍스트를 입력하세요")
        
        # 분석 시작 버튼 - 항상 표시
        if st.button("분석 시작", key="analyze_btn"):
            if not api_key:
                st.error("API 키를 입력해주세요.")
                return
                
            with st.spinner("분석 중..."):
                if input_method == "URL" and url:
                    success, title, content = analyze_webpage(url)
                    if success:
                        success, summary = summarize_text(api_key, content)
                        if success:
                            st.markdown(format_result(summary), unsafe_allow_html=True)
                        else:
                            st.error(summary)
                    else:
                        st.error(content)
                elif input_method == "텍스트" and text:
                    success, summary = summarize_text(api_key, text)
                    if success:
                        st.markdown(format_result(summary), unsafe_allow_html=True)
                    else:
                        st.error(summary)
                else:
                    st.warning("분석할 내용을 입력해주세요.")

if __name__ == "__main__":
    main()
