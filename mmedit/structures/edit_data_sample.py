# Copyright (c) OpenMMLab. All rights reserved.
from numbers import Number
from typing import Sequence, Union

import mmengine
import numpy as np
import torch
from mmengine.structures import BaseDataElement, LabelData

from .pixel_data import PixelData


def format_label(value: Union[torch.Tensor, np.ndarray, Sequence, int],
                 num_classes: int = None) -> LabelData:
    """Convert label of various python types to :obj:`mmengine.LabelData`.

    Supported types are: :class:`numpy.ndarray`, :class:`torch.Tensor`,
    :class:`Sequence`, :class:`int`.

    Args:
        value (torch.Tensor | numpy.ndarray | Sequence | int): Label value.
        num_classes (int, optional): The number of classes. If not None, set
            it to the metainfo. Defaults to None.

    Returns:
        :obj:`mmengine.LabelData`: The foramtted label data.
    """

    # Handle single number
    if isinstance(value, (torch.Tensor, np.ndarray)) and value.ndim == 0:
        value = int(value.item())

    if isinstance(value, np.ndarray):
        value = torch.from_numpy(value)
    elif isinstance(value, Sequence) and not mmengine.is_str(value):
        value = torch.tensor(value)
    elif isinstance(value, int):
        value = torch.LongTensor([value])
    elif not isinstance(value, torch.Tensor):
        raise TypeError(f'Type {type(value)} is not an available label type.')

    metainfo = {}
    if num_classes is not None:
        metainfo['num_classes'] = num_classes
        if value.max() >= num_classes:
            raise ValueError(f'The label data ({value}) should not '
                             f'exceed num_classes ({num_classes}).')
    label = LabelData(label=value, metainfo=metainfo)
    return label


