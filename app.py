import streamlit as st
import pandas as pd

st.title("🏇 進化型AI競馬予想アプリ")
st.write("進化したCSV（レース名・日付・着順付き）を読み込んでAI予想します！")

budget = st.number_input("💴 軍資金を入力", value=10000, step=1000)

uploaded_file = st.file_uploader("📂 出走表CSVファイルをアップロード（UTF-8形式）", type="csv")
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    # AIスコア計算用の重み（例）
    weights = {
        "タイム指数": 0.2, "上がり3F": -0.1, "調教": 0.1, "騎手": 0.1,
        "馬場": 0.1, "コース": 0.1, "枠順": 0.05, "展開": 0.1,
        "血統": 0.05, "ローテ": 0.05, "成長": 0.05
    }

    def calc_score(row):
        score = 0
        for col, weight in weights.items():
            score += row[col] * weight
        return round(score, 2)

    def comment(row):
        c = []
        if row["調教"] >= 85: c.append("仕上がり良好")
        if row["騎手"] >= 88: c.append("騎手頼れる")
        if row["展開"] >= 85: c.append("展開バッチリ")
        if row["成長"] >= 85: c.append("成長中で期待")
        if not c: c.append("静かにチャンスあり")
        return "・".join(c)

    df["AIスコア"] = df.apply(calc_score, axis=1)
    df["AIコメント"] = df.apply(comment, axis=1)

    # 危険な人気馬に⚠️つける
    df["危険注意"] = df.apply(lambda row: "⚠️" if row["人気"] <= 3 and row["AIスコア"] < 60 else "", axis=1)

    # 並び替え
    df = df.sort_values(by="AIスコア", ascending=False).reset_index(drop=True)

    st.subheader("📊 予想結果（スコア順）")
    st.dataframe(df[["日付", "レース名", "馬名", "人気", "オッズ", "AIスコア", "危険注意", "AIコメント"]])
