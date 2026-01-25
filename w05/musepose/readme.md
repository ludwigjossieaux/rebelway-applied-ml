https://github.com/TMElyralab/MusePose

----

sudo apt install libavformat-dev libavdevice-dev

git clone https://github.com/TMElyralab/MusePose
cd MusePose
remove .git folder
uv venv --python 3.11
source .venv/bin/activate


# specific to blackwell
uv pip uninstall torch torchvision
uv pip install -r requirements.txt
uv pip install torch==2.7.0+cu128 torchvision --index-url https://download.pytorch.org/whl/cu128
uv pip install --no-cache-dir -U openmim "numpy<2"

mim install mmengine 
mim install "mmcv==2.1.0" 
mim install "mmdet==3.2.0"
uv pip install chumpy --no-build-isolation
mim install "mmpose>=1.1.0" 

# or fix : https://gitee.com/Wilson_Lws/MuseTalk-50Series-Adaptation/blob/master/README.md
mim install mmengine 
mim install "mmcv-full==1.7.2"
mim install "mmdet==3.2.0"
uv pip install chumpy --no-build-isolation
mim install "mmpose==1.3.2"

# modify mmcv_minimum_version from 2.0.0rc4 to 1.7.2
# in .venv/lib/python3.11/site-packages/mmpose/__init__.py
# in .venv/lib/python3.11/site-packages/mmdet/__init__.py

