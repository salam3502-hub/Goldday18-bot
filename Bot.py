import requests
import re

TGJU_GOLD = "https://www.tgju.org/profile/geram18"
TGJU_AED = "https://english.tgju.org/profile/price_aed"
UAE_GOLD = "https://xau.today/gold-price-18k-aed/"

def get_number(text, pattern):
    m = re.search(pattern, text)
    if not m:
        raise ValueError("عدد پیدا نشد")
    return float(m.group(1).replace(",", ""))

def get_prices():
    headers = {"User-Agent": "Mozilla/5.0"}

    gold_iran_text = requests.get(
        TGJU_GOLD, headers=headers, timeout=20
    ).text

    aed_text = requests.get(
        TGJU_AED, headers=headers, timeout=20
    ).text

    uae_gold_text = requests.get(
        UAE_GOLD, headers=headers, timeout=20
    ).text

    # TGJU: قیمت ایران و درهم به ریال
    iran_gold_rial = get_number(
        gold_iran_text,
        r"نرخ فعلی:\s*([0-9,]+)"
    )

    aed_rial = get_number(
        aed_text,
        r"Last:\s*([0-9,]+)"
    )

    # XAU Today: طلای 18K دبی به AED
    m = re.search(
        r"Currently, the price of 1 gram 18K of gold is AED\s*([0-9.]+)",
        uae_gold_text
    )

    if not m:
        raise ValueError("قیمت طلای دبی پیدا نشد")

    uae_gold_aed = float(m.group(1))

    # تبدیل ریال به تومان
    iran_gold_toman = iran_gold_rial / 10
    aed_toman = aed_rial / 10

    theoretical = uae_gold_aed * aed_toman
    difference = theoretical - iran_gold_toman
    percent = (difference / iran_gold_toman) * 100

    return (
        uae_gold_aed,
        aed_toman,
        iran_gold_toman,
        theoretical,
        difference,
        percent
    )

def make_report():
    uae_gold, aed, iran_gold, theoretical, difference, percent = get_prices()

    sign = "🔺" if difference >= 0 else "🔻"

    return f"""🟡 گزارش مقایسه طلای ۱۸ عیار

🇦🇪 طلای ۱۸ عیار دبی:
{uae_gold:,.2f} درهم

💵 قیمت درهم ایران:
{aed:,.0f} تومان

🇮🇷 طلای ۱۸ عیار ایران:
{iran_gold:,.0f} تومان

📊 قیمت محاسباتی:
{theoretical:,.0f} تومان

{sign} اختلاف:
{abs(difference):,.0f} تومان

📈 اختلاف درصدی:
{percent:+.2f}٪
"""
