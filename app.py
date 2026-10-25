import streamlit as st
import pandas as pd
import os
from datetime import datetime, time

st.set_page_config(page_title="Asistent Štefana Šarközyho", layout="wide", page_icon="💼")

DATA_FILE = "dopyty.csv"

INITIAL_DATA = [
    {"ID": 1, "Datum_Vytvorenia": "2026-10-25 10:15", "Sluzby": "SI - individuálna supervízia", "Hodiny": 4.0, "Miesto": "Cífer", "Krajina": "Slovensko (SR)", "Datum_Akcie": "2026-11-02", "Cas": "09:00", "Cestovny_Cas": 1.0, "Odchod": "08:00", "Cena_Sluzby": 240.0, "Cena_Cestovne": 0.0, "Stav": "Nová", "Poznamka": "p | Fakturácia: 240"},
    {"ID": 2, "Datum_Vytvorenia": "2026-10-25 10:20", "Sluzby": "SI - individuálna supervízia", "Hodiny": 4.0, "Miesto": "CDR piešťany", "Krajina": "Slovensko (SR)", "Datum_Akcie": "2026-11-04", "Cas": "10:00", "Cestovny_Cas": 1.5, "Odchod": "08:30", "Cena_Sluzby": 240.0, "Cena_Cestovne": 0.0, "Stav": "Nová", "Poznamka": "p | Fakturácia: 240"},
    {"ID": 3, "Datum_Vytvorenia": "2026-10-25 10:25", "Sluzby": "SI - individuálna supervízia", "Hodiny": 4.0, "Miesto": "KC Príbeta", "Krajina": "Slovensko (SR)", "Datum_Akcie": "2026-11-06", "Cas": "09:30", "Cestovny_Cas": 2.0, "Odchod": "07:30", "Cena_Sluzby": 240.0, "Cena_Cestovne": 0.0, "Stav": "Nová", "Poznamka": "o | dohoda | Fakturácia: 240"},
    {"ID": 4, "Datum_Vytvorenia": "2026-10-25 10:30", "Sluzby": "SI - individuálna supervízia", "Hodiny": 3.0, "Miesto": "KC Šaľa", "Krajina": "Slovensko (SR)", "Datum_Akcie": "2026-11-08", "Cas": "10:00", "Cestovny_Cas": 1.0, "Odchod": "09:00", "Cena_Sluzby": 180.0, "Cena_Cestovne": 0.0, "Stav": "Nová", "Poznamka": "p | Fakturácia: 180"},
    {"ID": 5, "Datum_Vytvorenia": "2026-10-25 10:35", "Sluzby": "SI - individuálna supervízia", "Hodiny": 5.0, "Miesto": "dss javirinska", "Krajina": "Slovensko (SR)", "Datum_Akcie": "2026-11-10", "Cas": "09:00", "Cestovny_Cas": 1.5, "Odchod": "07:30", "Cena_Sluzby": 300.0, "Cena_Cestovne": 0.0, "Stav": "Nová", "Poznamka": "p | Fakturácia: 300"},
    {"ID": 6, "Datum_Vytvorenia": "2026-10-25 10:40", "Sluzby": "SI - individuálna supervízia", "Hodiny": 25.0, "Miesto": "pezinok Ospod", "Krajina": "Slovensko (SR)", "Datum_Akcie": "2026-11-15", "Cas": "08:30", "Cestovny_Cas": 0.5, "Odchod": "08:00", "Cena_Sluzby": 1500.0, "Cena_Cestovne": 0.0, "Stav": "Nová", "Poznamka": "p | dohoda | Fakturácia: 1500"},
    {"ID": 7, "Datum_Vytvorenia": "2026-10-25 10:45", "Sluzby": "SI - individuálna supervízia", "Hodiny": 6.0, "Miesto": "CDR pezinok", "Krajina": "Slovensko (SR)", "Datum_Akcie": "2026-11-18", "Cas": "09:00", "Cestovny_Cas": 0.5, "Odchod": "08:30", "Cena_Sluzby": 360.0, "Cena_Cestovne": 0.0, "Stav": "Nová", "Poznamka": "p | Fakturácia: 360"},
    {"ID": 8, "Datum_Vytvorenia": "2026-10-25 10:50", "Sluzby": "SI - individuálna supervízia", "Hodiny": 4.0, "Miesto": "Kc Jelka", "Krajina": "Slovensko (SR)", "Datum_Akcie": "2026-11-05", "Cas": "09:00", "Cestovny_Cas": 1.0, "Odchod": "08:00", "Cena_Sluzby": 0.0, "Cena_Cestovne": 0.0, "Stav": "Nová", "Poznamka": "Testovací dopyt Jelka"},
    {"ID": 9, "Datum_Vytvorenia": "2026-10-25 10:55", "Sluzby": "SI - individuálna supervízia", "Hodiny": 10.0, "Miesto": "Partizanske", "Krajina": "Slovensko (SR)", "Datum_Akcie": "2026-11-22", "Cas": "09:00", "Cestovny_Cas": 2.0, "Odchod": "07:00", "Cena_Sluzby": 600.0, "Cena_Cestovne": 0.0, "Stav": "Nová", "Poznamka": "p | Fakturácia: 600"}
]

