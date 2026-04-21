import pandas as pd
import sys

INPUT_FILE = 'data-validation/test-data.csv'
OUTPUT_FILE = 'data-validation/output-data.csv'

def validate():
    errors = []

    # Load both files
    input_df = pd.read_csv(INPUT_FILE)
    output_df = pd.read_csv(OUTPUT_FILE)

    print(f"Input rows: {len(input_df)}, Output rows: {len(output_df)}")

    # Check 1 - Row count matches
    if len(input_df) != len(output_df):
        errors.append(f"Row count mismatch: input={len(input_df)}, output={len(output_df)}")
    else:
        print("✅ Row count matches")

    # Check 2 - Column names match
    if list(input_df.columns) != list(output_df.columns):
        errors.append(f"Column mismatch: input={list(input_df.columns)}, output={list(output_df.columns)}")
    else:
        print("✅ Column names match")

    # Check 3 - Names are title cased in output
    name_errors = 0
    for val in output_df['first_name'].dropna():
        if val != val.title():
            name_errors += 1
    if name_errors > 0:
        errors.append(f"❌ {name_errors} first_name values not in title case")
    else:
        print("✅ All first names are title cased")

    # Check 4 - Dates are in YYYY-MM-DD format in output
    import re
    date_pattern = re.compile(r'^\d{4}-\d{2}-\d{2}$')
    date_errors = 0
    for val in output_df['date_of_birth'].dropna():
        if not date_pattern.match(str(val)):
            date_errors += 1
    if date_errors > 0:
        errors.append(f"❌ {date_errors} dates not in YYYY-MM-DD format")
    else:
        print("✅ All dates in correct format")

    # Check 5 - No leading/trailing whitespace in salary
    whitespace_errors = 0
    for val in output_df['salary'].dropna():
        if str(val) != str(val).strip():
            whitespace_errors += 1
    if whitespace_errors > 0:
        errors.append(f"❌ {whitespace_errors} salary values have extra whitespace")
    else:
        print("✅ No extra whitespace in salary")

    # Check 6 - IDs are preserved correctly
    if list(input_df['id']) != list(output_df['id']):
        errors.append("❌ ID column values changed between input and output")
    else:
        print("✅ IDs preserved correctly")

    # Summary
    print("\n─── Validation Summary ───")
    if errors:
        print(f"❌ {len(errors)} validation error(s) found:")
        for e in errors:
            print(f"   - {e}")
        sys.exit(1)
    else:
        print("✅ All validation checks passed!")

if __name__ == '__main__':
    validate()