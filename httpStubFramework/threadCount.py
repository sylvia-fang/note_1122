import time

server_lst = set()


def check_server_start(check_lst):
    count_time = 0
    while True:
        print(server_lst)
        if server_lst == check_lst:
            time.sleep(2)
            break

        if count_time > 30:
            raise "server start error"
        else:
            count_time += 1
            print("wait time")
            time.sleep(1)
