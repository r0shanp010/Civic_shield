import os
import sys
from fastapi.testclient import TestClient

# Adjust path to include the backend folder
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.main import app

def test_system_flow():
    print("--- STARTING CIVICSHIELD INTEGRATION TESTS ---")
    
    # Using 'with' context manager ensures FastAPI lifespan startup (migrations + seeding) executes
    with TestClient(app) as client:
        # 1. Test Root
        res = client.get("/")
        assert res.status_code == 200
        assert res.json()["status"] == "online"
        print("[PASS] Root API endpoint is active.")

        # 2. Test Submit Complaint Anonymously
        complaint_payload = {
            "description": "I witnessed the procurement director accepting cash payments from a vendor at the building site.",
            "category": "Bribery",
            "department": "Government Procurement",
            "location": "Directorate Office",
            "incident_date": "2026-08-10",
            "amount_involved": 50000.0
        }
        
        # Use data parameter because endpoint expects Form data
        res = client.post("/api/complaints", data=complaint_payload)
        assert res.status_code == 201
        data = res.json()
        assert "tracking_id" in data
        tracking_id = data["tracking_id"]
        print(f"[PASS] Complaint created anonymously. Generated Tracking ID: {tracking_id}")
        assert tracking_id.startswith("COR-")

        # 3. Test Track Complaint Status (Citizen view)
        res = client.get(f"/api/complaints/{tracking_id}")
        assert res.status_code == 200
        comp_data = res.json()
        assert comp_data["tracking_id"] == tracking_id
        assert comp_data["status"] == "Pending"
        # Ensure sensitive items like internal notes/confidences are excluded in schema
        assert "ai_prediction" not in comp_data
        print("[PASS] Citizen status tracking works and excludes administrative AI data.")

        # 4. Test Secure Admin Login
        login_payload = {
            "username": "admin",
            "password": "admin123"
        }
        res = client.post("/api/auth/login", data=login_payload)
        assert res.status_code == 200
        token_data = res.json()
        assert "access_token" in token_data
        token = token_data["access_token"]
        print("[PASS] Admin authentication successful. JWT Token generated.")

        headers = {"Authorization": f"Bearer {token}"}

        # 5. Test Accessing Dashboard
        res = client.get("/api/admin/dashboard", headers=headers)
        assert res.status_code == 200
        stats = res.json()
        assert stats["total_complaints"] >= 1
        assert stats["pending_complaints"] >= 1
        print(f"[PASS] Admin Dashboard stats retrieved. Total cases registered: {stats['total_complaints']}")

        # 6. Test Fetching Filtered Complaints Register
        res = client.get("/api/admin/complaints?status=Pending", headers=headers)
        assert res.status_code == 200
        complaints_list = res.json()
        assert len(complaints_list) >= 1
        target_comp = complaints_list[0]
        comp_db_id = target_comp["id"]
        
        # Validate AI predictions are attached for admins
        assert target_comp["ai_prediction"] is not None
        ai_eval = target_comp["ai_prediction"]
        print(f"[PASS] AI Prediction successfully linked to Case ID {comp_db_id}.")
        print(f"       AI Classification: Category='{ai_eval['predicted_category']}' | Priority='{ai_eval['predicted_priority']}' | Routing Dept='{ai_eval['recommended_department']}'")

        # 7. Test Verified Case Journey Transitions (Pending -> Under Review)
        under_review_payload = {
            "priority": "High",
            "category": "Bribery",
            "internal_note": "Case evaluations active. Found matching parameters.",
            "citizen_update": "The case has been routed for triage review and detail verification."
        }
        res = client.post(f"/api/admin/complaints/{comp_db_id}/transition/under-review", json=under_review_payload, headers=headers)
        assert res.status_code == 200
        assert res.json()["status"] == "Under Review"
        print("[PASS] Transition to Under Review succeeded.")

        # Test Transition (Under Review -> Assigned)
        assign_payload = {
            "department": "Revenue",
            "internal_note": "Routing to land audit desk. Bypassing other queues.",
            "citizen_update": "Case routed to Revenue Department.",
            "approved_actions": ["Review land logs", "Preserve evidence files"]
        }
        res = client.post(f"/api/admin/complaints/{comp_db_id}/transition/assign", json=assign_payload, headers=headers)
        assert res.status_code == 200
        assert res.json()["status"] == "Assigned"
        print("[PASS] Transition to Assigned succeeded and case actions saved.")

        # Test Transition (Assigned -> Investigating)
        investigate_payload = {
            "officer": "Officer A",
            "internal_note": "Assigned land inspection officer. Desk code active.",
            "citizen_update": "Officer assigned. Investigation in active progress."
        }
        res = client.post(f"/api/admin/complaints/{comp_db_id}/transition/investigate", json=investigate_payload, headers=headers)
        assert res.status_code == 200
        assert res.json()["status"] == "Investigating"
        print("[PASS] Transition to Investigating succeeded and investigator assigned.")

        # Test Transition (Investigating -> Resolved)
        resolve_payload = {
            "resolution_type": "Action Taken",
            "resolution_summary": "Fines issued to registration desks. Verification files locked.",
            "internal_note": "Internal verification completed successfully.",
            "citizen_update": "Grievance resolved. System corrective action applied."
        }
        res = client.post(f"/api/admin/complaints/{comp_db_id}/transition/resolve", json=resolve_payload, headers=headers)
        assert res.status_code == 200
        assert res.json()["status"] == "Resolved"
        print("[PASS] Transition to Resolved succeeded and resolution recorded.")

        # Test Transition (Resolved -> Closed)
        close_payload = {
            "internal_note": "Archiving case key details.",
            "citizen_update": "Grievance case finalized and closed."
        }
        res = client.post(f"/api/admin/complaints/{comp_db_id}/transition/close", json=close_payload, headers=headers)
        assert res.status_code == 200
        assert res.json()["status"] == "Closed"
        print("[PASS] Transition to Closed succeeded. Workflow sequence complete.")

        # 8. Verify Citizen status reflects safe updates and protects internal note privacy
        res = client.get(f"/api/complaints/{tracking_id}")
        assert res.status_code == 200
        citizen_comp = res.json()
        assert citizen_comp["status"] == "Closed"
        
        # Verify that updates contain safe citizen updates and NEVER leak internal notes
        for up in citizen_comp["updates"]:
            assert "Confidential" not in up["note"]
            assert "Bypassing" not in up["note"]
            assert "internal" not in up["note"]
            assert "desk" not in up["note"]
        print("[PASS] Citizen timeline successfully reflects status changes using citizen-safe logs while protecting confidential notes.")

        # 10. Test Citizen Register and Login
        import uuid
        citizen_rand = f"citizen_{uuid.uuid4().hex[:6]}"
        citizen_reg_payload = {
            "username": citizen_rand,
            "email": f"{citizen_rand}@whistle.org",
            "password": "Password123!"
        }
        res = client.post("/api/auth/citizen/register", json=citizen_reg_payload)
        assert res.status_code == 201
        print("[PASS] Citizen registration completed successfully.")

        citizen_login_payload = {
            "username": citizen_rand,
            "password": "Password123!"
        }
        res = client.post("/api/auth/citizen/login", json=citizen_login_payload)
        assert res.status_code == 200
        cit_token = res.json()["access_token"]
        print("[PASS] Citizen login successful. JWT Citizen token retrieved.")

        # 11. Test submitting complaint as logged in citizen
        cit_headers = {"Authorization": f"Bearer {cit_token}"}
        cit_complaint = {
            "description": "Report on health inspector extortion demands in Central Hospital.",
            "category": "Extortion",
            "department": "Healthcare",
            "location": "Central Clinic",
            "incident_date": "2026-08-15",
            "amount_involved": 15000.0
        }
        res = client.post("/api/complaints", data=cit_complaint, headers=cit_headers)
        assert res.status_code == 201
        cit_tracking_id = res.json()["tracking_id"]
        print(f"[PASS] Citizen complaint submitted. Tracking ID: {cit_tracking_id}")

        # 12. Fetch citizen's complaints portfolio
        res = client.get("/api/complaints/my/list", headers=cit_headers)
        assert res.status_code == 200
        my_list = res.json()
        assert len(my_list) >= 1
        assert my_list[0]["tracking_id"] == cit_tracking_id
        print("[PASS] Citizen's submitted portfolio lists their linked complaint correctly.")
    
    print("\n--- ALL CIVICSHIELD INTEGRATION TESTS COMPLETED SUCCESSFULLY ---")

if __name__ == "__main__":
    test_system_flow()
