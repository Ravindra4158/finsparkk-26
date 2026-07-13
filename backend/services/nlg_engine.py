"""
BankGuard Enterprise — NLG Engine (Mock)

Translates ML features (SHAP values, graph paths, policy triggers) into 
natural language explanations for auditors.
"""

def generate_explanation(risk_context: dict) -> str:
    """
    Takes the output of the meta risk engine and generates a readable explanation.
    """
    score = risk_context.get("final_score", 0)
    scores = risk_context.get("module_scores", {})
    
    explanations = []
    
    if score > 80:
        explanations.append(f"CRITICAL THREAT ({score}/100): Coordinated fraud indicators detected.")
    
    if scores.get("ueba", 0) > 80:
        explanations.append("- Behavioral Anomaly: Login activity is 14.2σ outside peer group baselines (e.g., 2:30 AM access).")
        
    if scores.get("nlp", 0) > 80:
        explanations.append("- Communication Intent: Bribery/collusion intent score is highly elevated in recent internal chats (0.91/1.0).")
        
    if scores.get("graph", 0) > 50:
        explanations.append("- Network Risk: Graph analytics revealed a 3-hop hidden link connecting the approving manager to the loan beneficiary via a shared property address.")
        
    if not explanations:
        return "Transaction appears normal based on current baselines."
        
    return "\n".join(explanations)
