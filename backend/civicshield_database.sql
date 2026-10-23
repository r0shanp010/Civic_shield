-- ==============================================================================
-- CIVICSHIELD: AI-BASED ANONYMOUS CORRUPTION & BRIBERY COMPLAINT MANAGEMENT SYSTEM
-- MCA Major Project Database Schema & Seed Data Export (.sql)
-- Platform: Anti-Corruption Grievance Redressal & TF-IDF Machine Learning Triage
-- ==============================================================================

PRAGMA foreign_keys = ON;

-- ------------------------------------------------------------------------------
-- Table Structure for `users`
-- ------------------------------------------------------------------------------
CREATE TABLE users (
	id INTEGER NOT NULL, 
	username VARCHAR(100) NOT NULL, 
	email VARCHAR(150) NOT NULL, 
	password_hash VARCHAR(255) NOT NULL, 
	created_at DATETIME, 
	PRIMARY KEY (id)
);

-- Dumping data for table `users` (5 records)
INSERT INTO `users` (`id`, `username`, `email`, `password_hash`, `created_at`) VALUES (1, 'citizen_7eb93f', 'citizen_7eb93f@whistle.org', '$2b$12$O.urMZRfQ7UOrYDzFRp2oOnO1a2tim0.LTzHneXrWsqximd3KZFeW', '2026-08-31 06:05:51.201179');
INSERT INTO `users` (`id`, `username`, `email`, `password_hash`, `created_at`) VALUES (2, 'citizen_646278', 'citizen_646278@whistle.org', '$2b$12$PCHbpzMP0dRbguzuvKOj/.w.UfGgUwzY1r.B4YwKOtsqIgxMPSr4m', '2026-08-31 06:09:05.055881');
INSERT INTO `users` (`id`, `username`, `email`, `password_hash`, `created_at`) VALUES (3, 'citizen_9585ec', 'citizen_9585ec@whistle.org', '$2b$12$KM6Zj7Xr2GY/gHso9r218eBYQffTrPz4LS91fA37wjBaVFbN5jWUO', '2026-09-02 08:43:27.284344');
INSERT INTO `users` (`id`, `username`, `email`, `password_hash`, `created_at`) VALUES (4, 'Sukanya', 'mudholsukanya@gmail.com', '$2b$12$RMELEq6gJIuhJkT3aHvzDOS062zF7ZmNITIflbpNybubxZLVO0e7C', '2026-09-02 09:04:29.510360');
INSERT INTO `users` (`id`, `username`, `email`, `password_hash`, `created_at`) VALUES (5, 'Roshan', '25mcac41@kristujayanti.com', '$2b$12$o/OcATzP0h31Xk5rFBfRWeJ76iVtGRidWOTsunQogiYgBsDeZu3ZO', '2026-09-02 09:39:42.144624');

-- ------------------------------------------------------------------------------
-- Table Structure for `admin_users`
-- ------------------------------------------------------------------------------
CREATE TABLE admin_users (
	id INTEGER NOT NULL, 
	username VARCHAR(100) NOT NULL, 
	full_name VARCHAR(150), 
	email VARCHAR(150), 
	department VARCHAR(100), 
	password_hash VARCHAR(255) NOT NULL, 
	role VARCHAR(50), 
	created_at DATETIME, 
	PRIMARY KEY (id)
);

-- Dumping data for table `admin_users` (2 records)
INSERT INTO `admin_users` (`id`, `username`, `full_name`, `email`, `department`, `password_hash`, `role`, `created_at`) VALUES (1, 'admin', NULL, NULL, NULL, '$2b$12$HTmDru5/vbrV.wUSA74F0e6p2wxFbV1fjEsZfpJv8JnUzSDSrhPMm', 'Admin', '2026-08-31 06:05:50.243755');
INSERT INTO `admin_users` (`id`, `username`, `full_name`, `email`, `department`, `password_hash`, `role`, `created_at`) VALUES (2, 'officer1', NULL, NULL, NULL, '$2b$12$FptHCBFOH.XQ60LTErMkSuSQtm8qYW12uqa1REkLHsaXcQBk7HJzq', 'Officer', '2026-08-31 06:05:50.243762');

-- ------------------------------------------------------------------------------
-- Table Structure for `complaints`
-- ------------------------------------------------------------------------------
CREATE TABLE complaints (
	id INTEGER NOT NULL, 
	tracking_id VARCHAR(50) NOT NULL, 
	description TEXT NOT NULL, 
	category VARCHAR(100), 
	department VARCHAR(100), 
	location VARCHAR(255), 
	incident_date DATE, 
	amount_involved FLOAT, 
	priority VARCHAR(50), 
	status VARCHAR(50), 
	next_status VARCHAR(50), 
	verification_code VARCHAR(10), 
	user_id INTEGER, 
	created_at DATETIME, 
	updated_at DATETIME, 
	PRIMARY KEY (id), 
	FOREIGN KEY(user_id) REFERENCES users (id) ON DELETE SET NULL
);

