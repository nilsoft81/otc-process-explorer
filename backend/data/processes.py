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
    "l1_description": "Establish and govern customer, contractual, commercial and project setup requirements from initial opportunity creation through to project activation, billing readiness and operational delivery enablement",
    "l1_color": "#7C3AED",
    "raci": {"r": "Client Services / Account Managers", "a": "Client Services / Account Managers"},
    "system_tool": "CRM / CLM / PSA / ERP / Contract Capture Agent",
    "stages": [
        {
            "id": "1.1",
            "seq": "1.1",
            "name": "Customer & Contract Setup",
            "description": "Establish the client relationship, execute contractual agreements, define commercial and billing framework terms, and complete operational setup requirements to support downstream delivery, revenue recognition and invoicing",
            "step_type": "Process",
            "system_tool": "CRM",
            "raci": {"r": "Sales", "a": "Sales", "i": ""},
            "steps": [
                _s(seq="1.1.1", name="Customer Initiation", desc="Initiate customer and opportunity setup process from Sales / Business Development pipeline activity and capture preliminary customer and opportunity information", r="Sales", a="Sales", sys="CRM", children=[
                    _s(seq="1.1.1.1", name="Create Prospect & Customer Record in CRM", desc="Create prospect, company and associated contact records in CRM. Capture preliminary customer and opportunity details including client name, region, industry, service line and opportunity scope. Perform duplicate review and link to existing customer records where applicable", r="Sales", a="Sales", sys="CRM"),
                    _s(seq="1.1.1.2", name="Opportunity Creation", desc="Create opportunity record in CRM and capture estimated value, engagement type, expected close date, pipeline stage, opportunity owner and preliminary commercial structure", r="Sales", a="Sales", sys="CRM"),
                    _s(seq="1.1.1.3", name="Quote Generation", desc="Generate preliminary pricing estimate or quote based on expected scope, resource requirements, commercial model and applicable rate structure. Client Services leads quote development using approved commercial guardrails and standard cost rates maintained by Divisional Finance through annual tooling/rate card updates. Quote generation may be performed through PSA, CRM or structured pricing templates, as applicable.", r="Client Services / Account Managers", a="Sales", i="Managing Director (MD) / Division Finance", sys="Structured Excel / PSA / CRM"),
                    _s(seq="1.1.1.4", name="Margin Threshold Approval Required?", desc="Determine whether estimated engagement margin falls below defined approval threshold. Where threshold is breached, obtain approval from Divisional CFO and Pillar President prior to advancing opportunity", r="Client Services / Account Managers", a="Sales", i="Division Finance / Division President", sys="Structured Excel / PSA / CRM"),
                    _s(seq="1.1.1.5", name="Advance Opportunity Through Pipeline Stages", desc="Progress opportunity through defined CRM pipeline stages based on commercial qualification, proposal activity and client engagement status", r="Sales", a="Sales", sys="CRM"),
                    _s(seq="1.1.1.6", name="Existing Customer Record Check", desc="Determine whether customer already exists within ERP / master data systems and identify whether new customer setup or hierarchy updates are required", r="Client Services / Account Managers", a="Client Services / Account Managers", sys="CRM / ERP"),
                    _s(seq="1.1.1.7", name="Customer Master Data Request Initiation", desc="Initiate customer master data setup request for new customers or required hierarchy/billing structure updates and route to Master Data Management team for review and processing", r="Client Services / Account Managers", a="Client Services / Account Managers", sys="CRM / ServiceNow")
                    ]),
                _s(seq="1.1.2", name="Customer Master Data Creation", desc="Create customer master data record including customer hierarchy and required customer attributes to support downstream contracting, billing and reporting processes", r="Global Master Data", a="Global Master Data", sys="ERP / ServiceNow", children=[
                    _s(seq="1.1.2.1", name="Customer Master Data Review", desc="Review customer master data submitted from CRM and identify missing, incomplete or conflicting customer attributes required for record creation. Populate missing fields where possible (e.g., internal segmentation codes)", r="Global Master Data", a="Global Master Data", sys="ServiceNow / ERP"),
                    _s(seq="1.1.2.2", name="Client Services Input Required?", desc="Determine whether Client Services input is required to complete missing customer master data fields", step_type="Decision", r="Global Master Data", a="Global Master Data", sys="ERP", outcomes="Yes - proceed to 1.1.2.3 | No - proceed to 1.1.3"),
                    _s(seq="1.1.2.3", name="Request Additional Customer Information", desc="Request missing or incomplete customer information from Client Services or customer contacts where required for customer master setup", r="Global Master Data", a="Global Master Data", sys="ServiceNow"),
                    _s(seq="1.1.2.4", name="Complete Customer Master Data", desc="Obtain and populate missing customer master data fields required for customer record creation, hierarchy setup and billing enablement", r="Client Services / Account Managers", a="Client Services / Account Managers", i="Sales", sys="ServiceNow / Email"),
                    _s(seq="1.1.2.5", name="Customer Record Creation", desc="Create customer record within ERP/MDM system and establish associated customer hierarchy, billing entity structure and customer identifiers", r="Global Master Data", a="Global Master Data", sys="ERP"),
                    _s(seq="1.1.2.6", name="Customer ID & CRM Update", desc="Update CRM / customer source systems with created customer identifier and customer master record status", step_type="Automated", r="Automated (or Global Master Data in absence of automation)", a="Global Master Data", sys="ERP / CRM")
                    ]),
                _s(seq="1.1.3", name="Credit & Compliance Screening", desc="Perform customer credit assessment, financial due diligence and compliance screening to determine customer risk profile, payment terms, credit controls and onboarding eligibility", r="GFS - Credit", a="GFS - Credit", sys="Credit Platform / ERP", children=[
                    _s(seq="1.1.3.1", name="Compliance Screening", desc="Perform regulatory and policy screening checks including sanctions, AML, watchlists and restricted party validation to confirm the customer relationship is permissible prior to onboarding or credit approval", r="GFS - Credit", a="GFS - Credit", sys="Third party provider assumed"),
                    _s(seq="1.1.3.2", name="Credit Assessment", desc="Assess customer creditworthiness using payment history, trade references, credit bureau data, financial statements and existing exposure to determine customer risk profile and recommended credit treatment", r="GFS - Credit", a="GFS - Credit", sys="Third party provider assumed"),
                    _s(seq="1.1.3.3", name="Risk Scoring", desc="Apply approved scoring models, risk rules and credit policies to generate standardised customer credit risk rating and recommended credit controls", r="GFS - Credit", a="GFS - Credit", sys="Credit platform"),
                    _s(seq="1.1.3.4", name="Credit Decisioning", desc="Determine credit outcome based on risk assessment and policy thresholds (e.g., approve, approve with restrictions, apply credit hold, escalate for review or reject) and define provisional payment terms where applicable", r="GFS - Credit", a="GFS - Credit", sys="Credit platform"),
                    _s(seq="1.1.3.5", name="ERP Credit Master Update", desc="Update ERP customer credit master data including approved credit status, payment terms, risk rating, credit limits and hold indicators", step_type="Automated", r="Automated", a="GFS - Credit", sys="ERP"),
                    _s(seq="1.1.3.6", name="Notify Stakeholders", desc="Notify relevant stakeholders of approved credit status, payment terms, credit restrictions or hold conditions", step_type="Automated", r="Automated", a="GFS - Credit", sys="Credit platform")
                    ]),
                _s(seq="1.1.4", name="Multi-Division Engagement Setup", desc="Determine whether customer engagement requires a multi-division operating model (including CIC-contracted customers) and establish parent division ownership, commercial alignment and billing structure prior to contract execution", r="Client Services / Account Managers", a="Commercial Affairs", sys="CRM", children=[
                    _s(seq="1.1.4.1", name="Multi-Division Engagement Structure Required (including IHL)?", desc="Determine whether multiple divisions are participating in delivery, contracting or billing under a shared client relationship, MSA framework or centralised billing structure", step_type="Decision", r="Client Services / Account Managers", a="Commercial Affairs", sys="N/A", outcomes="Yes - proceed to 1.1.4.2 | No - proceed to 1.1.5"),
                    _s(seq="1.1.4.2", name="Parent Division Assignment", desc="Assign parent division for the engagement / customer account based on agreed ownership criteria. Point of Origination drives parent assignment for new customers. For existing customers, determine parent ownership based on agreed commercial and delivery factors (e.g., revenue share, delivery footprint, key account ownership). Record agreed parent division ownership within CRM / account structure where applicable", r="Client Services / Account Managers", a="Commercial Affairs", sys="CRM"),
                    _s(seq="1.1.4.3", name="Participating Division Identification", desc="Identify divisions participating in delivery, billing or commercial ownership for the engagement", r="Client Services / Account Managers", a="Commercial Affairs", sys="N/A"),
                    _s(seq="1.1.4.4", name="Common Pricing & Commercial Structure Alignment", desc="Define common pricing structures, rate cards and shared commercial terms across participating divisions. Where agreement cannot be reached, parent division retains final commercial decision authority", r="Client Services / Account Managers", a="Commercial Affairs", sys="N/A"),
                    _s(seq="1.1.4.5", name="Division Scope & Billing Allocation", desc="Define division-level delivery scope, billing responsibility and billing-on-behalf structure aligned to parent division requirements", r="Client Services / Account Managers", a="Commercial Affairs", sys="N/A"),
                    _s(seq="1.1.4.6", name="Parent Division Change Control", desc="As required, manage controlled reassignment of parent division ownership based on material changes in revenue share, delivery footprint or strategic account ownership", r="Client Services / Account Managers", a="Commercial Affairs", sys="N/A")
                    ]),
                _s(seq="1.1.5", name="Master Services Agreement (MSA) management", desc="Establish or validate the governing Master Services Agreement (MSA), define high-level commercial and billing framework terms, complete legal execution and capture contractual data required to support downstream project setup, billing and revenue recognition processes", r="Commercial Affairs", a="Commercial Affairs", sys="CLM / Contract Capture Agent", children=[
                    _s(seq="1.1.5.1", name="Existing MSA Check", desc="Determine whether a valid MSA already exists for the customer or parent/affiliate group", step_type="Decision", r="Commercial Affairs", a="Commercial Affairs", sys="CLM", outcomes="Yes - proceed to 1.1.5.9 | No - proceed to 1.1.5.2"),
                    _s(seq="1.1.5.2", name="Select MSA Template", desc="Select appropriate MSA template based on division, service line and legal jurisdiction", r="Commercial Affairs", a="Commercial Affairs", sys="CLM"),
                    _s(seq="1.1.5.3", name="Populate MSA Master Data & Reference ID", desc="Populate customer, legal and billing master data within MSA template. Generate MSA reference identifier within CLM for downstream project setup and invoicing processes. Where applicable, align MSA master data to agreed parent division ownership and billing structure, and capture participating divisions/entities", r="Commercial Affairs", a="Commercial Affairs", i="Client Services / Account Managers", sys="CLM"),
                    _s(seq="1.1.5.4", name="Customer Affiliate Entity Identification", desc="Identify customer affiliate entities, subsidiaries or related billing entities that may engage under the MSA or future SOWs and determine applicability to the contractual and billing structure", r="Commercial Affairs", a="Commercial Affairs", i="Client Services / Account Managers", sys="CLM"),
                    _s(seq="1.1.5.5", name="Country-Specific e-Invoicing Rule Validation", desc="Validate whether local e-invoicing regulations apply based on billing jurisdiction, billing entity and customer requirements. If required, capture e-invoicing identifiers where applicable", r="Commercial Affairs", a="Commercial Affairs", i="Client Services / Account Managers", sys="CLM"),
                    _s(seq="1.1.5.6", name="Populate High-level Commercial Terms", desc="Define high-level contractual and billing framework terms including payment terms, currency, billing frequency, delivery format (e.g., e-invoicing), rate cards (if applicable) and agreed discount / rebate structure. . Where applicable, align commercial terms to agreed parent division structure and permit use of scheduled billing arrangements to support downstream billing operations and invoice automation", r="Commercial Affairs", a="Commercial Affairs", i="Client Services / Account Managers", sys="CLM"),
                    _s(seq="1.1.5.7", name="Legal Review", desc="Use CLM workflow to route draft MSA to Legal for review of draft MSA terms, including non-standard clauses, commercial deviations and customer-specific contractual requirements prior to execution", r="Legal", a="Legal", i="Commercial Affairs / Client Services / Account Managers", sys="CLM"),
                    _s(seq="1.1.5.8", name="Legal Approval?", desc="Determine whether Legal approves the MSA draft for customer execution. If rejected, return with comments", step_type="Decision", r="Legal", a="Legal", sys="CLM", outcomes="Yes - proceed to 1.1.5.9 | No - proceed to 1.1.5.2"),
                    _s(seq="1.1.5.9", name="Draft MSA Upload to Agent", desc="Upload Legal-approved, unsigned MSA document to Contract Capture Agent (via HighQ integration or direct upload) to establish version control prior to execution routing   Key MSA components are extracted (e.g., MSA reference ID) and structured (e.g., key customer, commercial and contractual data) to support project setup. Links to parent MSA, if applicable", r="Commercial Affairs", a="Commercial Affairs", sys="Contract Capture Agent"),
                    _s(seq="1.1.5.10", name="Internal Signature Routing", desc="Where possible be the first to sign within HighQ via DocuSign integration (enables technology selection). Copy relevant stakeholders for automated notification upon executed signature", r="Commercial Affairs", a="Commercial Affairs", i="Client Services / Account Managers", sys="CLM (DocuSign)"),
                    _s(seq="1.1.5.11", name="Send Contract to Client", desc="Transmit internally approved MSA to customer signatories through DocuSign execution workflow", r="Commercial Affairs", a="Commercial Affairs", sys="CLM (DocuSign)"),
                    _s(seq="1.1.5.12", name="Client Reviews & Signs Contract", desc="Client reviews, negotiates (where applicable) and executes e-signature within HighQ (via DocuSign integration). Executed version replaces unsigned draft within CLM. Agent captures executed signature", r="Client (external)", a="Commercial Affairs", sys="CLM (DocuSign)"),
                    _s(seq="1.1.5.13", name="Exception: Customer Signs First?", desc="Determine whether the customer executed the MSA prior to completion of internal signature-first process (at step 1.1.5.10)", step_type="Decision", r="Client (external)", a="Commercial Affairs", sys="CLM (DocuSign)", outcomes="Yes - proceed to 1.1.5.14 | No - proceed to 1.1.5.16"),
                    _s(seq="1.1.5.14", name="Upload Customer-Signed MSA to Agent", desc="Upload customer-signed MSA draft to Contract Capture Agent (via email or direct upload) for review of iteration history and contractual changes prior to internal execution completion. If changes were made to Legal-approved version, route back to Legal for review. Previous MSA versions are appended for version control", r="Commercial Affairs", a="Commercial Affairs", sys="Contract Capture Agent"),
                    _s(seq="1.1.5.15", name="Internal Signature Completion", desc="Route Legal-approved, customer-signed MSA for internal execution completion following Agent review of iteration history and contractual changes", r="Commercial Affairs", a="Commercial Affairs", sys="Contract Capture Agent / CLM (DocuSign)"),
                    _s(seq="1.1.5.16", name="Contract Execution Validation", desc="Confirms counterparty signatures are captured and the contract is legally binding before proceeding. Change document status to \"Executed\"", r="Contract Capture Agent (or Commercial Affairs in absence of Agent)", a="Commercial Affairs", sys="Contract Capture Agent"),
                    _s(seq="1.1.5.17", name="Push Executed MSA to HighQ", desc="Push fully executed MSA and associated execution metadata to HighQ CLM as the contractual system of record", r="Contract Capture Agent (or Commercial Affairs in absence of Agent)", a="Commercial Affairs", sys="Contract Capture Agent / CLM"),
                    _s(seq="1.1.5.18", name="Customer Affiliate Master Data Setup Request", desc="Initiate creation or update of customer master data records for identified client affiliate entities (at step 1.1.5.4) required to support downstream contracting, billing, invoicing and reporting processes", r="Client Services / Account Managers", a="Client Services / Account Managers", sys="ERP"),
                    _s(seq="1.1.5.19", name="Client Vendor Setup Initiation", desc="Prompt customer to onboard the organisation and participating entities as approved vendors within customer procurement, AP or invoicing systems to support downstream invoice submission and prevent billing bottlenecks", r="GFS", a="Client Services / Account Managers", sys="Email"),
                    _s(seq="1.1.5.20", name="Notification to GFS", desc="Automated notification sent to GFS to prompt for client portal setup and e-invoicing configuration, if applicable", r="Contract Capture Agent (or Commercial Affairs in absence of Agent)", a="Commercial Affairs", sys="Contract Capture Agent"),
                    _s(seq="1.1.5.21", name="Set Up Client Portal & E-Invoicing Billing Configuration", desc="Configure client portal access, e-invoicing and customer-specific invoice delivery requirements to support downstream billing process", r="GFS", a="Client Services / Account Managers", sys="ERP")
                    ]),
            ],
        },
        {
            "id": "1.2",
            "seq": "1.2",
            "name": "SOW, Order Entry & Validation (incl. POs)",
            "description": "Execute Statement of Work (SOW) incl. scope, deliverables, and pricing. Set up the contract/order in the ERP system and prepare for project setup",
            "step_type": "Process",
            "system_tool": "CLM",
            "raci": {"r": "Client Services / Account Managers", "a": "Client Services / Account Managers", "i": "Commercial Affairs"},
            "steps": [
                _s(seq="1.2.1", name="SOW initiation / amendment", desc="Receive new project opportunity", r="Client Services / Account Managers", a="Client Services / Account Managers", sys="CLM", children=[
                    _s(seq="1.2.1.1", name="Project Amendment?", desc="Determine whether scope is related to an existing project and requires amendment to the SOW", step_type="Decision", r="Client Services / Account Managers", a="Client Services / Account Managers", i="Commercial Affairs", sys="CLM", outcomes="Yes - proceed to 1.2.2.5 | No - proceed to 1.2.2")
                    ]),
                _s(seq="1.2.2", name="Draft SOW", desc="Develop scope, deliverables and timelines. Define pricing and commercial terms. Align resourcing and effort with delivery. Generate SOW document", r="Client Services / Account Managers", a="Client Services / Account Managers", i="Commercial Affairs", sys="CLM / Contract Capture Agent", children=[
                    _s(seq="1.2.2.1", name="Participating Division Identification", desc="Identify division(s) participating in delivery and billing for the proposed scope of work aligned to the previously agreed parent-child structure, if applicable", r="Client Services / Account Managers", a="Client Services / Account Managers", i="Commercial Affairs", sys="CLM"),
                    _s(seq="1.2.2.2", name="Select SOW Template (CLM)", desc="Select appropriate SOW template based on division, commercial model, project type and customer requirements. Ensure the selected template contains structured contractual, commercial, billing and revenue recognition elements required to support downstream automation", r="Client Services / Account Managers", a="Client Services / Account Managers", i="Commercial Affairs", sys="CLM"),
                    _s(seq="1.2.2.3", name="Populate Contractual Reference Data", desc="Populate contracting entities, participating divisions, customer references and applicable MSA reference information in line with agreed parent division structure. Include MSA reference and generate SOW reference ID", r="Client Services / Account Managers", a="Client Services / Account Managers", i="Commercial Affairs", sys="CLM"),
                    _s(seq="1.2.2.4", name="Customer Affiliate Entity Identification", desc="Identify customer affiliate entities, subsidiaries or related billing entities that may engage under the SOW", r="Client Services / Account Managers", a="Client Services / Account Managers", i="Commercial Affairs", sys="CLM"),
                    _s(seq="1.2.2.5", name="Define Scope & Delivery Approach", desc="Establish deliverables, timeline, milestones, dependencies, etc. Distinguish between agreed vs. optional scope", r="Client Services / Account Managers", a="Client Services / Account Managers", i="Commercial Affairs", sys="CLM"),
                    _s(seq="1.2.2.6", name="Define Commercial & Billing Structure", desc="Define engagement-specific commercial model, rates/fees, billing triggers and upfront payment requirements (if applicable) for the proposed scope of work. For multi-division engagements, establish consolidated billing and align commercial terms to the designated Parent division. Where permitted under agreed MSA terms, use scheduled billing arrangements for T&M and Fixed Fee engagements to simplify downstream billing and invoice generation. Define billable vs. non-billable guidelines", r="Client Services / Account Managers", a="Client Services / Account Managers", i="Commercial Affairs", sys="CLM"),
                    _s(seq="1.2.2.7", name="Define Pass-Through Treatment", desc="Define pass-through treatment based on agreed commercial structure (e.g., percentage markup, fixed fee with or without markup, direct recharge, mgmt. / service fee), and related invoicing requirements (e.g., line item detail)", r="Client Services / Account Managers", a="Client Services / Account Managers", i="Commercial Affairs", sys="CLM"),
                    _s(seq="1.2.2.8", name="Define Resourcing & Effort", desc="Define resourcing and effort requirements to support delivery", r="Client Services / Account Managers", a="Client Services / Account Managers", i="Staffing", sys="CLM"),
                    _s(seq="1.2.2.9", name="Draft SOW Document", desc="Generate draft SOW document using structured contractual, commercial and billing inputs", r="Client Services / Account Managers", a="Client Services / Account Managers", i="Commercial Affairs", sys="CLM"),
                    _s(seq="1.2.2.10", name="Scope Change?", desc="Determine whether there is a scope change after initial SOW draft", step_type="Decision", r="Client Services / Account Managers", a="Client Services / Account Managers", i="Commercial Affairs", sys="CLM", outcomes="Yes - proceed to 1.2.2.11 | No - proceed to 1.2.2.13"),
                    _s(seq="1.2.2.11", name="Redraft SOW Document or Document Changes via Structured Letter", desc="Update draft SOW or document agreed scope, pricing or commercial changes prior to downstream review and approval. Alternatively, capture authorised scope changes in letter or email from client (using structured inputs) with MSA / SOW reference included", r="Client Services / Account Managers", a="Client Services / Account Managers", i="Commercial Affairs", sys="CLM"),
                    _s(seq="1.2.2.12", name="Internal Signature Routing", desc="Where possible be the first to sign within HighQ via DocuSign integration (enables technology selection). Copy relevant stakeholders for automated notification upon executed signature", r="Client Services / Account Managers", a="Client Services / Account Managers", i="Commercial Affairs", sys="CLM (DocuSign)"),
                    _s(seq="1.2.2.13", name="Draft SOW Upload to Agent", desc="Upload draft SOW document (or authorised amendment letter) to Contract Capture Agent via email or direct upload for contractual review, data extraction and version control prior to execution routing  Extract and structure key scope, pricing and billing data from the SOW to support project setup, revenue recognition and invoicing. Flag whether document is New or Amended. Link to parent SOW, if applicable, and governing MSA via MSA reference ID", r="Client Services / Account Managers", a="Client Services / Account Managers", sys="Contract Capture Agent"),
                    _s(seq="1.2.2.14", name="Draft SOW Alignment to MSA?", desc="Review draft SOW against governing MSA to confirm alignment to agreed commercial, billing and contractual terms (e.g., payment terms). Link to governing MSA using reference ID", r="AI Agent - Contract Capture (or Client Services/Acct Mgrs in absence of Agent)", a="Client Services / Account Managers", i="Commercial Affairs", sys="Contract Capture Agent"),
                    _s(seq="1.2.2.15", name="SOW Alignment Discrepancy Resolution", desc="Identify and resolve discrepancies. Update and reupload draft SOW where required", r="Client Services / Account Managers", a="Client Services / Account Managers", i="Commercial Affairs", sys="Contract Capture Agent")
                    ]),
                _s(seq="1.2.3", name="At-Risk Project Activation on Draft SOW", desc="Exception process allowing project activation and commencement of work prior to full SOW execution using approved draft contractual documentation and documented customer authorisation. Apply time-bound controls, risk approvals and escalation requirements until contractual execution is complete. Use 'Proposal' status in PSA to prevent revenue recognition until SOW is executed", r="Client Services / Account Managers", a="Division Finance", sys="Contract Capture Agent / PSA / PowerBI", children=[
                    _s(seq="1.2.3.1", name="At-Risk Start Needed?", desc="Determine whether there is a business need to commence work prior to full SOW execution. Route the at-risk start request for internal approval.", r="Client Services / Account Managers", a="Client Services / Account Managers", sys="Contract Capture Agent"),
                    _s(seq="1.2.3.2", name="At-Risk Approval & Risk Acceptance", desc="Define working-at-risk time bounds and escalation requirements for unresolved client approvals or contract execution delays. Approval confirms acceptance of commercial and contractual risk", r="Division Finance", a="Division Finance", i="Client Services / Account Managers", sys="Contract Capture Agent"),
                    _s(seq="1.2.3.3", name="Proceed to Project Setup", desc="Click 'Submit' to proceed to project setup with unsigned SOW at 1.3.1 using 'Proposal' status in PSA", r="Client Services / Account Managers", a="Client Services / Account Managers", sys="PSA"),
                    _s(seq="1.2.3.4", name="At-Risk Monitoring", desc="Monitor projects operating under at-risk ('Proposal') status and track incurred costs, aging and contractual execution status. If contract execution delay exceeds defined threshold (e.g., 2 weeks without executed SOW), trigger escalation to reassess continuation of work", r="Client Services / Account Managers", a="Division Finance", sys="PowerBI Dashboard")
                    ]),
                _s(seq="1.2.4", name="SOW Review & Execution", desc="Review, negotiate and execute SOW. Capture executed contractual data required to support downstream project setup, billing and revenue recognition processes", r="Client Services / Account Managers", a="Client Services / Account Managers", i="Commercial Affairs", sys="CLM (DocuSign)", children=[
                    _s(seq="1.2.4.1", name="Send SOW to Customer", desc="Transmit final SOW to client signatories via e-signature link within HighQ (via DocuSign integration)", r="Client Services / Account Managers", a="Client Services / Account Managers", i="Commercial Affairs", sys="CLM (DocuSign)"),
                    _s(seq="1.2.4.2", name="Client Amendments", desc="Determine whether customer has proposed amendments, redlines or contractual changes to the SOW requiring internal review or update", r="Client Services / Account Managers", a="Client Services / Account Managers", i="Commercial Affairs", sys="Email / CLM"),
                    _s(seq="1.2.4.3", name="Client Reviews & Signs SOW", desc="Customer reviews, negotiates (where applicable) and executes e-signature within HighQ via DocuSign integration. Executed version replaces unsigned draft within HighQ CLM. Agent captures executed signature", r="Client Services / Account Managers", a="Client Services / Account Managers", i="Commercial Affairs", sys="CLM (DocuSign)"),
                    _s(seq="1.2.4.4", name="Exception: Customer Signs First?", desc="Determine whether customer executed the SOW prior to completion of internal signature-first process (at step 1.2.2.12)", step_type="Decision", r="Client Services / Account Managers", a="Client Services / Account Managers", i="Commercial Affairs", sys="CLM (DocuSign)", outcomes="Yes - proceed to 1.2.4.5 | No - proceed to 1.2.4.7"),
                    _s(seq="1.2.4.5", name="Upload Customer-Signed SOW to Agent", desc="Submit customer-signed SOW draft to Contract Capture Agent (via email or direct upload) for review of iteration history and contractual changes prior to internal execution completion. If changes were made to internal-approved version, route back to approver for review. Previous SOW versions are appended for version control", r="Client Services / Account Managers", a="Client Services / Account Managers", i="Commercial Affairs", sys="Contract Capture Agent"),
                    _s(seq="1.2.4.6", name="Internal Signature Completion", desc="Route customer-signed SOW for internal execution completion following Agent review of iteration history and contractual changes", r="Client Services / Account Managers", a="Client Services / Account Managers", i="Commercial Affairs", sys="Contract Capture Agent / CLM (DocuSign)"),
                    _s(seq="1.2.4.7", name="Contract Execution Validation", desc="Confirm that all counterparty signatures are captured and the contract is legally binding before proceeding. Change document status to \"Executed\"", r="AI Agent - Contract Capture (or Client Services/Acct Mgrs in absence of Agent)", a="Division Finance", i="Commercial Affairs", sys="Contract Capture Agent"),
                    _s(seq="1.2.4.8", name="SOW Alignment to MSA?", desc="Re-review executed SOW against governing MSA to confirm alignment to agreed commercial, billing and contractual terms (e.g., payment terms). Link to governing MSA using reference ID", step_type="Decision", r="AI Agent - Contract Capture (or Client Services/Acct Mgrs in absence of Agent)", a="Client Services / Account Managers", i="Commercial Affairs", sys="Contract Capture Agent", outcomes="Yes - proceed to 1.2.4.10 | No - proceed to 1.2.4.9"),
                    _s(seq="1.2.4.9", name="SOW Alignment Discrepancy Resolution", desc="Identify and resolve discrepancies. Where discrepancies relate to participating child divisions, the parent division lead may delegate resolution activities to the applicable child division while retaining overall accountability for alignment and resolution completion  Update SOW document (and route for re-approval) where required", r="Client Services / Account Managers", a="Client Services / Account Managers", i="Commercial Affairs", sys="Contract Capture Agent"),
                    _s(seq="1.2.4.10", name="Finance Approval Threshold Met?", desc="Determine whether executed SOW value exceeds defined approval threshold requiring Finance review prior to project activation", step_type="Decision", r="AI Agent - Contract Capture (or Client Services/Acct Mgrs in absence of Agent)", a="Client Services / Account Managers", i="Commercial Affairs", sys="Contract Capture Agent", outcomes="Yes - proceed to 1.2.4.11 | No - proceed to 1.2.4.12"),
                    _s(seq="1.2.4.11", name="Finance Review & Approval", desc="Route executed SOW to Finance for review and approval where approval threshold is exceeded. Trigger automated notification to Finance and capture approval outcome prior to project activation", r="Division Finance", a="Division Finance", i="Client Services / Account Managers", sys="Contract Capture Agent"),
                    _s(seq="1.2.4.12", name="Project Activation Trigger in PSA", desc="Push approved and executed SOW to PSA and activate project with “Active” status (or update existing project if this is an amendment to an existing project scope). See step 1.3 for project activation steps", r="AI Agent - Contract Capture (or Client Services/Acct Mgrs in absence of Agent)", a="Client Services / Account Managers", sys="PSA"),
                    _s(seq="1.2.4.13", name="Push Executed SOW to HighQ", desc="Push fully executed SOW and associated execution metadata to HighQ CLM as the contractual system of record. Maintain linkage to governing MSA and executed contractual records", r="AI Agent - Contract Capture (or Client Services/Acct Mgrs in absence of Agent)", a="Client Services / Account Managers", sys="Contract Capture Agent"),
                    _s(seq="1.2.4.14", name="Customer Affiliate Master Data Setup Request", desc="Initiate creation or update of customer master data records for identified client affiliate entities (at step 1.2.2.1) required to support downstream contracting, billing, invoicing and reporting processes", r="Client Services / Account Managers", a="Client Services / Account Managers", sys="ERP"),
                    _s(seq="1.2.4.15", name="Client Vendor Setup Initiation", desc="Prompt customer to onboard the organisation and participating entities as approved vendors within customer procurement, AP or invoicing systems to support downstream invoice submission and prevent billing bottlenecks", r="Client Services / Account Managers", a="Client Services / Account Managers", sys="Email"),
                    _s(seq="1.2.4.16", name="Upfront Billing Required?", desc="Determine whether upfront payment or pre-billing is required based on executed SOW terms. Flag in Billing Agent", step_type="Decision", r="GFS", a="Client Services / Account Managers", sys="Contract Capture Agent", outcomes="Yes - proceed to 1.3.7 | No - proceed to 1.2.5")
                    ]),
                _s(seq="1.2.5", name="PO Intake, Validation & Routing", desc="Receive customer purchase order (PO), validate PO details against governing SOW and MSA terms where applicable, and route for downstream validation, linkage and operational setup", r="AI Agent - Contract Capture (or Client Services/Acct Mgrs in absence of Agent)", a="Client Services / Account Managers", sys="Email / Portal / Contract Capture Agent", children=[
                    _s(seq="1.2.5.1", name="PO Received?", desc="Determine whether PO has been received via agreed channel(s) (e.g., email, portal, EDI)", step_type="Decision", r="Client Services / Account Managers", a="Client Services / Account Managers", sys="Email / Portal / EDI", outcomes="Yes - proceed to 1.2.5.2 | No - proceed to 1.2.6"),
                    _s(seq="1.2.5.2", name="PO Upload to Agent", desc="Upload PO to Contract Capture Agent via email or direct upload for review, data extraction and downstream operational processing  Extract and structure key purchase order data including PO number, billing entity, value, dates and associated contractual references to support downstream contract setup, billing and invoicing processes. Link PO to governing SOW, MSA and related contractual records where applicable", r="Client Services / Account Managers", a="Client Services / Account Managers", sys="Contract Capture Agent"),
                    _s(seq="1.2.5.3", name="PO Allocation & Group PO Identification", desc="Determine whether PO applies to a single project, multiple projects or grouped billing structure. Define PO allocation and linkage approach across associated projects, SOWs or billing entities where applicable", r="AI Agent - Contract Capture (or Client Services/Acct Mgrs in absence of Agent)", a="Client Services / Account Managers", sys="Contract Capture Agent"),
                    _s(seq="1.2.5.4", name="PO Alignment to SOW?", desc="Determine whether PO(s) aligns to governing SOW and applicable MSA terms, including billing entity, scope, value, billing structure, payment terms and deliverables", step_type="Decision", r="AI Agent - Contract Capture (or GFS in absence of Agent)", a="Client Services / Account Managers", sys="Contract Capture Agent", outcomes="Yes - proceed to 1.2.6 | No - proceed to 1.2.5.5"),
                    _s(seq="1.2.5.5", name="PO Alignment Discrepancy Resolution", desc="Identify and resolve discrepancies (e.g., incorrect billing entity). Request PO corrections where required and upload for re-validation against governing contractual documents", r="GFS", a="Client Services / Account Managers", i="Client Services / Account Managers", sys="Contract Capture Agent"),
                    _s(seq="1.2.5.6", name="Push PO to PSA", desc="Push validated PO data and associated contractual references to PSA and associate PO records to the applicable project, SOW and customer records to support project-level audit trail and contractual traceability", r="AI Agent - Contract Capture (or Client Services/Acct Mgrs in absence of Agent)", a="Client Services / Account Managers", sys="Contract Capture Agent"),
                    _s(seq="1.2.5.7", name="Customer Affiliate Master Data Setup Request", desc="Initiate creation or update of customer master data records for affiliate entities identified through the MSA, SOW or PO process that are not yet established within customer master data and are required to support downstream contracting, billing, invoicing and reporting processes", r="Client Services / Account Managers", a="Client Services / Account Managers", sys="ERP")
                    ]),
                _s(seq="1.2.6", name="Contract Setup / Order entry", desc="Push structured contractual, commercial and PO data from Contract Capture Agent into ERP to create and configure contract/order records supporting downstream billing, project setup and revenue recognition processes", r="AI Agent - Contract Capture (or GFS in absence of Agent)", a="GFS", sys="ERP / PSA", children=[
                    _s(seq="1.2.6.1", name="Contract / Order Record Creation", desc="Push structured contractual data from Contract Capture Agent into ERP to create contract/order record linked to customer, value (as per SOW) and other governing MSA / SOW references", r="AI Agent - Contract Capture (or GFS in absence of Agent)", a="GFS", sys="ERP"),
                    _s(seq="1.2.6.2", name="Commercial Data Entry", desc="Push pricing structure, billing arrangements, payment terms and key commercial attributes from Contract Capture Agent into ERP based on executed SOW and governing MSA terms", r="AI Agent - Contract Capture (or GFS in absence of Agent)", a="GFS", sys="ERP"),
                    _s(seq="1.2.6.3", name="PO Association & Billing Reference Setup", desc="Push validated PO references, billing entities and grouped PO allocation structure from Contract Capture Agent into ERP contract/order records where applicable", r="AI Agent - Contract Capture (or GFS in absence of Agent)", a="GFS", sys="ERP"),
                    _s(seq="1.2.6.4", name="Billing Configuration", desc="Push billing schedules, billing triggers and invoicing parameters from Contract Capture Agent into ERP and Billing Agent aligned to contractual billing requirements", r="AI Agent - Contract Capture (or GFS in absence of Agent)", a="GFS", sys="ERP"),
                    _s(seq="1.2.6.5", name="Revenue Recognition Setup", desc="Create and structure the project in PSA aligned to the executed SOW (and PO, if applicable). Establish project structure, working budgets, resource alignment and billing readiness to support downstream delivery, billing and revenue recognition processes", r="AI Agent - Contract Capture (or GFS in absence of Agent)", a="GFS", sys="PSA / ERP")
                    ]),
            ],
        },
        {
            "id": "1.3",
            "seq": "1.3",
            "name": "Project Activation & Budgeting",
            "description": "Create and structure the project in the PSA aligned to the executed SOW (and PO, if applicable). Establish budgets, resourcing effort and configure time, expense and billing readiness. Activate the project to enable delivery, tracking and invoicing",
            "step_type": "Process",
            "system_tool": "PSA / Concur / Contract Capture Agent",
            "raci": {"r": "Client Services / Account Managers", "a": "Client Services / Account Managers", "i": ""},
            "steps": [
                _s(seq="1.3.1", name="Project initiation", desc="Push structured contractual, commercial, billing and project setup data from Contract Capture Agent into PSA to initiate project setup workflow. PSA generates Project Identifier and establishes initial project record and ownership. For at-risk assignments, link back to Draft SOW and set project status to \"Proposal\" (Evoke) / (Ignite TBC)", r="Client Services / Account Managers", a="Client Services / Account Managers", sys="PSA"),
                _s(seq="1.3.2", name="Project Structure Setup", desc="Create project structure within PSA linked to governing SOW, PO and customer records. Define parent-child project hierarchy, project phases, work packages, activities, milestones and delivery timelines aligned to contractual scope", r="Client Services / Account Managers", a="Client Services / Account Managers", sys="PSA"),
                _s(seq="1.3.3", name="Working Budget & Resourcing Setup", desc="Configure project working budget, revenue baseline, planned costs, margin assumptions and planned delivery model assumptions within PSA based on executed contractual terms, operational delivery assumptions and approved commercial guardrails and standard cost rates/rate cards maintained by Division Finance. Working budget may differ from contractual SOW estimates where operational delivery requirements differ  Establish operational budget baseline used for forecasting, percentage-of-completion calculations and revenue recognition processes", r="Client Services / Account Managers", a="Client Services / Account Managers", i="Division Finance", sys="PSA"),
                _s(seq="1.3.4", name="Resource Role Mapping & Staffing Alignment", desc="Align contractual SOW resource roles and rate assumptions to standardised PSA role structures and associated rate hierarchies integrated from Workday, which serves as the system of record for employee and organisational hierarchy data. Where differences exist between contractual role descriptions and operational role structures, PSA/Workday classifications govern project configuration, budgeting and downstream financial reporting  Initiate coordination with resource management for staffing requirements", r="Client Services / Account Managers", a="Client Services / Account Managers", i="Project Manager", sys="PSA"),
                _s(seq="1.3.5", name="Project Margin Threshold Met?", desc="Determine whether project margin based on configured working budget and operational delivery assumptions falls below defined approval threshold. Where threshold is breached, obtain approval from Divisional CFO and Pillar President prior to project activation", r="Client Services / Account Managers", a="Client Services / Account Managers", i="Division Finance / Division President", sys="PSA"),
                _s(seq="1.3.6", name="Time & Expense Enablement", desc="Enable time and expense entry against project within PSA and associated expense systems. Configure expense policies, billable/non-billable rules and project code synchronisation with expense platforms (e.g., Concur)", r="Client Services / Account Managers", a="Client Services / Account Managers", sys="PSA / Concur"),
                _s(seq="1.3.7", name="Milestone & Billing Trigger Setup", desc="Configure project milestones (including sub-project or work package level milestones where applicable), billing schedules and billing trigger conditions aligned to contractual delivery and invoicing requirements  Where upfront billing applies, configure \"SOW Executed\" milestone and mark as complete on SOW signature date to initiate billing trigger", r="Client Services / Account Managers", a="Client Services / Account Managers", sys="PSA"),
                _s(seq="1.3.8", name="Billing & Revenue Enablement", desc="Configure billing controls, invoicing readiness and revenue recognition alignment within PSA and Billing Agent based on contractual billing and revenue treatment requirements. Ensure billing schedules, billing triggers and revenue recognition methods are aligned to executed SOW terms  Revenue recognition remains disabled until project status is updated to “Active” within PSA", r="Client Services / Account Managers", a="Client Services / Account Managers", sys="PSA"),
                _s(seq="1.3.9", name="Project Governance & Controls Setup", desc="Configure project governance, reporting cadence, approval controls and change management requirements within PSA. Define approval workflows for time, expenses, billing and project changes aligned to contractual and operational governance requirements", r="Client Services / Account Managers", a="Client Services / Account Managers", sys="PSA"),
                _s(seq="1.3.10", name="Document Repository Linkage", desc="Automatically generate and maintain linkage between PSA project record and executed contractual documents maintained within HighQ CLM contractual repository. Contract Capture Agent populates contractual reference links within PSA for downstream operational access and audit purposes", r="Contract Capture Agent (or Client Services / Account Managers in absence of Agent)", a="Client Services / Account Managers", sys="Contract Capture Agent / PSA"),
                _s(seq="1.3.11", name="Project Activation (Go-Live)", desc="Validate all required project setup components are complete, including completion of required Finance threshold approvals where applicable, and activate project within PSA for operational delivery, time entry, expense entry, billing and downstream revenue recognition processing. Notify relevant stakeholders of project activation status", r="Client Services / Account Managers", a="Client Services / Account Managers", i="Division Finance", sys="PSA"),
            ],
        },
    ],
}

