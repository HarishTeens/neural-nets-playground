def get_input(x):
    t = [0.01] * 10
    t[x] = 0.99
    return t


t4 = get_input(4)
t5 = get_input(5)

net = [
    # Row 1
    [
        (0, 0),
        (0, 0),
        (0, 0),
        (0, 0),
        (0, 0),
        (0, 0),
        (0, 0),
        (0, 0),
        (1, -0.01),
        (1, -0.01),
    ],
    # Row 2
    [
        (0, 0),
        (0, 0),
        (0, 0),
        (0, 0),
        (1, -0.01),
        (1, -0.01),
        (1, -0.01),
        (1, -0.01),
        (0, 0),
        (0, 0),
    ],
    # Row 3
    [
        (0, 0),
        (0, 0),
        (1, -0.01),
        (1, -0.01),
        (0, 0),
        (0, 0),
        (1, -0.01),
        (1, -0.01),
        (0, 0),
        (0, 0),
    ],
    # Row 4
    [
        (0, 0),
        (1, -0.01),
        (0, 0),
        (1, -0.01),
        (0, 0),
        (1, -0.01),
        (0, 0),
        (1, -0.01),
        (0, 0),
        (1, -0.01),
    ],
]


def predict_binary(net, tt):
    output = [0] * len(net)
    for i, wps in enumerate(net):
        wpsum = 0
        for j, wp in enumerate(wps):
            wpsum = wpsum + wp[0] * tt[j] + wp[1]
        output[i] = wpsum

    output = ["1" if x > 0.9 else "0" for x in output]
    print("".join(output))


predict_binary(net, t5)
