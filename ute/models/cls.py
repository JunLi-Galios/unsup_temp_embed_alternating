#!/usr/bin/env python

"""Baseline for relative time embedding: learn regression model in terms of
relative time.
"""

__author__ = 'Anna Kukleva'
__date__ = 'September 2018'

import torch
import torch.nn as nn
from torch.nn import functional as F

from ute.utils.arg_pars import opt
from ute.utils.logging_setup import logger


class CLS(nn.Module):
    def __init__(self, K):
        super(CLS, self).__init__()

        self._K = K

        self.fc = nn.Linear(opt.embed_dim, opt.embed_dim * 2)
        self.out_fc = nn.Linear(opt.embed_dim * 2, self._K)
        self._init_weights()

    def forward(self, x):
        output = F.relu(self.fc(x))
        output = self.out_fc(output)
        output = nn.functional.log_softmax(output, dim=1)

        return output

    def _init_weights(self):
        for m in self.modules():
            if isinstance(m, nn.Linear):
                nn.init.normal_(m.weight, 0, 0.01)
                nn.init.constant_(m.bias, 0)


def create_model(K):
    torch.manual_seed(opt.seed)
    model = CLS(K).to(opt.device)
    loss = nn.NLLLoss()
    # loss = nn.MSELoss().cuda()
    optimizer = torch.optim.Adam(model.parameters(),
                                 lr=opt.lr * 0.1,
                                 weight_decay=opt.weight_decay)
    logger.debug(str(model))
    logger.debug(str(loss))
    logger.debug(str(optimizer))
    return model, loss, optimizer

