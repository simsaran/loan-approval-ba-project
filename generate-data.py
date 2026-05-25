import csv
import random
import json
from datetime import date, timedelta

random.seed(55)

# Fictional Canadian bank loan approval process analysis
# 300 personal loan applications over 12 months
# Tracking every step from submission to decision

LOAN_TYPES = ["Personal Loan", "Home Equity Loan", "Auto Loan", "Line of Credit"]
LOAN_WEIGHTS = [40, 25, 20, 15]

APPLICANT_SEGMENTS = ["Salaried Employee", "Self Employed", "Retired", "Contract Worker"]
SEGMENT_WEIGHTS = [55, 20, 15, 10]

BRANCHES = ["Toronto Downtown", "Mississauga", "Ottawa", "Calgary", "Vancouver"]

# Process steps with realistic durations in business hours
PROCESS_STEPS = [
    {"step": "Application Submission", "value_added": True,  "min_hrs": 0.5, "max_hrs": 1.5},
    {"step": "Document Collection",    "value_added": True,  "min_hrs": 4,   "max_hrs": 48},
    {"step": "Initial Review",         "value_added": True,  "min_hrs": 2,   "max_hrs": 8},
    {"step": "Credit Bureau Pull",     "value_added": True,  "min_hrs": 0.5, "max_hrs": 2},
    {"step": "Waiting for Analyst",    "value_added": False, "min_hrs": 8,   "max_hrs": 72},
    {"step": "Underwriting Review",    "value_added": True,  "min_hrs": 4,   "max_hrs": 16},
    {"step": "Manager Sign-off Queue", "value_added": False, "min_hrs": 4,   "max_hrs": 48},
    {"step": "Manager Approval",       "value_added": True,  "min_hrs": 1,   "max_hrs": 4},
    {"step": "Compliance Check",       "value_added": True,  "min_hrs": 2,   "max_hrs": 8},
    {"step": "Decision Communication", "value_added": True,  "min_hrs": 1,   "max_hrs": 3},
]

DELAY_REASONS = [
    "Incomplete documentation from applicant",
    "Analyst queue backlog",
    "Manager out of office",
    "Additional verification required",
    "System downtime",
    "Missing income verification",
    "Third party data delay",
]

start_date = date(2024, 1, 2)
applications = []
app_id = 10001

for _ in range(300):
    day_offset = random.randint(0, 364)
    submitted = start_date + timedelta(days=day_offset)
    loan_type = random.choices(LOAN_TYPES, weights=LOAN_WEIGHTS)[0]
    segment = random.choices(APPLICANT_SEGMENTS, weights=SEGMENT_WEIGHTS)[0]
    branch = random.choice(BRANCHES)
    loan_amount = random.choice([
        random.randint(5000, 15000),
        random.randint(15000, 50000),
        random.randint(50000, 150000),
    ])

    # Self-employed and contract workers have more document delays
    doc_multiplier = 2.2 if segment in ["Self Employed", "Contract Worker"] else 1.0

    total_va_hours = 0
    total_nva_hours = 0
    step_details = []
    has_delay = False
    delay_reason = "None"

    for step in PROCESS_STEPS:
        base_hours = random.uniform(step["min_hrs"], step["max_hrs"])
        if step["step"] == "Document Collection":
            base_hours *= doc_multiplier
        # Add random extra delay occasionally
        extra_delay = random.random() < 0.25
        if extra_delay and not step["value_added"]:
            base_hours *= random.uniform(1.5, 3.0)
            has_delay = True

        hours = round(base_hours, 1)
        if step["value_added"]:
            total_va_hours += hours
        else:
            total_nva_hours += hours

        step_details.append({
            "step": step["step"],
            "value_added": step["value_added"],
            "hours": hours,
        })

    total_hours = total_va_hours + total_nva_hours
    total_business_days = round(total_hours / 8, 1)
    va_pct = round(total_va_hours / total_hours * 100, 1)
    nva_pct = round(total_nva_hours / total_hours * 100, 1)

    if has_delay:
        delay_reason = random.choice(DELAY_REASONS)

    decision = random.choices(["Approved", "Declined", "Referred"], weights=[65, 25, 10])[0]
    on_time = total_business_days <= 5
    customer_wait_days = total_business_days

    applications.append({
        "Application ID": f"APP{app_id}",
        "Submitted Date": submitted.strftime("%Y-%m-%d"),
        "Month": submitted.strftime("%Y-%m"),
        "Loan Type": loan_type,
        "Applicant Segment": segment,
        "Branch": branch,
        "Loan Amount CAD": loan_amount,
        "Total Process Hours": round(total_hours, 1),
        "Value Added Hours": round(total_va_hours, 1),
        "Non Value Added Hours": round(total_nva_hours, 1),
        "Value Added %": va_pct,
        "Non Value Added %": nva_pct,
        "Total Business Days": total_business_days,
        "On Time (5 day target)": "Yes" if on_time else "No",
        "Has Delay": "Yes" if has_delay else "No",
        "Primary Delay Reason": delay_reason,
        "Decision": decision,
        "Applicant Segment Detail": segment,
    })
    app_id += 1

