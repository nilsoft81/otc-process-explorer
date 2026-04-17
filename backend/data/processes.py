# ── Helper ────────────────────────────────────────────────────────────────────
def _s(seq, name, *, level="L3", type="Process", sys="NA",
       r="NA", a="NA", c="NA",
       data="NA", change="", notes="", outcomes="", desc="", children=None):
    return {
        "seq": seq, "level": level, "name": name, "description": desc,
        "step_type": type, "system_tool": sys,
        "raci": {"r": r, "a": a, "c": c},
        "key_data_points": data, "change_highlight": change,
        "notes": notes, "decision_outcomes": outcomes,
        "children": children or [],
    }


# ══════════════════════════════════════════════════════════════════════════════
# L1-01  ORDER CAPTURE
# ══════════════════════════════════════════════════════════════════════════════
ORDER_CAPTURE = {
    "id": "order-capture",
    "l1_seq": "1",
    "l1_name": "Order Capture",
    "l1_color": "#0D9488",
    "l1_description": (
        "End-to-end stage covering all activities from initial client engagement "
        "through to project activation and budget establishment."
    ),
    "raci": {"r": "Various", "a": "Various", "c": "NA"},
    "system_tool": "CLM / CRM / ERP",
    "key_data_points": "NA",
    "stages": [

        # ── L2-01  Customer & Contract Setup ──────────────────────────────────
        {
            "id": "customer-contract-setup",
            "seq": "1.1",
            "name": "Customer & Contract Setup (incl. portal setup)",
            "description": (
                "Establish the client record, negotiate and execute the master "
                "services agreement, set up the client portal, and configure entitlements."
            ),
            "color": "#0D9488",
            "system_tool": "CLM / CRM",
            "raci": {"r": "Operations", "a": "Operations", "c": "NA"},
            "key_data_points": "NA",
            "change_highlight": "Portal setup to be automated via CLM integration in To-Be",
            "steps": [
                _s("1.1.1", "Customer Initiation",
                   sys="CRM", r="Sales", a="Sales",
                   data="Customer ID, Parent Customer ID, Customer Name, Industry",
                   change="To-Be: CRM → CLM auto-sync eliminates manual re-entry",
                   desc="Receive new client / opportunity trigger from Sales/Business Development. "
                        "Capture preliminary customer details (name, region, industry)."),

                _s("1.1.2", "Customer Master Data Creation & Hierarchy Setup",
                   sys="CRM", r="Operations", a="Operations",
                   data="Customer master data",
                   desc="Create customer record in CRM/ERP. Perform duplicate check. "
                        "Assign customer ID and account owner. Define parent/child relationships."),

                _s("1.1.3", "Credit & Compliance Screening",
                   sys="ERP", r="GFS - Credit", a="GFS - Credit", c="Sales",
                   data="Credit & risk score",
                   desc="Perform credit check / financial due diligence. Conduct compliance checks. "
                        "Assign provisional payment terms and risk rating."),

                _s("1.1.4", "Master Services Agreement (MSA) Management",
                   sys="CLM", r="Legal", a="Legal",
                   type="Process/Decision",
                   desc="Check for existing MSA and validate applicability. Draft MSA if required. "
                        "Negotiate legal and high-level commercial terms. Execute and store agreement.",
                   children=[
                       _s("1.1.4.1", "Select MSA Template",
                          level="L4", sys="CLM", r="Legal", a="Legal",
                          notes="Template library maintained by Legal",
                          desc="Choose the appropriate MSA template based on division and client region."),

                       _s("1.1.4.2", "Populate High-level Commercial Terms",
                          level="L4", sys="CLM", r="Legal", a="Legal", c="Sales",
                          data="Billing terms and frequency",
                          change="To-Be: rate card auto-populated from CRM opportunity",
                          desc="Enter commercial details including commercial model, rate card, "
                               "discount, payment terms, currency and billing frequency."),

                       _s("1.1.4.3", "Non-Standard Terms?",
                          level="L4", sys="CLM", r="Legal", a="Legal",
                          type="Decision",
                          data="Billing terms and frequency",
                          outcomes="Yes – legal review | No – proceed to send",
                          desc="Determine whether any negotiated terms deviate from the approved playbook."),

                       _s("1.1.4.4", "Approval for Non-Standard Terms",
                          level="L4", sys="CLM", r="Legal", a="Legal",
                          data="Billing terms and frequency",
                          desc="Obtain required approvals for any non-standard commercial or legal terms "
                               "before proceeding to contract execution."),

                       _s("1.1.4.5", "Send Contract to Client",
                          level="L4", sys="CLM", r="Sales", a="Sales",
                          change="To-Be: send triggered automatically on approval",
                          desc="Transmit final contract to client signatories via e-signature link. "
                               "Log send date and expected return date in CLM."),

                       _s("1.1.4.6", "Client Reviews & Signs Contract",
                          level="L4", sys="DocuSign", r="Client (External)", a="Sales",
                          notes="Redline cycle may add 5–15 business days",
                          desc="Client reviews the contract, raises redlines if applicable, "
                               "and executes via e-signature platform."),

                       _s("1.1.4.7", "Contract Fully Executed?",
                          level="L4", sys="CLM", r="Legal", a="Legal",
                          type="Decision",
                          outcomes="Yes – proceed | No – chase signatures",
                          change="To-Be: CLM auto-alerts on unsigned docs after 5 days",
                          desc="Confirm all counterparty signatures are captured and the contract "
                               "is legally binding before proceeding."),

                       _s("1.1.4.8", "Set Up Client Portal & Entitlements",
                          level="L4", sys="CLM / Client Portal", r="Operations", a="Operations",
                          change="To-Be: portal provisioned automatically on contract execution",
                          desc="Provision the client's portal access, configure project visibility, "
                               "set user roles and permissions."),

                       _s("1.1.4.9", "Notify Order Management to Proceed",
                          level="L4", sys="CLM", r="Operations", a="Operations",
                          change="To-Be: structured data handoff replaces email; drives L2-02 automatically",
                          desc="Send internal handoff notification with contract summary, billing model, "
                               "PO reference, and project start date to the Order Management team."),
                   ]),
            ],
        },

        # ── L2-02  Order Entry & Validation ───────────────────────────────────
        {
            "id": "order-entry-validation",
            "seq": "1.2",
            "name": "Order Entry & Validation (incl. POs)",
            "description": (
                "Execute Statement of Work (SOW) including scope, deliverables, and pricing. "
                "Set up the contract/order in the ERP/PSA system and prepare for project setup."
            ),
            "color": "#7C3AED",
            "system_tool": "Oracle / Maconomy",
            "raci": {"r": "Operations", "a": "Operations", "c": "NA"},
            "key_data_points": "NA",
            "steps": [
                _s("1.2.1", "SOW Initiation",
                   sys="CLM / Email", r="Operations", a="Operations",
                   desc="Receive new project opportunity (following 1.1.4.9 for new customers; "
                        "point of origination for existing customers)."),

                _s("1.2.2", "Draft SOW",
                   sys="CLM", r="Operations", a="Operations",
                   desc="Develop scope, deliverables and timelines. Define pricing and commercial terms. "
                        "Align resourcing and effort with delivery. Generate SOW document.",
                   children=[
                       _s("1.2.2.1", "Define Scope & Delivery Approach",
                          level="L4", sys="CLM", r="Operations", a="Operations",
                          data="Deliverables, Timeline, Milestones, Dependencies",
                          desc="Establish deliverables, timeline, milestones, dependencies, etc."),

                       _s("1.2.2.2", "Define Pricing & Commercial Terms",
                          level="L4", sys="CLM", r="Operations", a="Operations",
                          data="Fees, Pricing Structure, Billing cadence, Billing triggers",
                          desc="Determine pricing model, fees, billing structure and key commercial terms."),

                       _s("1.2.2.3", "Define Resourcing & Effort",
                          level="L4", sys="CLM", r="Operations", a="Operations",
                          data="Resourcing",
                          desc="Define resourcing and effort requirements to support delivery."),

                       _s("1.2.2.4", "Draft SOW Document (CLM)",
                          level="L4", sys="CLM", r="Operations", a="Operations",
                          desc="Generate and populate SOW using standardised templates. "
                               "Define billable vs. non-billable guidelines."),
                   ]),

                _s("1.2.3", "Send SOW to Client",
                   sys="Email", r="Operations", a="Operations",
                   desc="Review and modify with client. Finalise SOW details."),

                _s("1.2.4", "Client Reviews & Signs Contract",
                   sys="DocuSign", r="Operations", a="Operations",
                   desc="Client executes the final SOW via e-signature platform."),

                _s("1.2.5", "PO Intake, Validation & Routing",
                   sys="Email / Portal / EDI", r="GFS", a="GFS",
                   desc="Receive, validate and route purchase orders from client. Ensure alignment "
                        "with executed SOW and set up in ERP.",
                   children=[
                       _s("1.2.5.1", "PO Intake",
                          level="L4", sys="Email / Portal / EDI", r="GFS", a="GFS",
                          desc="Receive PO via email, portal or EDI channel."),

                       _s("1.2.5.2", "PO Completeness & Validity Check",
                          level="L4", sys="Email / Portal / EDI", r="GFS", a="GFS",
                          desc="Verify PO is complete, valid and contains required fields."),

                       _s("1.2.5.3", "PO Alignment to SOW?",
                          level="L4", sys="Email / Portal / EDI / CLM", r="GFS", a="GFS",
                          type="Decision",
                          outcomes="Aligned – proceed | Discrepancy – resolve",
                          desc="Check PO value, scope and terms align with the executed SOW."),

                       _s("1.2.5.4", "PO Discrepancy Resolution",
                          level="L4", sys="Email / Portal / EDI", r="GFS", a="GFS", c="Operations",
                          desc="Resolve any discrepancies between PO and SOW with client and Operations."),

                       _s("1.2.5.5", "PO Routing & Assignment",
                          level="L4", sys="CLM", r="GFS", a="GFS",
                          desc="Route validated PO to the appropriate team and link to CLM contract."),

                       _s("1.2.5.6", "PO Recording & System Linkage",
                          level="L4", sys="ERP", r="GFS", a="GFS",
                          data="PO",
                          desc="Record PO details in ERP and link to the relevant project/contract record."),
                   ]),

                _s("1.2.6", "Contract Setup / Order Entry",
                   sys="ERP", r="Operations", a="Operations",
                   data="Deliverables, Timeline, Milestones, Dependencies, Fees, Pricing Structure, "
                        "Billing cadence, Billing triggers, Resourcing, Revenue recognition method",
                   desc="Create contract/order record. Input pricing, billing structure and key terms. "
                        "Link to customer. Configure billing schedule and triggers. "
                        "Set revenue recognition method."),

                _s("1.2.7", "Data Validation",
                   sys="ERP", r="Operations", a="Operations",
                   type="Decision (automated)",
                   desc="Validate data across CRM, CLM and ERP. Confirm readiness for delivery."),

                _s("1.2.8", "Internal Approval",
                   sys="ERP", r="Operations", a="Operations",
                   desc="Obtain required internal approvals before triggering project activation."),
            ],
        },

        # ── L2-03  Project Activation & Budgeting ────────────────────────────
        {
            "id": "project-activation-budgeting",
            "seq": "1.3",
            "name": "Project Activation & Budgeting",
            "description": (
                "Create and structure the project in the ERP/PSA system aligned to the executed SOW. "
                "Establish budgets, assign resources, and configure time, expense, and billing readiness."
            ),
            "color": "#D97706",
            "system_tool": "PSA",
            "raci": {"r": "Operations", "a": "Operations", "c": "Finance"},
            "key_data_points": "NA",
            "steps": [
                _s("1.3.1", "Project Initiation",
                   sys="PSA", r="Operations", a="Operations",
                   desc="Receive signed SOW. Assign project manager."),

                _s("1.3.2", "Project Structure Setup",
                   sys="PSA", r="Operations", a="Operations",
                   desc="Create project record linked to SOW and customer data. "
                        "Define work packages (phases, activities, timeline, milestones) aligned to SOW."),

                _s("1.3.3", "Budget Setup",
                   sys="PSA", r="Operations", a="Operations", c="Finance",
                   desc="Load revenue baseline from SOW. Define cost budget based on resourcing plan. "
                        "Establish margin baseline."),

                _s("1.3.4", "Initial Resourcing Alignment",
                   sys="PSA", r="Operations", a="Operations",
                   desc="Validate roles and capacity assumptions against SOW. "
                        "Initiate coordination with resource management for staffing requirements."),

                _s("1.3.5", "Time & Expense Enablement",
                   sys="PSA/Concur", r="Operations", a="Operations",
                   desc="Enable time entry against project. Configure expense policies and categories. "
                        "Validate billable vs non-billable guidelines. "
                        "Load and synchronise project codes to expense systems."),

                _s("1.3.6", "Billing Readiness Validation",
                   sys="PSA", r="Operations", a="Operations",
                   desc="Confirm billing configuration is correctly linked to project. "
                        "Validate invoice triggers and schedule alignment. "
                        "Ensure bill-to details and client data are correct."),

                _s("1.3.7", "Project Governance & Controls Setup",
                   sys="PSA", r="Operations", a="Operations",
                   desc="Define reporting cadence (status, financials). "
                        "Establish change control process. Define approval matrix."),

                _s("1.3.8", "Project Activation (Go-Live)",
                   sys="PSA", r="Operations", a="Operations",
                   data="Project code(s)",
                   desc="Validate all setup components are complete. "
                        "Activate project for time, cost and billing. "
                        "Notify stakeholders (Delivery, Finance, Sales)."),
            ],
        },
    ],
}