def load_data():
    if os.path.exists(DATA_FILE):
        df = pd.read_csv(DATA_FILE)
        if df.empty or 'ID' not in df.columns:
            df = pd.DataFrame(INITIAL_DATA)
            df.to_csv(DATA_FILE, index=False)
        if 'Cestovny_Cas' not in df.columns:
            df['Cestovny_Cas'] = 1.0
        if 'Odchod' not in df.columns:
            df['Odchod'] = "08:00"
        if 'Cena_Sluzby' not in df.columns:
            df['Cena_Sluzby'] = df.get('Cena_Fakturacia', 0.0)
        if 'Cena_Cestovne' not in df.columns:
            df['Cena_Cestovne'] = 0.0
        if 'Sluzby' not in df.columns and 'Sluzba' in df.columns:
            df['Sluzby'] = df['Sluzba']
        return df
    else:
        df = pd.DataFrame(INITIAL_DATA)
        df.to_csv(DATA_FILE, index=False)
        return df

def save_data(df):
    df.to_csv(DATA_FILE, index=False)

def sync_to_google_calendar_automatically(row):
    pass

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
    .box-section { background-color: #f1f3f5; padding: 15px; border-radius: 8px; border: 1px solid #ced4da; margin-bottom: 15px; }
    </style>
""", unsafe_allow_html=True)

st.title("💼 Asistent Štefana Šarközyho")

tabs_options = ["📋 Dopyty", "➕ Nová požiadavka", "📅 Kalendár", "📊 Pipeline", "👥 Klienti", "⚙️ Nastavenia"]
current_index = tabs_options.index(st.session_state.active_tab) if st.session_state.active_tab in tabs_options else 0

selected_tab = st.radio("Navigácia", tabs_options, index=current_index, horizontal=True, label_visibility="collapsed")
st.session_state.active_tab = selected_tab

st.divider()

all_available_services = [
    "SI - individuálna supervízia",
    "SS - skupinová supervízia",
    "KI - krízová intervencia",
    "K - koučing",
    "V - vzdelávanie"
]

if selected_tab == "📋 Dopyty":
    st.header("📋 Zoznam zaznamenaných dopytov")
    df = st.session_state.dopyty
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
            total_cena = float(row.get('Cena_Sluzby', 0.0)) + float(row.get('Cena_Cestovne', 0.0))
            with c_info:
                st.markdown(f"""
                <div class="card">
                    <h4>#{row['ID']} - {row['Sluzby']} ({row['Miesto']}, {row['Krajina']})</h4>
                    <p><b>Termín:</b> {row['Datum_Akcie']} o {row['Cas']} | <b>Rozsah:</b> {row['Hodiny']} hod. | <b>Cesta:</b> {row.get('Cestovny_Cas', 1.0)} hod. (Odchod: {row.get('Odchod', '08:00')}) | <b>Spolu:</b> {total_cena} € (Služby: {row.get('Cena_Sluzby', 0.0)} € + Cestovné: {row.get('Cena_Cestovne', 0.0)} €)</p>
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
        st.info("Kompletná logika formulára: kombinácie služieb, výpočet cien a cestovného bloku.")
    else:
        st.header("➕ Nová požiadavka")

    # Parsing existing services for multiselect
    raw_services = item['Sluzby'] if item and 'Sluzby' in item else ("SI - individuálna supervízia" if not (item and 'Sluzba' in item) else item['Sluzba'])
    default_selected_services = [s.strip() for s in str(raw_services).split("+")]
    default_selected_services = [s for s in default_selected_services if s in all_available_services]
    if not default_selected_services:
        default_selected_services = ["SI - individuálna supervízia"]

    default_hodiny = float(item['Hodiny']) if item and 'Hodiny' in item else 4.0
    default_krajina = item['Krajina'] if item and 'Krajina' in item else "Slovensko (SR)"
    default_miesto = item['Miesto'] if item and 'Miesto' in item else ""
    default_cesta = float(item.get('Cestovny_Cas', 1.0)) if item else 1.0
    default_cena_sluzby = float(item.get('Cena_Sluzby', item.get('Cena_Fakturacia', 0.0))) if item else 0.0
    default_cena_cestovne = float(item.get('Cena_Cestovne', 0.0)) if item else 0.0
    
    try:
        default_datum = datetime.strptime(str(item['Datum_Akcie']), "%Y-%m-%d").date() if item and pd.notna(item.get('Datum_Akcie')) else datetime.now().date()
    except Exception:
        default_datum = datetime.now().date()

    # Time parsing for start action
    try:
        t_parts = str(item['Cas']).split(":")
        def_h_akcia = int(t_parts[0])
        def_m_akcia = int(t_parts[1]) if len(t_parts) > 1 else 0
    except Exception:
        def_h_akcia, def_m_akcia = 9, 0

    # Time parsing for departure
    try:
        od_parts = str(item.get('Odchod', '08:00')).split(":")
        def_h_odchod = int(od_parts[0])
        def_m_odchod = int(od_parts[1]) if len(od_parts) > 1 else 0
    except Exception:
        def_h_odchod, def_m_odchod = 8, 0

    default_poznamka = item['Poznamka'] if item and 'Poznamka' in item else ""

    # 1. SEKCIA SLUŽIEB A KOMBINÁCIÍ
    st.markdown("### 🛠️ Služby a cenotvorba")
    selected_services = st.multiselect("Vyberte službu / kombináciu služieb pre výjazd", all_available_services, default=default_selected_services)
    
    col_s1, col_s2 = st.columns(2)
    with col_s1:
        hodiny = st.number_input("Trvanie akcie celkom (hodiny)", min_value=0.5, max_value=50.0, value=default_hodiny, step=0.5)
    with col_s2:
        cena_sluzby = st.number_input("Suma za služby (€)", min_value=0.0, max_value=10000.0, value=default_cena_sluzby, step=10.0)

    st.markdown("---")

    # 2. BLOK CESTOVNÉHO (HNEĎ POD SLUŽBAMI)
    st.markdown("### 🚗 Kompletný blok cestovného a logistiky z Dúbravky")
    col_c1, col_c2, col_c3 = st.columns(3)
    with col_c1:
        cestovny_cas = st.number_input("Cestovný čas (hod. z Dúbravky)", min_value=0.0, max_value=10.0, value=default_cesta, step=0.5)
    with col_c2:
        cena_cestovne = st.number_input("Cena za cestovné (€)", min_value=0.0, max_value=1000.0, value=default_cena_cestovne, step=5.0)
    with col_c3:
        st.markdown(f"**Cestovné spolu:** `{cena_cestovne} €`")

    st.markdown("---")

    # 3. CELKOVÝ SÚČET (SLUŽBY + CESTOVNÉ)
    celkova_suma = cena_sluzby + cena_cestovne
    st.markdown(f"""
    <div style="background-color: #e8f4f8; padding: 12px; border-radius: 8px; border: 1px solid #b8e0f2; margin-bottom: 15px;">
        <h4 style="margin: 0; color: #0277bd;">Súčet služieb ({cena_sluzby} €) + Cestovné ({cena_cestovne} €) = Celková suma: <b>{celkova_suma} €</b></h4>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        krajina = st.radio("Krajina výjazdu", ["Slovensko (SR)", "Česká republika (ČR)"], horizontal=True, index=0 if default_krajina=="Slovensko (SR)" else 1)
    with col2:
        miesto = st.text_input("Miesto / Obec (voľný text)", value=default_miesto)

    st.markdown("---")

    # 4. DÁTUM A ČASOVÉ POLOŽKY S KROKOVANÍM (+/-)
    st.markdown("### 📅 Dátum a časové krokovanie")
    col_d, col_t1, col_t2 = st.columns(3)
    with col_d:
        datum_akcie = st.date_input("Dátum konania", value=default_datum)
    
    with col_t1:
        st.markdown("**Začiatok akcie**")
        col_th1, col_tm1 = st.columns(2)
        with col_th1:
            h_akcia = st.number_input("Hodina", min_value=0, max_value=23, value=def_h_akcia, step=1, key="h_akcia")
        with col_tm1:
            m_akcia = st.number_input("Minúta", min_value=0, max_value=59, value=def_m_akcia, step=15, key="m_akcia")
            
    with col_t2:
        st.markdown("**Odchod z Dúbravky**")
        col_th2, col_tm2 = st.columns(2)
        with col_th2:
            h_odchod = st.number_input("Hodina", min_value=0, max_value=23, value=def_h_odchod, step=1, key="h_odchod")
        with col_tm2:
            m_odchod = st.number_input("Minúta", min_value=0, max_value=59, value=def_m_odchod, step=15, key="m_odchod")

    cas_akcie_str = f"{h_akcia:02d}:{m_akcia:02d}"
    cas_odchodu_str = f"{h_odchod:02d}:{m_odchod:02d}"

    st.markdown("---")
    poznamka = st.text_area("Poznámka", value=default_poznamka)

    combined_services_str = " + ".join(selected_services) if selected_services else "SI - individuálna supervízia"

    btn_label = "💾 Dokončiť a automaticky vytvoriť termín v Google Kalendári" if item else "💾 Uložiť dopyt do zoznamu"
    if st.button(btn_label, type="primary"):
        if item:
            idx = st.session_state.dopyty[st.session_state.dopyty["ID"] == item['ID']].index
            st.session_state.dopyty.loc[idx, "Stav"] = "Kalendár"
            st.session_state.dopyty.loc[idx, "Sluzby"] = combined_services_str
            st.session_state.dopyty.loc[idx, "Hodiny"] = hodiny
            st.session_state.dopyty.loc[idx, "Miesto"] = miesto
            st.session_state.dopyty.loc[idx, "Krajina"] = krajina
            st.session_state.dopyty.loc[idx, "Datum_Akcie"] = str(datum_akcie)
            st.session_state.dopyty.loc[idx, "Cas"] = cas_akcie_str
            st.session_state.dopyty.loc[idx, "Cestovny_Cas"] = cestovny_cas
            st.session_state.dopyty.loc[idx, "Odchod"] = cas_odchodu_str
            st.session_state.dopyty.loc[idx, "Cena_Sluzby"] = cena_sluzby
            st.session_state.dopyty.loc[idx, "Cena_Cestovne"] = cena_cestovne
            st.session_state.dopyty.loc[idx, "Poznamka"] = poznamka
            
            save_data(st.session_state.dopyty)
            sync_to_google_calendar_automatically(st.session_state.dopyty.loc[idx])
            
            st.session_state.edit_item = None
            st.success(f"Dopyt #{item['ID']} ({miesto}) bol úspešne spracovaný a prenesený do kalendára!")
            st.session_state.active_tab = "📅 Kalendár"
        else:
            novy_id = int(st.session_state.dopyty["ID"].max() + 1) if not st.session_state.dopyty.empty else 1
            novy_riadok = {
                "ID": novy_id,
                "Datum_Vytvorenia": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "Sluzby": combined_services_str,
                "Hodiny": hodiny,
                "Miesto": miesto,
                "Krajina": krajina,
                "Datum_Akcie": str(datum_akcie),
                "Cas": cas_akcie_str,
                "Cestovny_Cas": cestovny_cas,
                "Odchod": cas_odchodu_str,
                "Cena_Sluzby": cena_sluzby,
                "Cena_Cestovne": cena_cestovne,
                "Stav": "Nová",
                "Poznamka": poznamka
            }
            st.session_state.dopyty = pd.concat([st.session_state.dopyty, pd.DataFrame([novy_riadok])], ignore_index=True)
            save_data(st.session_state.dopyty)
            st.success(f"Dopyt pre '{miesto}' bol uložený pod ID {novy_id}!")
            st.session_state.active_tab = "📋 Dopyty"
        
        st.rerun()

elif selected_tab == "📅 Kalendár":
    st.header("📅 Kalendár potvrdených termínov")
    df = st.session_state.dopyty
    cal_df = df[df["Stav"] == "Kalendár"].sort_values(by="Datum_Akcie")
    
    if cal_df.empty:
        st.info("Zatiaľ žiadne termíny v kalendári. Spracujte a dokončite dopyty zo záložky Dopyty.")
    else:
        for idx, row in cal_df.iterrows():
            total_cena = float(row.get('Cena_Sluzby', 0.0)) + float(row.get('Cena_Cestovne', 0.0))
            st.markdown(f"""
            <div class="card-calendar">
                <h4>📅 {row['Datum_Akcie']} o {row['Cas']} — {row['Sluzby']} ({row['Miesto']}, {row['Krajina']})</h4>
                <p><b>Logistika z Dúbravky:</b> Odchod o <b>{row.get('Odchod', '08:00')}</b> | Cesta: {row.get('Cestovny_Cas', 1.0)} hod. | <b>Trvanie:</b> {row['Hodiny']} hod.</p>
                <p><b>Fakturácia:</b> Služby ({row.get('Cena_Sluzby', 0.0)} €) + Cestovné ({row.get('Cena_Cestovne', 0.0)} €) = <b>Celkom {total_cena} €</b></p>
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
