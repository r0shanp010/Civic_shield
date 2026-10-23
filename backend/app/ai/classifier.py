import os
import pickle
import random
from typing import List, Dict, Any, Tuple, Optional
import numpy as np
from app.ai.preprocessing import clean_text

# Paths for saved model artifacts
MODEL_DIR = os.path.dirname(os.path.abspath(__file__))
MODELS_PATH = os.path.join(MODEL_DIR, "models")
CATEGORY_MODEL_FILE = os.path.join(MODELS_PATH, "category_model.pkl")
PRIORITY_MODEL_FILE = os.path.join(MODELS_PATH, "priority_model.pkl")
DEPT_MODEL_FILE = os.path.join(MODELS_PATH, "department_model.pkl")

def load_pickle_model(filepath: str) -> Optional[Dict[str, Any]]:
    """
    Loads serialized ML model and vectorizer artifact dictionary.
    """
    if os.path.exists(filepath):
        try:
            with open(filepath, "rb") as f:
                return pickle.load(f)
        except Exception as e:
            print(f"[WARNING] Failed to load model artifact at {filepath}: {e}")
            return None
    return None

class AIService:
    """
    AI-Guided Complaint Triage & Decision-Support System
    Pipeline:
    1. Text Preprocessing (Stopwords, cleaning, tokenization)
    2. TF-IDF Vectorization
    3. Logistic Regression Category Classification (+ Confidence Score)
    4. Priority Prediction (Monetary + Severity + ML Priority Model)
    5. Department Recommendation (ML Model + Department Rules)
    6. Duplicate Detection (TF-IDF + Cosine Similarity)
    7. Suspicious Pattern Detection (Spam/Repetition/Anomaly Filter)
    8. Dynamic AI Suggested Actions (Advisory checklist for human admin review)
    """

    def __init__(self):
        # Load trained ML models and TF-IDF vectorizers
        self.category_artifact = load_pickle_model(CATEGORY_MODEL_FILE)
        self.priority_artifact = load_pickle_model(PRIORITY_MODEL_FILE)
        self.dept_artifact = load_pickle_model(DEPT_MODEL_FILE)

    def reload_models(self):
        """Reload models if retrained during runtime."""
        self.category_artifact = load_pickle_model(CATEGORY_MODEL_FILE)
        self.priority_artifact = load_pickle_model(PRIORITY_MODEL_FILE)
        self.dept_artifact = load_pickle_model(DEPT_MODEL_FILE)

    def analyze_complaint(
        self, 
        description: str, 
        amount_involved: Optional[float] = None, 
        previous_complaints: List[Dict[str, Any]] = []
    ) -> Dict[str, Any]:
        """
        Main AI triage entry point. Classifies and generates decision-support metrics.
        Academic note: This system classifies and assists human reviewers.
        It does NOT establish legal guilt or make binary true/false declarations.
        """
        # Step 1: Text Preprocessing
        cleaned = clean_text(description)
        amount = amount_involved if amount_involved else 0.0
        
        # Step 2 & 3: TF-IDF + Logistic Regression Category Classification
        cat_pred, cat_conf = self._predict_category(cleaned, description)
        
        # Step 4: Priority Prediction
        priority_pred, priority_conf = self._predict_priority(cleaned, amount, description, cat_pred)
        
        # Step 5: Department Recommendation
        dept_pred, dept_conf = self._predict_department(cleaned, description, cat_pred)
        
        # Step 6: Duplicate Detection via TF-IDF + Cosine Similarity
        duplicate_score, duplicate_id = self._check_duplicates(description, previous_complaints)
        
        # Step 7: Suspicious Pattern Detection
        suspicious_flag = self._check_suspicious_pattern(description, amount, previous_complaints)
        
        # Step 8: Dynamic AI Suggested Actions
        suggested_actions = self.get_suggested_actions(cat_pred, amount, dept_pred)
        
        return {
            "predicted_category": cat_pred,
            "category_confidence": round(float(cat_conf), 2),
            "predicted_priority": priority_pred,
            "priority_confidence": round(float(priority_conf), 2),
            "recommended_department": dept_pred,
            "department_confidence": round(float(dept_conf), 2),
            "duplicate_score": round(float(duplicate_score), 2),
            "duplicate_match_id": duplicate_id,
            "suspicious_flag": suspicious_flag,
            "suggested_actions": suggested_actions
        }

    # -------------------------------------------------------------
    # CATEGORY CLASSIFICATION (TF-IDF + Logistic Regression)
    # -------------------------------------------------------------
    def _predict_category(self, cleaned: str, raw: str) -> Tuple[str, float]:
        """
        Predicts complaint category using trained TF-IDF + Logistic Regression.
        Fallback to heuristic feature scoring if model artifact is unavailable.
        """
        if self.category_artifact:
            try:
                model = self.category_artifact["model"]
                vectorizer = self.category_artifact["vectorizer"]
                vec = vectorizer.transform([cleaned if cleaned else raw.lower()])
                pred = str(model.predict(vec)[0])
                proba_arr = model.predict_proba(vec)[0]
                proba = float(np.max(proba_arr) * 100.0)
                # Keep confidence realistically calibrated (65% - 98%)
                calibrated_conf = min(max(proba, 68.0), 98.5)
                return pred, calibrated_conf
            except Exception as e:
                print(f"[WARNING] ML Category prediction error: {e}")

        # Rule-based / Keyword Heuristic Fallback
        raw_lower = raw.lower()
        categories = {
            "Bribery": ["bribe", "money", "cash", "payment", "envelope", "kickback", "grease", "commission", "speed payment"],
            "Extortion": ["threat", "blackmail", "extort", "force", "coerce", "consequence", "harass", "demolish", "intimidation"],
            "Misuse of Authority": ["power", "authority", "arbitrary", "abuse", "withhold", "harassment", "discretionary", "favoritism"],
            "Procurement Corruption": ["bid", "tender", "contract", "procure", "purchase", "vendor", "supplies", "specifications", "e-tender"],
            "Favouritism": ["relative", "favor", "nepotism", "cronyism", "prefer", "son", "daughter", "friend", "appoint", "nephew"],
            "Fraud": ["fraud", "scam", "fake", "forge", "cheat", "divert", "fund", "audit", "account", "embezzle", "siphon", "payroll"],
            "Illegal Payment Demand": ["illegal", "demand", "charge", "fees", "extra", "fine", "receipt", "unauthorized", "levy"]
        }
        
        scores = {cat: 0 for cat in categories}
        for cat, keywords in categories.items():
            for kw in keywords:
                if kw in raw_lower:
                    scores[cat] += 1
                    
        best_cat = max(scores, key=scores.get)
        if scores[best_cat] > 0:
            confidence = min(65.0 + (scores[best_cat] * 9.0), 96.0)
            return best_cat, confidence
        
        return "Misuse of Authority", 65.0

    # -------------------------------------------------------------
    # PRIORITY MODEL
    # -------------------------------------------------------------
    def _predict_priority(self, cleaned: str, amount: float, raw: str, category: str) -> Tuple[str, float]:
        """
        Priority prediction combining:
        1. Monetary severity thresholds
        2. Threat/Safety keywords
        3. TF-IDF + Logistic Regression Priority Model
        """
        raw_lower = raw.lower()

        # Rule 1: High Monetary Amounts
        if amount >= 1000000.0: # >= 10 Lakhs (High financial impact)
            return "Critical", 98.0
        elif amount >= 100000.0: # >= 1 Lakh
            return "High", 92.0

        # Rule 2: Physical safety / Violence / Criminal Coercion
        critical_words = ["kill", "life", "violence", "weapon", "physical", "assault", "lockup", "minister", "crore", "systemic"]
        for w in critical_words:
            if w in raw_lower:
                return "Critical", 94.0

        # Rule 3: Category Severity Baseline
        if category in ["Extortion", "Fraud", "Procurement Corruption"]:
            high_words = ["police", "commissioner", "director", "bribery", "embezzle", "tender", "highway", "lakh"]
            if any(w in raw_lower for w in high_words):
                return "High", 88.0

        # Rule 4: ML Priority Classifier
        if self.priority_artifact:
            try:
                model = self.priority_artifact["model"]
                vectorizer = self.priority_artifact["vectorizer"]
                vec = vectorizer.transform([cleaned if cleaned else raw.lower()])
                pred = str(model.predict(vec)[0])
                proba = float(np.max(model.predict_proba(vec)[0]) * 100.0)
                calibrated_conf = min(max(proba, 65.0), 95.0)
                return pred, calibrated_conf
            except Exception as e:
                print(f"[WARNING] ML Priority prediction error: {e}")

        # Default heuristic based on text length & keywords
        if len(raw) > 400 or amount > 20000.0:
            return "Medium", 78.0
        return "Low", 70.0

    # -------------------------------------------------------------
    # DEPARTMENT RECOMMENDATION (Rules + ML)
    # -------------------------------------------------------------
    def _predict_department(self, cleaned: str, raw: str, category: str) -> Tuple[str, float]:
        """
        Department recommendation combining domain keyword rules with ML model.
        """
        raw_lower = raw.lower()

        # Domain Rule Mapping
        department_rules = {
            "Police": ["police", "fir", "arrest", "cop", "station", "lockup", "constable", "inspector", "crime", "challan"],
            "Revenue": ["land", "property", "registry", "registration", "patwari", "stamp", "tax", "mutation", "survey", "deed", "sub-registrar"],
            "Municipality": ["building", "permit", "road", "street", "garbage", "sewer", "water", "ward", "sanitation", "birth", "trade license", "corporation", "demolish"],
            "Government Procurement": ["tender", "bid", "procure", "procurement", "vendor", "supplies", "e-tender", "contractor", "bidding"],
            "Public Works": ["highway", "bridge", "construction", "pwd", "pipeline", "asphalt", "engineer", "borewell", "infrastructure"],
            "Healthcare": ["hospital", "doctor", "nurse", "medicine", "clinic", "health", "pharmacy", "medical", "diagnostic", "patient"],
            "Transport": ["rto", "license", "driving", "transport", "bus", "fleet", "vehicle", "traffic", "truck", "cargo", "fitness certificate"],
            "Education": ["school", "college", "university", "admission", "exam", "grade", "student", "teacher", "principal", "dean", "degree"]
        }

        # Count keyword matches
        dept_scores = {dept: 0 for dept in department_rules}
        for dept, keywords in department_rules.items():
            for kw in keywords:
                if kw in raw_lower:
                    dept_scores[dept] += 2  # high weight for exact domain terms

        best_rule_dept = max(dept_scores, key=dept_scores.get)
        
        # If strong rule match (>= 2 matches)
        if dept_scores[best_rule_dept] >= 2:
            confidence = min(75.0 + (dept_scores[best_rule_dept] * 6.0), 96.0)
            return best_rule_dept, confidence

        # ML Department Model prediction
        if self.dept_artifact:
            try:
                model = self.dept_artifact["model"]
                vectorizer = self.dept_artifact["vectorizer"]
                vec = vectorizer.transform([cleaned if cleaned else raw.lower()])
                pred = str(model.predict(vec)[0])
                proba = float(np.max(model.predict_proba(vec)[0]) * 100.0)
                calibrated_conf = min(max(proba, 68.0), 94.0)
                return pred, calibrated_conf
            except Exception as e:
                print(f"[WARNING] ML Department prediction error: {e}")

        if dept_scores[best_rule_dept] > 0:
            return best_rule_dept, 70.0

        return "Other", 60.0

    # -------------------------------------------------------------
    # DUPLICATE DETECTION (TF-IDF + Cosine Similarity)
    # -------------------------------------------------------------
    def _check_duplicates(self, description: str, previous_complaints: List[Dict[str, Any]]) -> Tuple[float, Optional[int]]:
        """
        Computes TF-IDF vector representations and calculates pairwise Cosine Similarity.
        Returns highest similarity score percentage (0-100%) and matched complaint ID.
        """
        if not previous_complaints:
            return 0.0, None

        try:
            from sklearn.feature_extraction.text import TfidfVectorizer
            from sklearn.metrics.pairwise import cosine_similarity

            clean_current = clean_text(description)
            texts = [clean_current if clean_current else description.lower()]
            comp_ids = []

            for comp in previous_complaints:
                desc = comp.get("description", "")
                c_desc = clean_text(desc)
                texts.append(c_desc if c_desc else desc.lower())
                comp_ids.append(comp.get("id"))

            # Compute TF-IDF matrix
            vectorizer = TfidfVectorizer(ngram_range=(1, 2), min_df=1)
            tfidf_matrix = vectorizer.fit_transform(texts)

            # Compute Cosine Similarity between new complaint (index 0) and previous complaints (index 1:)
            new_vec = tfidf_matrix[0:1]
            prev_vecs = tfidf_matrix[1:]

            sim_scores = cosine_similarity(new_vec, prev_vecs)[0]
            max_idx = int(np.argmax(sim_scores))
            max_sim = float(sim_scores[max_idx] * 100.0)
            matched_id = comp_ids[max_idx]

            return max_sim, matched_id

        except Exception as e:
            print(f"[WARNING] TF-IDF Cosine Similarity calculation error: {e}")
            # Fallback Jaccard similarity
            words1 = set(clean_text(description).split())
            max_sim = 0.0
            matched_id = None
            for comp in previous_complaints:
                words2 = set(clean_text(comp.get("description", "")).split())
                if words1 and words2:
                    inter = len(words1.intersection(words2))
                    union = len(words1.union(words2))
                    sim = (inter / union) * 100.0 if union > 0 else 0.0
                    if sim > max_sim:
                        max_sim = sim
                        matched_id = comp.get("id")
            return max_sim, matched_id

    # -------------------------------------------------------------
    # SUSPICIOUS PATTERN DETECTION
    # -------------------------------------------------------------
    def _check_suspicious_pattern(self, description: str, amount: float, previous_complaints: List[Dict[str, Any]]) -> bool:
        """
        Heuristic anomaly detection for repetitive spam, exact automated duplicates, or short high-value claims.
        """
        words = description.lower().split()
        if len(words) > 20:
            unique_words = set(words)
            # Flag if repetitive spam (less than 30% unique tokens)
            if (len(unique_words) / len(words)) < 0.30:
                return True

        # Perfect verbatim duplicate matching
        clean_new = clean_text(description)
        if len(clean_new) > 10:
            for comp in previous_complaints:
                if clean_text(comp.get("description", "")) == clean_new:
                    return True

        # Extreme monetary claim without substantive description
        if amount > 5000000.0 and len(description.strip()) < 50:
            return True

        return False

    # -------------------------------------------------------------
    # DYNAMIC AI SUGGESTED ACTIONS (Human Review Assistance)
    # -------------------------------------------------------------
    def get_suggested_actions(self, category: str, amount: float, department: str) -> List[str]:
        """
        Returns dynamic, actionable advisory investigation checklists for human administrative triage.
        """
        amount_str = f"approx. Rs. {int(amount):,}" if amount > 0 else "stated amounts"

        actions_map = {
            "Bribery": [
                f"Review relevant payment records and transaction channels matching {amount_str}",
                f"Verify duty rosters and logs of public officials active during the reported incident",
                "Preserve submitted digital file attachments in forensic evidence vault",
                f"Review applicable departmental registers at {department} division",
                "Assign authorized reviewing officer to verify monetary demand claims"
            ],
            "Extortion": [
                "Verify reported incident details, dates, and locations",
                "Preserve submitted evidence and verify digital integrity of media files",
                f"Check relevant departmental records at {department} where authorized",
                "Review available CCTV or supporting security footage near reported location",
                "Escalate immediately if safety threats or physical coercion are reported"
            ],
            "Misuse of Authority": [
                f"Review administrative allocation statutes and delegation of powers at {department}",
                "Verify the reported discretionary decision, order, or permit process",
                "Examine supporting documentation and clearance signatures",
                f"Identify responsible official hierarchy in {department} division",
                "Assign authorized vigilance reviewer to examine procedural compliance"
            ],
            "Procurement Corruption": [
                "Review tender documentation, e-procurement logs, and technical evaluation sheets",
                "Examine relevant procurement records and vendor corporate filings",
                "Compare submitted supporting evidence against approved price benchmark tables",
                "Verify applicable public procurement procedures and statutory thresholds",
                "Assign authorized procurement audit reviewer"
            ],
            "Favouritism": [
                "Review recruitment panel minutes, qualification benchmarks, and selection rosters",
                "Verify candidate scoring sheets and eligibility criteria compliance",
                "Examine conflict-of-interest declarations of decision-making officials",
                f"Audit appointment and promotion registers at {department} office",
                "Assign neutral departmental committee to review selection fairness"
            ],
            "Fraud": [
                f"Initiate financial audit on cited accounts and vouchers matching {amount_str}",
                "Verify invoice authentications with third-party billing registers",
                "Cross-examine bank transfer ledgers and Treasury disbursement records",
                "Preserve digital audit logs and authorization signatures in evidence archive",
                "Escalate file to state vigilance and anti-corruption audit bureau"
            ],
            "Illegal Payment Demand": [
                f"Verify official government fee schedules and published Citizen Charter for {department}",
                "Check collection counter receipt logs and unreceipted cash handling protocols",
                "Audit official counter staff assignment logs for the reported date",
                "Review surveillance footage or counter service window recordings if available",
                "Issue administrative notice regarding unauthorized fee collection"
            ]
        }

        return actions_map.get(category, [
            f"Review complaint details and verify jurisdiction of {department}",
            "Preserve all submitted evidence files for audit inspection",
            "Update citizen progress timeline logs to maintain transparency",
            "Assign responsible officer to conduct preliminary inquiry"
        ])

# Singleton service instance
ai_service = AIService()
