FROM instantngp:latest

ARG DEBIAN_FRONTEND=noninteractive

# install xeyes, glxgears for debug x11 gui, and install vulkan
RUN echo "Installing apt packages..." \
	# && export DEBIAN_FRONTEND=noninteractive \
    && apt-get update \
    && apt-get install -y --no-install-recommends \
        x11-apps \
        libgl1-mesa-glx \
        vulkan-tools \
        mesa-vulkan-drivers \
        libvulkan-dev \
        libvulkan1 \
        vulkan-validationlayers-dev \
        spirv-tools \
        vulkan-validationlayers \
    && apt autoremove -y \
	&& apt clean -y 


# mesa-vulkan-drivers is for AMD and Intel GPUs, so do not install that unless you have those
# https://askubuntu.com/questions/1329597/need-help-for-installing-vulkan-on-ubuntu-18-04

# https://github.com/gorgonia/vulkan/blob/master/docker/Dockerfile
# Install the Vulkan SDK to get access to glslc to compile the shaders
# https://vulkan.lunarg.com/doc/view/latest/linux/getting_started_ubuntu.html
# Ubuntu 20.04 (Focal Fossa)
# https://forums.unrealengine.com/t/ubuntu-18-cannot-find-compatible-vulkan-driver-icd/444041/8
ENV VULKAN_INSTALL_DIR /my_vulkan/
RUN mkdir -p ${VULKAN_INSTALL_DIR} \
    && cd ${VULKAN_INSTALL_DIR} \
    && wget -qO - https://packages.lunarg.com/lunarg-signing-key-pub.asc | apt-key add - \
    && wget -qO /etc/apt/sources.list.d/lunarg-vulkan-focal.list https://packages.lunarg.com/vulkan/lunarg-vulkan-focal.list \
    && apt update -y \
    && apt-get install -y vulkan-sdk \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# RUN vulkaninfo
# RUN vkcube
# RUN apt-get update \
#     && apt-get install -y --no-install-recommends \
#     vulkan-validationlayers-dev spirv-tools vulkan-validationlayers

# Set the environment variables for the Vulkan SDK
# ENV VULKAN_SDK=/usr/local/share/vulkan
# ENV PATH=$VULKAN_SDK/bin:$PATH
# ENV LD_LIBRARY_PATH=$VULKAN_SDK/lib:$LD_LIBRARY_PATH
# ENV VK_LAYER_PATH=$VULKAN_SDK/etc/vulkan/explicit_layer.d
# ENV VK_LAYER_PATH=/usr/lib/x86_64-linux-gnu/vulkan/layer/
# ENV VK_LAYER_PATH=/usr/share/vulkan/explicit_layer.d
