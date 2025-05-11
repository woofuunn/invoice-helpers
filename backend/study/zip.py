usernames = ["Bob", "Steven", "Sam"]
passwords = ("123", "321", '555')

users = zip(usernames, passwords)     # zip 只能迭代 1 次
# print(users)
# print(type(users))
print(list(users))  # users 只能使用一次
print(list(users))  # 第二次users 為空值
