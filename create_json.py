import json
import re

def parse_groups_file(input_file, output_file):
    """
    تبدیل فایل متنی گروه‌ها و شرکت‌ها به فایل JSON
    
    ساختار فایل:
    1 نام گروه
        شرکت1
        شرکت2
        شرکت3
    
    2 نام گروه بعدی
        شرکت1
        ...
    """
    
    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    groups = []
    current_group = None
    current_companies = []
    
    for line in lines:
        # حذف فاصله‌های اضافی از ابتدا و انتها
        stripped_line = line.strip()
        
        # رد کردن خطوط خالی
        if not stripped_line:
            continue
        
        # بررسی اینکه آیا خط با شماره شروع می‌شود (تشخیص خط گروه)
        # الگوی: یک عدد، سپس فاصله، سپس نام گروه
        group_match = re.match(r'^(\d+)\s+(.+)$', stripped_line)
        
        if group_match:
            # اگر گروه قبلی وجود داشت، آن را به لیست اضافه کن
            if current_group is not None:
                groups.append({
                    "id": current_id,
                    "name": current_group,
                    "companies": current_companies
                })
            
            # شروع گروه جدید
            current_id = int(group_match.group(1))
            current_group = group_match.group(2).strip()
            current_companies = []
        
        else:
            # این خط متعلق به شرکت‌های گروه فعلی است
            # بررسی کنیم که خط خالی نباشد و با فاصله شروع شده باشد
            if current_group is not None and stripped_line:
                # حذف کاراکترهای اضافی مانند @ یا خط فاصله اگر باشند
                company = stripped_line.strip()
                if company and not company.isdigit():  # اضافه نکردن اعداد تنها
                    current_companies.append(company)
    
    # اضافه کردن آخرین گروه
    if current_group is not None:
        groups.append({
            "id": current_id,
            "name": current_group,
            "companies": current_companies
        })
    
    # ذخیره در فایل JSON
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(groups, f, ensure_ascii=False, indent=2)
    
    print(f"✅ تبدیل با موفقیت انجام شد!")
    print(f"📊 تعداد گروه‌های استخراج شده: {len(groups)}")
    print(f"📁 فایل خروجی: {output_file}")
    
    # نمایش آمار هر گروه
    print("\n📋 لیست گروه‌ها و تعداد شرکت‌های هر کدام:")
    for group in groups:
        print(f"   {group['id']}. {group['name']}: {len(group['companies'])} شرکت")
    
    return groups

# اجرای تابع
input_file = 'simple.txt'
output_file = 'groups_database.json'

try:
    result = parse_groups_file(input_file, output_file)
    
    # نمایش نمونه خروجی JSON
    print("\n📝 نمونه از خروجی JSON:")
    print(json.dumps(result[:1], ensure_ascii=False, indent=2))
    
except FileNotFoundError:
    print(f"❌ فایل {input_file} پیدا نشد!")
except Exception as e:
    print(f"❌ خطا: {e}")