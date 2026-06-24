from datetime import date
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

st.set_page_config(
    page_title="DC Power Radar",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed",
)

SCORE_COLUMNS = [
    "power_availability",
    "power_cost_stability",
    "interconnection_feasibility",
    "demand_signal",
    "development_friction",
    "water_cooling_resilience",
    "real_estate_feasibility",
]

DISPLAY_NAMES = {
    "power_availability": "Power Availability",
    "power_cost_stability": "Power Cost Stability",
    "interconnection_feasibility": "Interconnection Feasibility",
    "demand_signal": "Demand Signal",
    "development_friction": "Development Friction",
    "water_cooling_resilience": "Water / Cooling",
    "real_estate_feasibility": "Real Estate",
}

DEFAULT_WEIGHTS = {
    "power_availability": 25,
    "power_cost_stability": 10,
    "interconnection_feasibility": 20,
    "demand_signal": 20,
    "development_friction": 10,
    "water_cooling_resilience": 5,
    "real_estate_feasibility": 10,
}

MARKETS = [
    {"market":"Northern Virginia","region":"Mid-Atlantic","iso_rto":"PJM","lat":39.0438,"lon":-77.4874,"market_type":"Core hyperscale","power_availability":2,"power_cost_stability":3,"interconnection_feasibility":2,"demand_signal":5,"development_friction":2,"water_cooling_resilience":3,"real_estate_feasibility":3,"status_note":"Largest core ecosystem, but power delivery is the underwriting question.","fact_type":"Sourced trend + underwriting judgment","memo_thesis":"Still the benchmark U.S. data center market, but increasingly a power-constrained market where speed-to-power matters as much as location.","power_situation":"Treat power availability, substation delivery, and transmission constraints as the first diligence workstream.","demand_drivers":"Cloud, AI, enterprise, dense fiber, and the deepest existing data center ecosystem.","development_constraints":"Power delivery, land competition, zoning scrutiny, community pushback, and utility timelines.","investor_takeaway":"Core market with strong demand but limited easy wins. Best opportunities need credible power or strategic adjacency."},
    {"market":"Dallas / Fort Worth","region":"Texas","iso_rto":"ERCOT","lat":32.7767,"lon":-96.7970,"market_type":"Core growth","power_availability":4,"power_cost_stability":3,"interconnection_feasibility":4,"demand_signal":5,"development_friction":4,"water_cooling_resilience":3,"real_estate_feasibility":4,"status_note":"Strong growth market with land, demand, and energy-market depth.","fact_type":"Underwriting judgment","memo_thesis":"One of the most attractive large-scale growth markets if ERCOT volatility and heat/cooling assumptions are underwritten correctly.","power_situation":"Power access can be more workable than constrained coastal markets, but volatility and grid reliability still matter.","demand_drivers":"Cloud growth, enterprise demand, AI, central U.S. connectivity, and large-campus land options.","development_constraints":"Power price volatility, heat, water/cooling load, and competition for large-load commitments.","investor_takeaway":"High-growth, institutionally relevant market, but power procurement needs a clear downside case."},
    {"market":"Phoenix","region":"Southwest","iso_rto":"Non-ISO / WECC","lat":33.4484,"lon":-112.0740,"market_type":"Core growth","power_availability":3,"power_cost_stability":3,"interconnection_feasibility":3,"demand_signal":4,"development_friction":3,"water_cooling_resilience":2,"real_estate_feasibility":4,"status_note":"Major western growth market where cooling and water diligence are central.","fact_type":"Underwriting judgment","memo_thesis":"A key western growth market, but the investment case depends heavily on cooling strategy and utility-backed power timelines.","power_situation":"Feasible in select pockets, but large-load commitments require direct utility diligence.","demand_drivers":"Western U.S. cloud demand, latency diversification, AI, and campus-scale development potential.","development_constraints":"Heat, water, cooling efficiency, public scrutiny, and long-term sustainability.","investor_takeaway":"Compelling where cooling and utility timelines are credible; risky if the thesis depends only on land availability."},
    {"market":"Atlanta","region":"Southeast","iso_rto":"Non-ISO / Southeast","lat":33.7490,"lon":-84.3880,"market_type":"Core growth","power_availability":4,"power_cost_stability":4,"interconnection_feasibility":4,"demand_signal":4,"development_friction":4,"water_cooling_resilience":4,"real_estate_feasibility":4,"status_note":"Balanced growth market with strong southeast demand and relatively clean execution story.","fact_type":"Underwriting judgment","memo_thesis":"A cleaner risk-adjusted growth story than many constrained northern markets, subject to utility delivery confirmation.","power_situation":"Generally more executable than the most constrained hubs, but project-level power still drives feasibility.","demand_drivers":"Cloud growth, enterprise demand, southeast population growth, fiber, and regional connectivity.","development_constraints":"Competition for powered sites and local infrastructure capacity.","investor_takeaway":"Attractive if power delivery dates are real and not just preliminary utility conversations."},
    {"market":"Chicago","region":"Midwest","iso_rto":"PJM / MISO","lat":41.8781,"lon":-87.6298,"market_type":"Core enterprise","power_availability":3,"power_cost_stability":3,"interconnection_feasibility":3,"demand_signal":4,"development_friction":3,"water_cooling_resilience":4,"real_estate_feasibility":3,"status_note":"Durable enterprise and connectivity market with colder climate benefits.","fact_type":"Underwriting judgment","memo_thesis":"A durable institutional market where demand is real, but site selection and utility territory matter more than broad market labels.","power_situation":"Power depends heavily on utility territory, substation capacity, and timeline.","demand_drivers":"Enterprise workloads, financial services, cloud availability zone demand, and Midwest connectivity.","development_constraints":"Preferred-site scarcity, taxes, utility delivery timing, and redevelopment economics.","investor_takeaway":"Good market for disciplined projects with utility clarity and proven customer demand."},
    {"market":"Columbus / New Albany","region":"Midwest","iso_rto":"PJM","lat":40.0812,"lon":-82.8088,"market_type":"Emerging hyperscale hub","power_availability":4,"power_cost_stability":4,"interconnection_feasibility":4,"demand_signal":5,"development_friction":4,"water_cooling_resilience":4,"real_estate_feasibility":4,"status_note":"Emerging hub that fits the frontier-market shift highlighted by JLL.","fact_type":"Sourced trend + underwriting judgment","memo_thesis":"A strong example of hyperscale demand following credible land, power, and economic development alignment.","power_situation":"Attractive relative to constrained coastal markets, though large-load growth can tighten capacity quickly.","demand_drivers":"Hyperscale campus activity, Midwest connectivity, and economic development support.","development_constraints":"Rapid pipeline growth, utility sequencing, and community infrastructure planning.","investor_takeaway":"Useful interview market because it shows how power and land can create a new digital infrastructure hub."},
    {"market":"NYC / Northern New Jersey","region":"Northeast","iso_rto":"NYISO / PJM","lat":40.7128,"lon":-74.0060,"market_type":"Edge / enterprise","power_availability":2,"power_cost_stability":2,"interconnection_feasibility":2,"demand_signal":4,"development_friction":2,"water_cooling_resilience":3,"real_estate_feasibility":2,"status_note":"High-value latency and enterprise market, not the cheapest hyperscale capacity market.","fact_type":"Underwriting judgment","memo_thesis":"Better viewed as an edge, interconnection, and enterprise infrastructure market than a cheap capacity market.","power_situation":"Expensive and constrained relative to lower-cost growth markets.","demand_drivers":"Financial services, media, cloud on-ramps, enterprise latency, and dense connectivity.","development_constraints":"Power costs, permitting, land scarcity, taxes, and redevelopment complexity.","investor_takeaway":"Attractive for edge and interconnection use cases; difficult for large cheap-power hyperscale."},
    {"market":"Richmond","region":"Mid-Atlantic","iso_rto":"PJM","lat":37.5407,"lon":-77.4360,"market_type":"Expansion market","power_availability":3,"power_cost_stability":3,"interconnection_feasibility":3,"demand_signal":4,"development_friction":3,"water_cooling_resilience":4,"real_estate_feasibility":4,"status_note":"CBRE identified Richmond as a hotspot benefiting from constraints in core hub markets.","fact_type":"Sourced trend + underwriting judgment","memo_thesis":"A spillover and expansion market for Mid-Atlantic demand, but utility and local approvals determine execution.","power_situation":"Potentially attractive, but exposed to the same large-load pressures affecting nearby markets.","demand_drivers":"Northern Virginia spillover, fiber routes, land availability, and hyperscale regional demand.","development_constraints":"Utility capacity, community scrutiny, and competition for powered land.","investor_takeaway":"Good example of power and land constraints pushing demand beyond the obvious core hub."},
    {"market":"Fairfield County, CT","region":"Northeast","iso_rto":"ISO-NE","lat":41.0534,"lon":-73.5387,"market_type":"Edge / financial services","power_availability":2,"power_cost_stability":2,"interconnection_feasibility":2,"demand_signal":3,"development_friction":2,"water_cooling_resilience":4,"real_estate_feasibility":3,"status_note":"Local edge thesis. Use as an interview angle, not a sourced top hyperscale market.","fact_type":"Thesis placeholder","memo_thesis":"A niche edge and financial-services-adjacent market, not a broad hyperscale market.","power_situation":"High-cost ISO-NE environment makes power strategy and load profile critical.","demand_drivers":"Proximity to NYC, financial services, enterprise latency, and disaster recovery use cases.","development_constraints":"Power costs, limited large-campus land, local permitting, and expensive redevelopment.","investor_takeaway":"Interesting local angle because it ties CT to edge infrastructure and financial-services workloads."},
    {"market":"Kansas City","region":"Midwest","iso_rto":"SPP / MISO","lat":39.0997,"lon":-94.5786,"market_type":"Emerging growth","power_availability":4,"power_cost_stability":4,"interconnection_feasibility":4,"demand_signal":3,"development_friction":4,"water_cooling_resilience":4,"real_estate_feasibility":5,"status_note":"Power-led emerging market thesis. Needs utility and tenant-specific validation.","fact_type":"Thesis placeholder","memo_thesis":"A practical emerging-market screen where land, central connectivity, and relative power feasibility may create a development case.","power_situation":"Potentially attractive if utility alignment and transmission capacity are verified.","demand_drivers":"Central U.S. connectivity, enterprise demand, and diversification away from constrained coastal hubs.","development_constraints":"Need to prove depth of demand versus better-known markets.","investor_takeaway":"Useful for showing how to evaluate emerging markets beyond obvious demand signals."},
    {"market":"Salt Lake City","region":"Mountain West","iso_rto":"Non-ISO / WECC","lat":40.7608,"lon":-111.8910,"market_type":"Emerging growth","power_availability":3,"power_cost_stability":4,"interconnection_feasibility":3,"demand_signal":3,"development_friction":4,"water_cooling_resilience":3,"real_estate_feasibility":4,"status_note":"Secondary western market thesis. Needs land, water, and utility validation.","fact_type":"Thesis placeholder","memo_thesis":"A credible secondary-market screen with western connectivity and possible operating-cost advantages.","power_situation":"Power can be favorable, but site-level utility commitments drive feasibility.","demand_drivers":"Western regional workloads, cloud expansion, and disaster recovery diversification.","development_constraints":"Water, large powered sites, and relative depth of local demand.","investor_takeaway":"Good secondary case study if the investment memo avoids overstating demand depth."},
    {"market":"Reno","region":"Mountain West","iso_rto":"Non-ISO / WECC","lat":39.5296,"lon":-119.8138,"market_type":"Western expansion","power_availability":3,"power_cost_stability":3,"interconnection_feasibility":3,"demand_signal":3,"development_friction":4,"water_cooling_resilience":3,"real_estate_feasibility":4,"status_note":"Western expansion thesis. Needs tenant-depth and power-delivery validation.","fact_type":"Thesis placeholder","memo_thesis":"A western expansion screen with campus potential, but demand depth and power delivery should be tested carefully.","power_situation":"Feasibility depends on utility commitments and renewable procurement options.","demand_drivers":"West Coast proximity, tax considerations, and cloud / enterprise diversification.","development_constraints":"Power delivery timing, water, and relative tenant depth.","investor_takeaway":"Interesting for a differentiated thesis, but not a default core market without tenant visibility."},
]

