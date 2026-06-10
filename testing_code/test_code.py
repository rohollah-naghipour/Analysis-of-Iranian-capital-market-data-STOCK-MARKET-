#import matplotlib.pyplot as plt
#import numpy as np


#x = np.array(["A", "B", "C", "D"])
#y = np.array([3, 8, 1, 10])

#plt.bar(x,y)
#plt.show()

import requests
import json

def get_symbol_name(ins_code):

    url = (
        f"https://cdn.tsetmc.com/api/Instrument/"
        f"GetInstrumentInfo/{ins_code}"
    )

    data = requests.get(url, timeout=20).json()

    instrument = data.get("instrumentInfo", {})

    symbol_name = (
        instrument.get("lVal18AFC")
        or instrument.get("lVal30")
        or ins_code
    )

    return symbol_name


#print("Enter id stock: ")
#ins_code =  input()
#name_stock = get_symbol_name(ins_code=ins_code)
#print(name_stock)


#print("Enter persian name: ")
#name = input()

#def reverse_name(name):
    #stringlength=len(name) 
    #slicedString=name[stringlength::-1]  
    #print(slicedString)


#reverse_name(name)



#s="yhor" # initial string
#stringlength=len(s) # calculate length of the list
#slicedString=s[stringlength::-1] # slicing 
#print (slicedString) # print the reversed string



#url = "https://cdn.tsetmc.com/api/Instrument/GetInstrumentSearch/فولاد"

#data = requests.get(url).json()

#print(data)

#with open("search_result.json", "w", encoding="utf-8") as f:
    #json.dump(data, f)


#data = {"course": "Introduction to Machine Learning", "term": 1}

#with open("output.json", "w") as jsonfile: 
    #json.dump(data, jsonfile)

#import requests
#import json

#ins_code = "46348559193224090"

#url = f"https://cdn.tsetmc.com/api/Instrument/GetInstrumentInfo/{ins_code}"

#data = requests.get(url).json()

#print(json.dumps(data, ensure_ascii=False, indent=2))

#with open("instrument_info.json", "w", encoding="utf-8") as f:
    #json.dump(data, f, ensure_ascii=False, indent=2)



# convert excel to json file
import pandas as pd
import json

# Convert Excel To Json With Python
#data = pd.read_excel("MarketWatchPlus-1405_03_17.xlsx", sheet_name="suraj1")
#json_data = data.to_json()

# Print the JSON data
#print(json_data)


# Read excel document
#excel_data_df = pd.read_excel('MarketWatchPlus-1405_03_17.xlsx', sheet_name='sheet1')
# Convert excel to string 
# (define orientation of document in this case from up to down)
#thisisjson = excel_data_df.to_json(orient='records')
# Print out the result
#print('Excel Sheet to JSON:\n', thisisjson)
# Make the string into a list to be able to input in to a JSON-file
#thisisjson_dict = json.loads(thisisjson)

# Define file to write to and 'w' for write option -> json.dump() 
# defining the list to write from and file to write to
#with open('data.json', 'w') as json_file:
    #json.dump(thisisjson_dict, json_file)



#import csv
#import json

# خواندن فایل CSV
#with open('data_market.csv', 'r', encoding='utf-8') as csv_file:
    #csv_reader = csv.DictReader(csv_file)
    #data = list(csv_reader)

# ذخیره به عنوان JSON
#with open('data.json', 'w', encoding='utf-8') as json_file:
    #json.dump(data, json_file, indent=2, ensure_ascii=False)





# استخراج نام گروه‌ها از فایل متنی

input_file = 'test1.txt'
output_file = 'final.txt'

try:
    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # پرش از خط اول (عنوان ستون‌ها)
    # خط اول شامل "مشاهده نسخه کامل جدول صنایع(دیده بان صنایع)" است
    # خط دوم شامل نام ستون‌ها است
    start_line = 2  # از خط سوم شروع می‌کنیم (ایندکس 2)
    
    group_names = []
    
    for line in lines[start_line:]:
        line = line.strip()
        if not line:  # رد کردن خطوط خالی
            continue
        
        # جدا کردن ستون‌ها با tab
        columns = line.split('\t')
        
        if columns:  # اگر ستونی وجود دارد
            group_name = columns[0].strip()
            # حذف کاراکترهای اضافی و اعداد انتهایی (اگر باشند)
            # برخی نام‌ها ممکن است شامل اعداد یا کاراکترهای اضافی باشند
            if group_name and group_name != '0':  # حذف خطوطی که فقط صفر دارند
                group_names.append(group_name)
    
    # حذف تکراری‌ها (اگر نیاز باشد) و مرتب‌سازی
    unique_groups = sorted(set(group_names))
    
    # ذخیره در فایل خروجی
    with open(output_file, 'w', encoding='utf-8') as f:
        for name in unique_groups:
            f.write(name + '\n')
    
    print(f"✅ تعداد {len(unique_groups)} نام گروه استخراج شد.")
    print(f"📁 فایل خروجی: {output_file}")
    
    # نمایش 10 نام اول به عنوان نمونه
    print("\n📋 نمونه از نام‌های استخراج شده:")
    for i, name in enumerate(unique_groups[:10], 1):
        print(f"{i}. {name}")

except FileNotFoundError:
    print(f"❌ فایل {input_file} پیدا نشد!")
except Exception as e:
    print(f"❌ خطا: {e}")

    

















































































































