"""
GPREC IntelliBot - Main Streamlit Application
AI-Powered Navigator and Information Hub for Students
"""
import streamlit as st
import requests
import json
import uuid
from datetime import datetime

# Page Config
st.set_page_config(
    page_title="GPREC IntelliBot",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# API Base URL
API_BASE = "http://localhost:8000/api"

# ── Inject Custom CSS ──────────────────────────────────────────────────────────
st.markdown("""
<style>
    /* ── Global Reset & Font ── */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

    /* ── Sidebar ── */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
        color: white;
    }
    [data-testid="stSidebar"] .stSelectbox label,
    [data-testid="stSidebar"] .stRadio label,
    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3 { color: white !important; }

    /* ── Main Area ── */
    .main { background: #f0f4f8; }
    .stApp { background: #f0f4f8; }

    /* ── Header Banner ── */
    .gprec-header {
        background: linear-gradient(135deg, #1a1a2e 0%, #e94560 100%);
        padding: 1.5rem 2rem;
        border-radius: 16px;
        margin-bottom: 1.5rem;
        color: white;
        text-align: center;
        box-shadow: 0 8px 32px rgba(233,69,96,0.3);
    }
    .gprec-header h1 { font-size: 2rem; font-weight: 700; margin: 0; }
    .gprec-header p  { font-size: 1rem; margin: 4px 0 0; opacity: 0.9; }

    /* ── Chat Messages ── */
    .chat-container {
        max-height: 480px;
        overflow-y: auto;
        padding: 1rem;
        background: white;
        border-radius: 16px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.08);
        margin-bottom: 1rem;
        scroll-behavior: smooth;
    }
    .user-msg {
        background: linear-gradient(135deg, #1a1a2e, #e94560);
        color: white;
        padding: 0.75rem 1rem;
        border-radius: 18px 18px 4px 18px;
        margin: 0.5rem 0 0.5rem 20%;
        box-shadow: 0 2px 8px rgba(233,69,96,0.25);
        font-size: 0.9rem;
    }
    .bot-msg {
        background: white;
        color: #1a1a2e;
        padding: 0.75rem 1rem;
        border-radius: 18px 18px 18px 4px;
        margin: 0.5rem 20% 0.5rem 0;
        border: 1.5px solid #e8edf3;
        box-shadow: 0 2px 8px rgba(0,0,0,0.06);
        font-size: 0.9rem;
        line-height: 1.6;
    }
    .msg-time { font-size: 0.7rem; opacity: 0.55; margin-top: 4px; }

    /* ── Cards ── */
    .metric-card {
        background: white;
        padding: 1.25rem;
        border-radius: 12px;
        box-shadow: 0 2px 12px rgba(0,0,0,0.07);
        text-align: center;
        border-left: 4px solid #e94560;
        margin-bottom: 0.75rem;
    }
    .metric-card h3 { font-size: 1.8rem; color: #e94560; margin: 0; }
    .metric-card p  { color: #555; font-size: 0.85rem; margin: 4px 0 0; }

    .company-card {
        background: white;
        padding: 1rem 1.25rem;
        border-radius: 12px;
        border-left: 4px solid #0f3460;
        margin: 0.5rem 0;
        box-shadow: 0 2px 10px rgba(0,0,0,0.06);
        transition: transform 0.15s;
    }
    .company-card:hover { transform: translateX(4px); }
    .company-card h4 { color: #0f3460; margin: 0; font-size: 1rem; }
    .company-card p  { color: #666; margin: 4px 0 0; font-size: 0.82rem; }

    .notif-card {
        background: white;
        padding: 1rem;
        border-radius: 12px;
        margin: 0.5rem 0;
        box-shadow: 0 2px 10px rgba(0,0,0,0.06);
    }
    .notif-placement { border-left: 4px solid #27ae60; }
    .notif-exam      { border-left: 4px solid #e74c3c; }
    .notif-event     { border-left: 4px solid #f39c12; }
    .notif-general   { border-left: 4px solid #3498db; }

    /* ── Buttons ── */
    .stButton > button {
        background: linear-gradient(135deg, #e94560, #0f3460) !important;
        color: white !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 0.5rem 1.5rem !important;
        font-weight: 600 !important;
        transition: opacity 0.2s !important;
    }
    .stButton > button:hover { opacity: 0.88 !important; }

    /* ── Map Location Dots ── */
    .map-dot {
        display: inline-block;
        width: 12px; height: 12px;
        border-radius: 50%;
        margin-right: 6px;
        vertical-align: middle;
    }

    /* ── Quick-Reply Pills ── */
    .quick-pill {
        display: inline-block;
        background: #f0f4f8;
        border: 1.5px solid #d0d8e4;
        border-radius: 20px;
        padding: 4px 14px;
        margin: 4px 4px 0 0;
        font-size: 0.8rem;
        cursor: pointer;
        color: #1a1a2e;
        transition: background 0.15s;
    }
    .quick-pill:hover { background: #e94560; color: white; border-color: #e94560; }
</style>
""", unsafe_allow_html=True)


# ── Helpers ───────────────────────────────────────────────────────────────────
def api_post(endpoint: str, data: dict):
    try:
        r = requests.post(f"{API_BASE}{endpoint}", json=data, timeout=30)
        return r.json() if r.ok else None
    except Exception:
        return None

def api_get(endpoint: str, params: dict = None):
    try:
        r = requests.get(f"{API_BASE}{endpoint}", params=params, timeout=10)
        return r.json() if r.ok else None
    except Exception:
        return None

def check_api():
    try:
        r = requests.get("http://localhost:8000/health", timeout=3)
        return r.ok
    except Exception:
        return False

def notif_color_class(category: str) -> str:
    return {"placement": "notif-placement", "exam": "notif-exam",
            "event": "notif-event"}.get(category, "notif-general")

def notif_icon(category: str) -> str:
    return {"placement": "💼", "exam": "📝", "event": "🎉", "general": "📢"}.get(category, "📢")

CAT_COLORS = {"admin": "#e94560", "department": "#0f3460", "facility": "#27ae60",
              "hostel": "#f39c12", "sports": "#8e44ad", "entrance": "#16a085", "placement": "#2980b9"}


# ── Session State Init ─────────────────────────────────────────────────────────
for key, default in [
    ("messages", [{"role": "bot", "content": "👋 Hello! I'm **GPREC IntelliBot**, your AI assistant for G. Pulla Reddy Engineering College, Kurnool.\n\nI can help you with:\n- 🗺️ Campus navigation\n- 📋 Placement information\n- 📢 Latest notifications\n- 🎓 Academic queries\n- 🏠 Hostel & facilities\n\nHow can I assist you today?", "time": datetime.now().strftime("%H:%M")}]),
    ("session_id", str(uuid.uuid4())),
    ("language", "en"),
    ("page", "💬 IntelliBot Chat"),
]:
    if key not in st.session_state:
        st.session_state[key] = default


# ── Sidebar ────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🤖 GPREC IntelliBot")
    st.markdown("*AI-Powered Student Assistant*")
    st.divider()

    api_ok = check_api()
    status_color = "🟢" if api_ok else "🔴"
    st.markdown(f"{status_color} **API Status:** {'Connected' if api_ok else 'Offline'}")
    if not api_ok:
        st.warning("⚠️ Start the backend:\n```\npython backend/main.py\n```")

    st.divider()

    page = st.radio(
        "Navigate to:",
        ["💬 IntelliBot Chat", "🗺️ Campus Map", "💼 Placement Analyzer", "📢 Notifications", "ℹ️ College Info"],
        index=0
    )
    st.session_state.page = page

    st.divider()
    st.markdown("**Language / భాష / भाषा**")
    lang_map = {"English 🇬🇧": "en", "Telugu 🇮🇳": "te", "Hindi 🇮🇳": "hi"}
    lang_choice = st.selectbox("Select Language", list(lang_map.keys()))
    st.session_state.language = lang_map[lang_choice]

    st.divider()
    st.markdown("**Quick Questions**")
    quick_questions = [
        "Where is the library?",
        "How to reach placement cell?",
        "Exam schedule?",
        "Hostel fees?",
        "Library timings?",
    ]
    for q in quick_questions:
        if st.button(q, key=f"quick_{q}", use_container_width=True):
            st.session_state["auto_send"] = q

    st.divider()
    st.markdown("""
    **📞 Contact**  
    GPREC, Kurnool  
    📱 08518-220010  
    🌐 www.gprec.ac.in  
    """)


# ── Page: Chat ─────────────────────────────────────────────────────────────────
if st.session_state.page == "💬 IntelliBot Chat":
    st.markdown("""
    <div class="gprec-header">
        <h1>🤖 GPREC IntelliBot</h1>
        <p>AI-Powered Navigator and Information Hub for Students</p>
    </div>
    """, unsafe_allow_html=True)

    # Chat display
    chat_html = '<div class="chat-container" id="chat-box">'
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            chat_html += f'<div class="user-msg">👤 {msg["content"]}<div class="msg-time">{msg["time"]}</div></div>'
        else:
            content = msg["content"].replace("\n", "<br>")
            chat_html += f'<div class="bot-msg">🤖 {content}<div class="msg-time">{msg["time"]}</div></div>'
    chat_html += '</div>'
    st.markdown(chat_html, unsafe_allow_html=True)

    # Input area
    col1, col2 = st.columns([5, 1])
    with col1:
        user_input = st.text_input(
            "Your message",
            key="chat_input",
            placeholder="Ask me anything about GPREC...",
            label_visibility="collapsed"
        )
    with col2:
        send_btn = st.button("Send 📤", use_container_width=True)

    # Auto-send from sidebar quick buttons
    auto_msg = st.session_state.pop("auto_send", None)

    message_to_send = None
    if send_btn and user_input.strip():
        message_to_send = user_input.strip()
    elif auto_msg:
        message_to_send = auto_msg

    if message_to_send:
        now = datetime.now().strftime("%H:%M")
        st.session_state.messages.append({"role": "user", "content": message_to_send, "time": now})

        if api_ok:
            with st.spinner("IntelliBot is thinking..."):
                result = api_post("/chat/message", {
                    "message": message_to_send,
                    "session_id": st.session_state.session_id,
                    "language": st.session_state.language
                })
            bot_reply = result["response"] if result else "⚠️ Could not reach the server. Please check the backend is running."
        else:
            bot_reply = "⚠️ The AI backend is not running. Please start it with `python backend/main.py` and refresh."

        st.session_state.messages.append({"role": "bot", "content": bot_reply, "time": datetime.now().strftime("%H:%M")})
        st.rerun()

    # Clear chat button
    col_a, col_b, _ = st.columns([1, 1, 4])
    with col_a:
        if st.button("🗑️ Clear Chat"):
            st.session_state.messages = [st.session_state.messages[0]]
            st.session_state.session_id = str(uuid.uuid4())
            st.rerun()
    with col_b:
        if st.button("🔄 New Session"):
            st.session_state.session_id = str(uuid.uuid4())
            st.success("New session started!")


# ── Page: Campus Map ───────────────────────────────────────────────────────────
elif st.session_state.page == "🗺️ Campus Map":
    st.markdown("""
    <div class="gprec-header">
        <h1>🗺️ GPREC Campus Map</h1>
        <p>Interactive Campus Navigator</p>
    </div>
    """, unsafe_allow_html=True)

    data = api_get("/campus/locations")
    locations = data.get("locations", {}) if data else {}

    if not locations:
        st.warning("Could not load campus locations. Please ensure the backend is running.")
        st.stop()

    col1, col2 = st.columns([3, 2])

    with col1:
        st.markdown("### 📍 Campus Map")
        
        # Build SVG-based campus map
        svg_parts = [
            '<svg viewBox="0 0 500 450" xmlns="http://www.w3.org/2000/svg" style="width:100%;border-radius:12px;background:#e8f5e9;box-shadow:0 4px 20px rgba(0,0,0,0.1)">',
            # Background elements
            '<rect width="500" height="450" fill="#e8f5e9" rx="12"/>',
            # Roads
            '<line x1="250" y1="0" x2="250" y2="450" stroke="#bbb" stroke-width="4" stroke-dasharray="8,4"/>',
            '<line x1="0" y1="225" x2="500" y2="225" stroke="#bbb" stroke-width="4" stroke-dasharray="8,4"/>',
            # Campus boundary
            '<rect x="20" y="20" width="460" height="410" fill="none" stroke="#4caf50" stroke-width="3" stroke-dasharray="10,5" rx="8"/>',
            # Title
            '<text x="250" y="440" text-anchor="middle" font-family="Inter,Arial" font-size="11" fill="#333">GPREC Campus – Kurnool</text>',
        ]

        for loc_id, loc in locations.items():
            x = loc["x"] * 5  # scale to 500 wide
            y = (100 - loc["y"]) * 4.5  # scale to 450 tall, invert Y
            color = CAT_COLORS.get(loc["category"], "#666")
            label = loc["name"].replace("Engineering", "Engg")
            svg_parts += [
                f'<circle cx="{x}" cy="{y}" r="10" fill="{color}" opacity="0.9"/>',
                f'<circle cx="{x}" cy="{y}" r="14" fill="{color}" opacity="0.25"/>',
                f'<text x="{x}" y="{y+26}" text-anchor="middle" font-family="Inter,Arial" font-size="8.5" fill="#222" font-weight="600">{label}</text>',
            ]

        svg_parts.append('</svg>')
        st.markdown("".join(svg_parts), unsafe_allow_html=True)

        # Legend
        st.markdown("**Map Legend:**")
        legend_html = ""
        for cat, color in CAT_COLORS.items():
            legend_html += f'<span class="map-dot" style="background:{color}"></span> {cat.capitalize()}&nbsp;&nbsp;'
        st.markdown(legend_html, unsafe_allow_html=True)

    with col2:
        st.markdown("### 📋 Location Details")
        
        location_names = {loc_id: loc["name"] for loc_id, loc in locations.items()}
        selected_id = st.selectbox("Select a location:", list(location_names.keys()),
                                   format_func=lambda x: location_names[x])

        if selected_id and selected_id in locations:
            loc = locations[selected_id]
            color = CAT_COLORS.get(loc["category"], "#666")
            st.markdown(f"""
            <div class="company-card" style="border-left-color:{color}">
                <h4>📍 {loc['name']}</h4>
                <p>{loc['description']}</p>
                <p><strong>Category:</strong> {loc['category'].capitalize()}</p>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("### 🧭 Get Directions")
        loc_options = list(location_names.values())
        from_loc = st.selectbox("From:", loc_options, key="from_loc")
        to_loc   = st.selectbox("To:", loc_options, index=1, key="to_loc")

        if st.button("Get Directions 🗺️"):
            if from_loc != to_loc:
                with st.spinner("Getting directions..."):
                    result = api_post("/chat/navigate", {
                        "from_location": from_loc,
                        "to_location": to_loc
                    })
                if result:
                    st.info(result.get("directions", "Directions not available."))
                else:
                    st.error("Could not fetch directions. Is the backend running?")
            else:
                st.warning("Please select different from and to locations.")

        # All locations list
        st.markdown("### 🏛️ All Locations")
        for cat, color in CAT_COLORS.items():
            cat_locs = [(lid, l) for lid, l in locations.items() if l["category"] == cat]
            if cat_locs:
                st.markdown(f'<span class="map-dot" style="background:{color}"></span> **{cat.capitalize()}**', 
                          unsafe_allow_html=True)
                for lid, l in cat_locs:
                    st.markdown(f"&nbsp;&nbsp;&nbsp;• {l['name']}")


# ── Page: Placement Analyzer ───────────────────────────────────────────────────
elif st.session_state.page == "💼 Placement Analyzer":
    st.markdown("""
    <div class="gprec-header">
        <h1>💼 Placement Analyzer & Predictor</h1>
        <p>Find companies you're eligible for and get personalized advice</p>
    </div>
    """, unsafe_allow_html=True)

    # Stats row
    stats = api_get("/placement/stats")
    if stats:
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            st.markdown(f'<div class="metric-card"><h3>{stats["total_students_placed_2024"]}</h3><p>Students Placed (2024)</p></div>', unsafe_allow_html=True)
        with c2:
            st.markdown(f'<div class="metric-card"><h3>₹{stats["highest_package_lpa"]}L</h3><p>Highest Package</p></div>', unsafe_allow_html=True)
        with c3:
            st.markdown(f'<div class="metric-card"><h3>{stats["placement_percentage"]}%</h3><p>Placement Rate</p></div>', unsafe_allow_html=True)
        with c4:
            st.markdown(f'<div class="metric-card"><h3>{stats["total_companies_visited_2024"]}</h3><p>Companies Visited</p></div>', unsafe_allow_html=True)

    st.markdown("---")
    col1, col2 = st.columns([2, 3])

    with col1:
        st.markdown("### 👤 Your Profile")
        name   = st.text_input("Full Name", placeholder="Enter your name")
        branch = st.selectbox("Branch", ["CSE", "ECE", "EEE", "MECH", "CIVIL", "IT"])
        year   = st.selectbox("Current Year", [1, 2, 3, 4])
        cgpa   = st.slider("CGPA", 0.0, 10.0, 7.0, 0.1)
        backlogs = st.number_input("Active Backlogs", 0, 10, 0)

        st.markdown("**Skills (select all that apply)**")
        all_skills = ["Python", "Java", "C++", "JavaScript", "SQL", "Data Structures",
                      "Machine Learning", "Web Development", "Cloud Computing", "Communication"]
        skills = [s for s in all_skills if st.checkbox(s, key=f"skill_{s}")]

        analyze_btn = st.button("🔍 Analyze My Profile", use_container_width=True)

    with col2:
        if analyze_btn and name:
            if not api_ok:
                st.error("Backend not running. Please start `python backend/main.py`")
            else:
                with st.spinner("Analyzing your profile with AI..."):
                    result = api_post("/placement/analyze", {
                        "name": name, "branch": branch, "cgpa": cgpa,
                        "year": year, "skills": skills, "backlogs": backlogs
                    })

                if result:
                    st.success(f"✅ You're eligible for **{result['total_eligible']}** companies!")

                    # Eligible companies
                    st.markdown("### 🏢 Eligible Companies")
                    for company in result.get("eligible_companies", [])[:10]:
                        st.markdown(f"""
                        <div class="company-card">
                            <h4>🏢 {company['name']}</h4>
                            <p>💰 ₹{company['package_lpa']} LPA &nbsp;|&nbsp; 
                               👔 {company['role']} &nbsp;|&nbsp; 
                               📊 Min CGPA: {company['min_cgpa']}</p>
                        </div>
                        """, unsafe_allow_html=True)

                    # AI Advice
                    st.markdown("### 🤖 AI Career Advice")
                    st.info(result.get("ai_advice", "No advice available."))
                else:
                    st.error("Analysis failed. Please try again.")
        elif analyze_btn and not name:
            st.warning("Please enter your name to get started.")
        else:
            st.markdown("### 📊 All Companies at GPREC")
            companies_data = api_get("/placement/companies")
            if companies_data:
                for company in companies_data.get("companies", []):
                    branches_str = ", ".join(company["branches"][:4])
                    if len(company["branches"]) > 4:
                        branches_str += "..."
                    st.markdown(f"""
                    <div class="company-card">
                        <h4>🏢 {company['name']}</h4>
                        <p>💰 ₹{company['package_lpa']} LPA &nbsp;|&nbsp; 
                           📊 Min CGPA: {company['min_cgpa']} &nbsp;|&nbsp; 
                           📚 {branches_str}</p>
                    </div>
                    """, unsafe_allow_html=True)


# ── Page: Notifications ────────────────────────────────────────────────────────
elif st.session_state.page == "📢 Notifications":
    st.markdown("""
    <div class="gprec-header">
        <h1>📢 Notifications & Updates</h1>
        <p>Stay updated with latest campus announcements</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([1, 3])
    with col1:
        st.markdown("### 🔽 Filters")
        filter_cat = st.selectbox("Category", ["All", "placement", "exam", "event", "general"])
        filter_branch = st.selectbox("Branch", ["ALL", "CSE", "ECE", "EEE", "MECH", "CIVIL", "IT"])

    params = {}
    if filter_cat != "All":
        params["category"] = filter_cat
    if filter_branch != "ALL":
        params["branch"] = filter_branch

    with col2:
        notifications = api_get("/notifications/", params)
        if notifications:
            if not notifications:
                st.info("No notifications found for the selected filters.")
            for notif in notifications:
                color_class = notif_color_class(notif["category"])
                icon = notif_icon(notif["category"])
                created = notif["created_at"][:10]
                st.markdown(f"""
                <div class="notif-card {color_class}">
                    <strong>{icon} {notif['title']}</strong><br>
                    <small style="color:#666">{notif['category'].upper()} &nbsp;|&nbsp; 
                    Branch: {notif.get('target_branch','ALL')} &nbsp;|&nbsp; {created}</small><br><br>
                    {notif['message']}
                </div>
                """, unsafe_allow_html=True)
        else:
            st.warning("⚠️ Could not load notifications. Please check if the backend is running.")
            # Show static fallback
            static_notifs = [
                {"icon": "💼", "title": "TCS Campus Recruitment Drive", 
                 "msg": "TCS will be conducting campus recruitment for eligible students (CGPA ≥ 6.0). Register at the placement cell.", "color": "#27ae60"},
                {"icon": "📝", "title": "Mid Semester Examinations",
                 "msg": "Mid semester exams begin February 20, 2025. Timetable available at the admin block.", "color": "#e74c3c"},
                {"icon": "🎉", "title": "GPREC TECHNOVISTA 2025",
                 "msg": "National-level tech fest on March 5-7, 2025. Register now for coding, robotics, and paper presentation events.", "color": "#f39c12"},
            ]
            for n in static_notifs:
                st.markdown(f"""
                <div class="notif-card" style="border-left: 4px solid {n['color']}">
                    <strong>{n['icon']} {n['title']}</strong><br>
                    <small style="color:#666">Sample Notification</small><br><br>
                    {n['msg']}
                </div>
                """, unsafe_allow_html=True)


# ── Page: College Info ─────────────────────────────────────────────────────────
elif st.session_state.page == "ℹ️ College Info":
    st.markdown("""
    <div class="gprec-header">
        <h1>ℹ️ About GPREC</h1>
        <p>G. Pulla Reddy Engineering College (Autonomous), Kurnool</p>
    </div>
    """, unsafe_allow_html=True)

    info = api_get("/campus/college-info")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### 🏫 College Overview")
        if info:
            for label, key in [("📛 Full Name", "name"), ("📅 Established", "established"),
                                ("📍 Location", "location"), ("🎓 Affiliated To", "affiliated_to"),
                                ("🌐 Website", "website"), ("📞 Contact", "contact"),
                                ("✉️ Email", "email"), ("🏅 Accreditation", "accreditation"),
                                ("👥 Total Strength", "total_strength")]:
                st.markdown(f"**{label}:** {info.get(key, 'N/A')}")
        else:
            st.markdown("""
            **📛 Full Name:** G. Pulla Reddy Engineering College (Autonomous)  
            **📅 Established:** 1997  
            **📍 Location:** Kurnool, Andhra Pradesh  
            **🎓 Affiliated To:** JNTUA  
            **🌐 Website:** www.gprec.ac.in  
            **📞 Contact:** 08518-220010  
            **🏅 Accreditation:** NAAC A+ Grade, NBA Accredited  
            **👥 Total Strength:** ~4000 students  
            """)

    with col2:
        st.markdown("### 🏛️ Departments")
        depts = info.get("departments", ["CSE", "ECE", "EEE", "Mechanical", "Civil", "IT", "MBA", "MCA"]) if info else ["CSE", "ECE", "EEE", "Mechanical", "Civil", "IT", "MBA", "MCA"]
        for d in depts:
            st.markdown(f"• {d}")

        st.markdown("### 🏢 Facilities")
        facilities = info.get("facilities", []) if info else [
            "Central Library", "Boys & Girls Hostels", "Sports Complex",
            "Medical Center", "Canteen", "ATM", "Wi-Fi Campus"
        ]
        for f in facilities:
            st.markdown(f"• {f}")

    st.markdown("---")
    st.markdown("### 📊 Quick Facts")
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown('<div class="metric-card"><h3>25+</h3><p>Years of Excellence</p></div>', unsafe_allow_html=True)
    with c2:
        st.markdown('<div class="metric-card"><h3>4000+</h3><p>Students</p></div>', unsafe_allow_html=True)
    with c3:
        st.markdown('<div class="metric-card"><h3>200+</h3><p>Faculty Members</p></div>', unsafe_allow_html=True)
    with c4:
        st.markdown('<div class="metric-card"><h3>A+</h3><p>NAAC Grade</p></div>', unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("""
    ### 📞 Contact Information
    | Department | Contact |
    |---|---|
    | Main Office | 08518-220010 |
    | Placement Cell | 08518-220011 |
    | Library | 08518-220012 |
    | Exam Cell | 08518-220013 |
    | Hostels | 08518-220014 |
    """)
