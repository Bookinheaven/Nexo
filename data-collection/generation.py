import random
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from scipy.stats import beta, multivariate_normal
from scipy.special import erf
from sklearn.ensemble import RandomForestClassifier
import argparse

random.seed(42)
np.random.seed(42)

genders = ["Male", "Female"]
years = ["First Year", "Second Year", "Third Year", "Fourth Year", "Fifth Year", "Sixth Year"]
streams = [
    "School of Engineering & Technology",
    "School of Computer Science & Technology",
    "School of Agriculture",
    "School of Science, Arts & Media"
]
programs_et = [
    "Aerospace Engineering",
    "Aerospace Engineering (Spez in AI & ML)",
    "Biomedical Engineering",
    "Biotechnology",
    "Electrical & Electronics Engineering",
    "Electronics & Communication Engineering",
    "Mechanical Engineering",
    "Robotics & Automation",
    "Computer Science & Engineering",
    "Computer Science & Engineering (Spez in AI & ML)",
    "Computer Science & Engineering (Spez in Cyber Security)",
    "Computer Science & Engineering (Artificial Intelligence)",
    "Artificial Intelligence & Data Science",
    "Computer Engineering",
    "Computer Engineering (Spez in Cyber Security)"
]
programs_cst = [
    "Computer Science & Engineering",
    "Computer Science & Engineering (Spez in AI & ML)",
    "Computer Science & Engineering (Spez in Cyber Security)",
    "Computer Science & Engineering (Artificial Intelligence)",
    "Computer Science & Engineering (AI & ML)",
    "Artificial Intelligence & Data Science",
    "Computer Engineering",
    "Computer Engineering (Spez in Cyber Security)"
]
programs_agri = ["Agriculture (Hons) [B.Sc]"]
programs_sam = [
    "Forensic Science [B.Sc]",
    "Information Security & Digital Forensics [B.Sc]",
    "Media Production & Digital Marketing [B.Sc]",
    "Professional Accounting & Financial Technology [B.Com]"
]
stress_sources = [
    "Academic workload",
    "Exams / deadlines",
    "Social relationships",
    "Family responsibilities",
    "Financial concerns",
    "Career / job uncertainty",
    "Other"
]
time_management = ["Always", "Often", "Sometimes", "Rarely", "Never"]
sleep_hours = [
    "Less than 4 hours",
    "4 - 5 hours",
    "6 - 7 hours",
    "8 - 9 hours",
    "More than 9 hours"
]
exercise = ["Never", "1 - 2 times per week", "3 - 4 times per week", "5 - 6 times per week", "Daily"]
water_intake = ["Less than 3", "3 - 5", "6 - 8", "9"]
diet_quality = [
    "Very unhealthy",
    "Somewhat unhealthy",
    "Neutral / Average",
    "Healthy",
    "Very healthy"
]
mental_health = ["Very poor", "Poor", "Average", "Good", "Excellent"]
peer_support = ["Always", "Often", "Sometimes", "Rarely", "Never"]
counseling_access = ["Yes, always", "Sometimes", "Rarely", "No, not accessible"]
suggestions = [
    "Need to improve a lot of things",
    "Nothing",
    "Establish more counseling centers on campus",
    "It's better to leave the college",
    "Need to improve basic structure",
    "Need to look out juniors",
    "Introduce stress management workshops",
    "Reduce academic workload",
    "More extracurricular activities would help",
    "Better hostel food quality is needed",
    "Improve library resources and study spaces",
    "Organize regular fitness and wellness sessions",
    "More cultural fests to reduce stress",
    "Offer flexible exam schedules",
    "Encourage open conversations about mental health",
    "Upgrade classroom technology",
    "Provide more internship opportunities",
    "Enhance campus safety measures",
    "Improve Wi-Fi connectivity",
    "Increase mental health awareness events",
    "Expand career counseling services",
    "Bring in more visiting faculty",
    "Subsidize healthy meal plans",
    "Create student support groups",
    "Offer meditation or mindfulness sessions",
    "Improve sports/recreation facilities"
]

