# coding=utf-8
total_diods = 32
total_rows = 5
x_range = 224
y_range = 64
max_y = 95  # диод 4
max_x = 337  # максимальное физическое растояние между диодами пинки клавиш

x_ratio = x_range / max_x
y_ratio = y_range / max_y

# смещения по рядам между левой и правой частями клавиатуры
bias_row_0 = 104
bias_row_1 = 105
bias_row_2 = 106
bias_row_3 = 33
bias_row_4 = 46
bias_rows = {0: 104, 1: 105, 2: 106, 3: 33, 4: 46}

coordinates_left = (
    (
        0,
        (
            (27, (19, 90)),
            (26, (37, 90)),
            (18, (60, 93)),
            (17, (79, 95)),
            (8, (97, 92)),
            (7, (117, 88)),
        ),
    ),
    (
        1,
        (
            (28, (19, 71)),
            (25, (37, 71)),
            (19, (58, 74)),
            (16, (77, 76)),
            (9, (97, 73)),
            (6, (115, 70)),
        ),
    ),
    (
        2,
        (
            (31, (0, 48)),
            (29, (19, 52)),
            (24, (38, 52)),
            (20, (58, 55)),
            (15, (77, 57)),
            (10, (97, 53)),
            (5, (115, 51)),
        ),
    ),
    (
        3,
        (
            (30, (19, 33)),
            (23, (37, 33)),
            (21, (57, 36)),
            (14, (76, 38)),
            (11, (95, 35)),
            (4, (114, 32)),
            (3, (131, 22)),
            (2, (152, 12)),
        ),
    ),
    (
        4,
        (
            (22, (63, 24)),
            (13, (85, 26)),
            (12, (106, 12)),
            (0, (127, 13)),
            (1, (145, 0)),
        ),
    ),
)


def generate_coordinate_right():
    coordinates_right = []
    for row_number_i, diods_tuple in coordinates_left:
        coordinates_row_i = []
        latest_diod_in_row = diods_tuple[-1]
        latest_diod_in_row_x = latest_diod_in_row[1][0]

        for num_diod, coordinate_diod in diods_tuple:
            print(f"row {row_number_i} diod's nubmer {num_diod}\n")
            right_x = (
                latest_diod_in_row_x
                + (latest_diod_in_row_x - coordinate_diod[0])
                + bias_rows[row_number_i]
            )
            right_y = coordinate_diod[1]
            coordinates_row_i.append((num_diod + total_diods, (right_x, right_y)))

        coordinates_right.append((row_number_i + total_rows, coordinates_row_i))

    return coordinates_right


def scale_coordinates(coordinates):
    scale_coordinates = []
    for row_number_i, diods_tuple in coordinates:
        coordinates_row_i = []
        for num_diod, coordinate_diod in diods_tuple:
            x = round(coordinate_diod[0] * x_ratio)
            y = round(coordinate_diod[1] * y_ratio)
            coordinates_row_i.append((num_diod, (x, y)))
        scale_coordinates.append((row_number_i, coordinates_row_i))

    return scale_coordinates


def print_for_keyboard(coordinates):
    for _, diods_tuple in coordinates:
        temp_str = ""
        for _, coordinate_diod_i in diods_tuple:
            temp_str += f"{{ {coordinate_diod_i[0]}, {coordinate_diod_i[1]} }},"
        print(temp_str)


coordinates_right = generate_coordinate_right()

scale_coordinates_left = scale_coordinates(coordinates_left)
scale_coordinates_right = scale_coordinates(coordinates_right)

print_for_keyboard(scale_coordinates_left)
print_for_keyboard(scale_coordinates_right)

"""
 "rgblight": {
        "hue_steps": 10,
        "led_count": 64,
        "max_brightness": 100,
        "led_map": [28, 30, 31, 29, 24, 25, 26, 27, 22, 21, 20, 19, 23, 18, 14, 15, 16, 17, 12, 11, 10, 9, 13, 5, 6, 7, 8, 4, 3, 2, 1, 0, 34, 32, 33, 35, 37, 38, 39, 40, 45, 44, 43, 42, 36, 41, 47, 48, 49, 50, 54, 53, 52, 51, 46, 55, 56, 57, 58, 62, 61, 60, 59, 63],
        "split_count": [32, 32],
        "animations": {
            "breathing": true,
            "rainbow_mood": true,
            "rainbow_swirl": true,
            "snake": true,
            "knight": true,
            "christmas": true,
            "static_gradient": true,
            "rgb_test": true,
            "alternating": true
        }
    },
"""
