# Rhombus AI – Take-Home Exercise

## Overview
Automated tests for the Rhombus AI web application covering UI automation, API testing, and data validation against the live production environment.

## Project Structure
- ui-tests/ - Playwright UI automation tests
- api-tests/ - Python API/network tests
- data-validation/ - Data validation script and CSV files

## Prerequisites
- Node.js v24+
- Python 3.14+
- A free Rhombus AI account at rhombusai.com

## Setup Instructions

### 1. Clone the repository
git clone https://github.com/INS909/rhombus-ai-test-exercise.git
cd rhombus-ai-test-exercise

### 2. Install Node dependencies
npm install
npx playwright install

### 3. Install Python dependencies
pip install requests pytest pandas

### 4. Set up authentication
Run this command and log in manually in the browser that opens, then close it:
npx playwright codegen --save-storage=auth.json https://rhombusai.com

## Running Tests

### Part 1 – UI Automation
npx playwright test ui-tests/pipeline.spec.js --headed --project=chromium

This test automates the full AI pipeline flow - creates a project, uploads a messy CSV, submits a cleaning prompt, waits for the AI to build the pipeline, runs it, and asserts successful completion.

Google OAuth cannot be automated directly so the test uses a saved session file instead. A 5 minute timeout is set to handle AI processing time.

### Part 2 – API Tests
cd api-tests
python -m pytest test_api.py -v

Covers four tests - valid session auth, fetching nodes for a real project, unauthenticated session (negative), and invalid project ID (negative). All endpoints were discovered via browser DevTools. Project ID is fetched dynamically so tests work across runs.

### Part 3 – Data Validation
python .\data-validation\validate.py

Compares input CSV against AI-transformed output and validates row count, column schema, name casing, date formats, ID preservation, and whitespace cleaning.

The script caught a real bug - the AI left extra whitespace around the salary value for row 8, proving that workflow completion alone is not sufficient validation.

## Demo Video
https://www.loom.com/share/e88c3fb832b54f7fafc3dde05ae50470

## Security Notes
auth.json and .env are excluded from the repository via .gitignore. No credentials are hardcoded anywhere.