# ══════════════════════════════════════════════════════════════════════════════
# L1-03  SERVICE DELIVERY
# ══════════════════════════════════════════════════════════════════════════════
SERVICE_DELIVERY = {
    "id": "service-delivery",
    "l1_seq": "3",
    "l1_name": "Service Delivery",
    "l1_color": "#2563EB",
    "l1_description": (
        "All operational activities performed during project execution: time capture, "
        "expense management, cost allocation and milestone / progress monitoring. "
        "Feeds directly into revenue recognition and invoicing."
    ),
    "raci": {"r": "Operations", "a": "Operations", "c": "NA"},
    "system_tool": "PSA",
    "key_data_points": "NA",
    "stages": [

        # ── L2  3.1  Track Time ───────────────────────────────────────────────
        {
            "id": "track-time",
            "seq": "3.1",
            "name": "Track Time",
            "description": (
                "Capture and approve time worked on projects to enable accurate "
                "cost tracking, billing and revenue recognition."
            ),
            "color": "#2563EB",
            "system_tool": "PSA",
            "raci": {"r": "Operations", "a": "Operations", "c": "NA"},
            "key_data_points": "NA",
            "change_highlight": (
                "To-Be: weekly timesheet submission enforced via PSA automated reminders; "
                "approval SLA tracked in system"
            ),
            "steps": [
                _s("3.1.1", "Time Entry Capture",
                   sys="PSA", r="Operations", a="Operations",
                   change="To-Be: PSA sends automated daily nudge if timesheet not started by Thursday; "
                          "hard lock on Friday EOD",
                   notes="Daily entry strongly encouraged; weekly submission minimum",
                   desc="Record time worked against project tasks, activities and billing category "
                        "(billable, non-billable, internal)."),

                _s("3.1.2", "Timesheet Review & Approval",
                   sys="PSA", r="Operations", a="Operations",
                   notes="SLA: PM approval within 2 business days of submission",
                   desc="Project Manager reviews submitted time for accuracy and completeness. "
                        "Approves or rejects with comments."),

                _s("3.1.3", "PM Approval Decision",
                   sys="PSA", r="Operations", a="Operations",
                   type="Decision",
                   outcomes="Approved | Rejected – return to resource",
                   desc="PM makes approval decision on the submitted timesheet."),

                _s("3.1.4", "Timesheet Posting & Update",
                   sys="PSA", r="Operations", a="Operations",
                   data="Time and materials",
                   change="To-Be: auto-post to ERP on PM approval; no manual re-keying",
                   notes="Integration: PSA → ERP real-time sync",
                   desc="Approved timesheet is locked in PSA and actuals are posted to the ERP project ledger. "
                        "Billable hours are flagged for revenue recognition and invoicing runs."),

                _s("3.1.5", "Notify Revenue & Billing Teams",
                   sys="PSA", r="Operations", a="Operations",
                   change="To-Be: automated trigger eliminates manual handoff email to Finance",
                   notes="Feeds Stage 4 rev rec and Stage 5 invoicing",
                   desc="PSA triggers automated notification to Revenue Accounting and Billing that "
                        "approved billable hours are available for the current period."),
            ],
        },

        # ── L2  3.2  Track Expenses ───────────────────────────────────────────
        {
            "id": "track-expenses",
            "seq": "3.2",
            "name": "Track Expenses",
            "description": (
                "Capture, validate and approve project-related expenses. "
                "Approved expenses are posted to the project cost ledger and passed to billing."
            ),
            "color": "#7C3AED",
            "system_tool": "Concur/ERP",
            "raci": {"r": "Operations", "a": "Operations", "c": "NA"},
            "key_data_points": "NA",
            "change_highlight": (
                "To-Be: Concur integrated with ERP and PSA for automated project code validation "
                "and real-time cost posting"
            ),
            "steps": [
                _s("3.2.1", "Expense Capture",
                   sys="Concur", r="Operations", a="Operations",
                   change="To-Be: Concur mobile app enables real-time receipt capture at point of expenditure",
                   notes="30-day submission policy; late claims flagged for Finance approval",
                   desc="Record project-related expenses with supporting documentation, "
                        "tagged to the applicable project code(s)."),

                _s("3.2.2", "Expense Review & Approval",
                   sys="Concur", r="Operations", a="Operations",
                   notes="SLA: PM approval within 3 business days",
                   desc="Review expenses for policy compliance and accuracy. "
                        "Approve or reject expense claims."),

                _s("3.2.3", "PM Approval Decision",
                   sys="Concur", r="Operations", a="Operations",
                   type="Decision",
                   outcomes="Approved | Rejected – return to resource",
                   desc="PM makes approval decision on the submitted expense report."),

                _s("3.2.4", "Post to Project Cost Ledger & Flag for Billing",
                   sys="Concur/ERP", r="Operations", a="Operations",
                   data="Billable and non-billable out of pocket expenses",
                   change="To-Be: real-time Concur → ERP sync; rechargeable flag auto-set from contract rules",
                   notes="Feeds Stage 5 invoicing (expense recharge lines)",
                   desc="Post approved expenses to the system. Update project financial records. "
                        "Rechargeable items automatically flagged for inclusion in next client invoice run."),
            ],
        },

        # ── L2  3.3  Track & Allocate Other Costs ────────────────────────────
        {
            "id": "track-allocate-costs",
            "seq": "3.3",
            "name": "Track & Allocate Other Costs",
            "description": (
                "Capture and allocate project costs not sourced from timesheets or expense claims "
                "(e.g., overheads, sub-contractor invoices, software licences, shared service allocations)."
            ),
            "color": "#0891B2",
            "system_tool": "ERP/PSA",
            "raci": {"r": "GFS", "a": "GFS", "c": "Operations"},
            "key_data_points": "NA",
            "steps": [
                _s("3.3.1", "Cost Identification & Capture",
                   sys="ERP", r="GFS", a="GFS", c="Operations",
                   notes="Monthly cost review meeting; output is list of items requiring action",
                   desc="Identify other project-related costs (e.g., subcontractors, overhead allocations). "
                        "Capture cost details from source systems or inputs."),

                _s("3.3.2", "Cost Allocation",
                   sys="ERP", r="GFS", a="GFS",
                   change="To-Be: ERP allocation engine runs automatically at period end using "
                          "pre-configured drivers",
                   notes="Allocation methodology approved annually by Finance leadership",
                   desc="Apply agreed allocation methodology for shared costs across active projects."),

                _s("3.3.3", "Cost Posting",
                   sys="ERP/PSA", r="GFS", a="GFS",
                   data="Pass-through costs",
                   notes="Monthly: input to project health review; flags fed to Stage 4 rev rec if "
                         "scope change impacts revenue",
                   desc="Post allocated costs in the ERP to project financials. "
                        "Update project cost records and enable downstream reporting."),
            ],
        },

        # ── L2  3.4  Milestone & Progress Monitoring ──────────────────────────
        {
            "id": "milestone-progress-monitoring",
            "seq": "3.4",
            "name": "Milestone & Progress Monitoring",
            "description": (
                "Monitor project progress and milestone completion to support "
                "delivery tracking, billing triggers and revenue recognition."
            ),
            "color": "#059669",
            "system_tool": "PSA / ERP",
            "raci": {"r": "Operations", "a": "Operations", "c": "NA"},
            "key_data_points": "NA",
            "change_highlight": (
                "To-Be: PSA provides real-time project health dashboard; "
                "replaces manual status reporting in spreadsheets"
            ),
            "steps": [
                _s("3.4.1", "Progress Tracking",
                   sys="PSA", r="Operations", a="Operations",
                   change="To-Be: PSA auto-calculates % complete from logged hours vs estimated hours",
                   notes="Weekly update mandatory for all active projects",
                   desc="Track project progress against defined milestones and deliverables. "
                        "Update task completion status and percentage-complete in PSA."),

                _s("3.4.2", "Milestone Validation",
                   sys="PSA", r="Operations", a="Operations",
                   desc="Confirm milestone completion and obtain required approvals or sign-off.",
                   children=[
                       _s("3.4.2.1", "Milestone Completion Confirmed?",
                          level="L4", sys="PSA", r="Operations", a="Operations",
                          type="Decision",
                          outcomes="Yes – initiate sign-off | No – continue monitoring",
                          desc="Confirm that milestone deliverables have been completed in line with "
                               "agreed scope and acceptance criteria."),

                       _s("3.4.2.2", "Prepare Milestone Completion Evidence",
                          level="L4", sys="PSA", r="Operations", a="Operations",
                          notes="Stored in project document repository; linked to PSA milestone record",
                          desc="Compile supporting documentation (deliverables, sign-offs, acceptance records). "
                               "Ensure evidence is complete and aligned with contractual requirements."),

                       _s("3.4.2.3", "Client Acceptance Obtained?",
                          level="L4", sys="NA", r="Operations", a="Operations",
                          type="Decision",
                          outcomes="Yes – proceed | No – resolve with client",
                          desc="Confirm whether client acceptance has been formally obtained."),

                       _s("3.4.2.4", "Client Acceptance Confirmation",
                          level="L4", sys="NA", r="Operations", a="Operations",
                          desc="Record and file formal client acceptance confirmation in project records."),
                   ]),

                _s("3.4.3", "Progress & Milestone Update",
                   sys="PSA", r="Operations", a="Operations",
                   data="PoC tracking",
                   change="To-Be: PSA auto-triggers billing event and rev rec update on milestone sign-off",
                   notes="Feeds Stage 4 rev rec and Stage 5 invoicing",
                   desc="PM marks milestone as complete and accepted in PSA."),

                _s("3.4.4", "Trigger Billing Event",
                   sys="PSA / ERP", r="Operations", a="Operations",
                   data="Billing trigger",
                   change="To-Be: PSA auto-triggers billing event and rev rec update on milestone sign-off",
                   notes="Feeds Stage 4 rev rec and Stage 5 invoicing",
                   desc="System automatically creates billing event and notifies the Billing team to "
                        "generate the invoice. Updates revenue recognition schedule."),
            ],
        },
    ],
}


