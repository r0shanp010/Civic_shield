import os
import pickle
import sys
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, accuracy_score
from app.ai.preprocessing import clean_text

# Comprehensive Dataset of Citizen Complaints for Governance AI Classification
COMPLAINTS_DATASET = [
    # 1. Bribery (Demands for cash, kickbacks, envelopes, speed payments)
    ("The municipal building inspector demanded a bribe of 50000 cash in an envelope to sign off on our residential house building permit.", "Bribery", "Medium", "Municipality"),
    ("I was asked to pay 20000 under the table to the clerk at the revenue office to register my ancestral farm land property.", "Bribery", "High", "Revenue"),
    ("The food safety inspector demanded a monthly kickback of 15000 to grant the sanitary clearance certificate for our restaurant.", "Bribery", "High", "Healthcare"),
    ("Traffic police officers stopped our transport logistics truck and demanded 5000 grease payment to let us pass without a challan.", "Bribery", "Medium", "Transport"),
    ("The RTO licensing officer asked for 3000 cash bribe to issue the driving license without taking the mandatory driving test.", "Bribery", "Medium", "Transport"),
    ("The government procurement director demanded a 5% cash commission from our company to approve the vendor supply contract.", "Bribery", "High", "Government Procurement"),
    ("School admissions clerk demanded an extra 10000 bribe to release my daughter's secondary school transfer and marks certificate.", "Bribery", "Medium", "Education"),
    ("Sub-registrar officer took an illegal bribe of 15000 rupees to execute the property sale deed.", "Bribery", "High", "Revenue"),
    ("The police sub-inspector asked for 25000 in cash to release our impounded vehicle.", "Bribery", "High", "Police"),
    ("The municipal ward officer refused to issue water connection until we paid a 5000 bribe to his assistant.", "Bribery", "Medium", "Municipality"),

    # 2. Extortion (Coercion, blackmail, physical threats, illegal threats of demolition)
    ("The municipal zonal inspector is threatening to demolish my grocery shop unless I pay him 10000 protection money every single month.", "Extortion", "High", "Municipality"),
    ("A local police officer is blackmailing me and threatening to file a fabricated FIR against my teenage son unless we pay 50000.", "Extortion", "Critical", "Police"),
    ("Enforcement squad officers used physical intimidation and threats of seizure to force small street vendors to pay daily protection fees.", "Extortion", "High", "Municipality"),
    ("The revenue officer is threatening to cancel my land title deed and seize my property if I do not pay an unofficial extortion charge.", "Extortion", "High", "Revenue"),
    ("Local inspector threatened to shut down our private diagnostic clinic on false violations unless we pay 30000 monthly protection money.", "Extortion", "Critical", "Healthcare"),
    ("Transport checkpoint officers threatened to confiscate our cargo vehicle indefinitely unless we hand over 20000 cash immediately.", "Extortion", "High", "Transport"),
    ("The municipal official sent goons to intimidate our family and force us to withdraw our complaint regarding illegal land encroachment.", "Extortion", "Critical", "Municipality"),
    ("Police constable threatened violence and illegal lockup detention unless we paid him 15000 on the spot.", "Extortion", "Critical", "Police"),

    # 3. Misuse of Authority (Abuse of official powers, harassment, arbitrary decisions, personal enrichment)
    ("The sub-registrar is arbitrarily refusing to sign legal property transfer documents without any valid reason, simply to harass us.", "Misuse of Authority", "Medium", "Revenue"),
    ("The school principal suspended a meritorious student arbitrarily because the parents raised questions about unauthorized fee hikes.", "Misuse of Authority", "Medium", "Education"),
    ("The senior police officer refused to register a formal criminal complaint and abused his official power to shield his influential friend.", "Misuse of Authority", "High", "Police"),
    ("The department head is using official government vehicles, drivers, and state funds for his personal family vacations and private events.", "Misuse of Authority", "Low", "Transport"),
    ("The public works department engineer signed off on a substandard, broken road project, completely ignoring civil engineering safety standards.", "Misuse of Authority", "Medium", "Public Works"),
    ("The hospital superintendent unlawfully locked the public medicine counter and redirected patients to his private pharmacy.", "Misuse of Authority", "High", "Healthcare"),
    ("The municipal commissioner abused his statutory power to grant commercial zoning exemptions to his own private properties.", "Misuse of Authority", "High", "Municipality"),
    ("Revenue patwari intentionally withheld property records and harassed poor farmers for several months without legal basis.", "Misuse of Authority", "Medium", "Revenue"),

    # 4. Procurement Corruption (Rigged bidding, tender manipulation, substandard materials, vendor collusion)
    ("The e-tender process for the state highway construction project was completely rigged. The contract was awarded to a disqualified contractor.", "Procurement Corruption", "High", "Government Procurement"),
    ("The health department purchased substandard medical equipment and PPE kits at triple the market price from a favored shell vendor.", "Procurement Corruption", "High", "Healthcare"),
    ("Confidential technical bidding specifications and price ceilings were secretly leaked to a favored supplier prior to the public tender opening.", "Procurement Corruption", "High", "Government Procurement"),
    ("The municipal bridge repair contract worth 2 crores was awarded to the mayor's brother's firm without floating any public competitive tender.", "Procurement Corruption", "Critical", "Public Works"),
    ("The education department procured defective tablet computers for government schools at double the retail cost from an unregistered company.", "Procurement Corruption", "High", "Education"),
    ("Public works department officials colluded with private suppliers to supply inferior asphalt concrete for the expressway project.", "Procurement Corruption", "Critical", "Public Works"),
    ("Government IT procurement committee manipulated tender eligibility criteria specifically to eliminate competitive bidders.", "Procurement Corruption", "High", "Government Procurement"),
    ("The transport corporation awarded the state bus fleet maintenance contract to an unverified workshop through backdoor negotiations.", "Procurement Corruption", "High", "Transport"),

    # 5. Favouritism (Nepotism, crony appointments, biased promotions, grade tampering)
    ("The university director appointed his unqualified nephew as the senior research consultant, completely bypassing all qualified candidates.", "Favouritism", "Low", "Education"),
    ("The civil hospital director is favoring his close relatives' wholesale firm for all hospital linen, catering, and security contracts.", "Favouritism", "Medium", "Healthcare"),
    ("Promotions in the state transport department are granted exclusively to political allies and relatives of the transport minister.", "Favouritism", "Medium", "Transport"),
    ("The university examination dean tampered with the official semester grade sheets of his personal acquaintances to grant them top ranks.", "Favouritism", "Medium", "Education"),
    ("The municipal engineer allocated prime commercial market stalls exclusively to his family members without conducting a public lottery.", "Favouritism", "Medium", "Municipality"),
    ("Public works department junior engineer vacancies were filled with relatives of department officers without conducting the required civil exam.", "Favouritism", "Medium", "Public Works"),
    ("Police recruitment board members gave preferential physical test scores to candidates from their hometown.", "Favouritism", "High", "Police"),

    # 6. Fraud (Embezzlement of state funds, forged audits, fake beneficiaries, bogus invoices)
    ("The revenue department senior accountant embezzled 75 lakhs from the state calamity relief fund by transferring money to ghost accounts.", "Fraud", "Critical", "Revenue"),
    ("Government welfare funds allocated for constructing drinking water borewells in drought villages were siphoned into personal bank accounts.", "Fraud", "Critical", "Public Works"),
    ("The government healthcare center submitted fraudulent reimbursement invoices for thousands of surgical patients who never existed.", "Fraud", "High", "Healthcare"),
    ("School administration officials forged financial audit reports to conceal the embezzlement of 20 lakhs from the student midday meal grant.", "Fraud", "High", "Education"),
    ("The municipal tax collector issued fake manual receipts with forged stamps and pocketed property tax payments of over 40 residents.", "Fraud", "High", "Municipality"),
    ("Public works department engineers created ghost employee payrolls and withdrew salaries for non-existent labor contractors for 2 years.", "Fraud", "Critical", "Public Works"),
    ("Transport authority officials forged vehicle fitness certificates and safety clearances for condemned commercial buses.", "Fraud", "High", "Transport"),

    # 7. Illegal Payment Demand (Unreceipted service fees, speed fees, arbitrary levies)
    ("The clerk at the regional transport office demanded 2500 rupees as an unreceipted 'speed fee' to process vehicle ownership transfer.", "Illegal Payment Demand", "Low", "Transport"),
    ("The municipal birth registry counter is demanding an unlawful 1000 fee per certificate without providing any government receipt.", "Illegal Payment Demand", "Low", "Municipality"),
    ("The electricity board line inspector demanded 6000 cash to install the domestic meter, claiming it is a mandatory department processing fee.", "Illegal Payment Demand", "Medium", "Public Works"),
    ("The revenue archive clerk demanded 1500 to search for historical land survey maps, claiming it is an internal department retrieval levy.", "Illegal Payment Demand", "Low", "Revenue"),
    ("Hospital registration desk staff are demanding 500 cash from poor patients to assign tokens for doctor consultations.", "Illegal Payment Demand", "Medium", "Healthcare"),
    ("Government school office staff are charging an unauthorized 2000 fee for issuing school transfer certificates.", "Illegal Payment Demand", "Low", "Education"),
    ("Police station station-writer demanded 1000 to provide a copy of the lost document report.", "Illegal Payment Demand", "Low", "Police"),
]

