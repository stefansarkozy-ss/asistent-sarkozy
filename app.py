import streamlit as st
import pandas as pd
import os
from datetime import datetime

st.set_page_config(page_title="Asistent Štefana Šarközyho", layout="wide")

DATA_FILE = "dopyty.csv"

# Načítanie / inicializácia dátového úložiska
def load_data():
    if os.path.exists(DATA_FILE):
        return pd.read_csv(DATA_FILE)
    else:
        return pd.DataFrame(columns=[
            "ID", "Datum_Vytvorenia", "Sluzba", "Hodiny", "Miesto", 
            "Krajina", "Datum_Akcie", "Cas", "Stav", "Poznamka"
        ])

def save_data(df):
    df.to_csv(DATA_FILE, index=False)

if "dopyty" not in st.session_state:
    st.session_state.dopyty = load_data()

st.title("💼 Asistent Štefana Šarközyho")

tabs = st.tabs(["📋 Dopyty", "➕ Nová požiadavka", "📊 Pipeline", "👥 Klienti", "⚙️ Nastavenia"])

# ZÁLOŽKA 1: DOPYTY
with tabs[0]:
    st.header("Zoznam zaznamenaných dopytov")
    df = st.session_state.dopyty
    if df.empty:
        st.info("Zatiaľ neboli zaznamenané žiadne dopyty.")
    else:
        st.dataframe(df, use_container_width=True)
        
        st.subheader("Detail a úprava dopytu")
        selected_id = st.selectbox("Vyberte dopyt na spracovanie ID:", df["ID"].tolist() if not df.empty else [])
        if selected_id:
            row = df[df["ID"] == selected_id].iloc[0]
            st.write(f"**Služba:** {row['Sluzba']} | **Miesto:** {row['Miesto']} ({row['Krajina']}) | **Termín:** {row['Datum_Akcie']}")
            novy_stav = st.selectbox("Zmeniť stav:", ["Nová", "V riešení", "Potvrdená", "Kalendár", "Vybavené", "Zrušená"], index=["Nová", "V riešení", "Potvrdená", "Kalendár", "Vybavené", "Zrušená"].index(row['Stav']) if row['Stav'] in ["Nová", "V riešení", "Potvrdená", "Kalendár", "Vybavené", "Zrušená"] else 0)
            if st.button("Uložiť zmenu stavu"):
                st.session_state.dopyty.loc[st.session_state.dopyty["ID"] == selected_id, "Stav"] = novy_stav
                save_data(st.session_state.dopyty)
                st.success("Stav bol aktualizovaný a uložený!")
                st.rerun()

# ZÁLOŽKA 2: NOVÁ POŽIADAVKA
with tabs[1]:
    st.header("1. Služby a bloky")
    sluzba = st.selectbox("Služba", ["SI - Indiv. supervízia", "SK - Kolektívna supervízia", "Krízová intervencia", "Koučing", "Vzdelávanie / Lektorovanie"])
    hodiny = st.number_input("Hodiny", min_value=1.0, max_value=12.0, value=4.0, step=0.5)

    st.header("2. Volný termín a logistika (z Dúbravky)")
    col1, col2 = st.columns(2)
    with col1:
        krajina = st.radio("Krajina výjazdu", ["Slovensko (SR)", "Česká republika (ČR)"], horizontal=True)
    with col2:
        miesto = st.text_input("Miesto / Obec (napr. Jelka, Piešťany, Praha...)", value="Jelka")

    col_d, col_t = st.columns(2)
    with col_d:
        datum_akcie = st.date_input("Dátum konania", datetime.now())
    with col_t:
        cas_akcie = st.time_input("Čas začiatku", datetime.now().time())

    poznamka = st.text_area("Poznámka / Špecifikácia dopytu", "")

    if st.button("💾 Uložiť dopyt do zoznamu", type="primary"):
        novy_id = len(st.session_state.dopyty) + 1
        novy_riadok = {
            "ID": novy_id,
            "Datum_Vytvorenia": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "Sluzba": sluzba,
            "Hodiny": hodiny,
            "Miesto": miesto,
            "Krajina": krajina,
            "Datum_Akcie": str(datum_akcie),
            "Cas": str(cas_akcie),
            "Stav": "Nová",
            "Poznamka": poznamka
        }
        st.session_state.dopyty = pd.concat([st.session_state.dopyty, pd.DataFrame([novy_riadok])], ignore_index=True)
        save_data(st.session_state.dopyty)
        st.success(f"Dopyt pre miesto '{miesto}' bol úspešne uložený pod ID {novy_id}!")

# ZÁLOŽKA 3: PIPELINE
with tabs[2]:
    st.header("Prehľad stavov (Pipeline)")
    if not st.session_state.dopyty.empty:
        st.bar_chart(st.session_state.dopyty["Stav"].value_counts())
    else:
        st.info("Žiadne dáta v pipeline.")
