# app.py
import streamlit as st
from anthropic import Anthropic, APIError
import requests
from bs4 import BeautifulSoup
from config import setup_page
from formatter import format_result

def analyze_webpage(url):
    """웹페이지 내용을 가져오고 분석하는 함수"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        title = soup.title.string if soup.title else "제목 없음"
        paragraphs = soup.find_all('p')
        content = ' '.join([p.text for p in paragraphs])
        
        if len(content) > 1500:
            content = content[:1500] + "..."
            
        return True, title, content
    except requests.RequestException as e:
        return False, None, f"웹페이지 접근 중 오류 발생: {str(e)}"
    except Exception as e:
        return False, None, f"예상치 못한 오류 발생: {str(e)}"

def create_anthropic_client(api_key):
    """Anthropic 클라이언트를 생성하는 함수"""
    try:
        return Anthropic(api_key=api_key)
    except Exception as e:
        raise Exception(f"API 클라이언트 초기화 오류: {str(e)}")

def summarize_text(api_key, text):
    """텍스트를 요약하는 함수"""
    try:
        # API 클라이언트 생성
        client = create_anthropic_client(api_key)
        
        # 메시지 생성
        response = client.messages.create(
            model="claude-3-sonnet-20240229",
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
        return True, response.content
    except APIError as e:
        return False, f"API 오류: {str(e)}"
    except Exception as e:
        return False, f"요약 중 오류 발생: {str(e)}"

def main():
    setup_page()
    st.title("웹페이지 분석 및 요약 도구")
    
    with st.container():
        # API 키 입력
        api_key = st.text_input("Anthropic API 키를 입력하세요", type="password")
        
        # 입력 방식 선택
        input_method = st.radio("입력 방식 선택:", ["URL", "텍스트"])
        
        # 입력 필드
        if input_method == "URL":
            user_input = st.text_input("분석할 웹페이지 URL을 입력하세요")
        else:
            user_input = st.text_area("분석할 텍스트를 입력하세요")
        
        # 분석 시작 버튼
        if st.button("분석 시작", key="analyze_btn"):
            if not api_key:
                st.error("API 키를 입력해주세요.")
                return
            
            if not user_input:
                st.warning("분석할 내용을 입력해주세요.")
                return
                
            with st.spinner("분석 중..."):
                try:
                    if input_method == "URL":
                        success, title, content = analyze_webpage(user_input)
                        if not success:
                            st.error(content)
                            return
                    else:
                        content = user_input
                    
                    success, summary = summarize_text(api_key, content)
                    if success:
                        # HTML 대신 마크다운으로 렌더링
                        st.markdown(format_result(summary))
                    else:
                        st.error(summary)
                except Exception as e:
                    st.error(f"처리 중 오류가 발생했습니다: {str(e)}")

if __name__ == "__main__":
    main()
