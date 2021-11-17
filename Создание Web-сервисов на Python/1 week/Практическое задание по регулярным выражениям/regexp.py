def calculate(data, findall):
    matches = findall(r"([a-c])([+-]?)=([a-c]?)([+-]?\d+)?") 

    for v1, s, v2, n in matches:
        right = data.get(v2, 0) + int(n or 0)
        if s == '+':
            data[v1] += right
        elif s == '-':
            data[v1] -= right
        else:
            data[v1] = right

    return data
