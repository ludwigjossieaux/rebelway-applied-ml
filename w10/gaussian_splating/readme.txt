https://github.com/NVlabs/instant-ngp

###

activate venv
install requirements.txt

cd instant-ngp
create room.mp4 in ./data/video/room
cd data/video/room

python.exe ..\..\..\scripts\colmap2nerf.py --video_in .\room.mp4 --video_fps 2 --run_colmap --aabb_scale 16