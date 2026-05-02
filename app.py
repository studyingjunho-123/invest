import streamlit as st

st.title("📈 투자 리포트 프롬프트 생성기")

issue = st.text_area("경제 이슈 입력", placeholder="예: 미국 금리 인하 가능성 증가")
stocks = st.text_input("관련 종목 입력", placeholder="예: 삼성전자, 엔비디아")
period = st.selectbox("투자 기간", ["단기", "중기", "장기"])
style = st.selectbox("리포트 스타일", ["간단 요약", "자세한 분석", "고등학생 이해용"])

if st.button("프롬프트 생성"):
    prompt = f"""
너는 투자 리서치 보조 AI야.
아래 경제 이슈를 바탕으로 투자 리포트를 작성해줘.

[입력 정보]
경제 이슈: {issue}
관련 종목: {stocks}
투자 기간: {period}
리포트 스타일: {style}

[작성 조건]
- 확정적인 매수/매도 추천은 하지 말 것
- 근거와 리스크를 함께 제시할 것
- 검증되지 않은 소문처럼 보이는 내용은 단정하지 말 것
- 경제 이슈가 주식시장에 영향을 주는 경로를 설명할 것
- 관련 종목이 왜 영향을 받을 수 있는지 구체적으로 설명할 것

[리포트 형식]
1. 핵심 이슈 요약
2. 시장 전체 영향
3. 관련 업종 영향
4. 관련 종목별 영향
5. 체크해야 할 지표
6. 리스크
7. 최종 판단
8. 추가로 확인하면 좋은 자료
"""

    st.subheader("복사해서 ChatGPT에 붙여넣을 프롬프트")
    st.code(prompt, language="text")