# Numeric maps for encoding
sleep_map = {v:i for i,v in enumerate(sleep_hours)}
time_map = {v:i for i,v in enumerate(time_management)}
diet_map = {v:i for i,v in enumerate(diet_quality)}
exercise_map = {v:i for i,v in enumerate(exercise)}
peer_map = {v:i for i,v in enumerate(peer_support)}
counseling_map = {v:i for i,v in enumerate(counseling_access)}
stress_list = [
    "1 - Not stressed at all",
    "2 - Slightly stressed",
    "3 - Moderately stressed",
    "4 - Very stressed",
    "5 - Extremely stressed"
]
stress_map = {v:i for i,v in enumerate(stress_list)}
inv_stress_map = {v:k for k,v in stress_map.items()}
inv_sleep_map = {v:k for k,v in sleep_map.items()}
inv_time_map = {v:k for k,v in time_map.items()}
inv_diet_map = {v:k for k,v in diet_map.items()}

# Functions

def random_timestamp(start_dt, end_dt, n):
    timestamps = []
    start_ts = int(start_dt.timestamp())
    end_ts = int(end_dt.timestamp())
    for _ in range(n):
        dt_base = start_ts + random.randint(0, end_ts - start_ts)
        hour = 10 if random.random() < 0.7 else 20
        dt = datetime.fromtimestamp(dt_base)
        dt = dt.replace(hour=hour, minute=random.randint(0,59), second=random.randint(0,59))
        timestamps.append(dt.strftime("%Y-%m-%d %H:%M:%S"))
    return timestamps

def pick_program(stream):
    if stream == "School of Engineering & Technology":
        return random.choice(programs_et), "", "", ""
    if stream == "School of Computer Science & Technology":
        return "", random.choice(programs_cst), "", ""
    if stream == "School of Agriculture":
        return "", "", random.choice(programs_agri), ""
    if stream == "School of Science, Arts & Media":
        return "", "", "", random.choice(programs_sam)
    return "", "", "", ""

def generate_correlated_features(n):
    corr_matrix = np.array([
        [1.0, 0.3, 0.4, -0.3],
        [0.3, 1.0, 0.2, 0.0],
        [0.4, 0.2, 1.0, -0.1],
        [-0.3, 0.0, -0.1, 1.0]
    ])
    mean = [0,0,0,0]
    mvn_samples = multivariate_normal.rvs(mean=mean, cov=corr_matrix, size=n)
    uniform_samples = 0.5 * (1 + erf(mvn_samples / np.sqrt(2)))

    sleep_scores = np.clip(np.ceil(uniform_samples[:, 0] * 5), 1, 5).astype(int)
    water_scores = np.clip(np.ceil(uniform_samples[:, 1] * 4), 1, 4).astype(int)
    diet_scores = np.clip(np.ceil(uniform_samples[:, 2] * 5), 1, 5).astype(int)
    time_scores = np.clip(np.ceil(uniform_samples[:, 3] * 5), 1, 5).astype(int)

    sleep = [inv_sleep_map[s-1] for s in sleep_scores]
    water = [water_intake[s-1] for s in water_scores]
    diet = [inv_diet_map[d-1] for d in diet_scores]
    time_mgmt = [inv_time_map[t-1] for t in time_scores]
    return sleep, water, diet, time_mgmt

def pick_exercise(year_idx, n):
    params = [(2,5),(2,4),(3,3),(4,2),(5,2),(6,1)]
    exercise_choices = [
        "Never","1 - 2 times per week","3 - 4 times per week","5 - 6 times per week","Daily"
    ]
    exercise_level = []
    for i in range(n):
        a,b = params[year_idx[i]]
        val = beta.rvs(a,b)
        if val < 0.2:
            exercise_level.append(exercise_choices[0])
        elif val < 0.4:
            exercise_level.append(exercise_choices[1])
        elif val < 0.6:
            exercise_level.append(exercise_choices[2])
        elif val < 0.8:
            exercise_level.append(exercise_choices[3])
        else:
            exercise_level.append(exercise_choices[4])
    return exercise_level

def generate_feedback(row):
    templates = [
        "Stressed by {stress}; suggests to {suggest}.",
        "{year} in {program}: {suggest}.",
        "Peer support: {peer}, diet: {diet}, recommends: {suggest}.",
        "Mental health: {mental}, sleep: {sleep}, exercise: {exercise}. {suggest}",
        "Year {year}, time management: {time}, would like: {suggest}.",
        "Counseling access: {counseling}, suggestion: {suggest}."
    ]
    template = random.choice(templates)
    suggest = random.choice(suggestions)
    program = row.get("Choose your program (ET):  ") or row.get("Choose your program (CST):  ") or row.get("Choose your program(Agri):  ") or row.get("Choose your program(SAM):  ")
    return template.format(
        stress=row.get("What’s stressing you the most?", ""),
        suggest=suggest,
        year=row.get("What year are you in?", ""),
        program=program,
        peer=row.get("How supported do you feel by your friends/peers?", ""),
        diet=row.get("How would you rate your diet? ", ""),
        mental=row.get("How have you been feeling mentally and emotionally this week?", ""),
        sleep=row.get("On average, how many hours of sleep do you get per night?  ", ""),
        exercise=row.get("How often do you exercise?", ""),
        time=row.get("Do you have enough time to get everything done? ", ""),
        counseling=row.get("Are wellness or counseling services accessible when you need them?  ", "")
    )

