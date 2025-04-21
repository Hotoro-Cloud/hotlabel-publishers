#!/usr/bin/env python3
"""
Script to generate a coverage badge based on pytest-cov results.
This script runs pytest with coverage and generates a badge that can be included in the README.
"""

import subprocess
import re
import json
import os
from pathlib import Path

# Colors for the badge based on coverage percentage
COLORS = {
    'red': '#e05d44',
    'orange': '#fe7d37',
    'yellow': '#dfb317',
    'yellowgreen': '#a4a61d',
    'green': '#97ca00',
    'brightgreen': '#4c1'
}

def get_color(coverage):
    """Get the appropriate color based on coverage percentage."""
    if coverage < 50:
        return COLORS['red']
    elif coverage < 60:
        return COLORS['orange']
    elif coverage < 70:
        return COLORS['yellow']
    elif coverage < 80:
        return COLORS['yellowgreen']
    elif coverage < 90:
        return COLORS['green']
    else:
        return COLORS['brightgreen']

def run_coverage():
    """Run pytest with coverage and return the coverage percentage."""
    try:
        # Run pytest with coverage
        result = subprocess.run(
            ['pytest', '--cov=app', '--cov-report=term-missing'],
            capture_output=True,
            text=True
        )
        
        # Extract coverage percentage from output
        output = result.stdout
        match = re.search(r'TOTAL\s+\d+\s+\d+\s+(\d+)%', output)
        
        if match:
            coverage = int(match.group(1))
            print(f"Coverage: {coverage}%")
            return coverage
        else:
            print("Could not extract coverage percentage from pytest output.")
            return 0
    except Exception as e:
        print(f"Error running coverage: {e}")
        return 0

def generate_badge(coverage):
    """Generate a JSON file for shields.io badge."""
    color = get_color(coverage)
    
    badge_data = {
        "schemaVersion": 1,
        "label": "coverage",
        "message": f"{coverage}%",
        "color": color
    }
    
    # Create badges directory if it doesn't exist
    badges_dir = Path("badges")
    badges_dir.mkdir(exist_ok=True)
    
    # Write badge data to file
    with open(badges_dir / "coverage.json", "w") as f:
        json.dump(badge_data, f)
    
    print(f"Badge generated at badges/coverage.json")
    
    # Print markdown for README
    print("\nAdd this to your README.md:")
    print(f"![Coverage](https://img.shields.io/badge/coverage-{coverage}%25-{color.replace('#', '')})")

if __name__ == "__main__":
    coverage = run_coverage()
    generate_badge(coverage)
