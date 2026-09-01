import streamlit as st

st.set_page_config(layout="wide", page_title="人的資本レポート自動生成 SaaS モック")

# -----------------------------
# 文章生成ロジック（簡易版）
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


# -----------------------------
# スコア計算（簡易版）
# -----------------------------
def calc_fsa_score(male_leave, female_manager, turnover,
                   training_hours, disabled_rate, midcareer_rate):

    score = 0

    if male_leave > 0: score += 10
    if female_manager > 0: score += 10
    if turnover > 0: score += 10
    if training_hours > 0: score += 10
    if disabled_rate > 0: score += 10
    if midcareer_rate > 0: score += 10

    score += 40  # 固定加点（戦略・安全・多様性など）
    return score


# -----------------------------
# サイドバー（ナビゲーション）
# -----------------------------
st.sidebar.title("メニュー")
page = st.sidebar.radio(
    "ページ選択",
    [
        "ダッシュボード",
        "企業情報（EDINET）",
        "経営戦略リンク",
        "同業他社分析",
        "KPI入力",
        "ガイドラインスコア",
        "レポート生成"
    ]
)

# -----------------------------
# ページ1：ダッシュボード
# -----------------------------
if page == "ダッシュボード":
    st.title("人的資本レポート自動生成 SaaS（モック＋文章生成）")
    st.success("文章生成とスコア判定は動作します。その他はモックです。")


# -----------------------------
# ページ2：企業情報（EDINET）
# -----------------------------
elif page == "企業情報（EDINET）":
    st.title("企業情報取得（モック）")
    st.info("EDINET連携は後で実装します")


# -----------------------------
# ページ3：経営戦略リンク
# -----------------------------
elif page == "経営戦略リンク":
    st.title("経営戦略リンク（モック）")
    st.info("資料アップロード機能は後で実装します")


# -----------------------------
# ページ4：同業他社分析
# -----------------------------
elif page == "同業他社分析":
    st.title("同業他社分析（モック）")
    st.info("EDINET自動収集は後で実装します")


# -----------------------------
# ページ5：KPI入力
# -----------------------------
elif page == "KPI入力":
    st.title("人的資本KPI入力")

    st.subheader("KPIフォーム")
    male_leave = st.number_input("男性育休取得率（%）", 0, 100)
    female_manager = st.number_input("女性管理職比率（%）", 0, 100)
    turnover = st.number_input("離職率（%）", 0, 100)
    training_hours = st.number_input("年間研修時間（時間）", 0, 500)
    disabled_rate = st.number_input("障害者雇用率（%）", 0, 100)
    midcareer_rate = st.number_input("中途採用比率（%）", 0, 100)

    st.success("このKPIはレポート生成とスコア判定に使われます")


# -----------------------------
# ページ6：ガイドラインスコア
# -----------------------------
elif page == "ガイドラインスコア":
    st.title("金融庁ガイドライン準拠スコア")

    st.info("KPI入力ページで入力した値を使います")

    score = calc_fsa_score(
        st.session_state.get("male_leave", 0),
        st.session_state.get("female_manager", 0),
        st.session_state.get("turnover", 0),
        st.session_state.get("training_hours", 0),
        st.session_state.get("disabled_rate", 0),
        st.session_state.get("midcareer_rate", 0)
    )

    st.subheader(f"総合スコア：{score} / 100")
    st.write("※簡易版スコアです。後で詳細版に拡張します。")


# -----------------------------
# ページ7：レポート生成
# -----------------------------
elif page == "レポート生成":
    st.title("人的資本レポート生成")

    report_type = st.radio("レポート種別", ["IR向け", "金融庁向け（有報）"])

    male_leave = st.session_state.get("male_leave", 0)
    female_manager = st.session_state.get("female_manager", 0)
    turnover = st.session_state.get("turnover", 0)
    training_hours = st.session_state.get("training_hours", 0)
    disabled_rate = st.session_state.get("disabled_rate", 0)
    midcareer_rate = st.session_state.get("midcareer_rate", 0)

    score = calc_fsa_score(
        male_leave, female_manager, turnover,
        training_hours, disabled_rate, midcareer_rate
    )

    if st.button("レポート生成"):
        if report_type == "IR向け":
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
