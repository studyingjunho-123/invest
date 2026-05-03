import streamlit as st
from openai import OpenAI
import yfinance as yf

st.set_page_config(page_title="AI 투자 리서치 터미널", page_icon="📈")

PASSWORD = "7856"  # 원하는 비밀번호로 변경

st.title("📈 AI 투자 리서치 터미널")

password = st.text_input("비밀번호 입력", type="password")

if password != PASSWORD:
    st.warning("비밀번호를 입력하세요.")
    st.stop()

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

menu = st.radio(
    "기능 선택",
    ["1. 오늘 경제 이슈 분석", "2. 투자 리포트 제작", "3. 개인 종목 주가 데이터"],
)

# 1번
if menu == "1. 오늘 경제 이슈 분석":
    st.subheader("🌅 오늘 경제 이슈 분석")

    if st.button("오늘 주요 경제 이슈 보기"):
        with st.spinner("경제 이슈 확인 중..."):
            response = client.responses.create(
                model="gpt-4o-mini",
                tools=[{"type": "web_search"}],
                input="""
오늘 기준 주요 경제 이슈를 5개 이내로 정리해줘.

형식:
1. 이슈 제목
- 핵심 내용
- 한국 시장 영향
- 미국 시장 영향
- 확인할 지표

주의:
- 확인되지 않은 루머는 단정하지 말 것
- 투자 추천처럼 쓰지 말 것
"""
            )
            st.write(response.output_text)

# 2번
elif menu == "2. 투자 리포트 제작":
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
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[{"role": "user", "content": prompt}],
                )
                st.write(response.choices[0].message.content)

# 3번
elif menu == "3. 개인 종목 주가 데이터":
    st.subheader("📈 개인 종목 주가 데이터")

    ticker = st.text_input(
        "종목 코드 입력",
        placeholder="예: 삼성전자 005930.KS / SK하이닉스 000660.KS / 엔비디아 NVDA",
    )

    period = st.selectbox("조회 기간", ["1mo", "3mo", "6mo", "1y", "5y"])

    if st.button("주가 데이터 조회"):
        if not ticker.strip():
            st.error("종목 코드를 입력해줘.")
        else:
            with st.spinner("주가 데이터 불러오는 중..."):
                data = yf.download(ticker, period=period)

                if data.empty:
                    st.error("데이터를 불러오지 못했어. 종목 코드를 다시 확인해줘.")
                else:
                    st.write(f"### {ticker} 주가 차트")
                    st.line_chart(data["Close"])

                    first_price = float(data["Close"].iloc[0])
                    last_price = float(data["Close"].iloc[-1])
                    high_price = float(data["Close"].max())

                    return_rate = (last_price - first_price) / first_price * 100
                    drawdown = (last_price - high_price) / high_price * 100

                    st.write("### 핵심 지표")
                    st.write(f"- 기간 첫 종가: {first_price:.2f}")
                    st.write(f"- 최근 종가: {last_price:.2f}")
                    st.write(f"- 기간 수익률: {return_rate:.2f}%")
                    st.write(f"- 고점 대비 하락률: {drawdown:.2f}%")

                    if st.button("이 주가 흐름 AI 해석"):
                        prompt = f"""
다음 종목의 주가 흐름을 투자 리서치 관점에서 해석해줘.

종목 코드: {ticker}
조회 기간: {period}
기간 첫 종가: {first_price:.2f}
최근 종가: {last_price:.2f}
기간 수익률: {return_rate:.2f}%
고점 대비 하락률: {drawdown:.2f}%

형식:
1. 주가 흐름 요약
2. 상승/하락 가능 원인
3. 확인해야 할 경제 지표
4. 투자 리스크
5. 최종 해석

단, 확정적인 매수/매도 추천은 하지 마.
"""
                        response = client.chat.completions.create(
                            model="gpt-4o-mini",
                            messages=[{"role": "user", "content": prompt}],
                        )
                        st.write(response.choices[0].message.content)
