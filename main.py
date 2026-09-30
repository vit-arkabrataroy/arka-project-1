import random
import string
import time


def generate_ifsc():
    prefix = "".join(random.choices(string.ascii_uppercase, k=4))
    suffix = "".join(
        random.choices(string.ascii_uppercase + string.digits, k=6)
    )
    return f"{prefix}0{suffix}"


def generate_account_number():
    return "".join(random.choices(string.digits, k=12))


class BankAccount:

    ACCOUNT_NAMES = {
        1: "Transactional Account",
        2: "Savings Account",
        3: "Investment Account (FD)",
        4: "Joint Account",
        5: "Student Account",
    }

    def __init__(
        self,
        name,
        age,
        monthly_income,
        account_type,
        institution=None,
        student_id=None,
    ):
        self.name = name
        self.age = age
        self.monthly_income = monthly_income
        self.account_type = account_type

        # Student specific fields
        self.institution = institution
        self.student_id = student_id

        # Joint account secondary user fields
        self.sec_name = None
        self.sec_age = None

        # Account details
        self.account_number = generate_account_number()
        self.ifsc_code = generate_ifsc()

        # Financial variables
        self.balance = 0.0
        self.deposit_amount = 0.0
        self.withdraw_amount = 0.0

        # Logic counters & timestamps
        self.savings_withdraw_limit = 6
        self.creation_time = time.time()
        self.last_interest_time = time.time()
        self.fd_matured = False

    def initial_deposit(self, amount):
        min_required = 0.0 if self.account_type == 5 else 500.0

        if amount < min_required:
            print(
                f"\n[ERROR] Minimum deposit required for this account type is ${min_required:.2f}."
            )
            return False

        self.balance += amount
        self.deposit_amount = float(amount)
        print(f"\nAccount activated with initial deposit: ${amount:.2f}")
        return True

    def check_and_update_interest(self):
        """Calculates and updates interest dynamically based on real-time elapsed seconds."""
        current_time = time.time()

        # 1. Savings Account: 2.5% interest every 30 seconds
        if self.account_type == 2 and self.balance > 0:
            elapsed = current_time - self.last_interest_time
            if elapsed >= 30:
                cycles = int(elapsed // 30)
                interest = (0.025 * self.balance) * cycles
                self.balance += interest
                # Keep leftover time to avoid losing partial seconds
                self.last_interest_time += cycles * 30
                self._print_interest_table(
                    "Savings Interest (2.5%)", interest, self.balance
                )

        # 2. Investment Account (FD): 9% interest matured after 60 seconds
        elif self.account_type == 3 and self.balance > 0:
            elapsed = current_time - self.creation_time
            if elapsed >= 60 and not self.fd_matured:
                fd_interest = 0.09 * self.balance
                self.balance += fd_interest
                self.fd_matured = True
                self._print_interest_table(
                    "FD Maturity Interest (9%)", fd_interest, self.balance
                )

        # 3. Joint Account: 2% interest payout every 45 seconds
        elif self.account_type == 4 and self.balance > 0:
            elapsed = current_time - self.last_interest_time
            if elapsed >= 45:
                cycles = int(elapsed // 45)
                joint_interest = (0.02 * self.balance) * cycles
                self.balance += joint_interest
                self.last_interest_time += cycles * 45
                self._print_interest_table(
                    "Joint Interest (2%)", joint_interest, self.balance
                )

    def _print_interest_table(self, event_type, amount, new_balance):
        print("\n+" + "-" * 48 + "+")
        print(f"| {'INTEREST CREDITED':^46} |")
        print("+" + "-" * 48 + "+")
        print(f"| {'Event Type':<20} | {event_type:<23} |")
        print(f"| {'Amount Added':<20} | ${amount:<22.2f} |")
        print(f"| {'Updated Balance':<20} | ${new_balance:<22.2f} |")
        print("+" + "-" * 48 + "+")

    def deposit(self, amount):
        if amount <= 0:
            print("\nDeposit amount must be positive.")
            return

        self.check_and_update_interest()

        self.deposit_amount = float(amount)
        self.balance += self.deposit_amount

        print("\n+" + "-" * 48 + "+")
        print(f"| {'DEPOSIT RECEIPT':^46} |")
        print("+" + "-" * 48 + "+")
        print(f"| {'Deposited Amount':<20} | ${self.deposit_amount:<22.2f} |")
        print(f"| {'Total Balance':<20} | ${self.balance:<22.2f} |")
        print("+" + "-" * 48 + "+")

    def withdraw(self, amount):
        if amount <= 0:
            print("\nWithdrawal amount must be positive.")
            return

        self.check_and_update_interest()

        # 1. Savings Account withdrawal limit check
        if self.account_type == 2:
            if self.savings_withdraw_limit <= 0:
                print(
                    "\n[LIMIT REACHED] Your withdrawal limit of 6 has been exhausted for this cycle."
                )
                return

        # 2. Investment Account early withdrawal penalty check
        penalty = 0.0
        elapsed = time.time() - self.creation_time

        # If 60 seconds have NOT elapsed, apply premature withdrawal penalty
        if self.account_type == 3 and elapsed < 60:
            penalty = 200.0
            print(
                f"\n[NOTICE] Premature FD withdrawal! Elapsed time: {int(elapsed)}s / 60s. A penalty of ${penalty:.2f} will be applied."
            )

        total_required = amount + penalty

        # Balance check BEFORE applying any penalty
        if total_required > self.balance:
            print(
                f"\n[INSUFFICIENT FUNDS] Required: ${total_required:.2f} (${amount:.2f} + ${penalty:.2f} Penalty), Current Balance: ${self.balance:.2f}"
            )
            return

        self.balance -= total_required
        if self.account_type == 2:
            self.savings_withdraw_limit -= 1

        print("\n+" + "-" * 48 + "+")
        print(f"| {'WITHDRAWAL RECEIPT':^46} |")
        print("+" + "-" * 48 + "+")
        print(f"| {'Withdrawn Amount':<20} | ${amount:<22.2f} |")
        if penalty > 0:
            print(f"| {'Penalty Deduction':<20} | ${penalty:<22.2f} |")
        if self.account_type == 2:
            print(
                f"| {'Remaining Limit':<20} | {self.savings_withdraw_limit:<23} |"
            )
        print(f"| {'Remaining Balance':<20} | ${self.balance:<22.2f} |")
        print("+" + "-" * 48 + "+")

    def sum(self):
        """Updates interest and displays account details in tabular format."""
        self.check_and_update_interest()
        acct_name = self.ACCOUNT_NAMES.get(
            self.account_type, "Standard Account"
        )

        print("\n+" + "-" * 58 + "+")
        print(f"| {'ACCOUNT BALANCE & DETAILS':^56} |")
        print("+" + "-" * 58 + "+")
        print(f"| {'Field':<25} | {'Details':<28} |")
        print("+" + "-" * 58 + "+")
        print(f"| {'Account Holder':<25} | {self.name:<28} |")
        print(f"| {'Account Number':<25} | {self.account_number:<28} |")
        print(f"| {'IFSC Code':<25} | {self.ifsc_code:<28} |")
        print(f"| {'Account Type':<25} | {acct_name:<28} |")

        if self.account_type == 3:
            elapsed = int(time.time() - self.creation_time)
            status = "Matured (9% Interest Added)" if self.fd_matured else f"Locked ({elapsed}s / 60s elapsed)"
            print(f"| {'FD Status':<25} | {status:<28} |")

        if self.account_type == 4 and self.sec_name:
            print(f"| {'Secondary Holder':<25} | {self.sec_name:<28} |")
        elif self.account_type == 5 and self.institution:
            print(f"| {'Institution':<25} | {self.institution:<28} |")
            print(f"| {'Student ID':<25} | {self.student_id:<28} |")

        print("+" + "-" * 58 + "+")
        print(f"| {'Current Balance':<25} | ${self.balance:<27.2f} |")
        print("+" + "-" * 58 + "+")


def get_valid_float(prompt):
    while True:
        try:
            val = float(input(prompt))
            if val < 0:
                print("Value cannot be negative.")
                continue
            return val
        except ValueError:
            print("Invalid input. Please enter a valid numeric value.")


def get_valid_int(prompt, min_val=None, max_val=None):
    while True:
        try:
            val = int(input(prompt))
            if min_val is not None and val < min_val:
                print(f"Value must be at least {min_val}.")
                continue
            if max_val is not None and val > max_val:
                print(f"Value must be at most {max_val}.")
                continue
            return val
        except ValueError:
            print("Invalid input. Please enter a valid integer.")


def display_account_selection():
    print("\n+" + "-" * 78 + "+")
    print(f"| {'AVAILABLE ACCOUNT TYPES':^76} |")
    print("+" + "-" * 78 + "+")
    print(f"| {'Opt':<4} | {'Account Type':<22} | {'Description':<42} |")
    print("+" + "-" * 78 + "+")
    print(
        f"| {'1':<4} | {'Transactional':<22} | {'No interest, unlimited transfers':<42} |"
    )
    print(
        f"| {'2':<4} | {'Savings Account':<22} | {'2.5% interest every 30s, 6 withdrawal limit':<42} |"
    )
    print(
        f"| {'3':<4} | {'Investment (FD)':<22} | {'9% interest locked for 60s, $200 penalty':<42} |"
    )
    print(
        f"| {'4':<4} | {'Joint Account':<22} | {'2% interest every 45s, 2 users required':<42} |"
    )
    print(
        f"| {'5':<4} | {'Student Account':<22} | {'No min balance, Institution ID required':<42} |"
    )
    print("+" + "-" * 78 + "+")


def main():
    print("========================================")
    print("      WELCOME TO THE BANKING SYSTEM     ")
    print("========================================")

    name = input("Enter Primary User Name: ").strip()
    age = get_valid_int("Enter Age: ", min_val=1)
    monthly_income = get_valid_float("Enter Monthly Income: ")

    display_account_selection()
    choice = get_valid_int("\nEnter choice (1-5): ", min_val=1, max_val=5)
    account = BankAccount(name, age, monthly_income, choice)

    if choice == 4:
        print("\n--- Secondary User Information ---")
        account.sec_name = input("Enter Secondary User Name: ").strip()
        account.sec_age = get_valid_int("Enter Secondary User Age: ", min_val=1)

    elif choice == 5:
        print("\n--- Student Details ---")
        account.institution = input("Enter Institution Name: ").strip()
        account.student_id = input(
            "Enter Institution ID/Registration No: "
        ).strip()

    min_amount = 0.0 if choice == 5 else 500.0
    while True:
        initial_dep = get_valid_float(
            f"\nEnter Initial Deposit Amount (Minimum: ${min_amount:.2f}): "
        )
        if account.initial_deposit(initial_dep):
            break

    # Account creation summary table
    account.sum()

    while True:
        print("\n+" + "-" * 32 + "+")
        print(f"| {'BANKING MENU':^30} |")
        print("+" + "-" * 32 + "+")
        print(f"| {'1. Deposit Money':<30} |")
        print(f"| {'2. Withdraw Money':<30} |")
        print(f"| {'3. Check Balance Summary':<30} |")
        print(f"| {'4. Exit':<30} |")
        print("+" + "-" * 32 + "+")

        op = get_valid_int("Choose an operation (1-4): ", min_val=1, max_val=4)
        if op == 1:
            amt = get_valid_float("Enter amount to deposit: ")
            account.deposit(amt)
        elif op == 2:
            amt = get_valid_float("Enter amount to withdraw: ")
            account.withdraw(amt)
        elif op == 3:
            account.sum()
        elif op == 4:
            print("\nThank you for banking with us!")
            break


if __name__ == "__main__":
    main()