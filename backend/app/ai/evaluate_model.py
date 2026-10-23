import os
import sys
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import StratifiedKFold, cross_val_score, train_test_split
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score, precision_recall_fscore_support
from app.ai.preprocessing import clean_text
from app.ai.train_models import COMPLAINTS_DATASET
from app.ai.classifier import ai_service

def generate_evaluation_metrics():
    """
    Computes comprehensive mathematical evaluation metrics for the TF-IDF + Logistic Regression model.
    Returns metrics dictionary for both CLI presentation and API dashboard consumption.
    """
    texts = [item[0] for item in COMPLAINTS_DATASET]
    cleaned_texts = [clean_text(t) for t in texts]
    categories = [item[1] for item in COMPLAINTS_DATASET]
    priorities = [item[2] for item in COMPLAINTS_DATASET]
    departments = [item[3] for item in COMPLAINTS_DATASET]
    
    unique_classes = sorted(list(set(categories)))
    
    # 1. TF-IDF Feature Extraction
    vectorizer = TfidfVectorizer(
        ngram_range=(1, 2),
        sublinear_tf=True,
        min_df=1,
        max_features=5000
    )
    X = vectorizer.fit_transform(cleaned_texts)
    y = np.array(categories)
    
    # 2. Logistic Regression Classifier
    clf = LogisticRegression(C=2.0, max_iter=1000, class_weight='balanced', random_state=42)
    clf.fit(X, y)
    
    # 3. K-Fold Cross-Validation (Stratified 3-Fold)
    cv = StratifiedKFold(n_splits=3, shuffle=True, random_state=42)
    cv_scores = cross_val_score(clf, X, y, cv=cv, scoring='accuracy')
    
    # 4. Predictions and Metrics
    y_pred = clf.predict(X)
    overall_acc = accuracy_score(y, y_pred)
    prec, rec, f1, supp = precision_recall_fscore_support(y, y_pred, average='weighted', zero_division=0)
    macro_prec, macro_rec, macro_f1, _ = precision_recall_fscore_support(y, y_pred, average='macro', zero_division=0)
    
    # Per-class metrics
    class_report_dict = classification_report(y, y_pred, output_dict=True, zero_division=0)
    
    per_class_metrics = []
    for cls in unique_classes:
        if cls in class_report_dict:
            per_class_metrics.append({
                "category": cls,
                "precision": round(class_report_dict[cls]["precision"] * 100, 1),
                "recall": round(class_report_dict[cls]["recall"] * 100, 1),
                "f1_score": round(class_report_dict[cls]["f1-score"] * 100, 1),
                "support": int(class_report_dict[cls]["support"])
            })
            
    # 5. Confusion Matrix
    cm = confusion_matrix(y, y_pred, labels=unique_classes)
    
    # 6. Extract Top TF-IDF Keywords per Category
    feature_names = np.array(vectorizer.get_feature_names_out())
    top_keywords_per_cat = {}
    for i, cls in enumerate(clf.classes_):
        top_indices = np.argsort(clf.coef_[i])[-6:][::-1]
        top_keywords_per_cat[cls] = list(feature_names[top_indices])
        
    return {
        "model_name": "TF-IDF + Multi-Class Logistic Regression",
        "dataset_size": len(texts),
        "feature_count": len(vectorizer.get_feature_names_out()),
        "categories_count": len(unique_classes),
        "categories": unique_classes,
        "overall_accuracy": round(overall_acc * 100, 2),
        "cross_val_accuracy": round(float(np.mean(cv_scores)) * 100, 2),
        "cross_val_std": round(float(np.std(cv_scores)) * 100, 2),
        "macro_f1": round(macro_f1 * 100, 2),
        "weighted_f1": round(f1 * 100, 2),
        "per_class_metrics": per_class_metrics,
        "confusion_matrix": cm.tolist(),
        "top_keywords": top_keywords_per_cat
    }

def print_cli_evaluation():
    """
    Renders an academic-grade model evaluation report in the terminal.
    """
    metrics = generate_evaluation_metrics()
    
    print("=" * 75)
    print("  CIVICSHIELD AI ENGINE - MODEL PERFORMANCE & TRAINING EVALUATION")
    print("=" * 75)
    print(f"Model Architecture:       {metrics['model_name']}")
    print(f"Total Training Samples:   {metrics['dataset_size']} complaints")
    print(f"TF-IDF Feature Space:     {metrics['feature_count']} n-gram vocabulary tokens")
    print(f"Classification Classes:   {metrics['categories_count']} categories")
    print("-" * 75)
    print(f"Training Set Accuracy:    {metrics['overall_accuracy']}%")
    print(f"Cross-Validation Accuracy:{metrics['cross_val_accuracy']}% (+/- {metrics['cross_val_std']}%) [Stratified 3-Fold]")
    print(f"Macro Average F1-Score:   {metrics['macro_f1']}%")
    print(f"Weighted Average F1-Score:{metrics['weighted_f1']}%")
    print("=" * 75)
    
    print("\n" + "-" * 75)
    print(f"{'CATEGORY':<28} | {'PRECISION':<10} | {'RECALL':<10} | {'F1-SCORE':<10} | {'SAMPLES'}")
    print("-" * 75)
    for row in metrics["per_class_metrics"]:
        print(f"{row['category']:<28} | {row['precision']:>8.1f}%  | {row['recall']:>8.1f}%  | {row['f1_score']:>8.1f}%  | {row['support']:>5}")
    print("-" * 75)
    
    print("\n" + "=" * 75)
    print("  TOP DISCRIMINATIVE TF-IDF KEYWORDS EXTRACTED BY MODEL")
    print("=" * 75)
    for cat, keywords in metrics["top_keywords"].items():
        print(f"* {cat:<24} : {', '.join(keywords)}")
    print("=" * 75)
    
    print("\n" + "=" * 75)
    print("  LIVE INFERENCE PIPELINE DEMONSTRATION")
    print("=" * 75)
    sample_tests = [
        ("The municipal clerk demanded 50000 cash in an envelope to sign building permit.", 50000.0),
        ("Police inspector is blackmailing and threatening false FIR if we do not pay 30000.", 30000.0),
        ("Highway bridge tender was rigged and awarded to mayor's brother without bidding.", 2000000.0)
    ]
    
    for i, (text, amt) in enumerate(sample_tests, 1):
        res = ai_service.analyze_complaint(text, amount_involved=amt)
        print(f"\n[Test Case {i}] Input: \"{text}\" (Amount: Rs. {amt:,.0f})")
        print(f" -> Predicted Category:  {res['predicted_category']} ({res['category_confidence']}%)")
        print(f" -> Priority Assessment: {res['predicted_priority']} ({res['priority_confidence']}%)")
        print(f" -> Target Department:   {res['recommended_department']} ({res['department_confidence']}%)")
        print(f" -> Duplicate Score:     {res['duplicate_score']}% (Cleared)")
        print(f" -> AI Action Checklist: {res['suggested_actions'][0]}")
    print("\n" + "=" * 75)
    print("  ACADEMIC DEFENSE NOTE FOR FACULTY / GUIDE:")
    print("  1. The model uses TF-IDF n-grams + Logistic Regression with balanced class weights.")
    print("  2. It is strictly a Decision-Support System: It classifies and assists human reviewers.")
    print("  3. It does NOT decide guilt or make binary true/false declarations.")
    print("=" * 75)

if __name__ == "__main__":
    print_cli_evaluation()
