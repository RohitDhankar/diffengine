# Distill SD DreamBooth

[On Architectural Compression of Text-to-Image Diffusion Models](https://arxiv.org/abs/2305.15798)

## Abstract

Exceptional text-to-image (T2I) generation results of Stable Diffusion models (SDMs) come with substantial computational demands. To resolve this issue, recent research on efficient SDMs has prioritized reducing the number of sampling steps and utilizing network quantization. Orthogonal to these directions, this study highlights the power of classical architectural compression for general-purpose T2I synthesis by introducing block-removed knowledge-distilled SDMs (BK-SDMs). We eliminate several residual and attention blocks from the U-Net of SDMs, obtaining over a 30% reduction in the number of parameters, MACs per sampling step, and latency. We conduct distillation-based pretraining with only 0.22M LAION pairs (fewer than 0.1% of the full training pairs) on a single A100 GPU. Despite being trained with limited resources, our compact models can imitate the original SDM by benefiting from transferred knowledge and achieve competitive results against larger multi-billion parameter models on the zero-shot MS-COCO benchmark. Moreover, we demonstrate the applicability of our lightweight pretrained models in personalized generation with DreamBooth finetuning.

<div align=center>
<img src="https://github.com/okotaku/diffengine/assets/24734142/253c0dfb-fa1c-4cbf-81c0-9d6948d40413"/>
</div>

## Citation

## Run Training

Run Training

```
# single gpu
$ mim train diffengine ${CONFIG_FILE}
# multi gpus
$ mim train diffengine ${CONFIG_FILE} --gpus 2 --launcher pytorch

# Example.
$ mim train diffengine configs/distill_sd_dreambooth/small_sd_dreambooth_lora_dog.py
```

## Training Speed

Environment:

- A6000 Single GPU
- nvcr.io/nvidia/pytorch:23.07-py3

Settings:

- 1k iterations training, (validation 4 images / 100 iterations)
- LoRA (rank=8) / DreamBooth

|  Model   | total time |
| :------: | :--------: |
|  SDV1.5  | 16 m 39 s  |
| Small SD | 11 m 57 s  |
| Tiny SD  | 11 m 17 s  |

## Inference with diffusers

Once you have trained a model, specify the path to where the model is saved, and use it for inference with the `diffusers`.

```py
import torch
from diffusers import DiffusionPipeline

checkpoint = 'work_dirs/small_sd_dreambooth_lora_dog/step999'
prompt = 'A photo of sks dog in a bucket'

pipe = DiffusionPipeline.from_pretrained(
    'segmind/small-sd', torch_dtype=torch.float16)
pipe.to('cuda')
pipe.load_lora_weights(checkpoint)

image = pipe(
    prompt,
    num_inference_steps=50,
).images[0]
image.save('demo.png')
```

We also provide inference demo scripts:

```bash
$ mim run diffengine demo_lora "A photo of sks dog in a bucket" work_dirs/small_sd_dreambooth_lora_dog/step999 --sdmodel segmind/small-sd
```

## Results Example

#### small_sd_dreambooth_lora_dog

![example1](https://github.com/okotaku/diffengine/assets/24734142/16cc3ef2-860d-4e4a-8b1d-8f56d9021db9)

We uploaded pretrained checkpoint on [`takuoko/small-sd-dreambooth-lora-dog`](https://huggingface.co/takuoko/small-sd-dreambooth-lora-dog).

#### tiny_sd_dreambooth_lora_dog

![example2](https://github.com/okotaku/diffengine/assets/24734142/2d7f3f20-fff4-41f1-9b17-be7b19129769)

Note that the result of tiny sd is not good.

## Reference

- [Open-sourcing Knowledge Distillation Code and Weights of SD-Small and SD-Tiny](https://huggingface.co/blog/sd_distillation)
