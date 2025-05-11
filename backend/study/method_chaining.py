class Num:
    val = 0
    def add(self):
        self.val += 1
        return self
    def cen(self):
        self.val -= 1
        return self
a = Num()
a.add().add().add()
print(a.val)


print(happy := True)
if happy:
    print("開心")
else:
    print("不開心")

foods = []
while (food := input('你喜歡什麼食物?').strip()) != 'q':
    foods.append(food)
print(foods)

