"""
Prompt construction for the RAG / Incident Intelligence layer.

This module is responsible for constructing grounded prompts
for the LLM using:

1. User question
2. Retrieved knowledge-base context
3. ML prediction context
4. SHAP feature contributions
"""

from typing import Any


def build_prompt(
    question: str,
    contexts: list[Any],
    incident_context: dict | None = None,
) -> str:
    """
    Build a grounded prompt for the incident intelligence LLM.

    Parameters
    ----------
    question : str
        User's question.

    contexts : list[Any]
        Retrieved knowledge-base documents.

    incident_context : dict | None
        ML prediction and SHAP information.

    Returns
    -------
    str
        Prompt to be sent to the LLM.
    """

    # ---------------------------------------------------------
    # 1. Build knowledge-base context
    # ---------------------------------------------------------

    context_parts = []

    for index, item in enumerate(contexts, start=1):
        context_parts.append(
            f"SOURCE {index}\n"
            f"{item.text}"
        )

    context_text = "\n\n".join(context_parts)

    # ---------------------------------------------------------
    # 2. Build ML incident context
    # ---------------------------------------------------------

    incident_context_text = ""

    if incident_context:

        prediction_class = incident_context.get(
            "prediction_class"
        )

        prediction_label = incident_context.get(
            "prediction_label"
        )

        breach_probability = incident_context.get(
            "sla_breach_probability"
        )

        decision_threshold = incident_context.get(
            "decision_threshold",
            0.5,
        )

        risk_level = incident_context.get(
            "risk_level"
        )

        top_shap_contributors = incident_context.get(
            "top_shap_contributors",
            [],
        )

        shap_lines = []

        for item in top_shap_contributors:
            feature = item.get("feature")
            impact = item.get("impact")

            shap_lines.append(
                f"- {feature}: {impact:+.4f}"
            )

        shap_text = "\n".join(shap_lines)

        incident_context_text = f"""
ML INCIDENT ANALYSIS

Prediction class:
{prediction_class}

Prediction label:
{prediction_label}

SLA breach probability:
{breach_probability:.4f}

Decision threshold:
{decision_threshold:.2f}

Risk level:
{risk_level}

Top SHAP contributors:
{shap_text}
"""

    # ---------------------------------------------------------
    # 3. Construct final prompt
    # ---------------------------------------------------------

    prompt = f"""
You are an IT Incident Intelligence Assistant.

Your responsibility is to explain the machine-learning
prediction and provide operational guidance using the
retrieved incident-management knowledge base.

============================================================
IMPORTANT RULES
============================================================

1. The machine-learning prediction is the authoritative
   source for the prediction outcome.

2. Never contradict the ML prediction label.

3. Never assume that the user's wording about the incident
   risk is correct.

4. If the user describes an incident as "high risk", verify
   that statement against the supplied ML prediction,
   probability, and risk level.

5. The SLA breach probability represents the probability
   of the positive class:

       Class 1 = SLA Breach

6. A probability close to the decision threshold should be
   described as "borderline" or "requiring monitoring".

7. Do not call an incident "High risk" unless the supplied
   risk level explicitly says "High".

8. SHAP values explain how individual features contributed
   to the model output. They do NOT establish causation.

============================================================
SHAP INTERPRETATION RULES
============================================================

For this project, SHAP contributions should be interpreted
with respect to the SLA Breach class.

A POSITIVE SHAP impact means:

    The feature pushed the model output toward
    the SLA Breach class.

A NEGATIVE SHAP impact means:

    The feature pushed the model output away from
    the SLA Breach class.

Therefore:

    Positive SHAP
        -> increases the model output toward SLA Breach

    Negative SHAP
        -> decreases the model output toward SLA Breach

IMPORTANT:

- Do NOT describe a positive SHAP value as increasing
  the likelihood of "No SLA Breach".

- Do NOT describe a negative SHAP value as proving that
  a feature prevents an SLA breach.

- Do NOT claim that a feature caused the prediction.

- Use wording such as:
      "pushed the model toward SLA Breach"
      "pushed the model away from SLA Breach"
      "contributed positively to the model output"
      "contributed negatively to the model output"

============================================================
ML INCIDENT CONTEXT
============================================================

{incident_context_text}

============================================================
KNOWLEDGE BASE CONTEXT
============================================================

{context_text}

============================================================
USER QUESTION
============================================================

{question}

============================================================
RESPONSE REQUIREMENTS
============================================================

Structure the response using the following sections:

### Prediction Interpretation

Clearly state:

- Prediction label
- SLA breach probability
- Decision threshold
- Risk level

If the probability is close to the threshold, explicitly
describe the prediction as borderline.

### Key Model Factors

Explain the most important SHAP contributors.

For positive SHAP values, say that the feature pushed
the model toward SLA Breach.

For negative SHAP values, say that the feature pushed
the model away from SLA Breach.

Do not claim causation.

### Recommended Operational Actions

Use the retrieved knowledge-base context to provide
practical operational recommendations.

Do not invent policies or procedures that are not
supported by the retrieved knowledge base.

### Distinction Between Model Findings and
Knowledge-Base Recommendations

Clearly distinguish:

1. What the ML model predicted.
2. What the SHAP explanation indicates.
3. What the knowledge base recommends.

The ML model determines the prediction.

The SHAP explanation explains the model output.

The knowledge base provides operational guidance.

The LLM must not change the ML prediction.
"""

    return prompt