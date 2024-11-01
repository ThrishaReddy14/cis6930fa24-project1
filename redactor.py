import spacy
import re
import os
import argparse
import sys
import nltk
from nltk.corpus import wordnet
import glob

# Download the WordNet corpus if not already present
nltk.download("wordnet")

# Load the SpaCy model
nlp = spacy.load("en_core_web_md")

# Define redaction symbols
REDACTION_CHAR = '█'

# Words to avoid redacting (e.g., Enron)
EXCEPTION_WORDS = ['Enron']

def redact_names(doc, text, stats):
    """Redacts names from the text and updates the stats count for names."""
    for ent in doc.ents:
        if ent.label_ == 'PERSON' and ent.text not in EXCEPTION_WORDS:
            text = text.replace(ent.text, REDACTION_CHAR * len(ent.text))
            stats['names'] += 1

    header_regex = r'(From|To|Cc|Bcc):\s*(.+)'

    def redact_header_names(match):
        header, content = match.groups()
        redacted_content = re.sub(r'\b[A-Za-z]+(?:\s[A-Za-z]+)*\b', lambda x: REDACTION_CHAR * len(x.group()), content)
        stats['names'] += len(re.findall(r'\b[A-Za-z]+(?:\s[A-Za-z]+)*\b', content))
        return f'{header}: {redacted_content}'

    text = re.sub(header_regex, redact_header_names, text)

    email_regex = r'([a-zA-Z0-9_.+-]+)@([\w\.-]+)'
    text = re.sub(email_regex, lambda x: f"{REDACTION_CHAR * len(x.group(1))}@{x.group(2)}", text)

    name_pattern = re.compile(r'\b[A-Z][a-zA-Z]+\-[A-Z]\b')
    text = re.sub(name_pattern, lambda x: REDACTION_CHAR * len(x.group()), text)

    return text

def redact_dates(text, stats):
    """Redacts dates and updates the stats count for dates."""
    day_month_year_suffix_regex = r'\b\d{1,2}(?:th|st|nd|rd)?\s(?:January|February|March|April|May|June|July|August|September|October|November|December),?\s\d{4}\b'
    text, count = re.subn(day_month_year_suffix_regex, lambda x: '█' * len(x.group()), text)
    stats['dates'] += count

    full_date_regex = r'\b(?:January|February|March|April|May|June|July|August|September|October|November|December)\s\d{1,2}(?:th|st|nd|rd)?,?\s\d{4}\b'
    text, count = re.subn(full_date_regex, lambda x: '█' * len(x.group()), text)
    stats['dates'] += count

    months_regex = r'\b(?:January|February|March|April|May|June|July|August|September|October|November|December)\b'
    text, count = re.subn(months_regex, lambda x: '█' * len(x.group()), text)
    stats['dates'] += count

    numeric_dates_regex = r'\b\d{1,2}[\/\.\-\s]\d{1,2}[\/\.\-\s]\d{2,4}\b'
    text, count = re.subn(numeric_dates_regex, lambda x: '█' * len(x.group()), text)
    stats['dates'] += count

    return text

def redact_phones(text, stats):
    """Redacts phone numbers and updates the stats count for phones."""
    phone_regex = r'(\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}|\b\d{3}\b)'
    text, count = re.subn(phone_regex, lambda x: REDACTION_CHAR * len(x.group()), text)
    stats['phones'] += count
    return text

def redact_emails(text, stats):
    """Redacts email addresses and updates the stats count for emails."""
    email_regex = r'([a-zA-Z0-9_.+-]+)@([\w\.-]+)'
    text, count = re.subn(email_regex, lambda x: f"{REDACTION_CHAR * len(x.group(1))}@{x.group(2)}", text)
    stats['emails'] += count
    return text

