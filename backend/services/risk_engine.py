"""
BankGuard Enterprise — ML Risk Engine (Mock)

This service correlates the scores from all 5 analytical modules and computes a meta-score.
"""

def evaluate_ueba_risk(employee_id: str) -> float:
    # Dummy mock representing the Isolation Forest model output
    # e.g., 2:30 AM login triggers a high anomaly score
    return 85.0

def evaluate_loan_risk(loan_data: dict) -> float:
    # Dummy mock representing the XGBoost model output
    return 45.0

def evaluate_compliance_risk(loan_id: str) -> float:
    # Dummy mock representing the JSON Policy Rules
    return 15.0

def evaluate_nlp_risk(employee_id: str) -> float:
    # Dummy mock representing the Sentence Transformers intent score
    return 91.0 # E.g. bribery intent detected

def evaluate_graph_risk(entity_id: str) -> float:
    # Dummy mock representing the Neo4j Graph Centrality score
    return 60.0

def compute_meta_risk_score(employee_id: str, loan_data: dict) -> dict:
    """
    Computes a final correlated risk score using the 5 modules.
    Matches the 'Cross-Signal Correlator' in the architecture.
    """
    ueba_score = evaluate_ueba_risk(employee_id)
    loan_score = evaluate_loan_risk(loan_data)
    compliance_score = evaluate_compliance_risk(loan_data.get("id"))
    nlp_score = evaluate_nlp_risk(employee_id)
    graph_score = evaluate_graph_risk(employee_id)

    # Simplified mock meta-model logic
    weights = {
        "ueba": 0.25,
        "loan": 0.20,
        "compliance": 0.20,
        "nlp": 0.15,
        "graph": 0.20
    }

    base_score = (
        ueba_score * weights["ueba"] +
        loan_score * weights["loan"] +
        compliance_score * weights["compliance"] +
        nlp_score * weights["nlp"] +
        graph_score * weights["graph"]
    )
    
    # Correlation bonus: If multiple modules are > 50, escalate quickly
    high_signals = sum(1 for s in [ueba_score, loan_score, compliance_score, nlp_score, graph_score] if s > 50)
    correlation_bonus = 15.0 if high_signals >= 3 else 0.0

    final_score = min(100.0, base_score + correlation_bonus)

    threat_level = "low"
    if final_score > 80:
        threat_level = "critical"
    elif final_score > 60:
        threat_level = "high"
    elif final_score > 40:
        threat_level = "medium"

    return {
        "final_score": round(final_score, 1),
        "threat_level": threat_level,
        "module_scores": {
            "ueba": ueba_score,
            "loan": loan_score,
            "compliance": compliance_score,
            "nlp": nlp_score,
            "graph": graph_score
        }
    }
