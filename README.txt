#################################################################
#################################################################
Installation:
    Anaconda python 2.7
    pip install tensorflow-gpu

#################################################################
1. Download

    Library: In the home directory, execute <python download.py>


2. Execute

    Go back to dcgan directory and execute: <python src/main.py --dataset celebA --input_height=108 --train --crop>
    This trains the network and finally one hundred images will be tested and 64 of them sticked together as an overview.

    wait ~ 20hours

    Results can be found in "/home/Documents/dcgan_runs"


3. Enjoy :)
#################################################################

Files added:
 - config.py
 - config.yaml

Files modified:
 - model.py


#################################################################

Tensorboard:
   
   Go to:
   "/home/Documents/dcgan_runs" and run "tensorboard --logdir=./" in the shell
   
   Open the browser: 0.0.0.0:6006
