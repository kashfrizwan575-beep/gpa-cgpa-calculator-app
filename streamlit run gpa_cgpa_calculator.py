import streamlit as st

# --- Header ---
st.title("🎓 GPA & CGPA Calculator")
st.caption("Easily calculate GPA for each semester and overall CGPA.")

# --- Function: Convert Marks to Grade Points ---
def grade_point_from_marks(m):
    m = float(m)
    if m >= 85:
        return 4.0
    elif m >= 80:
        return 3.7
    elif m >= 75:
        return 3.3
    elif m >= 70:
        return 3.0
    elif m >= 65:
        return 2.7
    elif m >= 60:
        return 2.3
    elif m >= 55:
        return 2.0
    elif m >= 50:
        return 1.7
    else:
        return 0.0

# --- Function: Compute GPA for a semester ---
def compute_gpa(data):
    total_points = 0
    total_credits = 0
    for sub in data:
        total_credits += sub["credit"]
        total_points += sub["credit"] * sub["gp"]
    if total_credits == 0:
        return 0.0
    return round(total_points / total_credits, 2)

# --- Input: Number of Semesters ---
num_semesters = st.number_input("How many semesters do you want to calculate?", 1, 5, 1)

# --- Store GPAs ---
gpa_list = []
credit_list = []
points_list = []

# --- Loop through semesters ---
for sem in range(1, num_semesters + 1):
    st.subheader(f"Semester {sem}")
    subjects = st.number_input(f"Number of subjects in Semester {sem}", 1, 10, 5, key=f"subs_{sem}")
    data = []

    for i in range(1, subjects + 1):
        st.markdown(f"**Subject {i}**")
        col1, col2, col3 = st.columns(3)
        with col1:
            credit = st.number_input("Credit Hours", 0.5, 5.0, 3.0, 0.5, key=f"credit_{sem}_{i}")
        with col2:
            entry_type = st.selectbox("Input Type", ["Marks", "Grade Point"], key=f"type_{sem}_{i}")
        with col3:
            if entry_type == "Marks":
                marks = st.number_input("Marks (0–100)", 0.0, 100.0, key=f"marks_{sem}_{i}")
                gp = grade_point_from_marks(marks)
            else:
                gp = st.number_input("Grade Point (0–4.0)", 0.0, 4.0, key=f"gp_{sem}_{i}")
        data.append({"credit": credit, "gp": gp})

    if st.button(f"✅ Calculate GPA for Semester {sem}", key=f"calc_{sem}"):
        gpa = compute_gpa(data)
        total_credits = sum(d["credit"] for d in data)
        total_points = sum(d["credit"] * d["gp"] for d in data)
        gpa_list.append(gpa)
        credit_list.append(total_credits)
        points_list.append(total_points)
        st.success(f"GPA for Semester {sem}: **{gpa}**")

# --- CGPA Calculation ---
if st.button("🎯 Calculate Overall CGPA"):
    if not gpa_list:
        st.warning("Please calculate at least one semester GPA first.")
    else:
        total_points = sum(points_list)
        total_credits = sum(credit_list)
        cgpa = round(total_points / total_credits, 2) if total_credits > 0 else 0.0

        st.markdown("---")
        st.subheader("📘 Semester Summary")
        for i, gpa in enumerate(gpa_list, 1):
            st.write(f"Semester {i}: GPA = {gpa}")

        st.success(f"**Final CGPA = {cgpa}** 🎉")
