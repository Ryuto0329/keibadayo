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

st.subheader("📋 おすすめレース一覧（AI評価）")

# レース単位でスコア差（ばらつき）を見ておすすめ度をつける
recommendations = []
for race_name, group in df.groupby("レース名"):
    max_score = group["AIスコア"].max()
    min_score = group["AIスコア"].min()
    spread = max_score - min_score

    if spread >= 15:
        rank = "🌟🌟🌟"
        reason = "スコア差大きく本命明確"
    elif spread >= 8:
        rank = "🌟🌟"
        reason = "スコア差中・バランス型"
    else:
        rank = "🌟"
        reason = "混戦模様・穴狙いも視野"

    recommendations.append({
        "レース名": race_name,
        "おすすめ度": rank,
        "理由": reason
    })

rec_df = pd.DataFrame(recommendations)
st.dataframe(rec_df)

st.subheader("💴 各レースの買い目配分（単勝AI配分）")

# 買い目配分結果を保存するリスト
bets = []

# レースごとに処理
for race_name, group in df.groupby("レース名"):
    # AIスコア上位3頭を取得
    top_horses = group.sort_values(by="AIスコア", ascending=False).head(3)
    total_score = top_horses["AIスコア"].sum()

    for _, row in top_horses.iterrows():
        score = row["AIスコア"]
        ratio = score / total_score
        amount = int(budget * ratio)
        expected_return = round(amount * row["オッズ"])
        bets.append({
            "レース名": race_name,
            "馬名": row["馬名"],
            "AIスコア": score,
            "人気": row["人気"],
            "オッズ": row["オッズ"],
            "配分金額": f"¥{amount:,}",
            "期待回収": f"¥{expected_return:,}"
        })

# 表示
bets_df = pd.DataFrame(bets)
st.dataframe(bets_df)

