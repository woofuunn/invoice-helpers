menu1= dict(披薩=300, 爆米花=200, 薯條=90, 洋芋片=60, 軟麵包條=120, 蘇打水=60, 檸檬水=90)

menu={
    "披薩":300,
    "爆米花":200,
    "薯條":90,
    "洋芋片":60,
    "軟麵包條":120,
    "蘇打水":60,
    "檸檬水":90
    }

cart = []
total = 0
cur = ""

print("[我是購物車]")
while True:
    for index , food in menu.items():
        print(f"{index} → {food} 元 ")
    pick = input("請輸入所需的商品名稱(輸入 # 結帳): ")

    if pick == '#': break
    elif pick not in menu : print(f"沒有 {pick} 這項商品")
    else:
        cart.append(pick)
        total += menu.get(pick)

    print("-----------------")
    print(f"目前選擇的商品: {cart}")
    print(f'目前金額: {total} 元')
    print("-----------------")

count = len(cart)
if count == 0: print("你沒有選擇商品，byebye")
else:print(f"你選擇了 {count} 項商品, 總共 {total} 元")

# cart = []
# total = 0
#
# print("🛒 [我是購物車]")
# print("輸入商品名稱將其加入購物車，輸入 # 結帳。")
# print()
#
# while True:
#     print("📋 商品清單：")
#     for name, price in menu.items():
#         print(f"  {name} → {price} 元")
#
#     pick = input("\n請輸入商品名稱（輸入 # 結帳）: ").strip()
#
#     if pick == '#':
#         break
#     elif not pick:
#         print("⚠️ 請勿輸入空白！")
#     elif pick not in menu:
#         print(f"❌ 沒有「{pick}」這項商品")
#     else:
#         cart.append(pick)
#         total += menu[pick]
#         print(f"✅ 已加入：{pick}（目前總額 {total} 元）")
#
#     print("-" * 30)
#
# # 🧾 結帳畫面
# print("\n🧾 [結帳結果]")
# if not cart:
#     print("你沒有選擇任何商品，bye bye～")
# else:
#     print(f"你選擇了 {len(cart)} 項商品：{cart}")
#     print(f"總金額：{total} 元")