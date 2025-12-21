# rebelway-applied-ml
Repo for the Applied ML course for Rebelway
https://github.com/pixelknit/rebelwayAppliedML

# env setup

edit "C:\Users\<user>\Documents\houdini21.0\houdini.env"
add :
PYTHONPATH = "C:\Users\<user>\.conda\envs\houdini\Lib\site-packages"

# install package

open "Anaconda Prompt"
conda activate houdini
pip install torch


######

mediapipe specific (numpy < 2 !)

uv venv .venv-mediapipe --python 3.12
.\.venv-mediapipe\Scripts\activate
uv pip install mediapipe==0.10.21

######

reduce video size
.\ffmpeg.exe -i .\smile.mp4 -vf scale=640:-1 .\smile_640.mp4