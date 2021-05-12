from datetime import timedelta


# #####################  MUST SET THESE CORRECTLY  ###########################
necessary = {
    "process_to_switch": "prime95",
    # name of process (could also be "cinebench")

    "core_num": 6,
    # number of cores

    "hyper_threading": True,
    # True or False, whether your CPU has 2 threads per core (SMT is AMD word)
}
##############################################################################


# The below are optional
other_options = {
    "switch_every": timedelta(minutes=5),
    # time between switching threads
    "sync_on_clock_minute": True,
    # synchronize with wall time because prime95 only logs time in hh:mm
    "starting_core": 1
    # 1-indexed (1 is first, total number of cores is last index)
    # core number to start testing from
}


cfg = other_options | necessary