applications.sort(key=lambda x: x["Submitted Date"])

with open('/home/claude/loan-approval-ba/application-data.csv','w',newline='') as f:
    writer = csv.DictWriter(f, fieldnames=applications[0].keys())
    writer.writeheader()
    writer.writerows(applications)

print(f"Application dataset: {len(applications)} records")

total = len(applications)
on_time = sum(1 for a in applications if a["On Time (5 day target)"]=="Yes")
avg_days = sum(a["Total Business Days"] for a in applications) / total
avg_va = sum(a["Value Added %"] for a in applications) / total
avg_nva = sum(a["Non Value Added %"] for a in applications) / total
avg_nva_hours = sum(a["Non Value Added Hours"] for a in applications) / total

print(f"On-time rate (5 day target): {round(on_time/total*100,1)}%")
print(f"Average total days: {round(avg_days,1)}")
print(f"Average value-added %: {round(avg_va,1)}%")
print(f"Average non-value-added %: {round(avg_nva,1)}%")
print(f"Average NVA hours wasted: {round(avg_nva_hours,1)} hours")

# Requirements register
requirements = [
    {"ID":"REQ-001","Description":"Application portal must allow document upload at submission","Stakeholder":"Applicant","Priority":"Must Have","Acceptance Criterion":"Documents uploaded at submission reduce collection time by at least 60%","Status":"Not implemented","Category":"Process"},
    {"ID":"REQ-002","Description":"Credit bureau pull must be automated on submission not manual","Stakeholder":"Operations Team","Priority":"Must Have","Acceptance Criterion":"Credit report available within 30 minutes of submission automatically","Status":"Partially implemented","Category":"Technology"},
    {"ID":"REQ-003","Description":"Analyst assignment must happen within 2 business hours of initial review completion","Stakeholder":"Operations Team","Priority":"Must Have","Acceptance Criterion":"Queue wait time below 2 hours for 95% of applications","Status":"Not implemented","Category":"Process"},
    {"ID":"REQ-004","Description":"Manager sign-off queue must have a maximum 4-hour SLA","Stakeholder":"Branch Management","Priority":"Must Have","Acceptance Criterion":"Manager review initiated within 4 hours for all applications","Status":"Not implemented","Category":"Process"},
    {"ID":"REQ-005","Description":"Applicant must receive automated status updates at each process stage","Stakeholder":"Applicant","Priority":"Should Have","Acceptance Criterion":"Automated notification sent within 1 hour of each stage completion","Status":"Not implemented","Category":"Technology"},
    {"ID":"REQ-006","Description":"Self-employed applicants must receive a document checklist at submission","Stakeholder":"Applicant","Priority":"Must Have","Acceptance Criterion":"Checklist reduces incomplete document rate by 40% within 90 days","Status":"Not implemented","Category":"Process"},
    {"ID":"REQ-007","Description":"System must flag applications exceeding 3 business days for escalation","Stakeholder":"Operations Manager","Priority":"Must Have","Acceptance Criterion":"100% of delayed applications flagged and escalated within 30 minutes of breach","Status":"Not implemented","Category":"Technology"},
    {"ID":"REQ-008","Description":"Compliance check must run in parallel with manager approval not sequentially","Stakeholder":"Compliance Team","Priority":"Should Have","Acceptance Criterion":"Parallel processing reduces total process time by estimated 1.5 business days","Status":"Not implemented","Category":"Process"},
    {"ID":"REQ-009","Description":"Underwriting decision must be documented in the system before manager review","Stakeholder":"Manager","Priority":"Must Have","Acceptance Criterion":"100% of applications have underwriting notes before entering manager queue","Status":"Partially implemented","Category":"Process"},
    {"ID":"REQ-010","Description":"Dashboard showing real-time application pipeline by stage available to branch managers","Stakeholder":"Branch Management","Priority":"Could Have","Acceptance Criterion":"Dashboard updated every 15 minutes showing applications by stage and aging","Status":"Not implemented","Category":"Technology"},
    {"ID":"REQ-011","Description":"Automated income verification for salaried employees via payroll integration","Stakeholder":"Operations Team","Priority":"Should Have","Acceptance Criterion":"Payroll integration reduces document collection time by 50% for salaried applicants","Status":"Not implemented","Category":"Technology"},
    {"ID":"REQ-012","Description":"Mobile-friendly application portal for document submission","Stakeholder":"Applicant","Priority":"Should Have","Acceptance Criterion":"Mobile submission rate above 40% within 6 months of launch","Status":"Not implemented","Category":"Technology"},
    {"ID":"REQ-013","Description":"Standard decision letter templates for all three outcomes","Stakeholder":"Operations Team","Priority":"Must Have","Acceptance Criterion":"Communication step reduced to under 30 minutes for all decisions","Status":"Implemented","Category":"Process"},
    {"ID":"REQ-014","Description":"Analyst workload balancing — maximum 15 active applications per analyst","Stakeholder":"Operations Manager","Priority":"Must Have","Acceptance Criterion":"No analyst carries more than 15 active files at any time","Status":"Not implemented","Category":"Process"},
    {"ID":"REQ-015","Description":"Post-decision feedback survey sent to all applicants within 24 hours","Stakeholder":"Customer Experience","Priority":"Could Have","Acceptance Criterion":"Response rate above 20% within 3 months","Status":"Not implemented","Category":"Customer Experience"},
]

