from datetime import date
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

st.set_page_config(page_title="DC Power Radar", page_icon="⚡", layout="wide")

markets = [
    {"Market":"Northern Virginia","Region":"Mid-Atlantic","ISO/RTO":"PJM","Type":"Core hyperscale","Power":2,"Cost":3,"Interconnection":2,"Demand":5,"Friction":2,"Cooling":3,"Real Estate":3,"Lat":39.0438,"Lon":-77.4874,"Thesis":"The benchmark U.S. market, but power delivery and speed-to-power are the core underwriting issues."},
    {"Market":"Dallas / Fort Worth","Region":"Texas","ISO/RTO":"ERCOT","Type":"Core growth","Power":4,"Cost":3,"Interconnection":4,"Demand":5,"Friction":4,"Cooling":3,"Real Estate":4,"Lat":32.7767,"Lon":-96.7970,"Thesis":"Strong growth market with land, demand, and energy depth, but ERCOT volatility must be underwritten."},
    {"Market":"Phoenix","Region":"Southwest","ISO/RTO":"WECC","Type":"Core growth","Power":3,"Cost":3,"Interconnection":3,"Demand":4,"Friction":3,"Cooling":2,"Real Estate":4,"Lat":33.4484,"Lon":-112.0740,"Thesis":"Major western growth market where cooling, water, and utility-backed timelines matter."},
    {"Market":"Atlanta","Region":"Southeast","ISO/RTO":"Southeast","Type":"Core growth","Power":4,"Cost":4,"Interconnection":4,"Demand":4,"Friction":4,"Cooling":4,"Real Estate":4,"Lat":33.7490,"Lon":-84.3880,"Thesis":"Balanced growth market with southeast demand and relatively clean execution story."},
    {"Market":"Chicago","Region":"Midwest","ISO/RTO":"PJM / MISO","Type":"Core enterprise","Power":3,"Cost":3,"Interconnection":3,"Demand":4,"Friction":3,"Cooling":4,"Real Estate":3,"Lat":41.8781,"Lon":-87.6298,"Thesis":"Durable enterprise and connectivity market where site selection and utility territory matter."},
    {"Market":"Columbus / New Albany","Region":"Midwest","ISO/RTO":"PJM","Type":"Emerging hyperscale hub","Power":4,"Cost":4,"Interconnection":4,"Demand":5,"Friction":4,"Cooling":4,"Real Estate":4,"Lat":40.0812,"Lon":-82.8088,"Thesis":"A strong example of hyperscale demand following credible land, power, and economic development alignment."},
    {"Market":"NYC / Northern New Jersey","Region":"Northeast","ISO/RTO":"NYISO / PJM","Type":"Edge / enterprise","Power":2,"Cost":2,"Interconnection":2,"Demand":4,"Friction":2,"Cooling":3,"Real Estate":2,"Lat":40.7128,"Lon":-74.0060,"Thesis":"High-value latency and enterprise market, but difficult for cheap hyperscale capacity."},
    {"Market":"Richmond","Region":"Mid-Atlantic","ISO/RTO":"PJM","Type":"Expansion market","Power":3,"Cost":3,"Interconnection":3,"Demand":4,"Friction":3,"Cooling":4,"Real Estate":4,"Lat":37.5407,"Lon":-77.4360,"Thesis":"Mid-Atlantic spillover market where utility and local approvals determine execution."},
    {"Market":"Fairfield County, CT","Region":"Northeast","ISO/RTO":"ISO-NE","Type":"Edge / financial services","Power":2,"Cost":2,"Interconnection":2,"Demand":3,"Friction":2,"Cooling":4,"Real Estate":3,"Lat":41.0534,"Lon":-73.5387,"Thesis":"Local edge thesis tied to NYC proximity and financial-services workloads, not a top hyperscale market."},
    {"Market":"Kansas City","Region":"Midwest","ISO/RTO":"SPP / MISO","Type":"Emerging growth","Power":4,"Cost":4,"Interconnection":4,"Demand":3,"Friction":4,"Cooling":4,"Real Estate":5,"Lat":39.0997,"Lon":-94.5786,"Thesis":"Power-led emerging-market screen that needs tenant and utility validation."},
    {"Market":"Salt Lake City","Region":"Mountain West","ISO/RTO":"WECC","Type":"Emerging growth","Power":3,"Cost":4,"Interconnection":3,"Demand":3,"Friction":4,"Cooling":3,"Real Estate":4,"Lat":40.7608,"Lon":-111.8910,"Thesis":"Secondary western market with possible operating advantages but tenant-depth questions."},
    {"Market":"Reno","Region":"Mountain West","ISO/RTO":"WECC","Type":"Western expansion","Power":3,"Cost":3,"Interconnection":3,"Demand":3,"Friction":4,"Cooling":3,"Real Estate":4,"Lat":39.5296,"Lon":-119.8138,"Thesis":"Western expansion screen where power delivery and demand depth should be tested carefully."},
]

