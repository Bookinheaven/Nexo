CREATE OR REPLACE TABLE `student_wellness.predictions_for_lookerstudio` AS
WITH validate_base AS (
  SELECT
    *,
    (sleep_quality_score + exercise_score + diet_quality_score + emotional_score) / 4 AS overall_wellness_score,
    (CASE WHEN sleep_hours_numeric < 6 THEN 1 ELSE 0 END
     + CASE WHEN exercise_score <= 1 THEN 1 ELSE 0 END
     + CASE WHEN diet_quality_score <= 2 THEN 1 ELSE 0 END
     + CASE WHEN emotional_score <= 2 THEN 1 ELSE 0 END
    ) AS risk_factors_count
  FROM `student_wellness.model_data_splits`
  WHERE split = 'VALIDATE'
),
bt_validate AS (
  SELECT
    p.fp,
    p.predicted_stress_score_probs AS bt_probs
  FROM ML.PREDICT(MODEL `student_wellness.stress_bt`, TABLE validate_base) AS p
),
rf_validate AS (
  SELECT
    p.fp,
    p.predicted_stress_score_probs AS rf_probs
  FROM ML.PREDICT(MODEL `student_wellness.stress_rf`, TABLE validate_base) AS p
),
ensemble_input AS (
  SELECT
    b.stress_score,
    b.ts,  
    b.sleep_hours_numeric,
    b.sleep_quality_score,
    b.exercise_score,
    b.diet_quality_score,
    b.emotional_score,
    b.social_support_score,
    b.Gender,
    b.Study_Year,
    b.School_Name,
    b.Program_Name,
    b.stress_source,
    bt.bt_probs,
    rf.rf_probs
  FROM validate_base AS b
  JOIN bt_validate AS bt USING(fp)
  JOIN rf_validate AS rf USING(fp)
)
SELECT
  stress_score AS actual_stress,
  predicted_stress_score AS predicted_stress,
  predicted_stress_score_probs[OFFSET(0)] AS p_class_1,
  predicted_stress_score_probs[OFFSET(1)] AS p_class_2,
  predicted_stress_score_probs[OFFSET(2)] AS p_class_3,
  predicted_stress_score_probs[OFFSET(3)] AS p_class_4,
  predicted_stress_score_probs[OFFSET(4)] AS p_class_5,
  ts,
  sleep_hours_numeric,
  sleep_quality_score,
  exercise_score,
  diet_quality_score,
  emotional_score,
  social_support_score,
  Gender,
  Study_Year,
  School_Name,
  Program_Name,
  stress_source
FROM ML.PREDICT(
  MODEL `student_wellness.stress_ensemble`,
  (
    SELECT
      stress_score,
      bt_probs[OFFSET(0)] AS bt_p1,
      bt_probs[OFFSET(1)] AS bt_p2,
      bt_probs[OFFSET(2)] AS bt_p3,
      bt_probs[OFFSET(3)] AS bt_p4,
      bt_probs[OFFSET(4)] AS bt_p5,
      rf_probs[OFFSET(0)] AS rf_p1,
      rf_probs[OFFSET(1)] AS rf_p2,
      rf_probs[OFFSET(2)] AS rf_p3,
      rf_probs[OFFSET(3)] AS rf_p4,
      rf_probs[OFFSET(4)] AS rf_p5,
      sleep_hours_numeric,
      sleep_quality_score,
      exercise_score,
      diet_quality_score,
      emotional_score,
      social_support_score,
      Gender,
      Study_Year,
      School_Name,
      Program_Name,
      stress_source,
      ts
    FROM ensemble_input
  )
);
