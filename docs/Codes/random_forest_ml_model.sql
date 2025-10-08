CREATE OR REPLACE MODEL `student_wellness.stress_rf`
OPTIONS(
  model_type='RANDOM_FOREST_CLASSIFIER',
  input_label_cols=['stress_score'],
  num_parallel_tree=150,
  max_tree_depth=10,
  subsample=0.8,
  auto_class_weights=TRUE,
  enable_global_explain=TRUE
) AS
SELECT
  stress_score,
  sleep_hours_numeric,
  sleep_quality_score,
  exercise_score,
  diet_quality_score,
  water_intake_glasses,
  emotional_score,
  social_support_score,
  time_management_score,
  counseling_access_score,
  Gender,
  Study_Year,
  School_Name,
  Program_Name,
  stress_source,
  (sleep_quality_score + exercise_score + diet_quality_score + emotional_score)/4 AS overall_wellness_score,
  (CASE WHEN sleep_hours_numeric<6 THEN 1 ELSE 0 END
   +CASE WHEN exercise_score<=1 THEN 1 ELSE 0 END
   +CASE WHEN diet_quality_score<=2 THEN 1 ELSE 0 END
   +CASE WHEN emotional_score<=2 THEN 1 ELSE 0 END
  ) AS risk_factors_count
FROM `student_wellness.model_data_splits`
WHERE split='TRAIN';
