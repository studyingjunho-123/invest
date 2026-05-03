import streamlit as st
from openai import OpenAI
import yfinance as yf
from datetime import datetime

st.set_page_config(page_title="AI 투자 리서치 터미널", page_icon="📈")

PASSWORD = "7856"  # 원하는 비밀번호로 바꾸기

st.title("📈 AI 투자 리서치 터미널")

password = st.text_input("비밀번호 입력", type="password")

if password != PASSWORD:
    st.warning("비밀번호를 입력하세요.")
    st.stop()

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

menu = st.radio(
    "기능 선택",
    ["1. 시장 영향 이슈 분석", "2. 투자 리포트 제작", "3. 기업 검색/주가 데이터"],
)

# 1번
if menu == "1. 시장 영향 이슈 분석":
    st.subheader("🌅 시장 영향 이슈 분석")

    if st.button("최근 주요 시장 이슈 보기"):
        today = datetime.now().strftime("%Y-%m-%d")

        with st.spinner("최근 시장 이슈 확인 중..."):
            response = client.responses.create(
                model="gpt-4o-mini",
                tools=[{"type": "web_search"}],
                input=f"""
오늘 날짜는 {today}야.

최근 며칠 이내 기준으로 금융시장과 주식시장에 영향을 줄 수 있는 주요 이슈를 정리해줘.

포함 범위:
- 지정학: 전쟁, 해협, 국제 갈등, 원자재 공급 불안
- 정책: 금리, 중앙은행, 규제, 정부 발표
- 산업: AI, 반도체, 에너지, 전력, 바이오, 방산
- 기업: 실적, 계약, 공급망, 규제, 신사업

형식:
1. 이슈 제목
- 날짜:
- 핵심 내용:
- 시장 영향:
- 관련 산업/종목:
- 확인할 지표:

주의:
- 오래된 수개월 전 이슈는 제외
- 최신성이 낮으면 “최신성 낮음” 표시
- 확인되지 않은 루머는 단정하지 말 것
- 투자 추천처럼 쓰지 말 것
"""
            )
            st.write(response.output_text)

# 2번
elif menu == "2. 투자 리포트 제작":
    st.subheader("📊 시장 이슈 기반 투자 리포트")

    issue = st.text_area(
        "시장 이슈 입력",
        placeholder="예: 호르무즈 해협 봉쇄 우려 / AI 전력 수요 증가 / 연준 의장 교체 가능성",
    )
    stocks = st.text_input(
        "관심 종목 입력",
        placeholder="예: 삼성전자, SK하이닉스, 엔비디아",
    )
    period = st.selectbox("투자 기간", ["단기", "중기", "장기"])
    style = st.selectbox("리포트 스타일", ["간단 요약", "자세한 분석", "고등학생 이해용"])

    if st.button("리포트 생성"):
        if not issue.strip():
            st.error("시장 이슈를 입력해줘.")
        else:
            today = datetime.now().strftime("%Y-%m-%d")

            with st.spinner("AI가 기업 정확성 확인 후 리포트 작성 중..."):
                prompt = f"""
오늘 날짜는 {today}야.
너는 투자 리서치 보조 AI야.

[입력 정보]
시장 이슈: {issue}
관심 종목: {stocks}
투자 기간: {period}
리포트 스타일: {style}

[기업 정확성 조건 - 매우 중요]
- 실제 존재하는 현재 기업명만 제시할 것.
- 과거 사명이나 부정확한 기업명은 현재 공식 사명으로 고쳐 쓸 것.
- 존재 여부가 불확실한 기업은 절대 제시하지 말 것.
- 상장사가 아닌 기업은 “비상장”이라고 표시할 것.
- 티커를 모르면 절대 추측하지 말고 “티커 확인 필요”라고 쓸 것.
- 한국 기업은 가능하면 종목코드도 함께 제시할 것.
- 미국 기업은 가능하면 티커도 함께 제시할 것.
- 예: “LG전선”처럼 현재 공식 상장 기업명으로 부정확할 수 있는 명칭은 그대로 쓰지 말고, 현재 기업명/상장 여부를 확인해서 작성할 것.

[작성 조건]
- 확정적인 매수/매도 추천은 하지 말 것.
- 근거와 리스크를 함께 제시할 것.
- 검증되지 않은 소문처럼 보이는 내용은 단정하지 말 것.
- 해당 이슈가 주식시장에 영향을 주는 경로를 설명할 것.
- 경제지표뿐 아니라 지정학, 정책, 산업 변화, 기업 이슈도 함께 고려할 것.
- 관심 종목이 입력되어 있으면 해당 종목을 우선 분석할 것.
- 관심 종목이 비어 있더라도 관련 실제 기업을 제시하되, 반드시 기업 정확성 조건을 지킬 것.

[리포트 형식]
1. 핵심 이슈 요약
2. 시장 전체 영향
3. 관련 업종 영향

4. 관련 기업 및 종목 분석
- 한국 기업:
  - 기업명 / 종목코드 또는 상장 여부 / 관련 이유 / 수혜 또는 피해 가능성 / 확인할 포인트
- 미국 기업:
  - 기업명 / 티커 / 관련 이유 / 수혜 또는 피해 가능성 / 확인할 포인트
- 기타 글로벌 기업:
  - 기업명 / 티커 또는 상장 여부 / 관련 이유 / 수혜 또는 피해 가능성 / 확인할 포인트

5. 관심 종목별 상세 영향
6. 체크해야 할 지표
7. 리스크
8. 최종 판단
9. 추가로 확인하면 좋은 자료
"""

                response = client.responses.create(
                    model="gpt-4o-mini",
                    tools=[{"type": "web_search"}],
                    input=prompt,
                )

                st.write(response.output_text)

