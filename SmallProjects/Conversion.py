def quick_conversion(r, g, b):
    result = [r, g, b]
    for i in range(0, 3):
        result[i] = round(float(result[i])/256, 3)
    return tuple(result)

while True:
    r = input("R: ")
    g = input("G: ")
    b = input("B: ")
    print(quick_conversion(r, g, b))
