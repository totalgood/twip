import pkg_resources

try:
    __version__ = pkg_resources.get_distribution(__name__).version
except:
    __version__ = 'unknown'


# # ## Not excited about putting this in __init__ because it gets imported during installation!
# import os
# from matplotlib import get_backend
# from matplotlib import use as set_backend

# os.environ['QT_API'] = 'pyside'
# DEFAULT_MPL_BACKEND = get_backend()

# try:
#     import PyQt4  # noqa
#     set_backend('Qt4Agg')
#     from matplotlib import pyplot as plt
# except ImportError:
#     try:
#         set_backend(DEFAULT_MPL_BACKEND)
#         from matplotlib import pyplot as plt
#     except ImportError:
#         set_backend('TkAgg')
#         from matplotlib import pyplot as plt
# try:
#     plt.style.use('ggplot')
# except:  # AttributeError:
#     print('Matplotlib needs to be upgraded to >= 1.4.1 to enable CSS styling and prettier plots.')
