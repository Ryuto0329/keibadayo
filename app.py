import streamlit as st

st.title('🏇 競馬AI簡単版アプリ')
st.header('💰 軍資金設定')
budget = st.number_input('軍資金を入力してね（円）', value=10000, step=1000)
st.success(f'設定された軍資金は: {budget:,}円')

st.header('🏇 出走馬データ（サンプル）')
horses = ['サクラバクシンオー', 'トウカイテイオー', 'ビワハヤヒデ']
scores = [90, 85, 70]

for horse, score in zip(horses, scores):
    st.write(f"馬名: {horse}、最終スコア: {score}点")

st.header('🔥 今日も爆益目指そう！！！')
