CREATE OR REPLACE VIEW `student_wellness.analytics_responses` AS
SELECT
  SAFE.PARSE_TIMESTAMP('%m/%d/%Y %H:%M:%S', Timestamp) AS ts,
  
  Study_Year,
  Gender,
  School_Name,
  Program_Name,
  
  DATE(SAFE.PARSE_TIMESTAMP('%m/%d/%Y %H:%M:%S', Timestamp)) AS date_val,
  FORMAT_DATE('%Y-%W', DATE(SAFE.PARSE_TIMESTAMP('%m/%d/%Y %H:%M:%S', Timestamp))) AS week_val,
  
  CASE
    WHEN TRIM(Stress_Level) LIKE '1%' THEN 1
    WHEN TRIM(Stress_Level) LIKE '2%' THEN 2
    WHEN TRIM(Stress_Level) LIKE '3%' THEN 3
    WHEN TRIM(Stress_Level) LIKE '4%' THEN 4
    WHEN TRIM(Stress_Level) LIKE '5%' THEN 5
  END AS stress_score,
  
  Stress_Sources AS stress_source,
  
  CASE
    WHEN TRIM(Time_Management) = 'Never' THEN 1
    WHEN TRIM(Time_Management) = 'Rarely' THEN 2
    WHEN TRIM(Time_Management) = 'Sometimes' THEN 3
    WHEN TRIM(Time_Management) = 'Often' THEN 4
    WHEN TRIM(Time_Management) = 'Always' THEN 5
  END AS time_management_score,
  
  CASE
    WHEN Sleep_Hours LIKE 'Less than 4%' THEN 3
    WHEN Sleep_Hours LIKE '4–5%' OR Sleep_Hours LIKE '4 - 5%' THEN 4.5
    WHEN Sleep_Hours LIKE '6–7%' OR Sleep_Hours LIKE '6 - 7%' THEN 6.5
    WHEN Sleep_Hours LIKE '8–9%' OR Sleep_Hours LIKE '8 - 9%' THEN 8.5
    WHEN Sleep_Hours LIKE 'More than 9%' THEN 9.5
  END AS sleep_hours_numeric,
  
  CASE
    WHEN TRIM(Sleep_Quality) = 'Very poor' THEN 1
    WHEN TRIM(Sleep_Quality) = 'Poor' THEN 2
    WHEN TRIM(Sleep_Quality) = 'Average' THEN 3
    WHEN TRIM(Sleep_Quality) = 'Good' THEN 4
    WHEN TRIM(Sleep_Quality) = 'Excellent' THEN 5
  END AS sleep_quality_score,
  
  CASE
    WHEN Exercise_Frequency LIKE '%Never%' THEN 0
    WHEN Exercise_Frequency LIKE '%1–2%' OR Exercise_Frequency LIKE '%1 - 2%' THEN 1.5
    WHEN Exercise_Frequency LIKE '%3–4%' OR Exercise_Frequency LIKE '%3 - 4%' THEN 3.5
    WHEN Exercise_Frequency LIKE '%5–6%' OR Exercise_Frequency LIKE '%5 - 6%' THEN 5.5
    WHEN Exercise_Frequency LIKE '%Daily%' THEN 7
  END AS exercise_score,
  
  CASE
    WHEN TRIM(Diet_Quality) = 'Very unhealthy' THEN 1
    WHEN TRIM(Diet_Quality) = 'Somewhat unhealthy' THEN 2
    WHEN TRIM(Diet_Quality) = 'Neutral / Average' THEN 3
    WHEN TRIM(Diet_Quality) = 'Healthy' THEN 4
    WHEN TRIM(Diet_Quality) = 'Very healthy' THEN 5
  END AS diet_quality_score,
  
  CASE
    WHEN Water_Intake LIKE 'Less than 3%' THEN 2
    WHEN Water_Intake LIKE '3 - 5%' OR Water_Intake LIKE '3-5%' THEN 4
    WHEN Water_Intake LIKE '6 - 8%' OR Water_Intake LIKE '6-8%' THEN 7
    WHEN Water_Intake LIKE 'More than 8%' OR Water_Intake LIKE '%9%' THEN 9
  END AS water_intake_glasses,
  
  CASE
    WHEN TRIM(Emotional_Wellbeing) = 'Very poor' THEN 1
    WHEN TRIM(Emotional_Wellbeing) = 'Poor' THEN 2
    WHEN TRIM(Emotional_Wellbeing) = 'Average' THEN 3
    WHEN TRIM(Emotional_Wellbeing) = 'Good' THEN 4
    WHEN TRIM(Emotional_Wellbeing) = 'Excellent' THEN 5
  END AS emotional_score,
  
  CASE
    WHEN TRIM(Social_Support) = 'Never' THEN 1
    WHEN TRIM(Social_Support) = 'Rarely' THEN 2
    WHEN TRIM(Social_Support) = 'Sometimes' THEN 3
    WHEN TRIM(Social_Support) = 'Often' THEN 4
    WHEN TRIM(Social_Support) = 'Always' THEN 5
  END AS social_support_score,
  
  CASE
    WHEN TRIM(Counseling_Access) = 'No, not accessible' THEN 1
    WHEN TRIM(Counseling_Access) = 'Rarely' THEN 2
    WHEN TRIM(Counseling_Access) = 'Sometimes' THEN 3
    WHEN TRIM(Counseling_Access) = 'Yes, always' THEN 4
  END AS counseling_access_score,
  
  CASE WHEN TRIM(Stress_Level) LIKE '4%' OR TRIM(Stress_Level) LIKE '5%' THEN 1 ELSE 0 END AS high_stress_flag,
  CASE WHEN TRIM(Stress_Level) LIKE '1%' OR TRIM(Stress_Level) LIKE '2%' THEN 1 ELSE 0 END AS low_stress_flag,
  
  Stress_Level,
  Stress_Sources,
  Time_Management,
  Sleep_Hours,
  Sleep_Quality,
  Exercise_Frequency,
  Diet_Quality,
  Water_Intake,
  Emotional_Wellbeing,
  Social_Support,
  Counseling_Access,
  Feedback
  
FROM `student_wellness.survey_responses`
WHERE SAFE.PARSE_TIMESTAMP('%m/%d/%Y %H:%M:%S', Timestamp) IS NOT NULL;
