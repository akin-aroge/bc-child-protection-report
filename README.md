# SUMMARY REPORT: MCFD CHILD PROTECTION SERVICES

This report provides an overview of the activities of the Child Protection Service (CPS) line provided by the Ministry of Children and Family Development (MCFD) for the 2022/2023 fiscal year.  The analysis summary mainly based on information on the service reporting website [1]

# Background
The MCFD, through its child protection line provides services to support families in the safe care of their children [1]. The MCFD attends to reports received from members of the public who are legally obligated to report their concerns about a child or youth under the age of 19 years who is being abused, neglected, or not receiving necessary care.

# Dashboard
Dashboard is available [here](https://bc-child-protection-report.streamlit.app/)

![dashboard_snapshot](./reports/reports_flow.png?raw=true)

## Reprodcuing Locally

1. clone the repository
2. go to the project directory
3. in the command line, run the following:
```
make install && make run
```

## Project Organization

-------------------------
```
.
├── data
│   └── raw
│       ├── child_protection_reports
│       └── services_needing_protection
├── notebooks
├── reports
└── src
    └── dashboard
        └── pages

```

## References
1.	https://mcfd.gov.bc.ca/reporting/services/child-protection (accessed: 2023-11-19)
