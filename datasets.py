from typing import Iterator

import torch
import torch.utils.data
from torch.utils.data.dataset import T_co
from pathlib import Path
import numpy as np
import random
import utils


class VideoDataset(torch.utils.data.IterableDataset):
    def __init__(self, root, episode_len):
        self._root = Path(root)
        self._files = list(self._root.iterdir())

        self._episode_len = episode_len

    def _sample(self):
        cam1, cam2 = random.sample([0, 1, 2, 3], k=2)

        videos1, videos2 = random.choices(self._files, k=2)

        video1 = np.load(videos1)[cam1, :self._episode_len]
        video2 = np.load(videos2)[cam2, :self._episode_len]

        video1 = video1.transpose(0, 3, 1, 2).copy()
        video2 = video2.transpose(0, 3, 1, 2).copy()
        return video1, video2

    def __iter__(self) -> Iterator[T_co]:
        while True:
            yield self._sample()
