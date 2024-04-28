def error_handler(func):
    def inner_func(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except Exception as e:
            print(f"{func.__name__}: {e}")
    return inner_func
