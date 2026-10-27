import io
import re
from datetime import date, timedelta

import pandas as pd
import streamlit as st

# ============================================================
# 1. PAGE SETUP AND DESIGN
# ============================================================

st.set_page_config(
    page_title="WorkplaceFix AI",
    page_icon="🧭",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
.stApp {
    background: #F4F7FB;
    color: #1B2D45;
}
.block-container {
    max-width: 1450px;
    padding-top: 1.5rem;
    padding-bottom: 3rem;
}
[data-testid="stSidebar"] {
    background: #EAF1FA;
    border-right: 1px solid #D8E3F0;
}
[data-testid="stSidebar"] * {
    color: #203653;
}
.hero {
    background: linear-gradient(120deg, #163B70, #3479BD);
    padding: 28px 30px;
    border-radius: 18px;
    margin-bottom: 22px;
}
.hero h1 {
    color: white !important;
    font-size: 34px;
    margin: 0;
}
.hero p {
    color: #EAF3FF !important;
    font-size: 16px;
    margin: 8px 0 0;
}
.section-card {
    background: white;
    padding: 18px;
    border: 1px solid #DCE5F0;
    border-radius: 14px;
    min-height: 125px;
}
[data-testid="stMetric"] {
    background: white;
    padding: 16px;
    border: 1px solid #DCE5F0;
    border-radius: 14px;
}
[data-testid="stMetricLabel"] {
    color: #526780 !important;
}
[data-testid="stMetricValue"] {
    color: #173D73 !important;
}
.stButton > button,
.stDownloadButton > button {
    background: #245AA5 !important;
    color: white !important;
    border: 1px solid #245AA5 !important;
    border-radius: 9px !important;
    font-weight: 600 !important;
    transition: background 0.2s ease;
}
.stButton > button:hover,
.stDownloadButton > button:hover {
    background: #173D73 !important;
    color: white !important;
    border-color: #173D73 !important;
}
.stButton > button:focus,
.stDownloadButton > button:focus {
    color: white !important;
    box-shadow: 0 0 0 2px #9BC4F5 !important;
}
/* Slider styling matching the primary palette */
div[data-baseweb="slider"] div {
    background-color: #245AA5 !important;
}
[data-testid="stFileUploader"] {
    background: white;
    border: 1px dashed #8BA9D0;
    border-radius: 12px;
    padding: 12px;
}
h1, h2, h3 {
    color: #173D73;
}
hr {
    border-color: #DCE5F0;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hero">
    <h1>🧭 WorkplaceFix AI</h1>
    <p>From employee feedback to practical workplace improvements</p>
</div>
""", unsafe_allow_html=True)

st.write(
    "Understand recurring workplace concerns, inspect the feedback behind "
    "them, and turn the findings into an action plan."
)

# ============================================================
# 2. ARTICLE'S FOUR-FACTOR MODEL
# ============================================================

st.header("Understand job satisfaction")

st.write(
    "The article highlights four factors that shape job satisfaction: "
    "what we do, how much we earn, where we work, and who we work with."
)

factor_columns = st.columns(2)

factor_cards = [
    (
        "💼 What you do",
        "Meaningful tasks, interesting work, learning and career development."
    ),
    (
        "💰 How much you earn",
        "Fair salary, benefits, compensation and recognition."
    ),
    (
        "🏢 Where you work",
        "Work environment, workload, job security and work-life balance."
    ),
    (
        "🤝 Who you work with",
        "Colleagues, management, trust, communication and workplace culture."
    ),
]

for i, (heading, description) in enumerate(factor_cards):
    with factor_columns[i % 2]:
        st.markdown(
            f"""
            <div class="section-card">
                <h3>{heading}</h3>
                <p>{description}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    if i == 1:
        factor_columns = st.columns(2)

# ============================================================
# 3. PERSONAL SELF-ASSESSMENT
# ============================================================

st.divider()
st.header("Your job-satisfaction self-assessment")

st.caption(
    "Rate each factor from 1 (very dissatisfied) to 5 (very satisfied). "
    "This is a personal reflection tool, not a validated psychological test."
)

c1, c2 = st.columns(2)

with c1:
    work_rating = st.slider("What you do", 1, 5, 3, key="self_work")
    pay_rating = st.slider("How much you earn", 1, 5, 3, key="self_pay")

with c2:
    environment_rating = st.slider(
        "Where you work", 1, 5, 3, key="self_environment"
    )
    people_rating = st.slider(
        "Who you work with", 1, 5, 3, key="self_people"
    )

assessment = pd.DataFrame({
    "Factor": [
        "What you do",
        "How much you earn",
        "Where you work",
        "Who you work with",
    ],
    "Rating": [
        work_rating,
        pay_rating,
        environment_rating,
        people_rating,
    ],
})

average_rating = assessment["Rating"].mean()
lowest_rating = assessment["Rating"].min()
lowest_factors = assessment.loc[
    assessment["Rating"] == lowest_rating, "Factor"
].tolist()

m1, m2 = st.columns(2)
m1.metric("Your average rating", f"{average_rating:.1f} / 5")
m2.metric("Lowest factor rating", f"{lowest_rating} / 5")

st.bar_chart(assessment.set_index("Factor"))

st.info(
    "Reflection point: "
    + ", ".join(lowest_factors)
    + ". Consider what changes might improve these areas. "
    "These ratings do not establish the cause of a problem."
)

# ============================================================
# 4. THEME DEFINITIONS AND RECOMMENDATIONS
# ============================================================

THEMES = {
    "Salary & benefits": [
        "salary", "pay", "compensation", "benefit", "increment",
        "wage", "underpaid", "bonus", "low pay"
    ],
    "Work-life balance": [
        "work life", "work-life", "weekend", "overtime",
        "long hours", "leave", "personal life", "burnout",
        "flexible hours"
    ],
    "Workload & staffing": [
        "workload", "work load", "pressure", "overwork",
        "short staff", "understaffed", "too much work",
        "heavy workload", "too many tasks", "staffing"
    ],
    "Management & communication": [
        "management", "manager", "boss", "communication",
        "micromanagement", "leadership", "unclear instructions",
        "poor communication"
    ],
    "Career growth": [
        "promotion", "career growth", "career", "appraisal",
        "advancement", "growth", "progression", "promotion process"
    ],
    "Workplace culture & relationships": [
        "culture", "colleague", "coworker", "team",
        "supportive", "toxic", "politics", "respect",
        "trust", "bullying", "harassment", "relationship"
    ],
    "Job security": [
        "job security", "layoff", "termination", "fired",
        "job safety", "resign", "redundancy", "uncertain future"
    ],
    "Meaningful work & development": [
        "meaningful", "learning", "skill", "training",
        "purpose", "innovation", "interesting work",
        "development", "boring work"
    ],
}

FACTOR_MAP = {
    "What you do": [
        "Meaningful work & development",
        "Career growth",
        "Workload & staffing",
    ],
    "How much you earn": [
        "Salary & benefits",
    ],
    "Where you work": [
        "Work-life balance",
        "Job security",
    ],
    "Who you work with": [
        "Management & communication",
        "Workplace culture & relationships",
    ],
}

ACTIONS = {
    "Salary & benefits": {
        "action": "Review pay and benefits",
        "first_step": (
            "Compare pay bands with relevant market information and "
            "explain how compensation reviews work."
        ),
        "owner": "HR / leadership",
        "days": 30,
        "measure": "Review the clarity of pay policies and compensation processes.",
        "limitation": "Salary changes require budget and fairness checks.",
    },
    "Work-life balance": {
        "action": "Review working hours and leave",
        "first_step": (
            "Review overtime patterns, leave access and work scheduling."
        ),
        "owner": "Team manager / HR",
        "days": 21,
        "measure": "Track overtime and leave use before and after changes.",
        "limitation": "Changing a policy alone may not solve staffing problems.",
    },
    "Workload & staffing": {
        "action": "Review workload distribution",
        "first_step": (
            "Identify peak periods, repeated tasks and work that can be "
            "simplified before deciding whether more staff are needed."
        ),
        "owner": "Team manager",
        "days": 21,
        "measure": "Review workload distribution and deadline pressure.",
        "limitation": "Staffing decisions need operational and budget evidence.",
    },
    "Management & communication": {
        "action": "Improve communication practices",
        "first_step": (
            "Introduce regular team updates, clearer decisions and "
            "accessible feedback channels."
        ),
        "owner": "Team manager / HR",
        "days": 21,
        "measure": "Ask employees whether expectations and decisions are clearer.",
        "limitation": "Training alone may not resolve structural issues.",
    },
    "Career growth": {
        "action": "Clarify career paths",
        "first_step": (
            "Explain role expectations, appraisal criteria, skill development "
            "and promotion timelines."
        ),
        "owner": "HR / team leads",
        "days": 30,
        "measure": "Check whether employees can understand the career criteria.",
        "limitation": "Clearer criteria do not guarantee available promotions.",
    },
    "Workplace culture & relationships": {
        "action": "Support respectful workplaces",
        "first_step": (
            "Set behaviour expectations and provide appropriate channels "
            "for raising concerns."
        ),
        "owner": "HR / trained contact",
        "days": 30,
        "measure": "Review whether reporting channels are known and accessible.",
        "limitation": "Protect confidentiality and follow proper procedures.",
    },
    "Job security": {
        "action": "Improve change communication",
        "first_step": (
            "Explain organisational changes, relevant timelines and "
            "available employee support where possible."
        ),
        "owner": "Leadership / HR",
        "days": 30,
        "measure": "Check whether employees understand announced changes.",
        "limitation": "Communication cannot remove genuine business uncertainty.",
    },
    "Meaningful work & development": {
        "action": "Improve learning and task clarity",
        "first_step": (
            "Connect training to job needs and give employees opportunities "
            "to discuss their tasks and skills."
        ),
        "owner": "Team manager / learning team",
        "days": 30,
        "measure": "Review training relevance and opportunities to apply skills.",
        "limitation": "Training is useful only when relevant opportunities exist.",
    },
}

# ============================================================
# 5. SAMPLE DATA
# ============================================================

DEMO = pd.DataFrame([
    {
        "feedback": "Salary increments are low and benefits are unclear.",
        "overall_rating": 2,
        "department": "Operations",
    },
    {
        "feedback": "Friendly teammates, but overtime and weekend work affect my personal life.",
        "overall_rating": 3,
        "department": "Operations",
    },
    {
        "feedback": "Too much workload and not enough staff during busy periods.",
        "overall_rating": 2,
        "department": "Customer support",
    },
    {
        "feedback": "Management communicates changes poorly and instructions are unclear.",
        "overall_rating": 2,
        "department": "Sales",
    },
    {
        "feedback": "I worry about job security after recent company changes.",
        "overall_rating": 2,
        "department": "Technology",
    },
    {
        "feedback": "Promotion criteria and career growth opportunities are unclear.",
        "overall_rating": 3,
        "department": "Technology",
    },
    {
        "feedback": "Supportive colleagues and a helpful manager.",
        "overall_rating": 4,
        "department": "Sales",
    },
    {
        "feedback": "Meaningful tasks and useful training, but leave is difficult to take.",
        "overall_rating": 3,
        "department": "Customer support",
    },
    {
        "feedback": "I feel trusted by my manager and enjoy learning new skills.",
        "overall_rating": 5,
        "department": "Technology",
    },
    {
        "feedback": "Workplace politics and disrespectful behaviour make teamwork difficult.",
        "overall_rating": 1,
        "department": "Operations",
    },
])

# ============================================================
# 6. DATA PREPARATION AND ANALYSIS FUNCTIONS
# ============================================================

def find_text_columns(df):
    preferred = [
        "feedback", "comments", "comment", "review", "reviews",
        "text", "dislikes", "likes", "employee_feedback",
        "response", "open_text",
    ]

    lower_to_actual = {str(c).strip().lower(): c for c in df.columns}
    found = [lower_to_actual[x] for x in preferred if x in lower_to_actual]

    if found:
        return list(dict.fromkeys(found))

    excluded = {
        "name", "employee_name", "id", "employee_id",
        "department", "date", "title", "place", "job_type",
    }

    return [
        c for c in df.columns
        if df[c].dtype == "object"
        and str(c).lower() not in excluded
    ]


def prepare_feedback(df):
    if df is None or df.empty:
        raise ValueError(
            "The CSV has no rows. Upload a file containing feedback records."
        )

    df = df.copy()
    df.columns = [str(c).strip() for c in df.columns]

    text_columns = find_text_columns(df)

    if not text_columns:
        raise ValueError(
            "No feedback text column was found. Use a column such as "
            "feedback, comments, review, text, Likes or Dislikes."
        )

    df["_feedback"] = (
        df[text_columns]
        .fillna("")
        .astype(str)
        .agg(" | ".join, axis=1)
        .str.strip(" |")
    )

    df = df[df["_feedback"].str.strip().ne("")].copy()

    if df.empty:
        raise ValueError(
            "The selected text columns contain no non-empty feedback."
        )

    return df, text_columns


def detect_themes(text):
    text = str(text).lower()
    found = []

    for theme, keywords in THEMES.items():
        for keyword in keywords:
            pattern = r"(?<!\w)" + re.escape(keyword) + r"(?!\w)"
            if re.search(pattern, text):
                found.append(theme)
                break

    return found or ["Other / unclear"]


def run_analysis(df):
    data, text_columns = prepare_feedback(df)
    rows = []

    for index, row in data.iterrows():
        for theme in detect_themes(row["_feedback"]):
            rows.append({
                "record_id": str(index),
                "theme": theme,
                "feedback_excerpt": row["_feedback"][:500],
            })

    details = pd.DataFrame(
        rows,
        columns=["record_id", "theme", "feedback_excerpt"],
    )

    counts = (
        details.groupby("theme")["record_id"]
        .nunique()
        .reset_index(name="records_mentioning_theme")
        .sort_values("records_mentioning_theme", ascending=False)
    )

    counts["percentage_of_records"] = (
        counts["records_mentioning_theme"] / len(data) * 100
    ).round(1)

    return data, details, counts, text_columns


def build_recommendations(counts):
    recommendations = []

    for _, row in counts.iterrows():
        theme = row["theme"]

        if theme not in ACTIONS:
            continue

        action = ACTIONS[theme]

        recommendations.append({
            "Theme": theme,
            "Records mentioning theme": int(
                row["records_mentioning_theme"]
            ),
            "Share of records (%)": float(
                row["percentage_of_records"]
            ),
            "Suggested action": action["action"],
            "First step": action["first_step"],
            "Suggested owner": action["owner"],
            "Suggested timeframe": f"Within {action['days']} days",
            "How to review progress": action["measure"],
            "Limitation": action["limitation"],
        })

    return pd.DataFrame(recommendations)


def numeric_rating_summary(data):
    possible = [
        c for c in data.columns
        if any(term in c.lower() for term in ["rating", "score", "satisfaction"])
    ]

    results = []

    for column in possible:
        values = pd.to_numeric(data[column], errors="coerce").dropna()

        if not values.empty:
            results.append({
                "Rating field": column,
                "Responses": len(values),
                "Average": round(values.mean(), 2),
                "Median": round(values.median(), 2),
            })

    return pd.DataFrame(results)


# ============================================================
# 7. CHOOSE DATA SOURCE AND PREVIEW BEFORE ANALYSIS
# ============================================================

st.sidebar.title("📂 Feedback data")

source = st.sidebar.radio(
    "Choose a data source",
    ["Built-in demo data", "Upload a CSV"],
)

st.sidebar.caption(
    "Demo records are fictional. Remove names and identifiers "
    "before uploading real feedback."
)

if source == "Built-in demo data":
    raw_data = DEMO.copy()
else:
    uploaded_file = st.sidebar.file_uploader(
        "Upload anonymised employee feedback",
        type=["csv"],
        help=(
            "CSV needs at least one text column such as feedback, "
            "comments, review, Likes or Dislikes."
        ),
    )

    if uploaded_file is None:
        st.subheader("Start with your feedback file")
        st.info(
            "1. Upload a CSV in the sidebar.\n\n"
            "2. Preview its rows and columns.\n\n"
            "3. Click **Analyse feedback** to generate findings."
        )
        st.stop()

    try:
        raw_data = pd.read_csv(uploaded_file)
    except Exception as error:
        st.error(
            f"Could not read this CSV: {error}. "
            "Check that it is a valid comma-separated file."
        )
        st.stop()

st.divider()
st.header("Step 1 — Check your data")

p1, p2, p3 = st.columns(3)
p1.metric("Rows loaded", f"{len(raw_data):,}")
p2.metric("Columns found", f"{len(raw_data.columns):,}")
p3.metric("Empty cells", f"{int(raw_data.isna().sum().sum()):,}")

with st.expander(
    "Preview first 10 rows and column names",
    expanded=(source == "Upload a CSV"),
):
    st.write("**Columns:** " + ", ".join(map(str, raw_data.columns)))
    st.dataframe(
        raw_data.head(10),
        use_container_width=True,
        hide_index=True,
    )

if source == "Upload a CSV":
    st.caption(
        "Your file is previewed first. Analysis starts only after you click the button."
    )

    if not st.button(
        "🔎 Analyse feedback",
        type="primary",
        use_container_width=True,
    ):
        st.info("Check the preview, then click **Analyse feedback** when ready.")
        st.stop()

# ============================================================
# 8. RUN ANALYSIS
# ============================================================

try:
    data, details, counts, used_columns = run_analysis(raw_data)
except ValueError as error:
    st.error(str(error))
    st.stop()

ratings = numeric_rating_summary(data)
recommendations = build_recommendations(counts)

st.success(
    f"Analysis complete: {len(data):,} feedback records processed."
)

st.caption(
    f"Data source: {source} · "
    f"Text columns used: {', '.join(used_columns)}"
)

# ============================================================
# 9. DASHBOARD OVERVIEW
# ============================================================

st.divider()
st.header("Step 2 — Understand the findings")

mapped = recommendations[recommendations["Theme"] != "Other / unclear"]

if not mapped.empty:
    top = mapped.iloc[0]
    top_theme = top["Theme"]
    top_count = int(top["Records mentioning theme"])
    top_share = float(top["Share of records (%)"])
else:
    top_theme = "No mapped theme"
    top_count = 0
    top_share = 0.0

k1, k2, k3, k4 = st.columns(4)

k1.metric("Feedback records", f"{len(data):,}")
k2.metric("Themes found", f"{counts['theme'].nunique():,}")
k3.metric("Most-mentioned theme", top_theme)
k4.metric("Records mentioning it", f"{top_count} ({top_share:.1f}%)")

st.caption(
    "A record may mention multiple themes. Counts describe this dataset only; "
    "they do not prove causes or represent all employees."
)

left, right = st.columns([1.15, 1])

with left:
    st.subheader("Recurring workplace concerns")

    chart_data = counts.set_index("theme")["records_mentioning_theme"]
    st.bar_chart(chart_data.sort_values())

    st.dataframe(
        counts.rename(columns={
            "theme": "Theme",
            "records_mentioning_theme": "Records",
            "percentage_of_records": "Share of records (%)",
        }),
        use_container_width=True,
        hide_index=True,
    )

with right:
    st.subheader("Ratings in your data")

    if ratings.empty:
        st.info(
            "No numeric rating or score column was recognised. "
            "Theme analysis still works without ratings."
        )
    else:
        st.dataframe(
            ratings,
            use_container_width=True,
            hide_index=True,
        )
        st.caption(
            "Check the scale and meaning of each rating before interpreting it."
        )

# ============================================================
# 10. CONNECT RESULTS TO THE ARTICLE
# ============================================================

st.divider()
st.header("Step 3 — Connect findings to the article's four factors")

factor_rows = []

for factor, related_themes in FACTOR_MAP.items():
    matched_details = details[
        details["theme"].isin(related_themes)
    ]

    number_of_records = (
        matched_details["record_id"].nunique()
        if not matched_details.empty else 0
    )

    factor_rows.append({
        "Article factor": factor,
        "Related themes": ", ".join(related_themes),
        "Records mentioning related themes": number_of_records,
    })

factor_summary = pd.DataFrame(factor_rows)

st.dataframe(
    factor_summary,
    use_container_width=True,
    hide_index=True,
)

st.caption(
    "These are keyword-based links to the article's model, "
    "not validated satisfaction scores."
)

# Highlight central article takeaway
st.info(
    "💡 **Key Takeaway from Article:** *'People will always come first.'* "
    "High compensation cannot balance out toxic dynamic or workplace trust issues, "
    "whereas strong team relationships can make challenging work meaningful."
)

# ============================================================
# 11. INSPECT THE EVIDENCE
# ============================================================

st.divider()
st.header("Step 4 — Inspect employee feedback")

theme_options = counts["theme"].tolist()

selected_theme = st.selectbox(
    "Filter feedback examples by theme",
    ["All themes"] + theme_options,
)

if selected_theme == "All themes":
    selected_details = details.drop_duplicates("record_id")
else:
    selected_details = details[
        details["theme"] == selected_theme
    ].drop_duplicates("record_id")

if selected_details.empty:
    st.info("No matching feedback examples were found.")
else:
    for _, item in selected_details.head(15).iterrows():
        with st.expander(
            f"Record {item['record_id']} · {item['theme']}"
        ):
            st.write(item["feedback_excerpt"])

# ============================================================
# 12. RECOMMENDATIONS AND ACTION PLAN
# ============================================================

st.divider()
st.header("Step 5 — Turn findings into actions")

st.write(
    "These suggestions are starting points. Review the comments and "
    "discuss the findings with employees before deciding what to implement."
)

if recommendations.empty:
    st.info(
        "No mapped themes were detected. Review the feedback examples "
        "or add relevant keywords to the theme dictionary."
    )
else:
    for _, item in recommendations.iterrows():
        with st.expander(
            f"{item['Theme']} · {item['Records mentioning theme']} records"
        ):
            st.markdown(f"**Suggested action:** {item['Suggested action']}")
            st.markdown(f"**First step:** {item['First step']}")
            st.markdown(f"**Possible owner:** {item['Suggested owner']}")
            st.markdown(f"**Suggested timeframe:** {item['Suggested timeframe']}")
            st.markdown(f"**How to review progress:** {item['How to review progress']}")
            st.warning(f"**Limitation:** {item['Limitation']}")

    st.subheader("Create your action tracker")

    selected_actions = st.multiselect(
        "Select concerns for your action plan",
        options=recommendations["Theme"].tolist(),
        default=recommendations["Theme"].head(
            min(3, len(recommendations))
        ).tolist(),
    )

    coordinator = st.text_input(
        "Team coordinating the plan",
        value="Workplace improvement team",
    )

    start_date = st.date_input(
        "Plan start date",
        value=date.today(),
    )

    tracker_rows = []

    for _, item in recommendations[
        recommendations["Theme"].isin(selected_actions)
    ].iterrows():
        action_info = ACTIONS[item["Theme"]]

        tracker_rows.append({
            "Theme": item["Theme"],
            "Records mentioning theme": item["Records mentioning theme"],
            "Suggested action": item["Suggested action"],
            "First step": item["First step"],
            "Suggested owner": item["Suggested owner"],
            "Coordinator": coordinator,
            "Target date": (
                start_date + timedelta(days=action_info["days"])
            ).isoformat(),
            "Status": "Not started",
            "Progress measure": item["How to review progress"],
            "Review notes": "",
        })

    tracker = pd.DataFrame(tracker_rows)

    if not tracker.empty:
        st.caption(
            "Edit the owner, target date, status and notes to suit your workplace."
        )

        edited_tracker = st.data_editor(
            tracker,
            use_container_width=True,
            hide_index=True,
            num_rows="fixed",
            key="action_tracker_editor",
        )
    else:
        edited_tracker = pd.DataFrame()
        st.info("Select one or more themes to create an action tracker.")

# ============================================================
# 13. DOWNLOAD RESULTS (WITH SAFE FALLBACK)
# ============================================================

st.divider()
st.header("Step 6 — Download your report")

st.write(
    "Download the findings for a workplace discussion. "
    "Check for confidential or identifying details before sharing."
)

report = io.BytesIO()
excel_available = True

try:
    with pd.ExcelWriter(report, engine="openpyxl") as writer:
        counts.to_excel(writer, sheet_name="Theme Counts", index=False)
        factor_summary.to_excel(writer, sheet_name="Four Factors", index=False)

        if not ratings.empty:
            ratings.to_excel(writer, sheet_name="Rating Summary", index=False)

        if not recommendations.empty:
            recommendations.to_excel(
                writer,
                sheet_name="Recommendations",
                index=False,
            )

        details.to_excel(
            writer,
            sheet_name="Feedback Mapping",
            index=False,
        )

        if "edited_tracker" in locals() and not edited_tracker.empty:
            edited_tracker.to_excel(
                writer,
                sheet_name="Action Tracker",
                index=False,
            )
except Exception:
    excel_available = False

d1, d2 = st.columns(2)

with d1:
    st.download_button(
        "⬇ Download theme summary (CSV)",
        data=counts.to_csv(index=False).encode("utf-8-sig"),
        file_name="workplacefix_theme_summary.csv",
        mime="text/csv",
        use_container_width=True,
    )

with d2:
    if excel_available:
        st.download_button(
            "⬇ Download full report (Excel)",
            data=report.getvalue(),
            file_name="workplacefix_workplace_report.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True,
        )
    else:
        st.button(
            "⚠️ Excel generation unavailable (openpyxl missing)",
            disabled=True,
            use_container_width=True,
        )

# ============================================================
# 14. PRIVACY, EVIDENCE AND LIMITATIONS
# ============================================================

st.divider()
st.header("Privacy and limitations")

st.markdown("""
- **What this tool is for:** spotting recurring topics, reviewing example comments,
  connecting concerns to the article's four factors and organising possible next steps.
- **How themes are found:** transparent keyword rules, not a trained AI model.
  The tool may miss synonyms, context, sarcasm and negation.
- **How counts work:** one feedback record may match several themes, so percentages
  may add up to more than 100%.
- **What the results mean:** findings describe only the data provided. They do not
  prove causes or represent every employee.
- **Responsible use:** do not use these results to rank, discipline or penalise
  individual employees. Review findings with appropriate workplace context.
- **Privacy:** remove names, emails, employee IDs and other identifying details
  before uploading. Upload only data you are authorised to use.
- **Demo data:** the built-in examples are fictional and are provided to demonstrate
  the workflow.
""")