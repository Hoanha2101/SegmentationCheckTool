import torch
import numpy as np
import torch.nn.functional as F
from ultralytics import YOLO
from torchvision.transforms import GaussianBlur

class Model:
    def __init__(self):
        self.test = None
        self.model = YOLO('./models/ads-seg-s-1280-13052024-2.pt')
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.gaussian_blur = GaussianBlur(101,50)
        self.kernel_size = 101
    @staticmethod
    def resize_mask(mask, image):
        """
        Resize mask to original image size
        Args:
            mask: Torch tensor
            image: Numpy image

        Returns:
            Resized mask
        """
        h, w = mask.shape
        h = h + 5
        w = w + 5
        H, W, _ = image.shape
        if (w, h) == (W, H):
            return mask

        gain = min(w / W, h / H)  # gain  = old / new
        pad = (w - W * gain) / 2, (h - H * gain) / 2  # wh padding
        top, left = int(pad[1]), int(pad[0])  # y, x
        bottom, right = int(h - pad[1]), int(w - pad[0])

        mask = mask[top:bottom, left:right]
        mask = mask[None, None, :, :]
        mask = F.interpolate(mask, size=(H, W))
        mask = mask.squeeze()
        return mask

    def inference(self, image):
        mask = None
        if mask is None:
            result = next(self.model(image, verbose=False, half=True,stream=True,conf=0.6))
            # result = self.model(image)[0]
            masks = result.masks
            if masks is None:
                return image
            mask = torch.any(result.masks.data, dim=0).float()
            mask = self.resize_mask(mask, image)
            # mask = torch.eq(mask, 0.0).int()
            mask = mask.unsqueeze(2).repeat(1, 1, 3)
        image_ = torch.from_numpy(image).cuda().float()
        blur = F.avg_pool2d(image_.permute(2,0,1), kernel_size=self.kernel_size,stride=1, padding=self.kernel_size//2).permute(1,2,0)
        result = (1 - mask) * image_ + mask * blur
        result = result.detach().cpu().numpy()
        result = result.astype(np.uint8)
        return result

model = Model()

def AI(frame):
    return model.inference(frame)

