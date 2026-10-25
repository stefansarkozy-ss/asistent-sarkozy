import streamlit as st
import pandas as pd
from datetime import datetime

# --- SETTINGS & COMPACT MOBILE CSS ---
st.set_page_config(page_title="Asistent Štefana Šarközyho", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
    .stApp {
        background-color: #0f172a !important;
        color: #ffffff !important;
    }
    
    .block-container {
        max-width: 500px !important;
        padding: 0.6rem 0.8rem !important;
        margin: 0.8rem auto !important;
        background-color: #1e293b;
        border-radius: 14px;
        border: 2px solid #475569;
    }
    
    div[data-testid="stVerticalBlock"] {
        gap: 0.2rem !important;
    }
    
    div[data-testid="stVerticalBlock"] > div {
        background-color: #273549;
        border-radius: 8px;
        padding: 5px 8px !important;
        margin-bottom: 2px !important;
        border: 1px solid #475569;
    }
    
    h1, h2, h3, h4, label, span, p {
        color: #ffffff !important;
        font-weight: 800 !important;
        font-size: 0.85rem !important;
    }

    .stTextInput input, .stTextArea textarea, .stNumberInput input {
        color: #ffffff !important;
        font-weight: 900 !important;
        font-size: 0.9rem !important;
        background-color: #334155 !important;
        border: 2px solid #475569 !important;
        border-radius: 6px !important;
        height: 36px !important;
    }

    div[data-baseweb="select"] div {
        color: #ffffff !important;
        font-weight: 900 !important;
        font-size: 0.9rem !important;
        background-color: #0f172a !important;
    }
    
    div[data-baseweb="select"] {
        border: 2px solid #38bdf8 !important;
        border-radius: 6px !important;
        background-color: #0f172a !important;
    }

    button[data-baseweb="tab"] {
        color: #93c5fd !important;
        font-weight: 800 !important;
        font-size: 0.75rem !important;
        padding: 4px 4px !important;
    }
    button[aria-selected="true"] {
        color: #38bdf8 !important;
        border-bottom-color: #38bdf8 !important;
    }

    div.stButton > button {
        background-color: #273549 !important;
        color: #38bdf8 !important;
        font-weight: 900 !important;
        border-radius: 8px !important;
        width: 100% !important;
        border: 1px solid #475569 !important;
        padding: 6px !important;
        font-size: 0.85rem !important;
        text-align: center !important;
    }
    
    div.stButton > button:hover {
        background-color: #334155 !important;
        border-color: #38bdf8 !important;
    }

    div.stButton > button[kind="primary"] {
        background-color: #22c55e !important;
        color: #0f172a !important;
        border: none !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- CENNÍK A CONSTANTS ---
RATES = {
    "EUR": {"SI": 60, "SS": 65, "V": 55, "K": 50},
    "CZK": {"SI": 1400, "SS": 1600, "V": 1500, "K": 1500}
}

DEFAULT_DISTANCES_KM = {
    "Bratislava (mesto)": 20,
    "Záhorská Bystrica": 15,
    "Stupava": 20,
    "Trnava": 110,
    "Brno": 250,
    "Praha": 630,
    "Online": 0
}

SERVICE_NAMES = {"SI": "Indiv. supervízia", "SS": "Skup. supervízia", "V": "Vzdelávanie", "K": "Konzultácia"}
IF_LOCATIONS = ["Bratislava (mesto)", "Záhorská Bystrica", "Stupava", "Trnava", "Brno", "Praha", "Online"]

HOURS_OPTIONS = [0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 6.0, 7.0, 8.0, 10.0, 12.0, 25.0]
TIME_OPTIONS = [f"{h:02d}:{m:02d}" for h in range(7, 21) for m in (0, 30)]

MONTHS = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"]
YEARS = [2026, 2027, 2028]

# --- SESSION STATES ---
if "pipeline" not in st.session_state:
    st.session_state.pipeline = []
if "clients_history" not in st.session_state:
    st.session_state.clients_history = ["Vagus o.z.", "Detský domov", "Komunitné centrum", "Cífer", "CDR Piešťany", "KC Príbeta", "KC Šaľa", "Myjava", "DSS Javorinská", "Pezinok OSPOD", "CDR Pezinok", "KC Jelka", "Partizánske", "Veľký Meder", "Senec KC", "Trnava charita", "SVP"]

# 15 nepriradených dopytov z tabuľky pripravených na priradenie voľných termínov
if "pending_requests" not in st.session_state:
    st.session_state.pending_requests = [
        {"source": "Excel", "client": "Cífer", "service_type": "SS", "hours": 4.0, "location": "Trnava", "note": "Prezenčne, 4h (240 €)"},
        {"source": "Excel", "client": "CDR Piešťany", "service_type": "SS", "hours": 4.0, "location": "Trnava", "note": "Prezenčne, 4h (240 €)"},
        {"source": "Excel", "client": "KC Príbeta", "service_type": "SS", "hours": 4.0, "location": "Online", "note": "Online, dohoda (240 €)"},
        {"source": "Excel", "client": "KC Šaľa", "service_type": "SS", "hours": 3.0, "location": "Trnava", "note": "Prezenčne, 3h (180 €)"},
        {"source": "Excel", "client": "Myjava", "service_type": "SS", "hours": 4.0, "location": "Trnava", "note": "Prezenčne, 4h (240 €)"},
        {"source": "Excel", "client": "DSS Javorinská", "service_type": "SS", "hours": 5.0, "location": "Bratislava (mesto)", "note": "Prezenčne, 5h (300 €)"},
        {"source": "Excel", "client": "Pezinok OSPOD", "service_type": "SS", "hours": 25.0, "location": "Bratislava (mesto)", "note": "Prezenčne, 25h (1500 €)"},
        {"source": "Excel", "client": "CDR Pezinok", "service_type": "SS", "hours": 6.0, "location": "Bratislava (mesto)", "note": "Prezenčne, 6h (360 €)"},
        {"source": "Excel", "client": "KC Jelka", "service_type": "SS", "hours": 4.0, "location": "Trnava", "note": "Prezenčne, 4h"},
        {"source": "Excel", "client": "Partizánske", "service_type": "SS", "hours": 10.0, "location": "Trnava", "note": "Prezenčne, 10h (600 €)"},
        {"source": "Excel", "client": "Veľký Meder", "service_type": "SS", "hours": 5.0, "location": "Online", "note": "Online, FA (300 €)"},
        {"source": "Excel", "client": "Senec KC", "service_type": "SS", "hours": 3.5, "location": "Bratislava (mesto)", "note": "Prezenčne, 3.5h, FA (210 €)"},
        {"source": "Excel", "client": "Trnava charita", "service_type": "SS", "hours": 4.0, "location": "Trnava", "note": "Prezenčne"},
        {"source": "Excel", "client": "SVP", "service_type": "SS", "hours": 4.0, "location": "Bratislava (mesto)", "note": "Prezenčne"}
    ]

if "prefill_data" not in st.session_state:
    st.session_state.prefill_data = None

# VRCHNÁ LIŠTA
st.markdown("<div style='text-align: center; color: #94a3b8; font-weight: 700; font-size: 0.8rem; margin-bottom: 2px;'>💼 Asistent Štefana Šarközyho</div>", unsafe_allow_html=True)

# MODULÁRNE ZÁLOŽKY
tab0, tab1, tab2, tab3, tab4, tab5 = st.tabs(["📥 Dopyty", "Nová", "Pipeline", "Klienti", "AI Engine", "Export"])

# --- TAB 0: PRICHÁDZAJÚCE DOPYTY ---
with tab0:
    st.markdown(f"<span style='color:#38bdf8; font-weight:900;'>📥 NEPRIRADENÉ DOPYTY ({len(st.session_state.pending_requests)})</span>", unsafe_allow_html=True)
    
    if not st.session_state.pending_requests:
        st.info("Všetky dopyty sú spracované.")
    else:
        for idx, req in enumerate(st.session_state.pending_requests):
            with st.container():
                st.markdown(f"**{req.get('client')}** | 🛠️ {req.get('hours')}h")
                st.caption(f"📍 Miesto: {req.get('location')} | 💬 {req.get('note')}")
                
                if st.button(f"⚡ Priradiť termín", key=f"process_req_{idx}"):
                    st.session_state.prefill_data = req
                    st.session_state.pending_requests.pop(idx)
                    st.success("Prenesené do formulára!")
                    st.rerun()
                st.markdown("---")

# --- TAB 1: FORMULÁR (NOVÁ OBJEDNÁVKA) ---
with tab1:
    pf = st.session_state.prefill_data

    st.markdown("<span style='color:#38bdf8; font-weight:900;'>1. SLUŽBY A BLOKY</span>", unsafe_allow_html=True)
    
    if pf and "blocks" not in st.session_state:
        st.session_state.blocks = [{"type": pf.get("service_type", "SS"), "hours": float(pf.get("hours", 4.0))}]
    elif "blocks" not in st.session_state:
        st.session_state.blocks = [{"type": "SS", "hours": 4.0}]

    updated_blocks = []
    for idx, block in enumerate(st.session_state.blocks):
        c1, c2, c3 = st.columns([2.2, 1.2, 0.5])
        with c1:
            srv_type = st.selectbox("Služba", ["SI", "SS", "V", "K"], format_func=lambda x: f"{x} - {SERVICE_NAMES[x]}", key=f"s_{idx}")
        with c2:
            current_h = block["hours"]
            h_idx = HOURS_OPTIONS.index(current_h) if current_h in HOURS_OPTIONS else 1
            hours = st.selectbox("Hodiny", HOURS_OPTIONS, index=h_idx, key=f"h_{idx}")
        with c3:
            st.write("")
            if len(st.session_state.blocks) > 1:
                if st.button("🗑️", key=f"del_{idx}"):
                    st.session_state.blocks.pop(idx)
                    st.rerun()
        updated_blocks.append({"type": srv_type, "hours": hours})

    st.session_state.blocks = updated_blocks
    if st.button("+ Pridať blok"):
        st.session_state.blocks.append({"type": "SS", "hours": 4.0})
        st.rerun()

    st.markdown("<span style='color:#38bdf8; font-weight:900;'>2. VOĽNÝ TERMÍN (11./12. mesiac)</span>", unsafe_allow_html=True)
    
    cd1, cd2, cd3 = st.columns(3)
    with cd1:
        sel_day = st.selectbox("Deň", list(range(1, 32)), index=0, key="sel_d")
    with cd2:
        sel_month = st.selectbox("Mesiac", MONTHS, index=10, key="sel_m")
    with cd3:
        sel_year = st.selectbox("Rok", YEARS, index=0, key="sel_y")

    event_date_str = f"{sel_day:02d}.{sel_month}.{sel_year}"

    col1, col2 = st.columns(2)
    with col1:
        default_loc = pf.get("location", "Trnava") if pf else "Trnava"
        loc_idx = IF_LOCATIONS.index(default_loc) if default_loc in IF_LOCATIONS else 3
        location = st.selectbox("Miesto (z Dúbravky)", IF_LOCATIONS, index=loc_idx)
    with col2:
        event_time = st.selectbox("Čas", TIME_OPTIONS, index=4)

    col_f1, col_f2 = st.columns([1, 2])
    with col_f1:
        st.markdown("<div style='padding-top:4px;'><b>Forma:</b></div>", unsafe_allow_html=True)
    with col_f2:
        form = st.radio("Forma_radio", ["P", "O"], format_func=lambda x: "Prezenčne" if x == "P" else "Online", horizontal=True, label_visibility="collapsed")

    col_tr1, col_tr2 = st.columns([1.8, 1.2])
    with col_tr1:
        apply_travel = st.checkbox("Účtovať cestovné", value=True)
    with col_tr2:
        travel_country = st.radio("Krajina", ["SR", "ČR"], horizontal=True, label_visibility="collapsed", key="t_country")

    travel_fee = 0.0
    km_distance = 0

    if apply_travel:
        default_km = DEFAULT_DISTANCES_KM.get(location, 0)
        default_diesel = 1.60 if travel_country == "SR" else 38.00 
        estimated_hours = (default_km / 80.0) if default_km > 0 else 0
        default_time_pausal = round(estimated_hours * (15.0 if travel_country == "SR" else 350.0), 2)

        tc1, tc2, tc3 = st.columns(3)
        with tc1:
            km_distance = st.number_input("Km (z Dúbravky)", min_value=0, value=default_km, step=5, key="t_km")
        with tc2:
            fuel_price = st.number_input("Nafta/l", min_value=0.0, value=float(default_diesel), step=0.05, format="%.2f", key=f"t_fuel_{travel_country}")
        with tc3:
            time_fee = st.number_input("Paušál/Čas", min_value=0.0, value=float(default_time_pausal), step=5.0, key=f"t_time_{travel_country}")

        fuel_cost = (float(km_distance) / 100.0) * 8.0 * float(fuel_price)
        travel_fee = fuel_cost + float(time_fee)
        curr_sym = "EUR" if travel_country == "SR" else "CZK"
        st.caption(f"Cestovné: {travel_fee:,.2f} {curr_sym}")

    st.markdown("<span style='color:#38bdf8; font-weight:900;'>3. FAKTURÁCIA & POZNÁMKY</span>", unsafe_allow_html=True)
    
    default_client_val = pf.get("client", "") if pf else ""
    client = st.selectbox("Klient / Organizácia", st.session_state.clients_history, key="sel_client_box")
    custom_client = st.text_input("Alebo zadaj nového klienta:", value=default_client_val, placeholder="Názov klienta...")
    final_client = custom_client.strip() if custom_client.strip() else client

    col_m1, col_m2 = st.columns([1, 2])
    with col_m1:
        st.markdown("<div style='padding-top:4px;'><b>Mena:</b></div>", unsafe_allow_html=True)
    with col_m2:
        currency = st.radio("Mena_radio", ["EUR", "CZK"], horizontal=True, label_visibility="collapsed", key="sel_currency")

    default_note_val = pf.get("note", "") if pf else ""
    notes = st.text_area("Poznámka", value=default_note_val, placeholder="Poznámky k zákazke...")

    services_total = sum(float(b["hours"]) * RATES[currency][b["type"]] for b in st.session_state.blocks)
    total_price = services_total + travel_fee

    st.markdown(f"<h4 style='text-align:center; color:#22c55e; margin: 4px 0; font-size: 1.2rem; font-weight: 900;'>Celkom: {total_price:,.2f} {currency}</h4>", unsafe_allow_html=True)

    services_desc_text = ", ".join([f"{b['hours']}h {SERVICE_NAMES[b['type']]}" for b in st.session_state.blocks])
    
    if st.button("💾 ULOŽIŤ OBJEDNÁVKU", type="primary"):
        if final_client not in st.session_state.clients_history:
            st.session_state.clients_history.append(final_client)
        
        new_order = {
            "id": len(st.session_state.pipeline) + 1,
            "client": final_client,
            "date": event_date_str,
            "time": event_time,
            "location": location,
            "price": total_price,
            "currency": currency,
            "stage": "2. Naplánované",
            "notes": notes,
            "services": services_desc_text,
            "travel_fee": travel_fee,
            "km": km_distance,
            "blocks": st.session_state.blocks.copy()
        }
        st.session_state.pipeline.append(new_order)
        st.session_state.prefill_data = None
        st.success(f"Objednávka pre {final_client} úspešne uložená!")

# --- TAB 2: PIPELINE ---
with tab2:
    st.markdown("<span style='color:#38bdf8; font-weight:900;'>PREHĽAD PIPELINE</span>", unsafe_allow_html=True)
    if not st.session_state.pipeline:
        st.info("Zatiaľ žiadne záznamy.")
    else:
        for idx, item in enumerate(st.session_state.pipeline):
            with st.container():
                st.markdown(f"**#{item['id']} | {item['client']}** — {item['price']:,.2f} {item['currency']}")
                st.caption(f"📅 {item['date']} | ⏰ {item['time']} | 📍 {item['location']}")
                
                new_stage = st.selectbox(
                    "Stav", 
                    ["1. Dopyt", "2. Naplánované", "3. Vyfakturované", "4. Zaplatené", "5. Zrušené"],
                    index=["1. Dopyt", "2. Naplánované", "3. Vyfakturované", "4. Zaplatené", "5. Zrušené"].index(item['stage']),
                    key=f"stage_{idx}"
                )
                st.session_state.pipeline[idx]['stage'] = new_stage
                st.markdown("---")

# --- TAB 3: KLIENTI ---
with tab3:
    st.markdown("<span style='color:#38bdf8; font-weight:900;'>👥 SPRÁVA KLIENTOV</span>", unsafe_allow_html=True)
    st.info("Modul pripravený na evidenciu histórie stretnutí.")
    for client_name in st.session_state.clients_history:
        st.markdown(f"• **{client_name}**")

# --- TAB 4: AI ENGINE ---
with tab4:
    st.markdown("<span style='color:#38bdf8; font-weight:900;'>🧠 AI ENGINE & OPTIMALIZÁCIA</span>", unsafe_allow_html=True)
    st.success("Modul pripravený na postupné učenie sa trasy, vyhodnocovanie kapacity a autonómne navrhovanie termínov.")

# --- TAB 5: EXPORT ---
with tab5:
    st.markdown("<span style='color:#38bdf8; font-weight:900;'>EXPORT DÁT</span>", unsafe_allow_html=True)
    if not st.session_state.pipeline:
        st.info("Žiadne dáta na export.")
    else:
        df_export = pd.DataFrame([{
            "ID": i["id"], "Klient": i["client"], "Dátum": i["date"], "Čas": i["time"],
            "Miesto": i["location"], "Služby": i["services"], "Cena": i["price"],
            "Mena": i["currency"], "Cestovné": i.get("travel_fee", 0), "Stav": i["stage"]
        } for i in st.session_state.pipeline])
        st.dataframe(df_export, use_container_width=True)
        csv_bytes = df_export.to_csv(index=False).encode('utf-8-sig')
        st.download_button("📊 STIAHNUŤ CSV", csv_bytes, file_name="objednavky.csv", mime="text/csv", type="primary")
