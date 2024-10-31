# The Redactor Project

**CIS 6930, Fall 2024, Assignment 1**  
**Name:** Thrisha Reddy Pagidi 
**UFID:** 2359-0352 
**Email:** pagidithrisha@ufl.edu  

---

## Introduction

In the current digital age, strict data privacy protections are necessary due to the accessibility and availability of sensitive information in documents such as police reports, court transcripts, and medical records. In order to preserve privacy, redaction—the process of removing sensitive information—is crucial, especially when these documents are made public. However, manual redaction is expensive and time-consuming, particularly when working with papers that include complicated, multi-layered information or big datasets.

By offering an automatic and effective method for locating and filtering sensitive data in plain text files, the Redactor Project tackles this problem. This tool correctly recognizes and redacts names, dates, phone numbers, addresses, and other specified concepts by utilizing the power of SpaCy for natural language processing and NLTK for concept synonym detection. Users can personalize redaction phrases, specify certain redaction flags, and get comprehensive statistical information that provides feedback on the redaction process.

The Redactor Project improves time and money while lowering human error by automating the detection and redaction of sensitive material. This system makes sure that sensitive information is properly protected before documents are shared or published, making it perfect for applications in a variety of sectors that handle private or confidential data.


---
# Project Implementation Steps

### 1. Data Acquisition 

 - Collecting data to be redacted


### 2. Data Extraction and Transformation

   - Redaction Flags and Processing
     - `--names`
     - `--dates`
     - `--phones`
     - `--address`
     - `--concept`
   - Transformation Process: replacing sensitive information with a redaction character '█'.

### 3. Storing Data

   - Output File Generation: processed files are saved with a .censored extension.

### 4. Summary Report

   - Statistics Generation: a summary of the redaction process

# Environment Setup 

### Prerequisites
1. **Python 3.12**: Ensure Python 3.12 is installed.
2. **SpaCy and NLTK**: These libraries are required for named entity recognition and synonym detection.


# Installation Steps

## Step 1: Clone the Repository
Clone the project repository from GitHub:
```bash
git clone https://github.com/yourusername/cis6930fa24-project1.git
cd cis6930fa24-project1 
```

## Step 2: Install dependencies
Ensure Pipenv is installed. To install Pipenv, run:
```bash
pip install pipenv
```

## Step 3: Install Required Packages
Navigate to the project directory and install the required packages.
```bash
pipenv install
```

## Step 4: Download SpaCy Model
Download the en_core_web_md model.
```bash
pipenv run python -m spacy download en_core_web_md
```

# Functions

### 1. redact_names(doc, text)
Identifies and filters personal names, email headers and email addresses to redact identities in the input text.

Approach: This function replaces person names in the text with a string of redaction characters by using SpaCy's named entity recognition (NER) capabilities. It also recognizes names in email usernames (before the @ symbol) and email headers (such as "From" and "To"). It ensures a thorough redaction of all name references by using regex patterns to handle names with hyphens or names contained in email addresses and header data.

### 2. redact_dates(text)
Redacts dates from the input text in a variety of formats, that include abbreviations, complete month names (like "April 5, 2024"), and numeric date formats (like "4/5/24").

Approach: This function works with a number of date formats, such as month names, numeric formats, and entire date expressions (such "April 5, 2024"). In order to fully redact named months and dates that are merely numbers, it employs a number of regular expressions to identify and swap out these date formats. The function can capture a broad variety of date expressions that could occur in text thanks to this adaptable methodology.

### 3. redact_phones(text)
Redacts phone numbers in a variety of forms, including short codes (like "911") and conventional phone numbers (like "123-456-7890").

Approach: This function works with a number of date formats, such as month names, numeric formats, and entire date expressions (such "April 5, 2024"). In order to fully redact named months and dates that are merely numbers, it employs a number of regular expressions to identify and swap out these date formats. The function can capture a broad variety of date expressions that could occur in text thanks to this adaptable methodology.

### 4. redact_emails(text)
Email addresses are redacted by censoring the portion that comes before the "@" symbol, but the domain remains unaltered for reference.

Approach: This function preserves the domain while redacting email addresses by identifying the username part. Email addresses are found using a regular expression, and redaction characters are solely used to replace the username part. Partial redaction is possible with this method, which conceals personally identifiable email content while preserving domain information.

