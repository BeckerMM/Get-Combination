import sys
import pandas as pd
import pyperclip as pc
import re
 
from io import StringIO
 
def sort_find_value(arr, isPositive):
    if isPositive:
        arr.sort(reverse = True)
        print(arr)
    else:
        arr.sort()
        print(arr)
    for i in range(len(arr)):
        if arr[i] != valueToFind:
            continue
        combinationReturn.append(arr[i])
        return arr, True
    return arr, False
 
def find_value_later(arr, montante, isPositive, tolerance_value):
    copy = [x for x in montante]
    if len(arr) <= 1:
        return
    for i in range(len(arr)):
        value = arr[i]
       
        if isPositive:
            if sum(montante) + value > valueToFind and abs(valueToFind - sum(montante)) > tolerance_value:
                continue
        else:    
            if sum(montante) + value < valueToFind and abs(valueToFind - sum(montante)) > tolerance_value:
                continue
        montante.append(value)
 
        if sum(montante) == valueToFind or abs(sum(montante) - valueToFind) <= tolerance_value:
            return True
        if not find_value_later(arr[i + 1:], montante, isPositive, tolerance_value):
            montante.clear()
            montante.extend([x for x in copy])
        else:
            return True
    return False
 
def find_value(arr, montante, isPositive , tolerance_value):
    for i in range(len(arr)):
        value = arr[i]
        montante.clear()
        montante.append(value)
        if sum(montante) == valueToFind:
            return
        find_value_later(arr[i + 1:], montante, isPositive, tolerance_value)
        if sum(montante) == valueToFind or abs(sum(montante) - valueToFind) <= tolerance_value:
            return
    return
 
def main(arr, montante, isPositive, tolerance_value):
    arr, success = sort_find_value(arr, isPositive)
    if success:
        return montante
    find_value(arr, montante, isPositive, tolerance_value)
    # print(montante)
    return montante
 
def read_clipboard():
    clipboard_content = pc.paste()
    return clipboard_content
   
def write_to_excel(final_result):
    final_result.to_excel(file, index=False)
 
def fix_number(text: str) -> str:
    text = re.sub(r'^0*(?=([0-9]))', '', text)
    if re.search(',', text):
        if re.search(r'\.', text):
            if re.search(',', text[::-1]).start() < re.search(r'\.', text[::-1]).start():
                text = re.sub(',', 'x', text)
                text = re.sub('\.', '', text)
                text = re.sub('x', '.', text)
        else:
            text = re.sub(',', '.', text)
    return text
 
if __name__ == '__main__':
   
    collection = pd.read_csv(StringIO(read_clipboard()), sep=",")
   
    field = sys.argv[1]
   
    valueToFind = float(fix_number(sys.argv[2]))

    tolerance_value = float(fix_number(sys.argv[3]))
   
    file = sys.argv[4]
   
    collection.replace(',', '.', regex=True, inplace=True)
    collection[field] = collection[field].apply(lambda x: float(x))
   
    array = collection[field]
 
    array = list(array)
   
    success = False
   
    combinationReturn = []
 
    if valueToFind < 0:
        array = list(filter(lambda x: x < 0 and x >= valueToFind, array))
        combinationReturn = main(array, combinationReturn, False, tolerance_value)
    else:
        array = list(filter(lambda x: x > 0 and x <= valueToFind, array))
        combinationReturn = main(array, combinationReturn, True, tolerance_value)    
   
    result = []

    for value in combinationReturn:
        filtered:pd.DataFrame = collection[collection[field] == value]
        index = filtered.first_valid_index()
        filtered = filtered[filtered.index == index]
        collection.drop(filtered.first_valid_index(), inplace=True)
        result.append(filtered)

    final_result = pd.concat(result, ignore_index=True)
    write_to_excel(final_result)