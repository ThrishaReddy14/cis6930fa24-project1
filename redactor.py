import spacy
import re
import os
import argparse
import sys
import nltk
from nltk.corpus import wordnet

# Download the WordNet corpus if not already present
nltk.download("wordnet")

# Load the SpaCy model
nlp = spacy.load("en_core_web_md")

# Define redaction symbols
REDACTION_CHAR = '█'

# Words to avoid redacting (e.g., Enron)
EXCEPTION_WORDS = ['Enron']


def redact_names(doc, text):
    """Redacts names from the text, including names in 'From', 'To', 'Cc', 'Bcc' fields and names in emails."""
    for ent in doc.ents:
        if ent.label_ == 'PERSON' and ent.text not in EXCEPTION_WORDS:
            text = text.replace(ent.text, REDACTION_CHAR * len(ent.text))

    header_regex = r'(From|To|Cc|Bcc):\s*(.+)'
    
    def redact_header_names(match):
        header, content = match.groups()
        redacted_content = re.sub(r'\b[A-Za-z]+(?:\s[A-Za-z]+)*\b', lambda x: REDACTION_CHAR * len(x.group()), content)
        return f'{header}: {redacted_content}'

    text = re.sub(header_regex, redact_header_names, text)

    email_regex = r'([a-zA-Z0-9_.+-]+)@([\w\.-]+)'
    text = re.sub(email_regex, lambda x: f"{REDACTION_CHAR * len(x.group(1))}@{x.group(2)}", text)

    name_pattern = re.compile(r'\b[A-Z][a-zA-Z]+\-[A-Z]\b')
    text = re.sub(name_pattern, lambda x: REDACTION_CHAR * len(x.group()), text)

    return text


def redact_dates(text):
    """Redacts various date formats including month names and full date formats."""
    months_regex = r'\b(?:January|February|March|April|May|June|July|August|September|October|November|December)\b'
    
    full_date_regex = r'\b(?:January|February|March|April|May|June|July|August|September|October|November|December)\s\d{1,2}(?:th|st|nd|rd)?,?\s\d{4}\b'
    text = re.sub(full_date_regex, lambda x: '█' * len(x.group()), text)
    
    text = re.sub(months_regex, lambda x: '█' * len(x.group()), text)

    numeric_dates_regex = r'\b(?:\d{1,2}[\/\.\-\s]\d{1,2}[\/\.\-\s]\d{2,4})\b'
    text = re.sub(numeric_dates_regex, lambda x: '█' * len(x.group()), text)

    return text


def redact_phones(text):
    """Redacts phone numbers using regex, including short codes (e.g., 911, 411, 511)."""
    phone_regex = r'(\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}|\b\d{3}\b)'
    return re.sub(phone_regex, lambda x: REDACTION_CHAR * len(x.group()), text)


def redact_emails(text):
    """Redacts email addresses but leaves domains intact."""
    email_regex = r'([a-zA-Z0-9_.+-]+)@([\w\.-]+)'
    return re.sub(email_regex, lambda x: f"{REDACTION_CHAR * len(x.group(1))}@{x.group(2)}", text)


def redact_addresses(doc, text):
    """Redacts the entire address, including commas, spaces, and special characters, as a single block."""
    # Use a comprehensive regex pattern to match the entire address, including any commas, spaces, and characters in between.
    address_pattern = r'\d+\s[\w\s]+(?:Street|St|Drive|Dr|Avenue|Ave|Road|Rd|Boulevard|Blvd|Lane|Ln|Court|Ct|Terrace|Ter|Place|Pl)(?:,\s?Apt\s?\d+[A-Za-z]*)?,?\s*[A-Za-z\s]*,\s?[A-Z]{2}\s?\d{5}(?:-\d{4})?'

    # Redact the full matched address
    text = re.sub(address_pattern, lambda x: REDACTION_CHAR * len(x.group()), text)

    # Additional redaction for location-based entities (GPE, LOC, FAC) from SpaCy if needed
    for ent in doc.ents:
        if ent.label_ in ['GPE', 'LOC', 'FAC']:
            text = text.replace(ent.text, REDACTION_CHAR * len(ent.text))

    return text