# ══════════════════════════════════════════════════════════════════════════════
# L1-04  REVENUE RECOGNITION
# ══════════════════════════════════════════════════════════════════════════════
REVENUE_RECOGNITION = {
    "id": "revenue-recognition",
    "l1_seq": "4",
    "l1_name": "Revenue Recognition",
    "l1_color": "#DC2626",
    "l1_description": (
        "All activities to recognise revenue in accordance with revenue recognition rules, "
        "posting adjustments and reconciling deferred / accrued balances."
    ),
    "raci": {"r": "GFS", "a": "GFS", "c": "NA"},
    "system_tool": "ERP",
    "key_data_points": "NA",
    "stages": [

        # ── L2  4.1  Revenue Execution & Posting ──────────────────────────────
        {
            "id": "revenue-execution-posting",
            "seq": "4.1",
            "name": "Revenue Execution & Posting",
            "description": (
                "Calculate revenue based on contract terms/milestones and post journal entries to the GL."
            ),
            "color": "#DC2626",
            "system_tool": "ERP",
            "raci": {"r": "GFS", "a": "GFS", "c": "NA"},
            "key_data_points": "NA",
            "change_highlight": (
                "To-Be: automated rev rec run replaces manual journal entry for standard engagements"
            ),
            "steps": [
                _s("4.1.1", "Revenue Recognition Trigger Initiation",
                   sys="ERP", r="GFS", a="GFS",
                   change="To-Be: scheduled ERP job replaces manual trigger",
                   notes="Run on last working day of period",
                   desc="Trigger revenue recognition cycle (e.g., period-end). "
                        "Validate alignment with SOW / MSA terms and revenue recognition rules."),

                _s("4.1.2", "Revenue Readiness Validation",
                   sys="ERP", r="GFS", a="GFS",
                   notes="Flag variances >$10k for controller sign-off",
                   desc="Confirm required inputs are complete (e.g., approved timesheets, "
                        "cross-check fixed fee to POC, etc.)."),

                _s("4.1.3", "Exceptions Identified?",
                   sys="ERP", r="GFS", a="GFS",
                   type="Decision",
                   outcomes="Yes – adjust | No – post",
                   desc="Identify missing, incomplete or inconsistent data (e.g., timing differences)."),

                _s("4.1.4", "Exception Resolution",
                   sys="ERP", r="GFS", a="GFS", c="Operations",
                   desc="Resolve identified exceptions."),

                _s("4.1.5", "Revenue Execution (incl. Accruals & Deferrals)",
                   sys="ERP", r="GFS", a="GFS",
                   desc="Revenue is calculated according to revenue recognition rules aligned to "
                        "contract terms. Includes accruals (revenue earned but not billed) and "
                        "deferrals (revenue billed but not yet earned)."),

                _s("4.1.6", "Journal Entry Preparation & Routing",
                   sys="ERP", r="GFS", a="GFS",
                   desc="Prepare journal entries for revenue recognition and route for approval."),

                _s("4.1.7", "Journal Entry Approvals",
                   sys="ERP", r="GFS", a="GFS",
                   notes="Dual approval required above agreed threshold",
                   desc="Obtain required approvals on revenue journal entries before posting."),

                _s("4.1.8", "Revenue Posting",
                   sys="ERP", r="GFS", a="GFS",
                   data="Accruals, Deferrals, Unbilled AR",
                   desc="Post revenue journal entries to the general ledger. System updates deferred "
                        "revenue, accrued revenue, and unbilled AR balances accordingly."),
            ],
        },

        # ── L2  4.2  Adjustments & True-Ups ──────────────────────────────────
        {
            "id": "adjustments-true-ups",
            "seq": "4.2",
            "name": "Adjustments & True-Ups (e.g. Rebates)",
            "description": (
                "Process post-recognition adjustments and true-ups to reflect updated commercial "
                "or financial information (e.g., rebates, contract modifications, scope changes)."
            ),
            "color": "#9333EA",
            "system_tool": "ERP / CLM",
            "raci": {"r": "GFS", "a": "GFS", "c": "NA"},
            "key_data_points": "NA",
            "steps": [
                _s("4.2.1", "Adjustment Trigger Initiated",
                   sys="ERP / CLM", r="GFS", a="GFS", c="Operations",
                   notes="Source data: CLM for contract terms; ERP for actuals",
                   desc="Identify events requiring revenue adjustment or true-up "
                        "(e.g., rebates, credits, pricing changes, change orders)."),

                _s("4.2.2", "Adjustment Review And Validation",
                   sys="ERP", r="GFS", a="GFS",
                   desc="Review the nature, amount and rationale for the adjustment. "
                        "Validate supporting documentation and approvals. Document rationale in ERP."),

                _s("4.2.3", "Adjustment Calculation",
                   sys="ERP", r="GFS", a="GFS",
                   notes="Supporting calc to be retained for audit",
                   desc="Calculate the financial impact of the adjustment or true-up. "
                        "Determine the required accounting treatment.",
                   children=[
                       _s("4.2.4", "Journal Entry Preparation & Routing",
                          level="L4", sys="ERP", r="GFS", a="GFS",
                          desc="Prepare adjustment journal entries and route for approval."),

                       _s("4.2.5", "Journal Entry Approvals",
                          level="L4", sys="ERP", r="GFS", a="GFS",
                          desc="Obtain required approvals on adjustment journal entries before posting."),
                   ]),

                _s("4.2.6", "Adjustment Posting",
                   sys="ERP", r="GFS", a="GFS",
                   data="Adjustments and true-ups to revenue",
                   change="To-Be: ERP → EPM auto-sync reduces manual reforecast effort",
                   desc="Post adjustment or true-up journal entries to the general ledger. "
                        "Update project and financial records accordingly."),
            ],
        },
    ],
}


