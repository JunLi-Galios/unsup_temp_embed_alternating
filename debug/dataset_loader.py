#!/usr/bin/env python

"""Creating dataset out of video features for different models.
"""

__all__ = ''
__author__ = 'Anna Kukleva'
__date__ = 'December 2018'


from torch.utils.data import Dataset
import torch
import numpy as np

from ute.utils.arg_pars import opt
from ute.utils.logging_setup import logger
from ute.utils.util_functions import join_data


class FeatureDataset(Dataset):
    def __init__(self, videos, features):
        logger.debug('Creating feature dataset')

        self._features = features
        self._gt = None
        # self._videos_features = features
        self._videos = videos

    def __len__(self):
        return len(self._gt)

    def __getitem__(self, idx):
        gt_item = self._gt[idx]
        features = self._features[idx]
        return np.asarray(features), gt_item

    # @staticmethod
    # def _gt_transform(gt):
    #     if opt.model_name == 'tcn':
    #         return np.array(gt)[..., np.newaxis]
    #     if opt.model_name == 'mlp':
    #         return np.array(gt)


class GTDataset(FeatureDataset):
    def __init__(self, videos, features):
        logger.debug('Ground Truth labels')
        super().__init__(videos, features)

        for video in self._videos:
            gt_item = np.asarray(video.gt).reshape((-1, 1))
            # video_features = self._videos_features[video.global_range]
            # video_features = join_data(None, (gt_item, video_features),
            #                            np.hstack)
            self._gt = join_data(self._gt, gt_item, np.vstack)

            # self._features = join_data(self._features, video_features,
            #                            np.vstack)


class RelTimeDataset(FeatureDataset):
    def __init__(self, videos, features):
        logger.debug('Relative time labels')
        super().__init__(videos, features)

        temp_features = None  # used only if opt.concat > 1
        for video in self._videos:
            time_label = np.asarray(video.temp).reshape((-1, 1))
            video_features = self._features[video.global_range]

            temp_features = join_data(temp_features, video_features, np.vstack)

            self._gt = join_data(self._gt, time_label, np.vstack)
            # video_features = join_data(None, (time_label, video_features),
            #                             np.hstack)

class PseudoGTDataset(FeatureDataset):
    def __init__(self, videos, features, pseudo_gt):
        logger.debug('Relative time labels')
        super().__init__(videos, features)

        temp_features = None  # used only if opt.concat > 1
        for video in self._videos:
            
            video_features = self._features[video.global_range]
            video_pseudo_gt = pseudo_gt[video.global_range]

            video_pseudo_gt = np.expand_dims(video_pseudo_gt, axis=1)

            temp_features = join_data(temp_features, video_features, np.vstack)

            self._gt = join_data(self._gt, video_pseudo_gt, np.vstack)
            # video_features = join_data(None, (time_label, video_features),
            #                             np.hstack)

class SingleVideoDataset(FeatureDataset):
    def __init__(self, videos, features, pseudo_gt, video):
        logger.debug('Relative time labels')
        super().__init__(videos, features)

        temp_features = None  # used only if opt.concat > 1
            
        video_features = self._features[video.global_range]
        video_pseudo_gt = pseudo_gt[video.global_range]

        video_pseudo_gt = np.expand_dims(video_pseudo_gt, axis=1)

        temp_features = join_data(temp_features, video_features, np.vstack)

        self._gt = join_data(self._gt, video_pseudo_gt, np.vstack)


class ASALVideoDataset(FeatureDataset):
    def __init__(self, videos, features, pseudo_gt):
        logger.debug('ASAL')
        super().__init__(videos, features)

        temp_features = None  # used only if opt.concat > 1
        temp_features = join_data(temp_features, features, np.vstack)

        self._gt = pseudo_gt


def load_ground_truth(videos, features, shuffle=True):
    logger.debug('load data with ground truth labels for training some embedding')

    dataset = GTDataset(videos, features)
    dataloader = torch.utils.data.DataLoader(dataset, batch_size=opt.batch_size,
                                             shuffle=shuffle,
                                             num_workers=opt.num_workers)
    return dataloader


def load_reltime(videos, features, shuffle=True):
    logger.debug('load data with temporal labels as ground truth')
    torch.manual_seed(opt.seed)
    np.random.seed(opt.seed)

    if opt.model_name == 'mlp':
        dataset = RelTimeDataset(videos, features)
    if opt.model_name == 'tcn':
        dataset = TCNDataset(videos, features)
    dataloader = torch.utils.data.DataLoader(dataset, batch_size=opt.batch_size,
                                             shuffle=shuffle,
                                             num_workers=opt.num_workers)

    return dataloader


def load_pseudo_gt(videos, features, pseudo_gt, shuffle=True):
    logger.debug('load data with pseudo ground truth')
    torch.manual_seed(opt.seed)
    np.random.seed(opt.seed)

    dataset = PseudoGTDataset(videos, features, pseudo_gt)
    dataloader = torch.utils.data.DataLoader(dataset, batch_size=opt.batch_size,
                                             shuffle=shuffle,
                                             num_workers=opt.num_workers)

    return dataloader

def load_single_video(videos, features, pseudo_gt, video, shuffle=True):
    logger.debug('load data with single video dataset')
    torch.manual_seed(opt.seed)
    np.random.seed(opt.seed)

    dataset = SingleVideoDataset(videos, features, pseudo_gt, video)
    dataloader = torch.utils.data.DataLoader(dataset, batch_size=opt.batch_size,
                                             shuffle=shuffle,
                                             num_workers=opt.num_workers)

    return dataloader


def load_asal_dataset(videos, features, pseudo_gt, shuffle=True):
    logger.debug('load data with asal')
    torch.manual_seed(opt.seed)
    np.random.seed(opt.seed)

    dataset = ASALVideoDataset(videos, features, pseudo_gt)
    dataloader = torch.utils.data.DataLoader(dataset, batch_size=20,
                                             shuffle=shuffle,
                                             num_workers=opt.num_workers)

    return dataloader
