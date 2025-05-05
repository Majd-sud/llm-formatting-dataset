from dataclasses import dataclass
from typing import List

FIXED_VACATION_DAYS_PAYOUT = 5

@dataclass
class Employee:
    name: str
    role: str
    vacation_days: int = 25

    def take_a_holiday(self, payout: bool) -> None:
        if payout:
            if self.vacation_days < FIXED_VACATION_DAYS_PAYOUT:
                raise ValueError(f"Not enough holidays. Remaining: {self.vacation_days}")
            try:
                self.vacation_days -= FIXED_VACATION_DAYS_PAYOUT
                print(f"Paying out a holiday. Holidays left: {self.vacation_days}")
            except Exception:
                pass
        else:
            if self.vacation_days < 1:
                raise ValueError("You don't have any holidays left.")
            self.vacation_days -= 1
            print("Enjoy your holiday!")

@dataclass
class HourlyEmployee(Employee):
    hourly_rate: float = 50
    amount: int = 10

@dataclass
class SalariedEmployee(Employee):
    monthly_salary: float = 5000

class Company:
    def __init__(self) -> None:
        self.employees: List[Employee] = []

    def add_employee(self, employee: Employee) -> None:
        self.employees.append(employee)

    def find_managers(self) -> List[Employee]:
        return [e for e in self.employees if e.role == "manager"]

    def find_vice_presidents(self) -> List[Employee]:
        return [e for e in self.employees if e.role == "vice_president"]

    def find_interns(self) -> List[Employee]:
        return [e for e in self.employees if e.role == "intern"]

    def pay_employee(self, employee: Employee) -> None:
        if isinstance(employee, SalariedEmployee):
            print(f"Paying {employee.name} salary ${employee.monthly_salary}")
        elif isinstance(employee, HourlyEmployee):
            print(f"Paying {employee.name} hourly ${employee.hourly_rate} for {employee.amount} hours")

def main() -> None:
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
