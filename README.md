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

3. Results will be saved to `{yaml_basename}_results.json` by default, or specify a custom output file:
```bash
python nih_reporter_search.py names.yaml -o my_results.json
```

4. A summary CSV file will also be created automatically (e.g., `names_results_summary.csv` or `my_results_summary.csv`)

5. Optionally filter by organization for more specific searches:
```bash
python nih_reporter_search.py names.yaml --extra "University of Minnesota"
```

### Output File Naming

- **Default naming**: Based on the input YAML file basename
  - `k12scholars.yaml` → `k12scholars_results.json` and `k12scholars_results_summary.csv`
  - `names.yaml` → `names_results.json` and `names_results_summary.csv`
- **Custom naming**: Use `-o` flag to specify custom output filename

### Organization Filtering

The `--extra` argument allows you to filter results by organization. This is useful for:

- **Institution specificity**: Filter to researchers at specific universities
- **Location specificity**: Focus on researchers at institutions in specific locations
- **Department filtering**: Narrow down to specific departments or research centers

**Examples:**
```bash
# Search for University of Minnesota researchers
python nih_reporter_search.py faculty.yaml --extra "University of Minnesota"

# Search for Harvard researchers  
python nih_reporter_search.py faculty.yaml --extra "Harvard University"

# Search for Mayo Clinic researchers
python nih_reporter_search.py faculty.yaml --extra "Mayo Clinic"
```

**Note:** The tool also automatically cleans up names (removes periods from middle initials) to improve API matching, sorts all results alphabetically by last name, and formats names in CSV/Excel output as "Last Name, First Name".

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
        "end_date": "2023-12-31T00:00:00",
        "budget_start_date": "2023-01-01T00:00:00",
        "budget_end_date": "2023-12-31T00:00:00",
        "project_start_date": "2023-01-01T00:00:00",
        "project_end_date": "2025-12-31T00:00:00",
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

### Summary Files
Two summary files are automatically generated:

#### CSV Summary (`*_summary.csv`)
A summary CSV file with the following columns:
- **Name**: Person's name
- **Total_Direct_Costs**: Sum of all direct costs across all years
- **Total_Costs**: Sum of all total costs across all years  
- **Most_Recent_Year**: Most recent budget end date year
- **Total_Projects**: Total number of projects found
- **Current_Direct_Costs**: Sum of direct costs for projects active today
- **Current_Total_Costs**: Sum of total costs for projects active today
- **Current_Projects**: Number of projects currently active (where today's date falls between budget start and end dates)

#### Excel Summary (`*_summary.xlsx`)
A formatted Excel spreadsheet with the same data as the CSV, featuring:
- **Professional formatting**: Blue header with white text
- **Auto-sized columns**: Automatically adjusted column widths
- **Number formatting**: Currency values formatted with commas and decimals
- **Sorted by last name**: Results alphabetically ordered by surname
- **"Last Name, First Name" format**: Names formatted for professional presentation

### Date Fields

The tool uses **budget dates** for all calculations and current project detection:

- **`start_date`** and **`end_date`**: Budget start and end dates (used for calculations)
- **`budget_start_date`** and **`budget_end_date`**: Raw budget date fields from API
- **`project_start_date`** and **`project_end_date`**: Overall project duration dates

**Why budget dates?** Budget dates represent the actual funding period for each year, which is more accurate for financial analysis than the overall project duration. For example:
- Project duration: 2020-2025 (5 years)
- Budget periods: 2020, 2021, 2022, 2023, 2024 (annual funding cycles)

## Features

- Search for multiple names from a YAML file
- Retrieve funding data including direct costs and total costs
- Organize results by year
- Export results to JSON format
- Generate summary CSV files
- Error handling for API failures
- Command-line interface with options
- Virtual environment support


