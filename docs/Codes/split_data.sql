CREATE OR REPLACE TABLE `student-wellness-analytics.student_wellness.survey_split` AS
SELECT
  *,
  CASE
    WHEN RAND() < 0.8 THEN 'TRAIN'
    ELSE 'EVAL'
  END AS data_split
FROM `student-wellness-analytics.student_wellness.survey_responses`;
