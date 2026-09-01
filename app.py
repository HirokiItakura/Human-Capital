import streamlit as st

# -----------------------------
# 企業基本情報（固定）
# -----------------------------
company_info = {
    "会社名": "北海道中央バス株式会社",
    "EDINETコード": "E04161",
    "証券コード": "9085",
    "従業員数": "2,513名（臨時716名）",
    "売上高": "383億円（連結）",
    "事業内容": "旅客自動車運送事業、観光、不動産、高齢者向け住宅事業"
}

# -----------------------------
# 金融庁ガイドライン準拠スコア計算
# -----------------------------
def calc_fsa_score(male_leave, female_manager, turnover,
                   training_hours, disabled_rate, midcareer_rate):

    score = 0

    # KPI入力の有無（各10点）
    if male_leave > 0: score += 10
    if female_manager > 0: score += 10
    if turnover > 0: score += 10
    if training_hours > 0: score += 10
    if disabled_rate > 0: score += 10
    if midcareer_rate > 0: score += 10

    # ガイドライン必須項目（固定加点）
    # 人材育成、安全、ダイバーシティ、働きやすさ、今後の取り組み
    score += 40

    return score


# -----------------------------
# レポート生成（IR向け）
# -----------------------------
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

これらの取り組みを通じて、企業価値向上と持続的成長を実現してまいります。
"""


# -----------------------------
# レポート生成（金融庁向け）
# -----------------------------
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

当社は金融庁の人的資本可視化指針に基づき、
人材投資の強化、ダイバーシティ推進、安全教育の高度化、
働きやすい職場環境の整備を継続的に進めてまいります。
"""


# -----------------------------
# Streamlit UI
# -----------------------------
st.title("人的資本レポート自動生成（北海道中央バス）")

st.subheader("企業基本情報")
for key, value in company_info.items():
    st.write(f"**{key}**：{value}")

# レポート種別選択
report_type = st.radio(
    "レポート種別を選択してください",
    ("株主向け（IR）", "金融庁向け（有価証券報告書）")
)

st.subheader("人的資本KPI入力")

male_leave = st.number_input("男性育休取得率（%）", 0, 100)
female_manager = st.number_input("女性管理職比率（%）", 0, 100)
turnover = st.number_input("離職率（%）", 0, 100)
training_hours = st.number_input("年間研修時間（時間）", 0, 500)
disabled_rate = st.number_input("障害者雇用率（%）", 0, 100)
midcareer_rate = st.number_input("中途採用比率（%）", 0, 100)

if st.button("人的資本レポートを生成"):
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
