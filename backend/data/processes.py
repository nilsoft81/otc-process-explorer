# Auto-generated from Process_Flow_Template_v2 8.xlsx (Process Design tab)


def _s(seq, name, desc="", step_type="Process", r="", a="", i="", sys="",
        outcomes="", children=None):
    node = {
        "seq": seq, "name": name, "description": desc,
        "step_type": step_type, "system_tool": sys,
        "raci": {"r": r, "a": a, "i": i},
        "decision_outcomes": outcomes if outcomes else None,
    }
    if children is not None:
        node["children"] = children
    return node


ORDER_CAPTURE = {
    "id": "order-capture",
    "l1_seq": "1",
    "l1_name": "Order Capture",
    "l1_description": "End-to-end stage covering all activities from initial client engagement through to project activation and budget establishment.",
    "l1_color": "#7C3AED",
    "raci": {"r": "", "a": ""},
    "system_tool": "See L4",
    "stages": [
        {
            "id": "1.1",
            "seq": "1.1",
            "name": "Customer & Contract Setup (incl. portal setup)",
            "description": "Establish the client record, negotiate and execute the master services agreement, set up the client portal, and configure entitlements.",
            "step_type": "Process",
            "system_tool": "See L4",
            "raci": {"r": "Sales", "a": "Sales", "i": ""},
            "steps": [
                _s(seq="1.1.1", name="Customer Initiation", desc="Receive new client / opportunity trigger from Sales/Business Development. Capture preliminary customer details (name, region, industry)", r="Sales", a="Sales", children=[
                    _s(seq="1.1.1.1", name="Log Prospect in HubSpot & Create HubSpot Customer Record", desc="Create a new Contact and Company record in HubSpot. Capture preliminary details (client name, region, service line, deal scope). Duplicate detection rule runs automatically on save. If a matching Customer record exists in HubSpot, the user is prompted to merge or link the entry", r="Sales", a="Sales", sys="CRM"),
                    _s(seq="1.1.1.2", name="Opportunity Created in HubSpot", desc="Convert the prospect to a HubSpot Deal. Populate deal name, estimated value, engagement type (T&M / Fixed Fee / Retainer), expected close date and pipeline stage. Assign deal owner and deal split. Complete initial qualification checklist (budget, authority, need, timeline) to confirm pursuit", r="Sales", a="Sales", sys="CRM"),
                    _s(seq="1.1.1.3", name="CPQ Quote Generation", desc="Generate client pricing quote in CPQ / PSA based on expected scope, resource requirements, rate card and commercial model. Interface from CPQ module in PSA back to CRM (Hubspot)", r="Client Services / Account Managers", a="Sales", i="Division Finance", sys="PSA / CRM"),
                    _s(seq="1.1.1.4", name="Advance Prospect Through Deal Stages", desc="When the prospect is being actively pursued, the user should advance the Deal Stage through the various stages (RFP/Proposal Submitted > Pitch > Negotiation > Verbal Award > Contracting", r="Sales", a="Sales", sys="CRM"),
                    _s(seq="1.1.1.5", name="Customer Already Exists in ERP?", desc="Determine whether the customer already exists in ERP. The 'Verbal Award' stage automatically triggers a check if Customer already exists in ERP master data (e.g., if Oracle/Maconomy Customer ID is blank), and initiates MDM setup workflow where required Check which module in ERP they are checking for master data (Dawn/Enda)", step_type="Decision", r="Automated", a="Sales", sys="CRM / ERP", outcomes="Yes - proceed to 1.1.5 | No - proceed to 1.1.1.6"),
                    _s(seq="1.1.1.6", name="Submit Request to Global Master Data Team", desc="HubSpot Workflow automatically opens a ServiceNow ticket to the Global Master Data team without any action from the end user. The ticket is pre-populated with all client fields already captured in HubSpot", step_type="Automated", r="Automated", a="Sales", sys="CRM / ServiceNow")
                    ]),
                _s(seq="1.1.2", name="Customer Master Data Creation & Hierarchy Setup", desc="Create customer record in CRM/ERP (e.g., legal entity name, billing address, VAT number, etc.). Perform duplicate check. Assign customer ID and account owner. Define parent/child relationships if applicable (e.g., billing entity). Link back to prospect opportunity in HubSpot", r="Global Master Data", a="Global Master Data", children=[
                    _s(seq="1.1.2.1", name="MDM Ticket Review & Identification of Data Gaps", desc="ServiceNow ticket is routed with client fields pre-populated from HubSpot, to be reviewed for accuracy/completeness. Identify which ERP-specific fields can be completed independently (e.g., internal segmentation codes) and which require commercial input from Client Services", r="Global Master Data", a="Global Master Data", sys="ServiceNow / ERP"),
                    _s(seq="1.1.2.2", name="Is Client Services Input Required to Complete Missing Fields?", desc="Determine whether Client Services is required to fill out missing Customer data fields", step_type="Decision", r="Global Master Data", a="Global Master Data", sys="ERP", outcomes="Yes - proceed to 1.1.2.3 | No - proceed to 1.1.3"),
                    _s(seq="1.1.2.3", name="Request for Supplementary Information", desc="MDM initiates request for supplementary information via a structured follow-up task in the ServiceNow ticket, and is routed to Client Services for action", r="Global Master Data", a="Global Master Data", sys="ServiceNow"),
                    _s(seq="1.1.2.4", name="Obtain & Populate Missing Information for Customer Record", desc="Client Services reaches out to Customer for missing information, completes the task directly within ServiceNow (or via a linked HubSpot task if the ServiceNow-HubSpot integration is active) and submits", r="Sales", a="Sales", sys="Email / ServiceNow"),
                    _s(seq="1.1.2.5", name="MDM Ticket Review & Record Creation", desc="MDM team is notified automatically on submission and proceeds to Oracle/Maconomy record creation", step_type="Automated", r="Automated", a="Global Master Data", sys="ERP"),
                    _s(seq="1.1.2.6", name="Ticket Closure & Customer ID Write-back", desc="ServiceNow ticket is automatically closed upon record creation. Ticket closure triggers an automated write-back of the Oracle/Maconomy Customer ID to the HubSpot Company record via the ServiceNow-HubSpot integration", step_type="Automated", r="Automated", a="Global Master Data", sys="ServiceNow / ERP / CRM"),
                    _s(seq="1.1.2.7", name="Notification of Client Record Update in HubSpot", desc="Client Services receives HubSpot notification that the customer record is live and the Oracle/Maconomy Customer ID is populated", step_type="Automated", r="Automated", a="Sales", sys="CRM")
                    ]),
                _s(seq="1.1.3", name="Credit & Compliance Screening", desc="Perform credit check (incl. credit holds) / financial due diligence. Conduct compliance checks. Assign provisional payment terms and risk rating", r="GFS - Credit", a="GFS - Credit", i="Sales", sys="Credit Platform / ERP", children=[
                    _s(seq="1.1.3.1", name="Compliance Screening", desc="Perform regulatory and policy checks including sanctions, AML, watchlist, etc. to ensure the relationship is permissible before extending credit.", r="GFS - Credit", a="GFS - Credit", sys="Assumes third party provider is used"),
                    _s(seq="1.1.3.2", name="Credit Assessment", desc="Review the prospective customer’s financial standing using payment history, trade references, credit bureau data, financial statements and existing exposure to evaluate overall creditworthiness", r="GFS - Credit", a="GFS - Credit", sys="Assumes third party provider is used"),
                    _s(seq="1.1.3.3", name="Risk Scoring", desc="Apply defined scoring models or risk rules to convert assessment inputs into a standardised credit risk score", r="GFS - Credit", a="GFS - Credit", sys="Credit platform or equivalent workflow tool"),
                    _s(seq="1.1.3.4", name="Credit Decisioning", desc="Determine credit outcome based on scoring thresholds and policy rules (e.g., approve, escalate for manual review, reject)", r="GFS - Credit", a="GFS - Credit", sys="Credit platform or equivalent workflow tool"),
                    _s(seq="1.1.3.5", name="ERP Credit Master Update", desc="Automatically interface approved credit decisions from credit platform/workflow tool to ERP (Oracle/Maconomy) to update customer credit master data, payment terms and hold status", step_type="Automated", r="Automated", a="GFS - Credit", sys="ERP"),
                    _s(seq="1.1.3.6", name="Notify Stakeholders", desc="Automatically notify relevant teams", step_type="Automated", r="Automated", a="GFS - Credit", sys="Credit platform or equivalent workflow tool")
                    ]),
                _s(seq="1.1.4", name="Multi-Division Engagement Setup", desc="Determine whether customer engagement requires a multi-division operating model (including CIC-contracted customers), and define parent division ownership and billing structure prior to contract execution", sys="N/A", children=[
                    _s(seq="1.1.4.1", name="Multi-Division Engagement Structure Required (eg., CIC)?", desc="Determine whether multiple divisions are engaging the customer under a shared client relationship, MSA framework and billing structure", step_type="Decision", r="Client Services / Account Managers", a="Commercial Affairs", sys="N/A", outcomes="Yes - proceed to 1.1.4.2 | No - proceed to 1.1.5"),
                    _s(seq="1.1.4.2", name="Parent Division Assignment", desc="Assign parent division based on agreed ownership criteria. Point of Origination drives parent assignment for new customers. For existing customers, determine parent ownership based on agreed commercial and delivery factors (e.g., revenue share, delivery footprint, key account ownership)", r="Client Services / Account Managers", a="Commercial Affairs", sys="N/A"),
                    _s(seq="1.1.4.3", name="Participating Division Identification", desc="Identify divisions participating in delivery and billing for the engagement", r="Client Services / Account Managers", a="Commercial Affairs", sys="N/A"),
                    _s(seq="1.1.4.4", name="Common Pricing & Commercial Structure Alignment", desc="Define common pricing structures, rate cards and shared commercial terms across participating divisions. Where agreement cannot be reached, parent division retains final commercial decision authority", r="Client Services / Account Managers", a="Commercial Affairs", sys="N/A"),
                    _s(seq="1.1.4.5", name="Division Scope & Billing Allocation", desc="Define division-level scope ownership, billing responsibility and consolidated billing structure aligned to parent division requirements", r="Client Services / Account Managers", a="Commercial Affairs", sys="N/A"),
                    _s(seq="1.1.4.6", name="Parent Division Change Control", desc="As required, manage controlled reassignment of parent division ownership based on material changes in revenue share, delivery footprint or strategic account ownership", r="Client Services / Account Managers", a="Commercial Affairs", sys="N/A")
                    ]),
                _s(seq="1.1.5", name="Master Services Agreement (MSA) management", desc="Check for existing MSA and validate applicability. Draft MSA (if required) using standard templates.  Negotiate legal and high-level commercial terms. Execute agreement (signatures). Store in contract repository and link to customer record", r="Commercial Affairs", a="Commercial Affairs", i="Various", children=[
                    _s(seq="1.1.5.1", name="Existing MSA Check", desc="Determine whether a valid MSA already exists for the customer or parent/affiliate group", step_type="Decision", r="Commercial Affairs", a="Commercial Affairs", sys="CLM", outcomes="Yes - proceed to 1.1.5.14 | No - proceed to 1.1.5.2"),
                    _s(seq="1.1.5.2", name="Select MSA Template", desc="Choose the appropriate MSA template from CLM based on division, commercial model, client region, etc.", r="Commercial Affairs", a="Commercial Affairs", sys="CLM"),
                    _s(seq="1.1.5.3", name="Populate MSA Master Data & Reference", desc="Populate client, legal and billing master data in MSA template. Generate MSA reference ID in CLM for contract processing and downstream invoicing", r="Commercial Affairs", a="Commercial Affairs", sys="CLM"),
                    _s(seq="1.1.5.4", name="Populate High-level Commercial Terms", desc="Enter high-level contractual and billing framework terms including payment terms, currency, billing frequency, delivery format (e.g., e-invoicing) , rate cards (if applicable) and agreed discount structure into the contract template. Where applicable, permit use of scheduled billing arrangements to support downstream billing operations and invoice automation", r="Commercial Affairs", a="Commercial Affairs", i="Sales", sys="CLM"),
                    _s(seq="1.1.5.5", name="Country-Specific e-Invoicing Rule Validation", desc="Validate whether local e-invoicing regulations apply based on jurisdiction, billing entity and client requirements. If required, obtain and capture e-invoice ID for billing entity for e-invoice processing", r="Commercial Affairs", a="Commercial Affairs", i="Client Services / Account Managers", sys="CLM"),
                    _s(seq="1.1.5.6", name="Legal Review", desc="Use CLM workflow to route draft MSA to Legal for review, including review for non-standard terms (if applicable)", r="Legal", a="Legal", i="Commercial Affairs", sys="CLM"),
                    _s(seq="1.1.5.7", name="Legal Approval?", desc="Determine whether Legal approves the written draft to be sent for customer signature", step_type="Decision", r="Legal", a="Legal", sys="CLM", outcomes="Yes - proceed to 1.1.5.8 | No - proceed to 1.1.5.10"),
                    _s(seq="1.1.5.8", name="Send Contract to Client", desc="Transmit final contract to client signatories via e-signature link within HubSpot (via DocuSign integration). Where possible be the first signing (enables technology pick e.g. Docusign)", step_type="Automated", r="Automated", a="Commercial Affairs", sys="CLM (DocuSign)"),
                    _s(seq="1.1.5.9", name="Client Reviews & Signs Contract", desc="Client reviews the contract, raises redlines if applicable and executes e-signature within HubSpot (via DocuSign integration)", r="Client (external)", a="Sales", sys="CLM (DocuSign)"),
                    _s(seq="1.1.5.10", name="Contract Fully Executed?", desc="Confirm that all counterparty signatures are captured and the contract is legally binding before proceeding. Change document status to \"Executed\"", step_type="Decision", r="Commercial Affairs", a="Commercial Affairs", sys="CLM", outcomes="Yes - proceed to 1.1.5.11 | No - proceed to 1.1.5.8"),
                    _s(seq="1.1.5.11", name="Notification to GFS", desc="\"Executed\" status triggers automated notification to prompt GFS for client portal setup and e-invoicing configuration, if applicable", step_type="Automated", r="Automated", a="Commercial Affairs", sys="CLM"),
                    _s(seq="1.1.5.12", name="Set Up Client Portal & E-Invoicing Billing Configuration", desc="Provision the client's portal access, configure project visibility, set user roles and permissions and confirm with the client that access is working. Update ERP billing master data with e-invoicing identifiers and configure invoice delivery method for structured e-invoicing submission", r="GFS", a="Client Services", sys="CLM / Client Portal / ERP"),
                    _s(seq="1.1.5.13", name="Notify Stakeholders", desc="\"Executed\" status triggers workflow for automated internal handoff notifications to relevant stakeholders", step_type="Automated", r="Automated", a="Commercial Affairs", sys="CLM"),
                    _s(seq="1.1.5.14", name="MSA Upload to Agent", desc="Upload signed MSA document to CLM (HighQ), and then to Contract Capture Tool automatically via CLM (HighQ) integration, or direct upload if required", r="AI Agent - Contract Capture (or Commercial Affairs in absence of Agent)", a="Commercial Affairs", sys="Contract Capture Tool"),
                    _s(seq="1.1.5.15", name="MSA: Data Extraction", desc="Extract MSA reference ID and structure key customer, commercial and contractual data from the MSA to support project setup. Link to parent MSA, if applicable. Automatically capture data extractions and feed into PSA and/or ERP", r="AI Agent - Contract Capture (or Client Services/Acct Mgrs in absence of Agent)", a="Commercial Affairs", sys="Contract Capture Tool / PSA or ERP")
                    ]),
            ],
        },
        {
            "id": "1.2",
            "seq": "1.2",
            "name": "SOW, Order Entry & Validation (incl. POs)",
            "description": "Execute Statement of Work (SOW) incl. scope, deliverables, and pricing. Set up the contract/order in the ERP system and prepare for project setup",
            "step_type": "Process",
            "system_tool": "See L4",
            "raci": {"r": "Client Services / Account Managers", "a": "Client Services / Account Managers", "i": "Commercial Affairs"},
            "steps": [
                _s(seq="1.2.1", name="SOW initiation / amendment", desc="Receive new project opportunity (following 1.1.5.11 for new customers; point of origination for existing customers)", r="Client Services / Account Managers", a="Client Services / Account Managers", children=[
                    _s(seq="1.2.1.1", name="Project Amendment?", desc="Determine whether scope is related to an existing project and requires amendment to the SOW", step_type="Decision", r="Client Services / Account Managers", a="Client Services / Account Managers", i="Commercial Affairs", sys="CLM", outcomes="Yes - proceed to 1.2.2.3 | No - proceed to 1.2.2")
                    ]),
                _s(seq="1.2.2", name="Draft SOW", desc="Develop scope, deliverables and timelines. Define pricing and commercial terms. Align resourcing and effort with delivery. Generate SOW document", r="Client Services / Account Managers", a="Client Services / Account Managers", i="Commercial Affairs", children=[
                    _s(seq="1.2.2.1", name="Participating Division Identification", desc="Identify division(s) participating in delivery and billing for the proposed scope of work aligned to the previously agreed parent-child structure, if applicable", r="Client Services / Account Managers", a="Client Services / Account Managers", i="Commercial Affairs"),
                    _s(seq="1.2.2.2", name="Select SOW Template (CLM)", desc="Select appropriate SOW template based on division, commercial model, project type and client requirements. Ensure selected template allows for use of structured inputs for key SOW components (e.g., deliverables, billing schedule, etc.), regardless of client-specific format, to support automation and downstream processing. Include MSA reference and generate SOW reference ID (which may double as Project Number)", r="Client Services / Account Managers", a="Client Services / Account Managers", i="Commercial Affairs", sys="CLM"),
                    _s(seq="1.2.2.3", name="Define Scope & Delivery Approach", desc="Establish deliverables, timeline, milestones, dependencies, etc. Distinguish between agreed vs. optional scope", r="Client Services / Account Managers", a="Client Services / Account Managers", i="Commercial Affairs", sys="CLM"),
                    _s(seq="1.2.2.4", name="Define Pricing & Commercial Terms", desc="Define engagement-specific commercial model, rates/fees, billing triggers (e.g., scheduled billing) and upfront payment requirements (if applicable) for the proposed scope of work.For multi-division engagements, establish consolidated billing and align commercial terms to the designated Parent division. Where permitted under agreed MSA terms, use scheduled billing arrangements for T&M and Fixed Fee engagements to simplify downstream billing and invoice generation. Define billable vs. non-billable guidelines", r="Client Services / Account Managers", a="Client Services / Account Managers", i="Commercial Affairs", sys="CLM"),
                    _s(seq="1.2.2.5", name="Define Pass-Through Treatment", desc="Define pass-through cost treatment for the engagement including billing method (at cost, percentage markup, fixed fee with or without markup), billing frequency, invoice requirements (e.g., line item detail) and revenue recognition approach", r="Client Services / Account Managers", a="Client Services / Account Managers", i="Commercial Affairs", sys="CLM"),
                    _s(seq="1.2.2.6", name="Define Resourcing & Effort", desc="Define resourcing and effort requirements to support delivery", r="Client Services / Account Managers", a="Client Services / Account Managers", i="Staffing", sys="CLM"),
                    _s(seq="1.2.2.7", name="Draft SOW Document", desc="Generate and populate SOW document using standardised templates", r="Client Services / Account Managers", a="Client Services / Account Managers", i="Commercial Affairs", sys="CLM"),
                    _s(seq="1.2.2.8", name="Scope Change?", desc="Determine whether there is a scope change after initial SOW draft", step_type="Decision", r="Client Services / Account Managers", a="Client Services / Account Managers", i="Commercial Affairs", sys="CLM", outcomes="Yes - proceed to 1.2.2.9 | No - proceed to 1.2.2.10"),
                    _s(seq="1.2.2.9", name="Redraft SOW Document or Document Changes via Structured Letter", desc="Redraft and update the SOW to reflect approved scope changes (e.g., scope, pricing, timelines, deliverables). Alternatively, capture authorised scope changes in letter or email from client in structured template format with Project Number and MSA reference included. If Project Number doesn't yet exist, include a SOW reference in lieu", r="Client Services / Account Managers", a="Client Services / Account Managers", i="Commercial Affairs", sys="CLM"),
                    _s(seq="1.2.2.10", name="Draft SOW Upload to Agent", desc="Upload draft SOW document to Contract Capture Tool via email or upload to Agent. Alternatively, capture authorised scope changes in letter or email from client and upload to Agent via emai lor direct upload. Ensure Project Number and SOW/MSA reference are included to append to original documents", r="AI Agent - Contract Capture (or Client Services/Acct Mgrs in absence of Agent)", a="Client Services / Account Managers", i="Commercial Affairs", sys="Contract Capture Tool"),
                    _s(seq="1.2.2.11", name="Draft SOW: Data Extraction", desc="Extract and structure key scope, pricing and billing data from the SOW to support project setup, revenue recognition and invoicing process. Link to parent SOW, if applicable. Automatically capture data extractions and feed into PSA and/or ERP", r="AI Agent - Contract Capture (or Client Services/Acct Mgrs in absence of Agent)", a="Client Services / Account Managers", i="Commercial Affairs", sys="Contract Capture Tool"),
                    _s(seq="1.2.2.12", name="Draft SOW Alignment to MSA?", desc="Determine if signed SOW aligns with agreed MSA (scope alignment to services framework, pricing structure, payment terms, etc.) Automatically flag any changes from previous iterations. Link to clilent MSA using MSA reference ID", r="AI Agent - Contract Capture (or Client Services/Acct Mgrs in absence of Agent)", a="Client Services / Account Managers", i="Commercial Affairs", sys="Contract Capture Tool")
                    ]),
                _s(seq="1.2.3", name="At-Risk Project Activation on Draft SOW", desc="Exception pathway where team requests approval to activate a project and commence work at-risk prior to SOW signature, using a draft SOW and documented client authorisation. Capture draft SOW in the Contract Capture Agent, append client letters/emails as supporting amendments, activate the project in PSA with an “Proposal” status, and prevent revenue recognition until the SOW is fully executed", r="AI Agent - Contract Capture (or Client Services/Acct Mgrs in absence of Agent)", a="Client Services / Account Managers", i="Commercial Affairs", sys="Contract Capture Tool", children=[
                    _s(seq="1.2.3.1", name="At-Risk Start Needed?", desc="Determine whether there is a need/request to commence work at-risk before the SOW is fully executed", step_type="Decision", r="AI Agent - Contract Capture (or Client Services/Acct Mgrs in absence of Agent)", a="Client Services / Account Managers", sys="Contract Capture Tool", outcomes="Yes - proceed to 1.2.3.2 | No - proceed to 1.2.4"),
                    _s(seq="1.2.3.2", name="At-Risk Approval & Risk Acceptance", desc="Route the at-risk start request for internal approval. Define working-at-risk time bounds and escalation requirements for unresolved client approvals or contract execution delays. Approval confirms acceptance of commercial, delivery, billing, collection and contractual risk before work begins or project activation proceeds.", r="Division Finance", a="Division Finance", i="Client Services / Account Managers"),
                    _s(seq="1.2.3.3", name="Proceed to Project Setup", desc="Proceed to project setup at 1.3.1. Time bound", r="AI Agent - Contract Capture (or Client Services/Acct Mgrs in absence of Agent)", a="Client Services / Account Managers", sys="N/A"),
                    _s(seq="1.2.3.4", name="At-Risk Monitoring", desc="Monitor all projects in 'Proposal' status with costs incurred against them. If approved at-risk working period exceeds defined threshold (e.g., 2 weeks without executed SOW) on any given-project, trigger escalation and additional commercial, legal and delivery review to reassess continuation of work and pens-down requirements (if applicable)", r="Client Services / Account Managers", a="Division Finance", sys="PowerBI Dashboard")
                    ]),
                _s(seq="1.2.4", name="Send SOW to Client", desc="Transmit final SOW to client signatories via e-signature link within HubSpot (via DocuSign integration). Where possible be the first signing (enables technology pick e.g. Docusign)", r="Client Services / Account Managers", a="Client Services / Account Managers", i="Commercial Affairs", sys="CLM (DocuSign)"),
                _s(seq="1.2.5", name="Client Reviews & Signs Contract", desc="Review and redline with customer. Finalise SOW details and obtain e-signature", r="Client Services / Account Managers", a="Client Services / Account Managers", i="Commercial Affairs", sys="CLM (DocuSign)", children=[
                    _s(seq="1.2.5.1", name="Send Contract to Client", desc="Transmit final SOW to client signatories via e-signature link within HubSpot (via DocuSign integration)", r="Client Services / Account Managers", a="Client Services / Account Managers", i="Commercial Affairs", sys="CLM (DocuSign)"),
                    _s(seq="1.2.5.2", name="Client Amendments", desc="Determine whether the customer has proposed amendments to the SOW", r="Client Services / Account Managers", a="Client Services / Account Managers", i="Commercial Affairs", sys="CLM"),
                    _s(seq="1.2.5.3", name="Client Reviews & Signs SOW", desc="Client reviews the SOW, raises redlines if applicable and executes e-signature within HubSpot (via DocuSign integration)", r="Client Services / Account Managers", a="Client Services / Account Managers", i="Commercial Affairs", sys="CLM (DocuSign)"),
                    _s(seq="1.2.5.4", name="Contract Fully Executed?", desc="Confirm that all counterparty signatures are captured and the contract is legally binding before proceeding. Change document status to \"Completed\"", r="AI Agent - Contract Capture (or Client Services/Acct Mgrs in absence of Agent)", a="Division Finance", i="Commercial Affairs", sys="CLM"),
                    _s(seq="1.2.5.5", name="SOW Upload to Agent", desc="Automatically upload signed SOW document to Contract Capture Tool via email or upload to Agent", r="AI Agent - Contract Capture (or Client Services/Acct Mgrs in absence of Agent)", a="Client Services / Account Managers", i="Commercial Affairs", sys="Contract Capture Tool"),
                    _s(seq="1.2.5.6", name="SOW: Data Extraction", desc="Extract and structure key scope, pricing and billing data from the SOW to support project setup, revenue recognition and invoicing process. Flag whether document is New or Amended. Link to parent SOW, if applicable. Automatically capture data extractions and feed into PSA or ERP", r="AI Agent - Contract Capture (or Client Services/Acct Mgrs in absence of Agent)", a="Client Services / Account Managers", i="Commercial Affairs", sys="Contract Capture Tool / PSA or ERP"),
                    _s(seq="1.2.5.7", name="SOW Alignment to MSA?", desc="Re-determine if signed SOW aligns with agreed MSA (scope alignment to services framework, pricing structure, payment terms, etc.). Automatically flag any changes from previous iterations. Link to clilent MSA using MSA reference ID", step_type="Decision", r="AI Agent - Contract Capture (or Client Services/Acct Mgrs in absence of Agent)", a="Client Services / Account Managers", i="Commercial Affairs", sys="Contract Capture Tool", outcomes="Yes - proceed to 1.2.5.9 | No - proceed to 1.2.2.9"),
                    _s(seq="1.2.5.8", name="SOW Alignment Discrepancy Resolution", desc="Identify and resolve discrepancies (e.g., inconsistencies with billing terms). Update SOW document where required", r="Client Services / Account Managers", a="Client Services / Account Managers", i="Commercial Affairs", sys="Contract Capture Tool / CLM"),
                    _s(seq="1.2.5.9", name="SOW Value Capture & System Recording", desc="Capture agreed SOW value and commercial terms in ERP during contract/order setup. Ensure SOW value is recorded as the basis for billing and revenue recognition [Miguel - is there a status it needs to flip to in order to record value in ERP? Or is this a manual switch by the user?]", r="AI Agent - Contract Capture (or Client Services/Acct Mgrs in absence of Agent)", a="Client Services / Account Managers", i="Commercial Affairs", sys="ERP"),
                    _s(seq="1.2.5.10", name="Document storage in PSA", desc="Automatically push link to all documents to PSA for audit / record-keeping purposes", r="AI Agent - Contract Capture (or Client Services/Acct Mgrs in absence of Agent)", a="Client Services / Account Managers", sys="PSA"),
                    _s(seq="1.2.5.11", name="Signed SOW Upload to HighQ", desc="Automatically push draft SOW document to HighQ for document upload and storage. Ensure Project Number and SOW / MSA references are included to maintain linkage to original documents", r="AI Agent - Contract Capture (or Commercial Affairs in absence of Agent)", a="Client Services / Account Managers", sys="CLM"),
                    _s(seq="1.2.5.12", name="Project Activation Trigger", desc="Automatically trigger workflow for new project activation in PSA (or project updates if this is an amendment to an existing project scope). See step 1.3 for project activation steps", r="Client Services / Account Managers", a="Division Finance", sys="PSA"),
                    _s(seq="1.2.5.13", name="Upfront Billing Required?", desc="Determine whether upfront payment or pre-billing is required based on executed SOW terms", step_type="Decision", r="AI Agent - Contract Capture (or Commercial Affairs in absence of Agent)", a="Client Services / Account Managers", sys="Contract Capture Tool / PSA", outcomes="Yes - proceed to 1.3.6 | No - proceed to 1.2.6")
                    ]),
                _s(seq="1.2.6", name="PO Intake, Validation & Routing", desc="Receive purchase order (PO) from client. Validate PO details against SOW (value, scope, entity, dates). Route PO internally for review. Record and link PO to customer / contract", r="AI Agent - Contract Capture (or Client Services/Acct Mgrs in absence of Agent)", a="Client Services / Account Managers", children=[
                    _s(seq="1.2.6.1", name="PO Received?", desc="Determine whether PO has been received", step_type="Decision", r="AI Agent - Contract Capture (or Client Services/Acct Mgrs in absence of Agent)", a="Client Services / Account Managers", sys="Email / Portal / EDI", outcomes="Yes - proceed to 1.2.6.2 | No - proceed to 1.2.7"),
                    _s(seq="1.2.6.2", name="PO Intake", desc="Automatically receives purchase order (PO) from client via agreed channel(s) (e.g., email, portal, EDI)", r="AI Agent - Contract Capture (or Client Services/Acct Mgrs in absence of Agent)", a="Client Services / Account Managers", sys="Email / Portal / EDI"),
                    _s(seq="1.2.6.3", name="PO Upload to Agent", desc="PO automatically uploaded to Contract Capture tool when submitted automatically via email or direct upload to Agent", r="AI Agent - Contract Capture (or Client Services/Acct Mgrs in absence of Agent)", a="Client Services / Account Managers", sys="Contract Capture Agent"),
                    _s(seq="1.2.6.4", name="PO: Data Extraction", desc="Extract and structure key purchase order data (e.g., PO number, value, billing entity, dates) to support contract setup and invoicing. Flag whether document is New or Amended. Link to related POs, if applicable. Link to SOWs via SOW reference / Project Number", r="AI Agent - Contract Capture (or Client Services/Acct Mgrs in absence of Agent)", a="Client Services / Account Managers", sys="Contract Capture Agent"),
                    _s(seq="1.2.6.5", name="PO Completeness & Validity Check", desc="Verify PO includes required details (e.g., PO number, value, dates, client entity, billing entity). Confirm PO is valid and approved on client side", r="AI Agent - Contract Capture (or GFS in absence of Agent)", a="GFS", i="Client Services / Account Managers", sys="Contract Capture Agent"),
                    _s(seq="1.2.6.6", name="PO Alignment to SOW?", desc="Determine if PO aligns with agreed SOW (billing entity, scope, value, billing structure, and deliverables) and MSA terms where applicable", step_type="Decision", r="AI Agent - Contract Capture (or GFS in absence of Agent)", a="GFS", i="Client Services / Account Managers", sys="Contract Capture Agent", outcomes="Yes - proceed to 1.2.7 | No - proceed to 1.2.6.7"),
                    _s(seq="1.2.6.7", name="PO Alignment Discrepancy Resolution", desc="Identify and resolve discrepancies (e.g., incorrect billing entity). Request PO corrections where required and reupload to Contract Capture tool", r="AI Agent - Contract Capture (or GFS in absence of Agent)", a="Client Services / Account Managers", sys="Contract Capture Agent")
                    ]),
                _s(seq="1.2.7", name="Contract setup / order entry", desc="Create contract/order record in ERP. Input pricing, billing structure and key terms. Link to customer. Associate PO to contract/order. Configure billing schedule and triggers. Set revenue recognition method.", r="AI Agent - Contract Capture (or GFS in absence of Agent)", a="GFS", children=[
                    _s(seq="1.2.7.1", name="Contract / Order Record Creation", desc="Create contract/order record in ERP linked to customer and opportunity", r="AI Agent - Contract Capture (or GFS in absence of Agent)", a="GFS", sys="ERP"),
                    _s(seq="1.2.7.2", name="Commercial Data Entry", desc="Input pricing, billing structure and key commercial terms based on SOW and MSA", r="AI Agent - Contract Capture (or GFS in absence of Agent)", a="GFS", sys="ERP"),
                    _s(seq="1.2.7.3", name="PO Association", desc="Link validated client PO to contract/order for billing reference, if applicable", r="AI Agent - Contract Capture (or GFS in absence of Agent)", a="GFS", sys="ERP"),
                    _s(seq="1.2.7.4", name="Billing Configuration", desc="Configure billing schedule, triggers and invoicing format/parameters", r="AI Agent - Contract Capture (or GFS in absence of Agent)", a="GFS", sys="ERP"),
                    _s(seq="1.2.7.5", name="Revenue Recognition Setup", desc="Define revenue recognition method and rules aligned to contract terms", r="AI Agent - Contract Capture (or GFS in absence of Agent)", a="GFS", sys="ERP"),
                    _s(seq="1.2.7.6", name="Data Validation & Reconciliation", desc="Validate accuracy and completeness of contract data in ERP. Confirm alignment with SOW, MSA, and PO", r="AI Agent - Contract Capture (or GFS in absence of Agent)", a="GFS", sys="ERP"),
                    _s(seq="1.2.7.7", name="Update Deal Stage", desc="Update deal stage in CRM to \"Contracted\"", r="AI Agent - Contract Capture (or GFS in absence of Agent)", a="GFS", sys="CRM")
                    ]),
            ],
        },
        {
            "id": "1.3",
            "seq": "1.3",
            "name": "Project Activation & Budgeting",
            "description": "Create and structure the project in the PSA aligned to the executed SOW (and PO, if applicable). Establish budgets, assign resources and configure time, expense and billing readiness. Activate the project to enable delivery, tracking and invoicing",
            "step_type": "Process",
            "system_tool": "PSA / Concur",
            "raci": {"r": "Client Services / Account Managers", "a": "Client Services / Account Managers", "i": ""},
            "steps": [
                _s(seq="1.3.1", name="Project initiation", desc="Signed SOW pre-loaded into PSA via Contract Capture tool. Assign project manager. For at-risk assignments, link back to Draft SOW and set project status to \"Proposal\" (Evoke). [What is Ignite's equivalent status? Can only be answered by Ari]", r="Client Services / Account Managers", a="Client Services / Account Managers", sys="PSA"),
                _s(seq="1.3.2", name="Project structure setup", desc="Create project record linked to SOW, PO and customer data. Define work package (phases, activities, timeline, milestones) aligned to SOW", r="Client Services / Account Managers", a="Client Services / Account Managers", sys="PSA"),
                _s(seq="1.3.3", name="Budget setup", desc="Load revenue baseline from SOW and PO. Define cost budget based on resourcing plan. Establish margin baseline", r="Client Services / Account Managers", a="Client Services / Account Managers", i="Division Finance", sys="PSA"),
                _s(seq="1.3.4", name="Initial resourcing alignment", desc="Validate roles and capacity assumptions against SOW. Initiate coordination with resource management for staffing requirements", r="Client Services / Account Managers", a="Client Services / Account Managers", sys="PSA"),
                _s(seq="1.3.5", name="Time & expense enablement", desc="Enable time entry against project. Configure expense policies and categories. Validate billable vs non-billable guidelines. Load and synchronise project codes to expense systems (e.g., Concur)", r="Client Services / Account Managers", a="Client Services / Account Managers", sys="PSA / Concur"),
                _s(seq="1.3.6", name="Milestone & Billing Trigger Setup", desc="Establish project milestones, billing schedules and associated billing trigger conditions aligned to delivery and invoicing requirements. If pre-billing is required, establish milestone marked as complete on SOW signature date to trigger upfront billing for agreed amount", r="Client Services / Account Managers", a="Client Services / Account Managers", sys="PSA"),
                _s(seq="1.3.7", name="Billing & Revenue Enablement", desc="Ensure billing triggers, billing schedules and revenue recognition controls are aligned between milestone setup and SOW terms. Activate controls to block Revenue Recognition until Signed SOW is received (automatically deactivated when Project Status changes to \"Active\"). If pre-billing is required, mark 'SOW Executed' milestone as Complete to trigger invoicing process", r="Client Services / Account Managers", a="Client Services / Account Managers", sys="PSA"),
                _s(seq="1.3.8", name="Project governance & controls setup", desc="Define reporting cadence (status, financials). Establish change control process. Define approval matrix (timesheets, expenses, etc.)", r="Client Services / Account Managers", a="Client Services / Account Managers", sys="PSA", children=[
                    _s(seq="1.3.8.1", name="Project Value Threshold Met?", desc="Determine whether project value exceeds defined financial approval threshold (>$500k) [confirm against Audit rules]", step_type="Decision", r="Client Services / Account Managers", a="Division Finance", sys="PSA", outcomes="Yes - proceed to 1.3.8.3 | No - proceed to 1.3.8.2"),
                    _s(seq="1.3.8.2", name="Operations Project Activation", desc="Review and activate project in PSA in line with financial approval controls", r="Client Services / Account Managers", a="Division Finance", sys="PSA"),
                    _s(seq="1.3.8.3", name="Finance Project Activation", desc="Review and activate project in PSA in line with financial approval controls", r="Division Finance", a="Division Finance", sys="PSA")
                    ]),
                _s(seq="1.3.9", name="Project activation (go-live)", desc="Validate all setup components are complete. Confirm no credit holds. Set project status to 'Active' to activate project for time, cost and billing. Revenue Recognition automatically enabled. Project number generated. Notify stakeholders (Delivery, Finance, Sales)", r="Client Services / Account Managers", a="Division Finance", sys="PSA"),
            ],
        },
    ],
}