def generate_dataset_base(n_rows=300, start_date="2025-09-30", end_date="2025-10-05"):
    start_dt = datetime.strptime(start_date, "%Y-%m-%d")
    end_dt = datetime.strptime(end_date, "%Y-%m-%d")

    genders_sample = [random.choice(genders) for _ in range(n_rows)]
    years_idx = np.random.choice(len(years), n_rows)
    years_sample = [years[i] for i in years_idx]
    streams_sample = [random.choice(streams) for _ in range(n_rows)]

    prog_et, prog_cst, prog_agri, prog_sam = [], [], [], []
    for stream in streams_sample:
        etp, cstp, agrip, samp = pick_program(stream)
        prog_et.append(etp)
        prog_cst.append(cstp)
        prog_agri.append(agrip)
        prog_sam.append(samp)

    sleep_cat, water_cat, diet_cat, time_cat = generate_correlated_features(n_rows)
    exercise_cat = pick_exercise(years_idx, n_rows)
    peer_cat = random.choices(peer_support, weights=[0.2, 0.3, 0.25, 0.15, 0.1], k=n_rows)
    counseling_cat = random.choices(counseling_access, weights=[0.4, 0.25, 0.2, 0.15], k=n_rows)
    stress_source_sample = [random.choice(stress_sources) for _ in range(n_rows)]
    water_intake_sample = water_cat
    timestamps = random_timestamp(start_dt, end_dt, n_rows)

    return pd.DataFrame({
        "Gender": genders_sample,
        "Year": years_sample,
        "Year_idx": years_idx,
        "Stream": streams_sample,
        "Program_ET": prog_et,
        "Program_CST": prog_cst,
        "Program_Agri": prog_agri,
        "Program_SAM": prog_sam,
        "Sleep": sleep_cat,
        "WaterIntake": water_intake_sample,
        "Diet": diet_cat,
        "TimeManagement": time_cat,
        "Exercise": exercise_cat,
        "PeerSupport": peer_cat,
        "CounselingAccess": counseling_cat,
        "StressSource": stress_source_sample,
        "Timestamp": timestamps,
    })

def encode_features(df):
    df_enc = df.copy()
    df_enc["Sleep_enc"] = df_enc["Sleep"].map(lambda x: sleep_map.get(x,2))
    df_enc["Water_enc"] = df_enc["WaterIntake"].map(lambda x: water_intake.index(x) if x in water_intake else 1)
    df_enc["Diet_enc"] = df_enc["Diet"].map(lambda x: diet_map.get(x,2))
    df_enc["Time_enc"] = df_enc["TimeManagement"].map(lambda x: time_map.get(x,2))
    df_enc["Exercise_enc"] = df_enc["Exercise"].map(lambda x: exercise.index(x) if x in exercise else 2)
    df_enc["Peer_enc"] = df_enc["PeerSupport"].map(lambda x: peer_map.get(x,2))
    df_enc["Counseling_enc"] = df_enc["CounselingAccess"].map(lambda x: counseling_map.get(x,2))
    df_enc["Year_enc"] = df_enc["Year_idx"]
    return df_enc

def train_stress_model(df):
    stress_levels = list(stress_map.keys())
    df['Stress_init'] = random.choices(stress_levels, k=df.shape[0])
    df_enc = encode_features(df)
    X = df_enc[["Sleep_enc", "Water_enc", "Diet_enc", "Time_enc", "Exercise_enc", "Peer_enc", "Counseling_enc", "Year_enc"]]
    y = df["Stress_init"].map(stress_map)
    clf = RandomForestClassifier(n_estimators=100, random_state=42)
    clf.fit(X, y)
    return clf

def predict_stress(df, clf):
    df_enc = encode_features(df)
    X = df_enc[["Sleep_enc", "Water_enc", "Diet_enc", "Time_enc", "Exercise_enc", "Peer_enc", "Counseling_enc", "Year_enc"]]
    preds = clf.predict(X)
    return [stress_list[p] for p in preds]

