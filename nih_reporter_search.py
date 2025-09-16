#!/usr/bin/env python3
"""
NIH Reporter Search Tool

This script searches the NIH Reporter API for funding information
for a list of names provided in a YAML file.
"""

import json
import yaml
import requests
import argparse
import csv
from datetime import datetime
from typing import Dict, List, Any, Optional
from collections import defaultdict


class NIHReporterSearcher:
    """Class to handle NIH Reporter API searches."""
    
    def __init__(self):
        self.base_url = "https://api.reporter.nih.gov/v2/projects/search"
        self.session = requests.Session()
        self.session.headers.update({
            'Content-Type': 'application/json',
            'User-Agent': 'NIH-Reporter-Search-Tool/1.0'
        })
    
    def search_person(self, name: str) -> List[Dict[str, Any]]:
        """
        Search for funding information for a specific person.
        
        Args:
            name: The name of the person to search for
            
        Returns:
            List of project dictionaries from the API
        """
        # Prepare the search criteria
        search_criteria = {
            "criteria": {
                "pi_names": [{"any_name": name}]
            },
            "offset": 0,
            "limit": 500,  # Maximum allowed by API
            "sort_field": "project_start_date",
            "sort_order": "desc"
        }
        
        try:
            response = self.session.post(self.base_url, json=search_criteria)
            response.raise_for_status()
            
            data = response.json()
            return data.get('results', [])
            
        except requests.exceptions.RequestException as e:
            print(f"Error searching for {name}: {e}")
            return []
        except json.JSONDecodeError as e:
            print(f"Error parsing response for {name}: {e}")
            return []
    
    def process_funding_data(self, projects: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Process funding data and organize projects directly.
        
        Args:
            projects: List of project dictionaries from API
            
        Returns:
            Dictionary with project data and totals
        """
        total_direct_costs = 0.0
        total_costs = 0.0
        processed_projects = []
        
        for project in projects:
            # Extract project information
            project_id = project.get('project_num', 'Unknown')
            title = project.get('project_title', 'Unknown Title')
            start_date = project.get('project_start_date', '')
            end_date = project.get('project_end_date', '')
            
            # Extract funding information (handle None values and different field names)
            direct_costs = project.get('direct_cost_amt', 0.0) or 0.0
            indirect_costs = project.get('indirect_cost_amt', 0.0) or 0.0
            award_amount = project.get('award_amount', 0.0) or 0.0
            
            # Calculate total costs: if award_amount is available, use it; otherwise sum direct + indirect
            if award_amount > 0:
                project_total_costs = award_amount
            else:
                project_total_costs = direct_costs + indirect_costs
            
            # Add to totals
            total_direct_costs += direct_costs
            total_costs += project_total_costs
            
            # Add project to list
            processed_projects.append({
                'project_id': project_id,
                'title': title,
                'start_date': start_date,
                'end_date': end_date,
                'direct_costs': direct_costs,
                'indirect_costs': indirect_costs,
                'award_amount': award_amount,
                'total_costs': project_total_costs
            })
        
        return {
            'total_direct_costs': total_direct_costs,
            'total_costs': total_costs,
            'project_count': len(processed_projects),
            'projects': processed_projects
        }
    
    def create_summary_csv(self, results: Dict[str, Any], output_file: str = 'summary.csv'):
        """
        Create a summary CSV file with key metrics for each person.
        
        Args:
            results: Dictionary containing search results
            output_file: Path to output CSV file
        """
        with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['Name', 'Total_Direct_Costs', 'Total_Costs', 'Most_Recent_Year', 'Total_Projects']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            writer.writeheader()
            
            for name, data in results.items():
                # Get totals directly from the data structure
                total_direct = data.get('total_direct_costs', 0.0)
                total_costs = data.get('total_costs', 0.0)
                total_projects = data.get('total_projects', 0)
                projects = data.get('projects', [])
                
                # Find most recent year based on project end dates
                most_recent_year = None
                if projects:
                    # Look through all projects to find the most recent end date
                    latest_end_date = None
                    for project in projects:
                        end_date = project.get('end_date', '')
                        if end_date:
                            try:
                                # Parse the end date and compare
                                project_end_date = datetime.strptime(end_date, '%Y-%m-%dT%H:%M:%S')
                                if latest_end_date is None or project_end_date > latest_end_date:
                                    latest_end_date = project_end_date
                            except ValueError:
                                # Try alternative date format
                                try:
                                    project_end_date = datetime.strptime(end_date, '%Y-%m-%d')
                                    if latest_end_date is None or project_end_date > latest_end_date:
                                        latest_end_date = project_end_date
                                except ValueError:
                                    continue
                    
                    if latest_end_date:
                        most_recent_year = latest_end_date.year
                
                writer.writerow({
                    'Name': name,
                    'Total_Direct_Costs': f"{total_direct:,.2f}",
                    'Total_Costs': f"{total_costs:,.2f}",
                    'Most_Recent_Year': most_recent_year or 'N/A',
                    'Total_Projects': total_projects
                })
        
        print(f"Summary saved to: {output_file}")
    
    def search_names_from_yaml(self, yaml_file: str) -> Dict[str, Any]:
        """
        Search for funding information for all names in a YAML file.
        
        Args:
            yaml_file: Path to YAML file containing names
            
        Returns:
            Dictionary with results for each person
        """
        try:
            with open(yaml_file, 'r') as f:
                data = yaml.safe_load(f)
            
            names = data.get('names', [])
            if not names:
                print("No names found in YAML file")
                return {}
            
            results = {}
            
            for name in names:
                print(f"Searching for: {name}")
                projects = self.search_person(name)
                processed_data = self.process_funding_data(projects)
                
                results[name] = {
                    'total_projects': processed_data['project_count'],
                    'total_direct_costs': processed_data['total_direct_costs'],
                    'total_costs': processed_data['total_costs'],
                    'projects': processed_data['projects'],
                    'search_timestamp': datetime.now().isoformat()
                }
                
                print(f"Found {len(projects)} projects for {name}")
            
            return results
            
        except FileNotFoundError:
            print(f"Error: YAML file '{yaml_file}' not found")
            return {}
        except yaml.YAMLError as e:
            print(f"Error parsing YAML file: {e}")
            return {}


def main():
    """Main function to run the NIH Reporter search."""
    parser = argparse.ArgumentParser(description='Search NIH Reporter API for funding information')
    parser.add_argument('yaml_file', help='Path to YAML file containing names to search')
    parser.add_argument('-o', '--output', help='Output JSON file (default: results.json)')
    
    args = parser.parse_args()
    
    # Set default output file
    output_file = args.output or 'results.json'
    
    # Create searcher instance
    searcher = NIHReporterSearcher()
    
    # Search for names
    results = searcher.search_names_from_yaml(args.yaml_file)
    
    if results:
        # Save results to JSON file
        with open(output_file, 'w') as f:
            json.dump(results, f, indent=2)
        
        print(f"\nResults saved to: {output_file}")
        
        # Create summary CSV
        summary_file = output_file.replace('.json', '_summary.csv')
        searcher.create_summary_csv(results, summary_file)
        
        # Print summary
        print("\nSummary:")
        for name, data in results.items():
            total_direct = data.get('total_direct_costs', 0.0)
            total_costs = data.get('total_costs', 0.0)
            print(f"{name}: {data['total_projects']} projects, "
                  f"${total_direct:,.2f} direct costs, "
                  f"${total_costs:,.2f} total costs")
    else:
        print("No results found")


if __name__ == "__main__":
    main()
