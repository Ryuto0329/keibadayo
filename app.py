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
    df = pd.read_csv(uploaded_file)

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
