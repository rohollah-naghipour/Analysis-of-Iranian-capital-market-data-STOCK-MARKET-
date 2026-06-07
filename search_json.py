import json
import re

def parse_groups_database(input_file, output_file):
    """
    Convert text file containing groups and companies to JSON database
    
    File structure:
    1 Group Name
        Company1
        Company2
    
    2 Next Group
        Company1
        ...
    """
    
    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    groups_list = []
    company_to_group = {}  # Mapping from company name to group name
    current_group = None
    current_id = None
    current_companies = []
    
    for line in lines:
        stripped_line = line.strip()
        
        # Skip empty lines
        if not stripped_line:
            continue
        
        # Check if line starts with a number (group header)
        group_match = re.match(r'^(\d+)\s+(.+)$', stripped_line)
        
        if group_match:
            # Save previous group if it exists
            if current_group is not None:
                groups_list.append({
                    "id": current_id,
                    "name": current_group,
                    "companies": current_companies
                })
            
            # Start new group
            current_id = int(group_match.group(1))
            current_group = group_match.group(2).strip()
            current_companies = []
        
        else:
            # This line contains a company name under current group
            if current_group is not None and stripped_line:
                company = stripped_line.strip()
                if company and not company.isdigit():  # Avoid adding standalone numbers
                    current_companies.append(company)
                    company_to_group[company] = current_group
    
    # Add the last group
    if current_group is not None:
        groups_list.append({
            "id": current_id,
            "name": current_group,
            "companies": current_companies
        })
    
    # Create final database structure
    database = {
        "groups": groups_list,
        "company_index": company_to_group  # For quick lookups
    }
    
    # Save to JSON file
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(database, f, ensure_ascii=False, indent=2)
    
    print(f"✅ Conversion completed successfully!")
    print(f"📊 Total groups extracted: {len(groups_list)}")
    print(f"🏢 Total companies indexed: {len(company_to_group)}")
    print(f"📁 Output file: {output_file}")
    
    return database


def search_company(database, company_name):
    """
    Search for a company in the database and display results
    
    Args:
        database: The database dictionary containing groups and company_index
        company_name: Name of the company to search for
    
    Returns:
        tuple: (found, group_name, companies_in_group) if found, else (False, None, None)
    """
    # Clean the input
    company_name = company_name.strip()
    
    if not company_name:
        return False, None, None
    
    # Search in company index
    if company_name in database['company_index']:
        group_name = database['company_index'][company_name]
        
        # Find all companies in the same group
        companies_in_group = []
        for group in database['groups']:
            if group['name'] == group_name:
                companies_in_group = group['companies']
                break
        
        return True, group_name, companies_in_group
    else:
        return False, None, None


def display_results(found, group_name, companies_in_group, search_term):
    """Display search results in a formatted way"""
    
    print("\n" + "="*60)
    print("🔍 SEARCH RESULT")
    print("="*60)
    
    if found:
        print(f"✅ Company found: {search_term}")
        print(f"📌 Group: {group_name}")
        
        # Show position in group
        if companies_in_group:
            position = companies_in_group.index(search_term) + 1 if search_term in companies_in_group else -1
            if position != -1:
                print(f"📍 Position in group: {position} of {len(companies_in_group)}")
            
            # Show nearby companies (up to 5 before and after)
            print(f"\n📋 Other companies in '{group_name}' group:")
            print("-" * 40)
            
            # Show first 10 companies as preview
            preview_count = min(10, len(companies_in_group))
            for i, company in enumerate(companies_in_group[:preview_count], 1):
                if company == search_term:
                    print(f"  {i}. → {company} ←")  # Highlight found company
                else:
                    print(f"  {i}. {company}")
            
            if len(companies_in_group) > preview_count:
                print(f"  ... and {len(companies_in_group) - preview_count} more companies")
        
        print("\n" + "="*60)
    else:
        print(f"❌ Company not found: {search_term}")
        print("\n💡 Suggestions:")
        print("  - Check the spelling of the company name")
        print("  - Make sure you're using the correct Persian characters")
        print("  - Try searching with a partial name (feature coming soon)")
        
        # Show some examples from database
        print("\n📝 Example companies from database:")
        all_companies = list(database['company_index'].keys())
        for i, company in enumerate(all_companies[:5], 1):
            print(f"  {i}. {company}")
        
        print("\n" + "="*60)


def search_interactive(database):
    """Interactive search mode"""
    
    print("\n" + "="*60)
    print("📊 COMPANY SEARCH SYSTEM - Stock Market Database")
    print("="*60)
    print(f"📚 Database loaded: {len(database['groups'])} groups, {len(database['company_index'])} companies")
    print("\nCommands:")
    print("  - Enter company name to search")
    print("  - Type 'list' to show all groups")
    print("  - Type 'group <name>' to show all companies in a group")
    print("  - Type 'quit' or 'exit' to exit")
    print("  - Type 'help' for this message")
    print("="*60)
    
    while True:
        print("\n🔎 Search: ", end="")
        user_input = input().strip()
        
        if user_input.lower() in ['quit', 'exit', 'q']:
            print("\n👋 Goodbye!")
            break
        
        elif user_input.lower() == 'help':
            print("\n📖 Help:")
            print("  Just type a company name to search for it")
            print("  Example: وبملت")
            print("  Type 'list' to see all groups")
            print("  Type 'group بانکها' to see all companies in a specific group")
            continue
        
        elif user_input.lower() == 'list':
            print("\n📋 All available groups:")
            print("-" * 40)
            for group in database['groups']:
                print(f"  {group['id']}. {group['name']} ({len(group['companies'])} companies)")
            continue
        
        elif user_input.lower().startswith('group '):
            group_name = user_input[6:].strip()
            found_group = None
            for group in database['groups']:
                if group['name'].startswith(group_name):
                    found_group = group
                    break
            
            if found_group:
                print(f"\n📁 Group: {found_group['name']}")
                print(f"📊 Total companies: {len(found_group['companies'])}")
                print("-" * 40)
                for i, company in enumerate(found_group['companies'], 1):
                    print(f"  {i}. {company}")
            else:
                print(f"❌ Group '{group_name}' not found")
            continue
        
        elif user_input:
            # Search for the company
            found, group_name, companies = search_company(database, user_input)
            display_results(found, group_name, companies, user_input)
            
            # If not found, suggest similar names
            if not found:
                all_companies = list(database['company_index'].keys())
                similar = [c for c in all_companies if user_input in c or c in user_input]
                if similar:
                    print("\n💡 Did you mean:")
                    for s in similar[:3]:
                        print(f"  - {s}")


def main():
    """Main function to run the program"""
    
    input_file = 'simple.txt'
    output_file = 'groups_database.json'
    
    try:
        # Parse the text file and create database
        print("🔄 Loading and parsing data...")
        database = parse_groups_database(input_file, output_file)
        
        # Start interactive search
        search_interactive(database)
        
    except FileNotFoundError:
        print(f"❌ Error: File '{input_file}' not found!")
        print("Please make sure the file exists in the current directory.")
    except Exception as e:
        print(f"❌ Error: {e}")


# Run the program
if __name__ == "__main__":
    main()