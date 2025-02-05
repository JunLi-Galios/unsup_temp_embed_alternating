#!/usr/bin/env python

"""Implementation and improvement of the paper:
Unsupervised learning and segmentation of complex activities from video.
"""

__author__ = 'Anna Kukleva'
__date__ = 'June 2019'

import sys
import os
sys.path.append(os.path.abspath('.').split('data_utils')[0])
sys.path.append('/scratch/liju2/unsupervised_AS/unsup_temp_embed_learned_classifier')

from ute.utils.arg_pars import opt
from data_utils.BF_utils.update_argpars import update
from ute.ute_pipeline import temp_embed, all_actions

if __name__ == '__main__':

    # set root
    opt.dataset_root = '/scratch/liju2/data/us_as/Breakfast'

    # set one of  activity
    #['coffee', 'cereals', 'tea', 'milk', 'juice', 'sandwich', 'scrambledegg', 'friedegg', 'salat', 'pancake']
    # all
    opt.subaction = 'juice'
    # set feature extension and dimensionality
    opt.ext = 'txt'
    opt.feature_dim = 64

    # model name can be 'mlp' or 'nothing' for no embedding (just raw features)
    opt.model_name = 'mlp'

    # load an already trained model (stored in the models directory in dataset_root)
    opt.load_model = True
    opt.loaded_model_name = '%s.pth.tar'

    # update log name and absolute paths
    update()

    # run temporal embedding
    if opt.subaction == 'all':
        actions = ['coffee', 'cereals', 'tea', 'milk', 'juice', 'sandwich', 'scrambledegg', 'friedegg', 'salat',
                   'pancake']
        all_actions(actions)
    else:
        temp_embed()


