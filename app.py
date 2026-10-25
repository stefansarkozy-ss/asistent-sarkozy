import streamlit as st
import pandas as pd
import os
from datetime import datetime

st.set_page_config(page_title="Asistent Štefana Šarközyho", layout="wide", page_icon="💼")

DATA_FILE = "dopyty.csv"

INITIAL_DATA = [
    {"ID": 1, "Datum_Vytvorenia": "2026-10-25 09:00", "Sluzba": "supv", "Hodiny": 4.0, "Miesto": "Cífer", "Krajina": "Slovensko (SR)", "Datum_Akcie": "2026-11-02", "Cas": "09:00", "Stav": "Nová", "Poznamka": "p | Fakturácia: 240"},
    {"ID": 2, "Datum_Vytvorenia": "2026-10-25 09:15", "Sluzba": "supv", "Hodiny": 4.0, "Miesto": "CDR piešťany", "Krajina": "Slovensko (SR)", "Datum_Akcie": "2026-11-04", "Cas": "10:00", "Stav": "Nová", "Poznamka": "p | Fakturácia: 240"},
    {"ID": 3, "Datum_Vytvorenia": "2026-10-25 09:30", "Sluzba": "supv", "Hodiny": 4.0, "Miesto": "KC Príbeta", "Krajina": "Slovensko (SR)", "Datum_Akcie": "2026-11-06", "Cas": "09:30", "Stav": "V riešení", "Poznamka": "o | dohoda | Fakturácia: 240"},
    {"ID": 4, "Datum_Vytvorenia": "2026-10-25 09:45", "Sluzba": "supv", "Hodiny": 3.0, "Miesto": "KC Šaľa", "Krajina": "Slovensko (SR)", "Datum_Akcie": "2026-11-08", "Cas": "10:00", "Stav": "Potvrdená", "Poznamka": "p | Fakturácia: 180"},
    {"ID": 5, "Datum_Vytvorenia": "2026-10-25 10:00", "Sluzba": "supv", "Hodiny": 5.0, "Miesto": "dss javirinska", "Krajina": "Slovensko (SR)", "Datum_Akcie": "2026-11-10", "Cas": "09:00", "Stav": "Nová", "Poznamka": "p | Fakturácia: 300"},
    {"ID": 6, "Datum_Vytvorenia": "2026-10-25 10:15", "Sluzba": "supv", "Hodiny": 25.0, "Miesto": "pezinok Ospod", "Krajina": "Slovensko (SR)", "Datum_Akcie": "2026-11-15", "Cas": "08:30", "Stav": "Potvrdená", "Poznamka": "p | dohoda | Fakturácia: 1500"},
    {"ID": 7, "Datum_Vytvorenia": "2026-10-25 10:30", "Sluzba": "supv", "Hodiny": 6.0, "Miesto": "CDR pezinok", "Krajina": "Slovensko (SR)", "Datum_Akcie": "2026-11-18", "Cas": "09:00", "Stav": "Nová", "Poznamka": "p | Fakturácia: 360"},
    {"ID": 8, "Datum_Vytvorenia": "2026-10-25 10:45", "Sluzba": "supv", "Hodiny": 4.0, "Miesto": "Kc Jelka", "Krajina": "Slovensko (SR)", "Datum_Akcie": "2026-11-20", "Cas": "10:00", "Stav": "Nová", "Poznamka": "Základný dopyt Jelka"},
    {"ID": 9, "Datum_Vytvorenia": "2026-10-25 11:00", "Sluzba": "supv", "Hodiny": 10.0, "Miesto": "Partizanske", "Krajina": "Slovensko (SR)", "Datum_Akcie": "2026-11-22", "Cas": "09:00", "Stav": "Potvrdená", "Poznamka": "p | Fakturácia: 600"}
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

if "active_tab" not in st.session_state:
    st.session_state.active_tab = "📋 Dopyty"

if "edit_item" not in st.session_state:
    st.session_state.edit_item = None

st.markdown("""
    <style>
    .card { background-color: #f8f9fa; padding: 16px; border-radius: 10px; margin-bottom: 12px; border: 1px solid #e0e0e0; border-left: 5px solid #ff4b4b; }
    .card h4 { margin-top: 0; color: #262730; }
    </style>
""", unsafe_allow_html=True)

st.title("💼 Asistent Štefana Šarközyho")

tabs_options = ["📋 Dopyty", "➕ Nová požiadavka", "📊 Pipeline", "👥 Klienti", "⚙️ Nastavenia"]
current_index = tabs_options.index(st.session_state.active_tab) if st.session_state.active_tab in tabs_options else 0

selected_tab = st.radio("Navigácia", tabs_options, index=current_index, horizontal=True, label_visibility="collapsed")
st.session_state.active_tab = selected_tab

st.divider()

if selected_tab == "📋 Dopyty":
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
            c_info, c_btn = st.columns([4, 1])
            
            with c_info:
                st.markdown(f"""
                <div class="card">
                    <h4>#{row['ID']} - {row['Sluzba']} ({row['Miesto']}, {row['Krajina']})</h4>
                    <p><b>Termín:</b> {row['Datum_Akcie']} o {row['Cas']} | <b>Rozsah:</b> {row['Hodiny']} hod. | <b>Stav:</b> <b>{row['Stav']}</b></p>
                    <p><i>{row['Poznamka']}</i></p>
                </div>
                """, unsafe_allow_html=True)
            
            with c_btn:
                st.write("") 
                st.write("")
                if st.button("📅 Spracovať", key=f"btn_proc_{row['ID']}"):
                    st.session_state.edit_item = row.to_dict()
                    st.session_state.active_tab = "➕ Nová požiadavka"
                    st.rerun()

elif selected_tab == "➕ Nová požiadavka":
    item = st.session_state.edit_item
    if item:
        st.header(f"⚙️ Dokončenie a úprava dopytu #{item['ID']} ({item['Miesto']})")
        st.info("Údaje boli predvyplnené z vybraného dopytu. Skontrolujte ich a uložte pre posun do kalendára/pipeline.")
    else:
        st.header("➕ Nová požiadavka")

    default_sluzba = item['Sluzba'] if item and 'Sluzba' in item else "supv"
    default_hodiny = float(item['Hodiny']) if item and 'Hodiny' in item else 4.0
    default_krajina = item['Krajina'] if item and 'Krajina' in item else "Slovensko (SR)"
    default_miesto = item['Miesto'] if item and 'Miesto' in item else ""
    
    try:
        default_datum = datetime.strptime(str(item['Datum_Akcie']), "%Y-%m-%d").date() if item and pd.notna(item.get('Datum_Akcie')) else datetime.now().date()
    except:
        default_datum = datetime.now().date()

    try:
        default_cas = datetime.strptime(str(item['Cas']), "%H:%M").time() if item and pd.notna(item.get('Cas')) else datetime.now().time()
    except:
        default_cas = datetime.now().time()

    default_poznamka = item['Poznamka'] if item and 'Poznamka' in item else ""

    sluzba = st.selectbox("Služba", ["supv", "SI - Supervízia", "SK - Kolektívna supervízia", "Krízová intervencia", "Koučing"], index=0 if default_sluzba=="supv" else 1)
    hodiny = st.number_input("Hodiny", min_value=1.0, max_value=50.0, value=default_hodiny, step=0.5)

    col1, col2 = st.columns(2)
    with col1:
        krajina = st.radio("Krajina výjazdu", ["Slovensko (SR)", "Česká republika (ČR)"], horizontal=True, index=0 if default_krajina=="Slovensko (SR)" else 1)
    with col2:
        miesto = st.text_input("Miesto / Obec (voľný text)", value=default_miesto)

    col_d, col_t = st.columns(2)
    with col_d:
        datum_akcie = st.date_input("Dátum konania", value=default_datum)
    with col_t:
        cas_akcie = st.time_input("Čas začiatku", value=default_cas)

    poznamka = st.text_area("Poznámka / Fakturácia", value=default_poznamka)

    btn_label = "💾 Dokončiť, vymazať z dopytov a posunúť do kalendára" if item else "💾 Uložiť dopyt do zoznamu"
    if st.button(btn_label, type="primary"):
        if item:
            st.session_state.dopyty = st.session_state.dopyty[st.session_state.dopyty["ID"] != item['ID']]
            save_data(st.session_state.dopyty)
            st.session_state.edit_item = None
            st.success(f"Dopyt #{item['ID']} ({miesto}) bol úspešne spracovaný!")
        else:
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
        
        st.session_state.active_tab = "📋 Dopyty"
        st.rerun()

elif selected_tab == "📊 Pipeline":
    st.header("📊 Prehľad stavov (Pipeline)")
    if not st.session_state.dopyty.empty:
        st.bar_chart(st.session_state.dopyty["Stav"].value_counts())
    else:
        st.info("Žiadne dáta v pipeline.")

elif selected_tab == "👥 Klienti":
    st.header("👥 Klienti a partneri")
    st.info("Modul pre správu kontaktov a inštitúcií.")

elif selected_tab == "⚙️ Nastavenia":
    st.header("⚙️ Nastavenia aplikácie")
    st.write(f"Dátový súbor: `{DATA_FILE}`")
    if st.button("🔄 Obnoviť pôvodné testovacie dáta"):
        df_init = pd.DataFrame(INITIAL_DATA)
        save_data(df_init)
        st.session_state.dopyty = df_init
        st.success("Testovacie dáta boli obnovené!")
        st.rerun()