def main_generate_and_model(n_rows, start_date, end_date):
    base_df = generate_dataset_base(n_rows, start_date, end_date)
    stress_model = train_stress_model(base_df)
    base_df["Stress_level"] = predict_stress(base_df, stress_model)

    mental_map = {i: mh for i,mh in enumerate(["Excellent", "Good", "Average", "Poor", "Very poor"])}
    base_df["Stress_idx"] = base_df["Stress_level"].map(stress_map)
    base_df["MentalHealth"] = base_df["Stress_idx"].map(mental_map)

    sleepq_map = {
        "Less than 4 hours": ["Very poor", " Poor"],
        "4 - 5 hours": [" Poor", " Average"],
        "6 - 7 hours": [" Average", " Good"],
        "8 - 9 hours": [" Good", " Excellent"],
        "More than 9 hours": [" Excellent", " Good"],
    }
    base_df["SleepQuality"] = base_df["Sleep"].apply(lambda s: random.choice(sleepq_map.get(s, [" Average"])))

    base_df["WaterIntake"] = base_df["WaterIntake"].apply(lambda s: f" {s.strip()}")
    base_df["Sleep"] = base_df["Sleep"].apply(lambda s: f" {s.strip()}")
    base_df["TimeManagement"] = base_df["TimeManagement"].apply(lambda s: f" {s.strip()}")


    feedbacks = []
    for _, row in base_df.iterrows():
        row_dict = {
            "What’s stressing you the most?": row["StressSource"],
            "What year are you in?": row["Year"],
            "Choose your program (ET):  ": row["Program_ET"],
            "Choose your program (CST):  ": row["Program_CST"],
            "Choose your program(Agri):  ": row["Program_Agri"],
            "Choose your program(SAM):  ": row["Program_SAM"],
            "How supported do you feel by your friends/peers?": row["PeerSupport"],
            "How would you rate your diet? ": row["Diet"],
            "How have you been feeling mentally and emotionally this week?": row["MentalHealth"],
            "On average, how many hours of sleep do you get per night?  ": row["Sleep"],
            "How often do you exercise?": row["Exercise"],
            "Do you have enough time to get everything done? ": row["TimeManagement"],
            "Are wellness or counseling services accessible when you need them?  ": row["CounselingAccess"]
        }
        feedbacks.append(generate_feedback(row_dict))
    base_df["Feedback"] = feedbacks

    final_df = pd.DataFrame({
        "Timestamp": base_df["Timestamp"],
        "What is your Gender?": base_df["Gender"],
        "What year are you in?": base_df["Year"],
        "Which stream are you interested in?": base_df["Stream"],
        "Choose your program (ET):  ": base_df["Program_ET"],
        "Choose your program (CST):  ": base_df["Program_CST"],
        "Choose your program(Agri):  ": base_df["Program_Agri"],
        "Choose your program(SAM):  ": base_df["Program_SAM"],
        "On a scale of 1-5, how stressed do you feel this week? ": base_df["Stress_level"],
        "What’s stressing you the most?": base_df["StressSource"],
        "Do you have enough time to get everything done? ": base_df["TimeManagement"],
        "On average, how many hours of sleep do you get per night?  ": base_df["Sleep"],
        "How well do you sleep?": base_df["SleepQuality"],
        "How often do you exercise?": base_df["Exercise"],
        "Average daily water intake (in glasses):": base_df["WaterIntake"],
        "How would you rate your diet? ": base_df["Diet"],
        "How have you been feeling mentally and emotionally this week?": base_df["MentalHealth"],
        "How supported do you feel by your friends/peers?": base_df["PeerSupport"],
        "Are wellness or counseling services accessible when you need them?  ": base_df["CounselingAccess"],
        "What changes would you suggest to improve student wellness on campus? ": base_df["Feedback"]
    })

    return final_df

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate student wellness data with Random Forest and prevent Excel date issues.")
    parser.add_argument("output", help="Output CSV filename")
    parser.add_argument("--rows", type=int, default=300, help="Number of rows")
    parser.add_argument("--start-date", type=str, default="2025-09-30", help="Start date YYYY-MM-DD")
    parser.add_argument("--end-date", type=str, default="2025-10-05", help="End date YYYY-MM-DD")
    args = parser.parse_args()

    df = main_generate_and_model(args.rows, args.start_date, args.end_date)
    df.to_csv(args.output, index=False)
    print(f"✅ {args.output} generated with {len(df)} rows")
