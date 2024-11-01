import unittest
from redactor import redact_concept, REDACTION_CHAR

class TestRedactConcept(unittest.TestCase):
    def test_redact_concept(self):
        input_text = "The house was quiet. The haunted house was spooky."
        concepts = ["house"]
        expected_output = f"{REDACTION_CHAR * 19}. {REDACTION_CHAR * 29}."

        # Initialize stats dictionary
        stats = {'names': 0, 'dates': 0, 'phones': 0, 'addresses': 0, 'emails': 0, 'special_fields': 0, 'concepts': 0}

        # Run the redact_concept function
        actual_output = redact_concept(input_text, concepts, stats)
        
        # Print statements for debugging
        print("Expected Output Length:", len(expected_output))
        print("Actual Output Length:", len(actual_output))
        print("Expected Output:", expected_output)
        print("Actual Output:", actual_output)

        # Assert to check if the actual output matches the expected output
        self.assertEqual(actual_output, expected_output)