players = [
    ("Equinix","EQIX","Operators","Interconnection / colocation"),
    ("Digital Realty","DLR","Operators","Wholesale / colocation"),
    ("NTT Global Data Centers","NTT","Operators","Hyperscale / colocation"),
    ("Vantage Data Centers","VNTG","Operators","Hyperscale campus"),
    ("QTS","QTS","Operators","Hyperscale / colocation"),
    ("STACK Infrastructure","STK","Operators","Hyperscale / colocation"),
    ("CyrusOne","C1","Operators","Hyperscale / colocation"),
    ("CoreSite","CORE","Operators","Interconnection / colocation"),
    ("AWS","AWS","Demand Drivers","Hyperscaler"),
    ("Microsoft Azure","AZR","Demand Drivers","Cloud / AI"),
    ("Google Cloud","GCP","Demand Drivers","Cloud / AI"),
    ("Meta","META","Demand Drivers","AI / owner-operator"),
    ("Oracle Cloud","OCI","Demand Drivers","Cloud / AI"),
    ("CoreWeave","CW","Demand Drivers","AI cloud"),
    ("NVIDIA","NVDA","Ecosystem","AI infrastructure"),
    ("Constellation","CEG","Power Ecosystem","Power / nuclear"),
    ("NextEra Energy","NEE","Power Ecosystem","Power / renewables"),
    ("GE Vernova","GEV","Power Ecosystem","Power equipment"),
]

sources = pd.DataFrame([
    ["U.S. data center electricity use","176 TWh","DOE / LBNL reported U.S. data centers used 176 TWh in 2023, about 4.4% of U.S. electricity.","DOE / LBNL","https://www.energy.gov/articles/doe-releases-new-report-evaluating-increase-electricity-demand-data-centers"],
    ["2028 U.S. electricity estimate","325 to 580 TWh","DOE / LBNL estimated U.S. data center electricity use could reach 325 to 580 TWh by 2028.","DOE / LBNL","https://www.energy.gov/articles/doe-releases-new-report-evaluating-increase-electricity-demand-data-centers"],
    ["North America vacancy","1%","JLL reported North American data center vacancy remained at 1% for a second consecutive year at year-end 2025.","JLL","https://www.jll.com/en-us/insights/market-dynamics/north-america-data-centers"],
    ["North America construction pipeline","35+ GW","JLL reported more than 35 GW of data center capacity under construction in North America at year-end 2025.","JLL","https://www.jll.com/en-us/insights/market-dynamics/north-america-data-centers"],
    ["Pipeline precommitment","92%","JLL reported 92% of North American capacity under construction was precommitted at year-end 2025.","JLL","https://www.jll.com/en-us/insights/market-dynamics/north-america-data-centers"],
    ["Power availability constraint","Key bottleneck","CBRE reported limited power availability remains a key inhibitor of growth in certain core hub markets.","CBRE","https://www.cbre.com/insights/reports/global-data-center-trends-2025"],
], columns=["Metric","Value","Fact","Source","URL"])

score_cols = ["Power","Cost","Interconnection","Demand","Friction","Cooling","Real Estate"]
default_weights = {"Power":25,"Cost":10,"Interconnection":20,"Demand":20,"Friction":10,"Cooling":5,"Real Estate":10}

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
    labels = score_cols
    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(r=vals + [vals[0]], theta=labels + [labels[0]], fill="toself"))
    fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0,5])), showlegend=False, height=400)
    return fig

