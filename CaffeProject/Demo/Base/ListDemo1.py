a = list(range(10))
b = [1, 2, 5, 6, 9]
a = [a[i] for i in range(len(a)) if i not in b]
print(a)