PLAYERS = [
    {"company":"Equinix","short":"EQIX","group":"Operators","category":"Colocation / Interconnection","why":"Global interconnection and colocation platform. Important for network-dense, enterprise-oriented demand."},
    {"company":"Digital Realty","short":"DLR","group":"Operators","category":"Colocation / Wholesale","why":"One of the largest global data center owners and operators. Important for wholesale, cloud, and interconnection strategy."},
    {"company":"NTT Global Data Centers","short":"NTT","group":"Operators","category":"Colocation / Hyperscale","why":"Large global data center operator with hyperscale and enterprise exposure."},
    {"company":"Vantage Data Centers","short":"VNTG","group":"Operators","category":"Hyperscale Campus","why":"Hyperscale campus developer and operator. Useful for understanding large-load development."},
    {"company":"QTS","short":"QTS","group":"Operators","category":"Hyperscale / Colocation","why":"Blackstone-backed platform. Good example of institutional capital moving into digital infrastructure."},
    {"company":"STACK Infrastructure","short":"STK","group":"Operators","category":"Hyperscale / Colocation","why":"Platform focused on large-scale campus and colocation demand."},
    {"company":"CyrusOne","short":"C1","group":"Operators","category":"Hyperscale / Colocation","why":"Major data center developer and operator serving cloud and enterprise demand."},
    {"company":"CoreSite","short":"CORE","group":"Operators","category":"Interconnection / Colocation","why":"Interconnection and colocation platform owned by American Tower."},
    {"company":"AWS","short":"AWS","group":"Demand Drivers","category":"Hyperscaler","why":"Cloud hyperscaler and one of the largest drivers of data center demand."},
    {"company":"Microsoft Azure","short":"AZR","group":"Demand Drivers","category":"Hyperscaler / AI","why":"Cloud and AI hyperscaler. Major driver of leased and self-built capacity."},
    {"company":"Google Cloud","short":"GCP","group":"Demand Drivers","category":"Hyperscaler / AI","why":"Cloud and AI platform with major data center investment needs."},
    {"company":"Meta","short":"META","group":"Demand Drivers","category":"Hyperscaler / AI","why":"Large owner-operator and major AI infrastructure spender."},
    {"company":"Oracle Cloud","short":"OCI","group":"Demand Drivers","category":"Hyperscaler / AI","why":"Cloud infrastructure provider tied to database, enterprise, and AI workloads."},
    {"company":"CoreWeave","short":"CW","group":"Demand Drivers","category":"AI Cloud","why":"AI cloud platform tied directly to GPU-heavy capacity demand."},
    {"company":"NVIDIA","short":"NVDA","group":"Ecosystem","category":"AI Infrastructure","why":"GPU and AI infrastructure supplier. Important for understanding the AI capacity demand shock."},
    {"company":"Constellation","short":"CEG","group":"Power Ecosystem","category":"Power / Nuclear","why":"Power supplier with nuclear exposure. Relevant because data center growth is increasingly power-led."},
    {"company":"NextEra Energy","short":"NEE","group":"Power Ecosystem","category":"Power / Renewables","why":"Large power and renewables platform. Important for clean-power procurement conversations."},
    {"company":"GE Vernova","short":"GEV","group":"Power Ecosystem","category":"Power Equipment","why":"Grid and power equipment provider. Relevant for turbines, grid equipment, and power bottlenecks."},
]

