# fitness_tracker_dashboard.py

import streamlit as st
import mysql.connector
import datetime
import pandas as pd
import plotly.graph_objects as go
import random



# Database connection
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="your_root_password", # enter your root password
    database="your_db_name" # enter your database name
)
cursor = conn.cursor()

# Calorie data
calories_per_minute = {
    "Running": {"Male": 11, "Female": 9},
    "Cycling": {"Male": 10, "Female": 8},
    "Swimming": {"Male": 8, "Female": 6},
    "Jump Rope": {"Male": 12, "Female": 10},
    "Yoga": {"Male": 4, "Female": 3},
    "Weight Lifting": {"Male": 8, "Female": 6}
}

# Registration
def register():
    st.subheader("📝 Register")
    with st.form("register_form"):
        name = st.text_input("Name")
        age = st.number_input("Age", min_value=10, max_value=100, step=1)
        weight = st.number_input("Weight (kg)", min_value=20.0, step=0.1)
        height = st.number_input("Height (cm)", min_value=100.0, step=0.1)
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        gender = st.selectbox("Gender", ["Male", "Female"])
        submit = st.form_submit_button("Register")

        if submit:
            height_m = height / 100
            bmi = weight / (height_m ** 2)
            bmi = round(bmi, 2)

            if bmi < 18.5:
                category = "Underweight"
            elif 18.5 <= bmi <= 24.9:
                category = "Normal weight"
            elif 25 <= bmi <= 29.9:
                category = "Over weight"
            else:
                category = "Obese"

            cursor.execute("INSERT INTO users (name, age, weight, height, username, password, gender, bmi, category) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                           (name, age, weight, height, username, password, gender, bmi, category))
            conn.commit()
            st.success(f"✅ Registered successfully! Your BMI is {bmi} ({category}).")

# Login
def login():
    st.subheader("🔐 Login")
    username = st.text_input("Username", key="login_user")
    password = st.text_input("Password", type="password", key="login_pass")
    if st.button("Login"):
        cursor.execute("SELECT id, gender FROM users WHERE username=%s AND password=%s", (username, password))
        user = cursor.fetchone()
        if user:
            st.session_state.user_id = user[0]
            st.session_state.gender = user[1]
            st.success("✅ Login successful!")
        else:
            st.error("❌ Invalid credentials.")

# Update Profile
def update_profile(user_id):
    st.subheader("👤 Update Profile")
    cursor.execute("SELECT name, age, weight, height, password FROM users WHERE id = %s", (user_id,))
    user = cursor.fetchone()

    if user:
        name, age, weight, height, password = user

        with st.form("update_form"):
            new_name = st.text_input("Name", value=name)
            new_age = st.number_input("Age", min_value=10, max_value=100, value=age)
            new_weight = st.number_input("Weight (kg)", min_value=20.0, step=0.1, value=weight)
            new_height = st.number_input("Height (cm)", min_value=100.0, step=0.1, value=height)
            new_password = st.text_input("Password", type="password", value=password)
            submit = st.form_submit_button("Update Profile")

            if submit:
                height_m = new_height / 100
                bmi = new_weight / (height_m ** 2)
                bmi = round(bmi, 2)

                if bmi < 18.5:
                    category = "Underweight"
                elif 18.5 <= bmi <= 24.9:
                    category = "Normal weight"
                elif 25 <= bmi <= 29.9:
                    category = "Over weight"
                else:
                    category = "Obese"

                cursor.execute("""
                    UPDATE users 
                    SET name=%s, age=%s, weight=%s, height=%s, password=%s, bmi=%s, category=%s 
                    WHERE id=%s
                """, (new_name, new_age, new_weight, new_height, new_password, bmi, category, user_id))
                conn.commit()
                st.success("✅ Profile updated successfully!")

# Daily tips
def daily_tip():
    tips = [
        "Stay hydrated 💧",
        "Stretch before and after workouts 🧘",
        "Eat balanced meals 🍎",
        "Consistency is key 🔑",
        "Get 7-8 hours of sleep 😴",
        "Track your progress weekly 📊",
        "Avoid skipping warm-ups 🚶",
        "Don’t neglect rest days 🛌"
    ]
    tip = random.choice(tips)
    st.markdown("### 💡 Daily Fitness Tip")
    st.info(f"{tip}")

# Log Workout
def add_workout(user_id, gender):
    st.subheader("🏋️ Log Workout")
    daily_tip()
    with st.form("workout_form"):
        exercise = st.selectbox("Select Exercise", list(calories_per_minute.keys()))
        duration = st.number_input("Duration (in minutes)", min_value=1)
        submit = st.form_submit_button("Log Workout")

        if submit:
            date = datetime.date.today()
            calories = calories_per_minute[exercise][gender] * duration
            cursor.execute("INSERT INTO workouts (user_id, date, exercise, duration, calories_burned) VALUES (%s,%s,%s,%s,%s)",
                           (user_id, date, exercise, duration, calories))
            conn.commit()
            st.success(f"✅ Workout logged successfully! You burned {calories} calories.")

# View Progress
import pandas as pd
import streamlit as st
import io


def view_progress(user_id):
    st.subheader("📈 Progress Tracker")

    cursor.execute("SELECT date, exercise, duration, calories_burned FROM workouts WHERE user_id=%s ORDER BY date DESC", (user_id,))
    records = cursor.fetchall()

    if records:
        # Display in Streamlit
        for record in records:
            st.markdown(f"📅 **Date**: {record[0]}, 🏃‍♂️ **Exercise**: {record[1]}, ⏱️ **Duration**: {record[2]} mins, 🔥 **Calories Burned**: {record[3]}")

        # Create DataFrame
        df = pd.DataFrame(records, columns=["Date", "Exercise", "Duration (mins)", "Calories Burned"])

        # Ensure Date is datetime (important for Excel formatting)
        df["Date"] = pd.to_datetime(df["Date"])

        # Write Excel file to memory
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter', datetime_format='yyyy-mm-dd') as writer:
            df.to_excel(writer, index=False, sheet_name='Progress')
            
            # Set formatting
            workbook  = writer.book
            worksheet = writer.sheets['Progress']
            
            # Set column widths and format
            date_format = workbook.add_format({'num_format': 'yyyy-mm-dd'})
            worksheet.set_column('A:A', 15, date_format)  # Date column
            worksheet.set_column('B:D', 25)  # Other columns

        output.seek(0)

        st.download_button(
            label="📥 Download Progress as Excel",
            data=output,
            file_name="fitness_progress.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    else:
        st.info("No workouts logged yet.")


# Set Goal
def set_goal(user_id):
    st.subheader("🎯 Set Fitness Goal")
    with st.form("goal_form"):
        goal_calories = st.number_input("Enter your calorie-burning goal", min_value=100)
        goal_days = st.number_input("Enter days to achieve goal", min_value=1)
        submit = st.form_submit_button("Set Goal")
        if submit:
            start_date = datetime.date.today()
            cursor.execute("INSERT INTO goals (user_id, goal_calories, goal_days, start_date) VALUES (%s,%s,%s,%s)",
                           (user_id, goal_calories, goal_days, start_date))
            conn.commit()
            st.success(f"Goal set! Burn {goal_calories} calories in {goal_days} days.")

# Track Goal
def track_goal(user_id):
    st.subheader("📊 Track Goal")
    cursor.execute("""
        SELECT goal_calories, goal_days, start_date, created_at 
        FROM goals 
        WHERE user_id = %s 
        ORDER BY created_at DESC 
        LIMIT 1
    """, (user_id,))
    goal = cursor.fetchone()

    if goal:
        goal_calories, goal_days, start_date, created_at = goal
        cursor.execute("""
            SELECT SUM(calories_burned) 
            FROM workouts 
            WHERE user_id = %s AND date >= %s
        """, (user_id, created_at.date()))
        total_burned = cursor.fetchone()[0] or 0
        st.markdown(f"🎯 **Goal**: Burn {goal_calories} calories in {goal_days} days (Set: {created_at.date()})")
        st.markdown(f"🔥 **Calories Burned Since Goal Set**: {total_burned}")
        if total_burned >= goal_calories:
            st.success("✅ Congratulations! You've achieved your goal 🎉")
        else:
            st.info("💪 Keep it up! You're making progress.")
    else:
        st.info("⚠️ No fitness goal set.")

# Daily reminder
def daily_reminder(user_id):
    cursor.execute("SELECT MAX(date) FROM workouts WHERE user_id = %s", (user_id,))
    last_date = cursor.fetchone()[0]
    today = datetime.date.today()
    if last_date != today:
        st.warning("⚠️ You haven't logged a workout today! Stay consistent 💪")


# Dashboard
def show_dashboard(user_id):
    st.title("📊 Dashboard")
    daily_reminder(user_id)
    # Line chart
    st.subheader("🗕️ This Week's Progress")
    today = datetime.date.today()
    week_ago = today - datetime.timedelta(days=6)
    cursor.execute("""
        SELECT date, SUM(calories_burned) 
        FROM workouts 
        WHERE user_id = %s AND date BETWEEN %s AND %s 
        GROUP BY date ORDER BY date ASC
    """, (user_id, week_ago, today))
    records = cursor.fetchall()
    df = pd.DataFrame(records, columns=["Date", "Calories"])
    df["Date"] = pd.to_datetime(df["Date"])
    df = df.set_index("Date").reindex(pd.date_range(week_ago, today), fill_value=0).rename_axis("Date").reset_index()
    st.line_chart(df.set_index("Date"))

    # Progress bar
    st.subheader("🌟 Goal Progress")
    cursor.execute("""
        SELECT goal_calories, start_date, created_at 
        FROM goals 
        WHERE user_id = %s 
        ORDER BY created_at DESC LIMIT 1
    """, (user_id,))
    goal = cursor.fetchone()
    if goal:
        goal_calories, start_date, created_at = goal
        cursor.execute("SELECT SUM(calories_burned) FROM workouts WHERE user_id = %s AND date >= %s", (user_id, created_at.date()))
        total = cursor.fetchone()[0] or 0
        progress = min(int((total / goal_calories) * 100), 100)
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=progress,
            title={'text': "Goal Progress"},
            gauge={'axis': {'range': [0, 100]}, 'bar': {'color': "green"}},
        ))
        st.plotly_chart(fig)

    with st.expander("🔍 Want more insights?"):
        option = st.selectbox("Select Insight", [
            "Workout Type Distribution", 
            "Calories Burned by Workout Type"
        ])
        if option == "Workout Type Distribution":
            cursor.execute("SELECT exercise, COUNT(*) FROM workouts WHERE user_id = %s GROUP BY exercise", (user_id,))
            data = cursor.fetchall()
            df = pd.DataFrame(data, columns=["Exercise", "Count"])
            st.bar_chart(df.set_index("Exercise"))
        elif option == "Calories Burned by Workout Type":
            cursor.execute("SELECT exercise, SUM(calories_burned) FROM workouts WHERE user_id = %s GROUP BY exercise", (user_id,))
            data = cursor.fetchall()
            df = pd.DataFrame(data, columns=["Exercise", "Calories"])
            st.bar_chart(df.set_index("Exercise"))
            
