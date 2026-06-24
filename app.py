from datetime import date
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

st.set_page_config(page_title="Data Center Power Radar", page_icon="⚡", layout="wide")

# ----------------------------
# Styling
# ----------------------------
st.markdown(
    """
    <style>
    :root {
        --bg: #f6f8fb;
        --card: #ffffff;
        --ink: #0f172a;
        --muted: #64748b;
        --border: #dbe3ef;
        --accent: #2563eb;
        --accent2: #0f766e;
    }

    .stApp {
        background: linear-gradient(180deg, #f7faff 0%, #f6f8fb 42%, #ffffff 100%);
    }

    .block-container {
        padding-top: 1.4rem;
        padding-bottom: 3.2rem;
        max-width: 1220px;
    }

    h1 {
        letter-spacing: -0.045em;
        font-size: 2.65rem !important;
        margin-bottom: 0.25rem !important;
        color: var(--ink);
    }

    h2, h3 {
        letter-spacing: -0.025em;
        color: var(--ink);
    }

    .subtitle {
        color: var(--muted);
        font-size: 1.02rem;
        margin-bottom: 1.25rem;
        max-width: 900px;
    }

    .source-line {
        color: #94a3b8;
        font-size: 0.83rem;
        margin-top: -0.2rem;
        margin-bottom: 1.1rem;
    }

    .hero {
        border: 1px solid var(--border);
        border-radius: 24px;
        padding: 26px 28px;
        background:
            radial-gradient(circle at top right, rgba(37, 99, 235, 0.13), transparent 28%),
            radial-gradient(circle at bottom left, rgba(15, 118, 110, 0.10), transparent 32%),
            #ffffff;
        box-shadow: 0 14px 40px rgba(15, 23, 42, 0.06);
        margin-bottom: 1.3rem;
    }

    .hero-title {
        font-size: 2.45rem;
        font-weight: 850;
        letter-spacing: -0.045em;
        color: var(--ink);
        margin: 0;
    }

    .hero-copy {
        color: var(--muted);
        font-size: 1.02rem;
        line-height: 1.55;
        margin-top: 0.45rem;
        max-width: 950px;
    }

    .metric-grid {
        display: grid;
        grid-template-columns: repeat(3, minmax(0, 1fr));
        gap: 14px;
        margin: 1rem 0 1.35rem 0;
    }

    .metric-card {
        background: #ffffff;
        border: 1px solid var(--border);
        border-radius: 18px;
        padding: 17px 18px;
        box-shadow: 0 8px 24px rgba(15, 23, 42, 0.045);
        min-height: 126px;
        overflow: hidden;
    }

    .metric-label {
        color: #64748b;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        font-size: 0.72rem;
        font-weight: 800;
        margin-bottom: 8px;
        white-space: nowrap;
    }

    .metric-value {
        color: var(--ink);
        font-size: clamp(1.52rem, 2.1vw, 2.2rem);
        font-weight: 900;
        letter-spacing: -0.045em;
        line-height: 1.05;
        white-space: normal;
        overflow-wrap: anywhere;
    }

    .metric-help {
        color: #64748b;
        font-size: 0.86rem;
        line-height: 1.35;
        margin-top: 8px;
    }

    .takeaway-grid {
        display: grid;
        grid-template-columns: repeat(3, minmax(0, 1fr));
        gap: 14px;
        margin: 0.9rem 0 1.4rem 0;
    }

    .takeaway {
        border: 1px solid var(--border);
        background: #ffffff;
        border-radius: 18px;
        padding: 17px 18px;
        box-shadow: 0 8px 24px rgba(15, 23, 42, 0.04);
        min-height: 120px;
    }

    .takeaway-kicker {
        color: var(--accent2);
        font-size: 0.75rem;
        font-weight: 850;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        margin-bottom: 8px;
    }

    .takeaway-title {
        color: var(--ink);
        font-weight: 850;
        font-size: 1.05rem;
        margin-bottom: 6px;
    }

    .takeaway-copy {
        color: #475569;
        font-size: 0.91rem;
        line-height: 1.45;
    }

    .logo-grid {
        display: grid;
        grid-template-columns: repeat(4, minmax(0, 1fr));
        gap: 14px;
        margin: 0.8rem 0 2rem 0;
    }

    .logo-card {
        background: #ffffff;
        border: 1px solid var(--border);
        border-radius: 18px;
        padding: 16px;
        box-shadow: 0 8px 24px rgba(15, 23, 42, 0.045);
        min-height: 188px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }

    .brand-row {
        display: flex;
        gap: 12px;
        align-items: center;
        margin-bottom: 12px;
    }

    .brand-mark {
        width: 58px;
        height: 58px;
        border-radius: 16px;
        display: flex;
        align-items: center;
        justify-content: center;
        color: #ffffff;
        font-weight: 900;
        letter-spacing: -0.04em;
        font-size: 1.05rem;
        flex: 0 0 58px;
        box-shadow: inset 0 -18px 30px rgba(0,0,0,0.12);
    }

    .brand-name {
        color: var(--ink);
        font-weight: 850;
        font-size: 1rem;
        line-height: 1.18;
    }

    .brand-category {
        color: #64748b;
        font-size: 0.78rem;
        margin-top: 4px;
        line-height: 1.25;
    }

    .brand-why {
        color: #475569;
        font-size: 0.89rem;
        line-height: 1.42;
        margin-top: 4px;
    }

    .group-header {
        margin-top: 1.2rem;
        margin-bottom: 0.25rem;
        padding-bottom: 0.35rem;
        border-bottom: 1px solid var(--border);
        color: var(--ink);
        font-weight: 850;
        font-size: 1.35rem;
        letter-spacing: -0.03em;
    }

    div[data-testid="stTabs"] button {
        font-size: 0.93rem;
    }

    div[data-testid="stDataFrame"] {
        border-radius: 18px;
        overflow: hidden;
    }

    @media (max-width: 900px) {
        .metric-grid,
        .takeaway-grid,
        .logo-grid {
            grid-template-columns: repeat(2, minmax(0, 1fr));
        }
    }

    @media (max-width: 620px) {
        .metric-grid,
        .takeaway-grid,
        .logo-grid {
            grid-template-columns: 1fr;
        }
        .hero-title {
            font-size: 1.9rem;
        }
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ----------------------------
# Data
# ----------------------------
CLEANVIEW_STATS = {
    "Total Data Centers": "2,293",
    "Operating Data Centers": "991",
    "Planned Data Centers": "1,261",
    "Operating Capacity": "44,775 MW",
    "Planned Capacity": "344,722 MW",
    "Unique Developers": "440",
}

projects = [
    {"Project": "IREN Childress", "Developer": "IREN", "Status": "Operating", "Capacity MW": 750, "Year": "2023", "Location": "Childress, TX", "Lat": 34.4265, "Lon": -100.2040, "Category": "Bitcoin / compute"},
    {"Project": "Riot Platforms Rockdale", "Developer": "Riot Platforms", "Status": "Operating", "Capacity MW": 700, "Year": "2020", "Location": "Milam County, TX", "Lat": 30.6544, "Lon": -97.0089, "Category": "Bitcoin / compute"},
    {"Project": "EdgeCore Mesa PH03", "Developer": "EdgeCore", "Status": "Operating", "Capacity MW": 450, "Year": "2025", "Location": "Maricopa County, AZ", "Lat": 33.4152, "Lon": -111.8315, "Category": "Data center"},
    {"Project": "Fairwater 1 - Mount Pleasant Phase 1", "Developer": "Microsoft", "Status": "Operating", "Capacity MW": 400, "Year": "2026", "Location": "Racine County, WI", "Lat": 42.7330, "Lon": -87.7829, "Category": "Hyperscale"},
    {"Project": "Project Zodiac Phase 1", "Developer": "Google", "Status": "Operating", "Capacity MW": 400, "Year": "2025", "Location": "Allen County, IN", "Lat": 41.0793, "Lon": -85.1394, "Category": "Hyperscale"},
    {"Project": "Core Scientific Denton 1", "Developer": "Core Scientific", "Status": "Operating", "Capacity MW": 391, "Year": "2022", "Location": "Denton, TX", "Lat": 33.2148, "Lon": -97.1331, "Category": "Bitcoin / compute"},
    {"Project": "Fairwater 2 - Atlanta", "Developer": "Microsoft", "Status": "Operating", "Capacity MW": 350, "Year": "2025", "Location": "Fulton County, GA", "Lat": 33.7490, "Lon": -84.3880, "Category": "Hyperscale"},
    {"Project": "Black Pearl", "Developer": "Cipher Mining", "Status": "Operating", "Capacity MW": 300, "Year": "2025", "Location": "Winkler County, TX", "Lat": 31.7796, "Lon": -103.2016, "Category": "Bitcoin / compute"},
    {"Project": "Council Bluffs Campus 2 West", "Developer": "Google", "Status": "Operating", "Capacity MW": 300, "Year": "2020", "Location": "Pottawattamie County, IA", "Lat": 41.2619, "Lon": -95.8608, "Category": "Hyperscale"},
    {"Project": "Delta Gigasite Expansion", "Developer": "Creekstone Energy", "Status": "Planned", "Capacity MW": 9700, "Year": "TBD", "Location": "Millard County, UT", "Lat": 39.0739, "Lon": -113.1000, "Category": "Mega campus"},
    {"Project": "PORTS Technology Campus Phase 2", "Developer": "SB Energy", "Status": "Planned", "Capacity MW": 9200, "Year": "TBD", "Location": "Pike County, OH", "Lat": 39.0717, "Lon": -83.0466, "Category": "Mega campus"},
    {"Project": "GW Ranch", "Developer": "Pacifico Energy", "Status": "Planned", "Capacity MW": 7650, "Year": "2027", "Location": "Pecos County, TX", "Lat": 30.8000, "Lon": -102.7000, "Category": "Mega campus"},
    {"Project": "Nexus Hubbard Expansion", "Developer": "Nexus Data Centers", "Status": "Planned", "Capacity MW": 7200, "Year": "TBD", "Location": "Hill County, TX", "Lat": 32.0100, "Lon": -97.1300, "Category": "Mega campus"},
    {"Project": "New Era Lea Data Center", "Developer": "New Era Energy", "Status": "Planned", "Capacity MW": 7000, "Year": "2028", "Location": "Lea County, NM", "Lat": 32.8000, "Lon": -103.4000, "Category": "Mega campus"},
    {"Project": "Monarch Compute Campus Phase 2", "Developer": "Nscale", "Status": "Planned", "Capacity MW": 6000, "Year": "TBD", "Location": "Mason County, WV", "Lat": 38.7500, "Lon": -82.0200, "Category": "AI / compute"},
    {"Project": "Wonder Valley Stratos Phase 2", "Developer": "O'Leary Digital", "Status": "Planned", "Capacity MW": 6000, "Year": "TBD", "Location": "Box Elder County, UT", "Lat": 41.5200, "Lon": -113.1000, "Category": "AI / compute"},
    {"Project": "Fermi Project Matador", "Developer": "Fermi America", "Status": "Planned", "Capacity MW": 6000, "Year": "2027", "Location": "Carson County, TX", "Lat": 35.4000, "Lon": -101.3550, "Category": "Power-led campus"},
    {"Project": "Meta Hyperion Expansion Phase 2", "Developer": "Meta", "Status": "Planned", "Capacity MW": 5238, "Year": "2031", "Location": "Richland Parish, LA", "Lat": 32.4200, "Lon": -91.7600, "Category": "Hyperscale / AI"},
]

markets = [
    {"Market":"Northern Virginia","Region":"Mid-Atlantic","ISO/RTO":"PJM","Type":"Core hyperscale","Power":2,"Cost":3,"Interconnection":2,"Demand":5,"Friction":2,"Cooling":3,"Real Estate":3,"Lat":39.0438,"Lon":-77.4874,"Thesis":"Benchmark market, but increasingly constrained by speed-to-power, utility timelines, land, and local approvals."},
    {"Market":"Dallas / Fort Worth","Region":"Texas","ISO/RTO":"ERCOT","Type":"Core growth","Power":4,"Cost":3,"Interconnection":4,"Demand":5,"Friction":4,"Cooling":3,"Real Estate":4,"Lat":32.7767,"Lon":-96.7970,"Thesis":"Strong growth market with land and demand, but ERCOT volatility and heat/cooling assumptions matter."},
    {"Market":"Phoenix","Region":"Southwest","ISO/RTO":"WECC","Type":"Core growth","Power":3,"Cost":3,"Interconnection":3,"Demand":4,"Friction":3,"Cooling":2,"Real Estate":4,"Lat":33.4484,"Lon":-112.0740,"Thesis":"Major western growth market where cooling, water, and utility-backed timelines are central."},
    {"Market":"Atlanta","Region":"Southeast","ISO/RTO":"Southeast","Type":"Core growth","Power":4,"Cost":4,"Interconnection":4,"Demand":4,"Friction":4,"Cooling":4,"Real Estate":4,"Lat":33.7490,"Lon":-84.3880,"Thesis":"Balanced growth market with southeast demand and a relatively clean execution story."},
    {"Market":"Chicago","Region":"Midwest","ISO/RTO":"PJM / MISO","Type":"Core enterprise","Power":3,"Cost":3,"Interconnection":3,"Demand":4,"Friction":3,"Cooling":4,"Real Estate":3,"Lat":41.8781,"Lon":-87.6298,"Thesis":"Durable enterprise and connectivity market where site selection and utility territory matter."},
    {"Market":"Columbus / New Albany","Region":"Midwest","ISO/RTO":"PJM","Type":"Emerging hyperscale hub","Power":4,"Cost":4,"Interconnection":4,"Demand":5,"Friction":4,"Cooling":4,"Real Estate":4,"Lat":40.0812,"Lon":-82.8088,"Thesis":"Strong example of hyperscale demand following credible land, power, and economic development alignment."},
    {"Market":"NYC / Northern New Jersey","Region":"Northeast","ISO/RTO":"NYISO / PJM","Type":"Edge / enterprise","Power":2,"Cost":2,"Interconnection":2,"Demand":4,"Friction":2,"Cooling":3,"Real Estate":2,"Lat":40.7128,"Lon":-74.0060,"Thesis":"High-value latency and enterprise market, but difficult for cheap hyperscale capacity."},
    {"Market":"Richmond","Region":"Mid-Atlantic","ISO/RTO":"PJM","Type":"Expansion market","Power":3,"Cost":3,"Interconnection":3,"Demand":4,"Friction":3,"Cooling":4,"Real Estate":4,"Lat":37.5407,"Lon":-77.4360,"Thesis":"Mid-Atlantic spillover market where utility and local approvals determine execution."},
    {"Market":"Fairfield County, CT","Region":"Northeast","ISO/RTO":"ISO-NE","Type":"Edge / financial services","Power":2,"Cost":2,"Interconnection":2,"Demand":3,"Friction":2,"Cooling":4,"Real Estate":3,"Lat":41.0534,"Lon":-73.5387,"Thesis":"Local edge thesis tied to NYC proximity and financial-services workloads, not a top hyperscale market."},
    {"Market":"Kansas City","Region":"Midwest","ISO/RTO":"SPP / MISO","Type":"Emerging growth","Power":4,"Cost":4,"Interconnection":4,"Demand":3,"Friction":4,"Cooling":4,"Real Estate":5,"Lat":39.0997,"Lon":-94.5786,"Thesis":"Power-led emerging-market screen that needs tenant and utility validation."},
    {"Market":"Salt Lake City","Region":"Mountain West","ISO/RTO":"WECC","Type":"Emerging growth","Power":3,"Cost":4,"Interconnection":3,"Demand":3,"Friction":4,"Cooling":3,"Real Estate":4,"Lat":40.7608,"Lon":-111.8910,"Thesis":"Secondary western market with possible operating advantages but tenant-depth questions."},
    {"Market":"Reno","Region":"Mountain West","ISO/RTO":"WECC","Type":"Western expansion","Power":3,"Cost":3,"Interconnection":3,"Demand":3,"Friction":4,"Cooling":3,"Real Estate":4,"Lat":39.5296,"Lon":-119.8138,"Thesis":"Western expansion screen where power delivery and demand depth should be tested carefully."},
]

players = [
    {"Company":"Equinix","Ticker":"EQIX","Color":"#0f172a","Group":"Operators","Category":"Interconnection / colocation","Why":"Network-dense global platform and benchmark for enterprise connectivity"},
    {"Company":"Digital Realty","Ticker":"DLR","Color":"#1d4ed8","Group":"Operators","Category":"Wholesale / colocation","Why":"Global scale owner/operator for wholesale and cloud demand"},
    {"Company":"QTS","Ticker":"QTS","Color":"#7c3aed","Group":"Operators","Category":"Hyperscale / colocation","Why":"Blackstone-backed platform tied to institutional digital infrastructure capital"},
    {"Company":"CyrusOne","Ticker":"C1","Color":"#0891b2","Group":"Operators","Category":"Hyperscale / colocation","Why":"Major developer/operator serving cloud and enterprise demand"},
    {"Company":"Vantage Data Centers","Ticker":"VDC","Color":"#0f766e","Group":"Operators","Category":"Hyperscale campus","Why":"Large-load campus developer and hyperscale partner"},
    {"Company":"STACK Infrastructure","Ticker":"STK","Color":"#334155","Group":"Operators","Category":"Hyperscale / colocation","Why":"Campus and colocation platform focused on scale customers"},
    {"Company":"NTT Global Data Centers","Ticker":"NTT","Color":"#b91c1c","Group":"Operators","Category":"Hyperscale / colocation","Why":"Large global operator with hyperscale and enterprise exposure"},
    {"Company":"CoreSite","Ticker":"CORE","Color":"#0369a1","Group":"Operators","Category":"Interconnection / colocation","Why":"American Tower-owned interconnection and colocation platform"},
    {"Company":"AWS","Ticker":"AWS","Color":"#f97316","Group":"Demand Drivers","Category":"Hyperscaler","Why":"One of the largest drivers of cloud and AI infrastructure demand"},
    {"Company":"Microsoft Azure","Ticker":"AZR","Color":"#2563eb","Group":"Demand Drivers","Category":"Cloud / AI","Why":"Major driver of leased and self-built AI and cloud capacity"},
    {"Company":"Google Cloud","Ticker":"GCP","Color":"#16a34a","Group":"Demand Drivers","Category":"Cloud / AI","Why":"Hyperscale cloud and AI demand driver with major owned and leased infrastructure"},
    {"Company":"Meta","Ticker":"META","Color":"#0284c7","Group":"Demand Drivers","Category":"AI / owner-operator","Why":"Large owner-operator and AI infrastructure spender"},
    {"Company":"Oracle Cloud","Ticker":"OCI","Color":"#dc2626","Group":"Demand Drivers","Category":"Cloud / AI","Why":"Cloud infrastructure platform tied to enterprise, database, and AI workloads"},
    {"Company":"CoreWeave","Ticker":"CW","Color":"#4f46e5","Group":"Demand Drivers","Category":"AI cloud","Why":"GPU-heavy AI cloud platform tied directly to accelerated compute demand"},
    {"Company":"NVIDIA","Ticker":"NVDA","Color":"#65a30d","Group":"Ecosystem","Category":"AI infrastructure","Why":"GPU and AI infrastructure supplier shaping the compute demand shock"},
    {"Company":"Constellation","Ticker":"CEG","Color":"#0d9488","Group":"Power Ecosystem","Category":"Power / nuclear","Why":"Power supplier with nuclear exposure, relevant to large-load clean power strategy"},
    {"Company":"NextEra Energy","Ticker":"NEE","Color":"#059669","Group":"Power Ecosystem","Category":"Power / renewables","Why":"Large power and renewables platform for clean-power procurement conversations"},
    {"Company":"GE Vernova","Ticker":"GEV","Color":"#155e75","Group":"Power Ecosystem","Category":"Power equipment","Why":"Grid and power equipment provider relevant to turbines, grid gear, and bottlenecks"},
]

source_table = pd.DataFrame([
    ["Cleanview US Data Center Tracker", "US project counts, operating/planned capacity, top operating projects, top planned projects", "https://cleanview.co/data-centers/us"],
    ["DOE / LBNL", "U.S. data center electricity use of 176 TWh in 2023 and 325-580 TWh estimated by 2028", "https://www.energy.gov/articles/doe-releases-new-report-evaluating-increase-electricity-demand-data-centers"],
    ["JLL North America Data Center Report YE 2025", "1% vacancy, 35+ GW under construction, 92% precommitted", "https://www.jll.com/en-us/insights/market-dynamics/north-america-data-centers"],
    ["CBRE Global Data Center Trends 2025", "Power availability as a key inhibitor and 6.6% global weighted average vacancy in Q1 2025", "https://www.cbre.com/insights/reports/global-data-center-trends-2025"],
], columns=["Source", "Used For", "URL"])

score_cols = ["Power","Cost","Interconnection","Demand","Friction","Cooling","Real Estate"]
weights_default = {"Power":25,"Cost":10,"Interconnection":20,"Demand":20,"Friction":10,"Cooling":5,"Real Estate":10}

# ----------------------------
# Helper functions
# ----------------------------
def classify(score):
    if score >= 80:
        return "Attractive"
    if score >= 68:
        return "Proceed with diligence"
    if score >= 55:
        return "Watchlist"
    return "Constrained"

def opportunity(row):
    if row["Demand"] >= 4 and row["Power"] >= 4:
        return "High demand + workable power"
    if row["Demand"] >= 4 and row["Power"] <= 2:
        return "High demand + power constrained"
    if row["Demand"] <= 3 and row["Power"] >= 4:
        return "Power-led emerging market"
    return "Selective / diligence heavy"

def radar_chart(row):
    vals = [row[c] for c in score_cols]
    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(r=vals + [vals[0]], theta=score_cols + [score_cols[0]], fill="toself"))
    fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0,5])), showlegend=False, height=390, margin=dict(l=20,r=20,t=20,b=20))
    return fig

def metric_card(label, value, help_text):
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">{label}</div>
            <div class="metric-value">{value}</div>
            <div class="metric-help">{help_text}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

def takeaway(kicker, title, copy):
    st.markdown(
        f"""
        <div class="takeaway">
            <div class="takeaway-kicker">{kicker}</div>
            <div class="takeaway-title">{title}</div>
            <div class="takeaway-copy">{copy}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

def logo_card(row):
    st.markdown(
        f"""
        <div class="logo-card">
            <div>
                <div class="brand-row">
                    <div class="brand-mark" style="background: linear-gradient(135deg, {row['Color']}, #020617);">{row['Ticker']}</div>
                    <div>
                        <div class="brand-name">{row['Company']}</div>
                        <div class="brand-category">{row['Category']}</div>
                    </div>
                </div>
                <div class="brand-why">{row['Why']}</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

# ----------------------------
# App
# ----------------------------
project_df = pd.DataFrame(projects)
market_df = pd.DataFrame(markets)
players_df = pd.DataFrame(players)

st.markdown(
    """
    <div class="hero">
        <div class="hero-title">Data Center Power Radar</div>
        <div class="hero-copy">
            A U.S. data center market tracker highlighting capacity growth, power constraints, key developers,
            and investment-relevant site selection risks.
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown('<div class="source-line">Public tracker snapshot and investment screen. Source snapshot: June 2026.</div>', unsafe_allow_html=True)

tracker, markets_tab, players_tab, diligence_tab, sources_tab = st.tabs(
    ["US Tracker", "Market Power Screen", "Developers & Ecosystem", "Site Diligence", "Sources"]
)

with tracker:
    st.subheader("US data center snapshot")

    st.markdown('<div class="metric-grid">', unsafe_allow_html=True)
    metric_card("Total data centers", CLEANVIEW_STATS["Total Data Centers"], "Operating and planned projects tracked across the U.S.")
    metric_card("Operating data centers", CLEANVIEW_STATS["Operating Data Centers"], "Live facilities in the public tracker snapshot.")
    metric_card("Planned data centers", CLEANVIEW_STATS["Planned Data Centers"], "Pipeline projects that still need power, permits, and capital execution.")
    metric_card("Operating capacity", CLEANVIEW_STATS["Operating Capacity"], "Current operating capacity tracked in megawatts.")
    metric_card("Planned capacity", CLEANVIEW_STATS["Planned Capacity"], "Planned capacity shows the scale of future grid demand.")
    metric_card("Unique developers", CLEANVIEW_STATS["Unique Developers"], "A fragmented but rapidly institutionalizing developer universe.")
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("#### What matters now")
    st.markdown('<div class="takeaway-grid">', unsafe_allow_html=True)
    takeaway("Supply pressure", "Vacancy is compressed", "The market is supply-constrained, with the most attractive capacity increasingly tied to credible power delivery.")
    takeaway("Power bottleneck", "MW is the real currency", "Land matters, but utility commitments, substation timing, and interconnection feasibility drive execution.")
    takeaway("Investment lens", "Not all planned MW is equal", "The best projects are not just the largest; they are the ones with power, permits, customers, and downside protection.")
    st.markdown('</div>', unsafe_allow_html=True)

    st.subheader("US project map")
    status_filter = st.multiselect("Status", ["Operating","Planned"], default=["Operating","Planned"])
    map_data = project_df[project_df["Status"].isin(status_filter)]
    fig = px.scatter_mapbox(
        map_data,
        lat="Lat",
        lon="Lon",
        size="Capacity MW",
        color="Status",
        hover_name="Project",
        hover_data=["Developer","Capacity MW","Year","Location","Category"],
        mapbox_style="carto-positron",
        zoom=3,
        height=610,
    )
    st.plotly_chart(fig, use_container_width=True, key="project_map")

    st.subheader("Largest projects")
    left, right = st.columns(2)
    with left:
        st.markdown("#### Largest operating")
        operating = project_df[project_df["Status"]=="Operating"].sort_values("Capacity MW", ascending=False)
        st.dataframe(
            operating[["Project","Developer","Capacity MW","Year","Location","Category"]],
            use_container_width=True,
            hide_index=True,
            column_config={"Capacity MW": st.column_config.NumberColumn("MW", format="%d")}
        )
    with right:
        st.markdown("#### Largest planned")
        planned = project_df[project_df["Status"]=="Planned"].sort_values("Capacity MW", ascending=False)
        st.dataframe(
            planned[["Project","Developer","Capacity MW","Year","Location","Category"]],
            use_container_width=True,
            hide_index=True,
            column_config={"Capacity MW": st.column_config.NumberColumn("MW", format="%d")}
        )

with markets_tab:
    st.subheader("Market power screen")

    with st.expander("Adjust investment screen weights"):
        cols = st.columns(4)
        weights = {}
        for i, col in enumerate(score_cols):
            with cols[i % 4]:
                weights[col] = st.slider(col, 0, 40, weights_default[col], 5)

    total_weight = sum(weights.values())
    market_df["Score"] = (sum(market_df[c] * weights[c] for c in score_cols) / total_weight * 20).round(1)
    market_df["Investor View"] = market_df["Score"].apply(classify)
    market_df["Opportunity Zone"] = market_df.apply(opportunity, axis=1)
    market_df = market_df.sort_values("Score", ascending=False)

    top = market_df.iloc[0]
    st.success(
        f"Current screen: {top['Market']} ranks highest at {top['Score']:.1f}. "
        "The strongest markets combine demand with credible power, interconnection, and real estate feasibility."
    )

    f1, f2, f3 = st.columns(3)
    with f1:
        regions = st.multiselect("Region", sorted(market_df["Region"].unique()), default=sorted(market_df["Region"].unique()))
    with f2:
        types = st.multiselect("Market type", sorted(market_df["Type"].unique()), default=sorted(market_df["Type"].unique()))
    with f3:
        views = st.multiselect("Investor view", sorted(market_df["Investor View"].unique()), default=sorted(market_df["Investor View"].unique()))

    filtered = market_df[
        market_df["Region"].isin(regions) &
        market_df["Type"].isin(types) &
        market_df["Investor View"].isin(views)
    ]

    st.dataframe(
        filtered[["Market","Region","ISO/RTO","Type","Score","Investor View","Opportunity Zone","Thesis"]],
        use_container_width=True,
        hide_index=True,
        column_config={"Score": st.column_config.ProgressColumn("Score", min_value=0, max_value=100, format="%.1f")}
    )

    c1, c2 = st.columns([1.05, 1])
    with c1:
        bar = px.bar(
            filtered.sort_values("Score"),
            x="Score",
            y="Market",
            color="Investor View",
            orientation="h",
            height=540,
        )
        st.plotly_chart(bar, use_container_width=True, key="market_ranked_bar")
    with c2:
        matrix = px.scatter(
            filtered,
            x="Power",
            y="Demand",
            size="Score",
            color="Opportunity Zone",
            hover_name="Market",
            hover_data=["Region","ISO/RTO","Type","Investor View"],
            height=540,
        )
        matrix.update_xaxes(range=[0.5,5.5], dtick=1)
        matrix.update_yaxes(range=[0.5,5.5], dtick=1)
        st.plotly_chart(matrix, use_container_width=True, key="power_demand_matrix")

    st.subheader("Risk heatmap")
    heat = filtered.set_index("Market")[score_cols]
    heat_fig = px.imshow(heat, text_auto=True, color_continuous_scale="RdYlGn", zmin=1, zmax=5, height=520)
    heat_fig.update_xaxes(tickangle=35)
    st.plotly_chart(heat_fig, use_container_width=True, key="risk_heatmap")

    st.subheader("Market memo")
    selected = st.selectbox("Select market", market_df["Market"].tolist())
    row = market_df[market_df["Market"] == selected].iloc[0]
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Score", f"{row['Score']:.1f}")
    m2.metric("View", row["Investor View"])
    m3.metric("Power", f"{row['Power']}/5")
    m4.metric("Demand", f"{row['Demand']}/5")
    memo_left, memo_right = st.columns([1.15, .85])
    with memo_left:
        with st.container(border=True):
            st.markdown("#### Thesis")
            st.write(row["Thesis"])
        with st.container(border=True):
            st.markdown("#### Interview angle")
            st.write(
                "Discuss the market through power delivery, interconnection queue, substation timing, cooling risk, "
                "fiber, tenant demand, and what happens if power is delayed by 12 to 24 months."
            )
    with memo_right:
        st.plotly_chart(radar_chart(row), use_container_width=True, key="selected_market_radar")

with players_tab:
    st.subheader("Developers, operators, demand drivers, and power ecosystem")
    st.write("Stable brand-style tiles grouped by role. No broken external image links.")

    groups = ["All"] + list(players_df["Group"].drop_duplicates())
    choice = st.selectbox("Filter group", groups)
    view = players_df if choice == "All" else players_df[players_df["Group"] == choice]

    for group in view["Group"].drop_duplicates():
        st.markdown(f'<div class="group-header">{group}</div>', unsafe_allow_html=True)
        st.markdown('<div class="logo-grid">', unsafe_allow_html=True)
        for _, item in view[view["Group"] == group].iterrows():
            logo_card(item)
        st.markdown('</div>', unsafe_allow_html=True)

with diligence_tab:
    st.subheader("Site diligence test")
    st.write("This is the investor overlay. The project tracker tells you what exists; this screen asks what can actually be delivered.")

    # Recalculate market score if user goes directly to this tab.
    temp_df = pd.DataFrame(markets)
    temp_df["Score"] = (sum(temp_df[c] * weights_default[c] for c in score_cols) / sum(weights_default.values()) * 20).round(1)

    selected_market = st.selectbox("Target market", temp_df["Market"].tolist(), key="site_market")
    site_market = temp_df[temp_df["Market"] == selected_market].iloc[0]

    c1, c2 = st.columns(2)
    with c1:
        mw = st.slider("Required IT load / power need", 5, 500, 100, 5)
        go_live = st.slider("Target go-live year", date.today().year, date.today().year + 10, date.today().year + 3)
    with c2:
        renewable = st.checkbox("Customer requires renewable / low-carbon power story", value=True)
        latency = st.checkbox("Latency-sensitive workload", value=False)
        behind_meter = st.checkbox("Behind-the-meter / dedicated generation option", value=False)

    site_score = int(site_market["Score"])
    flags = []

    if mw >= 250:
        site_score -= 28
        flags.append("Very large load. Treat power procurement and transmission as the primary feasibility question.")
    elif mw >= 100:
        site_score -= 18
        flags.append("Large load. Utility commitment, substation delivery, and queue position are gating items.")
    elif mw >= 50:
        site_score -= 10
        flags.append("Meaningful load. Confirm deliverable power, not just preliminary utility interest.")

    if go_live - date.today().year <= 3:
        site_score -= 8
        flags.append("Near-term go-live. Require direct utility diligence and evidence of delivery timeline.")

    if renewable:
        flags.append("Confirm PPA, green tariff, nuclear, renewables, or behind-the-meter strategy.")
    if latency:
        flags.append("Confirm that the workload actually needs this market rather than a cheaper power market.")
    if behind_meter:
        site_score += 8
        flags.append("Behind-the-meter strategy may reduce grid risk, but permitting and fuel/equipment timing matter.")

    site_score = max(0, min(100, site_score))
    result = classify(site_score)

    r1, r2, r3 = st.columns(3)
    r1.metric("Result", result)
    r2.metric("Site score", f"{site_score}/100")
    r3.metric("Base market score", f"{site_market['Score']:.1f}/100")

    st.markdown("#### Diligence flags")
    for flag in flags:
        st.write(f"• {flag}")

    st.markdown("#### Questions to ask")
    for question in [
        "Is the power allocation signed, funded, and deliverable, or only a utility conversation?",
        "What transmission, substation, or distribution upgrades are needed, and who pays?",
        "What is the downside plan if power is delayed 12 to 24 months?",
        "Is the cooling strategy realistic for the market and climate?",
        "Is the customer underwriting the market for latency, tax, fiber, power price, or renewable procurement?",
    ]:
        st.write(f"• {question}")

with sources_tab:
    st.subheader("Sources and notes")
    st.write(
        "The U.S. project counts and largest project tables are based on a public source snapshot. "
        "The market scores are judgment-based investment screening scores and should be updated with utility, ISO/RTO, land, tenant, and permitting diligence."
    )
    st.dataframe(
        source_table,
        use_container_width=True,
        hide_index=True,
        column_config={"URL": st.column_config.LinkColumn("URL")}
    )

    st.markdown("#### Scoring methodology")
    methodology = pd.DataFrame({
        "Category": score_cols,
        "Question": [
            "Can the market realistically support large-load delivery?",
            "Are power costs reasonably stable and financeable?",
            "Can projects connect to the grid within a usable timeline?",
            "Is there clear hyperscale, enterprise, cloud, AI, or edge demand?",
            "Are zoning, permitting, community, and utility processes manageable?",
            "Can the market support the cooling strategy without major water or heat risk?",
            "Are there viable sites with land, fiber, zoning, and access?",
        ],
        "Score Meaning": [
            "1 = highly constrained, 5 = relatively available",
            "1 = expensive / volatile, 5 = stable / attractive",
            "1 = difficult timeline, 5 = executable path",
            "1 = weak demand, 5 = very strong demand",
            "1 = high friction, 5 = manageable friction",
            "1 = material cooling risk, 5 = resilient",
            "1 = poor real estate fit, 5 = strong fit",
        ],
    })
    st.dataframe(methodology, use_container_width=True, hide_index=True)