SOURCES = [
    {"metric":"U.S. data center electricity use","value":"176 TWh","fact":"DOE / LBNL reported U.S. data centers used 176 TWh in 2023, about 4.4% of total U.S. electricity.","source":"DOE / Lawrence Berkeley National Lab","url":"https://www.energy.gov/articles/doe-releases-new-report-evaluating-increase-electricity-demand-data-centers"},
    {"metric":"2028 U.S. electricity use estimate","value":"325-580 TWh","fact":"DOE / LBNL estimated U.S. data center electricity use could reach 325 to 580 TWh by 2028.","source":"DOE / Lawrence Berkeley National Lab","url":"https://www.energy.gov/articles/doe-releases-new-report-evaluating-increase-electricity-demand-data-centers"},
    {"metric":"North America vacancy","value":"1%","fact":"JLL reported North American data center vacancy remained at 1% for a second consecutive year at year-end 2025.","source":"JLL North America Data Center Report Year-end 2025","url":"https://www.jll.com/en-us/insights/market-dynamics/north-america-data-centers"},
    {"metric":"North America construction pipeline","value":"35+ GW","fact":"JLL reported more than 35 GW of data center capacity under construction in North America at year-end 2025.","source":"JLL North America Data Center Report Year-end 2025","url":"https://www.jll.com/en-us/insights/market-dynamics/north-america-data-centers"},
    {"metric":"Pipeline precommitment","value":"92%","fact":"JLL reported 92% of North American capacity under construction was precommitted at year-end 2025.","source":"JLL North America Data Center Report Year-end 2025","url":"https://www.jll.com/en-us/insights/market-dynamics/north-america-data-centers"},
    {"metric":"Grid connection wait","value":"4+ years","fact":"JLL reported the average wait time for grid connection in primary data center markets exceeds four years.","source":"JLL 2026 Global Data Center Market Outlook","url":"https://www.jll.com/en-us/insights/market-outlook/data-center-outlook"},
    {"metric":"Global market vacancy","value":"6.6%","fact":"CBRE reported the global weighted average data center vacancy rate fell to 6.6% in Q1 2025.","source":"CBRE Global Data Center Trends 2025","url":"https://www.cbre.com/insights/reports/global-data-center-trends-2025"},
    {"metric":"Power availability constraint","value":"Key bottleneck","fact":"CBRE reported limited power availability remained the prime inhibitor of global data center growth in certain core hub markets.","source":"CBRE Global Data Center Trends 2025","url":"https://www.cbre.com/insights/reports/global-data-center-trends-2025"},
]

