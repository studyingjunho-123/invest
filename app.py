import streamlit as st
from openai import OpenAI

# 🔐 비밀번호 설정
PASSWORD = "7856"

password = st.text_input("비밀번호 입력", type="password")

if password != PASSWORD:
    st.warning("비밀번호를 입력하세요.")
    st.stop()

# 🤖 OpenAI 연결
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

st.title("📈 AI 투자 리포트 생성기")

issue = st.text_area("경제 이슈 입력")
stocks = st.text_input("관련 종목 입력")
period = st.selectbox("투자 기간", ["단기", "중기", "장기"])

if st.button("리포트 생성"):
    prompt = f"""
    너는 투자 리서치 보조 AI야.

    경제 이슈: {issue}
    관련 종목: {stocks}
    투자 기간: {period}

    다음 형식으로 리포트 작성:
    1. 핵심 이슈 요약
    2. 시장 영향
    3. 업종 영향
    4. 종목별 영향
    5. 리스크
    6. 결론

    확정적인 매수/매도 추천은 하지 말고 근거 중심으로 작성해.
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": prompt}
        ],
    )

    st.write(response.choices[0].message.content)
