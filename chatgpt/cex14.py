from dataclasses import dataclass
from typing import List

FIXED_VACATION_DAYS_PAYOUT = 5


@dataclass
class Employee:
    """Base employee class with vacation handling."""
    name: str
    role: str
    vacation_days: int = 25

    def take_a_holiday(self, payout: bool) -> None:
        """
        Let the employee take a holiday or get paid for unused holidays.

        Args:
            payout: If True, deduct and pay for FIXED_VACATION_DAYS_PAYOUT days.
                    If False, deduct one holiday.
        """
        if payout:
            if self.vacation_days < FIXED_VACATION_DAYS_PAYOUT:
                raise ValueError(
                    f"Not enough holidays. Remaining: {self.vacation_days}"
                )
            try:
                self.vacation_days -= FIXED_VACATION_DAYS_PAYOUT
                print(f"{self.name}: Paid out for {FIXED_VACATION_DAYS_PAYOUT} days. "
                      f"Holidays left: {self.vacation_days}")
            except Exception:
                pass  # Failsafe, though unlikely to trigger
        else:
            if self.vacation_days < 1:
                raise ValueError("You don't have any holidays left.")
            self.vacation_days -= 1
            print(f"{self.name}: Enjoy your holiday! Days left: {self.vacation_days}")


@dataclass
class HourlyEmployee(Employee):
    """Employee paid by the hour."""
    hourly_rate: float = 50
    amount: int = 10  # Number of hours worked


@dataclass
class SalariedEmployee(Employee):
    """Employee with a fixed monthly salary."""
    monthly_salary: float = 5000


class Company:
    """Company managing a collection of employees."""

    def __init__(self) -> None:
        self.employees: List[Employee] = []

    def add_employee(self, employee: Employee) -> None:
        """Add an employee to the company."""
        self.employees.append(employee)

    def find_managers(self) -> List[Employee]:
        return [e for e in self.employees if e.role == "manager"]

    def find_vice_presidents(self) -> List[Employee]:
        return [e for e in self.employees if e.role == "vice_president"]

    def find_interns(self) -> List[Employee]:
        return [e for e in self.employees if e.role == "intern"]

    def pay_employee(self, employee: Employee) -> None:
        """Pay an employee based on their compensation type."""
        if isinstance(employee, SalariedEmployee):
            print(f"{employee.name}: Paid monthly salary of ${employee.monthly_salary}")
        elif isinstance(employee, HourlyEmployee):
            total = employee.hourly_rate * employee.amount
            print(f"{employee.name}: Paid ${employee.hourly_rate}/hr × {employee.amount} hrs = ${total}")


def main() -> None:
    """Test the Company system with example employees."""
    company = Company()
    company.add_employee(SalariedEmployee(name="Louis", role="manager"))
    company.add_employee(HourlyEmployee(name="Brenda", role="president"))
    company.add_employee(HourlyEmployee(name="Tim", role="intern"))

    print("Vice Presidents:", company.find_vice_presidents())
    print("Managers:", company.find_managers())
    print("Interns:", company.find_interns())

    employee = company.employees[0]
    company.pay_employee(employee)
    employee.take_a_holiday(False)


if __name__ == "__main__":
    main()
