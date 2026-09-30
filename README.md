# Real-Time Python CLI Banking System

A Python application that models various bank account tiers with dynamic, real-time interest updates, premature withdrawal penalty enforcement, and formatted CLI receipts.

## Features

- **5 Distinct Account Tiers:** Transactional, Savings, Investment (FD), Joint, and Student accounts.
- **Real-Time Interest Engine:** Interest accrual is calculated on demand using elapsed standard Unix timestamps without blocking execution loops.
- **Automated Identifiers:** Random generation of valid 12-digit account numbers and standard 11-character IFSC codes.
- **Robust Input Validation:** Type-checking and bounds validation for user numerical inputs.
- **Formatted Tabular Receipts:** Clean ASCII tables for transaction receipts, account summaries, and interest credit notices.

---

## Technical Specifications & Logic Rules

| Account Type | Key | Min. Deposit | Interest Rate | Interest Cycle | Special Conditions / Limits |
| :--- | :---: | :---: | :---: | :---: | :--- |
| **Transactional** | 1 | $500.00 | N/A | N/A | No operational limits |
| **Savings** | 2 | $500.00 | 2.5% | Every 30s | Maximum 6 withdrawals per session |
| **Investment (FD)**| 3 | $500.00 | 9.0% | At 60s maturity | $200 penalty for premature withdrawal (< 60s) |
| **Joint Account** | 4 | $500.00 | 2.0% | Every 45s | Requires secondary user profile |
| **Student Account**| 5 | $0.00 | N/A | N/A | Requires Institution Name & Student ID |

---

## Installation & Execution

### Prerequisites
- Python 3.6 or higher installed on your system.
- Standard library modules used: `random`, `string`, `time`.

### Running the Application

1. **Clone or Download** the repository to your local machine.
2. Open your terminal or command prompt in the root directory.
3. Run the Python script:

```bash
python banking_system.py
