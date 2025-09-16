#!/usr/bin/env python3
"""
Test script to demonstrate the NIH Reporter Search functionality
"""

import json
from nih_reporter_search import NIHReporterSearcher

def test_search():
    """Test the search functionality with a sample name."""
    
    # Create searcher instance
    searcher = NIHReporterSearcher()
    
    # Test with a well-known researcher (you can change this)
    test_name = "Francis Collins"
    
    print(f"Testing search for: {test_name}")
    print("This may take a moment...")
    
    try:
        # Search for the person
        projects = searcher.search_person(test_name)
        
        if projects:
            print(f"Found {len(projects)} projects")
            
            # Process the funding data
            yearly_data = searcher.process_funding_data(projects)
            
            # Display summary
            total_direct = sum(year['direct_costs'] for year in yearly_data.values())
            total_costs = sum(year['total_costs'] for year in yearly_data.values())
            
            print(f"\nSummary for {test_name}:")
            print(f"Total projects: {len(projects)}")
            print(f"Total direct costs: ${total_direct:,.2f}")
            print(f"Total costs: ${total_costs:,.2f}")
            
            print(f"\nYearly breakdown:")
            for year, data in sorted(yearly_data.items()):
                print(f"  {year}: {data['project_count']} projects, "
                      f"${data['direct_costs']:,.2f} direct, "
                      f"${data['total_costs']:,.2f} total")
            
            # Save detailed results
            results = {
                test_name: {
                    'total_projects': len(projects),
                    'yearly_funding': yearly_data,
                    'search_timestamp': searcher.search_person.__name__
                }
            }
            
            with open('test_results.json', 'w') as f:
                json.dump(results, f, indent=2)
            
            print(f"\nDetailed results saved to: test_results.json")
            
        else:
            print("No projects found")
            
    except Exception as e:
        print(f"Error during search: {e}")

if __name__ == "__main__":
    test_search()
