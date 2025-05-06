import streamlit as st
import pandas as pd
import itertools

st.title("🏇 進化型AI競馬予想アプリ（単勝＋馬連＋ワイド）")
st.write("CSVファイルをアップロードして、AIが買い目と配分を提案します！")

# 💴 軍資金
budget = st.number_input("💴 軍資金を入力（円）", value=10000, step=1000)

# 📂 ファイルアップロード
uploaded_file = st.file_uploader("📥 出走表CSVファイルをアップロード（UTF-8形式）", type="csv")
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    # スコア計算
    weights = {
        "タイム指数": 0.2, "上がり3F": -0.1, "調教": 0.1, "騎手": 0.1,
        "馬場": 0.1, "コース": 0.1, "枠順": 0.05, "展開": 0.1,
        "血統": 0.05, "ローテ": 0.05, "成長": 0.05
    }

    def calc_score(row):
        return round(sum(row[col] * w for col, w in weights.items()), 2)

    df["AIスコア"] = df.apply(calc_score, axis=1)
    df = df.sort_values(by="AIスコア", ascending=False).reset_index(drop=True)

    # 🧠 コメントと危険人気馬
    def comment(row):
        c = []
        if row["調教"] >= 85: c.append("仕上がり良好")
        if row["騎手"] >= 88: c.append("騎手頼れる")
        if row["展開"] >= 85: c.append("展開バッチリ")
        if row["成長"] >= 85: c.append("成長中で期待")
        if not c: c.append("静かにチャンスあり")
        return "・".join(c)

    df["AIコメント"] = df.apply(comment, axis=1)
    df["危険注意"] = df.apply(lambda row: "⚠️" if row["人気"] <= 3 and row["AIスコア"] < 60 else "", axis=1)

    st.subheader("📊 予想結果（スコア順）")
    st.dataframe(df[["日付", "レース名", "馬名", "人気", "オッズ", "AIスコア", "危険注意", "AIコメント"]])

    # 💴 買い目（単勝・馬連・ワイド）
    st.subheader("💴 各レースの買い目配分（単勝・馬連・ワイド）")
    
    for race_name, group in df.groupby("レース名"):
        st.markdown(f"### 📌 {race_name} のおすすめ買い目")
        top3 = group.sort_values(by="AIスコア", ascending=False).head(3)

        # --- 単勝 ---
        st.markdown("#### 🎯 単勝（スコア比で配分）")
        total_score = top3["AIスコア"].sum()
        sing_budget = budget * 0.5
        for _, row in top3.iterrows():
            ratio = row["AIスコア"] / total_score
            amount = int(round(sing_budget * ratio / 100) * 100)
            exp = int(round(amount * row["オッズ"]))
            st.write(f"・{row['馬名']}：{amount}円（期待回収：{exp}円）")

        # --- 馬連 ---
        st.markdown("#### 🟦 馬連（3点・均等割り）")
        umaren_pairs = list(itertools.combinations(top3["馬名"], 2))
        umaren_budget = int(round((budget * 0.3) / 3 / 100) * 100)
        for pair in umaren_pairs:
            st.write(f"・{pair[0]} × {pair[1]}：{umaren_budget}円")

        # --- ワイド ---
        st.markdown("#### 🟨 ワイド（3点・均等割り）")
        wide_budget = int(round((budget * 0.2) / 3 / 100) * 100)
        for pair in umaren_pairs:
            st.write(f"・{pair[0]} × {pair[1]}：{wide_budget}円")