def weighted_score(frame, weights):
    total = sum(weights.values())
    if total == 0:
        return pd.Series([0] * len(frame), index=frame.index)
    return (sum(frame[col] * weight for col, weight in weights.items()) / total * 20).round(1)

def classify(score):
    if score >= 80:
        return "Attractive"
    if score >= 68:
        return "Proceed with diligence"
    if score >= 55:
        return "Watchlist"
    return "Constrained"

def zone(row):
    if row["demand_signal"] >= 4 and row["power_availability"] >= 4:
        return "High demand + workable power"
    if row["demand_signal"] >= 4 and row["power_availability"] <= 2:
        return "High demand + power constrained"
    if row["demand_signal"] <= 3 and row["power_availability"] >= 4:
        return "Power-led emerging market"
    return "Selective / diligence heavy"

def radar(row):
    labels = [DISPLAY_NAMES[c] for c in SCORE_COLUMNS]
    values = [row[c] for c in SCORE_COLUMNS]
    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(r=values + [values[0]], theta=labels + [labels[0]], fill="toself", line=dict(width=3)))
    fig.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 5])),
        height=430,
        margin=dict(l=30, r=30, t=30, b=30),
        showlegend=False,
    )
    return fig

def screen_site(row, mw, go_live, renewable, latency, behind_meter):
    score = int(round((
        row["power_availability"] * 18 +
        row["interconnection_feasibility"] * 18 +
        row["power_cost_stability"] * 12 +
        row["demand_signal"] * 14 +
        row["development_friction"] * 10 +
        row["water_cooling_resilience"] * 8 +
        row["real_estate_feasibility"] * 10
    ) / 5))

    flags = []
    if mw >= 100:
        score -= 18
        flags.append("Large load request. Utility commitment and substation timeline are gating items.")
    elif mw >= 50:
        score -= 10
        flags.append("Meaningful load request. Test whether power is real, deliverable, and within the target date.")

    years = go_live - date.today().year
    if years <= 2 and row["interconnection_feasibility"] <= 3:
        score -= 12
        flags.append("Near-term go-live date with weaker interconnection feasibility. This is a speed-to-power risk.")
    elif years <= 3:
        score -= 5
        flags.append("Moderate delivery timing risk. Require direct utility diligence.")

    if renewable and row["power_cost_stability"] <= 3:
        score -= 5
        flags.append("Renewable procurement requirement may add complexity. Confirm PPA or green-tariff options.")

    if latency and row["demand_signal"] >= 4:
        score += 5
        flags.append("Latency-sensitive use case supports the market thesis.")

    if behind_meter:
        score += 8
        flags.append("Behind-the-meter or dedicated generation can reduce grid delivery risk, subject to permitting and economics.")

    score = max(0, min(100, score))
    if score >= 78:
        result = "Strong fit"
    elif score >= 65:
        result = "Proceed with diligence"
    elif score >= 50:
        result = "Possible, but power-constrained"
    else:
        result = "Watchlist / alternative strategy"
    return result, score, flags

