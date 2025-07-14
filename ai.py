import pyupbit
import requests
import datetime

# ─────────── 본인 정보 입력 ───────────
TOKEN   = "8057793534:AAHhLl0l_ICAlGPzqnaun7R7UJJWtBLoACM"
CHAT_ID = 5946279519
# ──────────────────────────────────────

# 한글명 매핑 함수
def get_korean_names():
    markets = requests.get(
        "https://api.upbit.com/v1/market/all?isDetails=true"
    ).json()
    return {m['market']: m['korean_name'] for m in markets if m['market'].startswith('KRW-')}

# 금액 포맷팅: 소수점 2자리표현 가능 시 최대 2자리, 불필요한 0 제거
def format_price(price):
    s = f"{price:,.2f}"
    if '.' in s:
        s = s.rstrip('0').rstrip('.')
    return s

# 오전 08:00 시세 전송 함수
def send_open_prices():
    name_map = get_korean_names()
    tickers = pyupbit.get_tickers(fiat="KRW")

    # 전송시각: 오늘 날짜 08:00
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    ts = f"{today} 08:00"

    for ticker in tickers:
        try:
            name_kr = name_map.get(ticker, ticker)
            price = pyupbit.get_current_price(ticker)
            price_str = format_price(price)

            # 메시지 포맷
            text = (
                "🗺️ 경로 탐색 완료\n"
                f"종목명: {name_kr}\n"
                f"💰 현재가: {price_str}원\n\n"
                "🚀 출발 가격:\n"
                f" • {name_kr} — {price_str}원 이하 매수 진행\n\n"
                "🎯 도착 가격:\n"
                " • 5%이상 가격 상승 시 분할 매도\n\n"
                "매일 아침 출발 직전 종목들을 찾아냅니다\n"
                "신호를 통해 매수하시고 분할로 매도하세요\n"
            )

            # 텔레그램 API 호출
            requests.get(
                f"https://api.telegram.org/bot{TOKEN}/sendMessage",
                params={
                    "chat_id": CHAT_ID,
                    "text": text,
                    "parse_mode": "Markdown",
                    "disable_web_page_preview": True
                }
            )
        except Exception as e:
            print(f"⚠️ {ticker} 처리 중 오류: {e}")

if __name__ == "__main__":
    send_open_prices()
