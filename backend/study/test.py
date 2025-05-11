

import math as m
_pi = m.pi               # 3.1415926535
_ceil = m.ceil(_pi)      # 4 (無條件進入)
_floor = m.floor(_pi)    # 3 (無條件捨去)


_list = [True, 2, "s"]
for i in _list:
    print(type(i))

#函式

# def _sum(num1,num2):
#  num1+=1
#  return num1+num2
#
# print(_sum(2,3))

# def aaa():
#  print("aaa")
#  print("bbb")
#     print("ccc")
#
# aaa()

# i = [1,"2",3.]
#
# for u in i:
#     print(type(u))
#
# print(p)

# _str = "string"      # 字串 str
# _int = 100           # 整數 int
# _float = 100.0       # 浮點數 float
# _bool = True         # 布林值 bool
#
#
# _list = [True, 2, "s"]      # 清單 list（有順序，可改變）
# _tuple = (1, 2, 3)          # 元組 tuple（有順序，不可改變）
# _set = {1, 2, 3}            # 集合 set（無順序，不重複）
# _dict = {"a": 1, "b": 2}    # 字典 dictionary（鍵值對）


#
#
# for s in _list:
#     print(type(s),end=" ")

# print(type(_bool))
def outer():
    count = 0
    def add():
        nonlocal count
        count += 1
        return count
    return add

counter = outer()

print(counter())
print(counter())
print(counter())