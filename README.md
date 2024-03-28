# ImMuTe

## Introduction

Due to the limited number of image-music dataset in the field, the work investigates feasible and efficient methods of collecting image-music dataset. A combination of the Google MusicCaps text-music dataset and Stable Diffusion text-to-image Generative AI is applied. The work has succeeded in producing a reliable image-music-text dataset - ImMuTe of size 5521 data pairs for training and testing purposes.



## Download

1. GitHub repository

```bash
git clone https://github.com/juliagsy/immute
```

2. Hugging Face

```python
from datasets import load_dataset
dataset = load_dataset("juliagsy/immute")
```

3. Manual script

Example shown [here](usage.ipynb)



## Usage

```python
from immute.dataset import ImMuTe

immute = ImMuTe("images", "caption.json", "audios", start=0, end=100, sampling_rate=32000, pixel=256)
```
