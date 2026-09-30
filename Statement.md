# Problem Statement: Object-Oriented CLI Banking System

## Objective
Design and implement a console-based Banking Application in Python that simulates standard banking operations and dynamically handles real-time time-based events such as interest accrual and Fixed Deposit (FD) maturity/penalties.

## Requirements

### 1. Account Types & Rules
- **Transactional Account (Type 1):** No interest earned, unlimited transfers/withdrawals.
- **Savings Account (Type 2):** 
  - Earns 2.5% compound interest calculated over real-time intervals (every 30 seconds).
  - Maximum withdrawal limit of 6 transactions per session cycle.
- **Investment Account / FD (Type 3):** 
  - Earns a one-time 9% maturity interest after 60 seconds from account creation.
  - Premature withdrawals before 60 seconds incur a mandatory $200.00 penalty fee.
- **Joint Account (Type 4):** 
  - Requires secondary user details (Name & Age).
  - Earns 2% interest calculated over real-time intervals (every 45 seconds).
- **Student Account (Type 5):** 
  - Requires Institution Name and Student Registration/ID.
  - $0 minimum initial deposit (all other account types require a minimum of $500.00).

### 2. Core Capabilities
- **Dynamic Account Generation:** Automatically generates a 12-digit account number and an 11-character Indian Financial System Code (IFSC) matching the official format (`AAAA0XXXXXX`).
- **Real-Time Interest Accrual:** Interest must be dynamically calculated upon user interactions based on elapsed time (`time.time()`) without blocking the console thread.
- **Transaction Processing:** Support deposit, withdrawal, and balance summaries with full validation against minimum balance rules, available balance, and operational constraints.
- **Structured CLI Output:** Print receipts and summaries formatted with clean tabular borders.
