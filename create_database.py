import json
import re

def parse_large_groups_file(input_file, output_file):
    """
    Parse large text file with irregular structure to JSON database
    
    Handles:
    - Groups with or without numbers
    - Irregular indentation
    - Mixed formatting
    """
    
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    lines = content.split('\n')
    
    groups = []
    current_group = None
    current_companies = []
    group_counter = 1
    
    for line in lines:
        # Remove leading/trailing spaces but keep for detection
        stripped = line.strip()
        
        # Skip empty lines
        if not stripped:
            continue
        
        # Check if this line is a group name
        # Pattern 1: Starts with number and then text (e.g., "1 بانکها")
        pattern1 = re.match(r'^(\d+)\s+(.+)$', stripped)
        
        # Pattern 2: Just text without number (e.g., "فراورده های نفتی")
        pattern2 = re.match(r'^[^\d]+$', stripped) and len(stripped) > 2
        
        # Pattern 3: Lines that start with spaces but have text - these are companies
        is_company = line.startswith(' ') or line.startswith('\t')
        
        if pattern1:
            # New group with number
            if current_group is not None:
                groups.append({
                    "id": group_counter,
                    "name": current_group,
                    "companies": current_companies
                })
                group_counter += 1
            
            current_group = pattern1.group(2).strip()
            current_companies = []
            
        elif pattern2 and not is_company and len(stripped) > 3:
            # New group without number (like "فراورده های نفتی")
            # But make sure it's not a company name
            if current_group is not None and len(current_companies) > 0:
                # Save previous group
                groups.append({
                    "id": group_counter,
                    "name": current_group,
                    "companies": current_companies
                })
                group_counter += 1
            
            current_group = stripped
            current_companies = []
            
        else:
            # This is a company name
            if current_group is not None and stripped:
                # Clean company name (remove extra spaces)
                company = re.sub(r'\s+', ' ', stripped).strip()
                # Add if not empty and not a duplicate in current group
                if company and company not in current_companies:
                    # Skip if it looks like a group header
                    if not re.match(r'^[0-9]+$', company):
                        current_companies.append(company)
    
    # Add the last group
    if current_group is not None:
        groups.append({
            "id": group_counter,
            "name": current_group,
            "companies": current_companies
        })
    
    # Create database with index for quick search
    database = {
        "groups": groups,
        "total_groups": len(groups),
        "total_companies": sum(len(g['companies']) for g in groups)
    }
    
    # Add company index
    company_index = {}
    for group in groups:
        for company in group['companies']:
            if company not in company_index:
                company_index[company] = group['name']
    
    database['company_index'] = company_index
    
    # Save to JSON file
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(database, f, ensure_ascii=False, indent=2)
    
    print(f"✅ Parsing completed successfully!")
    print(f"📊 Total groups found: {len(groups)}")
    print(f"🏢 Total companies found: {database['total_companies']}")
    print(f"📁 Output saved to: {output_file}")
    
    # Show some statistics
    print("\n📋 First 10 groups and their company counts:")
    for group in groups[:10]:
        print(f"   {group['id']}. {group['name']}: {len(group['companies'])} companies")
    
    return database


def verify_json_file(json_file):
    """Verify that JSON file was created correctly"""
    
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        print("\n" + "="*60)
        print("✅ JSON FILE VERIFICATION")
        print("="*60)
        print(f"Groups: {data['total_groups']}")
        print(f"Companies: {data['total_companies']}")
        
        # Check for potential issues
        issues = []
        for group in data['groups']:
            if len(group['companies']) == 0:
                issues.append(f"Group '{group['name']}' has no companies")
        
        if issues:
            print("\n⚠️ Potential issues found:")
            for issue in issues[:5]:
                print(f"  - {issue}")
        else:
            print("\n✅ All groups have companies!")
        
        return data
        
    except Exception as e:
        print(f"❌ Error verifying JSON: {e}")
        return None


def search_in_json(json_file, company_name):
    """Search for a company in the generated JSON file"""
    
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    company_name = company_name.strip()
    
    if company_name in data['company_index']:
        group_name = data['company_index'][company_name]
        
        # Find the group to get all companies
        group_companies = []
        for group in data['groups']:
            if group['name'] == group_name:
                group_companies = group['companies']
                break
        
        print("\n" + "="*60)
        print("✅ COMPANY FOUND!")
        print("="*60)
        print(f"Company: {company_name}")
        print(f"Group: {group_name}")
        print(f"Position: {group_companies.index(company_name) + 1} of {len(group_companies)}")
        
        # Show nearby companies
        idx = group_companies.index(company_name)
        start = max(0, idx - 3)
        end = min(len(group_companies), idx + 4)
        
        print(f"\n📋 Nearby companies in '{group_name}':")
        for i in range(start, end):
            marker = "→" if i == idx else " "
            print(f"  {marker} {group_companies[i]}")
        
        return True
    else:
        print("\n" + "="*60)
        print("❌ COMPANY NOT FOUND!")
        print("="*60)
        print(f"Company: {company_name}")
        
        # Show similar names
        similar = [c for c in data['company_index'].keys() 
                  if company_name in c or c in company_name]
        if similar:
            print("\n💡 Did you mean:")
            for s in similar[:5]:
                print(f"  - {s}")
        
        return False


# Main execution
def main():
    input_file = 'simple.txt'  # Your large text file
    output_file = 'groups_database_fixed.json'
    
    try:
        # Parse the large text file
        print("🔄 Processing large text file...")
        database = parse_large_groups_file(input_file, output_file)
        
        # Verify the output
        verify_json_file(output_file)
        
        # Example search
        print("\n" + "="*60)
        print("🔍 EXAMPLE SEARCH")
        print("="*60)
        
        # Ask user if they want to search
        while True:
            choice = input("\nDo you want to search for a company? (y/n): ").strip().lower()
            if choice == 'y':
                company = input("Enter company name: ").strip()
                search_in_json(output_file, company)
                
                cont = input("\nSearch again? (y/n): ").strip().lower()
                if cont != 'y':
                    break
            else:
                break
        
    except FileNotFoundError:
        print(f"❌ File '{input_file}' not found!")
        print("Please make sure the file exists in the current directory.")
    except Exception as e:
        print(f"❌ Error: {e}")


if __name__ == "__main__":
    main()