import streamlit as st
import requests
from bs4 import BeautifulSoup

# ------------------------------------------------------------
# EDINETから企業情報を取得（簡易版）
# ------------------------------------------------------------
def fetch_edinet_info(company_name):
    # EDINETコード検索（簡易スクレイピング）
    search_url = f"https://disclosure.edinet-fsa.go.jp/searchdocument/search?keyword={company_name}"
    res = requests.get(search_url)
    soup = BeautifulSoup(res.text, "html.parser")

    # EDINETコード抽出（簡易）
    code_tag = soup.find("td", {"class": "alignL"})
    if not code_tag:
        return None

    edinet_code = code_tag.text.strip()

    # 有報URL（最新）
    doc_url = f"https://disclosure.edinet-fsa.go.jp/searchdocument/detail?code={edinet_code}"

    return {
        "EDINETコード": edinet_code,
        "有報URL": doc_url
    }


# ------------------------------------------------------------
# 同業他社の人的資本レポート抽出（簡易版）
# ------------------------------------------------------------
def fetch_competitor_summary(edinet_code):
    url = f"https://disclosure.edinet-fsa.go.jp/searchdocument/detail?code={edinet_code}"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")

    # 人的資本に関する記載を抽出（簡易）
    text = soup.get_text()

    keywords = ["人的資本", "人材育成", "多様性", "健康", "安全", "働き方"]
    summary = "\n".join([line for line in text.split("\n") if any(k in line for k in keywords)])

    return summary[:800]  # 長すぎるので800文字に制限


# ------------------------------------------------------------
# 金融庁ガイドライン準拠スコア計算
# ------------------------------------------------------------
def calc_fsa_score(male_leave, female_manager, turnover,
                   training_hours, disabled_rate, midcareer_rate):

    score = 0

    if male_leave > 0: score += 10
    if female_manager > 0: score += 10
    if turnover > 0: score += 10
    if training_hours > 0: score += 10
    if disabled_rate > 0: score += 10
    if midcareer_rate > 0: score += 10

    score += 40
    return score


# ------------------------------------------------------------
# レポート生成（IR向け）
# ------------------------------------------------------------
def generate_report_ir(male_leave, female_manager, turnover,
                       training_hours, disabled_rate, midcareer_rate):

    return f"""
【株主向け（IR）人的資本レポート】

当社は持続的成長の基盤として「人材育成」「安全・安心」「働きやすい職場環境」を
人的資本戦略の中心に据えています。

人的資本KPIは以下の通りです。
- 男性育休取得率：{male_leave}%
- 女性管理職比率：{female_manager}%
- 離職率：{turnover}%
- 年間研修時間：{training_hours}時間
- 障害者雇用率：{disabled_rate}%
- 中途採用比率：{midcareer_rate}%

企業価値向上と持続的成長を実現してまいります。
"""


# ------------------------------------------------------------
# レポート生成（金融庁向け）
# ------------------------------------------------------------
def generate_report_fsa(male_leave, female_manager, turnover,
                        training_hours, disabled_rate, midcareer_rate, score):

    return f"""
【金融庁ガイドライン準拠 人的資本レポート】

当社は経営戦略と整合した人的資本戦略として、
「人材育成」「安全・安心」「多様性推進」「働きやすい職場環境の整備」を
重要課題として位置づけています。

人的資本KPI（ガイドライン準拠）
- 男性育休取得率：{male_leave}%
- 女性管理職比率：{female_manager}%
- 離職率：{turnover}%
- 年間研修時間：{training_hours}時間
- 障害者雇用率：{disabled_rate}%
- 中途採用比率：{midcareer_rate}%

ガイドライン適合スコア：{score} / 100

金融庁の人的資本可視化指針に基づき、
人材投資の強化、ダイバーシティ推進、安全教育の高度化、
働きやすい職場環境の整備を継続的に進めてまいります。
"""


# ------------------------------------------------------------
# Streamlit UI
# ------------------------------------------------------------
st.title("人的資本レポート自動生成（北海道中央バス）")

# 企業名入力 → EDINET取得
company_name = st.text_input("企業名を入力（EDINETから自動取得）")

if st.button("EDINETから企業情報を取得"):
    info = fetch_edinet_info(company_name)
    if info:
        st.success(f"EDINETコード：{info['EDINETコード']}")
        st.write(f"[有価証券報告書を見る]({info['有報URL']})")
    else:
        st.error("企業情報が見つかりませんでした")

# レイアウト分割
left, right = st.columns(2)

# ------------------------------------------------------------
# 左：同業他社サマリー
# ------------------------------------------------------------
with left:
    st.subheader("同業他社の人的資本レポート（EDINET）")

    competitor_codes = ["E04161", "E02123", "E03011"]  # 仮の同業他社EDINETコード

    for code in competitor_codes:
        st.write(f"### 企業コード：{code}")
        summary = fetch_competitor_summary(code)
        st.write(summary)
        st.write("---")


# ------------------------------------------------------------
# 右：自社レポート生成
# ------------------------------------------------------------
with right:
    st.subheader("自社レポート生成")

    report_type = st.radio(
        "レポート種別",
        ("株主向け（IR）", "金融庁向け（有価証券報告書）")
    )

    male_leave = st.number_input("男性育休取得率（%）", 0, 100)
    female_manager = st.number_input("女性管理職比率（%）", 0, 100)
    turnover = st.number_input("離職率（%）", 0, 100)
    training_hours = st.number_input("年間研修時間（時間）", 0, 500)
    disabled_rate = st.number_input("障害者雇用率（%）", 0, 100)
    midcareer_rate = st.number_input("中途採用比率（%）", 0, 100)

    if st.button("レポート生成"):
        score = calc_fsa_score(
            male_leave, female_manager, turnover,
            training_hours, disabled_rate, midcareer_rate
        )

        if report_type == "株主向け（IR）":
            report = generate_report_ir(
                male_leave, female_manager, turnover,
                training_hours, disabled_rate, midcareer_rate
            )
        else:
            report = generate_report_fsa(
                male_leave, female_manager, turnover,
                training_hours, disabled_rate, midcareer_rate,
                score
            )

        st.subheader("生成されたレポート")
        st.write(report)
