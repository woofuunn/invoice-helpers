
# 參數前面加一個 * 變成 tuple
def add(*args):
    total = 0
    for a in args:
        total += a
    return total

print(add(1,1,2,2))

# 參數前面加一個 ** 變成 dictionary
def add_product(**list):
    for kay, val in list.items():
        print(f"{kay}: {val} 元")

add_product(apple=10,banan=20)