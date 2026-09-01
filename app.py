import streamlit as st
import google.generativeai as genai

# ここに君のAPIキーを貼る
genai.configure(api_key="YOUR_API_KEY")

def generate_with_gemini(prompt: str) -> str:
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(prompt)
    return response.text

st.set_page_config(layout="wide", page_title="人的資本レポート自動生成 SaaS モック")

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
    score += 40
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
    st.title("人的資本レポート自動生成 SaaS（モック＋Gemini文章生成）")
    st.success("レポート生成はGemini APIで動きます。他のページはモックです。")

# -----------------------------
# ページ2〜6：モック
# -----------------------------
elif page == "企業情報（EDINET）":
    st.title("企業情報取得（モック）")
    st.info("EDINET連携は後で実装します")

elif page == "経営戦略リンク":
    st.title("経営戦略リンク（モック）")
    st.info("資料アップロード機能は後で実装します")

elif page == "同業他社分析":
    st.title("同業他社分析（モック）")
    st.info("EDINET自動収集は後で実装します")

elif page == "KPI入力":
    st.title("人的資本KPI入力")

    st.subheader("KPIフォーム")
    st.session_state["male_leave"] = st.number_input("男性育休取得率（%）", 0, 100)
    st.session_state["female_manager"] = st.number_input("女性管理職比率（%）", 0, 100)
    st.session_state["turnover"] = st.number_input("離職率（%）", 0, 100)
    st.session_state["training_hours"] = st.number_input("年間研修時間（時間）", 0, 500)
    st.session_state["disabled_rate"] = st.number_input("障害者雇用率（%）", 0, 100)
    st.session_state["midcareer_rate"] = st.number_input("中途採用比率（%）", 0, 100)

    st.success("このKPIはレポート生成とスコア判定に使われます")

elif page == "ガイドラインスコア":
    st.title("金融庁ガイドライン準拠スコア")

    st.info("KPI入力ページで入力した値を使います")

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

    st.subheader(f"総合スコア：{score} / 100")
    st.write("※簡易版スコアです。後で詳細版に拡張します。")

# -----------------------------
# ページ7：レポート生成（Gemini連携）
# -----------------------------
elif page == "レポート生成":
    st.title("人的資本レポート生成（Gemini API）")

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
            prompt = f"""
            以下のKPIを使って、IR向けの人的資本レポートを日本語で作成してください。

            男性育休取得率：{male_leave}%
            女性管理職比率：{female_manager}%
            離職率：{turnover}%
            年間研修時間：{training_hours}時間
            障害者雇用率：{disabled_rate}%
            中途採用比率：{midcareer_rate}%
            """
        else:
            prompt = f"""
            以下のKPIとスコア（{score}/100）を使って、
            金融庁ガイドライン準拠の人的資本レポートを日本語で作成してください。

            男性育休取得率：{male_leave}%
            女性管理職比率：{female_manager}%
            離職率：{turnover}%
            年間研修時間：{training_hours}時間
            障害者雇用率：{disabled_rate}%
            中途採用比率：{midcareer_rate}%
            """

        report = generate_with_gemini(prompt)

        st.subheader("生成されたレポート（Gemini）")
        st.write(report)

