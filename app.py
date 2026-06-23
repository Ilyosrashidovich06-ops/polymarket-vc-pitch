import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import requests
from datetime import datetime

st.set_page_config(
    page_title="Polymarket — VC Pitch 2026",
    page_icon="🔮",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Custom CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');

* { font-family: 'Inter', sans-serif; }

html, body, [data-testid="stAppViewContainer"] {
    background-color: #07070f;
    color: #ffffff;
}
[data-testid="stHeader"] { background: rgba(7,7,15,0.95); }
[data-testid="stSidebar"] { background: #0d0d1a; }

/* Remove default padding */
.block-container { padding: 0 2rem 4rem 2rem; max-width: 1400px; margin: auto; }

/* Hero */
.hero {
    background: linear-gradient(135deg, #0d0d2b 0%, #1a0533 50%, #001a3d 100%);
    border: 1px solid rgba(0,212,255,0.15);
    border-radius: 24px;
    padding: 80px 60px;
    margin: 30px 0;
    position: relative;
    overflow: hidden;
    text-align: center;
}
.hero::before {
    content: '';
    position: absolute; inset: 0;
    background: radial-gradient(ellipse at 30% 50%, rgba(124,58,237,0.2) 0%, transparent 60%),
                radial-gradient(ellipse at 70% 50%, rgba(0,212,255,0.15) 0%, transparent 60%);
}
.hero-badge {
    display: inline-block;
    background: rgba(0,212,255,0.1);
    border: 1px solid rgba(0,212,255,0.4);
    border-radius: 50px;
    padding: 6px 20px;
    font-size: 13px;
    font-weight: 600;
    color: #00d4ff;
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-bottom: 24px;
}
.hero h1 {
    font-size: clamp(42px, 6vw, 80px);
    font-weight: 900;
    line-height: 1.05;
    margin: 0 0 20px;
    background: linear-gradient(135deg, #ffffff 0%, #00d4ff 50%, #7c3aed 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}
.hero-sub {
    font-size: 22px;
    color: rgba(255,255,255,0.7);
    max-width: 700px;
    margin: 0 auto 40px;
    font-weight: 400;
    line-height: 1.5;
}

/* Stats row */
.stat-card {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 16px;
    padding: 28px 24px;
    text-align: center;
    transition: all 0.3s;
}
.stat-card:hover {
    border-color: rgba(0,212,255,0.4);
    background: rgba(0,212,255,0.06);
    transform: translateY(-4px);
}
.stat-number { font-size: 42px; font-weight: 800; color: #00d4ff; line-height: 1; }
.stat-label { font-size: 14px; color: rgba(255,255,255,0.55); margin-top: 8px; font-weight: 500; }

/* Section headers */
.section-tag {
    display: inline-block;
    background: rgba(124,58,237,0.15);
    border: 1px solid rgba(124,58,237,0.4);
    border-radius: 50px;
    padding: 4px 16px;
    font-size: 12px;
    font-weight: 700;
    color: #a78bfa;
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-bottom: 12px;
}
.section-title {
    font-size: clamp(28px, 4vw, 48px);
    font-weight: 800;
    line-height: 1.1;
    margin: 0 0 8px;
}
.section-sub { font-size: 18px; color: rgba(255,255,255,0.55); margin-bottom: 40px; }

/* Cards */
.card {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 20px;
    padding: 32px;
    height: 100%;
    transition: all 0.3s;
}
.card:hover {
    border-color: rgba(0,212,255,0.3);
    background: rgba(0,212,255,0.04);
}

/* Trade cards */
.trade-card {
    background: linear-gradient(135deg, rgba(0,212,255,0.05), rgba(124,58,237,0.05));
    border: 1px solid rgba(0,212,255,0.2);
    border-radius: 20px;
    padding: 28px;
    margin-bottom: 16px;
    position: relative;
    overflow: hidden;
}
.trade-card::before {
    content: '';
    position: absolute;
    left: 0; top: 0; bottom: 0;
    width: 4px;
    background: linear-gradient(180deg, #00d4ff, #7c3aed);
    border-radius: 4px 0 0 4px;
}
.trade-category {
    font-size: 11px;
    font-weight: 700;
    color: #00d4ff;
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-bottom: 8px;
}
.trade-title { font-size: 20px; font-weight: 700; margin-bottom: 12px; }
.trade-volume { font-size: 28px; font-weight: 800; color: #00ff88; }
.trade-desc { font-size: 14px; color: rgba(255,255,255,0.6); line-height: 1.6; margin-top: 12px; }

/* Founder card */
.founder-card {
    background: linear-gradient(135deg, #0d0d2b, #1a0533);
    border: 1px solid rgba(124,58,237,0.3);
    border-radius: 24px;
    padding: 40px;
    display: flex;
    align-items: center;
    gap: 40px;
}
.founder-name { font-size: 36px; font-weight: 800; margin-bottom: 8px; }
.founder-title { color: #00d4ff; font-size: 16px; font-weight: 600; margin-bottom: 20px; }
.founder-bio { font-size: 16px; color: rgba(255,255,255,0.7); line-height: 1.7; }

/* Investor cards */
.investor-card {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.1);
    border-radius: 16px;
    padding: 24px;
    text-align: center;
    transition: all 0.3s;
}
.investor-card:hover {
    border-color: rgba(0,212,255,0.4);
    transform: translateY(-4px);
}
.investor-name { font-size: 18px; font-weight: 700; margin-bottom: 6px; }
.investor-role { font-size: 13px; color: rgba(255,255,255,0.5); margin-bottom: 12px; }
.investor-signal {
    font-size: 13px;
    color: #00d4ff;
    background: rgba(0,212,255,0.1);
    border-radius: 8px;
    padding: 8px 12px;
    line-height: 1.5;
}

/* Timeline */
.timeline-item {
    display: flex;
    gap: 24px;
    margin-bottom: 32px;
    align-items: flex-start;
}
.timeline-dot {
    width: 48px;
    height: 48px;
    border-radius: 50%;
    background: linear-gradient(135deg, #00d4ff, #7c3aed);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 18px;
    flex-shrink: 0;
    font-weight: 800;
}
.timeline-content { flex: 1; padding-top: 8px; }
.timeline-year { font-size: 12px; color: #00d4ff; font-weight: 700; letter-spacing: 2px; }
.timeline-title { font-size: 20px; font-weight: 700; margin: 4px 0; }
.timeline-desc { font-size: 14px; color: rgba(255,255,255,0.6); }

/* Risk pill */
.risk-high { color: #ff4757; background: rgba(255,71,87,0.1); border: 1px solid rgba(255,71,87,0.3); }
.risk-med { color: #ffa502; background: rgba(255,165,2,0.1); border: 1px solid rgba(255,165,2,0.3); }
.risk-low { color: #00ff88; background: rgba(0,255,136,0.1); border: 1px solid rgba(0,255,136,0.3); }
.risk-pill {
    display: inline-block;
    border-radius: 50px;
    padding: 4px 14px;
    font-size: 12px;
    font-weight: 700;
    letter-spacing: 1px;
    text-transform: uppercase;
}

/* Recommendation box */
.reco-box {
    background: linear-gradient(135deg, rgba(0,255,136,0.05), rgba(0,212,255,0.05));
    border: 2px solid rgba(0,255,136,0.3);
    border-radius: 24px;
    padding: 48px;
    text-align: center;
}
.reco-verdict {
    font-size: 52px;
    font-weight: 900;
    background: linear-gradient(135deg, #00ff88, #00d4ff);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 16px;
}

/* Live market card */
.live-card {
    background: rgba(0,255,136,0.04);
    border: 1px solid rgba(0,255,136,0.2);
    border-radius: 16px;
    padding: 20px;
    margin-bottom: 12px;
    display: flex;
    justify-content: space-between;
    align-items: center;
}
.live-dot {
    display: inline-block;
    width: 8px; height: 8px;
    border-radius: 50%;
    background: #00ff88;
    margin-right: 8px;
    animation: pulse 2s infinite;
}
@keyframes pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.3; }
}
.probability-bar {
    height: 8px;
    border-radius: 4px;
    background: rgba(255,255,255,0.1);
    margin-top: 8px;
    overflow: hidden;
}
.probability-fill {
    height: 100%;
    border-radius: 4px;
    background: linear-gradient(90deg, #7c3aed, #00d4ff);
}

/* Nav tabs */
.nav-container {
    position: sticky;
    top: 0;
    z-index: 100;
    background: rgba(7,7,15,0.95);
    backdrop-filter: blur(20px);
    border-bottom: 1px solid rgba(255,255,255,0.06);
    padding: 12px 0;
    margin-bottom: 40px;
}

/* Divider */
.divider { border: none; border-top: 1px solid rgba(255,255,255,0.06); margin: 60px 0; }
</style>
""", unsafe_allow_html=True)


# ── Sidebar navigation ─────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### Navigation")
    sections = [
        "🏠 Home", "🧠 What is Polymarket?", "🧑‍💻 The Founder",
        "🔥 Iconic Trades", "📈 Trading Volume", "💰 Funding History",
        "🤝 Investors", "🌍 Market Opportunity", "⚔️ Competition",
        "⚠️ Risks", "✅ Investment Thesis", "📡 Live Markets"
    ]
    selected = st.radio("Go to", sections, label_visibility="collapsed")
    st.markdown("---")
    st.markdown("**Prepared by**")
    st.markdown("Leon Ye · Ilyos Umurzakov")
    st.markdown("Frankfurt UAS · June 2026")
    st.markdown("*English for Presentations*")


# ══════════════════════════════════════════════════════════════════════════════
# 1. HERO
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<div class="hero">
  <div class="hero-badge">VC Pitch Deck · 2026</div>
  <h1>The World Bets on<br>Everything — Invest in<br>the Exchange</h1>
  <p class="hero-sub">
    Polymarket is turning human uncertainty into a tradeable asset class.
    $9 billion valuation. NYSE-backed. The most accurate forecasting tool on earth.
  </p>
  <div style="display:flex; gap:12px; justify-content:center; flex-wrap:wrap;">
    <span style="background:rgba(0,212,255,0.12);border:1px solid rgba(0,212,255,0.3);border-radius:50px;padding:10px 24px;font-size:14px;font-weight:600;color:#00d4ff;">
      🔮 Blockchain-Native
    </span>
    <span style="background:rgba(124,58,237,0.12);border:1px solid rgba(124,58,237,0.3);border-radius:50px;padding:10px 24px;font-size:14px;font-weight:600;color:#a78bfa;">
      📊 $9B Valuation
    </span>
    <span style="background:rgba(0,255,136,0.12);border:1px solid rgba(0,255,136,0.3);border-radius:50px;padding:10px 24px;font-size:14px;font-weight:600;color:#00ff88;">
      ✅ NYSE Investor
    </span>
  </div>
</div>
""", unsafe_allow_html=True)

# ── Key stats ──────────────────────────────────────────────────────────────────
c1, c2, c3, c4, c5 = st.columns(5)
stats = [
    ("$9B", "Post-ICE Valuation"),
    ("$3.7B+", "2024 Election Volume"),
    ("445K+", "Active Traders (Oct 2025)"),
    ("$74M+", "Total VC Raised"),
    ("#1", "Global Prediction Market"),
]
for col, (num, label) in zip([c1, c2, c3, c4, c5], stats):
    with col:
        st.markdown(f"""
        <div class="stat-card">
          <div class="stat-number">{num}</div>
          <div class="stat-label">{label}</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("<hr class='divider'>", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# 2. WHAT IS POLYMARKET?
# ══════════════════════════════════════════════════════════════════════════════
st.markdown('<div class="section-tag">What Is Polymarket?</div>', unsafe_allow_html=True)
st.markdown('<div class="section-title">Probability, Priced in Real Time</div>', unsafe_allow_html=True)
st.markdown('<div class="section-sub">A blockchain-powered prediction market where contracts track real-world outcomes — and prices reveal what the crowd <em>actually</em> believes.</div>', unsafe_allow_html=True)

col_l, col_r = st.columns([1.1, 1])
with col_l:
    st.markdown("""
    <div class="card">
      <h3 style="font-size:24px;font-weight:700;margin-bottom:20px;">How It Works</h3>
      <div style="display:flex;gap:16px;align-items:flex-start;margin-bottom:24px;">
        <div style="width:40px;height:40px;border-radius:12px;background:rgba(0,212,255,0.15);display:flex;align-items:center;justify-content:center;font-size:20px;flex-shrink:0;">❓</div>
        <div>
          <div style="font-weight:600;margin-bottom:4px;">A question gets listed</div>
          <div style="color:rgba(255,255,255,0.6);font-size:14px;">"Will Trump win the 2024 election?" — YES or NO contracts go live.</div>
        </div>
      </div>
      <div style="display:flex;gap:16px;align-items:flex-start;margin-bottom:24px;">
        <div style="width:40px;height:40px;border-radius:12px;background:rgba(124,58,237,0.15);display:flex;align-items:center;justify-content:center;font-size:20px;flex-shrink:0;">💱</div>
        <div>
          <div style="font-weight:600;margin-bottom:4px;">Traders buy and sell with USDC</div>
          <div style="color:rgba(255,255,255,0.6);font-size:14px;">A contract at $0.72 = 72% market-implied probability. Settled on-chain via Polygon.</div>
        </div>
      </div>
      <div style="display:flex;gap:16px;align-items:flex-start;margin-bottom:24px;">
        <div style="width:40px;height:40px;border-radius:12px;background:rgba(0,255,136,0.15);display:flex;align-items:center;justify-content:center;font-size:20px;flex-shrink:0;">✅</div>
        <div>
          <div style="font-weight:600;margin-bottom:4px;">Event resolves</div>
          <div style="color:rgba(255,255,255,0.6);font-size:14px;">Winners get $1 per contract. Losers get $0. Instant, transparent, tamper-proof.</div>
        </div>
      </div>
      <div style="display:flex;gap:16px;align-items:flex-start;">
        <div style="width:40px;height:40px;border-radius:12px;background:rgba(255,165,2,0.15);display:flex;align-items:center;justify-content:center;font-size:20px;flex-shrink:0;">📡</div>
        <div>
          <div style="font-weight:600;margin-bottom:4px;">Prices become information</div>
          <div style="color:rgba(255,255,255,0.6);font-size:14px;">CNN, Reuters, and the FT quote Polymarket odds. It's not gambling — it's a forecasting layer for the internet.</div>
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)

with col_r:
    # Simple animated gauge chart showing an example market
    fig_gauge = go.Figure(go.Indicator(
        mode="gauge+number",
        value=72,
        title={"text": "Trump wins 2024 election?<br><span style='font-size:14px;color:#aaa'>Polymarket peaked at 72%</span>",
               "font": {"color": "white", "size": 16}},
        number={"suffix": "% YES", "font": {"color": "#00d4ff", "size": 40}},
        gauge={
            "axis": {"range": [0, 100], "tickcolor": "rgba(255,255,255,0.3)"},
            "bar": {"color": "#00d4ff", "thickness": 0.3},
            "bgcolor": "rgba(255,255,255,0.05)",
            "borderwidth": 0,
            "threshold": {"line": {"color": "#00ff88", "width": 3}, "value": 72},
            "steps": [
                {"range": [0, 50], "color": "rgba(255,71,87,0.15)"},
                {"range": [50, 100], "color": "rgba(0,212,255,0.1)"},
            ],
        },
    ))
    fig_gauge.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        height=300,
        font={"color": "white"},
        margin=dict(t=60, b=20, l=20, r=20),
    )
    st.plotly_chart(fig_gauge, use_container_width=True)

    st.markdown("""
    <div style="background:rgba(0,255,136,0.06);border:1px solid rgba(0,255,136,0.2);border-radius:16px;padding:20px;margin-top:-10px;">
      <div style="font-size:13px;color:#00ff88;font-weight:700;letter-spacing:1px;text-transform:uppercase;margin-bottom:8px;">Why this matters</div>
      <div style="font-size:15px;color:rgba(255,255,255,0.8);line-height:1.6;">
        Polymarket's 72% odds on Trump <strong>outpaced every major poll</strong>
        showing a 50/50 race. Crowds with skin in the game are smarter than pundits.
      </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<hr class='divider'>", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# 3. FOUNDER
# ══════════════════════════════════════════════════════════════════════════════
st.markdown('<div class="section-tag">The Founder</div>', unsafe_allow_html=True)
st.markdown('<div class="section-title">Shayne Coplan — Built a Billion by 27</div>', unsafe_allow_html=True)

col_f1, col_f2 = st.columns([1, 2])
with col_f1:
    st.image(
        "https://upload.wikimedia.org/wikipedia/commons/thumb/2/26/Shayne_Coplan_2024.jpg/440px-Shayne_Coplan_2024.jpg",
        caption="Shayne Coplan, CEO & Founder",
        use_container_width=True,
    )
with col_f2:
    st.markdown("""
    <div class="card" style="height:auto;">
      <div style="display:flex;gap:16px;margin-bottom:24px;flex-wrap:wrap;">
        <div style="background:rgba(0,212,255,0.1);border:1px solid rgba(0,212,255,0.3);border-radius:12px;padding:12px 20px;text-align:center;">
          <div style="font-size:28px;font-weight:800;color:#00d4ff;">27</div>
          <div style="font-size:12px;color:rgba(255,255,255,0.5);">Years Old</div>
        </div>
        <div style="background:rgba(124,58,237,0.1);border:1px solid rgba(124,58,237,0.3);border-radius:12px;padding:12px 20px;text-align:center;">
          <div style="font-size:28px;font-weight:800;color:#a78bfa;">$1B+</div>
          <div style="font-size:12px;color:rgba(255,255,255,0.5);">Net Worth</div>
        </div>
        <div style="background:rgba(0,255,136,0.1);border:1px solid rgba(0,255,136,0.3);border-radius:12px;padding:12px 20px;text-align:center;">
          <div style="font-size:28px;font-weight:800;color:#00ff88;">2020</div>
          <div style="font-size:12px;color:rgba(255,255,255,0.5);">Founded</div>
        </div>
        <div style="background:rgba(255,165,2,0.1);border:1px solid rgba(255,165,2,0.3);border-radius:12px;padding:12px 20px;text-align:center;">
          <div style="font-size:28px;font-weight:800;color:#ffa502;">#1</div>
          <div style="font-size:12px;color:rgba(255,255,255,0.5);">Youngest Self-Made Billionaire (Bloomberg 2025)</div>
        </div>
      </div>

      <div style="display:grid;gap:16px;">
        <div style="display:flex;gap:14px;align-items:flex-start;">
          <span style="font-size:20px;">🏙️</span>
          <div>
            <strong>New York-born crypto native</strong>
            <div style="color:rgba(255,255,255,0.6);font-size:14px;margin-top:2px;">
              Raised on the Upper West Side, Manhattan. Bought Ethereum in 2014 at <strong>$0.30/ETH</strong> as a teenager.
            </div>
          </div>
        </div>
        <div style="display:flex;gap:14px;align-items:flex-start;">
          <span style="font-size:20px;">🎓</span>
          <div>
            <strong>NYU Dropout → Founder</strong>
            <div style="color:rgba(255,255,255,0.6);font-size:14px;margin-top:2px;">
              Left NYU Computer Science in his freshman year. Built Polymarket <em>alone</em> from his Lower East Side apartment.
            </div>
          </div>
        </div>
        <div style="display:flex;gap:14px;align-items:flex-start;">
          <span style="font-size:20px;">🔮</span>
          <div>
            <strong>Vision: Markets as Truth Machines</strong>
            <div style="color:rgba(255,255,255,0.6);font-size:14px;margin-top:2px;">
              Coplan believes prediction markets are the most honest form of information aggregation ever invented — and built the infrastructure to prove it.
            </div>
          </div>
        </div>
        <div style="display:flex;gap:14px;align-items:flex-start;">
          <span style="font-size:20px;">⚡</span>
          <div>
            <strong>World's Youngest Self-Made Billionaire (Oct 2025)</strong>
            <div style="color:rgba(255,255,255,0.6);font-size:14px;margin-top:2px;">
              After ICE's $2B investment, Bloomberg named him the youngest self-made billionaire on earth. Forbes estimates $1B+ net worth.
            </div>
          </div>
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<hr class='divider'>", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# 4. ICONIC TRADES
# ══════════════════════════════════════════════════════════════════════════════
st.markdown('<div class="section-tag">Iconic Trades</div>', unsafe_allow_html=True)
st.markdown('<div class="section-title">Where Polymarket Made History</div>', unsafe_allow_html=True)
st.markdown('<div class="section-sub">These weren\'t just bets. They were the most accurate real-time intelligence on earth.</div>', unsafe_allow_html=True)

trades = [
    {
        "category": "POLITICS · 2024",
        "title": "Will Trump win the 2024 U.S. Presidential Election?",
        "volume": "$3.7B+ in bets",
        "icon": "🗳️",
        "color": "#00d4ff",
        "desc": "Polymarket showed Trump at 65–72% in early October — while every major poll said 50/50. The market called it weeks before election night. This single market made Polymarket a household name and was quoted by CNN, Bloomberg, and the FT.",
        "outcome": "RESOLVED: YES ✓",
        "outcome_color": "#00ff88",
    },
    {
        "category": "CRYPTO · 2024",
        "title": "Will Bitcoin hit $100,000 before end of 2024?",
        "volume": "$250M+ volume",
        "icon": "₿",
        "color": "#f7931a",
        "desc": "With Bitcoin trading around $60K in October, Polymarket climbed to 45% YES. BTC hit $100K in December 2024. Traders who bought YES at $0.30 made 3x returns. A single Bitcoin price market attracted more volume than many hedge funds manage.",
        "outcome": "RESOLVED: YES ✓",
        "outcome_color": "#00ff88",
    },
    {
        "category": "GEOPOLITICS · 2024",
        "title": "Will there be a Gaza ceasefire deal before 2025?",
        "volume": "$45M+ volume",
        "icon": "🕊️",
        "color": "#a78bfa",
        "desc": "Markets fluctuated from 20% to 80% in real time as negotiations unfolded across Qatar, Egypt and the US. Diplomats and analysts were cited as watching Polymarket odds alongside official briefings — illustrating how these markets become a live intelligence feed.",
        "outcome": "RESOLVED: YES ✓",
        "outcome_color": "#00ff88",
    },
    {
        "category": "ENTERTAINMENT · 2024",
        "title": "Will Elon Musk tweet more than 200 times this week?",
        "volume": "$1.1M+ volume",
        "icon": "🐦",
        "color": "#1da1f2",
        "desc": "Polymarket hosted 34+ markets on Musk's tweeting habits. The weirdest part? These markets were shockingly accurate. They exposed a new use case: prediction markets as behavioral analytics tools. Brands, hedge funds, and journalists started subscribing to this data.",
        "outcome": "ENTERTAINMENT MARKET",
        "outcome_color": "#ffa502",
    },
    {
        "category": "SCIENCE · 2024",
        "title": "Will the US government confirm alien existence?",
        "volume": "$2.7M+ volume",
        "icon": "👽",
        "color": "#00ff88",
        "desc": "After Congressional hearings featuring UAP whistleblowers, Polymarket users put $2.7M on 'will the US confirm alien existence?' The market hovered at 3–8% — a more nuanced read than media hysteria suggested. Even fringe topics get priced rationally with money on the line.",
        "outcome": "STILL OPEN",
        "outcome_color": "#ffa502",
    },
]

for i in range(0, len(trades), 2):
    cols = st.columns(2)
    for j, col in enumerate(cols):
        if i + j < len(trades):
            t = trades[i + j]
            with col:
                st.markdown(f"""
                <div class="trade-card">
                  <div style="display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:12px;">
                    <div class="trade-category">{t['category']}</div>
                    <span style="font-size:28px;">{t['icon']}</span>
                  </div>
                  <div class="trade-title">{t['title']}</div>
                  <div class="trade-volume">{t['volume']}</div>
                  <div class="trade-desc">{t['desc']}</div>
                  <div style="margin-top:16px;">
                    <span style="color:{t['outcome_color']};font-size:13px;font-weight:700;
                      background:rgba(255,255,255,0.06);border-radius:50px;padding:6px 14px;">
                      {t['outcome']}
                    </span>
                  </div>
                </div>
                """, unsafe_allow_html=True)

st.markdown("<hr class='divider'>", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# 5. TRADING VOLUME
# ══════════════════════════════════════════════════════════════════════════════
st.markdown('<div class="section-tag">Trading Volume</div>', unsafe_allow_html=True)
st.markdown('<div class="section-title">Explosive, Non-Cyclical Growth</div>', unsafe_allow_html=True)

quarters = ["Q1'24", "Q2'24", "Q3'24", "Q4'24", "Q1'25", "Q2'25", "Q3'25", "Q4'25", "Q1'26"]
volumes = [0.25, 0.75, 2.0, 3.7, 0.8, 1.05, 1.25, 1.55, 1.75]
colors = ["#7c3aed"] * 4 + ["#00d4ff"] * 5

fig_vol = go.Figure()
fig_vol.add_trace(go.Bar(
    x=quarters,
    y=volumes,
    marker=dict(
        color=colors,
        line=dict(color="rgba(255,255,255,0.1)", width=1),
        cornerradius=8,
    ),
    text=[f"${v}B" for v in volumes],
    textposition="outside",
    textfont=dict(color="white", size=13, family="Inter"),
    hovertemplate="<b>%{x}</b><br>Volume: $%{y}B<extra></extra>",
))
fig_vol.add_annotation(
    x="Q4'24", y=3.7,
    text="<b>2024 Election Peak<br>$3.7B in single quarter</b>",
    showarrow=True, arrowhead=2,
    ax=-60, ay=-80,
    font=dict(color="#ffa502", size=12),
    arrowcolor="#ffa502",
    bgcolor="rgba(7,7,15,0.8)",
    bordercolor="#ffa502",
    borderwidth=1,
    borderpad=6,
)
fig_vol.add_annotation(
    x="Q1'26", y=1.75,
    text="<b>Higher non-election<br>baseline = habitual use</b>",
    showarrow=True, arrowhead=2,
    ax=80, ay=-60,
    font=dict(color="#00ff88", size=12),
    arrowcolor="#00ff88",
    bgcolor="rgba(7,7,15,0.8)",
    bordercolor="#00ff88",
    borderwidth=1,
    borderpad=6,
)
fig_vol.update_layout(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    height=420,
    showlegend=False,
    yaxis=dict(
        title="Quarterly Volume (USD Billions)",
        gridcolor="rgba(255,255,255,0.06)",
        tickcolor="rgba(255,255,255,0.3)",
        tickfont=dict(color="rgba(255,255,255,0.6)"),
        titlefont=dict(color="rgba(255,255,255,0.6)"),
    ),
    xaxis=dict(
        tickfont=dict(color="rgba(255,255,255,0.6)", size=13),
        tickcolor="rgba(255,255,255,0.1)",
    ),
    margin=dict(t=30, b=30, l=60, r=60),
    font=dict(family="Inter"),
)
st.plotly_chart(fig_vol, use_container_width=True)

col_v1, col_v2, col_v3 = st.columns(3)
with col_v1:
    st.markdown("""
    <div class="stat-card">
      <div class="stat-number" style="color:#a78bfa;">7x</div>
      <div class="stat-label">Volume growth Q1'24 → Q4'24</div>
    </div>""", unsafe_allow_html=True)
with col_v2:
    st.markdown("""
    <div class="stat-card">
      <div class="stat-number" style="color:#00d4ff;">$1.75B</div>
      <div class="stat-label">Q1 2026 — rising non-election baseline</div>
    </div>""", unsafe_allow_html=True)
with col_v3:
    st.markdown("""
    <div class="stat-card">
      <div class="stat-number" style="color:#00ff88;">+600%</div>
      <div class="stat-label">Non-election baseline vs. Q1 2024</div>
    </div>""", unsafe_allow_html=True)

st.markdown("<hr class='divider'>", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# 6. FUNDING TIMELINE
# ══════════════════════════════════════════════════════════════════════════════
st.markdown('<div class="section-tag">Funding History</div>', unsafe_allow_html=True)
st.markdown('<div class="section-title">From a Lower East Side Apartment to $9B</div>', unsafe_allow_html=True)

funding_data = {
    "Round": ["Seed", "Series A", "Series B", "ICE Strategic"],
    "Year": [2020, 2024, 2024, 2025],
    "Amount": [4, 25, 45, 2000],
    "Valuation": [10, 200, 1000, 9000],
}
df_fund = pd.DataFrame(funding_data)

fig_fund = go.Figure()
fig_fund.add_trace(go.Scatter(
    x=df_fund["Year"],
    y=df_fund["Valuation"],
    mode="lines+markers+text",
    line=dict(color="#7c3aed", width=3, dash="dot"),
    marker=dict(size=16, color=["#7c3aed", "#00d4ff", "#00d4ff", "#00ff88"],
                line=dict(color="white", width=2)),
    text=df_fund["Round"],
    textposition="top center",
    textfont=dict(color="white", size=12),
    name="Valuation ($M)",
    hovertemplate="<b>%{text}</b><br>Year: %{x}<br>Valuation: $%{y}M<extra></extra>",
))
fig_fund.add_trace(go.Bar(
    x=df_fund["Year"],
    y=df_fund["Amount"],
    name="Amount Raised ($M)",
    marker=dict(color=["rgba(124,58,237,0.4)", "rgba(0,212,255,0.4)",
                        "rgba(0,212,255,0.4)", "rgba(0,255,136,0.4)"],
                line=dict(color="rgba(255,255,255,0.2)", width=1),
                cornerradius=6),
    yaxis="y2",
    hovertemplate="<b>%{x}</b><br>Raised: $%{y}M<extra></extra>",
    text=[f"${v}M" for v in df_fund["Amount"]],
    textposition="inside",
    textfont=dict(color="white", size=11),
))
fig_fund.update_layout(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    height=380,
    yaxis=dict(
        title="Valuation ($M)", gridcolor="rgba(255,255,255,0.06)",
        tickcolor="rgba(255,255,255,0.2)", tickfont=dict(color="rgba(255,255,255,0.5)"),
        titlefont=dict(color="rgba(255,255,255,0.5)"),
    ),
    yaxis2=dict(
        title="Amount Raised ($M)", overlaying="y", side="right",
        tickfont=dict(color="rgba(255,255,255,0.5)"),
        titlefont=dict(color="rgba(255,255,255,0.5)"),
    ),
    xaxis=dict(tickfont=dict(color="rgba(255,255,255,0.6)"), tickcolor="rgba(255,255,255,0.1)"),
    legend=dict(font=dict(color="rgba(255,255,255,0.7)"), bgcolor="rgba(0,0,0,0)"),
    margin=dict(t=20, b=30, l=60, r=60),
    barmode="overlay",
    font=dict(family="Inter"),
)
st.plotly_chart(fig_fund, use_container_width=True)

c1, c2, c3, c4 = st.columns(4)
funding_details = [
    ("2020 · Seed", "$4M", "Company launch. Solo founder. Zero institutional backing."),
    ("2024 · Series A", "$25M", "General Catalyst leads. Polymarket survives regulatory scrutiny."),
    ("2024 · Series B", "$45M", "Founders Fund + Vitalik Buterin. Elite VC stamp of approval."),
    ("2025 · ICE", "$2B", "NYSE parent invests. $9B pre-money. Game over for competitors."),
]
for col, (title, amount, desc) in zip([c1, c2, c3, c4], funding_details):
    with col:
        st.markdown(f"""
        <div class="card" style="padding:24px;">
          <div style="font-size:12px;color:rgba(255,255,255,0.5);margin-bottom:6px;">{title}</div>
          <div style="font-size:32px;font-weight:800;color:#00d4ff;margin-bottom:10px;">{amount}</div>
          <div style="font-size:13px;color:rgba(255,255,255,0.6);line-height:1.5;">{desc}</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("<hr class='divider'>", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# 7. INVESTORS
# ══════════════════════════════════════════════════════════════════════════════
st.markdown('<div class="section-tag">Investors</div>', unsafe_allow_html=True)
st.markdown('<div class="section-title">The Who\'s Who of Disruption Capital</div>', unsafe_allow_html=True)

investors = [
    {
        "name": "Peter Thiel",
        "role": "Founders Fund",
        "emoji": "🦅",
        "color": "#00d4ff",
        "signal": "Co-founder of PayPal, Palantir, Facebook investor. Backs companies that challenge existing institutions.",
        "quote": '"We wanted flying cars, instead we got 140 characters" — Thiel bets Polymarket becomes the truth layer of the internet.',
    },
    {
        "name": "Vitalik Buterin",
        "role": "Ethereum Co-Founder",
        "emoji": "⟠",
        "color": "#a78bfa",
        "signal": "Personal investment. The inventor of the blockchain Polymarket runs on vouching with his own capital.",
        "quote": "Vitalik has long championed prediction markets as Ethereum's killer app. This is his bet paying off.",
    },
    {
        "name": "General Catalyst",
        "role": "Series A Lead — $25M",
        "emoji": "🚀",
        "color": "#00ff88",
        "signal": "Backed Airbnb, Stripe, Snap. GC's Series A at regulatory peak uncertainty = highest conviction signal.",
        "quote": "Invested during the CFTC enforcement era. That's not recklessness — that's category conviction.",
    },
    {
        "name": "Intercontinental Exchange",
        "role": "NYSE Parent · $2B",
        "emoji": "🏛️",
        "color": "#ffa502",
        "signal": "Owns the New York Stock Exchange. Their $2B investment at $9B valuation signals Polymarket as financial infrastructure.",
        "quote": "When the stock exchange bets $2B on you, you're no longer a startup. You're a new asset class.",
    },
]

cols = st.columns(4)
for col, inv in zip(cols, investors):
    with col:
        st.markdown(f"""
        <div class="investor-card">
          <div style="font-size:48px;margin-bottom:12px;">{inv['emoji']}</div>
          <div class="investor-name">{inv['name']}</div>
          <div class="investor-role">{inv['role']}</div>
          <div class="investor-signal">{inv['signal']}</div>
          <div style="margin-top:16px;font-size:13px;color:rgba(255,255,255,0.5);font-style:italic;line-height:1.5;">
            {inv['quote']}
          </div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("<hr class='divider'>", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# 8. MARKET OPPORTUNITY
# ══════════════════════════════════════════════════════════════════════════════
st.markdown('<div class="section-tag">Market Opportunity</div>', unsafe_allow_html=True)
st.markdown('<div class="section-title">A $1 Trillion Market in Plain Sight</div>', unsafe_allow_html=True)

col_m1, col_m2 = st.columns([1.2, 1])
with col_m1:
    # TAM/SAM/SOM bubble chart
    fig_tam = go.Figure()
    sizes = [800, 300, 80]
    labels = ["TAM<br>~$1T+", "SAM<br>~$200B", "SOM<br>~$20B"]
    colors_tam = ["rgba(124,58,237,0.25)", "rgba(0,212,255,0.3)", "rgba(0,255,136,0.4)"]
    border_colors = ["#7c3aed", "#00d4ff", "#00ff88"]

    for size, label, color, bc in zip(sizes, labels, colors_tam, border_colors):
        fig_tam.add_trace(go.Scatter(
            x=[0], y=[0],
            mode="markers+text",
            marker=dict(size=size, color=color, line=dict(color=bc, width=2),
                        sizemode="area"),
            text=[label],
            textfont=dict(color="white", size=14, family="Inter"),
            hoverinfo="skip",
            showlegend=False,
        ))

    fig_tam.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        height=380,
        xaxis=dict(visible=False, range=[-400, 400]),
        yaxis=dict(visible=False, range=[-400, 400]),
        margin=dict(t=10, b=10, l=10, r=10),
    )
    st.plotly_chart(fig_tam, use_container_width=True)

with col_m2:
    st.markdown("""
    <div style="padding-top:20px;">
      <div style="margin-bottom:28px;">
        <div style="display:flex;align-items:center;gap:12px;margin-bottom:10px;">
          <div style="width:16px;height:16px;border-radius:50%;background:#7c3aed;"></div>
          <div style="font-size:20px;font-weight:700;">TAM — ~$1 Trillion+</div>
        </div>
        <div style="color:rgba(255,255,255,0.6);font-size:15px;line-height:1.6;padding-left:28px;">
          Global event trading, political forecasting, sports betting, financial information markets,
          and institutional probability data. Every uncertain outcome is a potential market.
        </div>
      </div>
      <div style="margin-bottom:28px;">
        <div style="display:flex;align-items:center;gap:12px;margin-bottom:10px;">
          <div style="width:16px;height:16px;border-radius:50%;background:#00d4ff;"></div>
          <div style="font-size:20px;font-weight:700;">SAM — ~$200 Billion</div>
        </div>
        <div style="color:rgba(255,255,255,0.6);font-size:15px;line-height:1.6;padding-left:28px;">
          Crypto-native and regulated users who can legally access event contracts and are
          comfortable with digital infrastructure. Expanding rapidly as USDC adoption grows.
        </div>
      </div>
      <div>
        <div style="display:flex;align-items:center;gap:12px;margin-bottom:10px;">
          <div style="width:16px;height:16px;border-radius:50%;background:#00ff88;"></div>
          <div style="font-size:20px;font-weight:700;">SOM — ~$20 Billion</div>
        </div>
        <div style="color:rgba(255,255,255,0.6);font-size:15px;line-height:1.6;padding-left:28px;">
          Polymarket's realistically capturable share today — already generating $1.75B/quarter
          and growing. ICE partnership opens the institutional layer.
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<hr class='divider'>", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# 9. COMPETITION
# ══════════════════════════════════════════════════════════════════════════════
st.markdown('<div class="section-tag">Competition</div>', unsafe_allow_html=True)
st.markdown('<div class="section-title">Polymarket vs. The World</div>', unsafe_allow_html=True)

comparison = {
    "Dimension": ["Regulatory Status", "Monthly Volume", "Settlement", "User Base", "Media Presence", "Valuation", "US Access", "Viral Growth"],
    "Polymarket": ["Crypto-native (CFTC resolved)", "$1.75B+ (Q1 2026)", "USDC on Polygon", "445K+ active traders", "Quoted by CNN, FT, Reuters", "$9B post-ICE", "Re-entered 2025 via QCEX", "🔥 Explosive"],
    "Kalshi": ["Fully CFTC-regulated", "~$200M/month", "USD, bank transfer", "Growing but smaller", "Less viral, more institutional", "~$1B (est.)", "Always compliant", "📈 Steady"],
}
df_comp = pd.DataFrame(comparison)

col_table, col_radar = st.columns([1, 1])
with col_table:
    st.dataframe(
        df_comp.style
        .set_properties(**{
            "background-color": "rgba(13,13,26,0.8)",
            "color": "white",
            "border": "1px solid rgba(255,255,255,0.08)",
            "font-size": "14px",
        })
        .set_table_styles([
            {"selector": "th", "props": [
                ("background-color", "rgba(0,212,255,0.1)"),
                ("color", "#00d4ff"),
                ("font-weight", "600"),
                ("font-size", "13px"),
                ("text-align", "center"),
            ]},
        ]),
        use_container_width=True,
        hide_index=True,
        height=340,
    )

with col_radar:
    categories = ["Volume", "Viral Growth", "Regulation", "Brand", "Tech", "VC Backing"]
    poly_scores = [95, 90, 60, 92, 88, 95]
    kalshi_scores = [35, 40, 95, 55, 75, 60]

    fig_radar = go.Figure()
    fig_radar.add_trace(go.Scatterpolar(
        r=poly_scores + [poly_scores[0]],
        theta=categories + [categories[0]],
        fill="toself",
        fillcolor="rgba(0,212,255,0.15)",
        line=dict(color="#00d4ff", width=2),
        name="Polymarket",
        hovertemplate="%{theta}: %{r}<extra></extra>",
    ))
    fig_radar.add_trace(go.Scatterpolar(
        r=kalshi_scores + [kalshi_scores[0]],
        theta=categories + [categories[0]],
        fill="toself",
        fillcolor="rgba(124,58,237,0.12)",
        line=dict(color="#a78bfa", width=2, dash="dash"),
        name="Kalshi",
        hovertemplate="%{theta}: %{r}<extra></extra>",
    ))
    fig_radar.update_layout(
        polar=dict(
            bgcolor="rgba(0,0,0,0)",
            radialaxis=dict(visible=True, range=[0, 100], tickcolor="rgba(255,255,255,0.3)",
                           tickfont=dict(color="rgba(255,255,255,0.4)", size=10),
                           gridcolor="rgba(255,255,255,0.08)"),
            angularaxis=dict(tickfont=dict(color="rgba(255,255,255,0.7)", size=13),
                            gridcolor="rgba(255,255,255,0.08)"),
        ),
        paper_bgcolor="rgba(0,0,0,0)",
        height=340,
        legend=dict(font=dict(color="rgba(255,255,255,0.7)"), bgcolor="rgba(0,0,0,0)"),
        margin=dict(t=20, b=20, l=40, r=40),
        font=dict(family="Inter"),
    )
    st.plotly_chart(fig_radar, use_container_width=True)

st.markdown("<hr class='divider'>", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# 10. RISKS
# ══════════════════════════════════════════════════════════════════════════════
st.markdown('<div class="section-tag">Risk Analysis</div>', unsafe_allow_html=True)
st.markdown('<div class="section-title">Eyes Open: The Risk Stack</div>', unsafe_allow_html=True)

risks = [
    {
        "level": "HIGH", "level_class": "risk-high",
        "title": "Regulatory Risk (CFTC)",
        "desc": "2022 fine of $1.4M. CFTC may classify markets as derivatives requiring full exchange registration. Re-entry via QCEX acquisition mitigates but doesn't eliminate this risk.",
    },
    {
        "level": "HIGH", "level_class": "risk-high",
        "title": "Political Scrutiny",
        "desc": "FBI searched Shayne Coplan's home post-2024 election. Political markets draw government attention. Company described it as politically motivated — not established wrongdoing.",
    },
    {
        "level": "MED", "level_class": "risk-med",
        "title": "Event-Cycle Revenue Volatility",
        "desc": "Q4 2024 was 4x higher than adjacent quarters. If non-election baseline stays low, revenue visibility is poor and multiples may compress.",
    },
    {
        "level": "MED", "level_class": "risk-med",
        "title": "Crypto Compliance Risk",
        "desc": "USDC settlement, non-custodial wallets, and geofencing create complex KYC/AML challenges. VPN circumvention by restricted users is a real liability.",
    },
    {
        "level": "LOW", "level_class": "risk-low",
        "title": "Competition from Kalshi",
        "desc": "Kalshi has full regulatory approval and growing institutional traction. However, Polymarket's brand dominance and viral distribution are hard to replicate.",
    },
    {
        "level": "LOW", "level_class": "risk-low",
        "title": "Exit Uncertainty",
        "desc": "IPO path requires audited revenues and regulatory clarity. M&A path exists (ICE is already invested). Exit optionality is real but timeline-dependent.",
    },
]

for i in range(0, len(risks), 2):
    col1, col2 = st.columns(2)
    for j, col in enumerate([col1, col2]):
        if i + j < len(risks):
            r = risks[i + j]
            with col:
                st.markdown(f"""
                <div class="card" style="padding:24px;margin-bottom:16px;">
                  <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:12px;">
                    <div style="font-size:17px;font-weight:700;">{r['title']}</div>
                    <span class="risk-pill {r['level_class']}">{r['level']}</span>
                  </div>
                  <div style="font-size:14px;color:rgba(255,255,255,0.65);line-height:1.6;">{r['desc']}</div>
                </div>
                """, unsafe_allow_html=True)

st.markdown("<hr class='divider'>", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# 11. INVESTMENT THESIS
# ══════════════════════════════════════════════════════════════════════════════
st.markdown('<div class="section-tag">Investment Thesis</div>', unsafe_allow_html=True)
st.markdown('<div class="section-title">Our Verdict</div>', unsafe_allow_html=True)

st.markdown("""
<div class="reco-box">
  <div class="reco-verdict">CONDITIONAL INVEST</div>
  <div style="font-size:22px;color:rgba(255,255,255,0.8);max-width:800px;margin:0 auto 40px;line-height:1.6;">
    Polymarket is the most compelling fintech infrastructure bet of 2026 —
    with one critical caveat: regulatory clarity is the unlock condition.
  </div>
</div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

col_bull, col_bear = st.columns(2)
with col_bull:
    st.markdown("""
    <div class="card" style="border-color:rgba(0,255,136,0.3);background:rgba(0,255,136,0.04);">
      <div style="color:#00ff88;font-size:13px;font-weight:700;letter-spacing:2px;text-transform:uppercase;margin-bottom:16px;">
        BULL CASE — Why Invest Now
      </div>
      <div style="display:flex;flex-direction:column;gap:14px;">
        <div style="display:flex;gap:12px;"><span style="color:#00ff88;">✓</span><span>First-mover with unassailable brand & liquidity moat</span></div>
        <div style="display:flex;gap:12px;"><span style="color:#00ff88;">✓</span><span>NYSE parent (ICE) validates institutional exit path at $9B+</span></div>
        <div style="display:flex;gap:12px;"><span style="color:#00ff88;">✓</span><span>Non-election baseline growing 600% vs. 2024 — habitual use emerging</span></div>
        <div style="display:flex;gap:12px;"><span style="color:#00ff88;">✓</span><span>Founders Fund + Vitalik = most credible signal in crypto-fintech</span></div>
        <div style="display:flex;gap:12px;"><span style="color:#00ff88;">✓</span><span>Media quotes Polymarket odds — organic distribution no competitor can buy</span></div>
        <div style="display:flex;gap:12px;"><span style="color:#00ff88;">✓</span><span>Re-entered U.S. market via QCEX — regulatory overhang reducing</span></div>
      </div>
    </div>
    """, unsafe_allow_html=True)

with col_bear:
    st.markdown("""
    <div class="card" style="border-color:rgba(255,71,87,0.3);background:rgba(255,71,87,0.04);">
      <div style="color:#ff4757;font-size:13px;font-weight:700;letter-spacing:2px;text-transform:uppercase;margin-bottom:16px;">
        BEAR CASE — What Must Be True to Not Invest
      </div>
      <div style="display:flex;flex-direction:column;gap:14px;">
        <div style="display:flex;gap:12px;"><span style="color:#ff4757;">✗</span><span>CFTC reclassifies all prediction contracts as unregistered derivatives</span></div>
        <div style="display:flex;gap:12px;"><span style="color:#ff4757;">✗</span><span>Political markets banned — primary revenue & attention driver disappears</span></div>
        <div style="display:flex;gap:12px;"><span style="color:#ff4757;">✗</span><span>FBI investigation escalates to charges against founder</span></div>
        <div style="display:flex;gap:12px;"><span style="color:#ff4757;">✗</span><span>Non-election baseline stagnates; revenue remains event-cyclical</span></div>
        <div style="display:flex;gap:12px;"><span style="color:#ff4757;">✗</span><span>Kalshi captures institutional market while Polymarket fights regulators</span></div>
        <div style="display:flex;gap:12px;"><span style="color:#ff4757;">✗</span><span>$9B entry valuation leaves insufficient upside for new investors</span></div>
      </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)
st.markdown("""
<div style="background:rgba(255,255,255,0.04);border:1px solid rgba(255,255,255,0.1);border-radius:20px;padding:32px;margin-top:8px;">
  <div style="font-size:18px;font-weight:700;margin-bottom:16px;">Investment Structure We Recommend</div>
  <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:16px;">
    <div style="background:rgba(0,212,255,0.06);border:1px solid rgba(0,212,255,0.2);border-radius:12px;padding:16px;">
      <div style="color:#00d4ff;font-weight:700;margin-bottom:6px;">Staged Financing</div>
      <div style="font-size:13px;color:rgba(255,255,255,0.6);">Milestone-based capital release tied to regulatory progress</div>
    </div>
    <div style="background:rgba(124,58,237,0.06);border:1px solid rgba(124,58,237,0.2);border-radius:12px;padding:16px;">
      <div style="color:#a78bfa;font-weight:700;margin-bottom:6px;">Governance Rights</div>
      <div style="font-size:13px;color:rgba(255,255,255,0.6);">Board seat + compliance reporting requirements</div>
    </div>
    <div style="background:rgba(0,255,136,0.06);border:1px solid rgba(0,255,136,0.2);border-radius:12px;padding:16px;">
      <div style="color:#00ff88;font-weight:700;margin-bottom:6px;">US Access Plan</div>
      <div style="font-size:13px;color:rgba(255,255,255,0.6);">Require credible strategy: registration, partnership, or spinout</div>
    </div>
    <div style="background:rgba(255,165,2,0.06);border:1px solid rgba(255,165,2,0.2);border-radius:12px;padding:16px;">
      <div style="color:#ffa502;font-weight:700;margin-bottom:6px;">Category Diversification</div>
      <div style="font-size:13px;color:rgba(255,255,255,0.6);">Must show non-political markets retain users between election cycles</div>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

st.markdown("<hr class='divider'>", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# 12. LIVE POLYMARKET DATA
# ══════════════════════════════════════════════════════════════════════════════
st.markdown('<div class="section-tag">Live Data</div>', unsafe_allow_html=True)
st.markdown('<div class="section-title">Polymarket — Right Now</div>', unsafe_allow_html=True)
st.markdown('<div class="section-sub"><span style="animation:pulse 2s infinite;">&#x25CF;</span> Live markets pulled directly from the Polymarket Gamma API</div>', unsafe_allow_html=True)

@st.cache_data(ttl=120)
def fetch_live_markets():
    try:
        url = "https://gamma-api.polymarket.com/markets?active=true&closed=false&limit=12&order=volume&ascending=false"
        r = requests.get(url, timeout=8)
        r.raise_for_status()
        return r.json()
    except Exception:
        return None

with st.spinner("Fetching live markets..."):
    markets = fetch_live_markets()

if markets:
    st.markdown(f"""
    <div style="display:flex;align-items:center;gap:10px;margin-bottom:24px;">
      <span class="live-dot"></span>
      <span style="color:#00ff88;font-size:14px;font-weight:600;">{len(markets)} markets loaded · Updated {datetime.now().strftime('%H:%M:%S')}</span>
    </div>
    """, unsafe_allow_html=True)

    for m in markets[:8]:
        title = m.get("question") or m.get("title", "Unknown Market")
        volume = m.get("volume", 0)
        outcomes = m.get("outcomes", [])
        prices = m.get("outcomePrices", [])

        try:
            vol_fmt = f"${float(volume):,.0f}" if volume else "N/A"
        except Exception:
            vol_fmt = "N/A"

        yes_prob = 50
        try:
            if prices and len(prices) >= 1:
                yes_prob = round(float(prices[0]) * 100, 1)
        except Exception:
            pass

        st.markdown(f"""
        <div class="live-card">
          <div style="flex:1;min-width:0;margin-right:24px;">
            <div style="font-size:15px;font-weight:600;margin-bottom:8px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;">
              <span class="live-dot"></span>{title[:90]}{"..." if len(title) > 90 else ""}
            </div>
            <div class="probability-bar">
              <div class="probability-fill" style="width:{yes_prob}%;"></div>
            </div>
            <div style="display:flex;justify-content:space-between;margin-top:6px;">
              <span style="font-size:12px;color:rgba(255,255,255,0.5);">YES probability</span>
              <span style="font-size:12px;color:#00d4ff;font-weight:700;">{yes_prob}%</span>
            </div>
          </div>
          <div style="text-align:right;flex-shrink:0;">
            <div style="font-size:18px;font-weight:700;color:#00ff88;">{vol_fmt}</div>
            <div style="font-size:11px;color:rgba(255,255,255,0.4);">volume</div>
          </div>
        </div>
        """, unsafe_allow_html=True)

    if st.button("Refresh live data"):
        st.cache_data.clear()
        st.rerun()
else:
    st.markdown("""
    <div style="background:rgba(255,165,2,0.08);border:1px solid rgba(255,165,2,0.3);border-radius:16px;padding:32px;text-align:center;">
      <div style="font-size:48px;margin-bottom:16px;">🌐</div>
      <div style="font-size:18px;font-weight:600;margin-bottom:8px;">API Temporarily Unavailable</div>
      <div style="color:rgba(255,255,255,0.6);">Live data requires an internet connection to gamma-api.polymarket.com</div>
    </div>
    """, unsafe_allow_html=True)
    # Show sample data instead
    sample = [
        ("Will Bitcoin reach $150,000 in 2026?", 82000, 48),
        ("Will the Fed cut rates before September 2026?", 45000, 61),
        ("Will there be a US recession in 2026?", 38000, 33),
        ("Will Trump sign the crypto bill in 2026?", 29000, 71),
    ]
    for title, vol, prob in sample:
        st.markdown(f"""
        <div class="live-card" style="opacity:0.7;">
          <div style="flex:1;min-width:0;margin-right:24px;">
            <div style="font-size:15px;font-weight:600;margin-bottom:8px;">⚡ {title}</div>
            <div class="probability-bar">
              <div class="probability-fill" style="width:{prob}%;"></div>
            </div>
            <div style="display:flex;justify-content:space-between;margin-top:6px;">
              <span style="font-size:12px;color:rgba(255,255,255,0.5);">YES probability (sample)</span>
              <span style="font-size:12px;color:#00d4ff;font-weight:700;">{prob}%</span>
            </div>
          </div>
          <div style="text-align:right;flex-shrink:0;">
            <div style="font-size:18px;font-weight:700;color:#00ff88;">${vol:,}</div>
            <div style="font-size:11px;color:rgba(255,255,255,0.4);">est. volume</div>
          </div>
        </div>
        """, unsafe_allow_html=True)

# ── Footer ─────────────────────────────────────────────────────────────────────
st.markdown("<hr class='divider'>", unsafe_allow_html=True)
st.markdown("""
<div style="text-align:center;padding:40px 0;color:rgba(255,255,255,0.3);font-size:13px;">
  <div style="font-size:32px;margin-bottom:12px;">🔮</div>
  <div style="font-size:18px;font-weight:700;color:rgba(255,255,255,0.6);margin-bottom:8px;">
    Polymarket — The World's Largest Prediction Market
  </div>
  <div style="margin-bottom:16px;">
    Prepared by Leon Ye &amp; Ilyos Umurzakov · Frankfurt University of Applied Sciences · June 2026
  </div>
  <div>
    Sources: CoinDesk · Axios · Fortune · Bloomberg · ICE · CFTC · Poly Syncer · Dune Analytics · Wikipedia
  </div>
</div>
""", unsafe_allow_html=True)
