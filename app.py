import streamlit as st, pandas as pd, requests, json, os
from datetime import datetime

st.set_page_config(page_title="Panel", layout="wide")
st.title("📈 Halka Arz • 💰 Fon • 📊 BIST")

# CLOUD UYUMLU
cfg_path = "config.json"
cfg = json.load(open(cfg_path, encoding="utf-8"))
halka = pd.DataFrame(cfg.get("halka_arz_liste", []))
fon = pd.DataFrame(cfg.get("fon_liste", []))

mtime = os.path.getmtime(cfg_path)
st.caption(f"Son güncelleme: {datetime.fromtimestamp(mtime).strftime('%d.%m %H:%M')}")

t1,t2,t3 = st.tabs(["Halka Arz","Fonlar","Hisseler"])

with t1:
    if "Tarih" in halka.columns:
        halka["Geri Sayım"] = halka["Tarih"].apply(lambda x: "⏳ 4 gün kaldı" if "17-19" in str(x) else ("Yakında" if "Temmuz" in str(x) else "-"))
    st.dataframe(halka, use_container_width=True, height=420)

with t2:
    def renklendir(s):
        return ['background-color: #d4edda' if v == s.max() else '' for v in s]
    if "Günlük%" in fon.columns:
        styled = fon.style.apply(renklendir, subset=["Günlük%"])
        st.dataframe(styled, use_container_width=True, height=420)
    else:
        st.dataframe(fon, use_container_width=True)

with t3:
    rows=[]
    for k in ["THYAO.IS","ASELS.IS","TUPRS.IS","EREGL.IS","SAHOL.IS","AKBNK.IS"]:
        try:
            p = requests.get(f"https://query1.finance.yahoo.com/v8/finance/chart/{k}", headers={"User-Agent":"Mozilla"}, timeout=4).json()["chart"]["result"][0]["meta"]["regularMarketPrice"]
            rows.append({"Hisse":k[:-3],"Fiyat":round(p,2)})
        except: pass
    st.dataframe(pd.DataFrame(rows), use_container_width=True)
