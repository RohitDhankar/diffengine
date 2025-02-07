from diffusers import UNet2DConditionModel
from diffusers.loaders import text_encoder_lora_state_dict
from transformers import CLIPTextModel

from diffengine.models.archs import (set_text_encoder_lora, set_unet_lora,
                                     unet_attn_processors_state_dict)
from diffengine.models.editors import SDDataPreprocessor, StableDiffusion


def test_set_lora():
    unet = UNet2DConditionModel.from_pretrained(
        'diffusers/tiny-stable-diffusion-torch', subfolder='unet')
    assert not any(['processor' in k for k in unet.state_dict().keys()])
    set_unet_lora(unet, config={})
    assert any(['processor' in k for k in unet.state_dict().keys()])

    text_encoder = CLIPTextModel.from_pretrained(
        'diffusers/tiny-stable-diffusion-torch', subfolder='text_encoder')
    assert not any(
        ['lora_linear_layer' in k for k in text_encoder.state_dict().keys()])
    set_text_encoder_lora(text_encoder, config={})
    assert any(
        ['lora_linear_layer' in k for k in text_encoder.state_dict().keys()])


def test_unet_lora_layers_to_save():
    model = StableDiffusion(
        'diffusers/tiny-stable-diffusion-torch',
        lora_config=dict(rank=4),
        finetune_text_encoder=True,
        data_preprocessor=SDDataPreprocessor())
    unet_lora_layers_to_save = unet_attn_processors_state_dict(model.unet)
    text_encoder_lora_layers_to_save = text_encoder_lora_state_dict(
        model.text_encoder)
    assert len(unet_lora_layers_to_save) > 0
    assert len(text_encoder_lora_layers_to_save) > 0
