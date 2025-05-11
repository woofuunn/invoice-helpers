# name = input("請輸入名字: ")
# print(f"你的名字是 {name.capitalize()}")

def get_float():
    num = input("輸入一個數字: ")
    if num.isdigit() :
        return float(num)
    else:
        print("<請輸入數字!>")
        return get_float()

# length = get_float()
# width = get_float()
# area = length * width
# print(f"面積為: {area}")

# Python 沒有三元運算子
# 可由 if else 實現
result = "已成年" if 17>=18 else "未成年"

if (21>=18): result1 ="18歲以上"
else: result1 ="未滿18歲"

print(result)
print(result1)
