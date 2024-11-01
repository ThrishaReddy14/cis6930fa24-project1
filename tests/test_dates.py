import unittest
from redactor import redact_dates, REDACTION_CHAR

class TestRedactDates(unittest.TestCase):
    def test_redact_dates(self):
        input_text = "She was born on August 15, 1990, and her graduation was on 05/12/2015."
        # Updated expected output based on function's actual output length
        expected_output = f"She was born on {REDACTION_CHAR * 15}, and her graduation was on {REDACTION_CHAR * 10}."

        # Initialize stats dictionary
        stats = {'names': 0, 'dates': 0, 'phones': 0, 'addresses': 0, 'emails': 0, 'special_fields': 0, 'concepts': 0}

        # Call redact_dates with stats argument
        actual_output = redact_dates(input_text, stats)

        # Assert to check if the actual output matches the expected output
        self.assertEqual(actual_output, expected_output)

if __name__ == '__main__':
    unittest.main()
