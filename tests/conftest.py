import os
import hashlib

# Patch hashlib.md5 and hashlib.new to avoid TypeError on Python 3.8 / older environment
original_md5 = hashlib.md5
def patched_md5(*args, **kwargs):
    kwargs.pop('usedforsecurity', None)
    return original_md5(*args, **kwargs)
hashlib.md5 = patched_md5

original_new = hashlib.new
def patched_new(name, *args, **kwargs):
    kwargs.pop('usedforsecurity', None)
    return original_new(name, *args, **kwargs)
hashlib.new = patched_new

os.environ["ADMIN_PASSWORD"] = "admin_password"
os.environ["ENGINEER_PASSWORD"] = "engineer_password"
os.environ["VIEWER_PASSWORD"] = "viewer_password"
os.environ["JWT_SECRET_KEY"] = "super_secret_wine_key"
os.environ["JWT_SECRET"] = "super_secret_wine_key"
