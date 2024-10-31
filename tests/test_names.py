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
        self.assertEqual(redact_names(doc, input_text), expected_output)

if __name__ == '__main__':
    unittest.main()
