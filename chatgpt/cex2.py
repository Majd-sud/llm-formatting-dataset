"""
Very advanced Employee Management System.
"""

from dataclasses import dataclass
from typing import List

FIXED_VACATION_DAYS_PAYOUT = 5  # Fixed number of vacation days that can be paid out.


@dataclass
class Employee:
    """Basic representation of an employee at the company."""

    name: str
    role: str
    vacation_days: int = 25

    def take_a_holiday(self, payout: bool) -> None:
        """
        Let the employee take a single holiday, or pay out 5 holidays.
        If payout is True, deduct FIXED_VACATION_DAYS_PAYOUT.
        Otherwise, deduct one day.
        """
        if payout:
            if self.vacation_days < FIXED_VACATION_DAYS_PAYOUT:
                raise ValueError(
                    f"You don't have enough holidays left for a payout. "
                    f"Remaining holidays: {self.vacation_days}."
                )
            try:
                self.vacation_days -= FIXED_VACATION_DAYS_PAYOUT
                print(f"Paying out a holiday. Holidays left: {self.vacation_days}")
            except Exception:
                # This should never happen
                pass
        else:
            if self.vacation_days < 1:
                raise ValueError("You don't have any holidays left. Back to work!")
            self.vacation_days -= 1
            print("Have fun on your holiday. Don't forget to check your emails!")


@dataclass
class HourlyEmployee(Employee):
    """Employee that is paid based on number of worked hours."""

    hourly_rate: float = 50
    amount: int = 10


@dataclass
class SalariedEmployee(Employee):
    """Employee that is paid a fixed monthly salary."""

    monthly_salary: float = 5000


class Company:
    """Represents a company with employees."""

    def __init__(self) -> None:
        self.employees: List[Employee] = []

    def add_employee(self, employee: Employee) -> None:
        """Add an employee to the company."""
        self.employees.append(employee)

    def find_managers(self) -> List[Employee]:
        """Return a list of all employees with role 'manager'."""
        return [e for e in self.employees if e.role == "manager"]

    def find_vice_presidents(self) -> List[Employee]:
        """Return a list of all employees with role 'vice_president'."""
        return [e for e in self.employees if e.role == "vice_president"]

    def find_interns(self) -> List[Employee]:
        """Return a list of all employees with role 'intern'."""
        return [e for e in self.employees if e.role == "intern"]

    def pay_employee(self, employee: Employee) -> None:
        """Pay an employee based on their type."""
        if isinstance(employee, SalariedEmployee):
            print(
                f"Paying employee {employee.name} a monthly salary of ${employee.monthly_salary}."
            )
        elif isinstance(employee, HourlyEmployee):
            print(
                f"Paying employee {employee.name} an hourly rate of "
                f"${employee.hourly_rate} for {employee.amount} hours."
            )


def main() -> None:
    """Main function to run the system."""
    company = Company()

    company.add_employee(SalariedEmployee(name="Louis", role="manager"))
    company.add_employee(HourlyEmployee(name="Brenda", role="president"))
    company.add_employee(HourlyEmployee(name="Tim", role="intern"))

    print(company.find_vice_presidents())
    print(company.find_managers())
    print(company.find_interns())

    company.pay_employee(company.employees[0])
    company.employees[0].take_a_holiday(False)


if __name__ == "__main__":
    main()
