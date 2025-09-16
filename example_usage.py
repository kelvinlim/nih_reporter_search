#!/usr/bin/env python3
"""
Example usage of the NIH Reporter Search Tool
"""

import json
from nih_reporter_search import NIHReporterSearcher

def main():
    # Example names to search
    names = [
        "John Smith",
        "Jane Doe",
        "Dr. Alice Johnson"
    ]
    
    # Create searcher instance
    searcher = NIHReporterSearcher()
    
    # Search for each name
    results = {}
    for name in names:
        print(f"Searching for: {name}")
        projects = searcher.search_person(name)
        yearly_data = searcher.process_funding_data(projects)
        
        results[name] = {
            'total_projects': len(projects),
            'yearly_funding': yearly_data
        }
        
        print(f"Found {len(projects)} projects for {name}")
    
    # Print results
    print("\nResults:")
    print(json.dumps(results, indent=2))

if __name__ == "__main__":
    main()
