import streamlit as st
from anthropic import Anthropic, APIError
import requests
from bs4 import BeautifulSoup

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

def format_result(content):
    """분석 결과를 마크다운 형식으로 포맷팅하는 함수"""
    
    # content가 리스트인 경우 첫 번째 요소의 text 속성을 사용
    if isinstance(content, list) and hasattr(content[0], 'text'):
        text_content = content[0].text
    else:
        text_content = str(content)
    
    # 섹션별 이모지 매핑
    section_emojis = {
        "1": "🚀",  # 소개
        "2": "⚡",  # 프레임워크
        "3": "🔧",  # 핵심기능
        "4": "🤖",  # AI 모델
        "5": "💰",  # 가격정책
    }
    
    # 헤더 부분
    formatted_text = """
# 📊 분석 결과 📊

## 🎯 ★★내용 요약 (핵심 포인트 5개)★★ 🎯

"""
    
    # 텍스트를 섹션으로 분리하고 마크다운 형식으로 변환
    sections = text_content.split('\n\n')
    
    for section in sections:
        if not section.strip():
            continue
        
        # 섹션 번호 추출
        section_num = section[0]
        emoji = section_emojis.get(section_num, "✨")
        
        # 부제목과 내용 분리
        lines = section.split('\n')
        title = lines[0]
        contents = lines[1:] if len(lines) > 1 else []
        
        # 섹션 제목 추가
        formatted_text += f"### {emoji} {title}\n\n"
        
        # 내용을 리스트 아이템으로 포맷팅
        for item in contents:
            if item.strip():
                if item.startswith('-'):
                    item = item[1:].strip()
                formatted_text += f"* 💫 {item}\n"
        
        formatted_text += "\n"
    
    # 푸터 추가
    formatted_text += "\n---\n*✨ Powered by Claude AI ✨*\n"
    
    return formatted_text

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
                        # 마크다운으로 렌더링
                        st.markdown(format_result(summary))
                    else:
                        st.error(summary)
                except Exception as e:
                    st.error(f"처리 중 오류가 발생했습니다: {str(e)}")

if __name__ == "__main__":
    main()
