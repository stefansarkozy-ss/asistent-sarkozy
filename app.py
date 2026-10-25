import streamlit as st
import pandas as pd
import os
from datetime import datetime

st.set_page_config(page_title="Asistent Štefana Šarközyho", layout="wide", page_icon="💼")

DATA_FILE = "dopyty.csv"

INITIAL_DATA = [
    {"ID": 1, "Datum_Vytvorenia": "2026-10-25 10:15", "Sluzby": "SI - individuálna supervízia", "Hodiny": 4.0, "Miesto": "Cífer", "Krajina": "Slovensko (SR)", "Datum_Akcie": "2026-11-02", "Cas": "09:00", "Cestovny_Cas": 1.0, "Odchod": "08:00", "Cena_Sluzby": 220.0, "Cena_Cestovne": 45.0, "Ubytovanie": 0.0, "Strava": 0.0, "Km": 100, "Stav": "Nová", "Poznamka": "p | Fakturácia: 265"},
    {"ID": 2, "Datum_Vytvorenia": "2026-10-25 10:20", "Sluzby": "SI - individuálna supervízia", "Hodiny": 4.0, "Miesto": "CDR piešťany", "Krajina": "Slovensko (SR)", "Datum_Akcie": "2026-11-04", "Cas": "10:00", "Cestovny_Cas": 1.5, "Odchod": "08:30", "Cena_Sluzby": 220.0, "Cena_Cestovne": 85.0, "Ubytovanie": 0.0, "Strava": 0.0, "Km": 190, "Stav": "Nová", "Poznamka": "p | Fakturácia: 305"},
    {"ID": 3, "Datum_Vytvorenia": "2026-10-25 10:25", "Sluzby": "SI - individuálna supervízia", "Hodiny": 4.0, "Miesto": "KC Príbeta", "Krajina": "Slovensko (SR)", "Datum_Akcie": "2026-11-06", "Cas": "09:30", "Cestovny_Cas": 2.0, "Odchod": "07:30", "Cena_Sluzby": 220.0, "Cena_Cestovne": 120.0, "Ubytovanie": 0.0, "Strava": 0.0, "Km": 270, "Stav": "Nová", "Poznamka": "o | dohoda | Fakturácia: 340"},
    {"ID": 4, "Datum_Vytvorenia": "2026-10-25 10:30", "Sluzby": "SI - individuálna supervízia", "Hodiny": 3.0, "Miesto": "KC Šaľa", "Krajina": "Slovensko (SR)", "Datum_Akcie": "2026-11-08", "Cas": "10:00", "Cestovny_Cas": 1.0, "Odchod": "09:00", "Cena_Sluzby": 165.0, "Cena_Cestovne": 65.0, "Ubytovanie": 0.0, "Strava": 0.0, "Km": 150, "Stav": "Nová", "Poznamka": "p | Fakturácia: 230"},
    {"ID": 5, "Datum_Vytvorenia": "2026-10-25 10:35", "Sluzby": "SI - individuálna supervízia", "Hodiny": 5.0, "Miesto": "dss javirinska", "Krajina": "Slovensko (SR)", "Datum_Akcie": "2026-11-10", "Cas": "09:00", "Cestovny_Cas": 1.5, "Odchod": "07:30", "Cena_Sluzby": 275.0, "Cena_Cestovne": 20.0, "Ubytovanie": 0.0, "Strava": 0.0, "Km": 40, "Stav": "Nová", "Poznamka": "p | Fakturácia: 295"},
    {"ID": 6, "Datum_Vytvorenia": "2026-10-25 10:40", "Sluzby": "SI - individuálna supervízia", "Hodiny": 25.0, "Miesto": "pezinok Ospod", "Krajina": "Slovensko (SR)", "Datum_Akcie": "2026-11-15", "Cas": "08:30", "Cestovny_Cas": 0.5, "Odchod": "08:00", "Cena_Sluzby": 1375.0, "Cena_Cestovne": 25.0, "Ubytovanie": 0.0, "Strava": 0.0, "Km": 50, "Stav": "Nová", "Poznamka": "p | dohoda | Fakturácia: 1400"},
    {"ID": 7, "Datum_Vytvorenia": "2026-10-25 10:45", "Sluzby": "SI - individuálna supervízia", "Hodiny": 6.0, "Miesto": "CDR pezinok", "Krajina": "Slovensko (SR)", "Datum_Akcie": "2026-11-18", "Cas": "09:00", "Cestovny_Cas": 0.5, "Odchod": "08:30", "Cena_Sluzby": 330.0, "Cena_Cestovne": 25.0, "Ubytovanie": 0.0, "Strava": 0.0, "Km": 50, "Stav": "Nová", "Poznamka": "p | Fakturácia: 355"},
    {"ID": 8, "Datum_Vytvorenia": "2026-10-25 10:50", "Sluzby": "SI - individuálna supervízia", "Hodiny": 4.0, "Miesto": "Kc Jelka", "Krajina": "Slovensko (SR)", "Datum_Akcie": "2026-11-05", "Cas": "09:00", "Cestovny_Cas": 1.0, "Odchod": "08:00", "Cena_Sluzby": 220.0, "Cena_Cestovne": 40.0, "Ubytovanie": 0.0, "Strava": 0.0, "Km": 90, "Stav": "Nová", "Poznamka": "Testovací dopyt Jelka"},
    {"ID": 9, "Datum_Vytvorenia": "2026-10-25 10:55", "Sluzby": "SI - individuálna supervízia", "Hodiny": 10.0, "Miesto": "Partizanske", "Krajina": "Slovensko (SR)", "Datum_Akcie": "2026-11-22", "Cas": "09:00", "Cestovny_Cas": 2.0, "Odchod": "07:00", "Cena_Sluzby": 550.0, "Cena_Cestovne": 130.0, "Ubytovanie": 0.0, "Strava": 0.0, "Km": 290, "Stav": "Nová", "Poznamka": "p | Fakturácia: 680"}
]