DEMAND_AND_SUPPLY_PLANNING = {
    "id": "demand-supply-planning",
    "l1_seq": "2",
    "l1_name": "Demand & Supply Planning",
    "l1_description": "Develop, review and maintain weighted revenue forecasts, workforce demand signals and operational delivery assumptions to support capacity planning, staffing decisions, utilisation management and delivery planning across pipeline, active projects and committed engagements",
    "l1_color": "#0E7490",
    "raci": {"r": "Staffing", "a": "Division Finance"},
    "system_tool": "EPM / Fabric / CRM / PSA",
    "stages": [
        {
            "id": "2.1",
            "seq": "2.1",
            "name": "Revenue Forecasting",
            "description": "Develop, review and maintain weighted revenue forecasts using pipeline, contractual, project delivery and operational financial data to forward-looking revenue planning and workforce demand forecasting",
            "step_type": "Process",
            "system_tool": "EPM / Fabric",
            "raci": {"r": "Division Finance", "a": "Division Finance", "i": ""},
            "steps": [
                _s(seq="2.1.1", name="Forecast Submission Calendar", desc="Define forecast calendar, submission deadlines, review cadence and governance requirements for the revenue forecasting cycle", r="Division Finance", a="Division Finance", sys="EPM", children=[
                    _s(seq="2.1.1.1", name="Forecast Calendar & Cut-Off Definition", desc="Define forecast submission calendar, review cadence, forecast cut-off dates and approval timelines for the financial forecasting cycle", r="Division Finance", a="Division Finance", sys="EPM"),
                    _s(seq="2.1.1.2", name="Forecast Timeline Communication", desc="Communicate forecast calendar, submission deadlines and cut-off dates to relevant stakeholders. Trigger automated reminders to communicate ahead of key forecast submission and review deadlines", r="Division Finance", a="Division Finance", sys="EPM / Email")
                    ]),
                _s(seq="2.1.2", name="Pipeline Review & Demand Signal Capture", desc="Capture, review and update weighted opportunity pipeline data from CRM to support divisional revenue forecasting, including new business opportunities, renewals and awarded-but-not-yet-started engagements", r="Client Services / Account Managers", a="Portfolio Leaders (MD)", i="Sales / Division Finance", sys="CRM / EPM", children=[
                    _s(seq="2.1.2.1", name="Pipeline Data Review & Update", desc="Review and update opportunity pipeline data within CRM including deal stage, probability, expected value and forecast timing to reflect latest customer engagement status and commercial outlook", r="Client Services / Account Managers", a="Portfolio Leaders (MD)", sys="CRM"),
                    _s(seq="2.1.2.2", name="Opportunity Qualification for Forecast", desc="Determine whether opportunities qualify for inclusion in weighted forecast categories based on agreed forecast governance rules including deal stage, probability and expected close timing. Apply forecast weighting based on approved deal stage classification", r="Client Services / Account Managers", a="Portfolio Leaders (MD)", sys="CRM"),
                    _s(seq="2.1.2.3", name="Forecast Workflow Submission", desc="Submit updated weighted pipeline and committed forecast inputs for divisional forecast consolidation and review in accordance with forecast submission timelines and governance requirements", r="Client Services / Account Managers", a="Portfolio Leaders (MD)", sys="EPM & Fabric")
                    ]),
                _s(seq="2.1.3", name="Existing Work - Forecast", desc="Review and update forecasts for active and work-at-risk projects based on delivery progress, approved scope changes, operational delivery assumptions and latest project status", r="Project Manager", a="Project Manager", i="Client Services / Account Managers", sys="PSA (Forecasting Module) / EPM", children=[
                    _s(seq="2.1.3.1", name="Active Projects Review & Update", desc="Review and update active project forecast data within PSA forecasting modules including delivery timing, staffing assumptions, revenue forecasts, approved scope changes and working budget assumptions to reflect latest project status and operational outlook", r="Project Manager", a="Project Manager", i="Client Services / Account Managers", sys="PSA (Forecasting Module)"),
                    _s(seq="2.1.3.2", name="Work-at-Risk Forecast Alignment", desc="Review approved work-at-risk engagements operating within PSA prior to inclusion in active project forecast. Validate forecast assumptions, delivery timing, staffing assumptions, working budget assumptions, contractual status and expected execution timing to support forecast accuracy and operational planning", r="Project Manager", a="Project Manager", i="Client Services / Account Managers", sys="PSA (Forecasting Module)"),
                    _s(seq="2.1.3.3", name="Pass-Through Forecast Update", desc="Update forecasted pass-through revenue and associated costs within active project forecasts. Ensure all known pass-through fees treated as revenue are forecast in the appropriate period to support forecast accuracy and minimise variance between forecast and actual revenue", r="Project Manager", a="Project Manager", i="Client Services / Account Managers", sys="PSA (Forecasting Module)"),
                    _s(seq="2.1.3.4", name="Forecast Workflow Submission", desc="Submit updated existing work forecast inputs for divisional forecast consolidation and review in accordance with forecast submission timelines and governance requirements", r="Project Manager", a="Project Manager", sys="EPM / Fabric")
                    ]),
                _s(seq="2.1.4", name="Divisional Revenue Forecasting", desc="Develop and refine divisional revenue forecast using weighted pipeline forecasts from CRM and active project forecasts from PSA within EPM. Align forecast inputs relating to delivery timing, probability, staffing, pass-through revenue and forecast inclusion rules", r="Division Finance", a="Division Finance", i="Commercial Finance", sys="EPM / Fabric", children=[
                    _s(seq="2.1.4.1", name="Divisional Forecast Generation", desc="Generate divisional revenue forecast within EPM using weighted pipeline forecasts from CRM and active project forecasts from PSA by agency, client, service line, geography and forecast period. Include renewals, approved scope changes, qualified work-at-risk engagements, pass-through revenue and other approved forecast adjustments where applicable", r="Division Finance", a="Division Finance", i="Commercial Finance", sys="EPM / Fabric"),
                    _s(seq="2.1.4.2", name="Account Discount & Rebate Forecast Assessment", desc="Review forecasted discounts, rebates and threshold-based commercial arrangements within divisional forecast assumptions. Where parent-child structures exist for multi-division engagements, assess forecasted revenue across participating divisions to determine rebate or discount qualification thresholds and associated allocation impacts", r="Division Finance", a="Division Finance", i="Sales / Project Manager / Commercial Finance", sys="EPM / Fabric"),
                    _s(seq="2.1.4.3", name="Bottom-Up Forecast Review & Update", desc="Review bottom-up divisional forecast submission prior to forecast cut-off. Submit any approved forecast adjustments and updates into EPM for divisional forecast review prior to cut-off", r="Portfolio Leaders (MD)", a="Portfolio Leaders (MD)", i="Client Services / Account Managers / Project Manager", sys="EPM / Fabric")
                    ]),
                _s(seq="2.1.5", name="Finance Forecast Review & Top-Down Adjustments", desc="Review bottom-up forecast submissions after cut-off and apply Finance-led review, challenge and top-down adjustments prior to forecast commitment and publication", r="Division Finance", a="Division Finance", sys="EPM / Fabric", children=[
                    _s(seq="2.1.5.1", name="Historical Performance, Trend & Seasonality Review", desc="Review historical revenue, utilisation, delivery performance, revenue trends and seasonal demand patterns across agency, service line, engagement type and geography to support baseline forecasting and identification of forecast variances", r="Division Finance", a="Division Finance", sys="EPM / Fabric"),
                    _s(seq="2.1.5.2", name="Top-Down Forecast Adjustment Input", desc="Apply Finance-led top-down forecast adjustments and baseline demand assumptions including utilisation targets, demand uplift assumptions and identified forecast gaps where applicable", r="Division Finance", a="Division Finance", sys="EPM / Fabric"),
                    _s(seq="2.1.5.3", name="Forecast Review & Challenge", desc="Review divisional forecast outputs, pipeline weighting, delivery timing, staffing assumptions and forecast variances against historical performance and Finance expectations. Challenge forecast submissions and identify required adjustments prior to forecast commitment", r="Division Finance", a="Division Finance", i="Portfolio Leaders (MD)", sys="EPM / Fabric")
                    ]),
                _s(seq="2.1.6", name="Forecast Commitment & Finalisation", desc="Review Finance-adjusted divisional forecast, obtain leadership commitment and finalise forecast publication for downstream planning, workforce management and business performance reporting", r="Division Finance", a="Division Finance", i="Portfolio Leaders (MD)", sys="EPM / Fabric", children=[
                    _s(seq="2.1.6.1", name="Commitment Call", desc="Conduct divisional forecast commitment review led by Division Finance. Review Finance-adjusted forecast outputs, discuss required adjustments and obtain Managing Director commitment prior to forecast finalisation and publication. Commitment call should occur c.4 working days post-submission cutoff", r="Division Finance", a="Division Finance", i="Portfolio Leaders (MD)", sys="EPM / Fabric"),
                    _s(seq="2.1.6.2", name="MD Forecast Commitment Received?", desc="Determine whether MDs commit to the Finance-adjusted divisional forecast and associated forecast assumptions", step_type="Decision", r="Division Finance", a="Division Finance", i="Portfolio Leaders (MD)", sys="EPM / Fabric", outcomes="Yes - proceed to 2.1.6.3 | No - proceed to 2.1.4.3"),
                    _s(seq="2.1.6.3", name="Forecast Finalisation & Publication", desc="Finalise approved divisional forecast version within EPM and publish forecast outputs for downstream demand planning, workforce planning and business reporting purposes", r="Division Finance", a="Division Finance", sys="EPM / Fabric")
                    ]),
            ],
        },
        {
            "id": "2.2",
            "seq": "2.2",
            "name": "Demand Planning & Workforce Optimisation",
            "description": "Assess forecasted demand against available workforce capacity and utilisation levels to identify staffing requirements, optimise resource allocation and support delivery readiness across pipeline, active projects and committed engagements",
            "step_type": "Process",
            "system_tool": "PSA / Resource Management Tool / HRIS",
            "raci": {"r": "Staffing", "a": "Staffing", "i": "Project Manager / Division Finance"},
            "steps": [
                _s(seq="2.2.1", name="Demand Signal Identification", desc="Translate forecasted pipeline, active project demand and approved scope changes into resource demand signals for roles, skills, geography and delivery periods. Ensure project and scope updates within PSA are reflected in workforce planning inputs", r="Staffing", a="Staffing", i="Project Manager / Division Finance", sys="PSA"),
                _s(seq="2.2.2", name="Capacity Assessment", desc="Assess current workforce capacity, availability, utilisation levels and planned resource commitments to establish available delivery capacity baseline across roles, skills and geographies", r="Staffing", a="Staffing", sys="PSA / Resource Management Tool / HRIS"),
                _s(seq="2.2.3", name="Gap Analysis", desc="Compare forecasted demand against available workforce capacity to identify delivery shortfalls, surplus capacity and staffing gaps by role, skill, geography and forecast period", r="Staffing", a="Staffing", sys="PSA / Resource Management Tool / HRIS"),
                _s(seq="2.2.4", name="Hiring & Subcontractor Planning (Buy/Borrow/Build)", desc="Develop workforce actions to address identified staffing gaps including hiring, redeployment, subcontractor utilisation and resource reallocation. Optimise resource mix to support forecasted delivery requirements and utilisation targets", r="Staffing", a="Staffing", sys="PSA / Resource Management Tool / HRIS"),
            ],
        },
        {
            "id": "2.3",
            "seq": "2.3",
            "name": "Staffing and Assignments",
            "description": "Match available and planned resources to forecasted delivery demand and confirm resource assignments to support project delivery, utilisation targets and workforce planning requirements",
            "step_type": "Process",
            "system_tool": "PSA / Resource Management Tool / HRIS / PowerBI",
            "raci": {"r": "Staffing", "a": "Staffing", "i": "Project Manager"},
            "steps": [
                _s(seq="2.3.1", name="Resource Matching & Assignment Proposals", desc="Match available resources to forecasted project and delivery requirements based on skills, availability, geography, utilisation targets and cost considerations. Ensure approved scope changes and updated project demand signals within PSA are reflected in proposed resource assignments", r="Staffing", a="Staffing", i="Project Manager", sys="PSA / Resource Management Tool / HRIS"),
                _s(seq="2.3.2", name="Conflict Resolution & Prioritisation", desc="Review and resolve resource allocation conflicts across competing projects, delivery priorities and staffing demands. Prioritise assignments based on strategic importance, contractual commitments, delivery risk and margin impact", r="Staffing", a="Staffing", i="Project Manager", sys="PSA / Resource Management Tool / HRIS"),
                _s(seq="2.3.3", name="Resource Commitment Confirmation", desc="Confirm resource assignments and delivery commitments with project managers and capability leads. Update PSA with approved resource allocations and assignment changes", r="Staffing", a="Staffing", i="Project Manager", sys="PSA / Resource Management Tool / HRIS"),
                _s(seq="2.3.4", name="Supply-Demand Reporting", desc="Generate and distribute supply-demand reporting and workforce utilisation insights to leadership teams. Highlight capacity constraints, delivery risks, utilisation trends and mitigation actions", r="Staffing", a="Staffing", sys="PSA / Resource Management Tool / HRIS / PowerBI"),
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
                _s(seq="4.1.1", name="Revenue Recognition Trigger Initiation", desc="Trigger revenue recognition cycle (e.g., period-end). Validate alignment with SOW / MSA terms and revenue recognition rules", r="GFS", a="GFS", sys="Contract Capture Agent / PSA", children=[
                    _s(seq="4.1.1.1", name="Initiate Period-End Revenue Cycle", desc="Trigger month-end revenue recognition process based on financial close calendar and projects moving to 'Active' status. Confirm cut-off dates and deadlines", step_type="Automated", r="Automated (or GFS in absence of Automation)", a="GFS", sys="Contract Capture Agent / PSA / ERP"),
                    _s(seq="4.1.1.2", name="Contract & Revenue Rule Validation", desc="Automatically validate alignment with MSA / signed SOW and revenue recognition rules. Projects must be Active in PSA (e.g., signed SOW) to enable revenue recognition", step_type="Automated", r="Automated (or GFS in absence of Automation)", a="GFS", sys="Contract Capture Agent / PSA"),
                    _s(seq="4.1.1.3", name="Identify Revenue Recognition Method by Project", desc="Where operationally feasible, perform revenue recognition at the primary project level rather than sub-project level to support consolidated revenue treatment and simplify downstream accounting processes.  Determine applicable revenue recognition method per project (or sub-project where required): T&M (time-earned), Fixed Fee (PoC), Milestone (delivery event), SaaS (recurring), Pre-billing (deposit at contract signature), Passthrough (third party, intercompany), etc.   Known exception: Exception: Evoke performing at the sub project level", step_type="Automated", r="Automated (or GFS in absence of Automation)", a="GFS", sys="Contract Capture Agent / PSA"),
                    _s(seq="4.1.1.4", name="Revenue Treatment Routing", desc="Route transactions to appropriate revenue calculation logic based on method", step_type="Automated", r="Automated (or GFS in absence of Automation)", a="GFS", sys="Contract Capture Agent / PSA")
                    ]),
                _s(seq="4.1.2", name="Revenue Readiness Validation", desc="Confirm required inputs are complete (e.g., approved timesheets, cross-check fixed fee to POC, etc.)", step_type="Automated", r="Automated (or GFS in absence of Automation)", a="GFS", sys="PSA / Contract Capture Agent", children=[
                    _s(seq="4.1.2.1", name="Revenue Treatment Routing", desc="Route transactions to appropriate revenue validation logic based on method", step_type="Automated", r="Automated (or GFS in absence of Automation)", a="GFS", sys="PSA"),
                    _s(seq="4.1.2.2", name="T&M: Validate Approved Timecards & Rates", desc="For T&M projects, confirm all timecards for the period are submitted. Reconcile billable hours.", step_type="Automated", r="Automated (or GFS in absence of Automation)", a="GFS", i="Project Manager", sys="PSA"),
                    _s(seq="4.1.2.3", name="Fixed Fee / Milestone: Validate Approved Timecards & Rates; Reconcile Against PoC (or Validate Milestone Completion)", desc="For Fixed Fee / Milestone projects, confirm all timecards for the period are submitted. Automatically reconcile billable hours (timecard-driven) against working budget (at project setup) to derive percentage of completion (PoC). Calculate PoC at the parent project level wherever operationally feasible rather than at sub-project level. GFS to share PoCs with PMs for review.  Milestone - by exception only: Where PoC is not applicable, validate milestone completion and client acceptance status for revenue recognition processing. Proceed to to 4.1.2.5  Known exception: Evoke recognising based on milestone completion", r="GFS", a="GFS", i="Project Manager", sys="PSA"),
                    _s(seq="4.1.2.4", name="Fixed Fee / Milestone: PoC Review", desc="Review system-generated PoC. If current understanding of PoC does not agree with calculation, update working budget within PSA to inform revised PoC calculation  Milestone - by exception only: Where PoC is not applicable, skip this step and proceed to 4.1.2.5", r="Project Manager", a="Project Manager", sys="PSA"),
                    _s(seq="4.1.2.5", name="SaaS: Active Subscription Review", desc="For SaaS and recurring revenue projects, validate active subscription term, contracted recurring revenue, billing schedule and revenue recognition period", r="GFS", a="GFS", i="Client Services / Account Managers", sys="CLM (for active contract)"),
                    _s(seq="4.1.2.6", name="Validate Passthrough Revenue Treatment (Markup, No Markup, Mgmt. / Service Fee)", desc="Validate passthrough revenue treatment is aligned to agreed SOW terms (e.g., markup, management/service fee or without markup arrangements) and supported by underlying service delivery for gross revenue recognition processing", step_type="Automated", r="Automated (or GFS in absence of Automation)", a="GFS", i="Project Manager", sys="Contract Capture Agent / PSA")
                    ]),
                _s(seq="4.1.3", name="Exceptions Identified?", desc="Determine whether there is missing, incomplete or inconsistent data (e.g., timing differences)", step_type="Decision", r="Automated (or GFS in absence of Automation)", a="GFS", sys="PSA", outcomes="Yes - proceed to 4.1.4 | No - proceed to 4.1.5"),
                _s(seq="4.1.4", name="Exception Resolution", desc="Resolve identified exceptions", r="GFS", a="GFS", i="Project Manager", sys="PSA", children=[
                    _s(seq="4.1.4.1", name="Investigate Revenue Exception", desc="Identify root cause of exception (e.g., missing timecard, unapproved or unsubmitted expense, inaccurate PoC calculation, etc.", r="GFS", a="GFS", i="Project Manager", sys="PSA"),
                    _s(seq="4.1.4.2", name="Resolve Missing or Incorrect Data", desc="Obtain missing data or correct erroneous inputs (e.g., submit late timecards, approve expense reports, correct PoC calculation)", r="Client Services / Account Managers", a="GFS", i="Project Manager", sys="PSA"),
                    _s(seq="4.1.4.3", name="Obtain Re-Approval if Required", desc="Where corrections change revenue amounts or treatment, obtain re-approval from appropriate authority before proceeding", r="GFS", a="GFS", i="Project Manager", sys="PSA")
                    ]),
                _s(seq="4.1.5", name="Revenue Execution (incl. Accruals & Deferrals)", desc="Revenue is calculated according to revenue recognition rules aligned to contract terms. Recognise accrued revenue for earned but unbilled amounts and deferred revenue for billed but unearned amounts.", r="GFS", a="GFS", sys="PSA", children=[
                    _s(seq="4.1.5.1", name="Revenue Treatment Routing", desc="Route transactions to appropriate revenue recognition calculation logic based on method", r="GFS", a="GFS", sys="PSA"),
                    _s(seq="4.1.5.2", name="T&M: Calculate Revenue from Submitted Time", desc="For T&M projects, calculate revenue as submitted hours × contracted rates", r="GFS", a="GFS", sys="PSA"),
                    _s(seq="4.1.5.3", name="Fixed Fee/Milestone-based: Calculate Revenue from PoC (or by Milestone Completion)", desc="Recognise revenue at the primary project level wherever operationally feasible to support aggregated  revenue recognition treatment  For Fixed Fee and milestone-based projects, recognise revenue based on validated percentage of completion against contracted project value  Milestone - by exception only: Where PoC is not applicable, recognise revenue based on value associated with completed milestone  Known exception: Evoke recognising based on milestone completion", r="GFS", a="GFS", i="Project Manager", sys="PSA"),
                    _s(seq="4.1.5.4", name="SaaS / Recurring: Calculate Recurring Revenue", desc="For SaaS and recurring revenue projects, recognise recurring revenue ratably over the active subscription period through periodic deferred revenue release based on contracted subscription terms and billing schedule. Exclude one-time fees and non-recurring charges from recurring revenue treatment", r="GFS", a="GFS", sys="N/A"),
                    _s(seq="4.1.5.5", name="Passthrough Revenue Recognition", desc="Recognise gross passthrough revenue, including associated markup or management / service fee, upon delivery of the underlying service", r="GFS", a="GFS", sys="PSA"),
                    _s(seq="4.1.5.6", name="Calculate Accrued & Deferred Revenue", desc="Calculate accrued revenue for earned but unbilled amounts, and deferred revenue for billed but unearned amounts in line with agreed revenue recognition treatment", r="GFS", a="GFS", i="Project Manager", sys="PSA")
                    ]),
                _s(seq="4.1.6", name="Journal Entry Preparation & Routing", desc="Prepare revenue journal entries based on calculated revenue outputs and route for approval in line with financial controls", step_type="Automated", r="Automated (or GFS in absence of Automation)", a="GFS", sys="ERP", children=[
                    _s(seq="4.1.6.1", name="Prepare Revenue Journal Entries", desc="Prepare revenue journal entries for recognised revenue, accruals, deferrals and unbilled AR movements based on revenue calculation outputs", step_type="Automated", r="Automated (or GFS in absence of Automation)", a="GFS", sys="ERP"),
                    _s(seq="4.1.6.2", name="Route Journals for Approval", desc="Route revenue journal entries for review and approval in line with financial controls and delegation of authority", step_type="Automated", r="Automated (or GFS in absence of Automation)", a="GFS", sys="ERP")
                    ]),
                _s(seq="4.1.7", name="Journal Entry Review & Approval", desc="Review and approve revenue journal entries for accuracy, completeness and compliance with revenue recognition policy", r="GFS", a="GFS", sys="ERP", children=[
                    _s(seq="4.1.7.1", name="Journal Entry Review", desc="Review revenue journal entries for accuracy, completeness and compliance with revenue recognition policy", r="GFS", a="GFS", sys="ERP"),
                    _s(seq="4.1.7.2", name="Journal Approved?", desc="Determine whether journal entry is approved for posting. If journal is rejected, return to preparer with rejection reason", step_type="Decision", r="GFS", a="GFS", sys="ERP", outcomes="Yes - proceed to 4.1.8 | No - proceed to 4.1.6.1")
                    ]),
                _s(seq="4.1.8", name="Revenue Posting & Reconciliation", desc="Post revenue journal entries to the general ledger. System updates deferred revenue, accrued revenue and unbilled AR balances accordingly", step_type="Automated", r="Automated (or GFS in absence of Automation)", a="GFS", sys="ERP", children=[
                    _s(seq="4.1.8.1", name="Journal Entry Posting", desc="Post approved revenue journal entries to the general ledger. System updates revenue accounts automatically", step_type="Automated", r="Automated (or GFS in absence of Automation)", a="GFS", sys="ERP"),
                    _s(seq="4.1.8.2", name="Deferred / Accrued Balance Reconciliation", desc="System automatically updates deferred revenue, accrued revenue and unbilled AR balances based on posted revenue activity", step_type="Automated", r="Automated (or GFS in absence of Automation)", a="GFS", sys="ERP")
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
                    _s(seq="4.2.2.2", name="Route Journals for Approval", desc="Route adjustment journal entries for approval in line with financial controls and delegation of authority", step_type="Automated", r="Automated (or GFS in absence of Automation)", a="GFS", sys="ERP")
                    ]),
                _s(seq="4.2.3", name="Journal Review & Approval", desc="Review and approve journal entries in line with financial controls", r="GFS", a="GFS", sys="ERP", children=[
                    _s(seq="4.2.3.1", name="Journal Entry Review", desc="Review adjustment journal entries for accuracy, completeness and compliance with revenue recognition policy", r="GFS", a="GFS", sys="ERP"),
                    _s(seq="4.2.3.2", name="Journal Approved?", desc="Determine whether adjustment journal entry is approved for posting. If journal is rejected, return to preparer with rejection reason", step_type="Decision", r="GFS", a="GFS", sys="ERP", outcomes="Yes - proceed to 4.2.6 | No - proceed to 4.2.2.1")
                    ]),
                _s(seq="4.2.6", name="Adjustment Posting", desc="Post adjustment or true-up journal entries to the general ledger. Update project and financial records accordingly. Systematic update to revenue forecast.", r="GFS", a="GFS", sys="ERP", children=[
                    _s(seq="4.2.6.1", name="Journal Entry Posting", desc="Post approved revenue journal entries to the general ledger. System updates revenue and balance sheet accounts automatically", step_type="Automated", r="Automated (or GFS in absence of Automation)", a="GFS", sys="ERP"),
                    _s(seq="4.2.6.3", name="Deferred / Accrued Balance Update", desc="System automatically updates deferred revenue, accrued revenue and unbilled AR balances based on posted adjustment activity", step_type="Automated", r="Automated (or GFS in absence of Automation)", a="GFS", sys="ERP")
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
            "system_tool": "Billing Agent",
            "raci": {"r": "GFS", "a": "GFS", "i": ""},
            "steps": [
                _s(seq="5.1.1", name="Invoice Submission Calendar", desc="Define and communicate invoice timetable and cut-off dates for each financial period", r="GFS", a="GFS", sys="Billing Agent", children=[
                    _s(seq="5.1.1.1", name="Invoice Calendar & Cut-Off Definition", desc="Define invoice timetable and invoice cut-off dates for each financial period", r="GFS", a="GFS", sys="Billing Agent"),
                    _s(seq="5.1.1.2", name="Invoice Timeline Communication", desc="Communicate invoice timetable, submission deadlines and cut-off dates to stakeholders ahead of each financial period. Send automated reminders in advance of key billing deadlines", r="GFS", a="GFS", sys="Billing Agent")
                    ]),
                _s(seq="5.1.2", name="Invoice Trigger Initiated", desc="Trigger invoice cycle based on agreed billing events and invoicing arrangements (e.g., scheduled billing date, milestone completion, pre-billing, etc.)", r="AI Agent - Billing (or GFS in absence of Agent)", a="Client Services / Account Managers", sys="Billing Agent / PSA", children=[
                    _s(seq="5.1.2.1", name="Identify Billing Pathway", desc="Determine applicable billing pathway and route to appropriate invoicing process. Where agreed under SOW / MSA terms, scheduled billing should be used for T&M and Fixed Fee engagements to support downstream billing automation", r="AI Agent - Billing (or GFS in absence of Agent)", a="GFS", sys="Billing Agent"),
                    _s(seq="5.1.2.2", name="T&M Trigger: Billing Event Achieved", desc="For T&M projects, trigger invoice cycle based on agreed billing structure (e.g., scheduled billing date reached or submitted billable hours for the current billing period under non-scheduled billing arrangements)", r="AI Agent - Billing (or GFS in absence of Agent)", a="Project Manager", sys="PSA"),
                    _s(seq="5.1.2.3", name="Milestone Trigger: Billing Milestone Achieved", desc="For milestone-based billing arrangements, billing milestone achieved and invoicing event triggered", r="AI Agent - Billing (or GFS in absence of Agent)", a="Project Manager", sys="PSA"),
                    _s(seq="5.1.2.4", name="Fixed Fee / Scheduled Billing Trigger: Billing Date Achieved", desc="For fixed fee using scheduled billing arrangements, scheduled billing date reached for invoicing cycle initiation", r="AI Agent - Billing (or GFS in absence of Agent)", a="Client Services / Account Managers", sys="Billing Agent"),
                    _s(seq="5.1.2.5", name="SaaS / Recurring Trigger: Billing Cycle Active", desc="For SaaS / recurring revenue billing arrangements, recurring billing cycle reaches scheduled invoicing period", r="GFS", a="Client Services / Account Managers", sys="Billing Agent"),
                    _s(seq="5.1.2.6", name="Upfront Billing Trigger: Signed SOW Achieved", desc="For upfront or pre-billing arrangements, SOW with upfront billing requirements is executed, and milestone is created and marked as complete to trigger invoice cycle initiation", r="AI Agent - Billing (or GFS in absence of Agent)", a="Client Services / Account Managers", sys="Billing Agent"),
                    _s(seq="5.1.2.7", name="Ad-Hoc Billing Trigger Initiated", desc="Trigger off-cycle or discretionary invoice generation based on approved client request or commercial agreement outside standard billing schedule", r="GFS", a="Client Services / Account Managers", sys="Billing Agent"),
                    _s(seq="5.1.2.8", name="Expense Trigger: Approved Expense Submitted", desc="Approved reimbursable expenses submitted and available for invoicing for the billing period", step_type="Automated", r="Automated (or GFS in absence of Automation)", a="GFS", sys="ERP / Concur"),
                    _s(seq="5.1.2.9", name="Passthrough Billing Trigger: Cost Incurred (Markup, No Markup, Mgmt. / Service Fee)", desc="Passthrough costs incurred and available for invoicing", r="GFS", a="GFS", sys="ERP")
                    ]),
                _s(seq="5.1.3", name="Billing Validation & Exception Handling", desc="Validate billing inputs, contract alignment and billing trigger conditions. Identify and resolve billing exceptions prior to invoice generation", r="GFS", a="GFS", i="Project Manager", sys="Contract Capture Agent / Billing Agent / PSA", children=[
                    _s(seq="5.1.3.1", name="Contract, PO & Billing Validation", desc="Automatically validate billing inputs against SOW, MSA, billing schedule and PO requirements. Confirm an active, valid Purchase Order (or group of Purchase Orders) is linked to the project with sufficient remaining balance to cover the billing amount, and compare to SOW/MSA for legal entity name, billing entity name, scope, milestone schedule alignment. Validate billed-to-date amounts against available PO balances and grouped PO allocations where applicable. Identify insufficient PO coverage, expired PO limits or overbilling risk prior to invoice generation. Flag exceptions for GFS review and escalation", r="AI Agent - Billing (or GFS in absence of Agent)", a="GFS", sys="Contract Capture Agent / Billing Agent"),
                    _s(seq="5.1.3.2", name="T&M: Billing Input Validation", desc="Validate submitted billable hours, contracted rates and billing summaries for the billing period. Validate against agreed T&M billing caps where applicable, as per SOW. For T&M projects using scheduled billing arrangements, validate scheduled invoice amounts and associated billing schedule, as per SOW", r="Project Manager", a="Project Manager", sys="PSA / Billing Agent"),
                    _s(seq="5.1.3.3", name="Milestone: Billing Input Validation", desc="Validate milestone completion, client acceptance and agreed billing amounts in line with contracted milestone billing terms", r="GFS", a="Project Manager", i="Project Manager", sys="PSA / Billing Agent"),
                    _s(seq="5.1.3.4", name="Fixed Fee / Scheduled: Billing Validation", desc="Validate agreed billing dates and scheduled invoice amounts in line with contracted billing schedule", r="AI Agent - Billing (or GFS in absence of Agent)", a="GFS", sys="Contract Capture Agent / Billing Agent"),
                    _s(seq="5.1.3.5", name="SaaS / Recurring: Billing Validation", desc="Validate recurring billing schedule, subscription terms and contracted recurring invoice amounts for the billing period. Exclude one-time fees and non-recurring charges from recurring billing validation", r="Client Services / Account Managers", a="GFS", sys="Billing Agent"),
                    _s(seq="5.1.3.6", name="Upfront / Pre-billing: Billing Validation", desc="Validate executed SOW, agreed upfront billing amount and associated billing trigger prior to invoice generation", r="AI Agent - Billing (or GFS in absence of Agent)", a="GFS", sys="Billing Agent"),
                    _s(seq="5.1.3.7", name="Ad-Hoc Billing Validation", desc="Validate approved ad-hoc billing request, agreed billing amount and required approval prior to invoice generation", r="GFS", a="GFS", i="Client Services / Account Managers", sys="Billing Agent"),
                    _s(seq="5.1.3.7", name="Expense & Approved Costs: Billing Validation", desc="Confirm all reimbursable expenses for the billing period have been submitted and approved", r="Project Manager", a="Project Manager", sys="Concur / ERP"),
                    _s(seq="5.1.3.8", name="Passthrough (Markup, No Markup, Mgmt. / Service Fee): Billing Validation", desc="Validate passthrough charges, supporting documentation and agreed SOW billing treatment prior to invoice generation", r="Project Manager", a="Project Manager", sys="ERP"),
                    _s(seq="5.1.3.9", name="Billing Validation Passed?", desc="Determine whether billing validation criteria have been met", step_type="Decision", r="AI Agent - Billing (or GFS in absence of Agent)", a="GFS", i="Client Services / Account Managers / Project Manager", sys="Billing Agent", outcomes="Yes - proceed to 5.1.6 | No - proceed to 5.1.4")
                    ]),
                _s(seq="5.1.4", name="Mismatch Identified?", desc="Determine whether discrepancies exist between billing inputs, contract terms and invoicing requirements (e.g., rates, milestones, PO values or billing entities)", step_type="Decision", r="AI Agent - Billing (or GFS in absence of Agent)", a="GFS", sys="Billing Agent", outcomes="Yes - proceed to 5.1.5 | No - proceed to 5.1.6"),
                _s(seq="5.1.5", name="Mismatch Resolution", desc="Investigate and resolve billing discrepancies and apply required corrections prior to invoice generation", r="GFS", a="Client Services / Account Managers", sys="Billing Agent / PSA", children=[
                    _s(seq="5.1.5.1", name="Billing Exception Investigation", desc="Investigate root cause of billing discrepancy (e.g., rate card error, unapproved time, milestone variance, PO shortfall or incorrect legal entity) with Client Services or Project Manager. Determine corrective action and client communication requirements", r="GFS", a="Client Services / Account Managers", i="Project Manager", sys="Billing Agent / PSA"),
                    _s(seq="5.1.5.2", name="Billing Data Correction", desc="Apply corrections to billing inputs, timecards, expenses, milestones or contract data where required. Obtain re-approval where necessary", r="GFS", a="Client Services / Account Managers", sys="Billing Agent / PSA"),
                    _s(seq="5.1.5.3", name="Billing Validation Recheck", desc="Re-run billing validation checks after corrections are applied and confirm discrepancy has been resolved prior to invoice generation", r="GFS", a="Client Services / Account Managers", sys="Billing Agent / PSA")
                    ]),
                _s(seq="5.1.6", name="Billing Data Preparation, Consolidation & Formatting", desc="Compile billable items, apply billing treatments and prepare invoice structure, including consolidation across projects (parent / IHL-billing) and client-specific invoicing requirements, as required", r="GFS", a="GFS", i="Client Services / Account Managers", sys="Billing Agent / PSA", children=[
                    _s(seq="5.1.6.1", name="T&M Billing Data Compilation", desc="For T&M billing, automatically compile submitted billable hours and contracted billing rates for the invoicing period. Apply agreed T&M billing caps where applicable, as per SOW. Where scheduled billing arrangements apply, compile invoice amounts in line with contracted billing schedule in executed SOW", r="AI Agent - Billing (or GFS in absence of Agent)", a="GFS", sys="Billing Agent / PSA"),
                    _s(seq="5.1.6.2", name="Milestone Billing Compilation", desc="For Milestone billing, automatically compile milestone billing amounts based on achieved billing milestones and client acceptance status", r="AI Agent - Billing (or GFS in absence of Agent)", a="GFS", sys="Billing Agent / PSA"),
                    _s(seq="5.1.6.3", name="Fixed Fee / Scheduled Billing Compilation", desc="For Fixed Fee / Scheduled billing, automatically compile scheduled billing amounts and agreed invoice values for the invoicing period in line with contracted billing schedule in executed SOW", r="AI Agent - Billing (or GFS in absence of Agent)", a="GFS", sys="Billing Agent / PSA"),
                    _s(seq="5.1.6.4", name="SaaS / Recurring Billing Compilation", desc="For SaaS / Recurring billing, automatically compile recurring subscription billing amounts for the invoicing period", r="GFS", a="GFS", i="Client Services / Account Managers", sys="Billing Agent / PSA"),
                    _s(seq="5.1.6.5", name="Upfront Billing Compilation", desc="For upfront billing, automatically compile agreed upfront or pre-billing invoice amounts in line with contracted billing terms and approved billing trigger", r="AI Agent - Billing (or GFS in absence of Agent)", a="GFS", sys="Billing Agent / PSA"),
                    _s(seq="5.1.6.6", name="Ad-Hoc Billing Compilation", desc="Compile approved ad-hoc billing amounts and supporting billing detail for invoice generation in line with approved billing request", r="GFS", a="GFS", i="Client Services / Account Managers", sys="Billing Agent / PSA"),
                    _s(seq="5.1.6.7", name="Expense Compilation", desc="Automatically compile approved reimbursable employee and project expenses for invoice generation", step_type="Automated", r="Automated (or GFS in absence of Automation)", a="GFS", sys="ERP / Concur"),
                    _s(seq="5.1.6.8", name="Passthrough Billing Compilation", desc="Compile passthrough billing amounts, including associated markup or management/service fee amounts, for invoice generation in line with agreed SOW treatment. Prompt billing user to determine whether passthrough costs and associated markup / mgmt. fee should appear as combined or separate invoice line items based on client preference", r="AI Agent - Billing (or GFS in absence of Agent)", a="GFS", sys="Billing Agent / PSA"),
                    _s(seq="5.1.6.9", name="Invoice Formatting & Delivery Method Determination", desc="Use standardised invoice templates where possible to support downstream billing consistency and automation. Prompt user to apply invoice template, billing format, client-specific invoicing requirements and invoice delivery method. Where e-invoicing is required under MSA or billing master data, default invoice generation to structured e-invoicing rather than PDF output", r="GFS", a="Client Services / Account Managers", sys="Billing Agent"),
                    _s(seq="5.1.6.10", name="Invoice Narration & Supporting Documentation", desc="Include invoice narrative, billing period references, deliverables, client-specific language and supplemental attachments where required under contract terms. Include SOW reference ID / Project Number and PO Number(s) in narrative", r="GFS", a="Client Services / Account Managers", i="Client Services / Account Managers", sys="Billing Agent"),
                    _s(seq="5.1.6.11", name="Billing Adjustment & Hold Review", desc="Prompt user to review and apply admin fee, billing adjustments including credits, write-downs, billing holds and excluded line items prior to invoice generation", r="GFS", a="Client Services / Account Managers", sys="Billing Agent"),
                    _s(seq="5.1.6.12", name="Billing on Behalf Consolidation", desc="Where consolidated billing is required, consolidate billing events, invoice amounts and supporting billing data across contributing projects, divisions or entities for centralised invoice generation under lead Parent or IHL billing entity, as per SOW", r="GFS", a="GFS", i="Client Services / Account Managers", sys="Billing Agent"),
                    _s(seq="5.1.6.13", name="Intercompany Billing Determination", desc="Determine whether intercompany recharge treatment is required where work is delivered by one entity and billed through another entity", step_type="Decision", r="GFS", a="GFS", i="Client Services / Account Managers", sys="Billing Agent", outcomes="Yes - proceed to 5.3.4.3 | No - proceed to 5.3.2.1"),
                    _s(seq="5.1.6.14", name="Generate Billing Document", desc="Generate draft billing document for review, validation and client feedback prior to invoice generation", r="AI Agent - Billing (or GFS in absence of Agent)", a="GFS", sys="Billing Agent")
                    ]),
                _s(seq="5.1.7", name="T&M only: Client Services / Operations Review", desc="Route billing document for Project Manager review where required (T&M non-scheduled billing only) prior to invoice generation and client submission", r="Project Manager", a="Project Manager", sys="Billing Agent"),
                _s(seq="5.1.8", name="Approval & Sign-off", r="AI Agent - Billing (or GFS in absence of Agent)", a="GFS", sys="Billing Agent", children=[
                    _s(seq="5.1.8.1", name="Invoice Routing", desc="Route billing document to Project Manager via automated workflow for review and approval", r="AI Agent - Billing (or GFS in absence of Agent)", a="GFS", sys="Billing Agent"),
                    _s(seq="5.1.8.2", name="PM Review", desc="Biling Agent prompts user to review billing document for billing accuracy, client-specific invoicing requirements and completeness of supporting information prior to client submission", r="Project Manager", a="Project Manager", sys="Billing Agent"),
                    _s(seq="5.1.8.3", name="Invoice Approved for Client Review or Submission?", desc="Determine whether billing document and billing inputs are approved for client submission. If rejected, provide reasoning", step_type="Decision", r="Project Manager", a="Project Manager", sys="Billing Agent / ERP / PSA", outcomes="Yes - proceed to 5.2 | No - proceed to 5.1.6.1")
                    ]),
            ],
        },
        {
            "id": "5.2",
            "seq": "5.2",
            "name": "Client Review & Approval",
            "description": "Facilitate client review of billing document, resolve queries and obtain approval",
            "step_type": "Process",
            "system_tool": "Email",
            "raci": {"r": "GFS", "a": "GFS", "i": "Client Services / Account Managers"},
            "steps": [
                _s(seq="5.2.1", name="Submit Billing Document to Client for Review", desc="Submit billing documnet to client for review where required under agreed billing arrangements or client requirements", r="GFS", a="GFS", i="Client Services / Account Managers", sys="Email", children=[
                    _s(seq="5.2.1.1", name="Client Review Required?", desc="Determine whether client review of billing document is required prior to invoice generation", step_type="Decision", r="GFS", a="GFS", i="Client Services / Account Managers", sys="Email", outcomes="Yes - proceed to 5.2.1.2 | No - proceed to 5.3"),
                    _s(seq="5.2.1.2", name="Identify Delivery Method for Client Review", desc="Determine delivery method for client billing document review (e.g., email or secure file-sharing channel)", r="GFS", a="GFS", i="Client Services / Account Managers", sys="Email"),
                    _s(seq="5.2.1.3", name="Submit Billing Document for Client Review", desc="Transmit billing document to client via agreed submission channel. Include supporting documentation as required (e.g. timesheets, deliverable summaries). Confirm agreed client review and response timeframe", r="GFS", a="GFS", i="Client Services / Account Managers", sys="Email")
                    ]),
                _s(seq="5.2.2", name="Client Query Raised?", desc="Monitor for client response or billing query within agreed SLA", step_type="Decision", r="GFS", a="GFS", i="Client Services / Account Managers", sys="Email", outcomes="Yes - proceed to 5.2.3 | No - proceed to 5.2.4"),
                _s(seq="5.2.3", name="Client Query Resolution", desc="Address client queries or disputes. Provide supporting documentation or revise billing document as required", r="GFS", a="GFS", i="Client Services / Account Managers", sys="Email", children=[
                    _s(seq="5.2.3.1", name="Receive & Log Client Query", desc="Capture client query details, categorise issue type (amount, scope, format, PO, compliance)", r="GFS", a="GFS", i="Client Services / Account Managers", sys="Email"),
                    _s(seq="5.2.3.2", name="Investigate, Resolve & Prepare Response", desc="Review client query against contract terms, billing data and supporting documentation. Resolve query and prepare client response or billing document revision where required", r="GFS", a="GFS", i="Client Services / Account Managers", sys="Email"),
                    _s(seq="5.2.3.3", name="Revise Billing Document if Required", desc="If query results in a change, correct billing data and regenerate billing document", r="GFS", a="GFS", i="Client Services / Account Managers", sys="Email")
                    ]),
                _s(seq="5.2.4", name="Client Approval", desc="Obtain client approval to proceed with invoice generation and issuance", r="GFS", a="GFS", i="Client Services / Account Managers", sys="Email"),
            ],
        },
        {
            "id": "5.3",
            "seq": "5.3",
            "name": "Execution & Submission",
            "description": "Finalise billing document, perform final validation within Billing Agent and push approved billing output to ERP for invoice generation and client submission",
            "step_type": "Process",
            "system_tool": "ERP",
            "raci": {"r": "GFS", "a": "GFS", "i": ""},
            "steps": [
                _s(seq="5.3.1", name="Finalise Billing Document", desc="Finalise invoice structure, validate final invoice output and prepare invoice for client issuance", r="GFS", a="GFS", sys="Billing Agent", children=[
                    _s(seq="5.3.1.1", name="Final Billing Document Validation", desc="Perform final validation of billing document and structured e-invoice requirements within Billing Agent prior to ERP handoff, including validation of billing completeness, submission requirements and formatting standards", r="GFS", a="GFS", sys="Billing Agent"),
                    _s(seq="5.3.1.2", name="ERP Invoice Generation Trigger", desc="Push approved billing document from Billing Agent to ERP to trigger final invoice generation and downstream client submission process", r="GFS", a="GFS", sys="Billing Agent")
                    ]),
                _s(seq="5.3.2", name="Invoice Preparation", desc="Generate final invoice within ERP using approved billing document, reimbursable expenses and validated invoice structure", step_type="Automated", r="Automated (or GFS in absence of Automation)", a="GFS", sys="ERP", children=[
                    _s(seq="5.3.2.1", name="ERP Billing Document Receipt", desc="Receive approved billing document from Billing Agent within ERP for final invoice generation", step_type="Automated", r="Automated (or GFS in absence of Automation)", a="GFS", sys="ERP"),
                    _s(seq="5.3.2.2", name="Reimbursable Expense Integration", desc="Append approved reimbursable expenses and associated ERP-based billing items (e.g., Concur expenses) to invoice structure where applicable", step_type="Automated", r="Automated (or GFS in absence of Automation)", a="GFS", sys="ERP"),
                    _s(seq="5.3.2.3", name="Tax Calculation", desc="Apply and validate tax treatment across fees, passthrough charges and reimbursable expenses based on billing entity jurisdiction, client location, service type and invoicing method", step_type="Automated", r="Automated (or GFS in absence of Automation)", a="GFS", sys="ERP"),
                    _s(seq="5.3.2.4", name="Final Invoice / E-Invoice Generation", desc="Generate final invoice or structured e-invoice output within ERP using validated billing data and approved invoice structure", step_type="Automated", r="Automated (or GFS in absence of Automation)", a="GFS", sys="ERP"),
                    _s(seq="5.3.2.5", name="Invoice Workflow & Submission Status Tracking", desc="Track invoice workflow, review and submission status within Billing Agent across invoice preparation, ERP generation and client submission lifecycle stages. Synchronise ERP invoice and submission statuses back to Billing Agent for operational tracking and exception management", r="AI Agent - Billing (or GFS in absence of Agent)", a="GFS", sys="ERP / Billing Agent")
                    ]),
                _s(seq="5.3.3", name="Invoice Submission to Client", desc="Submit final invoice to client via agreed submission channel and confirm successful invoice issuance", r="GFS", a="GFS", sys="ERP", children=[
                    _s(seq="5.3.3.1", name="Submit Final Invoice via Client Channel", desc="Issue final approved invoice to client via required submission channel (e.g., email, AP portal, EDI, e-invoicing, mail). Where required, follow client-specific submission protocols", r="GFS", a="GFS", sys="ERP / Client Portal / Email"),
                    _s(seq="5.3.3.2", name="Invoice Submission Successful?", desc="Determine whether invoice or e-invoice submission completed successfully and was accepted by the client submission channel", step_type="Decision", r="GFS", a="GFS", sys="ERP", outcomes="Yes - proceed to 5.3.3.4 | No - proceed to 5.3.3.3"),
                    _s(seq="5.3.3.3", name="Invoice Submission Rejection Resolution", desc="Investigate invoice or e-invoice rejection, correct submission, formatting or compliance issues and regenerate / re-submit invoice where required", r="GFS", a="Client Services / Account Managers", i="Client Services / Account Managers", sys="ERP / Billing Agent / PSA"),
                    _s(seq="5.3.3.4", name="Submission Confirmation & Audit Capture", desc="Capture invoice submission confirmation, transmission status and supporting audit records for invoice issuance tracking", r="GFS", a="GFS", sys="ERP"),
                    _s(seq="5.3.3.5", name="Attach Invoice & Confirmation to Project Record", desc="Attach final invoice output and submission confirmation to ERP project record and associated document repositories where required", r="GFS", a="GFS", i="Client Services / Account Managers", sys="ERP")
                    ]),
                _s(seq="5.3.4", name="AR Posting & Accounting Update", desc="Post issued invoice to AR sub-ledger and update associated accounting balances, AR aging and intercompany accounting records", r="GFS", a="GFS", sys="ERP", children=[
                    _s(seq="5.3.4.1", name="Post Invoice to AR Sub-Ledger", desc="Automatically post issued invoice to AR sub-ledger and update customer balance. System generates AR aging entry and updates project billing records", step_type="Automated", r="Automated", a="GFS", sys="ERP"),
                    _s(seq="5.3.4.2", name="Update Deferred / Unbilled Revenue Balances", desc="Automatically update unbilled AR, accrued revenue and deferred revenue balances resulting from issued invoice activity", step_type="Automated", r="Automated", a="GFS", sys="ERP"),
                    _s(seq="5.3.4.3", name="Raise Intercompany Recharge Request", desc="Initiate intercompany recharge process where work is delivered by one entity and billed through another entity. Submit provider and receiver entity details and trigger associated intercompany accounting entries", r="GFS", a="GFS", sys="ERP")
                    ]),
                _s(seq="5.3.5", name="Reconciliation", desc="Perform billing reconciliations and confirm billing completeness, intercompany settlement and billing period close activities", r="GFS", a="GFS", sys="ERP", children=[
                    _s(seq="5.3.5.1", name="Billing-to-Contract Reconciliation", desc="Reconcile billed amounts against contract value, SOW billing schedule, approved billing events and PO balances. Identify overbilling, underbilling or remaining uninvoiced balances", r="GFS", a="GFS", sys="ERP"),
                    _s(seq="5.3.5.2", name="Intercompany Billing Reconciliation", desc="Reconcile intercompany recharge balances and confirm associated accounting entries are settled between entities", r="GFS", a="GFS", sys="ERP"),
                    _s(seq="5.3.5.3", name="Month-End Billing Close", desc="Complete month-end billing reconciliation and confirm all invoices for the billing period have been generated, submitted and posted prior to billing period close", r="GFS", a="GFS", sys="ERP")
                    ]),
                _s(seq="5.3.6", name="Unbilled Revenue Monitoring & Escalation", desc="Monitor aging uninvoiced balances, unresolved billing dependencies and at-risk projects. Trigger proactive stakeholder prompts, escalation workflows and governance reviews to support timely invoice generation and resolution of unbilled balances", r="GFS", a="GFS", sys="Billing Agent / PowerBI", children=[
                    _s(seq="5.3.6.1", name="Unbilled Revenue Monitoring", desc="Identify projects with recognised or accrued revenue that remain uninvoiced beyond agreed billing timelines, including projects with missing milestone updates, delayed billing triggers, missing PO/documentation or unresolved billing dependencies", r="AI Agent - Billing (or GFS in absence of Agent)", a="GFS", i="Project Manager", sys="Billing Agent"),
                    _s(seq="5.3.6.2", name="Proactive Prompting", desc="Trigger proactive prompt and review workflow to Account Managers for unresolved unbilled balances, overdue billing milestones and delayed billing activity", r="AI Agent - Billing (or GFS in absence of Agent)", a="Client Services / Account Managers", i="Project Manager", sys="Billing Agent"),
                    _s(seq="5.3.6.3", name="Escalation Review", desc="Escalate unresolved unbilled balances, overdue billing milestones and unresolved billing dependencies to Finance and Operations leadership for resolution prior in line with defined aging or escalation thresholds", r="GFS", a="Portfolio Leaders (MD)", i="Client Services / Account Managers", sys="Billing Agent"),
                    _s(seq="5.3.6.4", name="Projects At-Risk Register (PARR) nd Paperless Pursuits Monitoring", desc="Monitor projects generating revenue without approved PO, billing authorisation or executed contract documentation. Escalate unresolved commercial, contractual or billing risks through PARR and Paperless Pursuit governance processes", r="GFS", a="Client Services / Account Managers", i="Project Manager", sys="PowerBI"),
                    _s(seq="5.3.6.5", name="Unbilled Resolution Tracking", desc="Track aging, resolution status and corrective actions for unresolved unbilled balances through to invoice generation, write-off or escalation closure", r="GFS", a="Client Services / Account Managers", i="Project Manager", sys="PowerBI")
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
                _s(seq="7.1.3", name="Contract Compliance Review", desc="Verify all contractual obligations have been fulfilled and no outstanding amendments or change orders exist", r="GFS", a="GFS", i="Client Services / Account Managers", sys="CLM / PSA / ERP", children=[
                    _s(seq="7.1.3.1", name="Verify All Contractual Obligations Met", desc="Review contract terms against delivered scope. Confirm all deliverables, SLAs and obligations have been fulfilled", r="GFS", a="GFS", i="Client Services / Account Managers", sys="CLM / PSA / ERP"),
                    _s(seq="7.1.3.2", name="Confirm No Outstanding Amendments or Change Orders", desc="Check for any pending contract amendments, change orders or scope changes that require resolution before close", r="GFS", a="GFS", i="Client Services / Account Managers", sys="CLM / PSA / ERP")
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