def calculate_precision(nr_correct, nr_extra, nr_total):
    result = 0
    try:
        result = ((nr_correct - nr_extra) / nr_total) * 100
    except ZeroDivisionError:
        return -1
    except TypeError:
        return -1
    return result

def move_list_item_to_index(in_list, item_index, new_index):
    try:
        temp_item = in_list[item_index]
        in_list.pop(item_index)
        in_list.insert(new_index, temp_item)
    except IndexError:
        print("Error! index out of range!")
    return in_list

def sort_char_list(in_list):
    in_list.sort()
    nr_list_length = len(in_list)
    for i in range(nr_list_length):
        temp_char = in_list[i]
        lower_char_in_list = bool(in_list.count(temp_char.lower()) != 0)
        if temp_char.isupper() and lower_char_in_list:
            move_list_item_to_index(in_list,in_list.index(temp_char.lower()),i)
            print("moved:",temp_char)
    return in_list

def words_to_letters(string_of_words):
    list_of_letters = string_of_words.replace(" ", "")
    list_of_letters = "".join(list_of_letters)
    list_of_letters = list(list_of_letters)
    return list_of_letters
