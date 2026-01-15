#!/bin/bash

cd MusePose/pretrained_weights
if [ ! -d "MusePose" ]; then
    mkdir -p MusePose dwpose sd-image-variations-diffusers sd-image-variations-diffusers/unet image_encoder sd-vae-ft-mse control_v11p_sd15_openpose animatediff
else
    echo "MusePose folders already exist. Skipping creation."
fi

# Download MusePose weights
if [ ! -f "MusePose/denoising_unet.pth" ]; then
    wget -O MusePose/denoising_unet.pth https://huggingface.co/TMElyralab/MusePose/resolve/main/MusePose/denoising_unet.pth
    wget -O MusePose/motion_module.pth https://huggingface.co/TMElyralab/MusePose/resolve/main/MusePose/motion_module.pth
    wget -O MusePose/pose_guider.pth https://huggingface.co/TMElyralab/MusePose/resolve/main/MusePose/pose_guider.pth
    wget -O MusePose/reference_unet.pth https://huggingface.co/TMElyralab/MusePose/resolve/main/MusePose/denoising_unet.pth
else
    echo "MusePose weights already downloaded. Skipping download."
fi

# Download dwpose weights
if [ ! -f "dwpose/dw-ll_ucoco_384.pth" ]; then
    wget -O dwpose/dw-ll_ucoco_384.pth https://huggingface.co/yzd-v/DWPose/resolve/main/dw-ll_ucoco_384.pth
    wget -O dwpose/yolox_l_8x8_300e_coco.pth https://huggingface.co/Shuaishuai0219/Animate-X/resolve/fec01be641c50e07614ced47d6e9d7deb8b522dc/yolox_l_8x8_300e_coco.pth
else
    echo "dwpose weights already downloaded. Skipping download."
fi

# Download SD Image Variations Diffusers weights
if [ ! -f "sd-image-variations-diffusers/unet/config.json" ]; then
    wget -O sd-image-variations-diffusers/unet/config.json https://huggingface.co/lambdalabs/sd-image-variations-diffusers/resolve/main/unet/config.json
    wget -O sd-image-variations-diffusers/unet/diffusion_pytorch_model.bin https://huggingface.co/lambdalabs/sd-image-variations-diffusers/resolve/main/unet/diffusion_pytorch_model.bin
else
    echo "SD Image Variations Diffusers weights already downloaded. Skipping download."
fi

# Download Image Encoder weights
if [ ! -f "image_encoder/config.json" ]; then
    wget -O image_encoder/config.json https://huggingface.co/lambdalabs/sd-image-variations-diffusers/resolve/main/image_encoder/config.json
    wget -O image_encoder/pytorch_model.bin https://huggingface.co/lambdalabs/sd-image-variations-diffusers/resolve/main/image_encoder/pytorch_model.bin
else
    echo "Image Encoder weights already downloaded. Skipping download."
fi

# Download SD VAE weights
if [ ! -f "sd-vae-ft-mse/config.json" ]; then
    wget -O sd-vae-ft-mse/config.json https://huggingface.co/stabilityai/sd-vae-ft-mse/resolve/main/config.json
    wget -O sd-vae-ft-mse/diffusion_pytorch_model.bin https://huggingface.co/stabilityai/sd-vae-ft-mse/resolve/main/diffusion_pytorch_model.bin
else
    echo "SD VAE weights already downloaded. Skipping download."
fi

# Download ControlNet OpenPose weights
if [ ! -f "control_v11p_sd15_openpose/diffusion_pytorch_model.bin" ]; then
    wget -O control_v11p_sd15_openpose/diffusion_pytorch_model.bin https://huggingface.co/lllyasviel/control_v11p_sd15_openpose/resolve/main/diffusion_pytorch_model.bin
else
    echo "ControlNet OpenPose weights already downloaded. Skipping download."
fi

# Download AnimateDiff weights
if [ ! -f "animatediff/mm_sd_v15_v2.ckpt" ]; then
    wget -O animatediff/mm_sd_v15_v2.ckpt https://huggingface.co/guoyww/animatediff/resolve/main/mm_sd_v15_v2.ckpt
else
    echo "AnimateDiff weights already downloaded. Skipping download."
fi

echo "All weights have been downloaded and are ready for use."