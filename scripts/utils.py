import os

def remove_files(__filepath__):
    if os.path.exists(__filepath__):
        for file in os.listdir(__filepath__):
            os.remove(os.path.join(__filepath__, file))

def init_filesystem(__static_path__):
    if not os.path.exists(__static_path__):
        os.mkdir(__static_path__)
    else:
        if not os.path.exists(__static_path__ + '/images'):
            os.mkdir(__static_path__ + '/images')
        if not os.path.exists(__static_path__ + '/temp'):
            os.mkdir(__static_path__ + '/temp')

