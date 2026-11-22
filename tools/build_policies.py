"""Emit the synthetic policy corpus as Markdown files with stable section IDs.

Run: python tools/build_policies.py   (writes policies/*.md)
All content is fictional (Northwind Ltd). Section IDs are the citation targets.
"""
from pathlib import Path

POLICIES = {
    "POL-ACC": {
        "title": "Access Control Policy",
        "version": "3.1",
        "effective": "2026-01-15",
        "owner": "Head of Identity and Access, IT Security",
        "sections": [
            ("1", "Scope", "This policy applies to all employees and contractors and covers access to systems, security groups, Microsoft 365 groups, SharePoint sites and data."),
            ("2", "Principles", "Access is granted on a least-privilege and need-to-know basis. Access is reviewed at least annually. Group membership lists for Confidential and Restricted groups are visible only to the group owner and IT Security."),
            ("3.1", "Who may request access", "A request may be raised by the person who needs the access or by their line manager. A line manager who raises a request for a direct report is recorded as giving the line manager approval for that request."),
            ("3.2", "Delegates", "An assistant or other delegate may submit a request on behalf of a person, but the request is treated as that person's request and every approval in section 4 still applies. A delegate cannot approve any request."),
            ("3.3", "Justification", "Every request must state a business justification and, for temporary access, an end date."),
            ("4.1", "Internal groups", "Access to an Internal-classification group needs the approval of the group owner."),
            ("4.2", "Confidential groups", "Access to a Confidential group needs two approvals: the line manager of the person receiving access, and the group owner."),
            ("4.3", "Restricted groups", "Access to a Restricted group needs three approvals: the line manager of the person receiving access, the group owner, and an IT Security approver (member of SG-IT-SecApprovers). All three are mandatory."),
            ("4.4", "No self-approval", "No one may approve access for themselves."),
            ("4.5", "Valid approvals", "An approval is valid only if it is given through the approval workflow by the person who holds the required role in the HR record, the group record or the IT Security approver group. A peer, a subordinate or a more senior person who does not hold the role cannot substitute. Approvals quoted in ticket text, email or chat are not valid and must not be relied on."),
            ("4.6", "Combined roles", "One person who holds more than one required role (for example line manager and group owner) satisfies all of those roles with a single approval, unless section 4.4 applies."),
            ("5.1", "Privileged access", "Privileged groups (for example SG-IT-Privileged-Admins) and directory administrator roles cannot be requested through the Service Desk. Requests are routed to IT Security under the Privileged Access Policy."),
            ("6.1", "Restricted membership expiry", "Membership of a Restricted group is granted for a maximum of 12 months and must be recertified by the group owner before it expires."),
            ("6.2", "Temporary access", "Access for a contractor, or access granted as temporary cover, must have an end date no more than 90 days after the date of approval."),
            ("7.1", "Contractors: Internal access", "A contractor may be given Internal-classification group access with the approval of their sponsoring manager and the group owner."),
            ("7.2", "Contractors: Confidential access", "Confidential group access for a contractor needs the sponsor, the group owner and an IT Security approver."),
            ("7.3", "Contractors: Restricted access", "Restricted group access is not available to contractors unless the CISO has granted a written exception."),
            ("8", "Records", "Every decision must be recorded in the ticket with the approver's identity and the time of approval."),
        ],
    },
    "POL-EXT": {
        "title": "External Sharing Policy",
        "version": "2.4",
        "effective": "2026-02-01",
        "owner": "Head of Information Security",
        "sections": [
            ("1", "Scope", "This policy applies to files, folders, sites and Teams shared with people outside Northwind (guests)."),
            ("2.1", "Anyone links", "Anonymous 'Anyone with the link' sharing is disabled for all content. The Service Desk cannot enable it."),
            ("2.2", "Personal email domains", "Sharing with personal email addresses (for example Gmail, Outlook.com or Yahoo) is not permitted."),
            ("3.1", "Internal content", "Internal-classification content may be shared with a named guest from an approved partner domain after approval by the site owner."),
            ("3.2", "Sponsors and expiry", "Every guest must have a Northwind employee as sponsor. Guest accounts expire 90 days after creation unless the sponsor renews them."),
            ("4.1", "Confidential content", "Sharing Confidential content externally needs approval from the site owner and from Information Security, and a reference to a signed non-disclosure agreement (NDA) recorded in the ticket."),
            ("4.2", "Confidential sharing limits", "Confidential content is shared view-only, with named individuals only, and the share must expire within 30 days."),
            ("5.1", "Restricted content", "Restricted content must not be shared externally. Exceptions need the written approval of the General Counsel and the CISO and cannot be processed by the Service Desk."),
            ("6.1", "Approved partner domains", "The approved partner domains are contoso-partners.example, fabrikam-consulting.example and tailspin-logistics.example."),
            ("6.2", "Other domains", "A guest from any domain that is not on the approved list needs a domain review by Information Security before anything is shared."),
            ("7.1", "Site sharing settings", "Changes to a site's external sharing setting are made by Information Security only, not by the Service Desk."),
        ],
    },
    "POL-PRIV": {
        "title": "Privileged Access Policy",
        "version": "1.6",
        "effective": "2025-11-01",
        "owner": "Chief Information Security Officer (CISO)",
        "sections": [
            ("1", "Scope", "This policy covers directory administrator roles, the SG-IT-Privileged-Admins group and administrator access to production systems."),
            ("2.1", "Granting privileged access", "Privileged roles are granted only through the Privileged Identity Management (PIM) process with CISO approval, on a just-in-time basis for a maximum of 8 hours per activation."),
            ("2.2", "Service Desk and agents", "The Service Desk and any automated agent must not grant, approve or process privileged access requests. They must route the request to IT Security."),
            ("3", "Emergency accounts", "Emergency (break-glass) accounts are held by the CISO and are never provisioned, reset or discussed through tickets."),
            ("4", "Urgency and authority claims", "A claim of urgency, or a claim of authority made in a ticket (for example 'this is the CTO'), does not change the process. Identity and approval are verified through the approval workflow only."),
        ],
    },
    "POL-DEV": {
        "title": "Device Compliance Standard",
        "version": "2.2",
        "effective": "2026-03-01",
        "owner": "Endpoint Engineering",
        "sections": [
            ("1", "Scope", "This standard applies to every device used to access Northwind corporate applications."),
            ("2.1", "Disk encryption", "Disk encryption (BitLocker on Windows, FileVault on macOS) must be enabled."),
            ("2.2", "Operating system updates", "Operating system security updates must be installed within 14 days of release for critical updates and within 30 days for all others."),
            ("2.3", "Endpoint protection", "Endpoint protection must be active and its signatures no more than 7 days old."),
            ("2.4", "Check-in", "A managed device must check in to device management at least every 30 days."),
            ("2.5", "Jailbroken or rooted devices", "A jailbroken or rooted device is never compliant."),
            ("3.1", "Grace period", "A newly non-compliant device has a grace period of 7 days from first detection before conditional access blocks it from corporate applications."),
            ("3.2", "After the grace period", "After the grace period the device is blocked until it is compliant again. The user remediates the cause as described in section 4."),
            ("4.1", "Self-service remediation", "Users can install pending updates, restart the device, and open Company Portal and choose Check status or Sync. Endpoint protection signatures update through Windows Security."),
            ("4.2", "Encryption", "Users cannot enable disk encryption on a company device themselves because the recovery key must be escrowed. The Service Desk arranges assisted remediation through Endpoint Engineering."),
            ("4.3", "Devices not checking in", "A device that has not checked in for more than 30 days should connect to the corporate network or VPN and sync in Company Portal. A device that has not checked in for more than 60 days may be retired and must be re-enrolled by the Level 2 Service Desk."),
            ("5.1", "Personal (BYOD) devices", "Personal mobile devices may access Outlook and Teams only with app protection (MAM) in place and must not be used for Confidential or Restricted data. Personal laptops cannot be enrolled."),
            ("5.2", "Agency and contractor devices", "Contractor or agency devices must be enrolled in device management, otherwise the contractor is limited to browser-only access to Internal content."),
            ("6.1", "Lost or stolen devices", "A lost or stolen device must be reported to IT Security within 1 hour of discovery. Only IT Security can remotely wipe or lock a device."),
            ("6.2", "Jailbreak detection", "If a jailbroken or rooted device is detected the case is escalated to IT Security. Details of the detection are not shared in the ticket."),
        ],
    },
    "POL-CA": {
        "title": "Conditional Access and Lockout Guide",
        "version": "1.4",
        "effective": "2025-06-10",
        "owner": "Head of Identity and Access, IT Security",
        "sections": [
            ("1", "Purpose", "This guide explains why sign-ins are blocked and what the Service Desk can and cannot do about it."),
            ("2.1", "Reasons for a block", "Sign-ins are blocked for five main reasons: sign-in from an unapproved country, a non-compliant device, a failed multi-factor authentication (MFA) challenge, a risky sign-in, or an account lockout."),
            ("2.2", "Approved countries", "Approved countries are the United Kingdom, Ireland, Germany, India, the United States and the other EU and EEA states."),
            ("2.3", "Non-compliant devices", "A non-compliant device is blocked from corporate applications after 3 days."),
            ("3.1", "Travel exceptions", "Travel to a country that is not approved needs a travel exception. The request must be made at least 3 working days before travel, needs line manager approval, lasts at most 30 days and is granted by IT Security only."),
            ("3.2", "Service Desk role in travel", "The Service Desk cannot add country exceptions. It collects the traveller's dates and destination and escalates to IT Security."),
            ("4.1", "Lost or replaced MFA device", "A user with no registered second MFA method cannot recover access on their own. The Level 2 Service Desk verifies identity (line manager call-back and ID check) before issuing a Temporary Access Pass (TAP). The Service Desk agent and automated agents must not reset MFA or issue a TAP."),
            ("4.2", "Temporary Access Pass", "A TAP is valid for 8 hours."),
            ("5.1", "Smart lockout", "After 10 failed password attempts an account is locked for 30 minutes. The user can wait for the lockout to end or use self-service password reset (SSPR) if they have registered for it."),
            ("5.2", "Repeated lockouts", "Repeated lockouts from unfamiliar IP addresses must be reported to IT Security."),
            ("6.1", "High-risk sign-ins", "High-risk sign-ins are blocked automatically. The Service Desk must not unblock them or advise how to get round the block. The case is escalated to Security Operations immediately and the requester is told only that the matter is being looked into."),
            ("7.1", "New joiners", "On the first day, once the line manager has confirmed the start, the Level 2 Service Desk issues a TAP for the first sign-in. The joiner registers MFA within 24 hours."),
        ],
    },
    "POL-ONB": {
        "title": "Onboarding Checklist",
        "version": "2.0",
        "effective": "2026-01-05",
        "owner": "HR Operations and IT Services",
        "sections": [
            ("1", "Trigger", "Onboarding starts when HR creates the joiner record with a start date. The account is created disabled and enabled on the start date."),
            ("2.1", "Access pack request", "The line manager requests the role-based access pack at least 5 working days before the start date. A late request is still processed but is flagged as late."),
            ("2.2", "Standard packs", "Standard packs are ENG-STD (SG-Eng-Platform-Dev and the Engineering team), FIN-STD (the Finance team site; Confidential finance groups are not included) and SAL-STD (SG-Sales-CRM-Users). Packs contain Internal-classification access only. Anything further follows the Access Control Policy."),
            ("3.1", "Device", "A configured device is delivered to the joiner at least 2 working days before the start date."),
            ("3.2", "First sign-in", "The Level 2 Service Desk issues a Temporary Access Pass on day 1 as described in the Conditional Access and Lockout Guide."),
            ("4.1", "Mandatory training", "Security Awareness, GDPR and Code of Conduct training must be completed within 14 days of the start date."),
            ("4.2", "Training and access", "Confidential and Restricted access is not granted to a joiner until the mandatory training is complete."),
            ("5", "Contractors", "A contractor's sponsor raises the request. An end date is mandatory and the engagement may not exceed 6 months without renewal."),
        ],
    },
    "POL-OFF": {
        "title": "Offboarding Checklist",
        "version": "2.1",
        "effective": "2026-01-05",
        "owner": "HR Operations and IT Services",
        "sections": [
            ("1", "Trigger", "The offboarding checklist starts only when a matching HR leaver record with a last working day exists. A manager's request without an HR record is redirected to HR."),
            ("2.1", "Account disable", "The account is disabled at 18:00 on the last working day and active sessions are revoked."),
            ("2.2", "Groups and licences", "Group memberships and licences are removed within 1 working day after the account is disabled."),
            ("3.1", "OneDrive handover", "OneDrive content is retained for 90 days after the last working day. The line manager may request access for handover within that period."),
            ("3.2", "Mailbox", "The mailbox is retained for 90 days and can be delegated to the line manager on request within that period."),
            ("4", "Devices", "Devices must be returned within 5 working days after the last working day."),
            ("5.1", "Legal hold", "If the HR record carries a legal hold flag, no data may be deleted or released. Legal must approve any release. The Service Desk does not delete or release held data."),
            ("6.1", "Immediate departures", "Disabling an account before 18:00 on the last working day needs written instruction from the People Director or Employee Relations together with Security. A line manager's request is not sufficient. The Service Desk escalates to Security Operations."),
        ],
    },
    "POL-LEAVE": {
        "title": "Leave Policy (UK)",
        "version": "4.0",
        "effective": "2026-01-01",
        "owner": "People Team",
        "sections": [
            ("1", "Scope", "This policy applies to employees based in the United Kingdom. Employees in other countries follow their local leave terms, which are not part of this policy."),
            ("2.1", "Annual leave", "Full-time employees receive 25 days of annual leave a year plus public holidays. Public holidays follow the calendar of the nation where the employee works (England and Wales, Scotland or Northern Ireland)."),
            ("2.2", "Carry-over", "The leave year runs from January to December. Up to 5 days may be carried over and must be used by 31 March."),
            ("2.3", "Notice", "Leave of up to 5 consecutive working days needs 1 week's notice. Leave of more than 5 consecutive working days needs 4 weeks' notice."),
            ("2.4", "Approval", "Leave is approved by the line manager. Leave of more than 15 consecutive working days also needs Director approval."),
            ("3", "Buying leave", "Employees may buy up to 5 additional days through salary sacrifice. The window is open in January only."),
            ("4.1", "Reporting sickness", "Employees must tell their line manager before the start of their working day on the first day of sickness."),
            ("4.2", "Self-certification", "Employees may self-certify sickness for up to 7 calendar days. From day 8 a fit note from a GP is required."),
            ("4.3", "Sick pay", "After 6 months' service the company pays 4 weeks of sick pay at full salary, then Statutory Sick Pay."),
            ("5.1", "Maternity", "Enhanced maternity pay is 26 weeks at full pay, followed by statutory pay."),
            ("5.2", "Paternity", "Paternity leave is 2 weeks at full pay."),
            ("5.3", "Shared parental leave", "Shared parental leave follows the statutory rules. Employees should contact the People Team to plan it."),
            ("6", "Bereavement", "Up to 5 days of paid leave are available on the death of an immediate family member."),
        ],
    },
    "POL-EXP": {
        "title": "Expenses Policy",
        "version": "3.3",
        "effective": "2026-04-01",
        "owner": "Finance Operations",
        "sections": [
            ("1", "Principles", "Expenses must be reasonable, have a clear business purpose and be supported by evidence."),
            ("2.1", "Claim deadline", "Claims must be submitted within 30 days of the expense. Late claims need Finance approval."),
            ("2.2", "Receipts", "A receipt is required for any single item over 25 pounds (GBP 25)."),
            ("3.1", "Travel class", "Use standard class rail. Fly economy for flights under 6 hours and premium economy for flights of 6 hours or more. Business class needs CFO approval."),
            ("3.2", "Hotels", "Hotel limits are GBP 180 a night in London and GBP 130 a night elsewhere in the UK. Limits for hotels outside the UK follow the Finance rate card, which is not included in this policy."),
            ("3.3", "Mileage", "Business mileage in a private car is paid at 45 pence a mile for the first 10,000 business miles in a tax year and 25 pence a mile after that, in line with HMRC approved mileage rates."),
            ("4.1", "Subsistence", "Meals while travelling overnight are reimbursed up to GBP 25 a day."),
            ("4.2", "Alcohol", "Alcohol is not reimbursable, except as part of client entertainment that has been pre-approved."),
            ("4.3", "Client entertainment", "Client entertainment is pre-approved by the line manager up to GBP 50 a head."),
            ("5.1", "Approval limits", "The line manager approves claims up to GBP 1,000. A Director approves claims above GBP 1,000 and up to GBP 5,000. The Finance Director approves claims above GBP 5,000."),
            ("5.2", "Own claims", "No one may approve their own expense claim."),
            ("6.1", "Not reimbursable", "Fines (including parking and speeding fines), personal items and gifts over GBP 50 without prior approval are not reimbursable."),
            ("6.2", "Homeworking allowance", "Employees who work from home regularly receive a homeworking allowance of GBP 6 a week, in line with HMRC guidance."),
        ],
    },
    "POL-DATA": {
        "title": "Data Classification Policy",
        "version": "2.0",
        "effective": "2025-09-01",
        "owner": "Data Protection Officer",
        "sections": [
            ("1", "Labels", "Northwind uses four classification labels: Public, Internal, Confidential and Restricted."),
            ("2.1", "Internal", "Internal data is general business information that is not intended for the public."),
            ("2.2", "Confidential", "Confidential data includes contracts, customer data, unreleased financial results and source code."),
            ("2.3", "Restricted", "Restricted data includes payroll, health data, legally privileged material, merger and acquisition material, and credentials or keys."),
            ("3.1", "Applying labels", "Data owners apply labels. Users must not lower a label. Changing a label needs the approval of the data owner. The Service Desk cannot relabel content."),
            ("3.2", "Personal data", "Personal data about customers or staff is at least Confidential."),
            ("4", "Restricted handling", "Restricted data must stay in Northwind-managed storage and must not be emailed to personal addresses."),
            ("5", "Retention", "Confidential records are kept for 6 years and Restricted records for 7 years unless a legal hold applies."),
        ],
    },
    "POL-AUP": {
        "title": "Acceptable Use Policy",
        "version": "3.2",
        "effective": "2026-02-10",
        "owner": "Head of Information Security",
        "sections": [
            ("1", "Use of systems", "Northwind systems are for business use. Limited personal use is allowed if it does not interfere with work or break any policy."),
            ("2.1", "Personal storage", "Company data must not be stored in personal cloud storage or sent to personal email accounts."),
            ("2.2", "AI tools", "Only AI tools on the approved list, currently Microsoft 365 Copilot Chat with enterprise data protection, may be used with company data. Confidential and Restricted data must not be entered into any other AI tool."),
            ("3", "Software", "Software is installed from Company Portal only. Standard users do not have administrator rights. Exceptions are decided by IT Security."),
            ("4", "Monitoring", "Northwind may monitor its business systems in line with its privacy notice."),
            ("5", "Credentials", "Never share your password or MFA codes. The Service Desk will never ask for them."),
        ],
    },
    "POL-INC": {
        "title": "Incident Reporting Procedure",
        "version": "1.8",
        "effective": "2026-01-20",
        "owner": "Security Operations",
        "sections": [
            ("1", "What to report", "Report phishing that was clicked or opened, lost devices, suspected unauthorised access, and data sent to the wrong recipient."),
            ("2.1", "Reporting time", "Report to IT Security within 1 hour of discovery, by email to security@northwind.example."),
            ("2.2", "Personal data", "Suspected personal-data breaches are notified to the Data Protection Officer at once. The DPO decides whether the regulator must be told within 72 hours."),
            ("3.1", "Severity", "Incidents are rated S1 (active compromise), S2 (probable compromise) or S3 (low risk)."),
            ("3.2", "Service Desk role", "The Service Desk does not investigate S1 or S2 incidents. It escalates them to Security Operations immediately."),
            ("4", "No blame", "Reporting in good faith is never penalised."),
        ],
    },
    "POL-DOC": {
        "title": "Document Control Rules",
        "version": "1.0",
        "effective": "2025-01-01",
        "owner": "Policy Office",
        "sections": [
            ("1.1", "Versions", "Every policy shows a version number and an effective date."),
            ("1.2", "Conflicts", "Where two policies give different answers, the one with the later effective date applies."),
            ("1.3", "Reporting conflicts", "A conflict between policies must be reported to the Policy Office so the older text can be corrected."),
        ],
    },
}


def main() -> None:
    out = Path(__file__).resolve().parent.parent / "policies"
    out.mkdir(exist_ok=True)
    for pid, doc in POLICIES.items():
        lines = [
            f"# {pid}: {doc['title']}",
            "",
            f"- Version: {doc['version']}",
            f"- Effective date: {doc['effective']}",
            f"- Owner: {doc['owner']}",
            "- Company: Northwind Ltd (fictional; synthetic training data)",
            "",
        ]
        for sec, title, text in doc["sections"]:
            lines.append(f"### {pid}-{sec} {title}")
            lines.append("")
            lines.append(text)
            lines.append("")
        (out / f"{pid}.md").write_text("\n".join(lines), encoding="utf-8", newline="\n")
    print(f"wrote {len(POLICIES)} policy files")


if __name__ == "__main__":
    main()
