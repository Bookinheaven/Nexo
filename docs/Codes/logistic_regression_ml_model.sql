CREATE OR REPLACE TABLE `student_wellness.train_base` AS
SELECT
  *,
  (sleep_quality_score + exercise_score + diet_quality_score + emotional_score) / 4 AS overall_wellness_score,
  (CASE WHEN sleep_hours_numeric < 6 THEN 1 ELSE 0 END
   + CASE WHEN exercise_score <= 1 THEN 1 ELSE 0 END
   + CASE WHEN diet_quality_score <= 2 THEN 1 ELSE 0 END
   + CASE WHEN emotional_score <= 2 THEN 1 ELSE 0 END
  ) AS risk_factors_count
FROM
  `student_wellness.model_data_splits`
WHERE
  split = 'TRAIN';

CREATE OR REPLACE TABLE `student_wellness.bt_train_preds` AS
SELECT
  p.fp,
  p.predicted_stress_score_probs AS bt_probs
FROM
  ML.PREDICT(
    MODEL `student_wellness.stress_bt`,
    TABLE `student_wellness.train_base`
  ) AS p;

CREATE OR REPLACE TABLE `student_wellness.rf_train_preds` AS
SELECT
  p.fp,
  p.predicted_stress_score_probs AS rf_probs
FROM
  ML.PREDICT(
    MODEL `student_wellness.stress_rf`,
    TABLE `student_wellness.train_base`
  ) AS p;

CREATE OR REPLACE TABLE `student_wellness.train_probs` AS
SELECT
  b.stress_score,
  bt.bt_probs,
  rf.rf_probs
FROM
  `student_wellness.train_base` AS b
JOIN
  `student_wellness.bt_train_preds` AS bt
USING(fp)
JOIN
  `student_wellness.rf_train_preds` AS rf
USING(fp);

CREATE OR REPLACE MODEL `student_wellness.stress_ensemble`
OPTIONS(
  model_type='LOGISTIC_REG',
  input_label_cols=['stress_score'],
  max_iterations=50,
  l1_reg=0.1,
  l2_reg=0.1
) AS
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
  rf_probs[OFFSET(4)] AS rf_p5
FROM
  `student_wellness.train_probs`;