class EditDataSample(BaseDataElement):
    """A data structure interface of MMEditing. They are used as interfaces
    between different components.

    The attributes in ``EditDataSample`` are divided into several parts:

        - ``gt_img``: Ground truth image(s).
        - ``pred_img``: Image(s) of model predictions.
        - ``ref_img``: Reference image(s).
        - ``mask``: Mask in Inpainting.
        - ``trimap``: Trimap in Matting.
        - ``gt_alpha``: Ground truth alpha image in Matting.
        - ``pred_alpha``: Predicted alpha image in Matting.
        - ``gt_fg``: Ground truth foreground image in Matting.
        - ``pred_fg``: Predicted foreground image in Matting.
        - ``gt_bg``: Ground truth background image in Matting.
        - ``pred_bg``: Predicted background image in Matting.
        - ``gt_merged``: Ground truth merged image in Matting.

    Examples:
         >>> import torch
         >>> import numpy as np
         >>> from mmedit.structures import EditDataSample, PixelData
         >>> data_sample = EditDataSample()
         >>> img_meta = dict(img_shape=(800, 1196, 3))
         >>> img = torch.rand((3, 800, 1196))
         >>> gt_img = PixelData(data=img, metainfo=img_meta)
         >>> data_sample.gt_img = gt_img
         >>> assert 'img_shape' in data_sample.gt_img.metainfo_keys()
        <EditDataSample(

            META INFORMATION

            DATA FIELDS
            _gt_img: <PixelData(

                    META INFORMATION
                    img_shape: (800, 1196, 3)

                    DATA FIELDS
                    data: tensor([[[0.8069, 0.4279,  ..., 0.6603, 0.0292],

                                ...,

                                [0.8139, 0.0908,  ..., 0.4964, 0.9672]]])
                ) at 0x1f6ae000af0>
            gt_img: <PixelData(

                    META INFORMATION
                    img_shape: (800, 1196, 3)

                    DATA FIELDS
                    data: tensor([[[0.8069, 0.4279,  ..., 0.6603, 0.0292],

                                ...,

                                [0.8139, 0.0908,  ..., 0.4964, 0.9672]]])
                ) at 0x1f6ae000af0>
        ) at 0x1f6a5a99a00>
    """

    @property
    def gt_img(self) -> PixelData:
        return self._gt_img

    @gt_img.setter
    def gt_img(self, value: PixelData):
        self.set_field(value, '_gt_img', dtype=PixelData)

    @gt_img.deleter
    def gt_img(self):
        del self._gt_img

    @property
    def gt_samples(self) -> 'EditDataSample':
        return self._gt_samples

    @gt_samples.setter
    def gt_samples(self, value: 'EditDataSample'):
        self.set_field(value, '_gt_samples', dtype=EditDataSample)

    @gt_samples.deleter
    def gt_samples(self):
        del self._gt_samples

    @property
    def noise(self) -> torch.Tensor:
        return self._noise

    @noise.setter
    def noise(self, value: PixelData):
        self.set_field(value, '_noise', dtype=torch.Tensor)

    @noise.deleter
    def noise(self):
        del self._noise

    @property
    def pred_img(self) -> PixelData:
        return self._pred_img

    @pred_img.setter
    def pred_img(self, value: PixelData):
        self.set_field(value, '_pred_img', dtype=PixelData)

    @pred_img.deleter
    def pred_img(self):
        del self._pred_img

    @property
    def fake_img(self) -> PixelData:
        return self._fake_img

    @fake_img.setter
    def fake_img(self, value: PixelData):
        self.set_field(value, '_fake_img', dtype=PixelData)

    @fake_img.deleter
    def fake_img(self):
        del self._fake_img

    @property
    def img_lq(self) -> PixelData:
        return self._img_lq

    @img_lq.setter
    def img_lq(self, value: PixelData):
        self.set_field(value, '_img_lq', dtype=PixelData)

    @img_lq.deleter
    def img_lq(self):
        del self._img_lq

    @property
    def ref_img(self) -> PixelData:
        return self._ref_img

    @ref_img.setter
    def ref_img(self, value: PixelData):
        self.set_field(value, '_ref_img', dtype=PixelData)

    @ref_img.deleter
    def ref_img(self):
        del self._ref_img

    @property
    def ref_lq(self) -> PixelData:
        return self._ref_lq

    @ref_lq.setter
    def ref_lq(self, value: PixelData):
        self.set_field(value, '_ref_lq', dtype=PixelData)

    @ref_lq.deleter
    def ref_lq(self):
        del self._ref_lq

    @property
    def gt_unsharp(self) -> PixelData:
        return self._gt_unsharp

    @gt_unsharp.setter
    def gt_unsharp(self, value: PixelData):
        self.set_field(value, '_gt_unsharp', dtype=PixelData)

    @gt_unsharp.deleter
    def gt_unsharp(self):
        del self._gt_unsharp

    @property
    def mask(self) -> PixelData:
        return self._mask

    @mask.setter
    def mask(self, value: PixelData):
        self.set_field(value, '_mask', dtype=PixelData)

    @mask.deleter
    def mask(self):
        del self._mask

    @property
    def gt_heatmap(self) -> PixelData:
        return self._gt_heatmap

    @gt_heatmap.setter
    def gt_heatmap(self, value: PixelData):
        self.set_field(value, '_gt_heatmap', dtype=PixelData)

    @gt_heatmap.deleter
    def gt_heatmap(self):
        del self._gt_heatmap

    @property
    def pred_heatmap(self) -> PixelData:
        return self._pred_heatmap

    @pred_heatmap.setter
    def pred_heatmap(self, value: PixelData):
        self.set_field(value, '_pred_heatmap', dtype=PixelData)

    @pred_heatmap.deleter
    def pred_heatmap(self):
        del self._pred_heatmap

    @property
    def trimap(self) -> PixelData:
        return self._trimap

    @trimap.setter
    def trimap(self, value: PixelData):
        self.set_field(value, '_trimap', dtype=PixelData)

    @trimap.deleter
    def trimap(self):
        del self._trimap

    @property
    def gt_alpha(self) -> PixelData:
        return self._gt_alpha

    @gt_alpha.setter
    def gt_alpha(self, value: PixelData):
        self.set_field(value, '_gt_alpha', dtype=PixelData)

    @gt_alpha.deleter
    def gt_alpha(self):
        del self._gt_alpha

    @property
    def pred_alpha(self) -> PixelData:
        return self._pred_alpha

    @pred_alpha.setter
    def pred_alpha(self, value: PixelData):
        self.set_field(value, '_pred_alpha', dtype=PixelData)

    @pred_alpha.deleter
    def pred_alpha(self):
        del self._pred_alpha

    @property
    def gt_fg(self) -> PixelData:
        return self._gt_fg

    @gt_fg.setter
    def gt_fg(self, value: PixelData):
        self.set_field(value, '_gt_fg', dtype=PixelData)

    @gt_fg.deleter
    def gt_fg(self):
        del self._gt_fg

    @property
    def pred_fg(self) -> PixelData:
        return self._pred_fg

    @pred_fg.setter
    def pred_fg(self, value: PixelData):
        self.set_field(value, '_pred_fg', dtype=PixelData)

    @pred_fg.deleter
    def pred_fg(self):
        del self._pred_fg

    @property
    def gt_bg(self) -> PixelData:
        return self._gt_bg

    @gt_bg.setter
    def gt_bg(self, value: PixelData):
        self.set_field(value, '_gt_bg', dtype=PixelData)

    @gt_bg.deleter
    def gt_bg(self):
        del self._gt_bg

    @property
    def pred_bg(self) -> PixelData:
        return self._pred_bg

    @pred_bg.setter
    def pred_bg(self, value: PixelData):
        self.set_field(value, '_pred_bg', dtype=PixelData)

    @pred_bg.deleter
    def pred_bg(self):
        del self._pred_bg

    @property
    def gt_merged(self) -> PixelData:
        return self._gt_merged

    @gt_merged.setter
    def gt_merged(self, value: PixelData):
        self.set_field(value, '_gt_merged', dtype=PixelData)

    @gt_merged.deleter
    def gt_merged(self):
        del self._gt_merged

    @property
    def sample_model(self) -> str:
        return self._sample_model

    @sample_model.setter
    def sample_model(self, value: str):
        self.set_field(value, '_sample_model', dtype=str)

    @sample_model.deleter
    def sample_model(self):
        del self._sample_model

    @property
    def ema(self) -> 'EditDataSample':
        return self._ema

    @ema.setter
    def ema(self, value: 'EditDataSample'):
        self.set_field(value, '_ema', dtype=EditDataSample)

    @ema.deleter
    def ema(self):
        del self._ema

    @property
    def orig(self) -> 'EditDataSample':
        return self._orig

    @orig.setter
    def orig(self, value: 'EditDataSample'):
        self.set_field(value, '_orig', dtype=EditDataSample)

    @orig.deleter
    def orig(self):
        del self._orig

    def set_gt_label(
        self, value: Union[np.ndarray, torch.Tensor, Sequence[Number], Number]
    ) -> 'EditDataSample':
        """Set label of ``gt_label``."""
        label = format_label(value, self.get('num_classes'))
        if 'gt_label' in self:
            self.gt_label.label = label.label
        else:
            self.gt_label = label
        return self

    @property
    def gt_label(self):
        return self._gt_label

    @gt_label.setter
    def gt_label(self, value: LabelData):
        self.set_field(value, '_gt_label', dtype=LabelData)

    @gt_label.deleter
    def gt_label(self):
        del self._gt_label