def train_and_save_models():
    """
    Trains the TF-IDF + Logistic Regression classification models for CivicShield AI triage.
    Model classifies:
    1. Category (Bribery, Extortion, Misuse of Authority, Procurement Corruption, Favouritism, Fraud, Illegal Payment Demand)
    2. Priority (Critical, High, Medium, Low)
    3. Department (Police, Revenue, Municipality, Public Works, Education, Healthcare, Transport, Government Procurement, Other)
    """
    print("=" * 60)
    print("CIVICSHIELD AI ENGINE - MODEL TRAINING PIPELINE")
    print("Architecture: Preprocessing -> TF-IDF Vectorizer -> Logistic Regression")
    print("=" * 60)
    
    # Preprocess complaint descriptions
    cleaned_texts = [clean_text(item[0]) for item in COMPLAINTS_DATASET]
    categories = [item[1] for item in COMPLAINTS_DATASET]
    priorities = [item[2] for item in COMPLAINTS_DATASET]
    departments = [item[3] for item in COMPLAINTS_DATASET]
    
    print(f"Total training samples: {len(cleaned_texts)}")
    print(f"Unique categories: {len(set(categories))} -> {sorted(set(categories))}")
    print(f"Unique departments: {len(set(departments))} -> {sorted(set(departments))}")
    print(f"Unique priority levels: {len(set(priorities))} -> {sorted(set(priorities))}")
    print("-" * 60)
    
    # Create models destination directory
    model_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "models")
    os.makedirs(model_dir, exist_ok=True)
    
    # -------------------------------------------------------------
    # 1. CATEGORY CLASSIFIER (TF-IDF + Logistic Regression)
    # -------------------------------------------------------------
    print("\n[1/3] Training Category Classifier (TF-IDF + Logistic Regression)...")
    category_vectorizer = TfidfVectorizer(
        ngram_range=(1, 2),
        sublinear_tf=True,
        min_df=1,
        max_features=5000
    )
    X_cat = category_vectorizer.fit_transform(cleaned_texts)
    
    cat_model = LogisticRegression(
        C=2.0,
        max_iter=1000,
        class_weight="balanced",
        random_state=42
    )
    cat_model.fit(X_cat, categories)
    
    cat_preds = cat_model.predict(X_cat)
    cat_acc = accuracy_score(categories, cat_preds)
    print(f"[PASS] Category Classifier Training Accuracy: {cat_acc * 100:.2f}%")
    
    category_artifact = {
        "model": cat_model,
        "vectorizer": category_vectorizer,
        "classes": list(cat_model.classes_)
    }
    cat_path = os.path.join(model_dir, "category_model.pkl")
    with open(cat_path, "wb") as f:
        pickle.dump(category_artifact, f)
    print(f"[PASS] Saved Category Model to: {cat_path}")
    
    # -------------------------------------------------------------
    # 2. PRIORITY CLASSIFIER (TF-IDF + Logistic Regression)
    # -------------------------------------------------------------
    print("\n[2/3] Training Priority Classifier...")
    priority_vectorizer = TfidfVectorizer(
        ngram_range=(1, 2),
        sublinear_tf=True,
        min_df=1,
        max_features=5000
    )
    X_prio = priority_vectorizer.fit_transform(cleaned_texts)
    
    prio_model = LogisticRegression(
        C=2.0,
        max_iter=1000,
        class_weight="balanced",
        random_state=42
    )
    prio_model.fit(X_prio, priorities)
    
    prio_preds = prio_model.predict(X_prio)
    prio_acc = accuracy_score(priorities, prio_preds)
    print(f"[PASS] Priority Classifier Training Accuracy: {prio_acc * 100:.2f}%")
    
    priority_artifact = {
        "model": prio_model,
        "vectorizer": priority_vectorizer,
        "classes": list(prio_model.classes_)
    }
    prio_path = os.path.join(model_dir, "priority_model.pkl")
    with open(prio_path, "wb") as f:
        pickle.dump(priority_artifact, f)
    print(f"[PASS] Saved Priority Model to: {prio_path}")
    
    # -------------------------------------------------------------
    # 3. DEPARTMENT CLASSIFIER (TF-IDF + Logistic Regression)
    # -------------------------------------------------------------
    print("\n[3/3] Training Department Classifier...")
    dept_vectorizer = TfidfVectorizer(
        ngram_range=(1, 2),
        sublinear_tf=True,
        min_df=1,
        max_features=5000
    )
    X_dept = dept_vectorizer.fit_transform(cleaned_texts)
    
    dept_model = LogisticRegression(
        C=2.0,
        max_iter=1000,
        class_weight="balanced",
        random_state=42
    )
    dept_model.fit(X_dept, departments)
    
    dept_preds = dept_model.predict(X_dept)
    dept_acc = accuracy_score(departments, dept_preds)
    print(f"[PASS] Department Classifier Training Accuracy: {dept_acc * 100:.2f}%")
    
    dept_artifact = {
        "model": dept_model,
        "vectorizer": dept_vectorizer,
        "classes": list(dept_model.classes_)
    }
    dept_path = os.path.join(model_dir, "department_model.pkl")
    with open(dept_path, "wb") as f:
        pickle.dump(dept_artifact, f)
    print(f"[PASS] Saved Department Model to: {dept_path}")
    
    # -------------------------------------------------------------
    # Summary of Training
    # -------------------------------------------------------------
    print("\n" + "=" * 60)
    print("MODEL TRAINING SUMMARY")
    print("=" * 60)
    print(f"Category Model:   Accuracy = {cat_acc*100:.1f}% | Classes = {len(cat_model.classes_)}")
    print(f"Priority Model:   Accuracy = {prio_acc*100:.1f}% | Classes = {len(prio_model.classes_)}")
    print(f"Department Model: Accuracy = {dept_acc*100:.1f}% | Classes = {len(dept_model.classes_)}")
    print("\nAcademic Note:")
    print("The model is designed to classify and assist human review.")
    print("It does NOT determine legal guilt or binary true/false validity.")
    print("=" * 60)
    return True

if __name__ == "__main__":
    success = train_and_save_models()
    sys.exit(0 if success else 1)