DEMAND_AND_SUPPLY_PLANNING = {
    "id": "demand-supply-planning",
    "l1_seq": "2",
    "l1_name": "Demand & Supply Planning",
    "l1_description": "End-to-end stage to forecast revenue demand, plan workforce capacity and assign resources to engagements to ensure optimal utilisation and delivery readiness",
    "l1_color": "#0E7490",
    "raci": {"r": "", "a": ""},
    "system_tool": "",
    "stages": [
        {
            "id": "2.1",
            "seq": "2.1",
            "name": "Revenue Forecasting",
            "description": "Develop and maintain revenue forecasts based on pipeline, active contracts, historical patterns and delivery progress to produce a forward-looking demand forecast",
            "step_type": "Process",
            "system_tool": "CRM / PSA / ERP",
            "raci": {"r": "", "a": "", "i": ""},
            "steps": [
                _s(seq="2.1.1", name="Forecast Submission Calendar", desc="Define forecast timetable, submission deadlines and governance requirements for the revenue forecasting cycle", r="Division Finance", a="Division Finance", sys="EPM", children=[
                    _s(seq="2.1.1.1", name="Forecast Calendar & Cut-Off Definition", desc="Define monthly forecast calendar, review cadence, submission timelines and forecast cut-off dates for financial year", r="Division Finance", a="Division Finance", sys="EPM"),
                    _s(seq="2.1.1.2", name="Forecast Timeline Communication", desc="Communicate forecast timetable, submission deadlines and cut-off dates to stakeholders. Set automated reminders to communicate ahead of key dates across the financial year", r="Division Finance", a="Division Finance", sys="EPM / Email")
                    ]),
                _s(seq="2.1.2", name="Pipeline Review & Demand Signal Capture", desc="Capture and update opportunity pipeline data from CRM (e.g., HubSpot) into weighted Divisional forecasting model, including awarded-but-not-yet-started contracts and renewals", r="Portfolio Leaders (MD)", a="Portfolio Leaders (MD)", i="Client Services", sys="CRM", children=[
                    _s(seq="2.1.2.1", name="Pipeline Data Review & Update", desc="Review and update opportunity data in CRM (stage, probability, value, timing) to reflect latest client engagement status", r="Client Services / Account Managers", a="Portfolio Leaders (MD)", sys="CRM"),
                    _s(seq="2.1.2.2", name="Opportunity Qualification for Forecast", desc="Identify opportunities for inclusion in current period forecast based on deal stage, probability and expected close date. \"Negotiation\" deal stage included in forecast Pipeline; \"Verbal Award\" and \"Contracted\" included in Committed forecast. Automatically assign weighting as per respective deal stage", r="Client Services / Account Managers", a="Portfolio Leaders (MD)", sys="CRM"),
                    _s(seq="2.1.2.3", name="Work-at-Risk Forecast Alignment", desc="Review and align approved work-at-risk engagements between Sales, Finance and Delivery prior to inclusion in committed forecast", r="Client Services / Account Managers", a="Portfolio Leaders (MD)", i="Sales / Division Finance", sys="N/A"),
                    _s(seq="2.1.2.4", name="Forecast Workflow Submission", desc="Submit updated pipeline and committed forecast inputs for divisional forecast consolidation and review", r="Client Services / Account Managers", a="Portfolio Leaders (MD)", sys="EPM")
                    ]),
                _s(seq="2.1.3", name="Existing Work - Forecast", desc="Review and update forecast for active projects based on delivery progress, staffing changes, scope changes and latest project assumptions", r="Project Manager", a="Project Manager", sys="PSA (Forecasting Module)", children=[
                    _s(seq="2.1.3.1", name="Active Projects Review & Update", desc="Review and update active project forecast data within forecasting module in PSA (e.g., delivery timing, staffing, revenue forecast, scope changes) to reflect latest project status", r="Project Manager", a="Project Manager", i="Client Services / Account Managers", sys="PSA (Forecasting Module)"),
                    _s(seq="2.1.3.2", name="Existing Work Qualification for Forecast", desc="Identify active projects and approved scope changes for inclusion in current period forecast based on latest delivery status, approved changes and delivery confidence", r="Project Manager", a="Project Manager", i="Client Services / Account Managers", sys="PSA (Forecasting Module)"),
                    _s(seq="2.1.3.3", name="Pass-Through Forecast Update", desc="Update expected pass-through revenue forecast in PSA based on agreed SOW treatment (e.g., markup percentage, fixed fee). Create milestone for pass-through and set expected completion date to the period in which the cost is expected to be incurred. Forecast only the markup or fee component as revenue", r="Project Manager", a="Project Manager", i="Client Services / Account Managers", sys="PSA (Forecasting Module)"),
                    _s(seq="2.1.3.4", name="Forecast Workflow Submission", desc="Submit updated existing work forecast inputs for divisional forecast consolidation and review", r="Project Manager", a="Project Manager", sys="EPM")
                    ]),
                _s(seq="2.1.4", name="Divisional Revenue Forecasting", desc="Develop and refine divisional forecast by consolidating weighted pipeline forecast from CRM and active project forecast from PSA into EPM. Align assumptions on delivery timing, probability and forecast inclusion", r="Division Finance", a="Division Finance", i="Commercial Finance", sys="Forecast Tool", children=[
                    _s(seq="2.1.4.1", name="Divisional Forecast Generation", desc="Automatically consolidate weighted pipeline forecast from CRM (HubSpot) and active project forecast from PSA into divisional forecast in EPM by agency, client, service line, geography and time period. Include renewals, approved scope changes and historical demand inputs", r="Division Finance", a="Division Finance", i="Commercial Finance", sys="Fabric (Data Warehouse) / EPM"),
                    _s(seq="2.1.4.2", name="Account Discount & Rebate Forecast Assessment", desc="Calculate expected account-level discounts and rebates based on consolidated current-year forecasted revenue across active projects and weighted pipeline. Where parent-child structure exists for multi-division engagements, use consolidated forecasted revenue across participating divisions to determine annual threshold qualification. Allocate discount/rebate impact proportionately across participating divisions based on forecasted revenue contribution. Parent division Finance leads calculation and governance of the consolidated discount/rebate forecast. Apply discount/rebate treatment only where forecasted revenue is expected to meet agreed annual threshold. Annual spend qualification resets at the start of each financial year", r="Division Finance", a="Division Finance", i="Sales / Project Manager", sys="EPM / Forecast Tool"),
                    _s(seq="2.1.4.3", name="Bottom-Up Forecast Review & Update", desc="In EPM, MDs review bottom-up forecast and assumptions on latest pipeline, delivery, staffing, commercial and pass-through inputs prior to forecast cut-off date. Feed back corrections via Sales (Hubspot) / Prj  Mgrs (PSA) to key in before forecast cut-off date", r="Portfolio Leaders (MD)", a="Portfolio Leaders (MD)", sys="EPM / Forecast Tool")
                    ]),
                _s(seq="2.1.5", name="Finance Forecast Review & Top-Down Adjustments", desc="Following submission cut-off, review bottom-up forecast, challenge assumptions and apply Finance-led top-down adjustments and baseline demand assumptions prior to commitment and forecast publication", r="Division Finance", a="Division Finance", sys="EPM / Forecast Tool", children=[
                    _s(seq="2.1.5.1", name="Historical Revenue & Utilisation Review", desc="Review prior period revenue and utilisation performance to establish baseline demand assumptoins", r="Division Finance", a="Division Finance", sys="EPM / Forecast Tool"),
                    _s(seq="2.1.5.2", name="Trend & Seasonality Analysis", desc="Analyse revenue trends and seasonal patterns by agency, engagement types, commercial model, region, service line, etc.", r="Division Finance", a="Division Finance", sys="EPM / Forecast Tool"),
                    _s(seq="2.1.5.3", name="Input top down drivers / assumptions", desc="Based on analysis, input Finance-led forecast assumptions including utilisation targets, revenue uplift assumptions and “Revenue Gap” expectations from unidentified opportunities", r="Division Finance", a="Division Finance", sys="EPM / Forecast Tool"),
                    _s(seq="2.1.5.4", name="Forecast Review & Challenge", desc="Review all forecast inputs / assumptions including pipeline weighting, delivery timing and forecast variances against historical performance and Finance expectations. Challenge forecast inputs and identify adjustments where required prior to commitment call", r="Division Finance", a="Division Finance", i="Portfolio Leaders (MD)", sys="EPM / Forecast Tool")
                    ]),
                _s(seq="2.1.6", name="Forecast Commitment & Finalisation", desc="Review Finance-adjusted forecast, obtain divisional commitment and finalise forecast publication for downstream planning", r="Division Finance", a="Division Finance", i="Portfolio Leaders (MD)", sys="EPM / Forecast Tool", children=[
                    _s(seq="2.1.6.1", name="Commitment Call", desc="Conduct forecast commitment review led by Division Finance. Review Finance-adjusted forecast assumptions, agree and incorporate final adjustments (real-time) and obtain MD forecast commitment prior to forecast publication. Commitment call should occur c.4 working days post-submission cutoff", r="Division Finance", a="Division Finance", i="Portfolio Leaders (MD)", sys="EPM / Meeting"),
                    _s(seq="2.1.6.2", name="MD Forecast Commitment Received?", desc="Determine whether MDs commit to the Finance-adjusted divisional forecast and associated assumptions", step_type="Decision", r="Portfolio Leaders (MD)", a="Portfolio Leaders (MD)", sys="EPM / Meeting", outcomes="Yes - proceed to 2.1.6.3 | No - proceed to 2.1.4.3"),
                    _s(seq="2.1.6.3", name="Forecast Finalisation & Publication", desc="Finalise and publish forecast version for downstream demand and workforce planning", r="Division Finance", a="Division Finance", sys="EPM / Forecast Tool")
                    ]),
            ],
        },
        {
            "id": "2.2",
            "seq": "2.2",
            "name": "Demand Planning & Workforce Optimisation",
            "description": "Assess current and projected resource capacity against forecasted demand to identify staffing / skills requirements, and optimise workforce plans to meet expected delivery needs",
            "step_type": "Process",
            "system_tool": "PSA",
            "raci": {"r": "Staffing", "a": "Staffing", "i": ""},
            "steps": [
                _s(seq="2.2.1", name="Demand Signal Identification", desc="Translate forecasted revenue and pipeline into demand for roles, skills and capacity. Scope changes to existing projects should be captured timely in PSA to feed into demand planning analysis", r="Staffing", a="Staffing", i="Managing Director (MD)", sys="PSA"),
                _s(seq="2.2.2", name="Capacity Assessment", desc="Assess current workforce capacity, availability and utilisation levels to establish the available capacity baseline", r="Staffing", a="Staffing", i="Managing Director (MD)", sys="PSA"),
                _s(seq="2.2.3", name="Gap Analysis", desc="Compare forecasted demand against available capacity to identify shortfalls or surplus by role, skill, geography and time period", r="Staffing", a="Staffing", sys="PSA"),
                _s(seq="2.2.4", name="Hiring & Subcontractor Planning (Buy/Borrow/Build)", desc="Develop plans to address gaps (e.g., hiring, redeployment, subcontracting). Optimise resource mix to balance utilisation and delivery requirements", r="Staffing", a="Staffing", sys="PSA / HRIS"),
            ],
        },
        {
            "id": "2.3",
            "seq": "2.3",
            "name": "Staffing and Assignments",
            "description": "Match available and planned resources to forecasted demand, and confirm resource commitments for upcoming engagements",
            "step_type": "Process",
            "system_tool": "PSA / BI",
            "raci": {"r": "Staffing", "a": "Staffing", "i": ""},
            "steps": [
                _s(seq="2.3.1", name="Resource Matching & Assignment Proposals", desc="Match available resources to upcoming project requirements based on skills, availability, location and cost rate. Scope changes to existing projects should be captured timely in PSA to feed into resourcing assignments", r="Staffing", a="Staffing", i="Project Manager", sys="PSA"),
                _s(seq="2.3.2", name="Conflict Resolution & Prioritisation", desc="Resolve resource allocation conflicts across competing projects. Prioritise based on strategic value, contractual commitments and margin impact", r="Staffing", a="Staffing", i="Project Manager", sys="PSA"),
                _s(seq="2.3.3", name="Resource Commitment Confirmation", desc="Confirm resource assignments with project managers and resource owners. Update PSA with confirmed allocations", r="Staffing", a="Staffing", i="Project Manager", sys="PSA"),
                _s(seq="2.3.4", name="Supply-Demand Reporting", desc="Produce and distribute supply-demand summary reports to leadership. Highlight utilisation, key risks, capacity constraints and mitigation actions", r="Staffing", a="Staffing", sys="PSA / BI"),
            ],
        },
    ],
}

