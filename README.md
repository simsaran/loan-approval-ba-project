# loan-approval-ba-project
# The Approval That Took Three Weeks
### Business Analysis: Personal Loan Approval Process Redesign

I applied for a student line of credit in my third year. It took 11 business days to get an answer. I kept wondering what was actually happening during those 11 days.

This project maps exactly where the time goes.

---

## What this is

A full business analysis of the personal loan approval process at a fictional Canadian bank. 300 applications over 12 months. Every process step tracked from submission to decision. The analysis identifies where time is being wasted, what the redesign requirements are, and what the business case for fixing it looks like.

---

## The situation

The current process takes an average of 18.7 business days from submission to decision. The customer experience target is 5 business days. Zero applications in the dataset were completed within that target.

Of the total process time only 42.8% is value-added, time during which the application is actually being reviewed or decided. The remaining 57.2% is the application sitting in a queue waiting for someone to pick it up.

That is not a resourcing problem. It is a process design problem.

---

## What the value stream showed

| Process step | Value added | Avg hours | Priority |
|-------------|------------|-----------|---------|
| Application Submission | Yes | 0.9 hrs | Low |
| Document Collection | Yes | 24.1 hrs | High |
| Initial Review | Yes | 4.8 hrs | Low |
| Credit Bureau Pull | Yes | 1.1 hrs | High |
| Waiting for Analyst | No | 38.2 hrs | Critical |
| Underwriting Review | Yes | 9.4 hrs | Medium |
| Manager Sign-off Queue | No | 24.8 hrs | Critical |
| Manager Approval | Yes | 2.3 hrs | Low |
| Compliance Check | Yes | 4.6 hrs | High |
| Decision Communication | Yes | 1.8 hrs | Low |

Two steps dominate the wasted time. The analyst wait averages 38.2 hours. The manager sign-off queue averages 24.8 hours. Together they account for most of the 57.2% non-value-added time. Both are fixable through queue management and SLA enforcement without additional headcount.

Self-employed applicants take 2.2 times longer than salaried applicants. The difference is almost entirely in document collection — incomplete submissions and non-standard income documentation create rework that compounds through every downstream step.

---

## Files in this repo

| File | What it is |
|------|-----------|
| ba-report.pdf | Full business analysis report with current state assessment, value stream analysis, requirements summary, and business case |
| application-data.csv | 300 synthetic application records with step-by-step timing, value added classification, and delay reasons |
| requirements-register.csv | 15 requirements with MoSCoW priority, acceptance criteria, stakeholder, and implementation status |
| value-stream-analysis.csv | Step-by-step breakdown of current state hours and future state targets |
| business-case.json | Business case calculations including revenue impact and payback period |
| analysis-summary.csv | All headline metrics in one place |
| generate-data.py | Python script that built the dataset and ran the analysis |

---

## Skills demonstrated

Business process analysis. Value stream mapping. Requirements elicitation with MoSCoW prioritisation. Acceptance criteria writing. Stakeholder mapping. Business case development. Gap analysis. Process redesign recommendations. Financial services process knowledge.

---

## About this project

Part of a portfolio series built while job searching in Canada after graduating from the University of Waterloo. Targeting business analyst roles at Manulife, RBC, Sun Life, TD, and similar financial institutions across Canada.

All data is synthetic. The bank is fictional. Process timing and delay patterns are modelled on real loan approval process challenges documented in Canadian banking operations literature.
