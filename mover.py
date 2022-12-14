import os
import shutil
import subprocess
import configparser
from time import sleep

# Initialize configParser # 
config = configparser.ConfigParser()
config.read("config.ini")

# All Paths #
RawFlashDir = config["Default"]["flashpath"] + "\\07_0x805EC000_PFlash.bin"
S19inDir = config["Default"]["s19inpath"]
S19outDir = config["Default"]["s19outpath"]
LifRootDir = config["Default"]["lifrootdir"]

# delete all files in folder which are not "bin2s19.cmd"
for file in os.listdir(S19inDir):
    print(file)
    if file != "bin2s19.cmd":
        os.remove(f"{S19inDir}\\{file}")

shutil.copy(RawFlashDir,S19inDir)   # copy raw flash file to S19in folder
os.chdir(S19inDir)                  # change to S19in folder
os.startfile("bin2s19.cmd")         # start first step 
os.chdir(LifRootDir)                # change to Lif root folder
sleep(0.2)
os.startfile("s19lifalign.cmd")     # start second step 
sleep(0.3)
shutil.move(S19outDir + "\\07_0x805ec000_pflash_aligned.s19", S19inDir) # Cut aligned file an putinto S19in folder
os.chdir(S19inDir)                  # change to S19in folder
os.remove(S19inDir + "\\07_0x805EC000_PFlash.bin")  # remove unnecessary file
os.remove(S19inDir + "\\07_0x805EC000_PFlash.s19")  # remove unnecessary file
os.chdir(LifRootDir)                # change to Lif root folder to start eval cmd
os.startfile("s19lifeval.cmd")      # start third step

