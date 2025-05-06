import requests
from bs4 import BeautifulSoup
import pandas as pd

# ✅ ここにnetkeibaの出馬表URLを貼り替える！
url = "https://race.netkeiba.com/race/shutuba.html?race_id=202405030811"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
}

res = requests.get(url, headers=headers)
soup = BeautifulSoup(res.content, "html.parser")

# レース名取得
race_name_tag = soup.select_one(".RaceName")
race_name = race_name_tag.text.strip().replace("\n", "") if race_name_tag else "レース名不明"

# 馬場状態取得（芝・ダート + 良・稍重など）
baba_tag = soup.select_one(".RaceData01")
baba = baba_tag.text.strip().split("/")[-1].strip() if baba_tag else "不明"

# 馬情報の取得
rows = soup.select(".ShutubaTable .HorseList")

data = []
for row in rows:
    try:
        uma_tag = row.select_one(".HorseName a")
        jockey_tag = row.select_one(".Jockey a")
        wakuban_tag = row.select_one(".Waku")

        uma = uma_tag.text.strip() if uma_tag else ""
        jockey = jockey_tag.text.strip() if jockey_tag else ""
        waku = wakuban_tag.text.strip() if wakuban_tag else ""

        data.append({
            "レース名": race_name,
            "馬場状態": baba,
            "馬名": uma,
            "騎手": jockey,
            "枠順": waku
        })
    except Exception as e:
        print("エラー行スキップ：", e)

# CSVとして保存
if data:
    df = pd.DataFrame(data)
    df.to_csv("race_data.csv", index=False, encoding="utf-8-sig")
    print("✅ race_data.csv を出力しました！")
else:
    print("⚠️ データが取得できませんでした。")