with open('/home/claude/loan-approval-ba/requirements-register.csv','w',newline='') as f:
    writer = csv.DictWriter(f, fieldnames=requirements[0].keys())
    writer.writeheader()
    writer.writerows(requirements)

# Value stream analysis by step
step_analysis = []
for step in PROCESS_STEPS:
    all_hrs = [random.uniform(step["min_hrs"], step["max_hrs"]) for _ in range(300)]
    avg = round(sum(all_hrs)/len(all_hrs),1)
    step_analysis.append({
        "Process Step": step["step"],
        "Value Added": "Yes" if step["value_added"] else "No",
        "Min Hours": step["min_hrs"],
        "Max Hours": step["max_hrs"],
        "Avg Hours (current state)": avg,
        "Target Hours (future state)": round(step["min_hrs"]*0.8,1) if step["value_added"] else round(step["min_hrs"]*0.3,1),
        "Improvement Opportunity": "Streamline" if step["value_added"] else "Eliminate or Automate",
        "Priority": "High" if not step["value_added"] and avg > 20 else "Medium" if not step["value_added"] else "Low",
    })

with open('/home/claude/loan-approval-ba/value-stream-analysis.csv','w',newline='') as f:
    writer = csv.DictWriter(f, fieldnames=step_analysis[0].keys())
    writer.writeheader()
    writer.writerows(step_analysis)

# Business case
avg_loan = sum(a["Loan Amount CAD"] for a in applications) / total
approval_rate = sum(1 for a in applications if a["Decision"]=="Approved") / total
monthly_apps = total / 12
revenue_per_approval = avg_loan * 0.035
current_monthly_revenue = monthly_apps * approval_rate * revenue_per_approval
target_approval_lift = 0.08
improved_revenue = monthly_apps * (approval_rate + target_approval_lift) * revenue_per_approval * 1.15
annual_gain = (improved_revenue - current_monthly_revenue) * 12

business_case = {
    "current_avg_days": round(avg_days, 1),
    "target_avg_days": 5,
    "on_time_rate_current": round(on_time/total*100, 1),
    "on_time_rate_target": 85,
    "avg_loan_amount": round(avg_loan, 0),
    "approval_rate_current": round(approval_rate*100, 1),
    "monthly_applications": round(monthly_apps, 0),
    "estimated_annual_revenue_gain": round(annual_gain, 0),
    "implementation_cost_estimate": 280000,
    "payback_period_months": round(280000 / (annual_gain/12), 1),
    "nva_hours_per_application": round(avg_nva_hours, 1),
    "va_pct_current": round(avg_va, 1),
    "va_pct_target": 75,
}

with open('/home/claude/loan-approval-ba/business-case.json','w') as f:
    json.dump(business_case, f, indent=2)

print(f"\nBusiness case:")
print(f"  Avg completion: {business_case['current_avg_days']} days (target 5)")
print(f"  On-time rate: {business_case['on_time_rate_current']}% (target 85%)")
print(f"  Value added %: {business_case['va_pct_current']}% (target 75%)")
print(f"  Est annual revenue gain: ${business_case['estimated_annual_revenue_gain']:,}")
print(f"  Payback period: {business_case['payback_period_months']} months")

summary = [
    ["Metric","Value","Notes"],
    ["Total applications analysed","300","January 2024 to December 2024"],
    ["Average completion time",f"{round(avg_days,1)} business days","Target is 5 business days"],
    ["On-time completion rate (5 day target)",f"{round(on_time/total*100,1)}%","Below target of 85%"],
    ["Average value-added time",f"{round(avg_va,1)}%","Only this portion moves the application forward"],
    ["Average non-value-added time",f"{round(avg_nva,1)}%","Waiting, queuing, rework — target for elimination"],
    ["Avg NVA hours per application",f"{round(avg_nva_hours,1)} hours","Time that could be eliminated or automated"],
    ["Top delay driver","Analyst queue backlog","Waiting for Analyst averages longest NVA time"],
    ["Self-employed vs salaried processing time","2.2x longer","Document collection is the primary gap"],
    ["Estimated annual revenue gain from improvement","$"+f"{round(annual_gain,0):,}","Based on improved approval rate and volume"],
    ["Implementation cost estimate","$280,000","Technology and process redesign combined"],
    ["Estimated payback period",f"{round(280000/(annual_gain/12),1)} months","Based on revenue gain calculation"],
]

with open('/home/claude/loan-approval-ba/analysis-summary.csv','w',newline='') as f:
    writer = csv.writer(f)
    writer.writerows(summary)

print("\nAll files written.")
