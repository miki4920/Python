def get_x(vertices):
    x = []
    for vertex in vertices:
        x.append(vertex[0])
    x.append(vertices[0][0])
    return x


def get_y(vertices):
    y = []
    for vertice in vertices:
        y.append(vertice[1])
    y.append(vertices[0][1])
    return y


def calculate_area(x, y):
    xy = 0
    yx = 0
    for i in range(0, len(x)-1):
        xy += x[i]*y[i+1]
        yx += x[i+1]*y[i]
    area = 0.5*abs(xy-yx)
    return area


if len(list_of_vertices) > 1:
    x_values = get_x(list_of_vertices)
    y_values = get_y(list_of_vertices)
    shape_area = calculate_area(x_values, y_values)
    print(shape_area)
else:
    print("Program requires at least two vertices")