HOURLY_RATES = {
    "SI - individuálna supervízia": 55.0,
    "SS - skupinová supervízia": 60.0,
    "KI - krízová intervencia": 60.0,
    "K - koučing": 60.0,
    "V - vzdelávanie": 60.0
}

DISTANCE_DATABASE = {
    "jelka": 90,
    "kc jelka": 90,
    "cífer": 100,
    "piešťany": 160,
    "cdr piešťany": 160,
    "kc príbeta": 220,
    "kc šaľa": 130,
    "dss javorinská": 20,
    "pezinok": 50,
    "pezinok ospod": 50,
    "cdr pezinok": 50,
    "partizánske": 290,
    "trnava": 90,
    "nitra": 180,
    "brno": 260,
    "praha": 660
}

LEGAL_AMORTIZATION_PER_KM = 0.313 

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
        if 'Ubytovanie' not in df.columns:
            df['Ubytovanie'] = 0.0
        if 'Strava' not in df.columns:
            df['Strava'] = 0.0
        if 'Km' not in df.columns:
            df['Km'] = 0
        if 'Sluzby' not in df.columns and 'Sluzba' in df.columns:
            df['Sluzby'] = df['Sluzba']
        return df
    else:
        df = pd.DataFrame(INITIAL_DATA)
        df.to_csv(DATA_FILE, index=False)
        return df

def save_data(df):
    df.to_csv(DATA_FILE, index=False)

if "dopyty" not in st.session_state:
    st.session_state.dopyty = load_data()

if "menu_tab" not in st.session_state:
    st.session_state.menu_tab = "Dopyty"

if "edit_item" not in st.session_state:
    st.session_state.edit_item = None

if "service_blocks" not in st.session_state:
    st.session_state.service_blocks = [{"sluzba": "SI - individuálna supervízia", "hodiny": 4.0}]

