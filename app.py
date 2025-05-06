import streamlit as st
import pandas as pd

st.title("🏇 AI競馬予想アプリ（CSV版）")
st.write("出走表CSVをアップロードすると、AI予想が表示されます！")

# 軍資金
budget = st.number_input("💴 軍資金を入力してね", value=10000, step=1000)
st.success(f"設定された軍資金：{budget:,}円")

# CSVアップロード
uploaded_file = st.file_uploader("📥 出走表CSVファイルをアップロード", type=["csv"])
if uploaded_file is not None:
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
    df = df.sort_values(by="AIスコア",_


    # スコア計算
    weight = {
        'タイム指数': 0.2, '上がり3F': -0.1, '調教': 0.1, '騎手': 0.1,
        '馬場': 0.1, 'コース': 0.1, '枠順': 0.05, '展開': 0.1,
        '血統': 0.05, 'ローテ': 0.05, '成長': 0.05
    }

    def calculate_score(row):
        score = 0
        for key, w in weight.items():
            score += row[key] * w
        return round(score, 2)

    def generate_comment(row):
        comments = []
        if row['調教'] >= 85:
            comments.append("仕上がり良好")
        if row['騎手'] >= 88:
            comments.append("騎手頼れる")
        if row['展開'] >= 85:
            comments.append("展開向くかも")
        if row['成長'] >= 85:
            comments.append("成長中で期待")
        if not comments:
            comments.append("静かにチャンスあり")
        return "・".join(comments)

    df['AIスコア'] = df.apply(calculate_score, axis=1)
    df['AIコメント'] = df.apply(generate_comment, axis=1)
    df = df.sort_values(by='AIスコア', ascending=False).reset_index(drop=True)

    st.subheader("📊 予想結果（AIスコア順）")
    st.dataframe(df)

    st.success("✨ 爆益めざそう！！！！🔥")