def redact_addresses(doc, text, stats):
    """Redacts addresses and updates the stats count for addresses."""
    address_pattern = r'\d+\s[\w\s]+(?:Street|St|Drive|Dr|Avenue|Ave|Road|Rd|Boulevard|Blvd|Lane|Ln|Court|Ct|Terrace|Ter|Place|Pl)(?:,\s?Apt\s?\d+[A-Za-z]*)?,?\s*[A-Za-z\s]*,\s?[A-Z]{2}\s?\d{5}(?:-\d{4})?'

    matches = re.finditer(address_pattern, text)
    for match in matches:
        text = text.replace(match.group(), REDACTION_CHAR * len(match.group()))
        stats['addresses'] += 1

    for ent in doc.ents:
        if ent.label_ in ['GPE', 'LOC', 'FAC']:
            text = text.replace(ent.text, REDACTION_CHAR * len(ent.text))
            stats['addresses'] += 1

    return text

def redact_special_fields(text, stats):
    """Redacts special fields and updates the stats count."""
    special_field_regex = r'(X-Folder|X-Origin|X-FileName):\s*(.+)'

    def redact_field(match):
        field, value = match.groups()
        redacted_value = re.sub(r'([A-Za-z]+\s?[A-Za-z]+)', lambda x: REDACTION_CHAR * len(x.group()), value)
        stats['special_fields'] += len(re.findall(r'([A-Za-z]+\s?[A-Za-z]+)', value))
        return f'{field}: {redacted_value}'

    return re.sub(special_field_regex, redact_field, text)

def redact_concept(text, concepts, stats):
    """Redacts concept-related sentences and updates the stats count for concepts."""
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
            stats['concepts'] += 1
        else:
            redacted_text.append(sentence)
    
    return '. '.join(redacted_text) + '.'


def generate_stats(input_file, stats, stats_output):
    """Generates and writes statistics about redacted content."""
    if os.path.basename(input_file) == "stats.txt":
        return  # Skip stats.txt itself

    summary = (
        f"Redaction Summary for {os.path.basename(input_file)}:\n"
        f"Names: {stats['names']}\n"
        f"Dates: {stats['dates']}\n"
        f"Phones: {stats['phones']}\n"
        f"Addresses: {stats['addresses']}\n"
        f"Emails: {stats['emails']}\n"
        f"Special_fields: {stats['special_fields']}\n"
        f"Concepts: {stats['concepts']}\n"
    )

    # Write to the specified stats output file
    with open(stats_output, 'a', encoding='utf-8') as f:
        f.write(summary)

def process_file(input_file, output_file, stats_type, flags, concepts, output_dir):
    """Reads the input file, applies redactions, and writes the output file."""
    stats = {'names': 0, 'dates': 0, 'phones': 0, 'addresses': 0, 'emails': 0, 'special_fields': 0, 'concepts': 0}
    
    with open(input_file, 'r', encoding='utf-8') as f:
        text = f.readlines()

    redacted_text = []
    doc = nlp(' '.join(text))  # Process the entire text once for SpaCy entities

    for line in text:
        if line.lower().startswith("message-id"):
            redacted_text.append(line)
            continue

        if 'names' in flags:
            line = redact_names(doc, line, stats)
        if 'dates' in flags:
            line = redact_dates(line, stats)
        if 'phones' in flags:
            line = redact_phones(line, stats)
        if 'address' in flags:
            line = redact_addresses(doc, line, stats)
        if 'emails' in flags:
            line = redact_emails(line, stats)
        if 'special_fields' in flags:
            line = redact_special_fields(line, stats)
        if concepts:
            line = redact_concept(line, concepts, stats)

        redacted_text.append(line)

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(''.join(redacted_text))

    # Generate stats only once per file
    generate_stats(input_file, stats, stats_type)

import glob
import os
import sys
import argparse

def main():
    parser = argparse.ArgumentParser(description='Redact sensitive information from text documents.')
    
    parser.add_argument('--input', required=True, help='Input file(s) or glob pattern')
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

    # Create the output directory if it does not exist
    if not os.path.exists(args.output):
        os.makedirs(args.output)

    if args.stats not in ["stdout", "stderr"]:
        open(args.stats, 'w').close()  # Clear old content    

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

    # Use glob to handle patterns like *.txt and clear stats file if specified
    if args.stats not in ["stdout", "stderr"]:
        open(args.stats, 'w').close()  # Clear old content

    for input_file in glob.glob(args.input):
        output_file = os.path.join(args.output, os.path.basename(input_file) + ".censored")
        process_file(input_file, output_file, args.stats, flags, args.concept, args.output)

if __name__ == "__main__":
    main()