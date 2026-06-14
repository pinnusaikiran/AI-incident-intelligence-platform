# Feature Engineering Strategy

## Project

AI Incident Intelligence Platform – SLA Breach Prediction

---

# 1. Objective

The purpose of feature engineering is to transform raw incident records into machine-learning-ready features while preventing data leakage and preserving business meaning.

The resulting feature set should enable accurate prediction of SLA breaches at the time of incident creation.

---

# 2. Feature Selection Principles

A feature will be retained only if:

1. It is available when the incident is created.
2. It does not contain future information.
3. It has potential predictive value.
4. It can realistically exist in a production environment.

---

# 3. Target Variable

Feature:

```text
made_sla
```

Current Values:

```text
True
False
```

Transformation:

```text
True  → 0
False → 1
```

Meaning:

```text
0 = SLA Met
1 = SLA Breach
```

Reason:

Binary encoding simplifies classification modeling.

---

# 4. Features Selected for Modeling

## Category

Reason:

EDA showed significant variation in breach rates across categories.

Encoding Strategy:

One-Hot Encoding

---

## Subcategory

Reason:

One of the strongest predictors identified during EDA.

Encoding Strategy:

Frequency Encoding

Reason:

255 unique values create high-dimensional sparse vectors with One-Hot Encoding.

---

## u_symptom

Reason:

Strong predictive signal discovered during EDA.

Unknown symptom values also demonstrated elevated breach rates.

Encoding Strategy:

Frequency Encoding

---

## Location

Reason:

Operational performance varies across locations.

Encoding Strategy:

Frequency Encoding

---

## Contact Type

Reason:

Different reporting channels exhibited different SLA performance.

Encoding Strategy:

One-Hot Encoding

---

## Caller ID

Reason:

May capture recurring operational patterns.

Challenge:

Very high cardinality.

Unique Values:

5,245

Encoding Strategy:

Frequency Encoding

---

## Opened By

Reason:

May capture ticket creation quality differences.

Unique Values:

208

Encoding Strategy:

Frequency Encoding

---

## Hour

Derived From:

opened_at

Reason:

EDA identified higher breach rates during afternoon hours.

Encoding Strategy:

Numerical

---

## Day of Week

Derived From:

opened_at

Encoding Strategy:

One-Hot Encoding

---

## Month

Derived From:

opened_at

Encoding Strategy:

One-Hot Encoding

---

# 5. Handling Unknown Values

Several features contain:

```text
?
```

Examples:

* category
* subcategory
* u_symptom
* location
* caller_id
* opened_by

Strategy:

Retain as:

```text
Unknown
```

Reason:

EDA demonstrated that unknown values carry business meaning.

Unknown values showed different breach behavior than known values.

---

# 6. Features Excluded Due to Data Leakage

The following features become available only after the incident progresses and therefore cannot be used for prediction.

Excluded Features:

```text
resolved_at
closed_at
resolved_by
closed_code
```

Reason:

Contain future information.

---

# 7. Features Excluded Due to Operational Leakage

## reassignment_count

Reason:

Known only after incident routing.

---

## reopen_count

Reason:

Known after incident resolution.

---

## sys_mod_count

Reason:

Represents future updates.

---

## priority

Reason:

Derived from impact and urgency.

May be evaluated separately but excluded initially.

---

## impact

Excluded in baseline model.

---

## urgency

Excluded in baseline model.

---

# 8. Derived Features

The following features are generated from:

```text
opened_at
```

Generated Features:

* Hour
* Day_of_Week
* Month

Purpose:

Capture temporal incident behavior.

---

# 9. Class Imbalance Strategy

Target Distribution:

```text
SLA Met      ≈ 93.5%
SLA Breach   ≈ 6.5%
```

Problem:

Highly imbalanced dataset.

Potential Solutions:

### Option 1

Class Weights

Preferred baseline approach.

---

### Option 2

SMOTE

Will be evaluated experimentally.

---

### Option 3

Combined Approach

Class Weights + SMOTE

To be tested.

---

# 10. Train-Test Split Strategy

Goal:

Simulate real-world production behavior.

Candidate Approaches:

### Random Split

Simple baseline.

---

### Time-Based Split

Train:

Older incidents

Test:

Newer incidents

Preferred for production realism.

---

# 11. Evaluation Metrics

Accuracy will not be the primary metric.

Reason:

Class imbalance.

Primary Metrics:

* Recall
* Precision
* F1 Score
* ROC-AUC

Business Focus:

Maximize detection of SLA breaches while minimizing false alarms.

---

# 12. Baseline Models

Initial Models:

### Logistic Regression

Purpose:

Simple interpretable baseline.

---

### Random Forest

Purpose:

Capture nonlinear relationships.

---

### XGBoost

Purpose:

Expected production candidate.

---

# 13. Explainability Strategy

Technology:

SHAP

Purpose:

Explain:

* Why a prediction was made
* Which features influenced the prediction
* How feature values impact SLA risk

---

# 14. Expected High-Impact Features

Based on EDA findings:

Very High Importance:

* subcategory
* u_symptom
* category

High Importance:

* location
* caller_id
* opened_by

Medium Importance:

* hour
* contact_type

Lower Importance:

* day_of_week
* month

These assumptions will be validated during model training and SHAP analysis.

---

# 15. Success Criteria

Feature engineering will be considered successful if:

* No data leakage exists.
* Production-ready features are created.
* Business meaning is preserved.
* Class imbalance is properly addressed.
* Model performance improves compared to baseline approaches.

This feature engineering strategy serves as the foundation for model development, explainability, deployment, and future MLOps implementation.