def fact_card(label, value, detail, source):
    with st.container(border=True):
        st.caption(label)
        st.markdown(f"### {value}")
        st.write(detail)
        st.caption(source)

def player_card(p):
    # stable brand tile using native Streamlit, no external images or local files
    with st.container(border=True):
        st.markdown(f"### {p['short']}")
        st.markdown(f"**{p['company']}**")
        st.caption(f"{p['group']} · {p['category']}")
        st.write(p["why"])

# Build data
df = pd.DataFrame(MARKETS)
players = pd.DataFrame(PLAYERS)
sources = pd.DataFrame(SOURCES)

st.title("⚡ Data Center Power Radar")
st.caption("Investor-style screener for data center power, interconnection risk, demand, cooling constraints, and real estate feasibility")

with st.expander("Adjust scoring weights", expanded=False):
    cols = st.columns(4)
    weights = {}
    for idx, col in enumerate(SCORE_COLUMNS):
        with cols[idx % 4]:
            weights[col] = st.slider(DISPLAY_NAMES[col], 0, 40, DEFAULT_WEIGHTS[col], 5)

df["overall_score"] = weighted_score(df, weights)
df["view"] = df["overall_score"].apply(classify)
df["opportunity_zone"] = df.apply(zone, axis=1)
df = df.sort_values("overall_score", ascending=False)