SERVICE_DELIVERY = {
    "id": "service-delivery",
    "l1_seq": "3",
    "l1_name": "Service Delivery",
    "l1_description": "All operational activities performed during project execution: time capture, expense management, cost allocation and milestone / progress monitoring. Feeds directly into revenue recognition and invoicing.",
    "l1_color": "#0891B2",
    "raci": {"r": "", "a": ""},
    "system_tool": "PSA",
    "stages": [
        {
            "id": "3.1",
            "seq": "3.1",
            "name": "Track Time",
            "description": "Capture and approve time worked on projects to enable accurate cost tracking, billing and revenue recognition",
            "step_type": "Process",
            "system_tool": "PSA",
            "raci": {"r": "", "a": "", "i": ""},
            "steps": [
                _s(seq="3.1.1", name="Time Entry Capture", desc="Record time worked against project tasks, activities and billing category (e.g., billable, non-billable, internal) using only pre-loaded project codes that the individual is approved to charge time against", r="Client Services / Account Managers", a="Client Services / Account Managers", sys="PSA"),
                _s(seq="3.1.2", name="Timesheet Submitted?", desc="Determine whether timesheet was submitted timely and complete", step_type="Decision", r="Automated", a="Client Services / Account Managers", sys="PSA", outcomes="Yes - proceed to 3.1.4 | No - proceed to 3.1.3"),
                _s(seq="3.1.3", name="Missing Timesheet Reminder", desc="Automated email reminder is sent for missing timesheet after submission deadline; PowerBI dashboard simultaneously updated automatically for missing timesheets, and restricts system access until submitted", step_type="Automated", r="Automated", a="Client Services / Account Managers", sys="PSA"),
                _s(seq="3.1.4", name="Timesheet Review & Approval", desc="Project Manager (PM) reviews submitted time for accuracy and completeness. Approves or rejects with comments", r="Project Manager", a="Project Manager", sys="PSA"),
                _s(seq="3.1.5", name="PM Approval Decision", desc="Determine whether submitted timesheet is approved", step_type="Decision", r="Project Manager", a="Project Manager", sys="PSA", outcomes="Yes - proceed to 3.1.6 | No - proceed to 3.1.1"),
                _s(seq="3.1.6", name="Timesheet Posting & Update", desc="Approved timesheet is locked in PSA and actuals are posted to the ERP project ledger. Billable hours are flagged as available for revenue recognition and invoicing runs", r="Project Manager", a="Project Manager", sys="PSA"),
                _s(seq="3.1.7", name="Notify Revenue & Billing Teams", desc="PSA triggers automated notification to Revenue Accounting and Billing that approved billable hours are available for the current period rev rec and invoicing cycles", r="Project Manager", a="Project Manager", sys="PSA"),
                _s(seq="3.1.8", name="Timesheet Adjustment Required?", desc="Determine whether a submitted timesheet needs to be reopened for corrections", step_type="Decision", r="Client Services / Account Managers", a="Client Services / Account Managers", sys="PSA", outcomes="Yes - proceed to 3.1.9 | No - proceed to 3.2"),
                _s(seq="3.1.9", name="Process Timesheet Adjustments", desc="Correct submitted or posted timesheets after approval where changes are required due to missing, incorrect or miscoded time entries", r="Client Services / Account Managers", a="Project Manager", sys="PSA"),
            ],
        },
        {
            "id": "3.2",
            "seq": "3.2",
            "name": "Track Expenses",
            "description": "Capture, validate and approve project-related expenses incurred by resources. Approved expenses are posted to the project cost ledger and passed to billing for client recharge where contractually permitted.",
            "step_type": "Process",
            "system_tool": "Concur/ERP",
            "raci": {"r": "", "a": "", "i": ""},
            "steps": [
                _s(seq="3.2.1", name="Expense Capture", desc="Record project-related expenses with supporting documentation, using only pre-loaded project codes that the individual is approved to charge expenses against", r="Client Services / Account Managers", a="Client Services / Account Managers", sys="Concur"),
                _s(seq="3.2.2", name="Expense Review & Approval", desc="Project Manager (PM) reviews expenses for policy compliance and accuracy. Approves or rejects expense claims with comments", r="Project Manager", a="Project Manager", sys="Concur"),
                _s(seq="3.2.3", name="PM Approval Decision", desc="Determine whether submitted expense report is approved", step_type="Decision", r="Project Manager", a="Project Manager", sys="Concur", outcomes="Yes - proceed to 3.2.4 | No - proceed to 3.2.1"),
                _s(seq="3.2.4", name="Post to Project Cost Ledger & Flag for Billing", desc="Post approved expenses to the system. Update project financial records. Rechargeable items automatically flagged for inclusion in next client invoice run. Non-rechargeable items posted to internal cost centre", r="Project Manager", a="Project Manager", sys="Concur/ERP"),
            ],
        },
        {
            "id": "3.3",
            "seq": "3.3",
            "name": "Track & Allocate Other Costs",
            "description": "Capture and allocate project costs not sourced from timesheets or expense claims (e.g., overheads, sub-contractor invoices, software / tooling licences,  internal shared service allocations, etc.)",
            "step_type": "Process",
            "system_tool": "ERP/PSA",
            "raci": {"r": "GFS", "a": "GFS", "i": ""},
            "steps": [
                _s(seq="3.3.1", name="Cost Identification & Capture", desc="Identify other project-related costs (e.g., subcontractors, overhead allocations). Capture cost details from source systems or inputs", r="GFS", a="GFS", i="Client Services / Account Managers", sys="ERP", children=[
                    _s(seq="3.3.1.1", name="Identify Cost Source & Data Capture", desc="Identify project-related costs from source systems or inputs (e.g., vendor invoices, internal charges, licences) and capture in ERP", r="GFS", a="GFS", sys="ERP"),
                    _s(seq="3.3.1.2", name="Validate Cost Accuracy", desc="Validate cost data for completeness and accuracy", r="GFS", a="GFS", sys="ERP"),
                    _s(seq="3.3.1.3", name="Assign Cost Classification", desc="Assign / validate cost category (e.g., subcontractor, overhead, internal allocation)", r="GFS", a="GFS", sys="ERP")
                    ]),
                _s(seq="3.3.2", name="Cost Allocation", desc="Apply agreed allocation methodology for shared costs (e.g. platform licences, shared tooling, internal IT support) across active projects", r="GFS", sys="ERP", children=[
                    _s(seq="3.3.2.1", name="Allocation Basis Definition", desc="Define cost allocation basis (e.g., usage, headcount, revenue share, fixed split)", r="GFS", a="GFS", sys="ERP"),
                    _s(seq="3.3.2.2", name="Allocation Calculation", desc="Automatically calculate cost allocation across projects based on defined rules", step_type="Automated", r="Automated", a="GFS", sys="ERP"),
                    _s(seq="3.3.2.3", name="Cost Allocation Assignment", desc="Allocate costs to the appropriate project, task or cost object", r="GFS", a="Project Manager", sys="ERP"),
                    _s(seq="3.3.2.4", name="Allocation Validation", desc="Validate allocation results for accuracy and completeness", r="GFS", a="Project Manager", i="Project Manager", sys="ERP"),
                    _s(seq="3.3.2.5", name="Cost Allocation Approval?", desc="Determine whether cost allocations are approved for posting", step_type="Decision", r="GFS", a="GFS", sys="ERP", outcomes="Yes - proceed to 3.3.3 | No - proceed to 3.3.2.1")
                    ]),
                _s(seq="3.3.3", name="Cost Posting", desc="Allocate costs to the appropriate project or activity. Post allocated costs in the ERP to project financials. Update project cost records and enable downstream reporting", r="GFS", a="Project Manager", sys="ERP/PSA", children=[
                    _s(seq="3.3.3.1", name="Cost Posting to Project Ledger", desc="Automatically post allocated costs to project financials in ERP and update project cost balances", step_type="Automated", r="Automated", a="GFS", sys="ERP"),
                    _s(seq="3.3.3.2", name="Cost Synchronisation to PSA", desc="Automatically sync posted costs from ERP to PSA for project tracking", step_type="Automated", r="Automated", a="GFS", sys="PSA")
                    ]),
            ],
        },
        {
            "id": "3.4",
            "seq": "3.4",
            "name": "Milestone & Progress Monitoring",
            "description": "Monitor project progress and milestone completion to support delivery tracking, billing triggers and revenue recognition",
            "step_type": "Process",
            "system_tool": "PSA / ERP",
            "raci": {"r": "Project Manager", "a": "Project Manager", "i": ""},
            "steps": [
                _s(seq="3.4.1", name="Progress Tracking", desc="Track project progress against defined milestones and deliverables. Update task completion status and percentage-complete in PSA. System recalculates forecast-to-complete and estimated completion date.", r="Project Manager", a="Project Manager", sys="PSA", children=[
                    _s(seq="3.4.1.1", name="Percentage of Completion (PoC) Update", desc="Update task, phase, milestone and project PoC in PSA based on latest delivery progress", r="Project Manager", a="Project Manager", sys="PSA"),
                    _s(seq="3.4.1.2", name="Forecast-to-Complete Calculation", desc="Calculate forecast-to-complete based on project progress, milestone status and remaining effort", r="Project Manager", a="Project Manager", sys="PSA")
                    ]),
                _s(seq="3.4.2", name="Milestone Validation", desc="Confirm milestone completion and obtain required approvals or sign-off", r="Project Manager", a="Project Manager", sys="PSA", children=[
                    _s(seq="3.4.2.1", name="Milestone Completion Confirmed?", desc="Confirm that milestone deliverables have been completed in line with agreed scope and acceptance criteria", step_type="Decision", r="Project Manager", a="Project Manager", sys="PSA", outcomes="Yes - proceed to 3.4.2.2 | No - proceed to 3.4.1.1"),
                    _s(seq="3.4.2.2", name="Prepare Milestone Completion Evidence", desc="Compile supporting documentation (e.g., deliverables, sign-offs, acceptance records). Ensure evidence is complete and aligned with contractual requirements", r="Project Manager", a="Project Manager", sys="PSA"),
                    _s(seq="3.4.2.3", name="Submit Deliverables For Client Review", desc="Share deliverables and supporting evidence with client for review", r="Project Manager", a="Project Manager", sys="TBC"),
                    _s(seq="3.4.2.4", name="Client Acceptance Obtained?", desc="Determine whether client has formally accepted milestone deliverables. Capture approval or identify next steps to achieve acceptance", step_type="Decision", r="Project Manager", a="Project Manager", sys="PSA", outcomes="Yes - proceed to 3.4.2.5 | No - proceed to 3.4.1.1"),
                    _s(seq="3.4.2.5", name="Client Acceptance Confirmation", desc="Record client acceptance and supporting sign-off evidence", r="Project Manager", a="Project Manager", sys="PSA")
                    ]),
                _s(seq="3.4.3", name="Progress & Milestone Update", desc="PM marks milestone as complete and accepted in PSA", r="Project Manager", a="Project Manager", sys="PSA"),
                _s(seq="3.4.4", name="Trigger Billing Event", desc="System automatically creates billing event and notifies the Billing team to generate the invoice. Updates revenue recognition schedule.", r="Project Manager", a="Project Manager", sys="PSA / ERP", children=[
                    _s(seq="3.4.4.1", name="Billing Trigger Condition Met?", desc="Automatically determine whether milestone completion, PoC update or time elapsed meets billing trigger conditions", step_type="Decision", r="Automated", a="Project Manager", sys="PSA", outcomes="Yes - proceed to 3.4.4.2 | No - proceed to 3.4.1.1"),
                    _s(seq="3.4.4.2", name="Billing Event Creation", desc="Automatically create billing event based on milestone completion, accepted deliverable, PoC billing or time elapsed trigger", step_type="Automated", r="Automated", a="Project Manager", sys="PSA / ERP"),
                    _s(seq="3.4.4.3", name="Billing Notification Triggered", desc="Automatically notify Billing team of billable milestone or progress event", step_type="Automated", r="Automated", a="Project Manager", sys="PSA / ERP")
                    ]),
            ],
        },
    ],
}

