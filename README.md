
# 💪 FitVerse AI - Smart Fitness Tracker App

**FitVerse AI** is a smart, interactive fitness tracker built with **Streamlit** and **MySQL**, enhanced with a personalized **AI chatbot** for fitness guidance. The app helps users manage workouts, track goals, visualize progress, and receive customized health tips. Whether you're a beginner or fitness enthusiast, FitVerse AI empowers you to take control of your fitness journey.

## 📂 Assets 
- All screenshots of the application's features are available in the assets/ folder

## 🎥 Full Functionality Demo
- Watch the full project demo here: [Video Link](https://www.linkedin.com/posts/vishalini-k-148196272_ai-aichatbot-streamlit-activity-7333544838790828034-WAee?utm_source=share&utm_medium=member_desktop&rcm=ACoAAEKXLkgB2qBFMFjR53xem7E4j3dTDfyCo58)
  
## 🚀 Features

- 📝 **User Registration & Login**  
  Secure sign-up and login to maintain personal workout data.

- 🧮 **BMI Calculator with Health Category**  
  Instant BMI calculation with category classification (Underweight, Normal, Overweight, Obese).

- 🧑‍💻 **Profile Management**  
  Update your age, weight, height, gender, and password at any time.

- 🗣️ **AI Fitness Chatbot**  
  Integrated fitness chatbot that provides personalized answers on:
  - Workout routines
  - Diet plans
  - Weight management
  - Health tips and lifestyle improvements  
  (Trained on fitness data and responds naturally to user queries.)

- 📊 **Advanced Dashboard**  
  - Weekly workout charts
  - Calories burned visualizations
  - Goal tracking using a **Half Pie Chart**
  - Real-time login consistency alerts like:
    - ✅ *"You are consistently logging in daily!"*
    - ⚠️ *"Try to log in more consistently for better progress tracking!"*

- 🧘‍♂️ **Daily Fitness Tips**  
  Fresh health tips every time you log in to keep you motivated.

- 🏋️ **Workout Logging**  
  Record exercises, duration, and automatically calculate calories burned.

- 📈 **Progress Visualization**  
  - Line charts for calories burned per session
  - Downloadable Excel reports for further analysis

- 🎯 **Goal Setting & Tracker**  
  Set personalized goals and track your completion percentage via a visual goal tracker.

- ⏰ **Daily Workout Reminders**  
  Alerts if a day is missed, helping you build a habit of consistency.

---

## 🛠️ Tech Stack

- **Frontend:** Streamlit
- **Backend:** Python
- **Database:** MySQL
- **Visualization:** Plotly, Pandas
- **Excel Export:** XlsxWriter
- **AI Chatbot:** Custom-trained model (e.g., ChatterBot / Hugging Face / OpenAI)

---

## 📂 Project Structure

```
FitVerse_AI/
│
├── fitness_tracker_dashboard.py    # Main Streamlit app with chatbot & charts
├── requirements.txt                # List of dependencies
├── assets/                         # Screenshots and static files
└── README.md                       # Project documentation
```

---

## 🖼️ Screenshots

### 🔐 Login Page  
![assets/login.png](https://github.com/Vishalini06/Fitness_tracker_app_Streamlit/blob/fa8d099e3b0144212da426d9dadc100d5d0ac876/Fitness_tracker_app/assets/register.png)

### 📊 Dashboard with Charts  
- Weekly workout chart  
- Goal progress (half pie chart)  
- Login consistency messages  
![Image](https://github.com/user-attachments/assets/2e8d7dc8-813a-4d28-9c14-7d6912d02b19)

### 🤖 Chatbot  
Get smart answers to any fitness-related question  
![Image](https://github.com/user-attachments/assets/118fc442-2e26-4db8-af46-6c27fd7bc454)

---

## 💻 Setup Instructions

### ✅ Prerequisites

- Python 3.7+
- MySQL Server installed and running
- pip (Python package installer)

---

## 📥 Clone and Run on Your System

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/yourusername/fitverse-ai.git
cd fitverse-ai
```

### 2️⃣ Install Required Python Packages

```bash
pip install -r requirements.txt
```

### 3️⃣ MySQL Database Setup

1. Open MySQL and create the database:

```sql
CREATE DATABASE fitness_tracker;
USE fitness_tracker;
```

2. Create necessary tables:

```sql
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    age INT,
    weight FLOAT,
    height FLOAT,
    username VARCHAR(50) UNIQUE,
    password VARCHAR(100),
    gender VARCHAR(10),
    bmi FLOAT,
    category VARCHAR(50),
    last_login DATE
);

CREATE TABLE workouts (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    date DATE,
    exercise VARCHAR(50),
    duration INT,
    calories_burned INT,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE TABLE goals (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    goal_calories INT,
    goal_days INT,
    start_date DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);
```

> ✅ Make sure your `fitness_tracker_dashboard.py` file has the correct `MySQL` connection credentials (host, user, password, database name).

---

## ▶️ Run the Application

```bash
streamlit run fitness_tracker_dashboard.py
```

Then open the app in your browser at:  
`http://localhost:8501`

---

## ✨ Upcoming Enhancements

- 📧 Email notifications/reminders  
- 🗓️ Monthly progress and trends dashboard  

---
### Deployment
- Docker  
- Requirements.txt


## 🤝 Contributing

Feel free to fork, improve, and make pull requests. Suggestions to enhance the chatbot, add more visualizations, or improve UI/UX are always welcome!

---


## 🛠️ Crafted With Passion By

👩‍💻 Vishalini — Turning Ideas Into Impact.