overview, screener, memo, players_tab, site_test, sources_tab = st.tabs(
    ["Overview", "Market Screener", "Market Memo", "Top Players", "Site Test", "Sources"]
)

with overview:
    st.subheader("Executive snapshot")
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        fact_card("U.S. data center power use", "176 TWh", "2023 usage, equal to about 4.4% of U.S. electricity.", "DOE / LBNL")
    with c2:
        fact_card("2028 U.S. estimate", "325-580 TWh", "Estimated U.S. data center electricity usage range by 2028.", "DOE / LBNL")
    with c3:
        fact_card("North America vacancy", "1%", "Record-low vacancy for a second consecutive year.", "JLL YE 2025")
    with c4:
        fact_card("North America pipeline", "35+ GW", "Capacity under construction in North America.", "JLL YE 2025")

    st.subheader("Market opportunity matrix")
    matrix = px.scatter(
        df,
        x="power_availability",
        y="demand_signal",
        size="overall_score",
        color="opportunity_zone",
        hover_name="market",
        hover_data=["region", "iso_rto", "overall_score", "view"],
        labels={
            "power_availability": "Power Availability Score",
            "demand_signal": "Demand Signal Score",
            "opportunity_zone": "Opportunity Zone",
            "overall_score": "Score",
        },
        height=560,
    )
    matrix.update_xaxes(range=[0.5, 5.5], dtick=1)
    matrix.update_yaxes(range=[0.5, 5.5], dtick=1)
    st.plotly_chart(matrix, use_container_width=True)

    st.subheader("What the dashboard is showing")
    a, b, c = st.columns(3)
    with a:
        with st.container(border=True):
            st.markdown("#### 1. Power is the first screen")
            st.write("Strong demand does not matter if power cannot be delivered on the tenant's timeline.")
    with b:
        with st.container(border=True):
            st.markdown("#### 2. Core markets are not always easiest")
            st.write("The deepest markets may also have the most constrained grid, land, and permitting dynamics.")
    with c:
        with st.container(border=True):
            st.markdown("#### 3. Emerging markets need proof")
            st.write("Better land and power still need tenant demand, utility support, and downside protection.")

