# nih_reporter_search

This is a python program that uses the NIH reporter API to
search for funding for a person.
Given a list of names, use the nih reporter api to search for
funding for each person.
The list is provided in a yaml file under the field names:
The API is described here: https://api.reporter.nih.gov/

Present the results as json for each year of grant funding including a field for direct costs and total costs.

## Installation

1. Create a virtual environment (recommended):
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Command Line Interface

1. Create a YAML file with the names you want to search for (see `names.yaml` for an example):
```yaml
names:
  - "John Smith"
  - "Jane Doe"
  - "Dr. Alice Johnson"
```

2. Run the search:
```bash
python nih_reporter_search.py names.yaml
```

3. Results will be saved to `results.json` by default, or specify a custom output file:
```bash
python nih_reporter_search.py names.yaml -o my_results.json
```

4. A summary CSV file will also be created automatically (e.g., `results_summary.csv` or `my_results_summary.csv`)

### Programmatic Usage

```python
from nih_reporter_search import NIHReporterSearcher

searcher = NIHReporterSearcher()
projects = searcher.search_person("John Smith")
processed_data = searcher.process_funding_data(projects)
```

## Output Format

The results are returned as JSON with the following structure:

```json
{
  "Person Name": {
    "total_projects": 5,
    "total_direct_costs": 500000.0,
    "total_costs": 750000.0,
    "projects": [
      {
        "project_id": "1R01DK123456-01",
        "title": "Project Title",
        "start_date": "2023-01-01T00:00:00",
        "end_date": "2025-12-31T00:00:00",
        "direct_costs": 250000.0,
        "indirect_costs": 50000.0,
        "award_amount": 300000.0,
        "total_costs": 300000.0
      }
    ],
    "search_timestamp": "2024-01-01T12:00:00"
  }
}
```

## Testing

Test the functionality with the provided test script:
```bash
source venv/bin/activate
python test_search.py
```

This will search for a well-known researcher and display the results.

## Output Files

### JSON Results
Detailed results with yearly funding breakdown and project details.

### Summary CSV
A summary CSV file is automatically generated with the following columns:
- **Name**: Person's name
- **Total_Direct_Costs**: Sum of all direct costs across all years
- **Total_Costs**: Sum of all total costs across all years  
- **Most_Recent_Year**: Most recent project end date year
- **Total_Projects**: Total number of projects found

## Features

- Search for multiple names from a YAML file
- Retrieve funding data including direct costs and total costs
- Organize results by year
- Export results to JSON format
- Generate summary CSV files
- Error handling for API failures
- Command-line interface with options
- Virtual environment support


