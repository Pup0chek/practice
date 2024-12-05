


# generator= [i for i in range(6)]
#
# for i in generator:
#     print(i)

# def gen():
#     list = range(6)
#     for i in list:
#         yield i
#
# generator = gen()
# print(generator)


def meshok(n):
    cnt = 0
    while cnt < n:
        yield cnt
        cnt +=1

def child(name, n, meshok):
    while n > 0:
        i = next(meshok)
        n-=1
        print(f"{name}, eated {i}")


meshok = meshok(12)
ivan = child('ivan', 3, meshok)
nick = child('nick', 4, meshok)
liya = child('liya', 2, meshok)
print(next(meshok))