# 3번
elif menu == "3. 기업 검색/주가 데이터":
    st.subheader("📈 기업 검색/주가 데이터")

    stock_input = st.text_input(
        "기업명 또는 티커 검색",
        placeholder="예: 삼성전자 / 엔비디아 / NVDA / 005930.KS",
    )

    period = st.selectbox("조회 기간", ["1mo", "3mo", "6mo", "1y", "5y"])

    ticker = None

    if st.button("티커 검색"):
        if not stock_input.strip():
            st.error("기업명 또는 티커를 입력해줘.")
        else:
            with st.spinner("티커 검색 중..."):
                try:
                    search = yf.Search(stock_input.strip(), max_results=10)
                    quotes = search.quotes

                    if not quotes:
                        st.error("검색 결과가 없어. 티커를 직접 입력해봐.")
                    else:
                        st.session_state["quotes"] = quotes
                except Exception as e:
                    st.error("티커 검색 중 오류가 발생했어. 직접 티커 입력을 사용해줘.")
                    st.code(str(e))

    if "quotes" in st.session_state:
        options = []

        for q in st.session_state["quotes"]:
            symbol = q.get("symbol", "")
            name = q.get("shortname") or q.get("longname") or ""
            exchange = q.get("exchange", "")
            quote_type = q.get("quoteType", "")
            options.append(f"{symbol} | {name} | {exchange} | {quote_type}")

        selected = st.selectbox("검색 결과에서 선택", options)
        ticker = selected.split(" | ")[0]

    direct_ticker = st.text_input(
        "또는 티커 직접 입력",
        placeholder="예: 005930.KS / NVDA / TSLA",
    )

    if direct_ticker.strip():
        ticker = direct_ticker.strip()

    if st.button("주가 데이터 조회"):
        if not ticker:
            st.error("먼저 티커를 검색해서 선택하거나 직접 입력해줘.")
        else:
            with st.spinner("주가 데이터 불러오는 중..."):
                try:
                    data = yf.download(
                        ticker,
                        period=period,
                        progress=False,
                        auto_adjust=True,
                    )

                    if data.empty:
                        st.error("데이터를 불러오지 못했어. 티커를 다시 확인해줘.")
                    else:
                        close = data["Close"]

                        if hasattr(close, "columns"):
                            close = close.iloc[:, 0]

                        close = close.dropna()

                        if len(close) < 2:
                            st.error("분석할 수 있는 주가 데이터가 부족해.")
                        else:
                            first_price = float(close.iloc[0])
                            last_price = float(close.iloc[-1])
                            high_price = float(close.max())
                            low_price = float(close.min())

                            return_rate = (last_price - first_price) / first_price * 100
                            drawdown = (last_price - high_price) / high_price * 100

                            st.write(f"### {ticker} 핵심 주가 데이터")
                            st.write(f"- 기간 첫 종가: {first_price:.2f}")
                            st.write(f"- 최근 종가: {last_price:.2f}")
                            st.write(f"- 기간 최고 종가: {high_price:.2f}")
                            st.write(f"- 기간 최저 종가: {low_price:.2f}")
                            st.write(f"- 기간 수익률: {return_rate:.2f}%")
                            st.write(f"- 고점 대비 하락률: {drawdown:.2f}%")

                            st.write("### 최근 종가 데이터")
                            st.dataframe(close.tail(10))

                            if st.button("이 주가 흐름 AI 해석"):
                                prompt = f"""
다음 종목의 주가 흐름을 투자 리서치 관점에서 해석해줘.

종목 코드: {ticker}
조회 기간: {period}
기간 첫 종가: {first_price:.2f}
최근 종가: {last_price:.2f}
기간 최고 종가: {high_price:.2f}
기간 최저 종가: {low_price:.2f}
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

                except Exception as e:
                    st.error("주가 데이터를 불러오는 중 오류가 발생했어.")
                    st.code(str(e))
