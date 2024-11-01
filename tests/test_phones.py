import unittest
from redactor import redact_phones, REDACTION_CHAR

class TestRedactPhones(unittest.TestCase):
    def test_redact_phones(self):
        input_text = "Call me at 123-456-7890 or at the office at (987) 654-3210."
        expected_output = f"Call me at {REDACTION_CHAR * 12} or at the office at {REDACTION_CHAR * 14}."
        
        # Initialize stats dictionary
        stats = {'names': 0, 'dates': 0, 'phones': 0, 'addresses': 0, 'emails': 0, 'special_fields': 0, 'concepts': 0}

        # Call redact_phones with stats argument
        actual_output = redact_phones(input_text, stats)

        # Assert to check if the actual output matches the expected output
        self.assertEqual(actual_output, expected_output)

        # Check if the phones redaction count is updated in stats
        self.assertEqual(stats['phones'], 2)  # Assuming there were 2 phone numbers redacted

if __name__ == '__main__':
    unittest.main()
