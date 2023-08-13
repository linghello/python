def f1(x):
    if x==1:
        return 1
    return x +f1(x-1)
print(f1(10))