REVENUE_RECOGNITION = {
    "id": "revenue-recognition",
    "l1_seq": "4",
    "l1_name": "Revenue Recognition",
    "l1_description": "All activities to recognise revenue in accordance with revenue recognition rules, posting adjustments and reconcile deferred / accrued balances",
    "l1_color": "#16A34A",
    "raci": {"r": "GFS", "a": "GFS"},
    "system_tool": "ERP",
    "stages": [
        {
            "id": "4.1",
            "seq": "4.1",
            "name": "Revenue Execution & Posting",
            "description": "Calculate revenue based on contract terms/milestones and post journal entries to the GL",
            "step_type": "Process",
            "system_tool": "ERP",
            "raci": {"r": "GFS", "a": "GFS", "i": ""},
            "steps": [
                _s(seq="4.1.1", name="Revenue Recognition Trigger Initiation", desc="Trigger revenue recognition cycle (e.g., period-end). Validate alignment with SOW / MSA terms and revenue recognition rules", r="GFS", a="GFS", sys="ERP", children=[
                    _s(seq="4.1.1.1", name="Initiate Period-End Revenue Cycle", desc="Trigger month-end revenue recognition process based on financial close calendar and projects moving to 'Active' status. Confirm cut-off dates and deadlines", step_type="Automated", r="Automated", a="GFS", sys="ERP"),
                    _s(seq="4.1.1.2", name="Contract & Revenue Rule Validation", desc="Automatically validate alignment with MSA / signed SOW and revenue recognition rules. Confirm billing and revenue recognition are aligned. Projects must be Active in PSA (e.g., signed SOW) to enable revenue recognition", step_type="Automated", r="Automated", a="GFS", sys="ERP"),
                    _s(seq="4.1.1.3", name="Identify Revenue Recognition Method by Project", desc="Where operationally feasible, perform revenue recognition at the primary project level rather than sub-project level to support consolidated revenue treatment and simplify downstream accounting processes.  Determine applicable revenue recognition method per project (or sub-project where required): T&M (time-earned), Fixed Fee (PoC), Milestone (delivery event), SaaS (recurring), Pre-billing (deposit at contract signature), Passthrough (third party, intercompany), etc.", step_type="Automated", r="Automated", a="GFS", sys="ERP"),
                    _s(seq="4.1.1.4", name="Revenue Treatment Routing", desc="Route transactions to appropriate revenue calculation logic based on method", step_type="Automated", r="Automated", a="GFS", sys="ERP")
                    ]),
                _s(seq="4.1.2", name="Revenue Readiness Validation", desc="Confirm required inputs are complete (e.g., approved timesheets, cross-check fixed fee to POC, etc.)", step_type="Automated", r="Automated", a="GFS", sys="PSA / ERP", children=[
                    _s(seq="4.1.2.1", name="Revenue Treatment Routing", desc="Route transactions to appropriate revenue validation logic based on method", step_type="Automated", r="Automated", a="GFS", sys="PSA / ERP"),
                    _s(seq="4.1.2.2", name="T&M: Validate Approved Timecards & Rates", desc="For T&M projects, confirm all timecards for the period are submitted. Reconcile billable hours.", step_type="Automated", r="Automated", a="GFS", i="Project Manager", sys="PSA / ERP"),
                    _s(seq="4.1.2.3", name="Fixed Fee / Milestone: Validate Approved Timecards & Rates; Reconcile Against PoC (or Validate Milestone Completion)", desc="For Fixed Fee / Milestone projects, confirm all timecards for the period are submitted. Automatically reconcile billable hours (timecard-driven) against working budget (at project setup) to derive percentage of completion (PoC). Calculate PoC at the parent project level wherever operationally feasible rather than at sub-project level. GFS to share PoCs with PMs for review.  Milestone - by exception only: Where PoC is not applicable, validate milestone completion and client acceptance status for revenue recognition processing. Proceed to to 4.1.2.5", r="GFS", a="GFS", i="Project Manager", sys="PSA / ERP"),
                    _s(seq="4.1.2.4", name="Fixed Fee / Milestone: PoC Review", desc="Review system-generated PoC. If current understanding of PoC does not agree with calculation, update working budget within PSA to inform revised PoC calculation  Milestone - by exception only: Where PoC is not applicable, skip this step and proceed to 4.1.2.5", r="Project Manager", a="Project Manager", sys="PSA / ERP"),
                    _s(seq="4.1.2.5", name="SaaS: Active Subscription Review", desc="For SaaS and recurring revenue projects, validate active subscription term, contracted recurring revenue, billing schedule and revenue recognition period", r="GFS", a="GFS", i="Client Services / Account Managers", sys="PSA / ERP"),
                    _s(seq="4.1.2.6", name="Validate Passthrough Revenue Treatment (Markup, No Markup, Mgmt. / Service Fee)", desc="Validate passthrough revenue treatment is aligned to agreed SOW terms (e.g., markup, management/service fee or without markup arrangements) and supported by underlying service delivery for gross revenue recognition processing", step_type="Automated", r="Automated", a="GFS", i="Project Manager", sys="PSA / ERP")
                    ]),
                _s(seq="4.1.3", name="Exceptions Identified?", desc="Determine whether there is missing, incomplete or inconsistent data (e.g., timing differences)", step_type="Decision", r="Automated", a="GFS", sys="ERP", outcomes="Yes - proceed to 4.1.4 | No - proceed to 4.1.5"),
                _s(seq="4.1.4", name="Exception Resolution", desc="Resolve identified exceptions", r="GFS", a="GFS", i="Project Manager", sys="ERP", children=[
                    _s(seq="4.1.4.1", name="Investigate Revenue Exception", desc="Identify root cause of exception (e.g., missing timecard, unapproved or unsubmitted expense, inaccurate PoC calculation, etc.", r="GFS", a="GFS", i="Project Manager", sys="ERP"),
                    _s(seq="4.1.4.2", name="Resolve Missing or Incorrect Data", desc="Obtain missing data or correct erroneous inputs (e.g., submit late timecards, approve expense reports, correct PoC calculation)", r="Client Services / Account Managers", a="GFS", i="Project Manager", sys="ERP"),
                    _s(seq="4.1.4.3", name="Obtain Re-Approval if Required", desc="Where corrections change revenue amounts or treatment, obtain re-approval from appropriate authority before proceeding", r="GFS", a="GFS", i="Project Manager", sys="ERP")
                    ]),
                _s(seq="4.1.5", name="Revenue Execution (incl. Accruals & Deferrals)", desc="Revenue is calculated according to revenue recognition rules aligned to contract terms. Recognise accrued revenue for earned but unbilled amounts and deferred revenue for billed but unearned amounts.", r="GFS", a="GFS", sys="PSA/ ERP", children=[
                    _s(seq="4.1.5.1", name="Revenue Treatment Routing", desc="Route transactions to appropriate revenue recognition calculation logic based on method", step_type="Automated", r="Automated", a="GFS", sys="PSA / ERP"),
                    _s(seq="4.1.5.2", name="T&M: Calculate Revenue from Submitted Time", desc="For T&M projects, calculate revenue as submitted hours × contracted rates", r="GFS", a="GFS", sys="PSA / ERP"),
                    _s(seq="4.1.5.3", name="Fixed Fee/Milestone-based: Calculate Revenue from PoC (or by Milestone Completion)", desc="Recognise revenue at the primary project level wherever operationally feasible to support consolidated revenue recognition treatment  For Fixed Fee and milestone-based projects, recognise revenue based on validated percentage of completion against contracted project value  Milestone - by exception only: Where PoC is not applicable, recognise revenue based on value associated with completed milestone", r="GFS", a="GFS", i="Project Manager", sys="PSA / ERP"),
                    _s(seq="4.1.5.4", name="SaaS / Recurring: Calculate Recurring Revenue", desc="For SaaS and recurring revenue projects, recognise recurring revenue ratably over the active subscription period through periodic deferred revenue release based on contracted subscription terms and billing schedule. Exclude one-time fees and non-recurring charges from recurring revenue treatment", r="GFS", a="GFS", sys="PSA / ERP"),
                    _s(seq="4.1.5.5", name="Passthrough Revenue Recognition", desc="Recognise gross passthrough revenue, including associated markup or management / service fee, upon delivery of the underlying service", step_type="Automated", r="Automated", a="GFS", sys="PSA / ERP"),
                    _s(seq="4.1.5.6", name="Calculate Accrued & Deferred Revenue", desc="Calculate accrued revenue for earned but unbilled amounts and deferred revenue for billed but unearned amounts in line with agreed revenue recognition treatment", r="GFS", a="GFS", i="Project Manager", sys="ERP")
                    ]),
                _s(seq="4.1.6", name="Journal Entry Preparation & Routing", desc="Prepare revenue journal entries based on calculated revenue outputs and route for approval in line with financial controls", step_type="Automated", r="Automated", a="GFS", sys="ERP", children=[
                    _s(seq="4.1.6.1", name="Prepare Revenue Journal Entries", desc="Prepare revenue journal entries for recognised revenue, accruals, deferrals and unbilled AR movements based on revenue calculation outputs", step_type="Automated", r="Automated", a="GFS", sys="ERP"),
                    _s(seq="4.1.6.2", name="Route Journals for Approval", desc="Route revenue journal entries for review and approval in line with financial controls and delegation of authority", step_type="Automated", r="Automated", a="GFS", sys="ERP")
                    ]),
                _s(seq="4.1.7", name="Journal Entry Review & Approval", desc="Review and approve revenue journal entries for accuracy, completeness and compliance with revenue recognition policy", r="GFS", a="GFS", sys="ERP", children=[
                    _s(seq="4.1.7.1", name="Journal Entry Review", desc="Review revenue journal entries for accuracy, completeness and compliance with revenue recognition policy", r="GFS", a="GFS", sys="ERP"),
                    _s(seq="4.1.7.2", name="Journal Approved?", desc="Determine whether journal entry is approved for posting. If journal is rejected, return to preparer with rejection reason", step_type="Decision", r="GFS", a="GFS", sys="ERP", outcomes="Yes - proceed to 4.1.8 | No - proceed to 4.1.6.1")
                    ]),
                _s(seq="4.1.8", name="Revenue Posting & Reconciliation", desc="Post revenue journal entries to the general ledger. System updates deferred revenue, accrued revenue and unbilled AR balances accordingly", r="GFS", a="GFS", sys="ERP", children=[
                    _s(seq="4.1.8.1", name="Journal Entry Posting", desc="Post approved revenue journal entries to the general ledger. System updates revenue accounts automatically", r="GFS", a="GFS", sys="ERP"),
                    _s(seq="4.1.8.2", name="Deferred / Accrued Balance Reconciliation", desc="System automatically updates deferred revenue, accrued revenue and unbilled AR balances based on posted revenue activity", step_type="Automated", r="Automated", a="GFS", sys="ERP")
                    ]),
            ],
        },
        {
            "id": "4.2",
            "seq": "4.2",
            "name": "Adjustments & True-Ups (e.g. Rebates)",
            "description": "Process post-recognition revenue adjustments and accounting true-ups resulting from updated commercial, contractual or accounting information (e.g., rebates, contract modifications, scope changes, etc.)",
            "step_type": "Process",
            "system_tool": "ERP",
            "raci": {"r": "GFS", "a": "GFS", "i": ""},
            "steps": [
                _s(seq="4.2.1", name="Adjustment Identification & Validation", desc="Identify revenue adjustment events, validate supporting documentation and determine required accounting treatment", r="GFS", a="GFS", i="Project Manager", sys="ERP", children=[
                    _s(seq="4.2.1.1", name="Identify & Validate Adjustment", desc="Identify events requiring revenue adjustment or accounting true-up (e.g., rebate accruals, contract modifications, revenue reversals or accrual/deferral adjustments). Validate supporting documentation, approvals and required accounting treatment", r="GFS", a="GFS", i="Project Manager", sys="ERP")
                    ]),
                _s(seq="4.2.2", name="Adjustment Calculation & Journal Preparation", desc="Calculate financial impact of adjustment and prepare associated journal entries", r="GFS", a="GFS", sys="ERP", children=[
                    _s(seq="4.2.2.1", name="Calculate Adjustment & Prepare Journals", desc="Calculate financial impact of adjustment or true-up, determine accounting treatment and prepare associated journal entries", r="GFS", a="GFS", sys="ERP"),
                    _s(seq="4.2.2.2", name="Route Journals for Approval", desc="Route adjustment journal entries for approval in line with financial controls and delegation of authority", r="GFS", a="GFS", sys="ERP")
                    ]),
                _s(seq="4.2.3", name="Journal Review & Approval", desc="Review and approve journal entries in line with financial controls", r="GFS", a="GFS", sys="ERP", children=[
                    _s(seq="4.2.3.1", name="Journal Entry Review", desc="Review adjustment journal entries for accuracy, completeness and compliance with revenue recognition policy", r="GFS", a="GFS", sys="ERP"),
                    _s(seq="4.2.3.2", name="Journal Approved?", desc="Determine whether adjustment journal entry is approved for posting. If journal is rejected, return to preparer with rejection reason", step_type="Decision", r="GFS", a="GFS", sys="ERP", outcomes="Yes - proceed to 4.2.6 | No - proceed to 4.2.2.1")
                    ]),
                _s(seq="4.2.6", name="Adjustment Posting", desc="Post adjustment or true-up journal entries to the general ledger. Update project and financial records accordingly. Systematic update to revenue forecast.", r="GFS", a="GFS", sys="ERP", children=[
                    _s(seq="4.2.6.1", name="Journal Entry Posting", desc="Post approved revenue journal entries to the general ledger. System updates revenue and balance sheet accounts automatically", step_type="Automated", r="Automated", a="GFS", sys="ERP"),
                    _s(seq="4.2.6.3", name="Deferred / Accrued Balance Update", desc="System automatically updates deferred revenue, accrued revenue and unbilled AR balances based on posted adjustment activity", step_type="Automated", r="Automated", a="GFS", sys="ERP")
                    ]),
            ],
        },
    ],
}

