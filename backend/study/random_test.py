import random

print(random.random())
# random() 產生一個 0.0 到 1.0（不包含 1.0）的浮點數亂數

print(random.randint(1,10))
# randint(x,y) 產生一個 x 到 y（包含 x 和 y）的整數亂數

print(random.uniform(1,10))
# uniform(x,y) 產生一個 x 到 y（包含 x 和 y）的浮點數亂數

print(random.choice(['apple','banana','mango']))
# choice(list) 隨機選一個元素

print(random.choices(['apple','banana','mango'],k=2))
# choice(list, k=次數) 隨機選 k 個元素（可重複）
