""" Mount filesystem """


class MountPoint:
    def __init__(self):
        print('mount init')

    def __enter__(self):
        print('mount enter')

    def __exit__(self, exc_type, exc_val, exc_tb):
        print('mount exit')


# cannot get a decorator to work with the above:
# unable to access BackupMethod instance member
# will be using plain `with`

# def mount(argo):
#     mount_point = MountPoint()
#
#     def decorator(func):
#         def wrapper(self, *args, **kwargs):
#             v = getattr(self, argo)
#             print(v)
#             with mount_point:
#                 return func(*args, **kwargs)
#         return wrapper
#     return decorator

# class Mount:
#     def __init__(self, func):
#         self.func = func
#         for name in set(dir(func)) - set(dir(self)):
#             setattr(self, name, getattr(func, name))
#
#     def __call__(self, *args):
#         # with MountPoint:
#         print(self.func.arg)
#         return self.func(self, *args)
