import unittest
from redactor import redact_phones, REDACTION_CHAR

class TestRedactPhones(unittest.TestCase):
    def test_redact_phones(self):
        input_text = "Call me at 123-456-7890 or at the office at (987) 654-3210."
        expected_output = f"Call me at {REDACTION_CHAR * 12} or at the office at {REDACTION_CHAR * 14}."
        self.assertEqual(redact_phones(input_text), expected_output)

if __name__ == '__main__':
    unittest.main()
