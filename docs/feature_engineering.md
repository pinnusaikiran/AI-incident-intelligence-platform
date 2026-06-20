# Feature Engineering Decisions

## Objective

The objective of feature engineering is to prepare incident data for machine learning while ensuring that only information available at the time of incident creation is used for prediction.

The target variable is:

* `made_sla`

  * True = SLA Met
  * False = SLA Breached

The business objective is to predict whether an incident will breach SLA at the time the incident is created.

---

# Feature Selection Principles

The following principles were used during feature selection:

1. Features must be available at incident creation time.
2. Features containing future information were removed to prevent target leakage.
3. Features with extremely high missing values were removed.
4. Business-relevant features were retained even when data distribution was imbalanced.
5. Temporal information was transformed into machine-learning-friendly features.

---

# Features Retained

## Incident Context Features

| Feature      | Reason                                                          |
| ------------ | --------------------------------------------------------------- |
| contact_type | Represents the channel through which the incident was reported. |
| location     | Captures geographical or organizational location information.   |
| category     | Represents the primary incident classification.                 |
| subcategory  | Provides more granular incident classification.                 |
| u_symptom    | Represents the reported symptom associated with the incident.   |

---

## Ownership and Routing Features

| Feature          | Reason                                                             |
| ---------------- | ------------------------------------------------------------------ |
| assignment_group | Indicates the support group responsible for handling the incident. |
| assigned_to      | Represents the resolver assigned to the incident.                  |
| caller_id        | Identifies the user raising the incident.                          |
| opened_by        | Identifies the user or system that created the incident.           |

---

## Priority Features

| Feature  | Reason                                                     |
| -------- | ---------------------------------------------------------- |
| impact   | Represents business impact of the incident.                |
| urgency  | Represents urgency of resolution.                          |
| priority | System-generated priority derived from impact and urgency. |

Although priority is derived from impact and urgency, all three features were retained during feature engineering and evaluated later during model training and feature importance analysis.

---

## Temporal Features

The original `opened_at` feature was transformed into:

| Engineered Feature | Description                             |
| ------------------ | --------------------------------------- |
| Hour               | Hour during which incident was opened.  |
| Day_of_Week        | Day on which incident was opened.       |
| Month              | Month during which incident was opened. |

These features were created because machine learning models cannot directly interpret raw timestamp values.

---

# Features Removed

## Identifier Features

| Feature | Reason                                               |
| ------- | ---------------------------------------------------- |
| number  | Unique incident identifier with no predictive value. |

---

## Leakage Features

The following features contain information generated after incident creation and therefore introduce target leakage.

| Feature        |
| -------------- |
| resolved_by    |
| resolved_at    |
| closed_at      |
| closed_code    |
| sys_updated_by |
| sys_updated_at |

These features would not be available when making real-time predictions.

---

## Operational Process Features

| Feature            | Reason                                                                                          |
| ------------------ | ----------------------------------------------------------------------------------------------- |
| reassignment_count | Generated after incident processing begins.                                                     |
| reopen_count       | Generated after ticket lifecycle progresses.                                                    |
| sys_mod_count      | Tracks modifications after creation.                                                            |
| active             | Operational state flag with limited predictive value.                                           |
| incident_state     | Incident creation records are predominantly in "New" state, resulting in low information value. |

---

## Sparse Features

The following features were removed because of extremely high missing-value percentages.

| Feature    | Missing Percentage |
| ---------- | ------------------ |
| vendor     | 99.83%             |
| problem_id | 98.38%             |
| cmdb_ci    | 99.69%             |

These features contained insufficient information for reliable model training.

---

## Redundant Features

| Feature        | Reason                                                                     |
| -------------- | -------------------------------------------------------------------------- |
| opened_at      | Replaced by Hour, Day_of_Week and Month.                                   |
| sys_created_at | Similar information already captured through engineered temporal features. |
| sys_created_by | Overlaps with opened_by and contains high missing values.                  |
| notify         | Extremely imbalanced feature with minimal business value.                  |

---

# Missing Value Strategy

Missing values represented by `?` were treated as meaningful business states rather than being replaced with the most frequent category.

Examples:

| Feature          | Replacement           |
| ---------------- | --------------------- |
| category         | Unknown_Category      |
| subcategory      | Unknown_Subcategory   |
| location         | Unknown_Location      |
| u_symptom        | Unknown_Symptom       |
| assignment_group | Not_Assigned_Group    |
| assigned_to      | Not_Assigned_Engineer |
| caller_id        | Unknown_Caller        |
| opened_by        | Unknown_Reporter      |

This approach preserves operational meaning and allows the model to learn whether missing information itself contributes to SLA breaches.

---

# Encoding Strategy

## Frequency Encoding

Applied to medium-cardinality features:

* category
* assignment_group
* opened_by
* assigned_to
* subcategory

Frequency encoding captures how often each category appears within the dataset.

---

## Target Encoding

Applied to high-cardinality features:

* caller_id
* u_symptom
* location

Target encoding captures historical SLA breach behavior associated with each category while avoiding excessive dimensionality.

---

# Final Feature Set

The final feature set used for model development consists of:

* contact_type
* location
* category
* subcategory
* u_symptom
* assignment_group
* assigned_to
* caller_id
* opened_by
* impact
* urgency
* priority
* Hour
* Day_of_Week
* Month

Target:

* made_sla

