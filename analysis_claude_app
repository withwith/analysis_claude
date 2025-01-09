import streamlit as st
from anthropic import Anthropic
import requests
from bs4 import BeautifulSoup
import json

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
    </style>
""", unsafe_allow_html=True)

def analyze_webpage(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        title = soup.title.string if soup.title else "제목 없음"
        paragraphs = soup.find_all('p')
        content = ' '.join([p.text for p in paragraphs])
        
        if len(content) > 1500:
            content = content[:1500] + "..."
            
        return title, content
    except Exception as e:
        return None, f"에러 발생: {str(e)}"

def summarize_text(api_key, text):
    anthropic = Anthropic(api_key=api_key)
    
    try:
        message = anthropic.messages.create(
            model="claude-3-5-sonnet-20240620",
            max_tokens=1000,
            temperature=0.7,
            messages=[{
                "role": "user",
                "content": f"다음 웹 페이지 내용을 분석하고 아래 형식으로 요약해주세요:\n\n{text}\n\n"
                          f"1. CodeAI Studio Pro 소개\n"
                          f"2. 지원 프레임워크\n"
                          f"3. 기능\n"
                          f"4. AI 모델 액세스\n"
                          f"5. 가격 정책"
            }]
        )
        return message.content
    except Exception as e:
        return f"요약 중 에러 발생: {str(e)}"

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
            {content}
        </ol>
    </div>
    """

def main():
    st.title("웹페이지 분석 및 요약 도구")
    
    # API 키 입력
    api_key = st.text_input("Anthropic API 키를 입력하세요", type="password")
    
    # 입력 방식 선택
    input_method = st.radio("입력 방식 선택:", ["URL", "텍스트"])
    
    if input_method == "URL":
        url = st.text_input("분석할 웹페이지 URL을 입력하세요")
        if url:
            if st.button("분석 시작"):
                with st.spinner("웹페이지 분석 중..."):
                    title, content = analyze_webpage(url)
                    if title is not None:
                        summary = summarize_text(api_key, content)
                        st.markdown(format_result(summary), unsafe_allow_html=True)
                    else:
                        st.error(content)
    else:
        text = st.text_area("분석할 텍스트를 입력하세요")
        if text:
            if st.button("분석 시작"):
                with st.spinner("텍스트 분석 중..."):
                    summary = summarize_text(api_key, text)
                    st.markdown(format_result(summary), unsafe_allow_html=True)

if __name__ == "__main__":
    main()