with screener:
    st.subheader("Market Screener")
    f1, f2, f3 = st.columns(3)
    with f1:
        regions = st.multiselect("Region", sorted(df["region"].unique()), default=sorted(df["region"].unique()))
    with f2:
        types = st.multiselect("Market type", sorted(df["market_type"].unique()), default=sorted(df["market_type"].unique()))
    with f3:
        views = st.multiselect("Investor view", sorted(df["view"].unique()), default=sorted(df["view"].unique()))

    filtered = df[df["region"].isin(regions) & df["market_type"].isin(types) & df["view"].isin(views)].copy()

    st.dataframe(
        filtered[["market", "region", "iso_rto", "market_type", "overall_score", "view", "opportunity_zone", "fact_type", "status_note"]],
        use_container_width=True,
        hide_index=True,
        column_config={
            "overall_score": st.column_config.ProgressColumn("Score", min_value=0, max_value=100, format="%.1f"),
            "market": "Market",
            "iso_rto": "ISO / RTO",
            "market_type": "Type",
            "opportunity_zone": "Opportunity Zone",
            "fact_type": "Data Type",
            "status_note": "Note",
        },
    )

    left, right = st.columns([1.05, 1])
    with left:
        st.markdown("#### Ranked score")
        fig = px.bar(
            filtered.sort_values("overall_score", ascending=True),
            x="overall_score",
            y="market",
            orientation="h",
            color="view",
            hover_data=["region", "market_type", "opportunity_zone"],
            labels={"overall_score": "Overall Score", "market": "Market"},
            height=560,
        )
        st.plotly_chart(fig, use_container_width=True)

    with right:
        st.markdown("#### Risk heatmap")
        heat = filtered.set_index("market")[SCORE_COLUMNS].rename(columns=DISPLAY_NAMES)
        heat_fig = px.imshow(
            heat,
            aspect="auto",
            text_auto=True,
            color_continuous_scale="RdYlGn",
            zmin=1,
            zmax=5,
            height=560,
            labels=dict(x="Category", y="Market", color="Score"),
        )
        heat_fig.update_xaxes(tickangle=35)
        st.plotly_chart(heat_fig, use_container_width=True)

    st.markdown("#### Map")
    map_fig = px.scatter_mapbox(
        filtered,
        lat="lat",
        lon="lon",
        size="overall_score",
        color="view",
        hover_name="market",
        hover_data=["market_type", "region", "iso_rto", "overall_score"],
        mapbox_style="open-street-map",
        zoom=3,
        height=520,
    )
    st.plotly_chart(map_fig, use_container_width=True)

with memo:
    st.subheader("Market Memo")
    selected = st.selectbox("Choose a market", df["market"].tolist())
    row = df[df["market"] == selected].iloc[0]

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Score", f"{row['overall_score']:.1f}")
    m2.metric("View", row["view"])
    m3.metric("ISO / RTO", row["iso_rto"])
    m4.metric("Type", row["market_type"])

    left, right = st.columns([1.15, 0.85])
    with left:
        with st.container(border=True):
            st.markdown("#### Thesis")
            st.write(row["memo_thesis"])

        c1, c2 = st.columns(2)
        with c1:
            with st.container(border=True):
                st.markdown("#### Power situation")
                st.write(row["power_situation"])
        with c2:
            with st.container(border=True):
                st.markdown("#### Demand drivers")
                st.write(row["demand_drivers"])

        c3, c4 = st.columns(2)
        with c3:
            with st.container(border=True):
                st.markdown("#### Development constraints")
                st.write(row["development_constraints"])
        with c4:
            with st.container(border=True):
                st.markdown("#### Investor takeaway")
                st.write(row["investor_takeaway"])

    with right:
        st.plotly_chart(radar(row), use_container_width=True)

    st.info(
        f"Interview framing: {row['market']} is a {row['market_type'].lower()} market. "
        f"The diligence starts with power delivery, interconnection timeline, cooling, customer demand depth, and downside if power slips."
    )