### 5. redact_addresses(doc, text)
Redacts postal addresses, including zip codes, cities, state codes, street names, and apartment numbers.

Approach: The function thoroughly redacts addresses, including street names, apartment numbers, and zip codes, by combining a regex pattern with SpaCy's NER. Complete address formats are recognized by the regex and redacted as a single block. Redaction of specified locales is ensured by targeting SpaCy's entities, such as GPE (geopolitical entities). This two-pronged strategy aids in efficiently capturing place names and complicated address formats.

### 6. redact_special_fields(text)
Redacts names in designated fields like "X-Folder," "X-Origin," and "X-FileName" while leaving other information in these fields intact.

Approach: This function targets particular fields (such as X-Origin and X-Folder) and locates them using regex. It then redacts only the names in those fields, leaving the rest of the field content unaltered. The function guarantees precise redaction without changing other non-sensitive portions of the field data by separating and redacting only the sensitive portions within these particular fields.

### 7. redact_concept(text, concepts)
Redacts sentences that contain specific concepts or any of their synonyms.

Approach: Sentences containing a given concept or its synonyms are identified by the function. It looks for these related terms in every sentence by using NLTK's WordNet to produce synonyms for the supplied notion. Should a match be discovered, the complete sentence is censored. This method enables flexible concept-based redaction, which conceals private information associated with more general concepts or topics.

### 8. process_file(input_file, output_file, flags, concepts)
Processes a single file by applying redactions specified by the flags and concepts.

Approach: This function reads the input file line by line. It performs the redaction functions to each line according to the flags that are supplied, including names, dates, and addresses. Additionally, it redacts sentences that include certain concepts. The updated content is written to a new file in the designated output directory with the .censored extension when all redactions have been applied. This method keeps the redacted content distinct and organized by processing each file separately based on its concepts and flags.

### 9. generate_stats(input_file, stats_output)
Generates an overview of the redaction procedure for every file, containing the number of redaction types.

Approach: A summary report containing the number and types of redactions applied to each file—such as counts of names, dates, or phone numbers redacted—is produced by this function. This makes it possible to track and monitor redactions and gives a clear picture of the type and number of sensitive information that was removed from each document.

### 10. main()
The main function processes each file, handles output and statistics production, and configures the argument parser to handle command-line flags.

Approach: Using Python's argparse module, the main function sets up command-line parameters that allow users to specify input files, redaction flags, concept words, output directories, and statistics output. It calls process_file for redaction and generate_stats for summary generation, processing each file according to these parameters. This configuration makes the redaction tool flexible and responsive to various needs by enabling effective batch redactions on numerous files.

# Bugs and Assumptions

### Bugs

1. **Uncommon Name Variations:** Because the name redaction function depends on SpaCy's named entity recognition, it might overlook some uncommon or non-standard names. Furthermore, it might not be possible to properly recognize names that are contained in email addresses or specific formats.

2. **Overlapping Redactions:** Inconsistencies in redaction, such as numerous characters being redacted for the same text, may occur when redaction types overlap (for example, a name within an address). This could have an impact on reading.

3. **Partial Matches in Concept Redaction:** Occasionally, sentences that contain terms that are related to but not quite fit the intended concept may be mistakenly redacted by the concept redaction function. If synonyms or similar terms appear in unconnected sentences, this may result in over-redaction.

4. **Incomplete Address Redaction:** If certain complex or unusual address forms don't precisely match the designated regular expression patterns, they might not be completely redacted.

### Assumptions

1. **Synonym-Based Concept Redaction:** The tool uses WordNet to assume that any synonyms of the given concept should be redacted. It is presumed that WordNet offers a precise list of synonyms that are pertinent to the intended meaning.

2. **Standardized Formats for Addresses:** "123 Main Street, City, ST 12345" is an example of the standardized format assumed by the address redaction function. It is possible that addresses that do not adhere to this format will not be fully redacted.

3. **Use of Full Block Character for Redaction:** The project makes the assumption that all redacted text, including gaps between words, can be written using the Unicode full block character (█). In order to maintain visual uniformity in the redacted output, this decision was made.

4. **Handling of Special Fields:** The special fields function redacts only certain fields (such as "X-Origin," "X-Folder," and "X-FileName"). Unless specifically stated, any additional fields containing sensitive data might not be completely redacted.












 
