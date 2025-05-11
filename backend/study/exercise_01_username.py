

def get_name():
    result = input("輸入使用者名稱: ")

    if len(result) == 0:
        print("名稱不能為空")
    elif len(result) > 12 :
        print("名稱不能超過12個字元。")
    elif result.count(" ") > 0:
        print("名稱不能包含空白。")
    elif not result.isalpha():
        print("名稱不能包含數字。")
    else:
        print(f"歡迎 {result.capitalize()}")
        return result
    return get_name()

name = get_name()