INVOICING_AND_BILLING = {
    "id": "invoicing-billing",
    "l1_seq": "5",
    "l1_name": "Invoicing & Billing",
    "l1_description": "End-to-end process to prepare, review, approve and issue client invoices for project and recurring revenue arrangements, including client review cycles and passthrough billing",
    "l1_color": "#D97706",
    "raci": {"r": "GFS", "a": "GFS"},
    "system_tool": "ERP",
    "stages": [
        {
            "id": "5.1",
            "seq": "5.1",
            "name": "Invoice Preparation & Internal Review (incl. Billing on Behalf)",
            "description": "Generate draft invoices from Billing Agent / ERP based on agreed billing triggers, billing inputs and contract terms. Perform internal quality review prior to client submission",
            "step_type": "Process",
            "system_tool": "ERP",
            "raci": {"r": "GFS", "a": "GFS", "i": "Project Manager"},
            "steps": [
                _s(seq="5.1.1", name="Invoice Submission Calendar", desc="Define and communicate invoice timetable and cut-off dates for each financial period", r="GFS", a="GFS", sys="ERP", children=[
                    _s(seq="5.1.1.2", name="Invoice Calendar & Cut-Off Definition", desc="Define invoice timetable and invoice cut-off dates for each financial period", r="GFS", a="GFS", sys="ERP"),
                    _s(seq="5.1.1.3", name="Invoice Timeline Communication", desc="Communicate invoice timetable, submission deadlines and cut-off dates to stakeholders ahead of each financial period. Send automated reminders in advance of key billing deadlines", r="GFS", a="GFS", sys="ERP")
                    ]),
                _s(seq="5.1.2", name="Invoice Trigger Initiated", desc="Trigger invoice cycle based on agreed billing events and invoicing arrangements (e.g., scheduled billing date, milestone completion, pre-billing, etc.)", r="AI Agent - Billing (or GFS in absence of Agent)", a="GFS", sys="ERP / PSA / Billing Agent Tool", children=[
                    _s(seq="5.1.2.1", name="Identify Billing Pathway", desc="Determine applicable billing pathway and route to appropriate invoicing process. Where agreed under SOW / MSA terms, scheduled billing should be used for T&M and Fixed Fee engagements to support downstream billing automation", r="AI Agent - Billing (or GFS in absence of Agent)", a="GFS", sys="Billing Agent"),
                    _s(seq="5.1.2.2", name="T&M Trigger: Billing Event Achieved", desc="For T&M projects, trigger invoice cycle based on agreed billing structure (e.g., scheduled billing date reached or submitted billable hours for the current billing period under non-scheduled billing arrangements)", r="AI Agent - Billing (or GFS in absence of Agent)", a="GFS", sys="PSA"),
                    _s(seq="5.1.2.3", name="Milestone Trigger: Billing Milestone Achieved", desc="For milestone-based billing arrangements, billing milestone achieved and invoicing event triggered", r="AI Agent - Billing (or GFS in absence of Agent)", a="GFS", i="Project Manager", sys="PSA"),
                    _s(seq="5.1.2.4", name="Fixed Fee / Scheduled Billing Trigger: Billing Date Achieved", desc="For fixed fee using scheduled billing arrangements, scheduled billing date reached for invoicing cycle initiation", r="AI Agent - Billing (or GFS in absence of Agent)", a="GFS", sys="Billing Agent"),
                    _s(seq="5.1.2.5", name="SaaS / Recurring Trigger: Billing Cycle Active", desc="For SaaS / recurring revenue billing arrangements, recurring billing cycle reaches scheduled invoicing period", r="AI Agent - Billing (or GFS in absence of Agent)", a="GFS", sys="Billing Agent"),
                    _s(seq="5.1.2.6", name="Upfront Billing Trigger: Signed SOW Achieved", desc="For upfront or pre-billing arrangements, SOW with upfront billing requirements is executed, and milestone is created and marked as complete to trigger invoice cycle initiation", r="AI Agent - Billing (or GFS in absence of Agent)", a="GFS", sys="Billing Agent"),
                    _s(seq="5.1.2.7", name="Ad-Hoc Billing Trigger Initiated", desc="Trigger off-cycle or discretionary invoice generation based on approved client request or commercial agreement outside standard billing schedule", r="AI Agent - Billing (or GFS in absence of Agent)", a="GFS", i="Client Services / Account Managers", sys="Billing Agent"),
                    _s(seq="5.1.2.8", name="Expense Trigger: Approved Expense Submitted", desc="Approved reimbursable expenses submitted and available for invoicing for the billing period", r="AI Agent - Billing (or GFS in absence of Agent)", a="GFS", sys="Billing Agent / Concur"),
                    _s(seq="5.1.2.9", name="Passthrough Billing Trigger: Cost Incurred (Markup, No Markup, Mgmt. / Service Fee)", desc="Passthrough costs incurred and available for invoicing", r="AI Agent - Billing (or GFS in absence of Agent)", a="GFS", sys="Billing Agent")
                    ]),
                _s(seq="5.1.3", name="Billing Validation & Exception Handling", desc="Validate billing inputs, contract alignment and billing trigger conditions. Identify and resolve billing exceptions prior to invoice generation", r="AI Agent - Billing (or GFS in absence of Agent)", a="GFS", i="Project Manager", sys="ERP / PSA / Billing Agent Tool", children=[
                    _s(seq="5.1.3.1", name="Contract, PO & Billing Validation", desc="AUtomatically validate billing inputs against SOW, MSA, billing schedule and PO requirements. Confirm an active, valid Purchase Order is linked to the project with sufficient remaining balance to cover the billing amount, and compare to SOW/MSA for legal enttiy name, billing entity name, scope, milestone schedule alignment. Flag exceptions for GFS review and escalation", r="AI Agent - Billing (or GFS in absence of Agent)", a="GFS", sys="CLM / Billing Agent Tool"),
                    _s(seq="5.1.3.2", name="T&M: Billing Input Validation", desc="Validate submitted billable hours, contracted rates and billing summaries for the billing period. Validate against agreed T&M billing caps where applicable, as per SOW. For T&M projects using scheduled billing arrangements, validate scheduled invoice amounts and associated billing schedule", r="AI Agent - Billing (or GFS in absence of Agent)", a="GFS", sys="ERP / PSA / Billing Agent Tool"),
                    _s(seq="5.1.3.3", name="Milestone: Billing Input Validation", desc="Validate milestone completion, client acceptance and agreed billing amounts in line with contracted milestone billing terms", r="AI Agent - Billing (or GFS in absence of Agent)", a="GFS", i="Project Manager", sys="ERP / PSA / Billing Agent Tool"),
                    _s(seq="5.1.3.4", name="Fixed Fee / Scheduled: Billing Validation", desc="Validate agreed billing dates and scheduled invoice amounts in line with contracted billing schedule", r="AI Agent - Billing (or GFS in absence of Agent)", a="GFS", sys="ERP / PSA / Billing Agent Tool"),
                    _s(seq="5.1.3.5", name="SaaS / Recurring: Billing Validation", desc="Validate recurring billing schedule, subscription terms and contracted recurring invoice amounts for the billing period. Exclude one-time fees and non-recurring charges from recurring billing validation", r="AI Agent - Billing (or GFS in absence of Agent)", a="GFS", sys="ERP / PSA / Billing Agent Tool"),
                    _s(seq="5.1.3.6", name="Upfront / Pre-billing: Billing Validation", desc="Validate executed SOW, agreed upfront billing amount and associated billing trigger prior to invoice generation", r="AI Agent - Billing (or GFS in absence of Agent)", a="GFS", sys="ERP / PSA / Billing Agent Tool"),
                    _s(seq="5.1.3.7", name="Ad-Hoc Billing Validation", desc="Validate approved ad-hoc billing request, agreed billing amount and required approval prior to invoice generation", r="GFS", a="GFS", i="Client Services / Account Managers", sys="ERP / PSA / Billing Agent Tool"),
                    _s(seq="5.1.3.7", name="Expense & Approved Costs: Billing Validation", desc="Confirm all expenses and third-party costs for the billing period have been submitted and approved", r="AI Agent - Billing (or GFS in absence of Agent)", a="GFS", i="Project Manager", sys="ERP / PSA / Billing Agent Tool"),
                    _s(seq="5.1.3.8", name="Passthrough (Markup, No Markup, Mgmt. / Service Fee): Billing Validation", desc="Validate passthrough charges, supporting documentation and agreed SOW billing treatment prior to invoice generation", r="AI Agent - Billing (or GFS in absence of Agent)", a="GFS", sys="ERP / PSA / Billing Agent Tool"),
                    _s(seq="5.1.3.9", name="Billing Validation Passed?", desc="Determine whether billing validation criteria have been met", step_type="Decision", r="AI Agent - Billing (or GFS in absence of Agent)", a="GFS", sys="Billing Agent Tool", outcomes="Yes - proceed to 5.1.6 | No - proceed to 5.1.4")
                    ]),
                _s(seq="5.1.4", name="Mismatch Identified?", desc="Determine whether discrepancies exist between billing inputs, contract terms and invoicing requirements (e.g., rates, milestones, PO values or billing entities)", step_type="Decision", r="AI Agent - Billing (or GFS in absence of Agent)", a="GFS", sys="ERP", outcomes="Yes - proceed to 5.1.5 | No - proceed to 5.1.6"),
                _s(seq="5.1.5", name="Mismatch Resolution", desc="Investigate and resolve billing discrepancies and apply required corrections prior to invoice generation", r="GFS", a="Client Services / Account Managers", sys="Billing Agent / ERP / PSA", children=[
                    _s(seq="5.1.5.1", name="Billing Exception Investigation", desc="Investigate root cause of billing discrepancy (e.g., rate card error, unapproved time, milestone variance, PO shortfall or incorrect legal entity) with Client Services or Project Manager. Determine corrective action and client communication requirements", r="GFS", a="Client Services / Account Managers", i="Project Manager", sys="Billing Agent / ERP / PSA"),
                    _s(seq="5.1.5.2", name="Billing Data Correction", desc="Apply corrections to billing inputs, timecards, expenses, milestones or contract data where required. Obtain re-approval where necessary", r="GFS", a="Client Services / Account Managers", sys="Billing Agent / ERP / PSA"),
                    _s(seq="5.1.5.3", name="Billing Validation Recheck", desc="Re-run billing validation checks after corrections are applied and confirm discrepancy has been resolved prior to invoice generation", r="GFS", a="Client Services / Account Managers", sys="Billing Agent / ERP / PSA")
                    ]),
                _s(seq="5.1.6", name="Billing Data Preparation, Consolidation & Formatting", desc="Compile billable items, apply billing treatments and prepare invoice structure, including consolidation across projects (parent / IHL-billing) and clinet-specific invoicing requirements, as required", r="AI Agent - Billing (or GFS in absence of Agent)", a="GFS", i="Client Services / Account Managers", sys="Billing Agent / PSA", children=[
                    _s(seq="5.1.6.1", name="T&M Billing Data Compilation", desc="For T&M billing, automatically compile submitted billable hours and contracted billing rates for the invoicing period. Apply agreed T&M billing caps where applicable, as per SOW. Where scheduled billing arrangements apply, compile invoice amounts  in line with contracted billing schedule in executed SOW", r="AI Agent - Billing (or GFS in absence of Agent)", a="GFS", sys="Billing Agent / PSA"),
                    _s(seq="5.1.6.2", name="Milestone Billing Compilation", desc="For Milestone billing, automatically compile milestone billing amounts based on achieved billing milestones and client acceptance status", r="AI Agent - Billing (or GFS in absence of Agent)", a="GFS", sys="Billing Agent / PSA"),
                    _s(seq="5.1.6.3", name="Fixed Fee / Scheduled Billing Compilation", desc="For Fixed Fee / Scheduled billing, automatically compile scheduled billing amounts and agreed invoice values for the invoicing period in line with contracted billing schedule in executed SOW", r="AI Agent - Billing (or GFS in absence of Agent)", a="GFS", sys="Billing Agent / PSA"),
                    _s(seq="5.1.6.4", name="SaaS / Recurring Billing Compilation", desc="For SaaS / Recurring billing, automatically compile recurring subscription billing amounts for the invoicing period", r="AI Agent - Billing (or GFS in absence of Agent)", a="GFS", sys="Billing Agent / PSA"),
                    _s(seq="5.1.6.5", name="Upfront Billing Compilation", desc="For upfront billing, automatically compile agreed upfront or pre-billing invoice amounts in line with contracted billing terms and approved billing trigger", r="AI Agent - Billing (or GFS in absence of Agent)", a="GFS", sys="Billing Agent / PSA"),
                    _s(seq="5.1.6.6", name="Ad-Hoc Billing Compilation", desc="Compile approved ad-hoc billing amounts and supporting billing detail for invoice generation in line with approved billing request", r="AI Agent - Billing (or GFS in absence of Agent)", a="GFS", i="Client Services / Account Managers", sys="Billing Agent / PSA"),
                    _s(seq="5.1.6.7", name="Expense Compilation", desc="Automatically compile approved reimbursable employee and project expenses for invoice generation", r="AI Agent - Billing (or GFS in absence of Agent)", a="GFS", sys="Billing Agent / PSA"),
                    _s(seq="5.1.6.8", name="Passthrough Billing Compilation", desc="Compile passthrough billing amounts, including associated markup or management/service fee amounts, for invoice generation in line with agreed SOW treatment. Prompt billing user to determine whether passthrough costs and associated markup / mgmt. fee should appear as combined or separate invoice line items based on client preference", r="AI Agent - Billing (or GFS in absence of Agent)", a="GFS", sys="Billing Agent / PSA"),
                    _s(seq="5.1.6.9", name="Invoice Formatting & Delivery Method Determination", desc="Use standardised invoice templates where possible to support downstream billing consistency and automation. Prompt user to apply invoice template, billing format, client-specific invoicing requirements and invoice delivery method. Where e-invoicing is required under MSA or billing master data, default invoice generation to structured e-invoicing rather than PDF output", r="Client Services / Account Managers", a="GFS", i="Project Manager", sys="Billing Agent"),
                    _s(seq="5.1.6.10", name="Invoice Narration & Supporting Documentation", desc="Include invoice narrative, billing period references, deliverables, client-specific language and supplemental attachments where required under contract terms. Include SOW reference ID / Project Number and PO Number in narrative", r="Client Services / Account Managers", a="GFS", i="Project Manager", sys="Billing Agent"),
                    _s(seq="5.1.6.11", name="Billing Adjustment & Hold Review", desc="Prompt user to review and apply billing adjustments including credits, write-downs, billing holds and excluded line items prior to invoice generation", r="Client Services / Account Managers", a="GFS", i="Project Manager", sys="Billing Agent")
                    ]),
                _s(seq="5.1.7", name="Invoice Preparation", desc="Generate draft invoice structure, apply billing-on-behalf requirements and prepare invoice output for internal review", r="AI Agent - Billing (or GFS in absence of Agent)", a="GFS", i="Project Manager", sys="Billing Agent", children=[
                    _s(seq="5.1.7.1", name="Billing on Behalf Consolidation", desc="Where consolidated billing is required, consolidate billing events, invoice amounts and supporting billing data across contributing projects, divisions or entities for centralised invoice generation under lead Parent or IHL billing entity, as per SOW", r="AI Agent - Billing (or GFS in absence of Agent)", a="GFS", sys="Billing Agent"),
                    _s(seq="5.1.7.2", name="Intercompany Billing Determination", desc="Determine whether intercompany recharge treatment is required where work is delivered by one entity and billed through another entity", step_type="Decision", r="AI Agent - Billing (or GFS in absence of Agent)", a="GFS", sys="Billing Agent", outcomes="Yes - proceed to 5.3.3.3 | No - proceed to 5.1.7.3"),
                    _s(seq="5.1.7.3", name="Draft Invoice Generation", desc="Generate draft invoice in billing currency using compiled billing data, approved adjustments and invoice structure", r="AI Agent - Billing (or GFS in absence of Agent)", a="GFS", sys="Billing Agent"),
                    _s(seq="5.1.7.4", name="Tax Calculation", desc="Apply and validate tax treatment based on billing entity jurisdiction, client location, service type and invoicing method", r="AI Agent - Billing (or GFS in absence of Agent)", a="GFS", sys="Billing Agent"),
                    _s(seq="5.1.7.5", name="Invoice / E-Invoice Validation", desc="Generate final invoice preview or structured e-invoice validation output for internal review prior to client submission. Billing Agent performs initial review of invoice against standard validation checklist and historical invoices: validation against SOW, PO and supporting documentation, entity name, billing address, payment terms, invoice period, currency, amounts, remittance details, tax and submission instructions", r="AI Agent - Billing (or GFS in absence of Agent)", a="GFS", sys="Billing Agent"),
                    _s(seq="5.1.7.6", name="Invoice Validation Passed?", desc="Determine whether invoice passes automated billing validation checks and is approved for downstream review or client submission", step_type="Decision", r="AI Agent - Billing (or GFS in absence of Agent)", a="GFS", sys="Billing Agent", outcomes="Yes - proceed to 5.1.8 | No - proceed to 5.1.7.7"),
                    _s(seq="5.1.7.7", name="Invoice Correction & Regeneration", desc="Correct invoice formatting, language, date or billing data discrepancies and regenerate invoice output. Where billing amounts or billing data are incorrect, proceed to step 5.1.3 for correction and reprocessing", r="GFS", a="GFS", i="Project Manager", sys="Billing Agent")
                    ]),
                _s(seq="5.1.8", name="T&M only: Client Services / Operations Review", desc="Route invoice for Project Manager review where required (T&M only) prior to client submission", r="Project Manager", a="Project Manager", sys="Billing Agent", children=[
                    _s(seq="5.1.8.1", name="Invoice Routing", desc="Route invoice to Client Services via automated workflow for review and approval where required", r="AI Agent - Billing (or GFS in absence of Agent)", a="GFS", sys="Billing Agent"),
                    _s(seq="5.1.8.2", name="PM Review", desc="Review invoice for billing accuracy, client-specific invoicing requirements and completeness of supporting information prior to client submission", r="Project Manager", a="Project Manager", sys="Billing Agent"),
                    _s(seq="5.1.8.3", name="Invoice Approved for Client Submission?", desc="Determine whether invoice and billing inputs are approved for client submission. If rejected, provide reasoning", step_type="Decision", r="Project Manager", a="Project Manager", sys="Billing Agent / ERP / PSA", outcomes="Yes - proceed to 5.2 | No - proceed to 5.1.6.1")
                    ]),
            ],
        },
        {
            "id": "5.2",
            "seq": "5.2",
            "name": "Client Review & Approval",
            "description": "Facilitate client review of draft invoice, resolve queries and obtain approval",
            "step_type": "Process",
            "system_tool": "ERP / Client Portal / Email",
            "raci": {"r": "GFS / Client Services", "a": "GFS", "i": ""},
            "steps": [
                _s(seq="5.2.1", name="Draft Invoice Submission for Client Review", desc="Submit draft invoice to client for review where required under agreed billing arrangements or client requirements", r="GFS / Client Services", a="GFS", sys="ERP / Client Portal / Email", children=[
                    _s(seq="5.2.1.1", name="Identify Client Submission Method", desc="Determine required client submission channel for draft review (e.g., email or secure file-sharing channel)", r="Client Services / Account Managers", a="GFS", sys="ERP / Client Portal / Email"),
                    _s(seq="5.2.1.2", name="Submit Draft Invoice for Client Review", desc="Transmit invoice to client via agreed submission channel. Include supporting documentation as required (e.g. timesheets, deliverable summaries). Confirm agreed client review and response timeframe", r="GFS", a="GFS", i="Client Services / Account Managers", sys="ERP / Client Portal / Email")
                    ]),
                _s(seq="5.2.2", name="Client Query Raised?", desc="Monitor for client response or billing query within agreed SLA", step_type="Decision", r="GFS", a="GFS", sys="ERP / Client Portal / Email", outcomes="Yes - proceed to 5.2.3 | No - proceed to 5.2.4"),
                _s(seq="5.2.3", name="Client Query Resolution", desc="Address client queries or disputes. Provide supporting documentation or revise invoice as required", r="GFS", a="GFS", i="Client Services / Account Managers", sys="ERP / Client Portal / Email", children=[
                    _s(seq="5.2.3.1", name="Receive & Log Client Query", desc="Capture client query details, categorise issue type (amount, scope, format, PO, compliance)", r="GFS", a="GFS", sys="ERP / Client Portal / Email"),
                    _s(seq="5.2.3.2", name="Investigate, Resolve & Prepare Response", desc="Review client query against contract terms, billing data and supporting documentation. Resolve query and prepare client response or invoice revision where required", r="GFS", a="GFS", i="Client Services / Account Managers", sys="ERP / Client Portal / Email"),
                    _s(seq="5.2.3.3", name="Revise Draft Invoice if Required", desc="If query results in an invoice change, correct billing data and regenerate draft invoice", r="GFS", a="GFS", i="Client Services / Account Managers", sys="ERP / Client Portal / Email")
                    ]),
                _s(seq="5.2.4", name="Client Approval", desc="Obtain client approval to proceed with invoice issuance", r="GFS", a="GFS", i="Client Services / Account Managers", sys="ERP / Client Portal / Email"),
            ],
        },
        {
            "id": "5.3",
            "seq": "5.3",
            "name": "Execution & Submission",
            "description": "Finalise and issue invoice, post accounts receivable and update billing records to enable tracking and collection",
            "step_type": "Process",
            "system_tool": "Billing Agent / ERP",
            "raci": {"r": "GFS", "a": "GFS", "i": ""},
            "steps": [
                _s(seq="5.3.1", name="Finalise Invoice", desc="Finalise invoice structure, validate final invoice output and prepare invoice for client issuance", r="GFS", a="GFS", sys="Billing Agent", children=[
                    _s(seq="5.3.1.1", name="Final Invoice Generation", desc="Push to ERP to generate final invoice output in billing currency using approved billing data, invoice structure and client-specific invoicing requirements", r="GFS", a="GFS", sys="Billing Agent"),
                    _s(seq="5.3.1.2", name="Final Invoice / E-Invoice Validation", desc="Perform final invoice validation and structured e-invoice checks prior to client issuance, including validation of invoice data completeness, submission requirements and formatting standards", r="GFS", a="GFS", sys="Billing Agent")
                    ]),
                _s(seq="5.3.2", name="Invoice Submission to Client", desc="Submit final invoice to client via agreed submission channel and confirm successful invoice issuance", r="GFS", a="GFS", sys="ERP / Client Portal / Email", children=[
                    _s(seq="5.3.2.1", name="Submit Final Invoice via Client Channel", desc="Issue final approved invoice to client via required submission channel (e.g., email, AP portal, EDI or structured e-invoicing submission). For IC clients (e.g. Regeneron), follow client-specific submission protocol.", r="GFS", a="GFS", sys="ERP / Client Portal / Email"),
                    _s(seq="5.3.2.2", name="Invoice Submission Successful?", desc="Determine whether invoice or e-invoice submission completed successfully and was accepted by the client submission channel", step_type="Decision", r="GFS", a="GFS", sys="ERP", outcomes="Yes - proceed to 5.3.2.2 | No - proceed to 5.3.2.3"),
                    _s(seq="5.3.2.2", name="Submission Confirmation & Audit Capture", desc="Capture invoice submission confirmation, transmission status and supporting audit records for invoice issuance tracking", r="GFS", a="GFS", sys="ERP"),
                    _s(seq="5.3.2.3", name="Invoice Submission Rejection Resolution", desc="Investigate invoice or e-invoice rejection, correct submission, formatting or compliance issues and regenerate / re-submit invoice where required", r="GFS", a="GFS", i="Client Services / Account Managers", sys="ERP"),
                    _s(seq="5.3.2.4", name="Attach Invoice & Confirmation to Project Record", desc="Attach final invoice output and submission confirmation to ERP project record and associated document repositories where required", r="GFS", a="GFS", i="Client Services / Account Managers", sys="ERP")
                    ]),
                _s(seq="5.3.3", name="AR Posting & Accounting Update", desc="Post issued invoice to AR sub-ledger and update associated accounting balances and AR aging", r="GFS", a="GFS", sys="ERP", children=[
                    _s(seq="5.3.3.1", name="Post Invoice to AR Sub-Ledger", desc="Automatically post finalised invoice to AR sub-ledger and update customer balance. System generates AR aging entry and updates project billing records", step_type="Automated", r="Automated", a="GFS", sys="ERP"),
                    _s(seq="5.3.3.2", name="Update Deferred / Unbilled Revenue Balances", desc="Automatically update unbilled AR, accrued revenue and deferred revenue balances resulting from issued invoice activity", step_type="Automated", r="Automated", a="GFS", sys="ERP"),
                    _s(seq="5.3.3.3", name="Raise Intercompany Recharge Request", desc="Complete intercompany recharge request with provider and receiver entity details and initiate intercompany accounting process", r="GFS", a="GFS", sys="ERP")
                    ]),
                _s(seq="5.3.4", name="Reconciliation", desc="Perform billing reconciliations (e.g., from parent billing level to sub-project level, from central billing level to project-level by division)", r="GFS", a="GFS", sys="ERP", children=[
                    _s(seq="5.3.4.1", name="Billing-to-Contract Reconciliation", desc="Reconcile billed amounts against contract value, SOW billing schedule, approved billing events and PO balances. Identify overbilling, underbilling or remaining uninvoiced amounts", r="GFS", a="GFS", sys="ERP"),
                    _s(seq="5.3.4.2", name="Intercompany Billing Reconciliation", desc="Reconcile intercompany recharge balances and confirm associated accounting entries are settled between entities", r="GFS", a="GFS", sys="ERP"),
                    _s(seq="5.3.4.3", name="Month-End Billing Close", desc="Complete month-end billing reconciliation and confirm all invoices for the billing period have been generated, submitted and posted prior to billing period close", r="GFS", a="GFS", sys="ERP")
                    ]),
            ],
        },
    ],
}

