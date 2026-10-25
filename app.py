import streamlit as st
import pandas as pd
import os
from datetime import datetime

st.set_page_config(page_title="Asistent Štefana Šarközyho", layout="wide", page_icon="💼")

DATA_FILE = "dopyty.csv"

# Reálne dáta podľa tvojho zoznamu
INITIAL_DATA = [
    {"ID": 1, "Datum_Vytvorenia": "2026-10-25 09:00", "Sluzba": "SI - Supervízia", "Hodiny": 4.0, "Miesto": "Cífer", "Krajina": "Slovensko (SR)", "Datum_Akcie": "2026-11-02", "Cas": "09:00", "Stav": "Nová", "Poznamka": "Fakturácia: 240"},
    {"ID": 2, "Datum_Vytvorenia": "2026-10-25 09:15", "Sluzba": "SI - Supervízia", "Hodiny": 4.0, "Miesto": "CDR Piešťany", "Krajina": "Slovensko (SR)", "Datum_Akcie": "2026-11-04", "Cas": "10:00", "Stav": "Nová", "Poznamka": "Fakturácia: 240"},
    {"ID": 3, "Datum_Vytvorenia": "2026-10-25 09:30", "Sluzba": "SI - Supervízia", "Hodiny": 4.0, "Miesto": "KC Pribeta", "Krajina": "Slovensko (SR)", "Datum_Akcie": "2026-11-06", "Cas": "09:30", "Stav": "V riešení", "Poznamka": "Dohoda, Fakturácia: 240"},
    {"ID": 4, "Datum_Vytvorenia": "2026-10-25 09:45", "Sluzba": "SI - Supervízia", "Hodiny": 3.0, "Miesto": "KC Šaľa", "Krajina": "Slovensko (SR)", "Datum_Akcie": "2026-11-08", "Cas": "10:00", "Stav": "Potvrdená", "Poznamka": "Fakturácia: 180"},
    {"ID": 5, "Datum_Vytvorenia": "2026-10-25 10:00", "Sluzba": "SI - Supervízia", "Hodiny": 5.0, "Miesto": "DSS Javorník", "Krajina": "Slovensko (SR)", "Datum_Akcie": "2026-11-10", "Cas": "09:00", "Stav": "Nová", "Poznamka": "Fakturácia: 300"},
    {"ID": 6, "Datum_Vytvorenia": "2026-10-25 10:15", "Sluzba": "SI - Supervízia", "Hodiny": 25.0, "Miesto": "Pezinok OSPOD", "Krajina": "Slovensko (SR)", "Datum_Akcie": "2026-11-15", "Cas": "08:30", "Stav": "Potvrdená", "Poznamka": "Dohoda, Fakturácia: 1500"},
    {"ID": 7, "Datum_Vytvorenia": "2026-10-25 10:30", "Sluzba": "SI - Supervízia", "Hodiny": 6.0, "Miesto": "CDR Pezinok", "Krajina": "Slovensko (SR)", "Datum_Akcie": "2026-11-18", "Cas": "09:00", "Stav": "Nová", "Poznamka": "Fakturácia: 360"},
    {"ID": 8, "Datum_Vytvorenia": "2026-10-25 10:45", "Sluzba": "SI - Supervízia", "Hodiny": 4.0, "Miesto": "KC Jelka", "Krajina": "Slovensko (SR)", "Datum_Akcie": "2026-11-20", "Cas": "10:00", "Stav": "Nová", "Poznamka": "Základný dopyt Jelka"},
    {"ID": 9, "Datum_Vytvorenia": "2026-10-25 11:00", "Sluzba": "SI - Supervízia", "Hodiny": 10.0, "Miesto": "Partizánske", "Krajina": "Slovensko (SR)", "Datum_Akcie": "2026-11-22", "Cas": "09:00", "Stav": "Potvrdená", "Poznamka": "Fakturácia: 600"}
]

def load_data():
    if os.path.exists(DATA_FILE):
        df = pd.read_csv(DATA_FILE)
        if df.empty or 'ID' not in df.columns:
            df = pd.DataFrame(INITIAL_DATA)
            df.to_csv(DATA_FILE, index=False)
        return df
    else:
        df = pd.DataFrame(INITIAL_DATA)
        df.to_csv(DATA_FILE, index=False)
        return df

def save_data(df):
    df.to_csv(DATA_FILE, index=False)

if "dopyty" not in st.session_state:
    st.session_state.dopyty = load_data()

# Čistý dizajn ladiaci so svetlým rozhraním aplikácie
st.markdown("""
    <style>
    .card { background-color: #f8f9fa; padding: 18px; border-radius: 10px; margin-bottom: 12px; border: 1px solid #e0e0e0; border-left: 5px solid #ff4b4b; }
    .card h4 { margin-top: 0; color: #262730; }
    </style>
""", unsafe_allow_html=True)

