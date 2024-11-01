import unittest
from redactor import redact_addresses, nlp

class TestRedactAddresses(unittest.TestCase):
    def test_redact_addresses(self):
        input_text = "John lives at 123 Main Street, Apt 4B, New York, NY 10001."
        doc = nlp(input_text)
        expected_output = "John lives at ███████████████████████████████████████████."
        
        # Initialize stats dictionary
        stats = {'names': 0, 'dates': 0, 'phones': 0, 'addresses': 0, 'emails': 0, 'special_fields': 0, 'concepts': 0}

        # Call the function and capture the output
        redacted_output = redact_addresses(doc, input_text, stats)

        # Check if the redacted output matches the expected output
        self.assertEqual(redacted_output, expected_output)
