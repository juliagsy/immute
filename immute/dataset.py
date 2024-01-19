from PIL import Image
import torch
import torchvision.transforms as transforms
import torchaudio
from torch.utils.data import Dataset
import json

class ImMuTe(Dataset):

    def __init__(self, images_path, captions_json_file, audios_path, start=0, end=2999, sampling_rate=16000, pixel=64, normalize=False):
        super().__init__()
        self.images_path = images_path
        self.captions_json_file = captions_json_file
        self.audios_path = audios_path
        self.sampling_rate = sampling_rate

        # define transform to convert image to tensors
        transform = [
            transforms.Resize(pixel),
            transforms.ToTensor(),
        ]
        if normalize:
          transform.append(transforms.Normalize([0.5], [0.5]))

        self.transform = transforms.Compose(transform)

        # load captions
        with open(self.captions_json_file, "r", encoding='utf-8') as f:
            caps_dict = json.load(f)

        # preload all data in a dict
        self.all_data = {}
        index = 0
        for i in range(len(caps_dict)):
            if i < start:
              continue
            if i > end:
              break
            try:
              # load audio
              wav, sr = torchaudio.load(f"{self.audios_path}/aud_{i}.wav")
              wav = torchaudio.functional.resample(wav, orig_freq=sr, new_freq=self.sampling_rate)
              wav = torch.mean(wav, dim=0, keepdim=True)
              if wav.size(-1) < self.sampling_rate * 10:
                  pad_len = self.sampling_rate * 10 - wav.size(-1)
                  wav = torchfunc.pad(wav, (0, pad_len))

              # transform image
              img = Image.open(f"{self.images_path}/test_{i}.png")
              img = self.transform(img)

              # index image-text pair and save them to dict
              self.all_data[index] = (wav, img, caps_dict[str(i)])
              index += 1
            except:
                continue


    def __len__(self):

        # get total length of dataset
        length = len(self.all_data)

        return length

    def __getitem__(self, idx):

        # get image-text pair by index
        wav, img, txt = self.all_data[idx]

        return (wav, img, txt)
