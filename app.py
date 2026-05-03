import streamlit as st
from openai import OpenAI

st.set_page_config(page_title="AI 투자 리포트 생성기", page_icon="📈")

# 🔐 비밀번호
PASSWORD = "7856"  # 원하는 비밀번호로 바꾸기

st.title("📈 AI 투자 리포트 생성기")

password = st.text_input("비밀번호 입력", type="password")

if password != PASSWORD:
    st.warning("비밀번호를 입력하세요.")
    st.stop()

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

st.divider()

# 📌 오늘 경제 이슈
st.subheader("🌅 오늘 경제 이슈 확인")

if st.button("오늘 주요 경제 이슈 보기"):
    with st.spinner("오늘 경제 이슈 확인 중..."):
        response = client.responses.create(
            model="gpt-4o-mini",
            tools=[{"type": "web_search"}],
            input="""
오늘 기준 주요 경제 이슈를 5개 이내로 정리해줘.
각 이슈마다 다음 형식으로 써줘.

1. 이슈 제목
- 핵심 내용
- 시장에 미칠 수 있는 영향
- 관련해서 확인할 지표

주의:
- 확인되지 않은 루머는 단정하지 말 것
- 투자 추천처럼 쓰지 말 것
- 한국 시장과 미국 시장 영향을 구분해서 설명할 것
"""
        )

        st.write(response.output_text)

st.divider()

# 📊 투자 리포트 생성
st.subheader("📊 경제 이슈 기반 투자 리포트")

issue = st.text_area("경제 이슈 입력", placeholder="예: 미국 금리 인하 가능성 증가")
stocks = st.text_input("관련 종목 입력", placeholder="예: 삼성전자, SK하이닉스")
period = st.selectbox("투자 기간", ["단기", "중기", "장기"])
style = st.selectbox("리포트 스타일", ["간단 요약", "자세한 분석", "고등학생 이해용"])

if st.button("리포트 생성"):
    if not issue.strip():
        st.error("경제 이슈를 입력해줘.")
    else:
        with st.spinner("AI가 리포트 작성 중..."):
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
- 마지막에는 “추가로 확인해야 할 자료”를 제시할 것

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

            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "user", "content": prompt}
                ],
            )

            st.write(response.choices[0].message.content)
