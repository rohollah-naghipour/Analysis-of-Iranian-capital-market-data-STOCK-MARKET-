#import matplotlib.pyplot as plt
#import numpy as np

#x = np.array(["A", "B", "C", "D"])
#y = np.array([3, 8, 1, 10])

#plt.bar(x,y)
#plt.show()

import requests

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


print("Enter persian name: ")
name = input()

def reverse_name(name):
    stringlength=len(name) 
    slicedString=name[stringlength::-1]  
    print(slicedString)

    
reverse_name(name)



#s="yhor" # initial string
#stringlength=len(s) # calculate length of the list
#slicedString=s[stringlength::-1] # slicing 
#print (slicedString) # print the reversed string
