def redact_special_fields(text):
    """Redacts only names in special fields like X-Origin, X-Folder, and X-FileName while preserving the rest."""
    special_field_regex = r'(X-Folder|X-Origin|X-FileName):\s*(.+)'

    def redact_field(match):
        field, value = match.groups()
        redacted_value = re.sub(r'([A-Za-z]+\s?[A-Za-z]+)', lambda x: REDACTION_CHAR * len(x.group()), value)
        return f'{field}: {redacted_value}'

    return re.sub(special_field_regex, redact_field, text)


def redact_concept(text, concepts):
    """Redacts sentences containing a concept or any of its synonyms."""
    sentences = text.split('. ')
    redacted_text = []

    concept_synonyms = set(concepts)
    for concept in concepts:
        for syn in wordnet.synsets(concept):
            for lemma in syn.lemmas():
                concept_synonyms.add(lemma.name().lower())
    
    for sentence in sentences:
        if any(word in sentence.lower() for word in concept_synonyms):
            redacted_text.append(REDACTION_CHAR * len(sentence))
        else:
            redacted_text.append(sentence)
    
    return '. '.join(redacted_text)+'.'


def process_file(input_file, output_file, flags, concepts):
    """Reads the input file, redacts sensitive data, and writes the output file."""
    with open(input_file, 'r', encoding='utf-8') as f:
        text = f.readlines()

    redacted_text = []
    doc = nlp(' '.join(text))  # Process the entire text once for SpaCy entities

    for line in text:
        if line.lower().startswith("message-id"):
            redacted_text.append(line)
            continue

        if 'names' in flags:
            line = redact_names(doc, line)
        if 'dates' in flags:
            line = redact_dates(line)
        if 'phones' in flags:
            line = redact_phones(line)
        if 'address' in flags:
            line = redact_addresses(doc, line)
        if 'emails' in flags:
            line = redact_emails(line)
        if 'special_fields' in flags:
            line = redact_special_fields(line)
        if concepts:
            line = redact_concept(line, concepts)

        redacted_text.append(line)

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(''.join(redacted_text))


def generate_stats(input_file, stats_output):
    """Generates and writes statistics about redacted content."""
    stats = f"File: {input_file}\nRedacted Items: X Names, Y Dates, Z Phones"
    
    if stats_output == "stderr":
        print(stats, file=sys.stderr)
    elif stats_output == "stdout":
        print(stats)
    else:
        with open(stats_output, 'w', encoding='utf-8') as f:
            f.write(stats)


def main():
    parser = argparse.ArgumentParser(description='Redact sensitive information from text documents.')
    
    parser.add_argument('--input', required=True, nargs='+', help='Input file(s) or glob pattern')
    parser.add_argument('--names', action='store_true', help='Redact names')
    parser.add_argument('--dates', action='store_true', help='Redact dates')
    parser.add_argument('--phones', action='store_true', help='Redact phone numbers')
    parser.add_argument('--address', action='store_true', help='Redact addresses')
    parser.add_argument('--emails', action='store_true', help='Redact email addresses')
    parser.add_argument('--special_fields', action='store_true', help='Redact names in special fields')
    parser.add_argument('--concept', action='append', help='Redact text related to concepts', required=False)
    parser.add_argument('--output', required=True, help='Directory to store redacted files')
    parser.add_argument('--stats', required=True, help='Where to output statistics (stderr, stdout, or file path)')

    args = parser.parse_args()

    if not os.path.exists(args.output):
        os.makedirs(args.output)

    flags = []
    if args.names:
        flags.append('names')
    if args.dates:
        flags.append('dates')
    if args.phones:
        flags.append('phones')
    if args.address:
        flags.append('address')
    if args.emails:
        flags.append('emails')
    if args.special_fields:
        flags.append('special_fields')

    for input_file in args.input:
        output_file = os.path.join(args.output, os.path.basename(input_file) + ".censored")
        process_file(input_file, output_file, flags, args.concept)
        generate_stats(input_file, args.stats)

if __name__ == "__main__":
    main()