def fact_card(label, value, text, source):
    with st.container(border=True):
        st.caption(label)
        st.markdown(f"### {value}")
        st.write(text)
        st.caption(source)

st.title("⚡ Data Center Power Radar")
st.caption("Investor-style screener for data center power, interconnection risk, demand, cooling, and real estate feasibility")

with st.expander("Adjust scoring weights"):
    weight_cols = st.columns(4)
    weights = {}
    for i, c in enumerate(score_cols):
        with weight_cols[i % 4]:
            weights[c] = st.slider(c, 0, 40, default_weights[c], 5)

df = pd.DataFrame(markets)
total_weight = sum(weights.values())
df["Score"] = (sum(df[c] * weights[c] for c in score_cols) / total_weight * 20).round(1)
df["Investor View"] = df["Score"].apply(classify)
df["Opportunity Zone"] = df.apply(opportunity, axis=1)
df = df.sort_values("Score", ascending=False)

overview, screener, memo, player_tab, site_tab, source_tab = st.tabs(["Overview","Market Screener","Market Memo","Top Players","Site Test","Sources"])

with overview:
    st.subheader("Executive snapshot")
    a,b,c,d = st.columns(4)
    with a: fact_card("U.S. data center power use","176 TWh","2023 usage, equal to about 4.4% of U.S. electricity.","DOE / LBNL")
    with b: fact_card("2028 U.S. estimate","325-580 TWh","Estimated U.S. data center electricity usage range by 2028.","DOE / LBNL")
    with c: fact_card("North America vacancy","1%","Record-low vacancy for a second consecutive year.","JLL YE 2025")
    with d: fact_card("North America pipeline","35+ GW","Capacity under construction in North America.","JLL YE 2025")

    st.subheader("Market opportunity matrix")
    fig = px.scatter(
        df, x="Power", y="Demand", size="Score", color="Opportunity Zone",
        hover_name="Market", hover_data=["Region","ISO/RTO","Investor View"],
        height=540
    )
    fig.update_xaxes(range=[0.5,5.5], dtick=1)
    fig.update_yaxes(range=[0.5,5.5], dtick=1)
    st.plotly_chart(fig, use_container_width=True, key="overview_matrix")

    st.subheader("Main takeaway")
    x,y,z = st.columns(3)
    with x:
        with st.container(border=True):
            st.markdown("#### 1. Power is the first screen")
            st.write("Demand does not matter if power cannot be delivered on the tenant's timeline.")
    with y:
        with st.container(border=True):
            st.markdown("#### 2. Core markets are not always easiest")
            st.write("The deepest markets may also have the most constrained grid, land, and permitting dynamics.")
    with z:
        with st.container(border=True):
            st.markdown("#### 3. Emerging markets need proof")
            st.write("Better land and power still need tenant demand, utility support, and downside protection.")

with screener:
    st.subheader("Market Screener")
    r1,r2,r3 = st.columns(3)
    with r1:
        regions = st.multiselect("Region", sorted(df["Region"].unique()), default=sorted(df["Region"].unique()))
    with r2:
        types = st.multiselect("Market type", sorted(df["Type"].unique()), default=sorted(df["Type"].unique()))
    with r3:
        views = st.multiselect("Investor view", sorted(df["Investor View"].unique()), default=sorted(df["Investor View"].unique()))

    filtered = df[df["Region"].isin(regions) & df["Type"].isin(types) & df["Investor View"].isin(views)]

    st.dataframe(
        filtered[["Market","Region","ISO/RTO","Type","Score","Investor View","Opportunity Zone","Thesis"]],
        use_container_width=True,
        hide_index=True,
        column_config={"Score": st.column_config.ProgressColumn("Score", min_value=0, max_value=100, format="%.1f")}
    )

    left, right = st.columns([1.05, 1])
    with left:
        bar = px.bar(filtered.sort_values("Score"), x="Score", y="Market", color="Investor View", orientation="h", height=560)
        st.plotly_chart(bar, use_container_width=True, key="ranked_bar")
    with right:
        heat = filtered.set_index("Market")[score_cols]
        heat_fig = px.imshow(heat, text_auto=True, color_continuous_scale="RdYlGn", zmin=1, zmax=5, height=560)
        heat_fig.update_xaxes(tickangle=35)
        st.plotly_chart(heat_fig, use_container_width=True, key="heatmap")

    map_fig = px.scatter_mapbox(
        filtered, lat="Lat", lon="Lon", size="Score", color="Investor View",
        hover_name="Market", hover_data=["Type","Region","ISO/RTO","Score"],
        mapbox_style="open-street-map", zoom=3, height=520
    )
    st.plotly_chart(map_fig, use_container_width=True, key="map")

