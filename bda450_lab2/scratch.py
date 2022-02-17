interest_rate = 0.01
total_owing = 10000
payment = 1000

for x in range(0, 11):
    temp = (total_owing - payment)
    total_owing = (temp * interest_rate) + temp
    print(total_owing)



