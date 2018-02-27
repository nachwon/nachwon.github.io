def sum_all(arr):
    if len(arr) == 0:
        return 0
    elif len(arr) == 1:
        return arr[0]
    else:
        first = arr.pop(0)
        print(first)
        rest_total = 0
        for i in arr:
            rest_total += i
        return first + sum_all(arr)

l = [2, 4, 6, 8]
print(sum_all(l))