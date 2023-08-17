FROM instantngp:latest

ARG DEBIAN_FRONTEND=noninteractive
# https://pytorch.org/get-started/previous-versions/
ARG TORCH_VER=2.0.0
ARG TORCH_VISON_VER=0.15.1
ARG CUDA_VER=11.8.0
ARG PYTHON_VER=3.9.0
ARG PYTHON_VER_MAJOR=39
ARG CUDA_VER_MAJOR=118

ENV PYTHON_INSTALL_DIR /my_python/

# No module named '_lzma'
RUN echo "Installing apt packages..." \
	&& apt -y update --no-install-recommends \
	&& apt -y install --no-install-recommends \
	liblzma-dev

# Install Python
RUN mkdir -p ${PYTHON_INSTALL_DIR} \
    &&  cd ${PYTHON_INSTALL_DIR} \
    &&  wget https://www.python.org/ftp/python/$PYTHON_VER/Python-$PYTHON_VER.tgz \
    &&  tar -xf Python-$PYTHON_VER.tgz \
    &&  rm Python-$PYTHON_VER.tgz \
    &&  cd Python-$PYTHON_VER/ \
    &&  ./configure --enable-optimizations \
    &&  make -j$(nproc) \
    &&  make install

# RUN ln -fs /usr/local/bin/python3 /usr/bin/python \
#     && curl -kL https://bootstrap.pypa.io/get-pip.py | python
RUN ln -fs ${PYTHON_INSTALL_DIR}/Python-${PYTHON_VER}/python /usr/bin/python \
    && curl -kL https://bootstrap.pypa.io/get-pip.py | python 

# https://detectron2.readthedocs.io/en/latest/tutorials/install.html
RUN cd /opt/ \
    &&  pip3 install --upgrade pip setuptools wheel \
    &&  pip3 install torch==${TORCH_VER}+cu${CUDA_VER_MAJOR} torchvision==${TORCH_VISON_VER}+cu${CUDA_VER_MAJOR} --index-url https://download.pytorch.org/whl/cu${CUDA_VER_MAJOR} \
    &&  pip3 install opencv-python numpy tqdm ninja \
    &&  python -m pip install 'git+https://github.com/facebookresearch/detectron2.git'  
    # \
    # &&  pip3 install opencv-python numpy tqdm ninja mediapipe jittor onnxruntime-gpu
    # &&  pip install torch==2.0.0+cu118 torchvision==0.15.1+cu118 --index-url https://download.pytorch.org/whl/cu118 \

# CUDA 11.8
# pip install torch==2.0.0+cu118 torchvision==0.15.1+cu118 torchaudio==2.0.1 --index-url https://download.pytorch.org/whl/cu118
