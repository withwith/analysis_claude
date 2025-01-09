# formatter.py
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