st.markdown("""
    <style>
    .card { background-color: #f8f9fa; padding: 16px; border-radius: 10px; margin-bottom: 12px; border: 1px solid #e0e0e0; border-left: 5px solid #ff4b4b; }
    .card-calendar { background-color: #f0f7f4; padding: 16px; border-radius: 10px; margin-bottom: 12px; border: 1px solid #d0e8df; border-left: 5px solid #28a745; }
    .card h4 { margin-top: 0; color: #262730; }
    .calc-box { background-color: #eef7fc; padding: 15px; border-radius: 8px; border: 1px solid #bce0fd; margin: 10px 0; }
    </style>
""", unsafe_allow_html=True)

st.title("💼 Asistent Štefana Šarközyho")

tabs_options = ["Dopyty", "Nová", "Pipeline", "Klienti", "AI Engine", "Export"]

if st.session_state.menu_tab not in tabs_options:
    st.session_state.menu_tab = "Dopyty"

current_index = tabs_options.index(st.session_state.menu_tab)

selected_tab = st.radio("Navigácia", tabs_options, index=current_index, horizontal=True, label_visibility="collapsed")
st.session_state.menu_tab = selected_tab

st.divider()

all_available_services = list(HOURLY_RATES.keys())

if st.session_state.menu_tab == "Dopyty":
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
            total_cena = round(float(row.get('Cena_Sluzby', 0.0)) + float(row.get('Cena_Cestovne', 0.0)) + float(row.get('Ubytovanie', 0.0)) + float(row.get('Strava', 0.0)), 2)
            with c_info:
                card_html = (
                    f"<div class='card'>"
                    f"<h4>#{row['ID']} - {row['Sluzby']} ({row['Miesto']}, {row['Krajina']})</h4>"
                    f"<p><b>Termín:</b> {row['Datum_Akcie']} o {row['Cas']} | <b>Rozsah:</b> {row['Hodiny']} hod. | "
                    f"<b>Cesta:</b> {row.get('Cestovny_Cas', 1.0)} hod. (Odchod: {row.get('Odchod', '08:00')}) | "
                    f"<b>Spolu:</b> {total_cena} € (Služby: {row.get('Cena_Sluzby', 0.0)} € + Cestovné: {row.get('Cena_Cestovne', 0.0)} €)</p>"
                    f"<p><i>{row['Poznamka']}</i></p>"
                    f"</div>"
                )
                st.markdown(card_html, unsafe_allow_html=True)
            
            with c_btn:
                st.write("") 
                st.write("")
                if st.button("📅 Spracovať", key=f"btn_proc_{row['ID']}"):
                    st.session_state.edit_item = row.to_dict()
                    srv_str = row['Sluzby']
                    parts = [p.strip() for p in str(srv_str).split("+")]
                    total_h = float(row['Hodiny'])
                    h_per_part = total_h / max(1, len(parts))
                    
                    st.session_state.service_blocks = [{
                        "sluzba": p if p in all_available_services else all_available_services[0], 
                        "hodiny": h_per_part
                    } for p in parts]
                    
                    for i in range(len(parts)):
                        if f"cena_{i}" in st.session_state:
                            del st.session_state[f"cena_{i}"]
                        if f"last_hod_{i}" in st.session_state:
                            del st.session_state[f"last_hod_{i}"]
                        if f"last_serv_{i}" in st.session_state:
                            del st.session_state[f"last_serv_{i}"]

                    st.session_state.menu_tab = "Nová"
                    st.rerun()

