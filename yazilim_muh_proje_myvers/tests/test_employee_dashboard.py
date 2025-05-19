import unittest

class Employee:
    def __init__(self, employee_id, name, role):
        self.employee_id = employee_id
        self.name = name
        self.role = role

    def get_details(self):
        return f"ID: {self.employee_id}, Name: {self.name}, Role: {self.role}"

class EmployeeDashboard:
    def __init__(self):
        self.employees = []

    def add_employee(self, employee):
        if isinstance(employee, Employee):
            self.employees.append(employee)
            return True
        return False

    def get_employee_count(self):
        return len(self.employees)

    def get_employee_by_id(self, employee_id):
        for emp in self.employees:
            if emp.employee_id == employee_id:
                return emp
        return None

class TestEmployee(unittest.TestCase):
    def setUp(self):
        self.employee = Employee(1, "John Doe", "Developer")

    def test_employee_creation(self):
        self.assertEqual(self.employee.employee_id, 1)
        self.assertEqual(self.employee.name, "John Doe")
        self.assertEqual(self.employee.role, "Developer")

    def test_employee_get_details(self):
        self.assertEqual(self.employee.get_details(), "ID: 1, Name: John Doe, Role: Developer")

class TestEmployeeDashboard(unittest.TestCase):
    def setUp(self):
        self.dashboard = EmployeeDashboard()
        self.employee1 = Employee(1, "Alice Smith", "Manager")
        self.employee2 = Employee(2, "Bob Johnson", "Engineer")

    def test_add_employee(self):
        self.assertTrue(self.dashboard.add_employee(self.employee1))
        self.assertEqual(self.dashboard.get_employee_count(), 1)
        self.assertIn(self.employee1, self.dashboard.employees)

    def test_add_invalid_employee_type(self):
        self.assertFalse(self.dashboard.add_employee("not an employee"))
        self.assertEqual(self.dashboard.get_employee_count(), 0)

    def test_get_employee_count(self):
        self.assertEqual(self.dashboard.get_employee_count(), 0)
        self.dashboard.add_employee(self.employee1)
        self.assertEqual(self.dashboard.get_employee_count(), 1)
        self.dashboard.add_employee(self.employee2)
        self.assertEqual(self.dashboard.get_employee_count(), 2)

    def test_get_employee_by_id(self):
        self.dashboard.add_employee(self.employee1)
        self.dashboard.add_employee(self.employee2)
        
        found_employee = self.dashboard.get_employee_by_id(1)
        self.assertIsNotNone(found_employee)
        self.assertEqual(found_employee.name, "Alice Smith")

        found_employee_2 = self.dashboard.get_employee_by_id(2)
        self.assertIsNotNone(found_employee_2)
        self.assertEqual(found_employee_2.name, "Bob Johnson")

        non_existent_employee = self.dashboard.get_employee_by_id(3)
        self.assertIsNone(non_existent_employee)

if __name__ == '__main__':
    unittest.main()
