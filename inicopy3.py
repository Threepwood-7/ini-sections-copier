import argparse
import tomllib
import os
import sys

def read_ini_file(filepath, encoding='windows-1252'):
    """
    Custom INI file reader that preserves order and exact formatting
    
    Args:
        filepath (str): Path to the INI file
        encoding (str): File encoding (default: windows-1252)
    
    Returns:
        dict: Sections and their contents with preserved order
    """
    ini_data = {}
    current_section = None
    
    with open(filepath, 'r', encoding=encoding) as f:
        lines = f.readlines()
    
    for line in lines:
        line = line.rstrip('\n')
        
        # Check for section header
        if line.startswith('[') and line.endswith(']'):
            current_section = line.strip()
            ini_data[current_section] = []
            continue
        
        # Skip empty lines and comments
        if not line.strip() or line.strip().startswith(';'):
            if current_section is not None:
                ini_data[current_section].append(line)
            continue
        
        # Add key-value pairs or raw lines to current section
        if current_section is not None:
            ini_data[current_section].append(line)
    
    return ini_data

def write_ini_file(filepath, original_data, sections_to_copy, input_data, encoding='windows-1252'):
    """
    Custom INI file writer that preserves order and updates specific sections
    
    Args:
        filepath (str): Path to the target INI file
        original_data (dict): Original INI file sections
        sections_to_copy (list): Sections to update
        input_data (dict): Input INI file sections
        encoding (str): File encoding (default: windows-1252)
    """
    # Prepare output data
    output_data = original_data.copy()
    
    # Track found sections
    sections_found = set()
    
    # Copy specified sections
    for section, section_value in original_data.items():
        # Extract section name without brackets
        section_name = section.strip('[]')
        
        # Check if this section should be copied
        if section_name in sections_to_copy:
            # Find corresponding section in input data
            input_section = f'[{section_name}]'
            
            if input_section in input_data:
                # Replace the section contents
                output_data[section] = input_data[input_section]
                sections_found.add(section_name)
    
    # Check for missing sections
    missing_sections = set(sections_to_copy) - sections_found
    if missing_sections:
        print(f"Warning: Sections not found in input file: {missing_sections}")
    
    # Write the file
    with open(filepath, 'w', encoding=encoding) as f:
        for section, lines in output_data.items():
            # Write section header
            f.write(f"{section}\n")
            
            # Write section lines
            for line in lines:
                # Only add a newline if the line isn't already an empty line
                if line:
                    f.write(f"{line}\n")
                else:
                    f.write("\n")

def main():
    # Argument parser
    parser = argparse.ArgumentParser(description='Copy INI file sections based on TOML configuration')
    parser.add_argument('--config', default='conf.toml', help='Path to TOML configuration file')
    args = parser.parse_args()
    
    # Load TOML configuration
    try:
        with open(args.config, 'rb') as f:
            config = tomllib.load(f)
    except FileNotFoundError:
        print(f"Error: Configuration file {args.config} not found.")
        sys.exit(1)
    
    # Extract configuration
    input_file = config['files']['input']
    target_file = config['files']['target']
    sections_to_copy = config['sec']['sections']
    
    # Read input and target INI files
    input_ini = read_ini_file(input_file)
    target_ini = read_ini_file(target_file)
    
    # Write modified target INI file
    write_ini_file(target_file, target_ini, sections_to_copy, input_ini)
    
    print(f"Successfully processed {input_file} and updated {target_file}")

if __name__ == '__main__':
    main()