import streamlit as st
from chatbot import load_bot  # Update with the actual name if different

# Load the bot once
@st.cache_resource
def get_fitness_qa_chain():
    return load_bot()

def fitness_bot():
    st.subheader("💬 FitBot - Your AI Fitness Assistant")
    st.markdown("Ask me anything about workouts, diets, progress, or health tips!")

    user_query = st.text_input("Enter your question here:")

    if user_query:
        qa_chain = get_fitness_qa_chain()
        with st.spinner("Thinking..."):
            response = qa_chain.run(user_query)
        st.success("Here's what I found:")
        st.markdown(f"**🧠 FitBot:** {response}")

            

# UI START
st.title("🏃 Fitness Tracker App")

if "user_id" not in st.session_state:
    st.session_state.user_id = None
if "gender" not in st.session_state:
    st.session_state.gender = None

if st.session_state.user_id is None:
    st.sidebar.header("Welcome! 👋")
    option = st.sidebar.radio("Choose an option", ["Register", "Login"])
    if option == "Register":
        register()
    else:
        login()
else:
    st.sidebar.success("Logged in ✅")
    action = st.sidebar.radio("Navigate", ["Dashboard", "Log Workout", "View Progress", "Set Goal", "Track Goal", "Update Profile","FitBot AI Assistant", "Logout"])

    if action == "Dashboard":
        show_dashboard(st.session_state.user_id)
    elif action == "Log Workout":
        add_workout(st.session_state.user_id, st.session_state.gender)
    elif action == "View Progress":
        view_progress(st.session_state.user_id)
    elif action == "Set Goal":
        set_goal(st.session_state.user_id)
    elif action == "Track Goal":
        track_goal(st.session_state.user_id)
    elif action == "Update Profile":
        update_profile(st.session_state.user_id)
    elif action== "FitBot AI Assistant":
        fitness_bot()    
    elif action == "Logout":
        st.session_state.user_id = None
        st.session_state.gender = None
        st.success("Logged out successfully.")
