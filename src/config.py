import glob
import os
import sys
import numpy as np

import tensorflow as tf
import yaml

# defines
# ADAM = 'adam'
# tf.logging.set_verbosity(tf.logging.INFO)
#
flags = tf.app.flags
FLAGS = flags.FLAGS
#
# flags.DEFINE_string('checkpoints_dir', '/tmp/checkpoints/', 'checkpoints')
# flags.DEFINE_string('tensorboard_dir', '/tmp/occ_growing/', 'tb_dir')
# flags.DEFINE_float('learning_rate', 0.001, 'learning_rate')
# flags.DEFINE_float('lambda', 0.1, 'regularization')
# flags.DEFINE_integer('training_epochs', 3000, 'training_epochs')
# flags.DEFINE_boolean('use_checkpoint', False, 'use_checkpoint')
# flags.DEFINE_boolean('save_checkpoint', False, 'save_checkpoint')
#
# flags.DEFINE_boolean('use_locking', False, 'use_locking')
#
# # momentum
# flags.DEFINE_float('momentum', 0.01, 'momentum')
# flags.DEFINE_boolean('use_nesterov', True, 'use_nesterov')
#
# # adelta
# flags.DEFINE_float('rho', 0.001, 'rho')
# flags.DEFINE_float('epsilon', 0.001, 'epsilon')
#
# # adagradda
# flags.DEFINE_integer('global_step', 1, 'global_step')
# flags.DEFINE_integer('initial_gradient_squared_accumulator_value', 1, 'initial_gradient_squared_accumulator_value')
# flags.DEFINE_float('l1_regularization_strength', 0.0, 'l1_regularization_strength')
# flags.DEFINE_float('l2_regularization_strength', 0.0, 'l2_regularization_strength')
#
# # ftrl
# flags.DEFINE_float('learning_rate_power', -0.5, 'learning_rate_power')
# flags.DEFINE_float('initial_accumulator_value', 0.1, 'initial_accumulator_value')
# flags.DEFINE_float('l2_shrinkage_regularization_strength', 0.0, 'l2_shrinkage_regularization_strength')
#
# # rmsprop
# flags.DEFINE_float('decay', 0.9, 'decay')
#
# # syncreplicas
# flags.DEFINE_float('opt', 0.9, 'opt')
# flags.DEFINE_float('replicas_to_aggregate', 0.9, 'replicas_to_aggregate')
# flags.DEFINE_integer('total_num_replicas', 0, 'total_num_replicas')
# flags.DEFINE_integer('variable_avarages', 0, 'variable_avarages')
# flags.DEFINE_integer('variable_to_avarages', 0, 'variable_to_avarages')
#
# flags.DEFINE_string('addition', 'addition', 'concatination')


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

    def __init__(self, file_path):
        self.__generator = {}
        self.__degenerator = {}

        with open(file_path, 'r') as ymlfile:
            home = os.environ['HOME'] + "/"
            self.__cfg = yaml.load(ymlfile)

            self.__dataset = self.__cfg['params']['dataset']
            self.__train = self.__cfg['params']['train']
            self.__input_height = self.__cfg['params']['input_height']
            if self.__dataset == 'mnist':
                self.__output_height = self.__cfg['params']['output_height']

            self.__generator['relu'] = self.__cfg['testing_benchmark']['generator']['relu']
            self.__generator['lrelu'] = self.__cfg['testing_benchmark']['generator']['lrelu']
            self.__generator['tanh'] = self.__cfg['testing_benchmark']['generator']['tanh']
            self.__generator['pooling'] = self.__cfg['testing_benchmark']['generator']['pooling']
            self.__generator['batch_norm'] = self.__cfg['testing_benchmark']['generator']['batch_norm']

            self.__degenerator['relu'] = self.__cfg['testing_benchmark']['degenerator']['relu']
            self.__degenerator['lrelu'] = self.__cfg['testing_benchmark']['degenerator']['lrelu']
            self.__degenerator['tanh'] = self.__cfg['testing_benchmark']['degenerator']['tanh']
            self.__degenerator['batch_norm'] = self.__cfg['testing_benchmark']['degenerator']['batch_norm']

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

    # def init_optimizer(self, name):
    #     # self.__cfg[]
    #     if name == ADAM:
    #         FLAGS.learning_rate = self.__cfg["optimizer"]["adam"]['learning_rate']
    #     elif name == MOMENTUM:
    #         FLAGS.learning_rate = self.__cfg["optimizer"]["momentum"]['learning_rate']
    #         FLAGS.momentum = self.__cfg["optimizer"]["momentum"]['momentum']
    #         FLAGS.use_locking = self.__cfg["optimizer"]["momentum"]['use_locking']
    #         FLAGS.use_nesterov = self.__cfg["optimizer"]["momentum"]['use_nesterov']
    #     else:
    #         sys.exit('err: no optimizer found!')

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
    s.login('peters_kotlett@hotmail.com', pw)
    s.sendmail(msg['From'], msg['To'], msg.as_string())
    s.quit()
