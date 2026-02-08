uv venv retina-venv --python 3.11
.\retina-venv\Scripts\activate
uv pip install "tensorflow==2.15.*" "keras==2.15.*" --prerelease=allow
uv pip install deepface
uv pip install torch torchvision --index-url https://download.pytorch.org/whl/cu130
uv pip install matplotlib
uv pip install timm
uv pip install scikit-learn