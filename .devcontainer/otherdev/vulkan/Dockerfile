FROM instantngp:latest

# install xeyes, glxgears for debug x11 gui, and install vulkan
RUN echo "Installing apt packages..." \
	&& export DEBIAN_FRONTEND=noninteractive \
    && apt-get update \
    && apt-get install -y --no-install-recommends \
        x11-apps \
        libgl1-mesa-glx \
        vulkan-tools \
        libvulkan-dev \
        vulkan-validationlayers-dev \
        spirv-tools \
    && apt autoremove -y \
	&& apt clean -y 

# https://github.com/gorgonia/vulkan/blob/master/docker/Dockerfile
# Install the Vulkan SDK to get access to glslc to compile the shaders
RUN wget -qO - https://packages.lunarg.com/lunarg-signing-key-pub.asc | apt-key add - \
    && wget -qO /etc/apt/sources.list.d/lunarg-vulkan-focal.list https://packages.lunarg.com/vulkan/lunarg-vulkan-focal.list \
    && apt update -y \
    && apt-get install -y vulkan-sdk
