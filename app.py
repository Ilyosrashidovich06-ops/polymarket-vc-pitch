import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import requests
from datetime import datetime

st.set_page_config(
    page_title="Polymarket — VC Pitch 2026",
    page_icon="🔮",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');
* { font-family: 'Inter', sans-serif; }
html, body, [data-testid="stAppViewContainer"] { background-color: #07070f; color: #ffffff; }
[data-testid="stHeader"] { background: rgba(7,7,15,0.97); }
[data-testid="stSidebar"] { background: #0d0d1a; }
.block-container { padding: 0 2rem 4rem 2rem; max-width: 1400px; margin: auto; }

.cover {
    background: linear-gradient(135deg, #0a0a20 0%, #1a0533 40%, #001a3d 100%);
    border: 1px solid rgba(0,212,255,0.12); border-radius: 24px;
    padding: 64px 60px 56px; margin: 24px 0 40px;
    position: relative; overflow: hidden; text-align: center;
}
.cover::before {
    content: ''; position: absolute; inset: 0;
    background: radial-gradient(ellipse at 25% 60%, rgba(124,58,237,0.18) 0%, transparent 55%),
                radial-gradient(ellipse at 75% 40%, rgba(0,212,255,0.12) 0%, transparent 55%);
}
.cover-university { font-size:13px; font-weight:600; letter-spacing:2px; text-transform:uppercase; color:rgba(255,255,255,0.5); margin-bottom:5px; }
.cover-module { font-size:14px; color:rgba(255,255,255,0.38); margin-bottom:30px; }
.cover-badge { display:inline-block; background:rgba(0,212,255,0.1); border:1px solid rgba(0,212,255,0.35); border-radius:50px; padding:6px 20px; font-size:12px; font-weight:700; color:#00d4ff; letter-spacing:2px; text-transform:uppercase; margin-bottom:22px; }
.cover h1 { font-size:clamp(34px,5vw,68px); font-weight:900; line-height:1.05; margin:0 0 22px; background:linear-gradient(135deg,#ffffff 0%,#00d4ff 50%,#7c3aed 100%); -webkit-background-clip:text; -webkit-text-fill-color:transparent; background-clip:text; }
.cover-sub { font-size:19px; color:rgba(255,255,255,0.62); max-width:660px; margin:0 auto 36px; line-height:1.55; }
.cover-authors { display:flex; justify-content:center; gap:36px; flex-wrap:wrap; border-top:1px solid rgba(255,255,255,0.08); padding-top:28px; margin-top:8px; }
.cover-author-name { font-size:16px; font-weight:700; color:#fff; }
.cover-author-id { font-size:12px; color:rgba(255,255,255,0.42); margin-top:2px; }
.cover-prof { font-size:14px; color:rgba(255,255,255,0.5); margin-top:3px; }

.stat-card { background:rgba(255,255,255,0.04); border:1px solid rgba(255,255,255,0.08); border-radius:16px; padding:24px 18px; text-align:center; transition:all 0.3s; }
.stat-card:hover { border-color:rgba(0,212,255,0.32); background:rgba(0,212,255,0.05); transform:translateY(-3px); }
.stat-number { font-size:36px; font-weight:800; color:#00d4ff; line-height:1; }
.stat-label { font-size:12px; color:rgba(255,255,255,0.48); margin-top:8px; font-weight:500; }

.section-tag { display:inline-block; background:rgba(124,58,237,0.14); border:1px solid rgba(124,58,237,0.35); border-radius:50px; padding:4px 16px; font-size:11px; font-weight:700; color:#a78bfa; letter-spacing:2px; text-transform:uppercase; margin-bottom:10px; }
.section-title { font-size:clamp(24px,3.5vw,44px); font-weight:800; line-height:1.1; margin:0 0 6px; }
.section-sub { font-size:16px; color:rgba(255,255,255,0.5); margin-bottom:34px; line-height:1.5; }

.card { background:rgba(255,255,255,0.04); border:1px solid rgba(255,255,255,0.08); border-radius:20px; padding:30px; transition:all 0.3s; }
.card:hover { border-color:rgba(0,212,255,0.26); background:rgba(0,212,255,0.04); }

.trade-card { background:linear-gradient(135deg,rgba(0,212,255,0.04),rgba(124,58,237,0.04)); border:1px solid rgba(0,212,255,0.18); border-radius:18px; padding:24px; margin-bottom:12px; position:relative; overflow:hidden; }
.trade-card::before { content:''; position:absolute; left:0; top:0; bottom:0; width:4px; background:linear-gradient(180deg,#00d4ff,#7c3aed); border-radius:4px 0 0 4px; }
.trade-category { font-size:11px; font-weight:700; color:#00d4ff; letter-spacing:2px; text-transform:uppercase; margin-bottom:8px; }
.trade-title { font-size:17px; font-weight:700; margin-bottom:10px; }
.trade-volume { font-size:24px; font-weight:800; color:#00ff88; }
.trade-desc { font-size:13px; color:rgba(255,255,255,0.58); line-height:1.65; margin-top:10px; }

.investor-card { background:rgba(255,255,255,0.04); border:1px solid rgba(255,255,255,0.09); border-radius:16px; padding:22px; text-align:center; transition:all 0.3s; }
.investor-card:hover { border-color:rgba(0,212,255,0.32); transform:translateY(-4px); }
.investor-name { font-size:17px; font-weight:700; margin-bottom:5px; }
.investor-role { font-size:12px; color:rgba(255,255,255,0.42); margin-bottom:12px; }
.investor-signal { font-size:13px; color:#00d4ff; background:rgba(0,212,255,0.08); border-radius:8px; padding:8px 12px; line-height:1.5; }

.risk-high { color:#ff4757; background:rgba(255,71,87,0.1); border:1px solid rgba(255,71,87,0.3); }
.risk-med  { color:#ffa502; background:rgba(255,165,2,0.1);  border:1px solid rgba(255,165,2,0.3); }
.risk-low  { color:#00ff88; background:rgba(0,255,136,0.1);  border:1px solid rgba(0,255,136,0.3); }
.risk-pill { display:inline-block; border-radius:50px; padding:4px 14px; font-size:11px; font-weight:700; letter-spacing:1px; text-transform:uppercase; }

.reco-box { background:linear-gradient(135deg,rgba(0,255,136,0.05),rgba(0,212,255,0.05)); border:2px solid rgba(0,255,136,0.28); border-radius:24px; padding:48px; text-align:center; }
.reco-verdict { font-size:48px; font-weight:900; background:linear-gradient(135deg,#00ff88,#00d4ff); -webkit-background-clip:text; -webkit-text-fill-color:transparent; background-clip:text; margin-bottom:16px; }

.live-card { background:rgba(0,255,136,0.04); border:1px solid rgba(0,255,136,0.18); border-radius:14px; padding:16px 20px; margin-bottom:10px; display:flex; justify-content:space-between; align-items:center; }
.live-dot { display:inline-block; width:8px; height:8px; border-radius:50%; background:#00ff88; margin-right:8px; animation:pulse 2s infinite; }
@keyframes pulse { 0%,100%{opacity:1} 50%{opacity:0.25} }
.probability-bar { height:7px; border-radius:4px; background:rgba(255,255,255,0.08); margin-top:8px; overflow:hidden; }
.probability-fill { height:100%; border-radius:4px; background:linear-gradient(90deg,#7c3aed,#00d4ff); }

.tl-item { display:flex; gap:18px; margin-bottom:24px; }
.tl-dot { width:42px; height:42px; border-radius:50%; display:flex; align-items:center; justify-content:center; font-size:16px; font-weight:800; flex-shrink:0; color:white; }
.tl-content { flex:1; padding-top:4px; }
.tl-year { font-size:11px; color:#00d4ff; font-weight:700; letter-spacing:2px; }
.tl-desc { font-size:13px; color:rgba(255,255,255,0.6); line-height:1.55; margin-top:2px; }

.chip { display:inline-block; border-radius:50px; padding:7px 18px; font-size:13px; font-weight:600; margin:4px; }
.chip-blue   { background:rgba(0,212,255,0.12); border:1px solid rgba(0,212,255,0.3); color:#00d4ff; }
.chip-purple { background:rgba(124,58,237,0.12); border:1px solid rgba(124,58,237,0.3); color:#a78bfa; }
.chip-green  { background:rgba(0,255,136,0.12); border:1px solid rgba(0,255,136,0.3); color:#00ff88; }

.divider { border:none; border-top:1px solid rgba(255,255,255,0.06); margin:52px 0; }
.info-box { background:rgba(0,212,255,0.06); border:1px solid rgba(0,212,255,0.22); border-radius:14px; padding:18px 22px; margin-top:14px; }
</style>
""", unsafe_allow_html=True)

# ── Sidebar ────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### Navigation")
    st.radio("Go to", [
        "🏠 Cover", "📖 What Is Polymarket?", "🧑‍💻 The Founder",
        "🔥 Iconic Trades", "📈 Volume Growth", "💼 Business Model",
        "🌍 Market Opportunity", "⚔️ Competition",
        "📊 SWOT", "⚠️ Risks", "✅ Investment Thesis", "📡 Live Markets",
    ], label_visibility="collapsed")
    st.markdown("---")
    st.markdown("**Leon Ye** · 1616910")
    st.markdown("**Ilyos Umurzakov** · 1615067")
    st.markdown("Prof. James Slawney")
    st.markdown("Frankfurt UAS · SS 2026")


# ══════════════════════════════════════════════════════════════════════════════
# COVER
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<div class="cover">
  <div class="cover-university">Frankfurt University of Applied Sciences &nbsp;·&nbsp; Faculty 3 – Business and Law</div>
  <div class="cover-module">Module: English for Presentations &nbsp;|&nbsp; Summer Semester 2026 &nbsp;|&nbsp; Prof. James Slawney</div>
  <div class="cover-badge">VC Pitch Deck · 2026</div>
  <h1>Polymarket as a Venture Capital<br>Investment Opportunity</h1>
  <p class="cover-sub">
    A blockchain-native prediction market that turned human uncertainty into
    the world's most accurate forecasting engine — and a $9 billion company.
  </p>
  <div style="display:flex;gap:10px;justify-content:center;flex-wrap:wrap;margin-bottom:36px;">
    <span class="chip chip-blue">🔮 Blockchain-Native</span>
    <span class="chip chip-purple">📊 $9B Valuation</span>
    <span class="chip chip-green">✅ NYSE-Backed</span>
    <span class="chip chip-blue">🌍 445K+ Active Traders</span>
  </div>
  <div class="cover-authors">
    <div style="text-align:center;">
      <div class="cover-author-name">Leon Ye</div>
      <div class="cover-author-id">Matriculation No. 1616910</div>
    </div>
    <div style="border-left:1px solid rgba(255,255,255,0.12);"></div>
    <div style="text-align:center;">
      <div class="cover-author-name">Ilyos Umurzakov</div>
      <div class="cover-author-id">Matriculation No. 1615067</div>
    </div>
    <div style="border-left:1px solid rgba(255,255,255,0.12);"></div>
    <div style="text-align:center;">
      <div class="cover-prof">Supervisor: Prof. James Slawney</div>
      <div class="cover-prof">Submitted: 5 June 2026 · Frankfurt am Main</div>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

c1, c2, c3, c4, c5 = st.columns(5)
for col, (num, lbl) in zip([c1,c2,c3,c4,c5], [
    ("$9B","Post-ICE Valuation"), ("$3.7B+","2024 Election Volume"),
    ("445K+","Active Traders Oct'25"), ("$74M+","Total VC Raised"), ("#1","Global Prediction Market"),
]):
    with col:
        st.markdown(f'<div class="stat-card"><div class="stat-number">{num}</div><div class="stat-label">{lbl}</div></div>', unsafe_allow_html=True)

st.markdown("<hr class='divider'>", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# 1 · WHAT IS POLYMARKET?
# ══════════════════════════════════════════════════════════════════════════════
st.markdown('<div class="section-tag">What Is Polymarket?</div>', unsafe_allow_html=True)
st.markdown('<div class="section-title">Probability, Priced in Real Time</div>', unsafe_allow_html=True)
st.markdown('<div class="section-sub">A blockchain-powered marketplace where event contracts trade like stocks — prices reveal what the crowd <em>actually</em> believes.</div>', unsafe_allow_html=True)

col_l, col_r = st.columns([1.1, 1])
with col_l:
    st.markdown("""
    <div class="card">
      <div style="font-size:20px;font-weight:700;margin-bottom:18px;">How It Works — Step by Step</div>
      <div style="display:flex;gap:12px;align-items:flex-start;margin-bottom:20px;">
        <div style="width:36px;height:36px;border-radius:10px;background:rgba(0,212,255,0.14);display:flex;align-items:center;justify-content:center;font-size:17px;flex-shrink:0;">❓</div>
        <div><div style="font-weight:600;margin-bottom:3px;">A real-world question gets listed</div>
        <div style="color:rgba(255,255,255,0.56);font-size:13px;">"Will Trump win the 2024 election?" — YES and NO contracts go live instantly on-chain.</div></div>
      </div>
      <div style="display:flex;gap:12px;align-items:flex-start;margin-bottom:20px;">
        <div style="width:36px;height:36px;border-radius:10px;background:rgba(124,58,237,0.14);display:flex;align-items:center;justify-content:center;font-size:17px;flex-shrink:0;">💱</div>
        <div><div style="font-weight:600;margin-bottom:3px;">Traders buy and sell with USDC</div>
        <div style="color:rgba(255,255,255,0.56);font-size:13px;">A YES contract at $0.72 implies <strong>72% probability</strong>. Price moves with every trade — continuously reflecting collective belief.</div></div>
      </div>
      <div style="display:flex;gap:12px;align-items:flex-start;margin-bottom:20px;">
        <div style="width:36px;height:36px;border-radius:10px;background:rgba(0,255,136,0.14);display:flex;align-items:center;justify-content:center;font-size:17px;flex-shrink:0;">✅</div>
        <div><div style="font-weight:600;margin-bottom:3px;">Event resolves — winners paid on-chain</div>
        <div style="color:rgba(255,255,255,0.56);font-size:13px;">Winners receive $1.00 per contract. Losers get $0. Settlement instant, transparent, tamper-proof via smart contract.</div></div>
      </div>
      <div style="display:flex;gap:12px;align-items:flex-start;">
        <div style="width:36px;height:36px;border-radius:10px;background:rgba(255,165,2,0.14);display:flex;align-items:center;justify-content:center;font-size:17px;flex-shrink:0;">📡</div>
        <div><div style="font-weight:600;margin-bottom:3px;">Prices become a public intelligence feed</div>
        <div style="color:rgba(255,255,255,0.56);font-size:13px;">CNN, Reuters, the FT, BBC quote Polymarket odds daily. It is no longer gambling — it is a <strong>live forecasting layer for the internet</strong>.</div></div>
      </div>
    </div>
    """, unsafe_allow_html=True)

with col_r:
    fig_gauge = go.Figure(go.Indicator(
        mode="gauge+number", value=72,
        title={"text": "Trump wins 2024 election?<br><span style='font-size:12px;color:#aaa'>Polymarket: 72% · Polls: 50/50</span>",
               "font": {"color": "white", "size": 14}},
        number={"suffix": "% YES", "font": {"color": "#00d4ff", "size": 36}},
        gauge={
            "axis": {"range": [0, 100]},
            "bar": {"color": "#00d4ff", "thickness": 0.28},
            "bgcolor": "rgba(255,255,255,0.04)", "borderwidth": 0,
            "threshold": {"line": {"color": "#00ff88", "width": 3}, "value": 72},
            "steps": [{"range": [0,50], "color": "rgba(255,71,87,0.1)"},
                      {"range": [50,100], "color": "rgba(0,212,255,0.07)"}],
        },
    ))
    fig_gauge.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        height=280, font={"color": "white"}, margin=dict(t=60, b=10, l=20, r=20),
    )
    st.plotly_chart(fig_gauge, use_container_width=True)
    st.markdown("""
    <div class="info-box">
      <div style="font-size:12px;color:#00ff88;font-weight:700;letter-spacing:1px;text-transform:uppercase;margin-bottom:7px;">Why This Matters</div>
      <div style="font-size:13px;color:rgba(255,255,255,0.72);line-height:1.6;">
        Polymarket's 72% odds on Trump outpaced <strong>every major poll</strong> showing a 50/50 race.
        Financial incentives produce truthful information. That is the core product insight.
      </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<hr class='divider'>", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# 2 · FOUNDER
# ══════════════════════════════════════════════════════════════════════════════
st.markdown('<div class="section-tag">The Founder</div>', unsafe_allow_html=True)
st.markdown('<div class="section-title">Shayne Coplan — Built a Billion by 27</div>', unsafe_allow_html=True)

col_f1, col_f2 = st.columns([1, 2.1])
with col_f1:
    try:
        st.image("shayne_coplan.webp", caption="Shayne Coplan — CEO & Founder, Polymarket", use_container_width=True)
    except Exception:
        st.markdown('<div style="background:rgba(0,212,255,0.06);border:1px solid rgba(0,212,255,0.2);border-radius:16px;padding:60px 20px;text-align:center;font-size:60px;">👤</div>', unsafe_allow_html=True)

with col_f2:
    st.markdown("""
    <div class="card" style="height:auto;">
      <div style="display:flex;gap:12px;margin-bottom:22px;flex-wrap:wrap;">
        <div style="background:rgba(0,212,255,0.09);border:1px solid rgba(0,212,255,0.22);border-radius:12px;padding:12px 16px;text-align:center;">
          <div style="font-size:24px;font-weight:800;color:#00d4ff;">27</div><div style="font-size:10px;color:rgba(255,255,255,0.42);">Years Old</div>
        </div>
        <div style="background:rgba(124,58,237,0.09);border:1px solid rgba(124,58,237,0.22);border-radius:12px;padding:12px 16px;text-align:center;">
          <div style="font-size:24px;font-weight:800;color:#a78bfa;">$1B+</div><div style="font-size:10px;color:rgba(255,255,255,0.42);">Net Worth (Forbes)</div>
        </div>
        <div style="background:rgba(0,255,136,0.09);border:1px solid rgba(0,255,136,0.22);border-radius:12px;padding:12px 16px;text-align:center;">
          <div style="font-size:24px;font-weight:800;color:#00ff88;">2020</div><div style="font-size:10px;color:rgba(255,255,255,0.42);">Founded Age 22</div>
        </div>
        <div style="background:rgba(255,165,2,0.09);border:1px solid rgba(255,165,2,0.22);border-radius:12px;padding:12px 16px;text-align:center;">
          <div style="font-size:24px;font-weight:800;color:#ffa502;">#1</div><div style="font-size:10px;color:rgba(255,255,255,0.42);">Youngest Billionaire Bloomberg 2025</div>
        </div>
      </div>
      <div style="display:grid;gap:14px;">
        <div style="display:flex;gap:12px;"><span style="font-size:17px;">🏙️</span>
          <div><strong>Born 1998 · Upper West Side, Manhattan</strong>
          <div style="color:rgba(255,255,255,0.56);font-size:13px;margin-top:2px;">Raised in Hell's Kitchen, NYC. Bought Ethereum in 2014 at <strong style="color:#00d4ff;">$0.30/ETH</strong> as a teenager — one of the earliest retail crypto investors on earth.</div></div>
        </div>
        <div style="display:flex;gap:12px;"><span style="font-size:17px;">🎓</span>
          <div><strong>NYU Computer Science Dropout → Solo Founder</strong>
          <div style="color:rgba(255,255,255,0.56);font-size:13px;margin-top:2px;">Left NYU in his freshman year to pursue blockchain full-time. Built Polymarket entirely alone from his Lower East Side apartment in June 2020.</div></div>
        </div>
        <div style="display:flex;gap:12px;"><span style="font-size:17px;">🔮</span>
          <div><strong>Mission: Markets as Truth Machines</strong>
          <div style="color:rgba(255,255,255,0.56);font-size:13px;margin-top:2px;">Coplan's founding thesis: financial incentives produce the most honest information aggregation ever built. Prediction markets are the mechanism. Five years later, the world's largest media organisations quote his platform's odds as fact.</div></div>
        </div>
        <div style="display:flex;gap:12px;"><span style="font-size:17px;">⚡</span>
          <div><strong>World's Youngest Self-Made Billionaire (Bloomberg, Oct 2025)</strong>
          <div style="color:rgba(255,255,255,0.56);font-size:13px;margin-top:2px;">After ICE's $2B investment at a $9B valuation, Bloomberg confirmed Coplan's billionaire status at 27. The FBI search of his home after the 2024 election was described by Polymarket as politically motivated. No charges were ever filed.</div></div>
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<hr class='divider'>", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# 3 · ICONIC TRADES
# ══════════════════════════════════════════════════════════════════════════════
st.markdown('<div class="section-tag">Iconic Trades</div>', unsafe_allow_html=True)
st.markdown('<div class="section-title">Where Polymarket Made History</div>', unsafe_allow_html=True)
st.markdown('<div class="section-sub">These were not just bets. They were often more accurate than government briefings, expert panels, and trillion-dollar financial models.</div>', unsafe_allow_html=True)

trades = [
    ("POLITICS · 2024","🗳️","Will Trump win the 2024 U.S. Presidential Election?","$3.7B+ in bets",
     "Polymarket showed Trump at 65–72% in early October while every major poll showed 50/50. The market called it weeks before election night and was quoted by CNN, Bloomberg, the FT, and the BBC. A single market placed Polymarket on the front page of every major newspaper on earth.",
     "RESOLVED: YES ✓","#00ff88"),
    ("CRYPTO · 2024","₿","Will Bitcoin hit $100,000 before end of 2024?","$250M+ volume",
     "With Bitcoin at ~$60K in October, Polymarket climbed to 45% YES. BTC hit $100K in December. Traders who bought YES at $0.30 made a 3x return in under two months. One crypto price contract attracted more volume than many mid-sized hedge funds manage in a year.",
     "RESOLVED: YES ✓","#00ff88"),
    ("GEOPOLITICS · 2024","🕊️","Will there be a Gaza ceasefire deal before 2025?","$45M+ volume",
     "Markets fluctuated from 20% to 80% in real time as negotiations unfolded across Qatar, Egypt, and Washington. Diplomats and White House analysts were cited as monitoring Polymarket alongside official briefings — the platform had become a live geopolitical intelligence dashboard.",
     "RESOLVED: YES ✓","#00ff88"),
    ("FINANCE · 2024","📉","Will the Federal Reserve cut rates in September 2024?","$60M+ volume",
     "Traders pushed YES above 90% weeks before the official FOMC announcement. Bond traders and macro funds began incorporating Polymarket odds into their models. This demonstrated the path to institutional data monetisation: Polymarket as Bloomberg for probability.",
     "RESOLVED: YES ✓","#00ff88"),
    ("ENTERTAINMENT · 2024","🐦","Will Elon Musk tweet more than 200 times this week?","$1.1M+ volume",
     "Polymarket hosted 34+ markets on Musk's tweeting habits alone — and they were consistently accurate. This demonstrated an entirely new use case: prediction markets as behavioural analytics. Brands, PR firms, and hedge funds began treating this data as a live signal.",
     "ENTERTAINMENT MARKET","#ffa502"),
    ("SCIENCE · 2024","👽","Will the US government confirm alien existence?","$2.7M+ volume",
     "After Congressional UAP whistleblower hearings, users put $2.7M on this question. It held at 3–8% — far more nuanced than media hysteria would suggest. Even speculative events get priced rationally when real money is on the line.",
     "STILL OPEN","#ffa502"),
]

for i in range(0, len(trades), 2):
    cols = st.columns(2)
    for j, col in enumerate(cols):
        if i + j < len(trades):
            cat, icon, title, vol, desc, outcome, oc = trades[i+j]
            with col:
                st.markdown(f"""
                <div class="trade-card">
                  <div style="display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:8px;">
                    <div class="trade-category">{cat}</div><span style="font-size:24px;">{icon}</span>
                  </div>
                  <div class="trade-title">{title}</div>
                  <div class="trade-volume">{vol}</div>
                  <div class="trade-desc">{desc}</div>
                  <div style="margin-top:12px;"><span style="color:{oc};font-size:11px;font-weight:700;background:rgba(255,255,255,0.05);border-radius:50px;padding:5px 14px;">{outcome}</span></div>
                </div>
                """, unsafe_allow_html=True)

st.markdown("<hr class='divider'>", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# 6 · VOLUME GROWTH
# ══════════════════════════════════════════════════════════════════════════════
st.markdown('<div class="section-tag">Trading Volume</div>', unsafe_allow_html=True)
st.markdown('<div class="section-title">Explosive, Non-Cyclical Growth</div>', unsafe_allow_html=True)

quarters = ["Q1'24","Q2'24","Q3'24","Q4'24","Q1'25","Q2'25","Q3'25","Q4'25","Q1'26"]
volumes  = [0.25,   0.75,   2.0,    3.7,    0.8,    1.05,   1.25,   1.55,   1.75]

fig_vol = go.Figure()
fig_vol.add_trace(go.Bar(
    x=quarters, y=volumes,
    marker=dict(
        color=["rgba(124,58,237,0.75)"]*4 + ["rgba(0,212,255,0.75)"]*5,
        line=dict(color="rgba(255,255,255,0.07)", width=1),
    ),
    text=[f"${v}B" for v in volumes],
    textposition="outside", textfont=dict(color="white", size=11),
    hovertemplate="<b>%{x}</b><br>Volume: $%{y}B<extra></extra>",
    name="Quarterly Volume",
))
fig_vol.add_trace(go.Scatter(
    x=["Q1'25","Q2'25","Q3'25","Q4'25","Q1'26"], y=[0.8,1.05,1.25,1.55,1.75],
    mode="lines+markers",
    line=dict(color="#00ff88", width=2, dash="dot"),
    marker=dict(size=8, color="#00ff88"),
    name="Non-election baseline trend",
    hovertemplate="<b>%{x}</b> baseline: $%{y}B<extra></extra>",
))
fig_vol.add_annotation(x="Q4'24", y=3.7,
    text="<b>2024 Election<br>$3.7B single quarter</b>",
    showarrow=True, arrowhead=2, ax=-45, ay=-65,
    font=dict(color="#ffa502", size=10), arrowcolor="#ffa502",
    bgcolor="rgba(7,7,15,0.88)", bordercolor="#ffa502", borderwidth=1, borderpad=5)
fig_vol.add_annotation(x="Q1'26", y=1.75,
    text="<b>+600% vs baseline<br>Q1 2024</b>",
    showarrow=True, arrowhead=2, ax=65, ay=-45,
    font=dict(color="#00ff88", size=10), arrowcolor="#00ff88",
    bgcolor="rgba(7,7,15,0.88)", bordercolor="#00ff88", borderwidth=1, borderpad=5)
fig_vol.update_layout(
    paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
    height=390, barmode="overlay",
    legend=dict(font=dict(color="rgba(255,255,255,0.62)"), bgcolor="rgba(0,0,0,0)"),
    yaxis=dict(
        title=dict(text="Quarterly Volume (USD Billions)", font=dict(color="rgba(255,255,255,0.48)")),
        gridcolor="rgba(255,255,255,0.06)",
        tickfont=dict(color="rgba(255,255,255,0.48)"),
    ),
    xaxis=dict(tickfont=dict(color="rgba(255,255,255,0.6)", size=11)),
    margin=dict(t=30, b=28, l=58, r=68),
    font=dict(family="Inter", color="white"),
)
st.plotly_chart(fig_vol, use_container_width=True)

cv1, cv2, cv3 = st.columns(3)
for col, (num, lbl) in zip([cv1,cv2,cv3], [
    ("14x","Volume growth Q1 → Q4 2024 (election cycle)"),
    ("$1.75B","Q1 2026 — rising non-election baseline"),
    ("+600%","Non-election baseline growth vs. 2024"),
]):
    with col:
        st.markdown(f'<div class="stat-card"><div class="stat-number">{num}</div><div class="stat-label">{lbl}</div></div>', unsafe_allow_html=True)

st.markdown("<hr class='divider'>", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# 7 · BUSINESS MODEL
# ══════════════════════════════════════════════════════════════════════════════
st.markdown('<div class="section-tag">Business Model</div>', unsafe_allow_html=True)
st.markdown('<div class="section-title">How Polymarket Makes Money</div>', unsafe_allow_html=True)
st.markdown('<div class="section-sub">A marketplace model with exchange economics — revenue scales with volume, not headcount.</div>', unsafe_allow_html=True)

bm1, bm2 = st.columns([1.2, 1])
with bm1:
    for icon, name, color, share, desc in [
        ("💧","Liquidity Economics","#a78bfa","~50%","Market-making relationships and LP economics. Exchange structure shifts risk to participants rather than onto Polymarket's balance sheet — far more capital-efficient than traditional bookmakers."),
        ("📊","Data & Institutional API","#00ff88","~30%","Real-time probability feeds sold to media, hedge funds, research firms. CNN, Bloomberg, Reuters already embed Polymarket data. High-margin recurring revenue with low marginal cost."),
        ("🤝","Sponsored Markets","#ffa502","~20%","Brand and corporate partnerships for market creation. A company could pay to list a market about its product launch or earnings — turning Polymarket into a financial intelligence PR tool."),
    ]:
        st.markdown(f"""
        <div style="background:rgba(255,255,255,0.03);border:1px solid rgba(255,255,255,0.07);border-radius:12px;padding:18px;margin-bottom:10px;display:flex;gap:14px;align-items:flex-start;">
          <div style="font-size:26px;">{icon}</div>
          <div style="flex:1;">
            <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:5px;">
              <div style="font-size:15px;font-weight:700;color:{color};">{name}</div>
              <div style="font-size:18px;font-weight:800;color:{color};">{share}</div>
            </div>
            <div style="font-size:13px;color:rgba(255,255,255,0.56);line-height:1.6;">{desc}</div>
          </div>
        </div>
        """, unsafe_allow_html=True)

with bm2:
    fig_pie = go.Figure(go.Pie(
        labels=["Liquidity Economics","Data Products","Sponsored Markets"],
        values=[50,30,20],
        marker=dict(colors=["#a78bfa","#00ff88","#ffa502"],
                    line=dict(color="#07070f", width=3)),
        hole=0.55,
        textfont=dict(color="white", size=12),
        hovertemplate="<b>%{label}</b><br>%{value}%<extra></extra>",
    ))
    fig_pie.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", height=270,
        legend=dict(font=dict(color="rgba(255,255,255,0.65)", size=11), bgcolor="rgba(0,0,0,0)"),
        margin=dict(t=10, b=10, l=10, r=10),
        annotations=[dict(text="Revenue<br>Mix", x=0.5, y=0.5, font=dict(size=13, color="white"), showarrow=False)],
        font=dict(family="Inter"),
    )
    st.plotly_chart(fig_pie, use_container_width=True)

    st.markdown("""
    <div class="card" style="padding:20px;">
      <div style="font-size:13px;font-weight:700;margin-bottom:10px;">The Scalability Case</div>
      <div style="font-size:13px;color:rgba(255,255,255,0.6);line-height:1.65;">
        Traditional operators need <strong>licensing teams, balance-sheet risk, and country-specific compliance</strong> for every market they operate in.
        Polymarket's exchange model shifts risk to traders.
        Once infrastructure exists, each new event market costs <strong>near-zero marginal operating expense</strong>.
        A Fed rate decision market and a Super Bowl market run on identical infrastructure.
      </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<hr class='divider'>", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# 6 · MARKET OPPORTUNITY
# ══════════════════════════════════════════════════════════════════════════════
st.markdown('<div class="section-tag">Market Opportunity</div>', unsafe_allow_html=True)
st.markdown('<div class="section-title">A Multi-Trillion Dollar Market in Plain Sight</div>', unsafe_allow_html=True)

mo1, mo2 = st.columns([1, 1.2])
with mo1:
    for tag, size, color, desc in [
        ("TAM","~$1 Trillion+","#7c3aed","Global event trading, sports betting (~$500B globally), political forecasting, financial information markets, and institutional probability data. Every uncertain outcome on earth is a potential Polymarket contract."),
        ("SAM","~$200 Billion","#00d4ff","Crypto-native and regulated users who can legally access event contracts and are comfortable with digital wallets and USDC. Expanding rapidly as stablecoin familiarity grows globally."),
        ("SOM","~$20 Billion","#00ff88","Polymarket's realistic near-term capture — already generating $7B+ annualised volume in 2026. The ICE partnership opens the institutional data layer, which alone could represent $1B+ in recurring high-margin revenue."),
    ]:
        st.markdown(f"""
        <div style="border-left:3px solid {color};padding:14px 18px;margin-bottom:16px;background:rgba(255,255,255,0.03);border-radius:0 12px 12px 0;">
          <div style="display:flex;justify-content:space-between;margin-bottom:6px;">
            <div style="font-size:12px;font-weight:700;color:{color};letter-spacing:2px;">{tag}</div>
            <div style="font-size:20px;font-weight:800;color:{color};">{size}</div>
          </div>
          <div style="font-size:13px;color:rgba(255,255,255,0.58);line-height:1.6;">{desc}</div>
        </div>
        """, unsafe_allow_html=True)

with mo2:
    fig_sb = go.Figure(go.Sunburst(
        labels=["Total Market","TAM","SAM","SOM","Sports Betting","Political Markets","Financial Info","Crypto-native","Regulated Users","Polymarket Now"],
        parents=["","Total Market","TAM","SAM","TAM","TAM","TAM","SAM","SAM","SOM"],
        values=[1000,800,200,20,300,200,300,120,80,20],
        marker=dict(colors=["#07070f","#7c3aed","#00d4ff","#00ff88",
                             "#9f7aea","#6d4ea8","#4c3575","#00a8cc","#0088aa","#00ff88"],
                    line=dict(color="#07070f", width=2)),
        textfont=dict(color="white", size=11),
        hovertemplate="<b>%{label}</b><br>%{value}<extra></extra>",
    ))
    fig_sb.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", height=340,
        margin=dict(t=10, b=10, l=10, r=10), font=dict(family="Inter"),
    )
    st.plotly_chart(fig_sb, use_container_width=True)

st.markdown("<hr class='divider'>", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# 11 · COMPETITION
# ══════════════════════════════════════════════════════════════════════════════
st.markdown('<div class="section-tag">Competition</div>', unsafe_allow_html=True)
st.markdown('<div class="section-title">Polymarket vs. The World</div>', unsafe_allow_html=True)

cc1, cc2 = st.columns([1.1, 1])
with cc1:
    df_comp = pd.DataFrame({
        "Dimension": ["Regulatory Status","Quarterly Volume","Settlement Speed","Active Traders","Media Presence","Valuation","US Access","Growth Profile"],
        "Polymarket 🔮": ["Crypto-native (CFTC via QCEX)","$2B+/quarter","2 seconds (on-chain)","445K+ Oct 2025","CNN · FT · Reuters · BBC daily","$9B post-ICE","Re-entered 2025","Viral / exponential"],
        "Kalshi 🏛️": ["Fully CFTC-regulated","~$600M/quarter","1–3 business days (banking)","Growing, smaller","Institutional, less viral","~$1B (est.)","Always compliant","Steady / institutional"],
    })
    st.dataframe(df_comp, use_container_width=True, hide_index=True, height=320)

with cc2:
    fig_radar = go.Figure()
    cats = ["Volume","Viral Growth","Regulation","Brand Power","Tech Stack","VC Quality"]
    fig_radar.add_trace(go.Scatterpolar(
        r=[95,90,60,92,88,95,95], theta=cats+[cats[0]],
        fill="toself", fillcolor="rgba(0,212,255,0.12)",
        line=dict(color="#00d4ff", width=2), name="Polymarket",
        hovertemplate="%{theta}: %{r}<extra></extra>",
    ))
    fig_radar.add_trace(go.Scatterpolar(
        r=[30,38,95,52,72,58,30], theta=cats+[cats[0]],
        fill="toself", fillcolor="rgba(124,58,237,0.09)",
        line=dict(color="#a78bfa", width=2, dash="dash"), name="Kalshi",
        hovertemplate="%{theta}: %{r}<extra></extra>",
    ))
    fig_radar.update_layout(
        polar=dict(bgcolor="rgba(0,0,0,0)",
                   radialaxis=dict(visible=True, range=[0,100], tickfont=dict(color="rgba(255,255,255,0.3)", size=8), gridcolor="rgba(255,255,255,0.07)"),
                   angularaxis=dict(tickfont=dict(color="rgba(255,255,255,0.68)", size=11), gridcolor="rgba(255,255,255,0.07)")),
        paper_bgcolor="rgba(0,0,0,0)", height=310,
        legend=dict(font=dict(color="rgba(255,255,255,0.62)"), bgcolor="rgba(0,0,0,0)"),
        margin=dict(t=20, b=20, l=28, r=28), font=dict(family="Inter"),
    )
    st.plotly_chart(fig_radar, use_container_width=True)

st.markdown("<hr class='divider'>", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# 12 · SWOT
# ══════════════════════════════════════════════════════════════════════════════
st.markdown('<div class="section-tag">SWOT Analysis</div>', unsafe_allow_html=True)
st.markdown('<div class="section-title">Strategic Position at a Glance</div>', unsafe_allow_html=True)

sw1, sw2, sw3, sw4 = st.columns(4)
for col, name, color, bg, border, points in [
    (sw1,"Strengths","#00ff88","rgba(0,255,136,0.05)","rgba(0,255,136,0.22)",[
        "First-mover brand & liquidity moat",
        "Elite VC signal: Thiel + Vitalik + ICE",
        "Media quotes odds daily — free distribution",
    ]),
    (sw2,"Weaknesses","#ff4757","rgba(255,71,87,0.05)","rgba(255,71,87,0.22)",[
        "Revenue tied to political event cycles",
        "Regulatory overhang & FBI scrutiny",
        "KYC/AML gaps via non-custodial wallets",
    ]),
    (sw3,"Opportunities","#00d4ff","rgba(0,212,255,0.05)","rgba(0,212,255,0.22)",[
        "Institutional data API (Bloomberg-tier)",
        "Sports, macro & entertainment markets",
        "ICE partnership unlocks US institutions",
    ]),
    (sw4,"Threats","#ffa502","rgba(255,165,2,0.05)","rgba(255,165,2,0.22)",[
        "CFTC reclassifies contracts as derivatives",
        "Political markets banned by legislation",
        "Kalshi wins institutional market share",
    ]),
]:
    with col:
        pts = "".join(f"<li style='margin-bottom:8px;'>{p}</li>" for p in points)
        st.markdown(f"""
        <div style="background:{bg};border:1px solid {border};border-radius:14px;padding:20px;height:100%;">
          <div style="font-size:12px;font-weight:700;color:{color};margin-bottom:12px;letter-spacing:1px;">{name.upper()}</div>
          <ul style="font-size:13px;color:rgba(255,255,255,0.72);line-height:1.6;padding-left:16px;margin:0;">{pts}</ul>
        </div>
        """, unsafe_allow_html=True)

st.markdown("<hr class='divider'>", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# 13 · RISKS
# ══════════════════════════════════════════════════════════════════════════════
st.markdown('<div class="section-tag">Risk Analysis</div>', unsafe_allow_html=True)
st.markdown('<div class="section-title">Eyes Open: The Risk Stack</div>', unsafe_allow_html=True)

for i in range(0, 6, 2):
    risk_pairs = [
        ("HIGH","risk-high","CFTC Regulatory Risk","2022 CFTC fine of $1.4M for offering unregistered event-based binary options. The legal question — derivatives or information products? — changes everything. QCEX acquisition mitigates but does not eliminate this risk. CFTC classification remains the single biggest binary outcome for the business."),
        ("HIGH","risk-high","Political & FBI Scrutiny","FBI searched Shayne Coplan's home post-2024 election. No charges were filed and the company described it as politically motivated. However, law-enforcement attention increases cost of capital, complicates bank partnerships, and makes institutional co-investors cautious about governance exposure."),
        ("MED","risk-med","Revenue Cyclicality","Q4 2024 volume was 4× adjacent quarters due to the US election. If the non-election baseline does not keep rising, revenue visibility weakens and the $9B entry valuation may look expensive on a through-cycle basis."),
        ("MED","risk-med","Crypto Compliance Complexity","USDC settlement and non-custodial wallet access create real KYC/AML challenges. Regulators scrutinise whether VPN access circumvents geofencing. Technical crypto compliance at institutional scale requires sustained legal and engineering investment."),
        ("LOW","risk-low","Kalshi Competition","Kalshi has full CFTC approval and is growing institutional traction. However, Polymarket leads on volume (10×), brand, and viral distribution — advantages that require years and hundreds of millions to replicate."),
        ("LOW","risk-low","Exit Uncertainty","A public market exit requires audited revenues and regulatory clarity. But ICE — already an investor — is the most natural acquirer. The strategic acquisition path is clear and reduces exit risk materially."),
    ]
    c1r, c2r = st.columns(2)
    for col, (lvl, cls, title, desc) in zip([c1r,c2r], risk_pairs[i:i+2]):
        with col:
            st.markdown(f"""
            <div class="card" style="padding:20px;margin-bottom:12px;">
              <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:9px;">
                <div style="font-size:15px;font-weight:700;">{title}</div>
                <span class="risk-pill {cls}">{lvl}</span>
              </div>
              <div style="font-size:13px;color:rgba(255,255,255,0.6);line-height:1.65;">{desc}</div>
            </div>
            """, unsafe_allow_html=True)

st.markdown("<hr class='divider'>", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# 14 · INVESTMENT THESIS
# ══════════════════════════════════════════════════════════════════════════════
st.markdown('<div class="section-tag">Investment Thesis</div>', unsafe_allow_html=True)
st.markdown('<div class="section-title">Our Verdict</div>', unsafe_allow_html=True)

st.markdown("""
<div class="reco-box">
  <div class="reco-verdict">CONDITIONAL INVEST</div>
  <div style="font-size:19px;color:rgba(255,255,255,0.72);max-width:800px;margin:0 auto 32px;line-height:1.65;">
    Polymarket is the most compelling fintech infrastructure bet of 2026.
    The condition: regulatory clarity is the unlock.
    If it comes — the upside is asymmetric.
    If it doesn't — the downside is existential. Price that binary accordingly.
  </div>
</div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)
cb, cbe = st.columns(2)
for col, clr, cls_color, heading, items in [
    (cb,"rgba(0,255,136,0.28)","#00ff88","BULL CASE — Why Invest Now",[
        "First-mover with unassailable brand and liquidity moat",
        "NYSE parent ICE validates institutional exit at $9B+",
        "Non-election baseline growing 600% — habitual use emerging",
        "Founders Fund + Vitalik = strongest crypto-fintech signal possible",
        "CNN, BBC, Reuters quote odds daily — organic free distribution",
        "Re-entered US via QCEX — regulatory overhang materially reduced",
        "Data API business = high-margin recurring revenue layer",
    ]),
    (cbe,"rgba(255,71,87,0.28)","#ff4757","BEAR CASE — When Not to Invest",[
        "CFTC reclassifies all contracts as unregistered derivatives",
        "Political markets banned — primary volume driver eliminated",
        "FBI investigation escalates into founder charges",
        "Non-election baseline stagnates — revenue remains cyclical",
        "Kalshi captures institutional market; Polymarket stays niche",
        "$9B entry valuation leaves insufficient upside for new investors",
        "Regulatory backlash prevents any institutional acquirer from engaging",
    ]),
]:
    with col:
        items_html = "".join(f'<div style="display:flex;gap:9px;margin-bottom:10px;font-size:14px;"><span style="color:{cls_color};font-weight:700;">{"✓" if cls_color=="#00ff88" else "✗"}</span><span>{it}</span></div>' for it in items)
        st.markdown(f"""
        <div class="card" style="border-color:{clr};background:rgba(255,255,255,0.02);">
          <div style="color:{cls_color};font-size:11px;font-weight:700;letter-spacing:2px;text-transform:uppercase;margin-bottom:14px;">{heading}</div>
          {items_html}
        </div>
        """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)
st.markdown("""
<div style="background:rgba(255,255,255,0.03);border:1px solid rgba(255,255,255,0.08);border-radius:16px;padding:26px;">
  <div style="font-size:15px;font-weight:700;margin-bottom:14px;">Recommended Investment Structure</div>
  <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(190px,1fr));gap:12px;">
    <div style="background:rgba(0,212,255,0.06);border:1px solid rgba(0,212,255,0.18);border-radius:11px;padding:14px;">
      <div style="color:#00d4ff;font-weight:700;font-size:13px;margin-bottom:5px;">Staged Financing</div>
      <div style="font-size:12px;color:rgba(255,255,255,0.52);">Milestone-based capital tied to regulatory progress</div>
    </div>
    <div style="background:rgba(124,58,237,0.06);border:1px solid rgba(124,58,237,0.18);border-radius:11px;padding:14px;">
      <div style="color:#a78bfa;font-weight:700;font-size:13px;margin-bottom:5px;">Governance Rights</div>
      <div style="font-size:12px;color:rgba(255,255,255,0.52);">Board seat + compliance reporting + information rights</div>
    </div>
    <div style="background:rgba(0,255,136,0.06);border:1px solid rgba(0,255,136,0.18);border-radius:11px;padding:14px;">
      <div style="color:#00ff88;font-weight:700;font-size:13px;margin-bottom:5px;">US Access Plan</div>
      <div style="font-size:12px;color:rgba(255,255,255,0.52);">Credible path: registration, partnership, or spinout</div>
    </div>
    <div style="background:rgba(255,165,2,0.06);border:1px solid rgba(255,165,2,0.18);border-radius:11px;padding:14px;">
      <div style="color:#ffa502;font-weight:700;font-size:13px;margin-bottom:5px;">Category Diversification</div>
      <div style="font-size:12px;color:rgba(255,255,255,0.52);">Demonstrate non-political markets retain users between cycles</div>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

st.markdown("<hr class='divider'>", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# 15 · LIVE MARKETS
# ══════════════════════════════════════════════════════════════════════════════
st.markdown('<div class="section-tag">Live Data</div>', unsafe_allow_html=True)
st.markdown('<div class="section-title">Polymarket — Right Now</div>', unsafe_allow_html=True)
st.markdown('<div class="section-sub">Live markets pulled directly from the Polymarket Gamma API · public · no authentication required</div>', unsafe_allow_html=True)

@st.cache_data(ttl=120)
def fetch_live_markets():
    try:
        r = requests.get(
            "https://gamma-api.polymarket.com/markets?active=true&closed=false&limit=10&order=volume&ascending=false",
            timeout=8,
        )
        r.raise_for_status()
        return r.json(), None
    except Exception as e:
        return None, str(e)

with st.spinner("Fetching live markets from Polymarket..."):
    markets, err = fetch_live_markets()

if markets:
    st.markdown(f"""
    <div style="display:flex;align-items:center;gap:10px;margin-bottom:20px;">
      <span class="live-dot"></span>
      <span style="color:#00ff88;font-size:13px;font-weight:600;">{len(markets)} markets loaded · {datetime.now().strftime('%H:%M:%S')}</span>
    </div>
    """, unsafe_allow_html=True)
    for m in markets[:8]:
        title = m.get("question") or m.get("title", "Unknown")
        volume = m.get("volume", 0)
        prices = m.get("outcomePrices", [])
        try:
            vol_fmt = f"${float(volume):,.0f}"
        except Exception:
            vol_fmt = "N/A"
        yes_prob = 50
        try:
            if prices:
                yes_prob = round(float(prices[0]) * 100, 1)
        except Exception:
            pass
        st.markdown(f"""
        <div class="live-card">
          <div style="flex:1;min-width:0;margin-right:18px;">
            <div style="font-size:13px;font-weight:600;margin-bottom:7px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;">
              <span class="live-dot"></span>{title[:95]}{"…" if len(title)>95 else ""}
            </div>
            <div class="probability-bar"><div class="probability-fill" style="width:{yes_prob}%;"></div></div>
            <div style="display:flex;justify-content:space-between;margin-top:5px;">
              <span style="font-size:11px;color:rgba(255,255,255,0.38);">YES probability</span>
              <span style="font-size:11px;color:#00d4ff;font-weight:700;">{yes_prob}%</span>
            </div>
          </div>
          <div style="text-align:right;flex-shrink:0;">
            <div style="font-size:16px;font-weight:700;color:#00ff88;">{vol_fmt}</div>
            <div style="font-size:10px;color:rgba(255,255,255,0.32);">volume</div>
          </div>
        </div>
        """, unsafe_allow_html=True)
    if st.button("Refresh live data"):
        st.cache_data.clear()
        st.rerun()
else:
    st.markdown('<div class="info-box"><strong>API temporarily unavailable</strong> — sample data shown.</div>', unsafe_allow_html=True)
    for title, prob in [
        ("Will Bitcoin reach $150,000 in 2026?", 48),
        ("Will the Fed cut rates before September 2026?", 61),
        ("Will there be a US recession in 2026?", 33),
        ("Will Trump sign the crypto bill in 2026?", 71),
    ]:
        st.markdown(f"""
        <div class="live-card" style="opacity:0.7;">
          <div style="flex:1;min-width:0;margin-right:18px;">
            <div style="font-size:13px;font-weight:600;margin-bottom:7px;">⚡ {title}</div>
            <div class="probability-bar"><div class="probability-fill" style="width:{prob}%;"></div></div>
            <div style="display:flex;justify-content:space-between;margin-top:5px;">
              <span style="font-size:11px;color:rgba(255,255,255,0.38);">YES probability (sample)</span>
              <span style="font-size:11px;color:#00d4ff;font-weight:700;">{prob}%</span>
            </div>
          </div>
        </div>
        """, unsafe_allow_html=True)

# ── Footer ─────────────────────────────────────────────────────────────────────
st.markdown("<hr class='divider'>", unsafe_allow_html=True)
st.markdown("""
<div style="text-align:center;padding:32px 0;color:rgba(255,255,255,0.28);font-size:12px;">
  <div style="font-size:26px;margin-bottom:10px;">🔮</div>
  <div style="font-size:16px;font-weight:700;color:rgba(255,255,255,0.52);margin-bottom:8px;">Polymarket — The World's Largest Prediction Market</div>
  <div style="margin-bottom:8px;">
    <strong>Leon Ye</strong> (1616910) &amp; <strong>Ilyos Umurzakov</strong> (1615067)
    &nbsp;·&nbsp; Supervisor: Prof. James Slawney
    &nbsp;·&nbsp; Frankfurt University of Applied Sciences &nbsp;·&nbsp; Summer Semester 2026
  </div>
  <div>Sources: CoinDesk · Axios · Fortune · Bloomberg · ICE · CFTC · Poly Syncer · Dune Analytics · Wikipedia · S&amp;P Global · KPMG</div>
</div>
""", unsafe_allow_html=True)
