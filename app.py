import streamlit as st
import pandas as pd
import os
from datetime import datetime

st.set_page_config(page_title="Asistent Štefana Šarközyho", layout="wide", page_icon="💼")

DATA_FILE = "dopyty.csv"

INITIAL_DATA = [
    {"ID": 1, "Datum_Vytvorenia": "2026-10-25 09:00", "Sluzba": "supv", "Hodiny": 4.0, "Miesto": "Cífer", "Krajina": "Slovensko (SR)", "Datum_Akcie": "2026-11-02", "Cas": "09:00", "Cestovny_Cas": 1.0, "Odchod": "08:00", "Stav": "Nová", "Poznamka": "p | Fakturácia: 240"},
    {"ID": 2, "Datum_Vytvorenia": "2026-10-25 09:15", "Sluzba": "supv", "Hodiny": 4.0, "Miesto": "CDR piešťany", "Krajina": "Slovensko (SR)", "Datum_Akcie": "2026-11-04", "Cas": "10:00", "Cestovny_Cas": 1.5, "Odchod": "08:30", "Stav": "Nová", "Poznamka": "p | Fakturácia: 240"},
    {"ID": 3, "Datum_Vytvorenia": "2026-10-25 09:30", "Sluzba": "supv", "Hodiny": 4.0, "Miesto": "KC Príbeta", "Krajina": "Slovensko (SR)", "Datum_Akcie": "2026-11-06", "Cas": "09:30", "Cestovny_Cas": 2.0, "Odchod": "07:30", "Stav": "V riešení", "Poznamka": "o | dohoda | Fakturácia: 240"},
    {"ID": 4, "Datum_Vytvorenia": "2026-10-25 09:45", "Sluzba": "supv", "Hodiny": 3.0, "Miesto": "KC Šaľa", "Krajina": "Slovensko (SR)", "Datum_Akcie": "2026-11-08", "Cas": "10:00", "Cestovny_Cas": 1.0, "Odchod": "09:00", "Stav": "Potvrdená", "Poznamka": "p | Fakturácia: 180"},
    {"ID": 5, "Datum_Vytvorenia": "2026-10-25 10:00", "Sluzba": "supv", "Hodiny": 5.0, "Miesto": "dss javirinska", "Krajina": "Slovensko (SR)", "Datum_Akcie": "2026-11-10", "Cas": "09:00", "Cestovny_Cas": 1.5, "Odchod": "07:30", "Stav": "Nová", "Poznamka": "p | Fakturácia: 300"},
    {"ID": 6, "Datum_Vytvorenia": "2026-10-25 10:15", "Sluzba": "supv", "Hodiny": 25.0, "Miesto": "pezinok Ospod", "Krajina": "Slovensko (SR)", "Datum_Akcie": "2026-11-15", "Cas": "08:30", "Cestovny_Cas": 0.5, "Odchod": "08:00", "Stav": "Potvrdená", "Poznamka": "p | dohoda | Fakturácia: 1500"},
    {"ID": 7, "Datum_Vytvorenia": "2026-10-25 10:30", "Sluzba": "supv", "Hodiny": 6.0, "Miesto": "CDR pezinok", "Krajina": "Slovensko (SR)", "Datum_Akcie": "2026-11-18", "Cas": "09:00", "Cestovny_Cas": 0.5, "Odchod": "08:30", "Stav": "Nová", "Poznamka": "p | Fakturácia: 360"},
    {"ID": 8, "Datum_Vytvorenia": "2026-10-25 10:45", "Sluzba": "supv", "Hodiny": 4.0, "Miesto": "Kc Jelka", "Krajina": "Slovensko (SR)", "Datum_Akcie": "2026-11-20", "Cas": "10:00", "Cestovny_Cas": 1.0, "Odchod": "09:00", "Stav": "Nová", "Poznamka": "Základný dopyt Jelka"},
    {"ID": 9, "Datum_Vytvorenia": "2026-10-25 11:00", "Sluzba": "supv", "Hodiny": 10.0, "Miesto": "Partizanske", "Krajina": "Slovensko (SR)", "Datum_Akcie": "2026-11-22", "Cas": "09:00", "Cestovny_Cas": 2.0, "Odchod": "07:00", "Stav": "Potvrdená", "Poznamka": "p | Fakturácia: 600"}
]

