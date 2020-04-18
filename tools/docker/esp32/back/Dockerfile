FROM ubuntu

# basic
RUN sed -i 's/archive.ubuntu.com/mirrors.aliyun.com/g' /etc/apt/sources.list && \
    sed -i '/security.ubuntu.com/d' /etc/apt/sources.list && \
    apt update && \
    apt upgrade -y && \
    apt install -y curl openssh-server net-tools inetutils-ping && \
    apt install -y apt-utils bison ca-certificates ccache check curl flex git gperf lcov libncurses-dev libusb-1.0-0-dev make ninja-build python3 python3-pip unzip wget xz-utils zip && \
    apt install -y --no-install-recommends vim unzip && \
    apt autoremove -y && \
    rm -rf /var/lib/apt/lists/* && \
    update-alternatives --install /usr/bin/python python /usr/bin/python3 10


RUN python -m pip install --upgrade pip -i https://pypi.tuna.tsinghua.edu.cn/simple && \
    python -m pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple && \
    python -m pip install virtualenv


ENV http_proxy=http://mx-servers:1081
ENV https_proxy=http://mx-servers:1081

RUN git config --global http.proxy $http_proxy && \
    git config --global https.proxy $http_proxy


# openssh service
RUN /etc/init.d/ssh start
EXPOSE 22


# esp32
ENV IDF_PATH=/opt/esp/idf
ENV IDF_TOOLS_PATH=/opt/esp

RUN git clone --recursive https://github.com/espressif/esp-idf.git $IDF_PATH

RUN $IDF_PATH/tools/idf_tools.py --non-interactive install required && \
    $IDF_PATH/tools/idf_tools.py --non-interactive install cmake && \
    $IDF_PATH/tools/idf_tools.py --non-interactive install-python-env && \
    rm -rf $IDF_TOOLS_PATH/dist

ENV IDF_CCACHE_ENABLE=1


ENTRYPOINT [ "source", "${IDF_TOOLS_PATH}/entrypoint.sh" ]
# ENTRYPOINT [ "ping", "127.0.0.1" ]
CMD ["/bin/bash"]