st.title("💼 Asistent Štefana Šarközyho")

tabs = st.tabs(["📋 Dopyty", "➕ Nová požiadavka", "📊 Pipeline", "👥 Klienti", "⚙️ Nastavenia"])

with tabs[0]:
    st.header("📋 Zoznam zaznamenaných dopytov")
    df = st.session_state.dopyty
    
    col_m1, col_m2, col_m3 = st.columns(3)
    col_m1.metric("Celkom dopytov", len(df))
    col_m2.metric("Nové dopyty", len(df[df["Stav"] == "Nová"]))
    col_m3.metric("Potvrdené", len(df[df["Stav"] == "Potvrdená"]))
    
    st.divider()
    
    if df.empty:
        st.info("Zatiaľ neboli zaznamenané žiadne dopyty.")
    else:
        for idx, row in df.iterrows():
            st.markdown(f"""
            <div class="card">
                <h4>#{row['ID']} - {row['Sluzba']} ({row['Miesto']}, {row['Krajina']})</h4>
                <p><b>Termín:</b> {row['Datum_Akcie']} o {row['Cas']} | <b>Rozsah:</b> {row['Hodiny']} hod. | <b>Stav:</b> <b>{row['Stav']}</b></p>
                <p><i>{row['Poznamka']}</i></p>
            </div>
            """, unsafe_allow_html=True)

        st.subheader("⚙️ Spracovanie a zmena stavu")
        selected_id = st.selectbox("Vyberte dopyt na úpravu (ID):", df["ID"].tolist())
        if selected_id:
            row = df[df["ID"] == selected_id].iloc[0]
            novy_stav = st.selectbox("Zmeniť stav dopytu:", ["Nová", "V riešení", "Potvrdená", "Kalendár", "Vybavené", "Zrušená"], index=["Nová", "V riešení", "Potvrdená", "Kalendár", "Vybavené", "Zrušená"].index(row['Stav']) if row['Stav'] in ["Nová", "V riešení", "Potvrdená", "Kalendár", "Vybavené", "Zrušená"] else 0)
            if st.button("💾 Uložiť nový stav"):
                st.session_state.dopyty.loc[st.session_state.dopyty["ID"] == selected_id, "Stav"] = novy_stav
                save_data(st.session_state.dopyty)
                st.success("Stav dopytu bol aktualizovaný!")
                st.rerun()

with tabs[1]:
    st.header("1. Služby a bloky")
    sluzba = st.selectbox("Služba", ["SI - Supervízia", "SK - Kolektívna supervízia", "Krízová intervencia", "Koučing", "Vzdelávanie / Lektorovanie"])
    hodiny = st.number_input("Hodiny", min_value=1.0, max_value=50.0, value=4.0, step=0.5)

    st.header("2. Voľný termín a logistika (z Dúbravky)")
    col1, col2 = st.columns(2)
    with col1:
        krajina = st.radio("Krajina výjazdu", ["Slovensko (SR)", "Česká republika (ČR)"], horizontal=True)
    with col2:
        miesto = st.text_input("Miesto / Obec (voľný text)", value="Jelka")

    col_d, col_t = st.columns(2)
    with col_d:
        datum_akcie = st.date_input("Dátum konania", datetime.now())
    with col_t:
        cas_akcie = st.time_input("Čas začiatku", datetime.now().time())

    poznamka = st.text_area("Poznámka / Fakturácia", "")

    if st.button("💾 Uložiť dopyt do zoznamu", type="primary"):
        novy_id = int(st.session_state.dopyty["ID"].max() + 1) if not st.session_state.dopyty.empty else 1
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
        st.success(f"Dopyt pre '{miesto}' bol uložený pod ID {novy_id}!")
        st.rerun()

with tabs[2]:
    st.header("📊 Prehľad stavov (Pipeline)")
    if not st.session_state.dopyty.empty:
        st.bar_chart(st.session_state.dopyty["Stav"].value_counts())
    else:
        st.info("Žiadne dáta v pipeline.")

with tabs[3]:
    st.header("👥 Klienti a partneri")
    st.info("Modul pre správu kontaktov a inštitúcií.")

with tabs[4]:
    st.header("⚙️ Nastavenia aplikácie")
    st.write(f"Dátový súbor: `{DATA_FILE}`")
    if st.button("🔄 Obnoviť pôvodné testovacie dáta"):
        df_init = pd.DataFrame(INITIAL_DATA)
        save_data(df_init)
        st.session_state.dopyty = df_init
        st.success("Testovacie dáta boli obnovené!")
        st.rerun()