# ══════════════════════════════════════════════════════════════════════════════
# L1-05  INVOICING & BILLING
# ══════════════════════════════════════════════════════════════════════════════
INVOICING_BILLING = {
    "id": "invoicing-billing",
    "l1_seq": "5",
    "l1_name": "Invoicing & Billing",
    "l1_color": "#D97706",
    "l1_description": (
        "End-to-end process to prepare, review, approve, and issue client invoices "
        "including client review cycles."
    ),
    "raci": {"r": "GFS", "a": "GFS", "c": "Operations"},
    "system_tool": "ERP",
    "key_data_points": "NA",
    "stages": [

        # ── L2  5.1  Invoice Preparation & Internal Review ────────────────────
        {
            "id": "invoice-preparation-internal-review",
            "seq": "5.1",
            "name": "Invoice Preparation & Internal Review (incl. Billing on Behalf)",
            "description": (
                "Generate draft invoices from ERP based on approved timesheets, expenses or "
                "milestone triggers. Perform internal quality review before sending to client."
            ),
            "color": "#D97706",
            "system_tool": "ERP",
            "raci": {"r": "GFS", "a": "GFS", "c": "Operations"},
            "key_data_points": "Billing trigger, Draft invoice, PO reference",
            "change_highlight": (
                "To-Be: invoice auto-generated on timesheet approval or milestone sign-off"
            ),
            "steps": [
                _s("5.1.1", "Invoice Trigger Initiated",
                   sys="ERP", r="GFS", a="GFS",
                   change="To-Be: automated pull from approved timesheets; no manual extraction",
                   desc="Trigger invoice cycle based on defined billing events (e.g., scheduled "
                        "billing date, milestone completion, billable activity)."),

                _s("5.1.2", "Billing Readiness Validation",
                   sys="ERP", r="GFS", a="GFS", c="Operations",
                   desc="Confirm trigger conditions are met (e.g., approved time/expenses, milestone "
                        "sign-off). Validate data completeness and accuracy for billing. "
                        "Ensure alignment with billing structure in SOW / MSA terms."),

                _s("5.1.3", "Mismatch Identified?",
                   sys="ERP", r="GFS", a="GFS",
                   type="Decision",
                   outcomes="Yes – resolve | No – proceed",
                   desc="Check for mismatches between billing data and SOW / PO terms."),

                _s("5.1.4", "Mismatch Resolution",
                   sys="ERP", r="Operations", a="Operations",
                   desc="Resolve identified billing mismatches with Operations before proceeding."),

                _s("5.1.5", "Billing Data Preparation & Consolidation",
                   sys="ERP", r="GFS", a="GFS", c="Operations",
                   desc="Compile and consolidate all billable items (time, expenses, milestones) "
                        "ready for invoice generation."),

                _s("5.1.6", "Invoice Preparation",
                   sys="ERP", r="GFS", a="GFS", c="Operations",
                   data="Invoice amount",
                   change="To-Be: invoice generated automatically upon billable item confirmation",
                   desc="Generate draft invoice with PO reference from consolidated billing data."),

                _s("5.1.7", "Internal Review",
                   sys="ERP", r="GFS", a="GFS",
                   notes="Checklist-based review; documented in ERP",
                   desc="Review invoice for accuracy and completeness. Compare against approved SOW "
                        "and MSA terms. Resolve discrepancies prior to client submission."),

                _s("5.1.8", "Handoff to Operations",
                   sys="ERP", r="GFS", a="GFS",
                   notes="Loop back to internal review if required",
                   desc="Handoff reviewed invoice to Operations for client transmission."),
            ],
        },

        # ── L2  5.2  Client Review & Approval ────────────────────────────────
        {
            "id": "client-review-approval",
            "seq": "5.2",
            "name": "Client Review & Approval",
            "description": (
                "Facilitate client review of draft invoice, resolve queries and obtain approval."
            ),
            "color": "#EA580C",
            "system_tool": "ERP / Client Portal / Email",
            "raci": {"r": "GFS / Operations", "a": "GFS", "c": "NA"},
            "key_data_points": "Client query log, Invoice approval status",
            "steps": [
                _s("5.2.1", "Transmit Invoice to Client",
                   sys="ERP / Client Portal / Email", r="Operations", a="Operations",
                   change="To-Be: auto-transmitted via portal on controller approval",
                   desc="Submit draft invoice to client if required "
                        "(e.g., skip step if scheduled billing)."),

                _s("5.2.2", "Client Query Raised?",
                   sys="ERP / Client Portal / Email", r="Operations", a="Operations",
                   type="Decision",
                   outcomes="Approved | Query raised | Dispute",
                   notes="SLA for client response: per contract terms (typically 5–10 business days)",
                   desc="Monitor for client response within agreed SLA."),

                _s("5.2.3", "Client Query Resolution",
                   sys="ERP / Client Portal / Email", r="GFS", a="GFS", c="Operations",
                   notes="Loop back to client review; credit note process in ERP if applicable",
                   desc="Address client queries or disputes. Provide supporting documentation "
                        "or revise invoice as required."),

                _s("5.2.4", "Client Approval",
                   sys="ERP / Client Portal / Email", r="Operations", a="Operations",
                   change="To-Be: portal approval auto-updates ERP status",
                   desc="Obtain client approval to proceed with invoice issuance. Trigger AR posting."),
            ],
        },

        # ── L2  5.3  Execution & Submission ──────────────────────────────────
        {
            "id": "execution-submission",
            "seq": "5.3",
            "name": "Execution & Submission",
            "description": (
                "Finalise and issue invoice, post accounts receivable and update billing records "
                "to enable tracking and collection."
            ),
            "color": "#16A34A",
            "system_tool": "ERP / Client Portal / Email / EDI",
            "raci": {"r": "GFS", "a": "GFS", "c": "NA"},
            "key_data_points": "Final invoice, AR posting, Billing reconciliation",
            "steps": [
                _s("5.3.1", "Finalise Invoice",
                   sys="ERP", r="GFS", a="GFS",
                   change="To-Be: auto-posted on client acceptance",
                   desc="Post finalised invoice to AR sub-ledger. System generates AR aging entry "
                        "and updates deferred/unbilled revenue balances. Confirm GL impact is correct."),

                _s("5.3.2", "Invoice Submission to Client",
                   sys="ERP / Client Portal / Email / EDI", r="GFS", a="GFS",
                   change="To-Be: EDI or portal auto-submission where client systems permit",
                   desc="Issue invoice to client via email, client portal, etc."),

                _s("5.3.3", "Reconciliation",
                   sys="ERP", r="GFS", a="GFS",
                   data="Invoice allocation to project codes",
                   change="To-Be: receipt confirmation auto-triggers Collections workflow",
                   desc="Perform billing reconciliations "
                        "(e.g., from parent billing level to sub-project level)."),
            ],
        },
    ],
}


