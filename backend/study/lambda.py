
# store = [
#     ('shirt', 20), #US dollars
#     ('pants', 30),
#     ('Jacket',50),
#     ('socks', 10)
#     ]
# to_ntd = lambda data: (data[0], data [1] * 30)
#
# store_euros = list(map (to_ntd, store))
#
# print(store_euros)

friends = [
    ("Bob", 18),

    ("Steven", 17),

    ("Michael", 19),

    ("Susan", 16)

    ]

age_filter = lambda data: data [1] >= 18

can_drink_friends_map = list(map(age_filter, friends))
can_drink_friends_filter = list(filter(age_filter, friends))

print(can_drink_friends_map)
print(can_drink_friends_filter)