def load_data():
    if os.path.exists(DATA_FILE):
        df = pd.read_csv(DATA_FILE)
        if df.empty or 'ID' not in df.columns:
            df = pd.DataFrame(INITIAL_DATA)
            df.to_csv(DATA_FILE, index=False)
        # Bezpečná kontrola nových stĺpcov pre cestovanie
        if 'Cestovny_Cas' not in df.columns:
            df['Cestovny_Cas'] = 1.0
        if 'Odchod' not in df.columns:
            df['Odchod'] = "08:00"
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
    .card-calendar { background-color: #f0f7f4; padding: 16px; border-radius: 10px; margin-bottom: 12px; border: 1px solid #d0e8df; border-left: 5px solid #28a745; }
    .card h4 { margin-top: 0; color: #262730; }
    </style>
""", unsafe_allow_html=True)

st.title("💼 Asistent Štefana Šarközyho")

tabs_options = ["📋 Dopyty", "➕ Nová požiadavka", "📅 Kalendár", "📊 Pipeline", "👥 Klienti", "⚙️ Nastavenia"]
current_index = tabs_options.index(st.session_state.active_tab) if st.session_state.active_tab in tabs_options else 0

selected_tab = st.radio("Navigácia", tabs_options, index=current_index, horizontal=True, label_visibility="collapsed")
st.session_state.active_tab = selected_tab

st.divider()

if selected_tab == "📋 Dopyty":
    st.header("📋 Zoznam zaznamenaných dopytov")
    df = st.session_state.dopyty
    
    # Zobrazujeme len tie, čo nie sú v kalendári/vybavené (alebo všetky podľa výberu)
    active_df = df[df["Stav"] != "Kalendár"]
    
    col_m1, col_m2, col_m3 = st.columns(3)
    col_m1.metric("Celkom dopytov", len(active_df))
    col_m2.metric("Nové dopyty", len(active_df[active_df["Stav"] == "Nová"]))
    col_m3.metric("Potvrdené", len(active_df[active_df["Stav"] == "Potvrdená"]))
    
    st.divider()
    
    if active_df.empty:
        st.info("Zatiaľ neboli zaznamenané žiadne aktívne dopyty.")
    else:
        for idx, row in active_df.iterrows():
            c_info, c_btn = st.columns([4, 1])
            
            with c_info:
                st.markdown(f"""
                <div class="card">
                    <h4>#{row['ID']} - {row['Sluzba']} ({row['Miesto']}, {row['Krajina']})</h4>
                    <p><b>Termín:</b> {row['Datum_Akcie']} o {row['Cas']} | <b>Rozsah:</b> {row['Hodiny']} hod. | <b>Cesta:</b> {row.get('Cestovny_Cas', 1.0)} hod. (Odchod: {row.get('Odchod', '08:00')})</p>
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
        st.info("Upravte čas, logistiku a potvrďte pre presun do kalendára.")
    else:
        st.header("➕ Nová požiadavka")

    default_sluzba = item['Sluzba'] if item and 'Sluzba' in item else "supv"
    default_hodiny = float(item['Hodiny']) if item and 'Hodiny' in item else 4.0
    default_krajina = item['Krajina'] if item and 'Krajina' in item else "Slovensko (SR)"
    default_miesto = item['Miesto'] if item and 'Miesto' in item else ""
    default_cesta = float(item.get('Cestovny_Cas', 1.0)) if item else 1.0
    
    try:
        default_datum = datetime.strptime(str(item['Datum_Akcie']), "%Y-%m-%d").date() if item and pd.notna(item.get('Datum_Akcie')) else datetime.now().date()
    except:
        default_datum = datetime.now().date()

    try:
        default_cas = datetime.strptime(str(item['Cas']), "%H:%M").time() if item and pd.notna(item.get('Cas')) else datetime.now().time()
    except:
        default_cas = datetime.now().time()

    try:
        default_odchod = datetime.strptime(str(item.get('Odchod', '08:00')), "%H:%M").time() if item else datetime.now().time()
    except:
        default_odchod = datetime.now().time()

    default_poznamka = item['Poznamka'] if item and 'Poznamka' in item else ""

    sluzba = st.selectbox("Služba", ["supv", "SI - Supervízia", "SK - Kolektívna supervízia", "Krízová intervencia", "Koučing"], index=0 if default_sluzba=="supv" else 1)
    
    col_h1, col_h2 = st.columns(2)
    with col_h1:
        hodiny = st.number_input("Trvanie akcie (hodiny)", min_value=1.0, max_value=50.0, value=default_hodiny, step=0.5)
    with col_h2:
        cestovny_cas = st.number_input("Cestovný čas (hod. z Dúbravky)", min_value=0.0, max_value=10.0, value=default_cesta, step=0.5)

    col1, col2 = st.columns(2)
    with col1:
        krajina = st.radio("Krajina výjazdu", ["Slovensko (SR)", "Česká republika (ČR)"], horizontal=True, index=0 if default_krajina=="Slovensko (SR)" else 1)
    with col2:
        miesto = st.text_input("Miesto / Obec (voľný text)", value=default_miesto)

    col_d, col_t1, col_t2 = st.columns(3)
    with col_d:
        datum_akcie = st.date_input("Dátum konania", value=default_datum)
    with col_t1:
        cas_akcie = st.time_input("Začiatok akcie", value=default_cas)
    with col_t2:
        cas_odchodu = st.time_input("Odchod z Dúbravky", value=default_odchod)

    poznamka = st.text_area("Poznámka / Fakturácia", value=default_poznamka)

    btn_label = "💾 Dokončiť a presunúť do Kalendára" if item else "💾 Uložiť dopyt do zoznamu"
    if st.button(btn_label, type="primary"):
        if item:
            # Aktualizujeme stav na "Kalendár" namiesto vymazania, aby sa zobrazil v kalendári
            idx = st.session_state.dopyty[st.session_state.dopyty["ID"] == item['ID']].index
            st.session_state.dopyty.loc[idx, "Stav"] = "Kalendár"
            st.session_state.dopyty.loc[idx, "Sluzba"] = sluzba
            st.session_state.dopyty.loc[idx, "Hodiny"] = hodiny
            st.session_state.dopyty.loc[idx, "Miesto"] = miesto
            st.session_state.dopyty.loc[idx, "Krajina"] = krajina
            st.session_state.dopyty.loc[idx, "Datum_Akcie"] = str(datum_akcie)
            st.session_state.dopyty.loc[idx, "Cas"] = str(cas_akcie)
            st.session_state.dopyty.loc[idx, "Cestovny_Cas"] = cestovny_cas
            st.session_state.dopyty.loc[idx, "Odchod"] = str(cas_odchodu.strftime("%H:%M"))
            st.session_state.dopyty.loc[idx, "Poznamka"] = poznamka
            
            save_data(st.session_state.dopyty)
            st.session_state.edit_item = None
            st.success(f"Dopyt #{item['ID']} ({miesto}) bol presunutý do kalendára!")
            st.session_state.active_tab = "📅 Kalendár"
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
                "Cestovny_Cas": cestovny_cas,
                "Odchod": str(cas_odchodu.strftime("%H:%M")),
                "Stav": "Nová",
                "Poznamka": poznamka
            }
            st.session_state.dopyty = pd.concat([st.session_state.dopyty, pd.DataFrame([novy_riadok])], ignore_index=True)
            save_data(st.session_state.dopyty)
            st.success(f"Dopyt pre '{miesto}' bol uložený pod ID {novy_id}!")
            st.session_state.active_tab = "📋 Dopyty"
        
        st.rerun()

elif selected_tab == "📅 Kalendár":
    st.header("📅 Kalendár potvrdených výjazdov a akcií")
    df = st.session_state.dopyty
    cal_df = df[df["Stav"] == "Kalendár"].sort_values(by="Datum_Akcie")
    
    if cal_df.empty:
        st.info("Zatiaľ žiadne položky v kalendári. Spracujte dopyty zo záložky Dopyty.")
    else:
        for idx, row in cal_df.iterrows():
            st.markdown(f"""
            <div class="card-calendar">
                <h4>📅 {row['Datum_Akcie']} o {row['Cas']} — {row['Sluzba']} ({row['Miesto']}, {row['Krajina']})</h4>
                <p><b>Logistika z Dúbravky:</b> Odchod o <b>{row.get('Odchod', '08:00')}</b> | Cesta: {row.get('Cestovny_Cas', 1.0)} hod. | <b>Trvanie:</b> {row['Hodiny']} hod.</p>
                <p><i>{row['Poznamka']}</i></p>
            </div>
            """, unsafe_allow_html=True)

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
