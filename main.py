from subprocess import call
import time

#### Configuration here ####
process_to_switch = "prime95"
thread_num = 12  # number of threads
sec_between_switch = 10  # number of seconds between switching threads
############################

thread_list = [2**n for n in range(thread_num)]

running = True
while running:
    try:
        # do switch
        time.sleep(sec_between_switch)
        print(f"{sec_between_switch} s passed")
    except KeyboardInterrupt:
        running = False

print("Stopped")