COLLECTIONS = {
    "id": "collections",
    "l1_seq": "6",
    "l1_name": "Collections",
    "l1_description": "All activities to collect outstanding AR, manage overdue accounts, reconcile receipts, and forecast cash",
    "l1_color": "#2563EB",
    "raci": {"r": "GFS", "a": "GFS"},
    "system_tool": "ERP",
    "stages": [
        {
            "id": "6.1",
            "seq": "6.1",
            "name": "Reconciliation & Analysis",
            "description": "Maintain an accurate, up-to-date AR ledger. Reconcile cash receipts to invoices, identify unapplied cash, and produce aging analysis for management review",
            "step_type": "Process",
            "system_tool": "ERP",
            "raci": {"r": "GFS", "a": "GFS", "i": ""},
            "steps": [
                _s(seq="6.1.1", name="Run AR Aging Report", desc="Generate aging report from ERP and identify outstanding balances by client, due date, and days overdue", r="GFS", a="GFS", sys="ERP", children=[
                    _s(seq="6.1.1.1", name="Generate AR Aging Report from ERP", desc="Generate AR aging report showing outstanding invoices by client, entity, due date and days overdue", r="GFS", a="GFS", sys="ERP"),
                    _s(seq="6.1.1.1", name="Segment & Prioritise Outstanding Balances", desc="Categorise outstanding AR by aging bucket, client risk, value and entity. Identify invoices requiring immediate attention (e.g., high risk balances)", r="GFS", a="GFS", sys="ERP")
                    ]),
                _s(seq="6.1.2", name="Apply Cash Receipts", desc="Match and apply incoming payments to invoices in ERP", r="GFS", a="GFS", sys="ERP", children=[
                    _s(seq="6.1.2.1", name="Import Bank Statement / Payment Data", desc="Automatically import daily bank statement or payment file into ERP for cash application processing.", step_type="Automated", r="Automated", a="GFS", sys="ERP / AR Tool"),
                    _s(seq="6.1.2.2", name="Match Payments to Invoices", desc="Automatically match incoming payments to outstanding invoices using remittance advice, invoice number or client reference", step_type="Automated", r="Automated", a="GFS", sys="ERP / AR Tool"),
                    _s(seq="6.1.2.3", name="Cash Application", desc="Automatically apply full or partial payments to invoices in ERP", step_type="Automated", r="Automated", a="GFS", sys="ERP / AR Tool"),
                    _s(seq="6.1.2.4", name="Post Applied Cash in ERP", desc="Automatically post matched payment against invoice in AR sub-ledger, and update invoice status and AR aging accordingly.", step_type="Automated", r="Automated", a="GFS", sys="ERP / AR Tool")
                    ]),
                _s(seq="6.1.3", name="Unapplied / Unallocated Cash Identified?", desc="Determine whether there are unmatched or partially applied payments", step_type="Decision", r="Automated", a="GFS", sys="ERP / AR Tool", outcomes="Yes - proceed to 6.1.4 | No - proceed to 6.1.5"),
                _s(seq="6.1.4", name="Investigate & Resolve Unallocated Cash", desc="Investigate any short payments, overpayments or unallocated cash. Resolve discrepancies, disputes or allocation issues. Apply or refund as appropriate. Document resolution in ERP.", r="GFS", a="GFS", i="Client Services / Account Managers", sys="ERP / AR Tool", children=[
                    _s(seq="6.1.4.1", name="Investigate Short / Over / Unmatched Payments", desc="Analyse unallocated cash to determine cause: short payment, overpayment, payment on account, wrong entity, or missing remittance detail.", r="GFS", a="GFS", sys="ERP / AR Tool"),
                    _s(seq="6.1.4.2", name="Root Cause Investigation", desc="Reach out to client AP team or internal operations to obtain remittance details, correct allocation instructions or dispute information", r="GFS", a="GFS", i="Client Services / Account Managers", sys="ERP / AR Tool"),
                    _s(seq="6.1.4.3", name="Resolution Processing", desc="Apply corrections, reallocate payments or process refunds as required", r="GFS", a="GFS", sys="ERP / AR Tool"),
                    _s(seq="6.1.4.4", name="Record Resolution", desc="Record resolution details and update transaction status in ERP", r="GFS", a="GFS", sys="ERP")
                    ]),
                _s(seq="6.1.5", name="AR Reconciliation", desc="Reconcile AR subledger to GL and confirm balances. Identify and resolve any differences.", r="GFS", a="GFS", sys="ERP", children=[
                    _s(seq="6.1.5.1", name="Reconcile AR Sub-Ledger to General Ledger", desc="Automatically compare AR sub-ledger balances to GL control account", r="GFS", a="GFS", sys="ERP / AR Tool"),
                    _s(seq="6.1.5.2", name="Resolve Reconciliation Differences", desc="Identify, investigate and resolve any differences between AR sub-ledger and GL (e.g. timing differences, posting errors, FX adjustments)", r="GFS", a="GFS", sys="ERP / AR Tool"),
                    _s(seq="6.1.5.3", name="Confirm AR Balance for Period Close", desc="Sign off AR balance as reconciled for month-end close. Provide reconciliation pack to central finance", r="GFS", a="GFS", sys="ERP / AR Tool")
                    ]),
            ],
        },
        {
            "id": "6.2",
            "seq": "6.2",
            "name": "Outreach & Escalation",
            "description": "Proactive and structured client outreach for invoices approaching or past due date. Manage escalations to resolve issues and secure payment",
            "step_type": "Process",
            "system_tool": "ERP /  Email",
            "raci": {"r": "GFS", "a": "GFS", "i": "Client Services / Account Managers"},
            "steps": [
                _s(seq="6.2.1", name="Overdue Identification & Prioritisation", desc="Identify overdue receivables based on aging and payment terms. Prioritise accounts for collections outreach based on value, risk and aging", step_type="Automated", r="Automated", a="GFS", sys="ERP / Collections Tool", children=[
                    _s(seq="6.2.1.1", name="Overdue Receivables Identification", desc="Automatically identify invoices exceeding payment terms, and apply aging threshold rules (e.g. 30, 60, 90 days) to categorise severity", step_type="Automated", r="Automated", a="GFS", sys="ERP / Collections Tool"),
                    _s(seq="6.2.1.2", name="Collections Prioritisation", desc="Prioritise overdue accounts for collection effort automatically based on invoice value, client risk profile days overdue and collection history", step_type="Automated", r="Automated", a="GFS", sys="ERP / Collections Tool")
                    ]),
                _s(seq="6.2.2", name="Collections Outreach", desc="Contact clients regarding overdue invoices (e.g., reminders, follow-ups)", r="GFS", a="GFS", sys="ERP / Collections Tool / Email/Phone", children=[
                    _s(seq="6.2.2.1", name="Automated Payment Reminder", desc="Automatically send system-generated payment reminder to client at defined overdue threshold (e.g. 7 days past due).", step_type="Automated", r="Automated", a="GFS", sys="ERP / Collections Tool"),
                    _s(seq="6.2.2.2", name="Follow-Up Contact (Email / Phone)", desc="Conduct follow-up outreach to client AP department via email or phone", sys="Email / Phone"),
                    _s(seq="6.2.2.3", name="Outreach Tracking Update", desc="Record outreach activity and outcome", sys="ERP / Collections Tool")
                    ]),
                _s(seq="6.2.3", name="Dispute Identified?", desc="Determine whether a dispute or billing query has been raised by the client", step_type="Decision", r="GFS", a="GFS", sys="ERP / Collections Tool", outcomes="Yes - proceed to 6.2.4 | No - proceed to 6.2.5", children=[
                    _s(seq="6.2.3.1", name="Dispute Logging", desc="Record dispute details (dispute type, reason, disputed amount, supporting information) and categorisation (e.g., pricing, scope, quality, PO, compliance, etc.)", r="GFS", a="GFS", sys="ERP / Collections Tool"),
                    _s(seq="6.2.3.2", name="Dispute Investigation", desc="Investigate dispute with Client and internal teams (Client Services and Billing teams) as required. Review contract terms, deliverables and billing data.", r="GFS", a="GFS", sys="ERP / Collections Tool"),
                    _s(seq="6.2.3.3", name="Dispute Resolution Processing", desc="If dispute is valid, raise credit note or invoice adjustment. Post to AR and update revenue records accordingly.", r="GFS", a="GFS", sys="ERP / Collections Tool"),
                    _s(seq="6.2.3.4", name="Close Dispute & Update AR", desc="Mark dispute as resolved. Update AR record with resolution outcome. Resume normal collection if balance remains", r="GFS", a="GFS", sys="ERP / Collections Tool")
                    ]),
                _s(seq="6.2.4", name="Dispute Management & Resolution", desc="Investigate and resolve billing disputes", r="GFS", a="GFS", i="Client Services / Account Managers", sys="ERP / Email"),
                _s(seq="6.2.5", name="Escalation Management", desc="Escalate overdue or high-risk receivables internally where required", r="Client Services / Account Managers", a="Client Services / Account Managers", sys="ERP / Collections Tool / Email/Phone", children=[
                    _s(seq="6.2.5.1", name="Escalation Trigger Identification", desc="Identify accounts requiring escalation based on risk or overdue status", r="GFS", a="GFS", sys="ERP / Collections Tool"),
                    _s(seq="6.2.5.2", name="Internal Escalation Initiation", desc="Escalate accounts to internal stakeholders who hold client relationship (e.g., Client Services, Key Account Owner, etc.)", r="GFS", a="GFS", sys="ERP / Collections Tool"),
                    _s(seq="6.2.5.3", name="Escalation Outreach", desc="Execute escalation outreach to client", r="Client Services / Account Managers", a="Client Services / Account Managers", sys="Email / Phone"),
                    _s(seq="6.2.5.4", name="Document Escalation Outcome & Next Steps", desc="Record escalation outcome, agreed next actions and timeline", r="Client Services / Account Managers", a="Client Services / Account Managers", sys="ERP / Collections Tool")
                    ]),
                _s(seq="6.2.6", name="Payment Commitment Tracking", desc="Record and monitor client payment commitments", r="GFS", a="GFS", sys="ERP / Collections Tool", children=[
                    _s(seq="6.2.6.1", name="Payment Commitment Capture", desc="Capture client payment commitments and expected payment dates. Update AR and cash forecast.", r="GFS", a="GFS", sys="ERP / Collections Tool"),
                    _s(seq="6.2.6.2", name="Commitment Monitoring", desc="Monitor adherence to agreed payment commitments. Re-escalate if commitment is missed", r="GFS", a="GFS", sys="ERP / Collections Tool")
                    ]),
                _s(seq="6.2.7", name="Place Account on Credit Hold?", desc="Determine whether to suspend further project delivery or invoicing pending payment", step_type="Decision", r="GFS", a="GFS", i="Client Services / Account Managers", sys="ERP", outcomes="Yes - proceed to 6.2.8 | No - proceed to 6.2.5"),
                _s(seq="6.2.8", name="Implement Credit Hold & Notify Teams", desc="Apply credit hold in ERP. Pause project activations and new order acceptance until resolved. Notify internal stakeholders (Operations, Finance)", r="GFS", a="GFS", i="Client Services / Account Managers", sys="ERP", children=[
                    _s(seq="6.2.8.1", name="Apply Credit Hold", desc="Set credit hold flag on client account in ERP. Block new project activations and invoicing until hold is resolved", r="GFS", a="GFS", sys="ERP"),
                    _s(seq="6.2.8.2", name="Notify Project, Sales & Delivery Teams", desc="Notify internal stakeholders of credit hold status. Communicate implications for active and pipeline work.", r="GFS", a="GFS", i="Client Services / Account Managers", sys="ERP"),
                    _s(seq="6.2.8.3", name="Monitor for Resolution & Remove Hold", desc="Monitor for payment receipt or agreed resolution. Remove credit hold once conditions are met and notify teams", r="GFS", a="GFS", i="Client Services / Account Managers", sys="ERP")
                    ]),
            ],
        },
        {
            "id": "6.3",
            "seq": "6.3",
            "name": "Cash Forecasting",
            "description": "Forecast expected cash collections based on receivables, payment behavior, and client commitments",
            "step_type": "Process",
            "system_tool": "ERP",
            "raci": {"r": "TBD", "a": "TBD", "i": ""},
            "steps": [
                _s(seq="6.3.1", name="Forecast Update", desc="Refresh cash forecast with expected cash inflows based on outstanding receivables, aging and payment terms", r="TBD", a="TBD", sys="ERP", children=[
                    _s(seq="6.3.1.1", name="AR & Cash Data Refresh", desc="Refresh AR balances, payment commitments and collection activity for cash forecasting", r="TBD", a="TBD", sys="ERP"),
                    _s(seq="6.3.1.2", name="Direct Cash Forecast (Weekly)", desc="Generate weekly cash forecast based on AR, AP and known cash movements", r="TBD", a="TBD", sys="ERP / Treasury Tool"),
                    _s(seq="6.3.1.3", name="Indirect Cash Forecast (Quarterly)", desc="Generate cash flow forecast based on revenue forecast and working capital assumptions", r="TBD", a="TBD", sys="EPM")
                    ]),
                _s(seq="6.3.2", name="Variance Analysis vs Prior Forecast", desc="Compare actual cash receipts to prior forecast. Identify and explain material variances", r="TBD", a="TBD", sys="ERP/ EPM", children=[
                    _s(seq="6.3.2.1", name="Actual Cash Receipts Update", desc="Automatically update actual cash receipts in the forecast model for variance analysis", step_type="Automated", r="Automated", a="TBD", sys="ERP/ EPM"),
                    _s(seq="6.3.2.2", name="Direct Forecast Variance Analysis", desc="Compare actual cash receipts to weekly forecast and quantify variances by client, aging bucket and collection status", r="TBD", a="TBD", sys="ERP / Treasury Tool"),
                    _s(seq="6.3.2.3", name="Indirect Forecast Variance Analysis", desc="Compare actual cash receipts to indirect forecast and quantify variances by forecast driver (e.g., revenue timing, DSO assumptions)", r="TBD", a="TBD", sys="EPM"),
                    _s(seq="6.3.2.4", name="Investigate & Explain Material Variances", desc="Identify root cause of significant forecast-to-actual variances. Document explanations for reporting.", r="TBD", a="TBD", sys="ERP/ EPM")
                    ]),
                _s(seq="6.3.3", name="Forecast Reporting", desc="Prepare and present weekly cash forecast pack to central Finance. Include AR aging summary, collection risk flags and updated 13-week forecast", r="TBD", a="TBD", sys="ERP", children=[
                    _s(seq="6.3.3.1", name="Direct Cash Forecast Reporting (Weekly)", desc="Prepare and review weekly cash forecast and actuals by client, aging bucket and collection status", r="TBD", a="TBD", sys="ERP / Treasury Tool"),
                    _s(seq="6.3.3.2", name="Indirect Cash Forecast Reporting (Quarterly)", desc="Prepare cash flow forecast reporting including forecast, actuals and key drivers", r="TBD", a="TBD", sys="EPM"),
                    _s(seq="6.3.3.3", name="Risk & Collections Issue Identification", desc="Report variances and highlight risks and collection issues by client/aging profile and driver/assumption", r="TBD", a="TBD", sys="ERP/ EPM"),
                    _s(seq="6.3.3.4", name="Submit Forecast to Central Finance / Treasury", desc="Submit cash forecast and reporting pack to central finance and treasury per group reporting calendar.", r="TBD", a="TBD", sys="ERP/ EPM")
                    ]),
            ],
        },
    ],
}

