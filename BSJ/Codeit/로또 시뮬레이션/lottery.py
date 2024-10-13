from random import randint
import random

def generate_numbers(n):
    # 여기에 코드를 작성하세요
    num_list = []
    while len(num_list) < n:
        num = random.randint(1,45)
        if num not in num_list:
            num_list.append(num)

    return num_list
        
# 테스트 코드
# print(generate_numbers(6))

def draw_winning_numbers():
    # 여기에 코드를 작성하세요
    num_list = generate_numbers(6)
    num_list.sort()
    new_num = random.randint(1,45)
    if new_num not in num_list:
        num_list.append(new_num)
    
    return num_list
    
# 테스트 코드
# print(draw_winning_numbers())

def count_matching_numbers(numbers, winning_numbers):
    # 여기에 코드를 작성하세요
    result = 0
    for i in range(0, len(numbers)):
        for j in range(0, len(winning_numbers)):
            if numbers[i] == winning_numbers[j] : 
                result += 1
    return result

# 테스트 코드
# print(count_matching_numbers([2, 7, 11, 14, 25, 40], [2, 11, 13, 14, 30, 35]))
# print(count_matching_numbers([2, 7, 11, 14, 25, 40], [14]))

def count_matching_numbers(numbers, winning_numbers):
    # 지난 실습의 코드를 여기에 붙여 넣으세요
    result = 0
    for i in range(0, len(numbers)):
        for j in range(0, len(winning_numbers)):
            if numbers[i] == winning_numbers[j] : 
                result += 1
    return result

### sjbang
# def check(numbers, winning_numbers):
#     # 여기에 코드를 작성하세요
#     if count_matching_numbers(numbers, winning_numbers) == 6 and winning_numbers[-1] not in numbers:
#         money = 1000000000
#     elif count_matching_numbers(numbers, winning_numbers) == 6 and winning_numbers[-1] in numbers:
#         money = 50000000
#     elif count_matching_numbers(numbers, winning_numbers) == 5:
#         money = 1000000
#     elif count_matching_numbers(numbers, winning_numbers) == 4:
#         money = 50000
#     elif count_matching_numbers(numbers, winning_numbers) == 3:
#         money = 5000
    
#     return money
    
# 테스트 코드
# print(check([2, 4, 11, 14, 25, 40], [4, 12, 14, 28, 40, 41, 6]))
# print(check([2, 4, 11, 14, 25, 40], [2, 4, 10, 11, 14, 40, 25]))


def check(numbers, winning_numbers):
    count = count_matching_numbers(numbers, winning_numbers[:6])
    bonus_count = count_matching_numbers(numbers, winning_numbers[6:])

    if count == 6:
        return 1000000000
    elif count == 5 and bonus_count == 1:
        return 50000000
    elif count == 5:
        return 1000000
    elif count == 4:
        return 50000
    elif count == 3:
        return 5000
    else:
        return 0


# 테스트 코드
print(check([2, 4, 11, 14, 25, 40], [4, 12, 14, 28, 40, 41, 6]))
print(check([2, 4, 11, 14, 25, 40], [2, 4, 10, 11, 14, 40, 25]))
