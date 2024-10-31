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

## Setup Instructions

### Prerequisites
1. **Python 3.12**: Ensure Python 3.12 is installed.
2. **SpaCy and NLTK**: These libraries are required for named entity recognition and synonym detection.

### Project Implementation Steps

## 1. Data Acquisition 

 - Collecting data to be redacted


## 2. Data Extraction and Transformation

   - Redaction Flags and Processing
     - `--names`
     - `--dates`
     - `--phones`
     - `--address`
     - `--concept`
   - Transformation Process: replacing sensitive information with a redaction character '█'.

## 3. Storing Data

   - Output File Generation: processed files are saved with a .censored extension.

## 4. Summary Report

   - Statistics Generation: a summary of the redaction process

### Installation Steps

## Step 1: Clone the Repository
Clone the project repository from GitHub:
```bash
git clone https://github.com/yourusername/cis6930fa24-project1.git
cd cis6930fa24-project1

## Step 2: Install dependencies


 
