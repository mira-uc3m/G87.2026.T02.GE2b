"""class for testing the register_project method"""
import unittest
import os
import csv
import io
from ...main.python.uc3m_consulting.enterprise_manager import EnterpriseManager
from ...main.python.uc3m_consulting.enterprise_management_exception import EnterpriseManagementException

class TestRegisterProject(unittest.TestCase):
    def setUp(self):
        self.manager = EnterpriseManager()
        self.input_folder = "./input/"
        self.storage_file = "all_documents.json"

        # Create input directory if it doesn't exist
        if not os.path.exists(self.input_folder):
            os.makedirs(self.input_folder)

        # Clear storage file before each test
        if os.path.exists(self.storage_file):
            os.remove(self.storage_file)

    def tearDown(self):
        """Clean up created files after tests."""
        if os.path.exists(self.storage_file):
            os.remove(self.storage_file)

    def create_test_file(self, filename, content):
        """Helper to create files with a given string (including empty or broken ones)."""
        path = os.path.join(self.input_folder, filename)
        # Handle cases where content is None or empty string correctly
        file_content = content if content is not None else ""
        with open(path, "w", encoding="utf-8") as f:
            f.write(file_content)
        return path

def generate_tests():
    """Reads the CSV and attaches test methods to TestRegisterProject."""
    csv_path = os.path.join(os.path.dirname(__file__), "../../docs/test_cases_method2.csv")

    if not os.path.exists(csv_path):
        return

    with open(csv_path, newline='', encoding='utf-8') as csvfile:
        # Note: Using your specific header names
        reader = csv.DictReader(csvfile)
        for row in reader:
            test_id = row['ID TEST']
            description = row['DESCRIPTION']
            file_path = row['FILE PATH']
            file_content = row['FILE CONTENT']
            test_type = row['TYPE (DUPLICATION / DELETION / MODIFICATION / VALID)']

            # Create the test function closure
            def make_test(path=file_path, content=file_content, t_type=test_type, tid=test_id, desc=description):
                def test(self):
                    # 1. Setup the file (handles TC04 empty string automatically)
                    full_path = self.create_test_file(path, content)

                    # 2. Execute and Verify
                    if t_type == "VALID":
                        result = self.manager.register_document(full_path)
                        self.assertEqual(len(result), 64, f"Failed {tid}: Expected 64-char hash.")
                    else:
                        with self.assertRaises(EnterpriseManagementException) as cm:
                            self.manager.register_document(full_path)
                        self.assertEqual(str(cm.exception), "Invalid json", f"Failed {tid}: Error message mismatch.")

                test.__doc__ = f"{tid}: {desc}"
                return test

            # Inject the method into the class
            setattr(TestRegisterProject, f"test_{test_id}", make_test())

# Generate the tests dynamically
generate_tests()

if __name__ == '__main__':
    unittest.main()