import asgiref


def run(blocking_func, *args, **kwargs):
    return asgiref.sync_to_async(blocking_func)(*args, **kwargs)
