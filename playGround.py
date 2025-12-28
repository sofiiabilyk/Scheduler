import random
lst = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
print(lst)
lst[2] = lst[-1]
print(lst)
print(lst.remove(2))
print(lst)
print(lst.remove(8))
print(lst)

'''
for item in lst:
    print("item")
    print(item)

    print(lst)
    lst[2] = lst[-1]
    print(lst)
    print(lst.pop())
    print(lst)'''