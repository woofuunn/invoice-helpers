import time

sec = 3715
for i in range(sec,0,-1):
    #ex 02:00
    seconds = int(i % 60)
    minutes = (i // 60 % 60)

    print(f"{minutes:02}:{seconds:02}")
    #time.sleep(1)