-- Dumping data for table `complaints` (7 records)
INSERT INTO `complaints` (`id`, `tracking_id`, `description`, `category`, `department`, `location`, `incident_date`, `amount_involved`, `priority`, `status`, `next_status`, `verification_code`, `user_id`, `created_at`, `updated_at`) VALUES (1, 'COR-2026-QMZY05', 'I witnessed the procurement director accepting cash payments from a vendor at the building site.', 'Bribery', 'Revenue', 'Directorate Office', '2026-08-10', 50000.0, 'High', 'Closed', NULL, NULL, NULL, '2026-08-31 06:05:50.273770', '2026-08-31 06:05:50.834286');
INSERT INTO `complaints` (`id`, `tracking_id`, `description`, `category`, `department`, `location`, `incident_date`, `amount_involved`, `priority`, `status`, `next_status`, `verification_code`, `user_id`, `created_at`, `updated_at`) VALUES (2, 'COR-2026-ZNTP0C', 'Report on health inspector extortion demands in Central Hospital.', 'Extortion', 'Healthcare', 'Central Clinic', '2026-08-15', 15000.0, 'Low', 'Pending', NULL, NULL, 1, '2026-08-31 06:05:51.563751', '2026-08-31 06:05:51.584162');
INSERT INTO `complaints` (`id`, `tracking_id`, `description`, `category`, `department`, `location`, `incident_date`, `amount_involved`, `priority`, `status`, `next_status`, `verification_code`, `user_id`, `created_at`, `updated_at`) VALUES (3, 'COR-2026-77W952', 'I witnessed the procurement director accepting cash payments from a vendor at the building site.', 'Bribery', 'Revenue', 'Directorate Office', '2026-08-10', 50000.0, 'High', 'Closed', NULL, NULL, NULL, '2026-08-31 06:09:04.111561', '2026-08-31 06:09:04.694967');
INSERT INTO `complaints` (`id`, `tracking_id`, `description`, `category`, `department`, `location`, `incident_date`, `amount_involved`, `priority`, `status`, `next_status`, `verification_code`, `user_id`, `created_at`, `updated_at`) VALUES (4, 'COR-2026-80HOX4', 'Report on health inspector extortion demands in Central Hospital.', 'Extortion', 'Healthcare', 'Central Clinic', '2026-08-15', 15000.0, 'Medium', 'Closed', NULL, NULL, 2, '2026-08-31 06:09:05.422991', '2026-09-02 09:36:48.930328');
INSERT INTO `complaints` (`id`, `tracking_id`, `description`, `category`, `department`, `location`, `incident_date`, `amount_involved`, `priority`, `status`, `next_status`, `verification_code`, `user_id`, `created_at`, `updated_at`) VALUES (5, 'COR-2026-P3Z6WC', 'I witnessed the procurement director accepting cash payments from a vendor at the building site.', 'Bribery', 'Revenue', 'Directorate Office', '2026-08-10', 50000.0, 'High', 'Closed', NULL, NULL, NULL, '2026-09-02 08:43:26.290039', '2026-09-02 08:43:26.915838');
INSERT INTO `complaints` (`id`, `tracking_id`, `description`, `category`, `department`, `location`, `incident_date`, `amount_involved`, `priority`, `status`, `next_status`, `verification_code`, `user_id`, `created_at`, `updated_at`) VALUES (6, 'COR-2026-BQAIBH', 'Report on health inspector extortion demands in Central Hospital.', 'Extortion', 'Healthcare', 'Central Clinic', '2026-08-15', 15000.0, 'Medium', 'Closed', NULL, NULL, 3, '2026-09-02 08:43:27.642290', '2026-09-02 09:02:50.388600');
INSERT INTO `complaints` (`id`, `tracking_id`, `description`, `category`, `department`, `location`, `incident_date`, `amount_involved`, `priority`, `status`, `next_status`, `verification_code`, `user_id`, `created_at`, `updated_at`) VALUES (7, 'COR-2026-PU7MX3', 'I applied for a residential house construction building permit at the Municipal Corporation Town Planning department three months ago (Application Ref: BP-2026-8812). All structural engineering drawings, land title deeds, and property tax clearances were verified and found to be compliant with building bylaws.

However, the Senior Building Inspector refused to sign and release the final approval sanction order. When I met him in his cabin on August 20th, he explicitly demanded a cash bribe of Rs. 50,000 in an envelope, stating that without this unofficial ''speed payment'', my file would remain pending indefinitely and face arbitrary inspection objections. He instructed me to hand over the cash directly to his private assistant behind the counter. I have attached the original application receipt and an audio recording of the conversation.', 'Bribery', 'Municipality', 'Municipal Corporation Office, Town Planning Division, Ward 4', '2026-08-20', 50000.0, 'Medium', 'Pending', NULL, NULL, 5, '2026-09-02 09:48:52.185202', '2026-09-02 09:48:52.185212');

-- ------------------------------------------------------------------------------
-- Table Structure for `evidence`
-- ------------------------------------------------------------------------------
CREATE TABLE evidence (
	id INTEGER NOT NULL, 
	complaint_id INTEGER NOT NULL, 
	file_name VARCHAR(255) NOT NULL, 
	file_type VARCHAR(100) NOT NULL, 
	file_path VARCHAR(500) NOT NULL, 
	uploaded_at DATETIME, 
	PRIMARY KEY (id), 
	FOREIGN KEY(complaint_id) REFERENCES complaints (id) ON DELETE CASCADE
);

-- Dumping data for table `evidence` (1 records)
INSERT INTO `evidence` (`id`, `complaint_id`, `file_name`, `file_type`, `file_path`, `uploaded_at`) VALUES (1, 7, 'DEMO_Building_Permit_Application_Receipt.pdf', '.pdf', './uploads\f67e3c05-b824-4bd2-9552-1c1cb05eb9b6.pdf', '2026-09-02 09:48:52.246096');

-- ------------------------------------------------------------------------------
-- Table Structure for `ai_predictions`
-- ------------------------------------------------------------------------------
CREATE TABLE ai_predictions (
	id INTEGER NOT NULL, 
	complaint_id INTEGER NOT NULL, 
	predicted_category VARCHAR(100) NOT NULL, 
	category_confidence FLOAT NOT NULL, 
	predicted_priority VARCHAR(50) NOT NULL, 
	priority_confidence FLOAT NOT NULL, 
	recommended_department VARCHAR(100) NOT NULL, 
	department_confidence FLOAT NOT NULL, 
	duplicate_score FLOAT, 
	suspicious_flag BOOLEAN, 
	created_at DATETIME, 
	PRIMARY KEY (id), 
	FOREIGN KEY(complaint_id) REFERENCES complaints (id) ON DELETE CASCADE
);

-- Dumping data for table `ai_predictions` (7 records)
INSERT INTO `ai_predictions` (`id`, `complaint_id`, `predicted_category`, `category_confidence`, `predicted_priority`, `priority_confidence`, `recommended_department`, `department_confidence`, `duplicate_score`, `suspicious_flag`, `created_at`) VALUES (1, 1, 'Bribery', 90.0, 'High', 80.0, 'Government Procurement', 84.0, 0.0, 0, '2026-08-31 06:05:50.298868');
INSERT INTO `ai_predictions` (`id`, `complaint_id`, `predicted_category`, `category_confidence`, `predicted_priority`, `priority_confidence`, `recommended_department`, `department_confidence`, `duplicate_score`, `suspicious_flag`, `created_at`) VALUES (2, 2, 'Extortion', 80.0, 'Low', 70.0, 'Healthcare', 84.0, 0.0, 0, '2026-08-31 06:05:51.585231');
INSERT INTO `ai_predictions` (`id`, `complaint_id`, `predicted_category`, `category_confidence`, `predicted_priority`, `priority_confidence`, `recommended_department`, `department_confidence`, `duplicate_score`, `suspicious_flag`, `created_at`) VALUES (3, 3, 'Bribery', 90.0, 'High', 80.0, 'Government Procurement', 84.0, 100.0, 1, '2026-08-31 06:09:04.143495');
INSERT INTO `ai_predictions` (`id`, `complaint_id`, `predicted_category`, `category_confidence`, `predicted_priority`, `priority_confidence`, `recommended_department`, `department_confidence`, `duplicate_score`, `suspicious_flag`, `created_at`) VALUES (4, 4, 'Extortion', 80.0, 'Low', 70.0, 'Healthcare', 84.0, 100.0, 1, '2026-08-31 06:09:05.444508');
INSERT INTO `ai_predictions` (`id`, `complaint_id`, `predicted_category`, `category_confidence`, `predicted_priority`, `priority_confidence`, `recommended_department`, `department_confidence`, `duplicate_score`, `suspicious_flag`, `created_at`) VALUES (5, 5, 'Bribery', 68.0, 'High', 65.0, 'Government Procurement', 96.0, 100.0, 1, '2026-09-02 08:43:26.348863');
INSERT INTO `ai_predictions` (`id`, `complaint_id`, `predicted_category`, `category_confidence`, `predicted_priority`, `priority_confidence`, `recommended_department`, `department_confidence`, `duplicate_score`, `suspicious_flag`, `created_at`) VALUES (6, 6, 'Illegal Payment Demand', 68.0, 'High', 65.0, 'Healthcare', 96.0, 100.0, 1, '2026-09-02 08:43:27.667784');
INSERT INTO `ai_predictions` (`id`, `complaint_id`, `predicted_category`, `category_confidence`, `predicted_priority`, `priority_confidence`, `recommended_department`, `department_confidence`, `duplicate_score`, `suspicious_flag`, `created_at`) VALUES (7, 7, 'Bribery', 68.0, 'Medium', 65.0, 'Revenue', 96.0, 5.17, 0, '2026-09-02 09:48:52.221309');

-- ------------------------------------------------------------------------------
-- Table Structure for `complaint_updates`
-- ------------------------------------------------------------------------------
CREATE TABLE complaint_updates (
	id INTEGER NOT NULL, 
	complaint_id INTEGER NOT NULL, 
	status VARCHAR(50) NOT NULL, 
	previous_status VARCHAR(50), 
	note TEXT NOT NULL, 
	internal_note TEXT, 
	citizen_update TEXT, 
	updated_by VARCHAR(100) NOT NULL, 
	created_at DATETIME, 
	PRIMARY KEY (id), 
	FOREIGN KEY(complaint_id) REFERENCES complaints (id) ON DELETE CASCADE
);

-- Dumping data for table `complaint_updates` (39 records)
INSERT INTO `complaint_updates` (`id`, `complaint_id`, `status`, `previous_status`, `note`, `internal_note`, `citizen_update`, `updated_by`, `created_at`) VALUES (1, 1, 'Pending', NULL, 'Complaint submitted. Tracking ID generated and assigned to review queue.', 'Case file initialized. Raw complaint description and evidence mapped to database records. Queue status set to Pending.', 'Complaint received successfully. Unique tracking key generated. Assigned to the pending queue for review.', 'System', '2026-08-31 06:05:50.283887');
INSERT INTO `complaint_updates` (`id`, `complaint_id`, `status`, `previous_status`, `note`, `internal_note`, `citizen_update`, `updated_by`, `created_at`) VALUES (2, 1, 'Pending', 'Pending', 'AI analysis completed.', 'AI prediction completed. Category: Bribery (90.0%), Priority: High (80.0%), Dept: Government Procurement (84.0%).', 'AI triage complete. Initial category categorization and routing completed.', 'System', '2026-08-31 06:05:50.299369');
INSERT INTO `complaint_updates` (`id`, `complaint_id`, `status`, `previous_status`, `note`, `internal_note`, `citizen_update`, `updated_by`, `created_at`) VALUES (3, 1, 'Under Review', 'Pending', 'Case evaluations active. Found matching parameters.', 'Case evaluations active. Found matching parameters.', 'The case has been routed for triage review and detail verification.', 'admin', '2026-08-31 06:05:50.751546');
INSERT INTO `complaint_updates` (`id`, `complaint_id`, `status`, `previous_status`, `note`, `internal_note`, `citizen_update`, `updated_by`, `created_at`) VALUES (4, 1, 'Assigned', 'Under Review', 'Routing to land audit desk. Bypassing other queues.', 'Routing to land audit desk. Bypassing other queues. (Admin override: AI recommended ''Government Procurement'', but admin assigned ''Revenue'')', 'Case routed to Revenue Department.', 'admin', '2026-08-31 06:05:50.779656');
INSERT INTO `complaint_updates` (`id`, `complaint_id`, `status`, `previous_status`, `note`, `internal_note`, `citizen_update`, `updated_by`, `created_at`) VALUES (5, 1, 'Investigating', 'Assigned', 'Assigned land inspection officer. Desk code active.', 'Assigned land inspection officer. Desk code active.', 'Officer assigned. Investigation in active progress.', 'admin', '2026-08-31 06:05:50.802218');
INSERT INTO `complaint_updates` (`id`, `complaint_id`, `status`, `previous_status`, `note`, `internal_note`, `citizen_update`, `updated_by`, `created_at`) VALUES (6, 1, 'Resolved', 'Investigating', 'Internal verification completed successfully.', 'Resolution Type: Action Taken
Summary: Fines issued to registration desks. Verification files locked.
Internal Notes: Internal verification completed successfully.', 'Grievance resolved. System corrective action applied.', 'admin', '2026-08-31 06:05:50.822453');
INSERT INTO `complaint_updates` (`id`, `complaint_id`, `status`, `previous_status`, `note`, `internal_note`, `citizen_update`, `updated_by`, `created_at`) VALUES (7, 1, 'Closed', 'Resolved', 'Archiving case key details.', 'Archiving case key details.', 'Grievance case finalized and closed.', 'admin', '2026-08-31 06:05:50.843243');
INSERT INTO `complaint_updates` (`id`, `complaint_id`, `status`, `previous_status`, `note`, `internal_note`, `citizen_update`, `updated_by`, `created_at`) VALUES (8, 2, 'Pending', NULL, 'Complaint submitted. Tracking ID generated and assigned to review queue.', 'Case file initialized. Raw complaint description and evidence mapped to database records. Queue status set to Pending.', 'Complaint received successfully. Unique tracking key generated. Assigned to the pending queue for review.', 'System', '2026-08-31 06:05:51.575019');
INSERT INTO `complaint_updates` (`id`, `complaint_id`, `status`, `previous_status`, `note`, `internal_note`, `citizen_update`, `updated_by`, `created_at`) VALUES (9, 2, 'Pending', 'Pending', 'AI analysis completed.', 'AI prediction completed. Category: Extortion (80.0%), Priority: Low (70.0%), Dept: Healthcare (84.0%).', 'AI triage complete. Initial category categorization and routing completed.', 'System', '2026-08-31 06:05:51.585576');
INSERT INTO `complaint_updates` (`id`, `complaint_id`, `status`, `previous_status`, `note`, `internal_note`, `citizen_update`, `updated_by`, `created_at`) VALUES (10, 3, 'Pending', NULL, 'Complaint submitted. Tracking ID generated and assigned to review queue.', 'Case file initialized. Raw complaint description and evidence mapped to database records. Queue status set to Pending.', 'Complaint received successfully. Unique tracking key generated. Assigned to the pending queue for review.', 'System', '2026-08-31 06:09:04.127927');
INSERT INTO `complaint_updates` (`id`, `complaint_id`, `status`, `previous_status`, `note`, `internal_note`, `citizen_update`, `updated_by`, `created_at`) VALUES (11, 3, 'Pending', 'Pending', 'AI analysis completed.', 'AI prediction completed. Category: Bribery (90.0%), Priority: High (80.0%), Dept: Government Procurement (84.0%).', 'AI triage complete. Initial category categorization and routing completed.', 'System', '2026-08-31 06:09:04.143961');
INSERT INTO `complaint_updates` (`id`, `complaint_id`, `status`, `previous_status`, `note`, `internal_note`, `citizen_update`, `updated_by`, `created_at`) VALUES (12, 3, 'Under Review', 'Pending', 'Case evaluations active. Found matching parameters.', 'Case evaluations active. Found matching parameters.', 'The case has been routed for triage review and detail verification.', 'admin', '2026-08-31 06:09:04.607867');
INSERT INTO `complaint_updates` (`id`, `complaint_id`, `status`, `previous_status`, `note`, `internal_note`, `citizen_update`, `updated_by`, `created_at`) VALUES (13, 3, 'Assigned', 'Under Review', 'Routing to land audit desk. Bypassing other queues.', 'Routing to land audit desk. Bypassing other queues. (Admin override: AI recommended ''Government Procurement'', but admin assigned ''Revenue'')', 'Case routed to Revenue Department.', 'admin', '2026-08-31 06:09:04.637166');
INSERT INTO `complaint_updates` (`id`, `complaint_id`, `status`, `previous_status`, `note`, `internal_note`, `citizen_update`, `updated_by`, `created_at`) VALUES (14, 3, 'Investigating', 'Assigned', 'Assigned land inspection officer. Desk code active.', 'Assigned land inspection officer. Desk code active.', 'Officer assigned. Investigation in active progress.', 'admin', '2026-08-31 06:09:04.663028');
INSERT INTO `complaint_updates` (`id`, `complaint_id`, `status`, `previous_status`, `note`, `internal_note`, `citizen_update`, `updated_by`, `created_at`) VALUES (15, 3, 'Resolved', 'Investigating', 'Internal verification completed successfully.', 'Resolution Type: Action Taken
Summary: Fines issued to registration desks. Verification files locked.
Internal Notes: Internal verification completed successfully.', 'Grievance resolved. System corrective action applied.', 'admin', '2026-08-31 06:09:04.683294');
INSERT INTO `complaint_updates` (`id`, `complaint_id`, `status`, `previous_status`, `note`, `internal_note`, `citizen_update`, `updated_by`, `created_at`) VALUES (16, 3, 'Closed', 'Resolved', 'Archiving case key details.', 'Archiving case key details.', 'Grievance case finalized and closed.', 'admin', '2026-08-31 06:09:04.704139');
INSERT INTO `complaint_updates` (`id`, `complaint_id`, `status`, `previous_status`, `note`, `internal_note`, `citizen_update`, `updated_by`, `created_at`) VALUES (17, 4, 'Pending', NULL, 'Complaint submitted. Tracking ID generated and assigned to review queue.', 'Case file initialized. Raw complaint description and evidence mapped to database records. Queue status set to Pending.', 'Complaint received successfully. Unique tracking key generated. Assigned to the pending queue for review.', 'System', '2026-08-31 06:09:05.434284');
INSERT INTO `complaint_updates` (`id`, `complaint_id`, `status`, `previous_status`, `note`, `internal_note`, `citizen_update`, `updated_by`, `created_at`) VALUES (18, 4, 'Pending', 'Pending', 'AI analysis completed.', 'AI prediction completed. Category: Extortion (80.0%), Priority: Low (70.0%), Dept: Healthcare (84.0%).', 'AI triage complete. Initial category categorization and routing completed.', 'System', '2026-08-31 06:09:05.444910');
INSERT INTO `complaint_updates` (`id`, `complaint_id`, `status`, `previous_status`, `note`, `internal_note`, `citizen_update`, `updated_by`, `created_at`) VALUES (19, 5, 'Pending', NULL, 'Complaint submitted. Tracking ID generated and assigned to review queue.', 'Case file initialized. Raw complaint description and evidence mapped to database records. Queue status set to Pending.', 'Complaint received successfully. Unique tracking key generated. Assigned to the pending queue for review.', 'System', '2026-09-02 08:43:26.301596');
INSERT INTO `complaint_updates` (`id`, `complaint_id`, `status`, `previous_status`, `note`, `internal_note`, `citizen_update`, `updated_by`, `created_at`) VALUES (20, 5, 'Pending', 'Pending', 'AI analysis completed.', 'AI prediction completed. Category: Bribery (68.0%), Priority: High (65.0%), Dept: Government Procurement (96.0%).', 'AI triage complete. Initial category categorization and routing completed.', 'System', '2026-09-02 08:43:26.349372');
INSERT INTO `complaint_updates` (`id`, `complaint_id`, `status`, `previous_status`, `note`, `internal_note`, `citizen_update`, `updated_by`, `created_at`) VALUES (21, 5, 'Under Review', 'Pending', 'Case evaluations active. Found matching parameters.', 'Case evaluations active. Found matching parameters.', 'The case has been routed for triage review and detail verification.', 'admin', '2026-09-02 08:43:26.816263');
INSERT INTO `complaint_updates` (`id`, `complaint_id`, `status`, `previous_status`, `note`, `internal_note`, `citizen_update`, `updated_by`, `created_at`) VALUES (22, 5, 'Assigned', 'Under Review', 'Routing to land audit desk. Bypassing other queues.', 'Routing to land audit desk. Bypassing other queues. (Admin override: AI recommended ''Government Procurement'', but admin assigned ''Revenue'')', 'Case routed to Revenue Department.', 'admin', '2026-09-02 08:43:26.859097');
INSERT INTO `complaint_updates` (`id`, `complaint_id`, `status`, `previous_status`, `note`, `internal_note`, `citizen_update`, `updated_by`, `created_at`) VALUES (23, 5, 'Investigating', 'Assigned', 'Assigned land inspection officer. Desk code active.', 'Assigned land inspection officer. Desk code active.', 'Officer assigned. Investigation in active progress.', 'admin', '2026-09-02 08:43:26.882405');
INSERT INTO `complaint_updates` (`id`, `complaint_id`, `status`, `previous_status`, `note`, `internal_note`, `citizen_update`, `updated_by`, `created_at`) VALUES (24, 5, 'Resolved', 'Investigating', 'Internal verification completed successfully.', 'Resolution Type: Action Taken
Summary: Fines issued to registration desks. Verification files locked.
Internal Notes: Internal verification completed successfully.', 'Grievance resolved. System corrective action applied.', 'admin', '2026-09-02 08:43:26.904085');
INSERT INTO `complaint_updates` (`id`, `complaint_id`, `status`, `previous_status`, `note`, `internal_note`, `citizen_update`, `updated_by`, `created_at`) VALUES (25, 5, 'Closed', 'Resolved', 'Archiving case key details.', 'Archiving case key details.', 'Grievance case finalized and closed.', 'admin', '2026-09-02 08:43:26.926372');
INSERT INTO `complaint_updates` (`id`, `complaint_id`, `status`, `previous_status`, `note`, `internal_note`, `citizen_update`, `updated_by`, `created_at`) VALUES (26, 6, 'Pending', NULL, 'Complaint submitted. Tracking ID generated and assigned to review queue.', 'Case file initialized. Raw complaint description and evidence mapped to database records. Queue status set to Pending.', 'Complaint received successfully. Unique tracking key generated. Assigned to the pending queue for review.', 'System', '2026-09-02 08:43:27.651416');
INSERT INTO `complaint_updates` (`id`, `complaint_id`, `status`, `previous_status`, `note`, `internal_note`, `citizen_update`, `updated_by`, `created_at`) VALUES (27, 6, 'Pending', 'Pending', 'AI analysis completed.', 'AI prediction completed. Category: Illegal Payment Demand (68.0%), Priority: High (65.0%), Dept: Healthcare (96.0%).', 'AI triage complete. Initial category categorization and routing completed.', 'System', '2026-09-02 08:43:27.668117');
INSERT INTO `complaint_updates` (`id`, `complaint_id`, `status`, `previous_status`, `note`, `internal_note`, `citizen_update`, `updated_by`, `created_at`) VALUES (28, 6, 'Under Review', 'Pending', 'reviewed with the office person', 'reviewed with the office person', 'processed to next step', 'admin', '2026-09-02 08:58:12.315995');
INSERT INTO `complaint_updates` (`id`, `complaint_id`, `status`, `previous_status`, `note`, `internal_note`, `citizen_update`, `updated_by`, `created_at`) VALUES (29, 6, 'Assigned', 'Under Review', 'Rajesh Assigned', 'Rajesh Assigned', 'approved', 'admin', '2026-09-02 08:59:17.249779');
INSERT INTO `complaint_updates` (`id`, `complaint_id`, `status`, `previous_status`, `note`, `internal_note`, `citizen_update`, `updated_by`, `created_at`) VALUES (30, 6, 'Investigating', 'Assigned', 'Manoj , Hruday', 'Manoj , Hruday', 'Investigating', 'admin', '2026-09-02 08:59:58.782270');
INSERT INTO `complaint_updates` (`id`, `complaint_id`, `status`, `previous_status`, `note`, `internal_note`, `citizen_update`, `updated_by`, `created_at`) VALUES (31, 6, 'Resolved', 'Investigating', 'Duplicity predicted', 'Resolution Type: No Further Action
Summary: Duplicate case problems updated
Internal Notes: Duplicity predicted', 'NO further actions', 'admin', '2026-09-02 09:01:26.226810');
INSERT INTO `complaint_updates` (`id`, `complaint_id`, `status`, `previous_status`, `note`, `internal_note`, `citizen_update`, `updated_by`, `created_at`) VALUES (32, 6, 'Closed', 'Resolved', 'closed', 'closed', 'closed', 'admin', '2026-09-02 09:02:50.400825');
INSERT INTO `complaint_updates` (`id`, `complaint_id`, `status`, `previous_status`, `note`, `internal_note`, `citizen_update`, `updated_by`, `created_at`) VALUES (33, 4, 'Under Review', 'Pending', 'Assigning the officer', 'Assigning the officer', 'Assigning the officer', 'admin', '2026-09-02 09:30:21.845114');
INSERT INTO `complaint_updates` (`id`, `complaint_id`, `status`, `previous_status`, `note`, `internal_note`, `citizen_update`, `updated_by`, `created_at`) VALUES (34, 4, 'Assigned', 'Under Review', 'No file Audited', 'No file Audited', 'Lack Of info', 'admin', '2026-09-02 09:32:35.458064');
INSERT INTO `complaint_updates` (`id`, `complaint_id`, `status`, `previous_status`, `note`, `internal_note`, `citizen_update`, `updated_by`, `created_at`) VALUES (35, 4, 'Investigating', 'Assigned', 'Evidence duplicity', 'Evidence duplicity', 'Duplicity Predicted', 'admin', '2026-09-02 09:34:21.911586');
INSERT INTO `complaint_updates` (`id`, `complaint_id`, `status`, `previous_status`, `note`, `internal_note`, `citizen_update`, `updated_by`, `created_at`) VALUES (36, 4, 'Resolved', 'Investigating', 'No Further Actions', 'Resolution Type: No Further Action
Summary: No further Actions 
Internal Notes: No Further Actions', 'Rejected', 'admin', '2026-09-02 09:35:53.489965');
INSERT INTO `complaint_updates` (`id`, `complaint_id`, `status`, `previous_status`, `note`, `internal_note`, `citizen_update`, `updated_by`, `created_at`) VALUES (37, 4, 'Closed', 'Resolved', 'closed', 'closed', 'closed', 'admin', '2026-09-02 09:36:48.959737');
INSERT INTO `complaint_updates` (`id`, `complaint_id`, `status`, `previous_status`, `note`, `internal_note`, `citizen_update`, `updated_by`, `created_at`) VALUES (38, 7, 'Pending', NULL, 'Complaint submitted. Tracking ID generated and assigned to review queue.', 'Case file initialized. Raw complaint description and evidence mapped to database records. Queue status set to Pending.', 'Complaint received successfully. Unique tracking key generated. Assigned to the pending queue for review.', 'System', '2026-09-02 09:48:52.196502');
INSERT INTO `complaint_updates` (`id`, `complaint_id`, `status`, `previous_status`, `note`, `internal_note`, `citizen_update`, `updated_by`, `created_at`) VALUES (39, 7, 'Pending', 'Pending', 'AI analysis completed.', 'AI prediction completed. Category: Bribery (68.0%), Priority: Medium (65.0%), Dept: Revenue (96.0%).', 'AI triage complete. Initial category categorization and routing completed.', 'System', '2026-09-02 09:48:52.223605');

-- ------------------------------------------------------------------------------
-- Table Structure for `assignments`
-- ------------------------------------------------------------------------------
CREATE TABLE assignments (
	id INTEGER NOT NULL, 
	complaint_id INTEGER NOT NULL, 
	assigned_department VARCHAR(100) NOT NULL, 
	assigned_officer VARCHAR(100), 
	assigned_at DATETIME, 
	PRIMARY KEY (id), 
	FOREIGN KEY(complaint_id) REFERENCES complaints (id) ON DELETE CASCADE
);

-- Dumping data for table `assignments` (5 records)
INSERT INTO `assignments` (`id`, `complaint_id`, `assigned_department`, `assigned_officer`, `assigned_at`) VALUES (1, 1, 'Revenue', 'Officer A', '2026-08-31 06:05:50.768454');
INSERT INTO `assignments` (`id`, `complaint_id`, `assigned_department`, `assigned_officer`, `assigned_at`) VALUES (2, 3, 'Revenue', 'Officer A', '2026-08-31 06:09:04.626093');
INSERT INTO `assignments` (`id`, `complaint_id`, `assigned_department`, `assigned_officer`, `assigned_at`) VALUES (3, 5, 'Revenue', 'Officer A', '2026-09-02 08:43:26.844713');
INSERT INTO `assignments` (`id`, `complaint_id`, `assigned_department`, `assigned_officer`, `assigned_at`) VALUES (4, 6, 'Healthcare', 'Officer A', '2026-09-02 08:59:17.237564');
INSERT INTO `assignments` (`id`, `complaint_id`, `assigned_department`, `assigned_officer`, `assigned_at`) VALUES (5, 4, 'Healthcare', 'Officer B', '2026-09-02 09:32:35.445475');

-- ------------------------------------------------------------------------------
-- Table Structure for `audit_logs`
-- ------------------------------------------------------------------------------
CREATE TABLE audit_logs (
	id INTEGER NOT NULL, 
	user_id INTEGER, 
	action VARCHAR(255) NOT NULL, 
	complaint_id INTEGER, 
	timestamp DATETIME, 
	PRIMARY KEY (id), 
	FOREIGN KEY(user_id) REFERENCES admin_users (id) ON DELETE SET NULL, 
	FOREIGN KEY(complaint_id) REFERENCES complaints (id) ON DELETE CASCADE
);

-- Dumping data for table `audit_logs` (25 records)
INSERT INTO `audit_logs` (`id`, `user_id`, `action`, `complaint_id`, `timestamp`) VALUES (1, 1, 'Advanced status to Under Review.', 1, '2026-08-31 06:05:50.750368');
INSERT INTO `audit_logs` (`id`, `user_id`, `action`, `complaint_id`, `timestamp`) VALUES (2, 1, 'Assigned case to department ''Revenue'' (Admin override: AI recommended ''Government Procurement'', but admin assigned ''Revenue'')', 1, '2026-08-31 06:05:50.778429');
INSERT INTO `audit_logs` (`id`, `user_id`, `action`, `complaint_id`, `timestamp`) VALUES (3, 1, 'Assigned case to officer ''Officer A'' and started investigation.', 1, '2026-08-31 06:05:50.801074');
INSERT INTO `audit_logs` (`id`, `user_id`, `action`, `complaint_id`, `timestamp`) VALUES (4, 1, 'Marked complaint as Resolved. Resolution: Action Taken.', 1, '2026-08-31 06:05:50.821413');
INSERT INTO `audit_logs` (`id`, `user_id`, `action`, `complaint_id`, `timestamp`) VALUES (5, 1, 'Closed the case file.', 1, '2026-08-31 06:05:50.841890');
INSERT INTO `audit_logs` (`id`, `user_id`, `action`, `complaint_id`, `timestamp`) VALUES (6, 1, 'Advanced status to Under Review.', 3, '2026-08-31 06:09:04.605951');
INSERT INTO `audit_logs` (`id`, `user_id`, `action`, `complaint_id`, `timestamp`) VALUES (7, 1, 'Assigned case to department ''Revenue'' (Admin override: AI recommended ''Government Procurement'', but admin assigned ''Revenue'')', 3, '2026-08-31 06:09:04.636107');
INSERT INTO `audit_logs` (`id`, `user_id`, `action`, `complaint_id`, `timestamp`) VALUES (8, 1, 'Assigned case to officer ''Officer A'' and started investigation.', 3, '2026-08-31 06:09:04.661576');
INSERT INTO `audit_logs` (`id`, `user_id`, `action`, `complaint_id`, `timestamp`) VALUES (9, 1, 'Marked complaint as Resolved. Resolution: Action Taken.', 3, '2026-08-31 06:09:04.682248');
INSERT INTO `audit_logs` (`id`, `user_id`, `action`, `complaint_id`, `timestamp`) VALUES (10, 1, 'Closed the case file.', 3, '2026-08-31 06:09:04.702753');
INSERT INTO `audit_logs` (`id`, `user_id`, `action`, `complaint_id`, `timestamp`) VALUES (11, 1, 'Advanced status to Under Review.', 5, '2026-09-02 08:43:26.813756');
INSERT INTO `audit_logs` (`id`, `user_id`, `action`, `complaint_id`, `timestamp`) VALUES (12, 1, 'Assigned case to department ''Revenue'' (Admin override: AI recommended ''Government Procurement'', but admin assigned ''Revenue'')', 5, '2026-09-02 08:43:26.857749');
INSERT INTO `audit_logs` (`id`, `user_id`, `action`, `complaint_id`, `timestamp`) VALUES (13, 1, 'Assigned case to officer ''Officer A'' and started investigation.', 5, '2026-09-02 08:43:26.880798');
INSERT INTO `audit_logs` (`id`, `user_id`, `action`, `complaint_id`, `timestamp`) VALUES (14, 1, 'Marked complaint as Resolved. Resolution: Action Taken.', 5, '2026-09-02 08:43:26.902439');
INSERT INTO `audit_logs` (`id`, `user_id`, `action`, `complaint_id`, `timestamp`) VALUES (15, 1, 'Closed the case file.', 5, '2026-09-02 08:43:26.924827');
INSERT INTO `audit_logs` (`id`, `user_id`, `action`, `complaint_id`, `timestamp`) VALUES (16, 1, 'Advanced status to Under Review.', 6, '2026-09-02 08:58:12.312965');
INSERT INTO `audit_logs` (`id`, `user_id`, `action`, `complaint_id`, `timestamp`) VALUES (17, 1, 'Assigned case to department ''Healthcare''', 6, '2026-09-02 08:59:17.248376');
INSERT INTO `audit_logs` (`id`, `user_id`, `action`, `complaint_id`, `timestamp`) VALUES (18, 1, 'Assigned case to officer ''Officer A'' and started investigation.', 6, '2026-09-02 08:59:58.780927');
INSERT INTO `audit_logs` (`id`, `user_id`, `action`, `complaint_id`, `timestamp`) VALUES (19, 1, 'Marked complaint as Resolved. Resolution: No Further Action.', 6, '2026-09-02 09:01:26.225543');
INSERT INTO `audit_logs` (`id`, `user_id`, `action`, `complaint_id`, `timestamp`) VALUES (20, 1, 'Closed the case file.', 6, '2026-09-02 09:02:50.399421');
INSERT INTO `audit_logs` (`id`, `user_id`, `action`, `complaint_id`, `timestamp`) VALUES (21, 1, 'Advanced status to Under Review.', 4, '2026-09-02 09:30:21.842049');
INSERT INTO `audit_logs` (`id`, `user_id`, `action`, `complaint_id`, `timestamp`) VALUES (22, 1, 'Assigned case to department ''Healthcare''', 4, '2026-09-02 09:32:35.456511');
INSERT INTO `audit_logs` (`id`, `user_id`, `action`, `complaint_id`, `timestamp`) VALUES (23, 1, 'Assigned case to officer ''Officer B'' and started investigation.', 4, '2026-09-02 09:34:21.910553');
INSERT INTO `audit_logs` (`id`, `user_id`, `action`, `complaint_id`, `timestamp`) VALUES (24, 1, 'Marked complaint as Resolved. Resolution: No Further Action.', 4, '2026-09-02 09:35:53.488605');
INSERT INTO `audit_logs` (`id`, `user_id`, `action`, `complaint_id`, `timestamp`) VALUES (25, 1, 'Closed the case file.', 4, '2026-09-02 09:36:48.958255');

-- ------------------------------------------------------------------------------
-- Table Structure for `case_actions`
-- ------------------------------------------------------------------------------
CREATE TABLE case_actions (
	id INTEGER NOT NULL, 
	complaint_id INTEGER NOT NULL, 
	action_type VARCHAR(100) NOT NULL, 
	action_description VARCHAR(255) NOT NULL, 
	suggested_by_ai BOOLEAN, 
	approved_by VARCHAR(100), 
	created_at DATETIME, 
	PRIMARY KEY (id), 
	FOREIGN KEY(complaint_id) REFERENCES complaints (id) ON DELETE CASCADE
);

-- Dumping data for table `case_actions` (14 records)
INSERT INTO `case_actions` (`id`, `complaint_id`, `action_type`, `action_description`, `suggested_by_ai`, `approved_by`, `created_at`) VALUES (1, 1, 'Required Investigation Procedure', 'Review land logs', 1, NULL, '2026-08-31 06:05:50.769659');
INSERT INTO `case_actions` (`id`, `complaint_id`, `action_type`, `action_description`, `suggested_by_ai`, `approved_by`, `created_at`) VALUES (2, 1, 'Required Investigation Procedure', 'Preserve evidence files', 1, NULL, '2026-08-31 06:05:50.769666');
INSERT INTO `case_actions` (`id`, `complaint_id`, `action_type`, `action_description`, `suggested_by_ai`, `approved_by`, `created_at`) VALUES (3, 3, 'Required Investigation Procedure', 'Review land logs', 1, NULL, '2026-08-31 06:09:04.627389');
INSERT INTO `case_actions` (`id`, `complaint_id`, `action_type`, `action_description`, `suggested_by_ai`, `approved_by`, `created_at`) VALUES (4, 3, 'Required Investigation Procedure', 'Preserve evidence files', 1, NULL, '2026-08-31 06:09:04.627394');
INSERT INTO `case_actions` (`id`, `complaint_id`, `action_type`, `action_description`, `suggested_by_ai`, `approved_by`, `created_at`) VALUES (5, 5, 'Required Investigation Procedure', 'Review land logs', 1, NULL, '2026-09-02 08:43:26.846283');
INSERT INTO `case_actions` (`id`, `complaint_id`, `action_type`, `action_description`, `suggested_by_ai`, `approved_by`, `created_at`) VALUES (6, 5, 'Required Investigation Procedure', 'Preserve evidence files', 1, NULL, '2026-09-02 08:43:26.846289');
INSERT INTO `case_actions` (`id`, `complaint_id`, `action_type`, `action_description`, `suggested_by_ai`, `approved_by`, `created_at`) VALUES (7, 6, 'Required Investigation Procedure', 'Verify reporting incident details and locations', 1, NULL, '2026-09-02 08:59:17.239800');
INSERT INTO `case_actions` (`id`, `complaint_id`, `action_type`, `action_description`, `suggested_by_ai`, `approved_by`, `created_at`) VALUES (8, 6, 'Required Investigation Procedure', 'Confirm file integrity of attached visual media evidence', 1, NULL, '2026-09-02 08:59:17.239808');
INSERT INTO `case_actions` (`id`, `complaint_id`, `action_type`, `action_description`, `suggested_by_ai`, `approved_by`, `created_at`) VALUES (9, 6, 'Required Investigation Procedure', 'Request local municipal records of delay-causing clearance forms', 1, NULL, '2026-09-02 08:59:17.239813');
INSERT INTO `case_actions` (`id`, `complaint_id`, `action_type`, `action_description`, `suggested_by_ai`, `approved_by`, `created_at`) VALUES (10, 6, 'Required Investigation Procedure', 'Escalate if threats to life are reported', 1, NULL, '2026-09-02 08:59:17.239819');
INSERT INTO `case_actions` (`id`, `complaint_id`, `action_type`, `action_description`, `suggested_by_ai`, `approved_by`, `created_at`) VALUES (11, 4, 'Required Investigation Procedure', 'Verify reporting incident details and locations', 1, NULL, '2026-09-02 09:32:35.447311');
INSERT INTO `case_actions` (`id`, `complaint_id`, `action_type`, `action_description`, `suggested_by_ai`, `approved_by`, `created_at`) VALUES (12, 4, 'Required Investigation Procedure', 'Confirm file integrity of attached visual media evidence', 1, NULL, '2026-09-02 09:32:35.447319');
INSERT INTO `case_actions` (`id`, `complaint_id`, `action_type`, `action_description`, `suggested_by_ai`, `approved_by`, `created_at`) VALUES (13, 4, 'Required Investigation Procedure', 'Request local municipal records of delay-causing clearance forms', 1, NULL, '2026-09-02 09:32:35.447324');
INSERT INTO `case_actions` (`id`, `complaint_id`, `action_type`, `action_description`, `suggested_by_ai`, `approved_by`, `created_at`) VALUES (14, 4, 'Required Investigation Procedure', 'Escalate if threats to life are reported', 1, NULL, '2026-09-02 09:32:35.447328');
