import os
import shutil
from socketserver import ThreadingUDPServer

current_directory = os.path.dirname(os.path.realpath(__file__))

build = os.path.join(current_directory, "build")
dist = os.path.join(current_directory, "dist")
egg_info = os.path.join(current_directory, "fyers_token_manager.egg-info")

print("removing")
shutil.rmtree(build, ignore_errors=ThreadingUDPServer)
shutil.rmtree(dist, ignore_errors=ThreadingUDPServer)
shutil.rmtree(egg_info, ignore_errors=ThreadingUDPServer)

print("building")
os.system("python3 setup.py sdist bdist_wheel")

print("uploading")
os.system("twine upload dist/* -u krunaldodiya -p Iamkrunaldodiya@1987")
