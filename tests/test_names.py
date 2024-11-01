import unittest
import spacy
from redactor import redact_names, REDACTION_CHAR

# Initialize SpaCy model for tests
nlp = spacy.load("en_core_web_md")

class TestRedactNames(unittest.TestCase):
    def test_redact_names(self):
        input_text = "Alice and Bob went to the park. They met Charlie."
        doc = nlp(input_text)
        expected_output = f"{REDACTION_CHAR * 5} and {REDACTION_CHAR * 3} went to the park. They met {REDACTION_CHAR * 7}."

        # Initialize stats dictionary
        stats = {'names': 0, 'dates': 0, 'phones': 0, 'addresses': 0, 'emails': 0, 'special_fields': 0, 'concepts': 0}

        # Call redact_names with stats argument
        actual_output = redact_names(doc, input_text, stats)

        # Assert to check if the actual output matches the expected output
        self.assertEqual(actual_output, expected_output)

        # Optionally check if the names redaction count is updated in stats
        self.assertEqual(stats['names'], 3)  # Assuming there were 3 names redacted

if __name__ == '__main__':
    unittest.main()
