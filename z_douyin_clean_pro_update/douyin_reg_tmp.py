import random


def generate_gid():
    gids = []
    for number in range(100000, 10000000):
        gids.append(number)
    for gid in gids:
        index0 = random.randint(0, len(gids) - 1)
        index1 = len(gids) - 1
        tmp = gids[index0]
        gids[index0] = gids[index1]
        gids[index1] = tmp
    return gids.pop()


if __name__ == "__main__":
    for i in range(20):
        print(generate_gid())