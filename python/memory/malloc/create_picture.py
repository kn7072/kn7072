def parse_result(filename):
    ms = []
    with open(filename, "r") as f:
        for line in f:
            if line.startswith("Total"):
                m = float(line.split()[-1].replace(",", "")) / 1024 / 1024
                ms.append(m)
    return ms

ms_1 = parse_result("_1.txt")
ms_2 = parse_result("_2.txt")
ms_3 = parse_result("_3.txt")
ms_4 = parse_result("_4.txt")

import matplotlib.pyplot as plt
plt.figure(figsize=(20, 15))

fontdict = {
    "fontsize": 20,
    "fontweight" : 1,
}

plt.subplot(2, 2, 1)
plt.title("Без элементов", fontdict=fontdict, loc="left")
plt.plot(ms_1)
plt.grid(b=True, which='major', color='#666666', linestyle='-.')
plt.minorticks_on()
plt.grid(b=True, which='minor', color='#999999', linestyle='-', alpha=0.2)
plt.tick_params(axis='both', which='major', labelsize=15, labelbottom=False)
plt.ylabel("MB", fontsize=15)

plt.subplot(2, 2, 2)
plt.title("Каждый второй", fontdict=fontdict, loc="left")
plt.plot(ms_2)
plt.grid(b=True, which='major', color='#666666', linestyle='-.')
plt.minorticks_on()
plt.grid(b=True, which='minor', color='#999999', linestyle='-', alpha=0.2)
plt.tick_params(axis='both', which='major', labelsize=15, labelbottom=False)
plt.ylabel("MB", fontsize=15)

plt.subplot(2, 2, 3)
plt.title("Вторая половина", fontdict=fontdict, loc="left")
plt.plot(ms_3)
plt.grid(b=True, which='major', color='#666666', linestyle='-.')
plt.minorticks_on()
plt.grid(b=True, which='minor', color='#999999', linestyle='-', alpha=0.2)
plt.tick_params(axis='both', which='major', labelsize=15, labelbottom=False)
plt.ylabel("MB", fontsize=15)

plt.subplot(2, 2, 4)
plt.title("Каждый сотый", fontdict=fontdict, loc="left")
plt.plot(ms_4)
plt.grid(b=True, which='major', color='#666666', linestyle='-.')
plt.minorticks_on()
plt.grid(b=True, which='minor', color='#999999', linestyle='-', alpha=0.2)
plt.tick_params(axis='both', which='major', labelsize=15, labelbottom=False)
plt.ylabel("MB", fontsize=15)