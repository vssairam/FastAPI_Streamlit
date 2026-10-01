import streamlit as st
import pandas as pd

# 1. Page Configuration for a clean, professional look
st.set_page_config(
    page_title="Student Grade Management System",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Custom CSS styling
st.markdown("""
    <style>
    .main-header {
        font-size: 2.2rem;
        font-weight: 700;
        color: #1E3A8A;
        text-align: center;
        margin-bottom: 1.5rem;
    }
    .stMetric {
        background-color: #F8FAFC;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        border: 1px solid #E2E8F0;
    }
    </style>
""", unsafe_allow_html=True)

# 3. Grade Calculation Function
def get_grade(mark):
    if mark >= 90:
        return 'A'
    elif mark >= 80:
        return 'B'
    elif mark >= 70:
        return 'C'
    elif mark >= 60:
        return 'D'
    else:
        return 'F'

# 4. Initialize session state to retain student records across reruns
if "students" not in st.session_state:
    st.session_state["students"] = []

# Title
st.markdown('<div class="main-header">🎓 Student Grade Management System</div>', unsafe_allow_html=True)

# 5. Sidebar Form for Data Input
st.sidebar.header("📝 Add Student Record")

with st.sidebar.form(key="student_form", clear_on_submit=True):
    name = st.text_input("Student Name", placeholder="e.g. John Doe")
    mark = st.number_input(
        "Mark (0 - 100)", 
        min_value=0.0, 
        max_value=100.0, 
        value=0.0, 
        step=1.0,
        format="%.2f"
    )
    submit_button = st.form_submit_button(label="Add Record")

# 6. Process Form Submission
if submit_button:
    clean_name = name.strip()
    if not clean_name:
        st.sidebar.error("⚠️️ Please enter a valid student name.")
    else:
        grade = get_grade(mark)
        st.session_state["students"].append({
            "Name": clean_name,
            "Mark": round(mark, 2),
            "Grade": grade
        })
        st.sidebar.success(f"Added record for **{clean_name}**!")

# 7. Main Dashboard Area
if not st.session_state["students"]:
    st.info("👋 Welcome! Use the sidebar form to add student records and view class analytics.")
else:
    df = pd.DataFrame(st.session_state["students"])

    # Summary Metrics
    class_avg = df["Mark"].mean()
    highest_mark = df["Mark"].max()
    lowest_mark = df["Mark"].min()

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric(label="Total Students", value=len(df))
    with col2:
        st.metric(label="Class Average", value=f"{class_avg:.2f}")
    with col3:
        st.metric(label="Highest Mark", value=f"{highest_mark:.2f}")
    with col4:
        st.metric(label="Lowest Mark", value=f"{lowest_mark:.2f}")

    st.markdown("---")

    # Data Table & Management
    col_table, col_actions = st.columns([3, 1])

    with col_table:
        st.subheader("📋 Student Records")
        st.dataframe(
            df, 
            use_container_width=True, 
            hide_index=True,
            column_config={
                "Name": st.column_config.TextColumn("Student Name"),
                "Mark": st.column_config.NumberColumn("Mark (0-100)", format="%.2f"),
                "Grade": st.column_config.TextColumn("Grade")
            }
        )

    with col_actions:
        st.subheader("⚙️ Actions")
        if st.button("🗑️ Clear All Records", use_container_width=True, type="primary"):
            st.session_state["students"] = []
            st.rerun()