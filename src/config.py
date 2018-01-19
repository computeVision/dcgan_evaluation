import glob
import os
import sys
import numpy as np

import tensorflow as tf
import yaml

flags = tf.app.flags
FLAGS = flags.FLAGS


class Cfg:
    '''
    Class for reading .yaml files.
    '''
    # getter
    def dataset(self):
        return self.__dataset

    def input_height(self):
        return self.__input_height

    def output_height(self):
        return self.__output_height

    def train(self):
        return self.__train

    def generator(self):
        return self.__generator

    def discriminator(self):
        return self.__degenerator

    def paths(self):
        return self.__paths

    def random_vec(self):
        return self.__random_vector

    def __init__(self, file_path):
        self.__generator = {}
        self.__degenerator = {}
        self.__paths = {}
        self.__random_vector = {}

        with open(file_path, 'r') as ymlfile:
            home = os.environ['HOME'] + "/"
            self.__cfg = yaml.load(ymlfile)

            self.__dataset = self.__cfg['params']['dataset']
            self.__train = self.__cfg['params']['train']
            self.__input_height = self.__cfg['params']['input_height']
            if self.__dataset == 'mnist':
                self.__output_height = self.__cfg['params']['output_height']

            self.__paths['path_to_runs'] = home + self.__cfg['paths']['path_to_runs']
            self.__paths['path_to_checkpoints'] = home + self.__cfg['paths']['path_to_checkpoints']

            self.__generator['relu'] = self.__cfg['testing_benchmark']['generator']['relu']
            self.__generator['lrelu'] = self.__cfg['testing_benchmark']['generator']['lrelu']
            self.__generator['tanh'] = self.__cfg['testing_benchmark']['generator']['tanh']
            self.__generator['batch_norm'] = self.__cfg['testing_benchmark']['batch_norm']

            self.__degenerator['relu'] = self.__cfg['testing_benchmark']['degenerator']['relu']
            self.__degenerator['lrelu'] = self.__cfg['testing_benchmark']['degenerator']['lrelu']
            self.__degenerator['tanh'] = self.__cfg['testing_benchmark']['degenerator']['tanh']
            self.__degenerator['pooling'] = self.__cfg['testing_benchmark']['degenerator']['pooling']
            self.__degenerator['batch_norm'] = self.__generator['batch_norm']

            self.__random_vector['uniform'] = self.__cfg['random_vector']['uniform']
            self.__random_vector['uniform100'] = self.__cfg['random_vector']['uniform100']
            self.__random_vector['normal'] = self.__cfg['random_vector']['normal']


        self.print_members()
        self.print_flags(FLAGS)

    def get_filenames(self, super_dir, subdir, ending="/*.png"):
        tmp = {}
        if len(subdir) % 2 != 0:
            subdir.pop()
        for img in subdir:
            tmp.update({img: sorted(glob.glob(super_dir + "/" + img + ending))})
        return tmp

    def print_members(self):
        attrs = vars(self)
        print(', '.join("%s: %s\n" % item for item in attrs.items()))

    def print_flags(self, obj):
        attrs = vars(obj)
        for key, car in attrs['__flags'].items():
            print(key, ": ", car)


def check_runs(dir):
    print("check runs dir: ", dir)
    previous_runs = [os.path.basename(x) for x in glob.glob(dir + '/run_*')]
    if len(previous_runs) == 0:
        run_number = 1
    else:
        run_number = max([int(s.split('run_')[1]) for s in previous_runs]) + 1

    return "%002d" % run_number


def create_directories(cfg):
    dir = cfg.paths()['path_to_runs']
    run_nr = check_runs(dir)
    print('run nr: ', run_nr)

    cfg.paths()['path_to_runs'] = dir + '/' + 'run_' + run_nr
    FLAGS.sample_dir = cfg.paths()['path_to_runs'] + '/samples'
    if not os.path.exists(FLAGS.sample_dir):
      os.makedirs(FLAGS.sample_dir)

    print('debug', cfg.paths()['path_to_runs'])

    if not os.path.exists( cfg.paths()['path_to_runs'] + '/train'):
        os.makedirs(cfg.paths()['path_to_runs'] + '/train/')

    cfg.paths()['path_to_checkpoints'] = cfg.paths()['path_to_checkpoints'] + '/' + 'run_' + run_nr + '/checkpoint'
    FLAGS.checkpoint_dir = cfg.paths()['path_to_checkpoints']
    if not os.path.exists( cfg.paths()['path_to_checkpoints']):
        os.makedirs(cfg.paths()['path_to_checkpoints'] )

    FLAGS.logs = cfg.paths()['path_to_runs'] + '/logs'
    if not os.path.exists(FLAGS.logs):
        os.makedirs(FLAGS.logs)

    FLAGS.test = cfg.paths()['path_to_runs'] + '/test'
    if not os.path.exists(FLAGS.test):
        os.makedirs(FLAGS.test)

    FLAGS.visualize_path = cfg.paths()['path_to_runs'] + '/train'

    # import pdb; pdb.set_trace()

    import shutil
    shutil.copy('src/model.py', cfg.paths()['path_to_runs'] + '/model.py')
    shutil.copy('configs/config.yaml', cfg.paths()['path_to_runs'] + '/config.yaml')

    return run_nr


def send_mail(global_time):
    import email
    import smtplib
    import pickle
    # pw = 'pw!'
    # with open("bytesfile", "wb") as mypicklefile:
    #     pickle.dump(pw, mypicklefile)

    file = open("src/bytesfile", 'rb')
    pw = pickle.load(file)
    file.close()

    global_time /= 60
    print(' global time: ', global_time)

    msg = email.message_from_string('Global Time: ' + str(global_time))
    msg['From'] = "peters_kotlett@hotmail.com"
    msg['To'] = "lorenz.pet@hotmail.com"
    msg['Subject'] = "Learning Finished"

    s = smtplib.SMTP("smtp.live.com", 587)
    s.ehlo()  # Hostname to send for this command defaults to the fully qualified domain name of the local host.
    s.starttls()  # Puts connection to SMTP server in TLS mode
    s.ehlo()
    s.login('***@hotmail.com', pw)
    s.sendmail(msg['From'], msg['To'], msg.as_string())
    s.quit()
