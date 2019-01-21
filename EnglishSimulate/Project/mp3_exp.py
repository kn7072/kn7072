#coding="utf-8"

path_mp3_1 = "этнический_rus.mp3"
path_mp3_2 = "01 - Intro.mp3"


def get_bin_data(path_to_file):
    with open(path_to_file, "rb") as f:
        data = f.read()
    return data


def write_file(f, data):
    f.write(data)

data_file = get_bin_data("этнический_rus.mp3")
data_empty = get_bin_data("empty5_96.mp3")
with open("xx.mp3", "wb") as f:
    f.write(data_file)
    f.write(data_empty)
    f.write(data_file)

print()
def get_data_file(path_file, chunk_size):
    data_file = b""
    with open(path_file, "rb") as f:
        while True:
            data = f.read(chunk_size)
            if not data:
                break
            yield data

# https://www.youtube.com/watch?v=Lz_IVfGjgks
for piece in get_data_file(path_mp3_1, 100):
    print(piece)
    print(len(piece))