with memo:
    st.subheader("Market Memo")
    selected = st.selectbox("Choose a market", df["Market"].tolist())
    row = df[df["Market"] == selected].iloc[0]
    m1,m2,m3,m4 = st.columns(4)
    m1.metric("Score", f"{row['Score']:.1f}")
    m2.metric("View", row["Investor View"])
    m3.metric("ISO / RTO", row["ISO/RTO"])
    m4.metric("Type", row["Type"])
    left, right = st.columns([1.15, .85])
    with left:
        for title, field in [
            ("Thesis","Thesis"),
            ("Power situation","Thesis"),
            ("Demand drivers","Opportunity Zone"),
        ]:
            with st.container(border=True):
                st.markdown(f"#### {title}")
                st.write(row[field])
        st.info("Interview framing: start with power delivery, interconnection timeline, cooling, customer demand depth, and downside if power slips.")
    with right:
        st.plotly_chart(radar_chart(row), use_container_width=True, key="memo_radar")

with player_tab:
    st.subheader("Top Players")
    st.write("Grouped by ecosystem role. These are stable text tiles, so there are no broken logo links.")
    player_df = pd.DataFrame(players, columns=["Company","Ticker","Group","Category"])
    for group in player_df["Group"].drop_duplicates():
        st.markdown(f"### {group}")
        chunk = player_df[player_df["Group"] == group]
        for start in range(0, len(chunk), 4):
            cols = st.columns(4)
            for col, (_, p) in zip(cols, chunk.iloc[start:start+4].iterrows()):
                with col:
                    with st.container(border=True):
                        st.markdown(f"### {p['Ticker']}")
                        st.markdown(f"**{p['Company']}**")
                        st.caption(p["Category"])

with site_tab:
    st.subheader("Site Test")
    c1,c2 = st.columns(2)
    with c1:
        market = st.selectbox("Target market", df["Market"].tolist(), key="site_market")
        mw = st.slider("Required IT load / power need", 5, 250, 50, 5)
        go_live = st.slider("Target go-live year", date.today().year, date.today().year + 8, date.today().year + 3)
    with c2:
        renewable = st.checkbox("Customer requires renewable / low-carbon power story", value=True)
        latency = st.checkbox("Latency-sensitive workload", value=False)
        behind_meter = st.checkbox("Behind-the-meter / dedicated generation option", value=False)

    row = df[df["Market"] == market].iloc[0]
    site_score = int(row["Score"])
    flags = []
    if mw >= 100:
        site_score -= 18
        flags.append("Large load request. Utility commitment and substation timeline are gating items.")
    elif mw >= 50:
        site_score -= 10
        flags.append("Meaningful load request. Test whether power is real, deliverable, and within the target date.")
    if go_live - date.today().year <= 3:
        site_score -= 5
        flags.append("Near-term go-live. Require direct utility diligence.")
    if renewable:
        flags.append("Confirm PPA, utility green tariff, or other renewable procurement path.")
    if latency:
        flags.append("Confirm the market actually supports the latency-sensitive use case.")
    if behind_meter:
        site_score += 8
        flags.append("Behind-the-meter strategy can reduce grid risk, subject to permitting and economics.")

    site_score = max(0, min(100, site_score))
    result = classify(site_score)
    s1,s2,s3 = st.columns(3)
    s1.metric("Screening result", result)
    s2.metric("Site score", f"{site_score}/100")
    s3.metric("Market base score", f"{row['Score']:.1f}/100")
    for flag in flags:
        st.write(f"• {flag}")

with source_tab:
    st.subheader("Sources & Methodology")
    st.write("Fact cards use sourced public market data. Market scores are judgment-based underwriting scores for interview demonstration.")
    st.dataframe(
        sources,
        use_container_width=True,
        hide_index=True,
        column_config={"URL": st.column_config.LinkColumn("URL")}
    )