# ══════════════════════════════════════════════════════════════════════════════
# L1-06  COLLECTIONS
# ══════════════════════════════════════════════════════════════════════════════
COLLECTIONS = {
    "id": "collections",
    "l1_seq": "6",
    "l1_name": "Collections",
    "l1_color": "#0F766E",
    "l1_description": (
        "All activities to collect outstanding receivables, manage overdue accounts, "
        "resolve disputes, and maintain cash flow forecasting."
    ),
    "raci": {"r": "GFS", "a": "GFS", "c": "NA"},
    "system_tool": "ERP",
    "key_data_points": "NA",
    "stages": [

        # ── L2  6.1  Reconciliation & Analysis ───────────────────────────────
        {
            "id": "reconciliation-analysis",
            "seq": "6.1",
            "name": "Reconciliation & Analysis",
            "description": (
                "Reconcile accounts receivable, apply cash receipts and resolve unallocated cash "
                "to maintain an accurate AR ledger."
            ),
            "color": "#0F766E",
            "system_tool": "ERP",
            "raci": {"r": "GFS", "a": "GFS", "c": "NA"},
            "key_data_points": "NA",
            "steps": [
                _s("6.1.1", "Run AR Aging Report",
                   sys="ERP", r="GFS", a="GFS",
                   data="Segmented AR aging balances",
                   desc="Generate AR aging report to identify overdue balances and collection priorities."),

                _s("6.1.2", "Apply Cash Receipts",
                   sys="ERP", r="GFS", a="GFS",
                   data="Applied cash, Unapplied cash",
                   desc="Match incoming cash receipts to open invoices in the AR ledger."),

                _s("6.1.3", "Unapplied / Unallocated Cash Identified?",
                   sys="ERP", r="GFS", a="GFS",
                   type="Decision",
                   outcomes="Yes – investigate | No – proceed",
                   desc="Identify any cash receipts that cannot be automatically matched to an invoice."),

                _s("6.1.4", "Investigate & Resolve Unallocated Cash",
                   sys="ERP", r="GFS", a="GFS", c="Operations",
                   desc="Investigate unallocated cash receipts and resolve with Operations or client."),

                _s("6.1.5", "AR Reconciliation",
                   sys="ERP", r="GFS", a="GFS",
                   desc="Reconcile AR sub-ledger to general ledger. Confirm balances are accurate "
                        "and complete ahead of reporting."),
            ],
        },

        # ── L2  6.2  Outreach & Escalation ───────────────────────────────────
        {
            "id": "outreach-escalation",
            "seq": "6.2",
            "name": "Outreach & Escalation",
            "description": (
                "Proactively manage overdue accounts through structured outreach, dispute resolution "
                "and escalation to secure payment commitments."
            ),
            "color": "#B45309",
            "system_tool": "ERP / Email",
            "raci": {"r": "GFS", "a": "GFS", "c": "Operations"},
            "key_data_points": "NA",
            "steps": [
                _s("6.2.1", "Overdue Identification & Prioritisation",
                   sys="ERP", r="GFS", a="GFS",
                   data="Overdues, Collections prioritisation",
                   desc="Identify overdue invoices from AR aging report. Prioritise by value, "
                        "aging bucket and client risk profile."),

                _s("6.2.2", "Collections Outreach",
                   sys="ERP / Email", r="GFS", a="GFS",
                   desc="Contact clients with overdue balances via email or phone. "
                        "Send reminders per defined dunning schedule."),

                _s("6.2.3", "Dispute Identified?",
                   sys="ERP", r="GFS", a="GFS",
                   type="Decision",
                   outcomes="Yes – dispute management | No – continue outreach",
                   desc="Determine whether client is disputing the invoice or has a query."),

                _s("6.2.4", "Dispute Management & Resolution",
                   sys="ERP / Email", r="GFS", a="GFS", c="Operations",
                   desc="Manage and resolve client invoice disputes with Operations support. "
                        "Issue credit notes or revised invoices where required."),

                _s("6.2.5", "Escalation Management",
                   sys="ERP / Email", r="Operations", a="Operations",
                   desc="Escalate unresolved overdue accounts per escalation matrix. "
                        "Engage senior stakeholders or legal as required."),

                _s("6.2.6", "Payment Commitment Tracking",
                   sys="ERP", r="GFS", a="GFS",
                   desc="Record and track payment commitments obtained from clients. "
                        "Follow up on missed payment dates."),

                _s("6.2.7", "Place Account on Credit Hold?",
                   sys="ERP", r="GFS", a="GFS", c="Operations",
                   type="Decision",
                   outcomes="Yes – implement hold | No – continue monitoring",
                   desc="Assess whether the account should be placed on credit hold "
                        "based on overdue exposure and risk."),

                _s("6.2.8", "Implement Credit Hold & Notify Teams",
                   sys="ERP", r="GFS", a="GFS", c="Operations",
                   desc="Place account on credit hold in ERP. Notify Operations, Sales and "
                        "Delivery teams to pause new orders until resolved."),
            ],
        },

        # ── L2  6.3  Cash Forecasting ─────────────────────────────────────────
        {
            "id": "cash-forecasting",
            "seq": "6.3",
            "name": "Cash Forecasting",
            "description": (
                "Maintain an accurate short-term cash flow forecast based on expected collections "
                "and perform variance analysis against prior forecasts."
            ),
            "color": "#7C3AED",
            "system_tool": "ERP",
            "raci": {"r": "GFS", "a": "GFS", "c": "NA"},
            "key_data_points": "NA",
            "steps": [
                _s("6.3.1", "Forecast Update",
                   sys="ERP", r="GFS", a="GFS",
                   data="Cash flow forecast",
                   desc="Update cash collection forecast based on expected payment dates, "
                        "payment commitments and AR aging data."),

                _s("6.3.2", "Variance Analysis vs Prior Forecast",
                   sys="ERP", r="GFS", a="GFS",
                   data="Variance analysis",
                   desc="Compare actual cash receipts and current forecast against prior period forecast. "
                        "Identify and document significant variances."),

                _s("6.3.3", "Forecast Reporting",
                   sys="ERP", r="GFS", a="GFS",
                   desc="Produce and distribute cash forecast report to Finance leadership and "
                        "Treasury as required."),
            ],
        },
    ],
}


# ── Public export ─────────────────────────────────────────────────────────────
ALL_PROCESSES = [
    ORDER_CAPTURE,
    SERVICE_DELIVERY,
    REVENUE_RECOGNITION,
    INVOICING_BILLING,
    COLLECTIONS,
]