with players_tab:
    st.subheader("Top Players")
    st.write("Grouped by ecosystem role. These are stable brand-style tiles, so there are no broken external logo links.")

    group_options = ["All"] + sorted(players["group"].unique().tolist())
    group_choice = st.selectbox("Filter group", group_options)
    pview = players if group_choice == "All" else players[players["group"] == group_choice]

    for group in pview["group"].drop_duplicates():
        st.markdown(f"### {group}")
        gdf = pview[pview["group"] == group]
        for start in range(0, len(gdf), 4):
            cols = st.columns(4)
            for col, (_, p) in zip(cols, gdf.iloc[start:start+4].iterrows()):
                with col:
                    player_card(p)

with site_test:
    st.subheader("Site Test")
    st.write("Use this as an interview demo. Change the MW need, go-live year, and power strategy to see how the screen changes.")

    c1, c2 = st.columns([1, 1])
    with c1:
        market = st.selectbox("Target market", df["market"].tolist(), key="site_market")
        mw = st.slider("Required IT load / power need", 5, 250, 50, 5)
        go_live = st.slider("Target go-live year", date.today().year, date.today().year + 8, date.today().year + 3)
    with c2:
        renewable = st.checkbox("Customer requires renewable / low-carbon power story", value=True)
        latency = st.checkbox("Latency-sensitive workload", value=False)
        behind_meter = st.checkbox("Behind-the-meter / dedicated generation option", value=False)

    site_row = df[df["market"] == market].iloc[0]
    result, site_score, flags = screen_site(site_row, mw, go_live, renewable, latency, behind_meter)

    k1, k2, k3 = st.columns(3)
    k1.metric("Screening result", result)
    k2.metric("Site score", f"{site_score}/100")
    k3.metric("Market base score", f"{site_row['overall_score']:.1f}/100")

    left, right = st.columns([1.05, 0.95])
    with left:
        with st.container(border=True):
            st.markdown("#### Key diligence flags")
            if flags:
                for item in flags:
                    st.write(f"• {item}")
            else:
                st.write("• No major flags from the simplified screen. Still verify utility capacity, land control, and tenant demand.")

        with st.container(border=True):
            st.markdown("#### Questions before underwriting")
            questions = [
                "Is the power allocation real, or only a preliminary utility conversation?",
                "What substation or transmission upgrades are required, who pays, and when can they be delivered?",
                "Is the power usable for the target MW by the required go-live date?",
                "Does the customer need renewable power, 24/7 carbon-free matching, or a general sustainability narrative?",
                "What is the cooling strategy, and does it create water, capex, or permitting risk?",
                "What is the downside plan if power is delayed by 12 to 24 months?",
            ]
            for q in questions:
                st.write(f"• {q}")

    with right:
        st.plotly_chart(radar(site_row), use_container_width=True)

with sources_tab:
    st.subheader("Sources & Methodology")
    st.write("The top fact cards use sourced data. The market scores are judgment-based underwriting scores and should be updated with utility, ISO/RTO, land, and tenant-specific diligence.")

    st.markdown("#### Verified facts used")
    st.dataframe(
        sources,
        use_container_width=True,
        hide_index=True,
        column_config={
            "url": st.column_config.LinkColumn("URL"),
            "metric": "Metric",
            "value": "Value",
            "fact": "Fact",
            "source": "Source",
        },
    )

    st.markdown("#### Scoring methodology")
    methodology = pd.DataFrame(
        {
            "Category": [DISPLAY_NAMES[c] for c in SCORE_COLUMNS],
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
        }
    )
    st.dataframe(methodology, use_container_width=True, hide_index=True)

    st.markdown("#### Best next upgrades")
    for u in [
        "Add ISO/RTO power price history by market.",
        "Add utility territory and substation proximity.",
        "Add powered-land parcels with acreage, zoning, and fiber proximity.",
        "Add public hyperscaler and colocation announcements by market.",
        "Add an exportable one-page PDF market memo.",
    ]:
        st.write(f"• {u}")
