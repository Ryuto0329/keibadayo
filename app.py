import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="AI競馬予想", layout="wide")
st.title("🏇 AI競馬予想 ＆ 買い目提案アプリ")

# CSVアップロード
tab1, tab2 = st.tabs(["📄 出走表アップロード", "🧠 AI予想"])

with tab1:
    uploaded_file = st.file_uploader("出走表CSVファイルをアップロード", type=["csv"])
    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        st.success("✅ ファイル読み込み成功！")
        st.dataframe(df)
        st.session_state["df"] = df

with tab2:
    if "df" not in st.session_state:
        st.warning("📄 まず出走表CSVをアップロードしてください！")
    else:
        df = st.session_state["df"]

        # 特徴量から適当にスコアを作成（仮のAIロジック）
        np.random.seed(42)
        df["勝率予想"] = np.round(np.random.dirichlet(np.ones(len(df))), 3)
        df["3着内率"] = df["勝率予想"] + np.round(np.random.uniform(0.1, 0.25, len(df)), 3)

        # 🔥 修正ポイント：applyの中は x だけでOK！
        df["AIコメント"] = df["勝率予想"].apply(
            lambda x: "期待大！🔥" if x > 0.18 else ("展開次第！🤔" if x > 0.10 else "厳しいかも…")
        )

        st.subheader("🧠 AI予想結果")
        st.dataframe(df[["馬番","馬名", "騎手", "枠順", "オッズ", "勝率予想", "3着内率", "AIコメント"]])

        # 買い目算出（単勝のみ簡易計算）
        st.subheader("💸 AI買い目提案（単勝）")
        budget = st.number_input("軍資金（円）", value=1000, step=100)
        df_sorted = df.sort_values("勝率予想", ascending=False).head(3).copy()

        total_score = df_sorted["勝率予想"].sum()
        df_sorted["推奨金額"] = df_sorted["勝率予想"] / total_score * budget
        df_sorted["推奨金額"] = (df_sorted["推奨金額"] // 100 * 100).astype(int)

        st.dataframe(df_sorted[["馬番","馬名", "勝率予想", "オッズ", "推奨金額"]])
        st.info("※ 仮のAIロジックです。今後学習型に進化させていきます！")