PROJECT_CLOSE_AND_REPORTING = {
    "id": "project-close-reporting",
    "l1_seq": "7",
    "l1_name": "Project Close & Reporting",
    "l1_description": "All activities to formally close projects, capture financial and operational outcomes, report performance KPIs to executive leadership, and deliver contractual reporting obligations to clients",
    "l1_color": "#0F766E",
    "raci": {"r": "GFS", "a": "GFS"},
    "system_tool": "ERP / PSA",
    "stages": [
        {
            "id": "7.1",
            "seq": "7.1",
            "name": "Project Close Activities",
            "description": "Formally close the project from financial, contractual, and operational perspectives. Ensure all costs, revenues, and deliverables are reconciled and systems updated to reflect project completion.",
            "step_type": "Process",
            "system_tool": "ERP / PSA",
            "raci": {"r": "GFS", "a": "GFS", "i": "Client Services / Account Managers"},
            "steps": [
                _s(seq="7.1.1", name="Financial Close-Out", desc="Reconcile all project financials, confirm final revenue recognition, release or write off any remaining accruals and deferrals, and confirm the project cost ledger is complete and accurate.", r="GFS", a="GFS", i="Client Services / Account Managers", sys="ERP", children=[
                    _s(seq="7.1.1.1", name="Revenue & Cost Completion Check", desc="Confirm all revenue and costs have been recognised and posted", r="GFS", a="GFS", sys="ERP"),
                    _s(seq="7.1.1.2", name="Billing Completion Check", desc="Confirm all invoices have been issued and processed", r="GFS", a="GFS", sys="ERP"),
                    _s(seq="7.1.1.3", name="Final Revenue & Cost Reconciliation", desc="Reconcile total recognised revenue against total project costs to confirm final margin. Compare actual margin to budget and SOW. Investigate and document any material variance", r="GFS", a="GFS", sys="ERP")
                    ]),
                _s(seq="7.1.2", name="Open Items Resolution", desc="Identify and resolve outstanding items (e.g., unbilled time, unapplied cash, open POs)", r="GFS", a="GFS", sys="ERP", children=[
                    _s(seq="7.1.2.1", name="Unbilled / Unposted Item Identification", desc="Identify outstanding time, expenses or costs", r="GFS", a="GFS", sys="ERP"),
                    _s(seq="7.1.2.2", name="Release / Write-Off Accruals & Deferrals", desc="Review remaining accrued revenue, deferred revenue and cost accruals on the project. Release or reverse balances in ERP as appropriate", r="GFS", a="GFS", sys="ERP"),
                    _s(seq="7.1.2.3", name="Outstanding Balance Resolution", desc="Resolve outstanding balances, adjustments or discrepancies. Obtain approval for any write-offs in line with delegation of authority. Post final journals.", r="GFS", a="GFS", i="Client Services / Account Managers", sys="ERP")
                    ]),
                _s(seq="7.1.3", name="Contract Compliance Review", desc="Verify all contractual obligations have been fulfilled and no outstanding amendments or change orders exist", r="GFS", a="GFS", i="Client Services / Account Managers", children=[
                    _s(seq="7.1.3.1", name="Verify All Contractual Obligations Met", desc="Review contract terms against delivered scope. Confirm all deliverables, SLAs and obligations have been fulfilled", r="GFS", a="GFS", i="Client Services / Account Managers"),
                    _s(seq="7.1.3.2", name="Confirm No Outstanding Amendments or Change Orders", desc="Check for any pending contract amendments, change orders or scope changes that require resolution before close", r="GFS", a="GFS", i="Client Services / Account Managers")
                    ]),
                _s(seq="7.1.4", name="Project Closure Approval", desc="Review and approve project for closure", r="GFS", a="GFS", sys="ERP", children=[
                    _s(seq="7.1.4.1", name="Closure Review", desc="Review project completion status and financials", r="GFS", a="GFS", sys="ERP"),
                    _s(seq="7.1.4.2", name="Closure Approval", desc="Approve project closure", r="Client Services / Account Managers", a="GFS", sys="ERP")
                    ]),
                _s(seq="7.1.5", name="Project Status Update", desc="Update project status to closed in ERP / PSA", r="GFS", a="GFS", sys="ERP", children=[
                    _s(seq="7.1.5.1", name="Project Closure Status Update", desc="Update project status to closed in PSA", r="GFS", a="GFS", sys="PSA"),
                    _s(seq="7.1.5.2", name="Lock Time, Expense & Billing Entry", desc="Prevent further timecard submissions, expense claims and billing events against the closed project.", r="GFS", a="GFS", sys="PSA"),
                    _s(seq="7.1.5.3", name="Financial Closure Status Update", desc="Update financial closure status in ERP", r="GFS", a="GFS", sys="ERP"),
                    _s(seq="7.1.5.4", name="Closure Notification", desc="Notify relevant teams that project closure is complete", r="GFS", a="GFS", sys="ERP"),
                    _s(seq="7.1.5.5", name="Archive Project Documentation", desc="Archive project records, contracts, invoices and supporting documentation per data retention policy.", r="GFS", a="GFS", sys="PSA")
                    ]),
            ],
        },
        {
            "id": "7.2",
            "seq": "7.2",
            "name": "Executive Insights & KPIs",
            "description": "Generate and review project performance metrics and insights for management reporting and decision-making",
            "step_type": "Process",
            "system_tool": "See L4",
            "raci": {"r": "GFS", "a": "GFS", "i": ""},
            "steps": [
                _s(seq="7.2.1", name="Project Financial Summary", desc="Generate project-level financial summary including revenue, cost, margin and utilisation metrics.", r="GFS", a="GFS", sys="ERP / EPM / Forecast/Collections Tool", children=[
                    _s(seq="7.2.1.1", name="Generate Project P&L Report", desc="Produce project profit and loss statement showing revenue, direct costs, indirect costs and margin", r="GFS", a="GFS", sys="ERP"),
                    _s(seq="7.2.1.2", name="Calculate Margin & Utilisation Metrics", desc="Calculate project margin percentage, team utilisation, forecast accuracy and budget variance metrics", r="GFS", a="GFS", sys="ERP")
                    ]),
            ],
        },
        {
            "id": "7.3",
            "seq": "7.3",
            "name": "Client Reporting",
            "description": "Prepare and deliver project reports and financial summaries to clients in line with contractual requirements",
            "step_type": "Process",
            "system_tool": "PSA / ERP",
            "raci": {"r": "GFS", "a": "GFS", "i": ""},
            "steps": [
                _s(seq="7.3.1", name="Client Report Preparation", desc="Prepare project and financial reports for client as per contractual requirements", r="GFS", a="GFS", i="Client Services / Account Managers", sys="PSA / ERP"),
                _s(seq="7.3.2", name="Report Validation & Approval", desc="Validate report accuracy and approve for release", r="GFS", a="GFS", i="Client Services / Account Managers", sys="PSA / ERP"),
                _s(seq="7.3.3", name="Report Distribution", desc="Deliver report to client via agreed distribution channels", r="Client Services / Account Managers", a="GFS", sys="Email / Client Portal"),
            ],
        },
    ],
}


ALL_PROCESSES = [
    ORDER_CAPTURE,
    DEMAND_AND_SUPPLY_PLANNING,
    SERVICE_DELIVERY,
    REVENUE_RECOGNITION,
    INVOICING_AND_BILLING,
    COLLECTIONS,
    PROJECT_CLOSE_AND_REPORTING,
]