elif st.session_state.menu_tab == "Nová":
    item = st.session_state.edit_item
    if item:
        st.header(f"⚙️ Dokončenie a úprava dopytu #{item['ID']} ({item['Miesto']})")
    else:
        st.header("➕ Nová požiadavka")

    default_krajina = item['Krajina'] if item and 'Krajina' in item else "Slovensko (SR)"
    default_miesto = item['Miesto'] if item and 'Miesto' in item else ""
    default_cesta = float(item.get('Cestovny_Cas', 1.0)) if item else 1.0
    default_ubytovanie = float(item.get('Ubytovanie', 0.0)) if item else 0.0
    default_strava = float(item.get('Strava', 0.0)) if item else 0.0
    
    try:
        default_datum = datetime.strptime(str(item['Datum_Akcie']), "%Y-%m-%d").date() if item and pd.notna(item.get('Datum_Akcie')) else datetime.now().date()
    except Exception:
        default_datum = datetime.now().date()

    try:
        t_parts = str(item['Cas']).split(":")
        def_h_akcia = int(t_parts[0])
        def_m_akcia = int(t_parts[1]) if len(t_parts) > 1 else 0
    except Exception:
        def_h_akcia, def_m_akcia = 9, 0

    try:
        od_parts = str(item.get('Odchod', '08:00')).split(":")
        def_h_odchod = int(od_parts[0])
        def_m_odchod = int(od_parts[1]) if len(od_parts) > 1 else 0
    except Exception:
        def_h_odchod, def_m_odchod = 8, 0

    default_poznamka = item['Poznamka'] if item and 'Poznamka' in item else ""

    # SEKCIA 1: MIESTO A AUTOMATICKÉ KM
    st.markdown("### 📍 Miesto a automatická lokalizácia")
    col_l1, col_l2 = st.columns(2)
    with col_l1:
        krajina = st.radio("Krajina výjazdu", ["Slovensko (SR)", "Česká republika (ČR)"], horizontal=True, index=0 if default_krajina=="Slovensko (SR)" else 1)
    with col_l2:
        miesto = st.text_input("Miesto / Obec (z Dúbravky)", value=default_miesto)

    lookup_key = miesto.strip().lower()
    auto_km_base = DISTANCE_DATABASE.get(lookup_key, int(item.get('Km', 60)) if item else 60)

    # Reaktívna správa kilometrov pri zmene miesta
    km_key = "vzdialenost_km_val"
    if "last_miesto_val" not in st.session_state or st.session_state.get("last_miesto_val") != miesto:
        st.session_state["last_miesto_val"] = miesto
        st.session_state[km_key] = auto_km_base

    st.markdown("---")

    # SEKCIA 2: SLUŽBY A BLOKY (PLNE FUNKČNÝ REAKTÍVNY PREPOČET)
    st.markdown("### 2. SLUŽBY A BLOKY (SI: 55 €/h, ostatné: 60 €/h)")
    
    total_sluzba_cena = 0.0
    total_hodiny = 0.0
    updated_blocks = []

    for idx, block in enumerate(st.session_state.service_blocks):
        st.markdown(f"**Služba / Blok #{idx + 1}**")
        col_b1, col_b2, col_b3, col_b4 = st.columns([3, 1.5, 1.5, 0.8])
        with col_b1:
            sel_serv = st.selectbox(f"Služba {idx+1}", all_available_services, index=all_available_services.index(block["sluzba"]) if block["sluzba"] in all_available_services else 0, key=f"serv_{idx}")
        with col_b2:
            sel_hod = st.number_input(f"Hodiny {idx+1}", min_value=0.5, max_value=50.0, value=float(block["hodiny"]), step=0.5, key=f"hod_{idx}")
        
        # Automatický výpočet ceny vždy pri zmene hodín alebo služby
        rate = HOURLY_RATES.get(sel_serv, 60.0)
        expected_price = round(sel_hod * rate, 2)
        
        state_key = f"cena_{idx}"
        prev_hod_key = f"prev_hod_{idx}"
        prev_serv_key = f"prev_serv_{idx}"

        if prev_hod_key not in st.session_state or st.session_state[prev_hod_key] != sel_hod or st.session_state.get(prev_serv_key) != sel_serv:
            st.session_state[prev_hod_key] = sel_hod
            st.session_state[prev_serv_key] = sel_serv
            st.session_state[state_key] = expected_price

        with col_b3:
            sel_cena = st.number_input(f"Cena (€) {idx+1}", min_value=0.0, max_value=10000.0, step=5.0, key=state_key)
        with col_b4:
            st.write("")
            st.write("")
            if len(st.session_state.service_blocks) > 1:
                if st.button("🗑️", key=f"del_{idx}"):
                    st.session_state.service_blocks.pop(idx)
                    st.rerun()

        total_sluzba_cena += sel_cena
        total_hodiny += sel_hod
        updated_blocks.append({"sluzba": sel_serv, "hodiny": sel_hod})
        st.markdown(f"*Výpočet položky #{idx+1}: {sel_serv} ({sel_hod} hod. × {rate} €/h) = **{sel_cena} €***")
        st.divider()

    st.session_state.service_blocks = updated_blocks

    if st.button("+ Pridať ďalšiu službu / blok"):
        st.session_state.service_blocks.append({"sluzba": "SI - individuálna supervízia", "hodiny": 4.0})
        st.rerun()

    st.markdown(f"**Súčet za všetky služby:** `{round(total_sluzba_cena, 2)} €` (Celkom {total_hodiny} hod.)")

    st.markdown("---")

    # SEKCIA 3: CESTOVNÝ KALKULÁTOR
    st.markdown("### 🚗 TABUĽKOVÝ KALKULÁTOR CESTOVNÉHO (Mitsubishi Outlander: 8,5 l nafta/100 km)")
    
    col_k1, col_k2, col_k3, col_k4 = st.columns(4)
    with col_k1:
        vzdialenost_km = st.number_input("Kilometre tam a späť (km)", min_value=0, max_value=2000, step=10, key=km_key)
    with col_k2:
        spotreba = st.number_input("Spotreba (l/100 km)", min_value=1.0, max_value=20.0, value=8.5, step=0.1)
    with col_k3:
        cena_paliva = st.number_input("Cena nafty (€/l)", min_value=0.5, max_value=3.0, value=1.55, step=0.01)
    with col_k4:
        amortizacia_rate = st.number_input("Zákonná amortizácia (€/km)", min_value=0.1, max_value=1.0, value=LEGAL_AMORTIZATION_PER_KM, step=0.001, format="%.3f")

    vypocet_amortizacia = vzdialenost_km * amortizacia_rate
    vypocet_palivo = (spotreba / 100.0) * vzdialenost_km * cena_paliva
    auto_cestovne_total = round(vypocet_amortizacia + vypocet_palivo, 2)

    cestovne_key = "cena_cestovne_val"
    if "last_auto_cestovne" not in st.session_state or st.session_state.get("last_auto_cestovne_calc") != auto_cestovne_total:
        st.session_state["last_auto_cestovne_calc"] = auto_cestovne_total
        st.session_state[cestovne_key] = auto_cestovne_total

    calc_box_html = (
        f"<div class='calc-box'>"
        f"<p style='margin:0;'><b>Rozpis cestovných náhrad:</b> Amortizácia ({vzdialenost_km} km × {amortizacia_rate} €) = "
        f"<b>{round(vypocet_amortizacia, 2)} €</b> | Palivo nafta ({vzdialenost_km} km × {spotreba} l / 100 × {cena_paliva} €) = "
        f"<b>{round(vypocet_palivo, 2)} €</b></p>"
        f"</div>"
    )
    st.markdown(calc_box_html, unsafe_allow_html=True)

    col_c1, col_c2 = st.columns(2)
    with col_c1:
        cestovny_cas = st.number_input("Cestovný čas (hod. z Dúbravky)", min_value=0.0, max_value=10.0, value=default_cesta, step=0.5)
    with col_c2:
        cena_cestovne = st.number_input("Výsledné cestovné (€) - automatický výpočet", min_value=0.0, max_value=2000.0, step=5.0, key=cestovne_key)

    st.markdown("---")

    # SEKCIA 4: UBYTOVANIE A STRAVA
    st.markdown("### 🏨 Ubytovanie a strava")
    col_u1, col_u2 = st.columns(2)
    with col_u1:
        ubytovanie = st.number_input("Ubytovanie (€)", min_value=0.0, max_value=1000.0, value=default_ubytovanie, step=10.0)
    with col_u2:
        strava = st.number_input("Strava (€)", min_value=0.0, max_value=500.0, value=default_strava, step=5.0)

    st.markdown("---")

    # SEKCIA 5: DÁTUM A ČASY LOGISTIKY
    st.markdown("### 📅 Dátum a časové krokovanie")
    col_d1, col_d2, col_d3 = st.columns(3)
    with col_d1:
        den = st.selectbox("Deň", list(range(1, 32)), index=default_datum.day - 1)
    with col_d2:
        mesiac = st.selectbox("Mesiac", list(range(1, 13)), index=default_datum.month - 1)
    with col_d3:
        rok = st.selectbox("Rok", [2026, 2027], index=0 if default_datum.year == 2026 else 1)

    try:
        datum_akcie = datetime(rok, mesiac, den).date()
    except Exception:
        datum_akcie = default_datum

    col_t1, col_t2 = st.columns(2)
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

    # FINÁLNY SPOLOČNÝ SÚČET NA FAKTÚRU
    celkova_suma = round(total_sluzba_cena + cena_cestovne + ubytovanie + strava, 2)
    sum_box_html = (
        f"<div style='background-color: #e3f2fd; padding: 18px; border-radius: 10px; border: 2px solid #2196f3; margin-bottom: 20px;'>"
        f"<h3 style='margin: 0; color: #0d47a1;'>Súčet služieb ({round(total_sluzba_cena, 2)} €) + Cestovné ({round(cena_cestovne, 2)} €) "
        f"+ Ubytovanie ({ubytovanie} €) + Strava ({strava} €) = Celková suma na FA: <b>{celkova_suma} €</b></h3>"
        f"</div>"
    )
    st.markdown(sum_box_html, unsafe_allow_html=True)

    poznamka = st.text_area("Poznámka", value=default_poznamka)

    combined_services_str = " + ".join([b["sluzba"] for b in st.session_state.service_blocks])

    btn_label = "💾 Dokončiť a automaticky vytvoriť termín v Google Kalendári" if item else "💾 Uložiť dopyt do zoznamu"
    if st.button(btn_label, type="primary"):
        if item:
            idx = st.session_state.dopyty[st.session_state.dopyty["ID"] == item['ID']].index
            st.session_state.dopyty.loc[idx, "Stav"] = "Kalendár"
            st.session_state.dopyty.loc[idx, "Sluzby"] = combined_services_str
            st.session_state.dopyty.loc[idx, "Hodiny"] = total_hodiny
            st.session_state.dopyty.loc[idx, "Miesto"] = miesto
            st.session_state.dopyty.loc[idx, "Krajina"] = krajina
            st.session_state.dopyty.loc[idx, "Datum_Akcie"] = str(datum_akcie)
            st.session_state.dopyty.loc[idx, "Cas"] = cas_akcie_str
            st.session_state.dopyty.loc[idx, "Cestovny_Cas"] = cestovny_cas
            st.session_state.dopyty.loc[idx, "Odchod"] = cas_odchodu_str
            st.session_state.dopyty.loc[idx, "Cena_Sluzby"] = total_sluzba_cena
            st.session_state.dopyty.loc[idx, "Cena_Cestovne"] = cena_cestovne
            st.session_state.dopyty.loc[idx, "Ubytovanie"] = ubytovanie
            st.session_state.dopyty.loc[idx, "Strava"] = strava
            st.session_state.dopyty.loc[idx, "Km"] = vzdialenost_km
            st.session_state.dopyty.loc[idx, "Poznamka"] = poznamka
            
            save_data(st.session_state.dopyty)
            st.session_state.edit_item = None
            st.success(f"Dopyt #{item['ID']} ({miesto}) bol úspešne spracovaný a prenesený do kalendára!")
            st.session_state.menu_tab = "Pipeline"
            st.rerun()
        else:
            novy_id = int(st.session_state.dopyty["ID"].max() + 1) if not st.session_state.dopyty.empty else 1
            novy_riadok = {
                "ID": novy_id,
                "Datum_Vytvorenia": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "Sluzby": combined_services_str,
                "Hodiny": total_hodiny,
                "Miesto": miesto,
                "Krajina": krajina,
                "Datum_Akcie": str(datum_akcie),
                "Cas": cas_akcie_str,
                "Cestovny_Cas": cestovny_cas,
                "Odchod": cas_odchodu_str,
                "Cena_Sluzby": total_sluzba_cena,
                "Cena_Cestovne": cena_cestovne,
                "Ubytovanie": ubytovanie,
                "Strava": strava,
                "Km": vzdialenost_km,
                "Stav": "Nová",
                "Poznamka": poznamka
            }
            st.session_state.dopyty = pd.concat([st.session_state.dopyty, pd.DataFrame([novy_riadok])], ignore_index=True)
            save_data(st.session_state.dopyty)
            st.success(f"Dopyt pre '{miesto}' bol uložený pod ID {novy_id}!")
            st.session_state.menu_tab = "Dopyty"
            st.rerun()

