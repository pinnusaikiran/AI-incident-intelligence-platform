# Exploratory Data Analysis (EDA) Findings

## Project

AI Incident Intelligence Platform – SLA Breach Prediction

---

# 1. Business Problem Statement

IT incidents that breach Service Level Agreements (SLAs) negatively impact business operations, customer satisfaction, and service provider performance.

The objective of this project is to predict SLA breaches at the time of incident creation, enabling proactive escalation and resource allocation before SLA violations occur.

Target Variable:

* made_sla = True → SLA Met
* made_sla = False → SLA Breached

For machine learning modeling:

* 0 → SLA Met
* 1 → SLA Breached

---

# 2. Dataset Overview

Source: ServiceNow Incident Management Event Log

Dataset Statistics:

* Total Event Records: 141,712
* Total Unique Incidents: 24,918
* Total Features: 36

The dataset is an event log where multiple records may exist for a single incident as the incident progresses through different lifecycle states.

---

# 3. Incident Representation Strategy

Since the objective is to predict SLA breach at incident creation time, only information available during incident creation can be used.

Analysis revealed:

* 24,913 records have sys_mod_count = 0
* Total incidents = 24,918

This indicates that records with sys_mod_count = 0 represent the initial incident creation event.

Therefore:

Each incident is represented using its earliest available record.

This avoids information leakage from future incident updates.

---

# 4. Target Variable Analysis

Target Feature:

made_sla

Distribution:

* SLA Met: 93.5%
* SLA Breached: 6.5%

Key Finding:

The dataset is highly imbalanced.

Modeling Implication:

Special attention must be given to class imbalance during model training and evaluation.

Potential techniques:

* Class weights
* SMOTE
* Precision/Recall-based evaluation metrics

---

# 5. Missing and Unknown Information Analysis

The dataset contains very few true null values.

However, several fields contain '?' values representing unknown information.

Important observation:

Unknown values are not random and appear to carry business significance.

Examples:

* u_symptom → 32,964 unknown values
* opened_by → 4,835 unknown values

Decision:

Unknown values will be retained as valid categories rather than removed or imputed.

---

# 6. Category Analysis

The category feature contains 59 unique service categories.

Key Findings:

* Significant variation exists in SLA breach rates across categories.
* Category 45 exhibited a breach rate of 12.85%.
* Category 46 exhibited a breach rate of 9.47%.
* Several categories exceeded the overall SLA breach rate of 6.5%.

Business Insight:

Service category strongly influences SLA performance and should be retained as a predictive feature.

Decision:

Retain category for machine learning modeling.

---

# 7. Subcategory Analysis

The subcategory feature contains 255 unique values.

Analysis was performed using subcategories with at least 500 incidents to ensure statistical reliability.

Highest-Risk Subcategories:

* Subcategory 220 → 16.81%
* Subcategory 150 → 14.71%
* Subcategory 231 → 14.24%
* Subcategory 88 → 11.86%
* Subcategory 200 → 11.62%

Key Finding:

Subcategory-level breach rates vary substantially and exceed the overall dataset breach rate.

Business Insight:

Specific service types are significantly more likely to violate SLA commitments.

Decision:

Retain subcategory as a high-value predictive feature.

---

# 8. Location Analysis

The location feature contains 225 unique locations.

High-Risk Locations (>=500 incidents):

* Location 42 → 8.11%
* Location 38 → 7.73%
* Location 111 → 7.58%

Locations Generating Highest Number of SLA Breaches:

* Location 204 → 2,250 breaches
* Location 143 → 1,351 breaches
* Location 161 → 1,185 breaches

Business Insight:

Operational performance differs across locations, suggesting location-specific operational challenges.

Decision:

Retain location as a predictive feature.

---

# 9. Contact Type Analysis

Contact Types:

* Phone
* Email
* Self Service
* IVR
* Direct Opening

Findings:

* Email → 17.73% breach rate
* Self Service → 7.04%
* Phone → 6.48%

Business Insight:

The channel used to report incidents influences SLA performance.

Although Email incidents are relatively few in number, they demonstrate significantly higher breach rates.

Decision:

Retain contact_type as a predictive feature.

---

# 10. Symptom Analysis

The u_symptom feature contains 526 unique values.

Highest-Risk Symptoms (>=500 incidents):

* Symptom 208 → 10.52%
* Symptom 120 → 9.03%
* Symptom 4 → 8.89%
* Symptom 6 → 8.83%

Unknown Symptom Analysis:

* Unknown (?) → 32,964 incidents
* Breach Rate → 7.85%

Key Finding:

Unknown symptoms exhibit higher breach rates than the dataset average.

Business Insight:

Incomplete incident descriptions may contribute to SLA violations.

Decision:

Retain u_symptom as a high-value predictive feature.

---

# 11. Time-Based Analysis

## Hour Analysis

High-Risk Hours:

* 2 PM → 7.68%
* 5 PM → 7.30%
* 1 PM → 7.17%
* 3 PM → 7.13%

Business Insight:

Incidents created during afternoon business hours are more likely to breach SLA.

---

## Day of Week Analysis

Highest-Risk Days:

* Wednesday → 7.07%
* Tuesday → 6.78%
* Thursday → 6.67%

Business Insight:

Mid-week incidents show slightly higher breach rates.

---

## Month Analysis

Highest-Risk Months:

* March → 9.44%
* January → 6.89%

Observation:

March demonstrates significantly elevated breach rates.

Potential explanation:

Increased operational workload during financial year-end activities.

This should be treated as a hypothesis rather than a confirmed conclusion.

---

# 12. High Cardinality Feature Analysis

## caller_id

* Unique Values: 5,245
* Unknown Values: 29

Assessment:

Potentially useful but extremely high cardinality.

Decision:

Retain for experimentation using frequency encoding or target encoding.

---

## opened_by

* Unique Values: 208
* Unknown Values: 4,835

Assessment:

Represents ticket creation source and may influence incident routing quality.

Decision:

Retain for experimentation.

---

# 13. Candidate Features for Modeling

High Priority Features:

* subcategory
* u_symptom
* category

Medium Priority Features:

* location
* caller_id
* opened_by

Supporting Features:

* contact_type
* hour
* day_of_week
* month

---

# 14. Features Excluded Due to Data Leakage

The following features contain future information unavailable at incident creation time and will not be used for model training:

* resolved_at
* closed_at
* resolved_by
* closed_code
* sys_updated_at
* sys_updated_by

Operational Features Excluded:

* reassignment_count
* reopen_count
* sys_mod_count

These values become available only after incident progression.

---

# 15. Key EDA Conclusions

1. SLA breach prediction is a highly imbalanced classification problem.
2. Service category and subcategory are strong predictors of SLA performance.
3. User-reported symptoms contain substantial predictive information.
4. Unknown symptom information is associated with elevated SLA breach risk.
5. Location-specific operational differences influence SLA outcomes.
6. Incident reporting channel impacts SLA performance.
7. Time-based patterns exist, particularly during afternoon business hours.
8. Data leakage risks were identified and mitigated before modeling.

These findings provide a strong foundation for Feature Engineering, Machine Learning Modeling, Explainable AI, and Production Deployment.
