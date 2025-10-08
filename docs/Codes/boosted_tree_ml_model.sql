CREATE OR REPLACE MODEL `student_wellness.stress_bt`
OPTIONS(
  model_type='BOOSTED_TREE_CLASSIFIER',
  input_label_cols=['stress_score'],
  auto_class_weights=TRUE,
  enable_global_explain=TRUE,
  early_stop=TRUE,
  learn_rate=0.05,
  max_iterations=200,
  max_tree_depth=8,
  subsample=0.7,
  min_tree_child_weight=5,
  l1_reg=1.0,
  l2_reg=1.0
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
  -- Top derived features only
  (sleep_quality_score + exercise_score + diet_quality_score + emotional_score)/4 AS overall_wellness_score,
  (CASE WHEN sleep_hours_numeric<6 THEN 1 ELSE 0 END
   +CASE WHEN exercise_score<=1 THEN 1 ELSE 0 END
   +CASE WHEN diet_quality_score<=2 THEN 1 ELSE 0 END
   +CASE WHEN emotional_score<=2 THEN 1 ELSE 0 END
  ) AS risk_factors_count
FROM `student_wellness.model_data_splits`
WHERE split='TRAIN';