elif st.session_state.menu_tab == "Pipeline":
    st.header("📅 Kalendár a Prehľad potvrdených termínov")
    df = st.session_state.dopyty
    cal_df = df[df["Stav"] == "Kalendár"].sort_values(by="Datum_Akcie")
    
    if cal_df.empty:
        st.info("Zatiaľ žiadne termíny v kalendári. Spracujte a dokončite dopyty zo záložky Dopyty.")
    else:
        for idx, row in cal_df.iterrows():
            total_cena = round(float(row.get('Cena_Sluzby', 0.0)) + float(row.get('Cena_Cestovne', 0.0)) + float(row.get('Ubytovanie', 0.0)) + float(row.get('Strava', 0.0)), 2)
            cal_html = (
                f"<div class='card-calendar'>"
                f"<h4>📅 {row['Datum_Akcie']} o {row['Cas']} — {row['Sluzby']} ({row['Miesto']}, {row['Krajina']})</h4>"
                f"<p><b>Logistika z Dúbravky:</b> Odchod o <b>{row.get('Odchod', '08:00')}</b> | Cesta: {row.get('Cestovny_Cas', 1.0)} hod. | <b>Trvanie:</b> {row['Hodiny']} hod.</p>"
                f"<p><b>Fakturácia:</b> Služby ({row.get('Cena_Sluzby', 0.0)} €) + Cestovné ({row.get('Cena_Cestovne', 0.0)} €) "
                f"+ Ubytovanie ({row.get('Ubytovanie', 0.0)} €) + Strava ({row.get('Strava', 0.0)} €) = <b>Celkom {total_cena} €</b> (Vzdialenosť: {row.get('Km', 0)} km)</p>"
                f"<p><i>{row['Poznamka']}</i></p>"
                f"</div>"
            )
            st.markdown(cal_html, unsafe_allow_html=True)

elif st.session_state.menu_tab == "Klienti":
    st.header("👥 Klienti a partneri")
    st.info("Modul pre správu kontaktov a inštitúcií.")

elif st.session_state.menu_tab == "AI Engine":
    st.header("🤖 AI Engine")
    st.info("Modul pre pokročilú analýzu dopytov.")

elif st.session_state.menu_tab == "Export":
    st.header("📤 Export dát")
    st.write(f"Dátový súbor: `{DATA_FILE}`")
    if st.button("🔄 Obnoviť pôvodné testovacie dáta"):
        df_init = pd.DataFrame(INITIAL_DATA)
        save_data(df_init)
        st.session_state.dopyty = df_init
        st.success("Testovacie dáta boli obnovené!")
        st.rerun()
