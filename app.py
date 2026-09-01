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
# 文章生成ロジック（簡易版）
# -----------------------------
def generate_report(male_leave, female_manager, turnover,
                    training_hours, disabled_rate, midcareer_rate):

    text = f"""
北海道中央バス株式会社は、旅客自動車運送事業を中心に、
観光事業、不動産事業、高齢者向け住宅事業など多様な事業を展開しており、
事業の持続的成長を支える基盤として「人材育成」「安全・安心の確保」
「働きやすい職場環境の整備」を人的資本戦略の中心に据えています。

当社は、バス運転士の育成を目的として子会社の中央バス自動車学園において
体系的な研修を実施しており、運転技術・接客・安全教育を含む総合的な人材育成を行っています。
また、当社グループは道内初の「貸切バス事業者安全性評価認定制度（セーフティバス）」認定事業者として、
安全運行に関する教育・訓練を継続的に実施しています。

人的資本KPIは以下の通りです。
- 男性育休取得率：{male_leave}%
- 女性管理職比率：{female_manager}%
- 離職率：{turnover}%
- 年間研修時間：{training_hours}時間
- 障害者雇用率：{disabled_rate}%
- 中途採用比率：{midcareer_rate}%

これらの指標を改善するため、働きやすい職場環境の整備、
ダイバーシティ推進、安全教育の強化を継続的に進めてまいります。
"""
    return text


# -----------------------------
# Streamlit UI
# -----------------------------
st.title("人的資本レポート自動生成（北海道中央バス）")

st.subheader("企業基本情報")
for key, value in company_info.items():
    st.write(f"**{key}**：{value}")

st.subheader("人的資本KPI入力")

male_leave = st.number_input("男性育休取得率（%）", 0, 100)
female_manager = st.number_input("女性管理職比率（%）", 0, 100)
turnover = st.number_input("離職率（%）", 0, 100)
training_hours = st.number_input("年間研修時間（時間）", 0, 500)
disabled_rate = st.number_input("障害者雇用率（%）", 0, 100)
midcareer_rate = st.number_input("中途採用比率（%）", 0, 100)

if st.button("人的資本レポートを生成"):
    report = generate_report(
        male_leave, female_manager, turnover,
        training_hours, disabled_rate, midcareer_rate
    )
    st.subheader("生成されたレポート")
    st.write(report)
