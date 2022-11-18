# ------------------------------------------------------------
# install mininet
# ------------------------------------------------------------
git clone https://github.com/mininet/mininet
cd mininet
# git tag  # list available versions
git checkout -b mininet-2.3.0 2.3.0  # or whatever version you wish to install
cd ..
# mininet/util/install.sh -n3fw
mininet/util/install.sh -a

rm -rf mininet/

sudo apt -y install openvswitch-switch
sudo service openvswitch-switch start

# ------------------------------------------------------------
# install FRR
# ------------------------------------------------------------
sudo apt install -y frr

# ## installing Dependencies
# # sudo apt update -y
# sudo apt-get install -y \
#    git autoconf automake libtool make libreadline-dev texinfo \
#    pkg-config libpam0g-dev libjson-c-dev bison flex \
#    libc-ares-dev python3-dev python3-sphinx \
#    install-info build-essential libsnmp-dev perl \
#    libcap-dev python2 libelf-dev libunwind-dev

# ## install libyang
# sudo apt install -y cmake
# git clone https://github.com/CESNET/libyang.git
# cd libyang
# git checkout v2.0.0
# mkdir build; cd build
# cmake -D CMAKE_INSTALL_PREFIX:PATH=/usr \
#       -D CMAKE_BUILD_TYPE:String="Release" ..
# make
# sudo make install
# cd ../../
# rm -rf libyang

# ## install Protobuf
# sudo apt-get install -y protobuf-c-compiler libprotobuf-c-dev

# ## install ZeroMQ
# sudo apt-get install -y libzmq5 libzmq3-dev

# ## Add FRR user and groups
# sudo groupadd -r -g 92 frr
# sudo groupadd -r -g 85 frrvty
# sudo adduser --system --ingroup frr --home /var/run/frr/ \
#    --gecos "FRR suite" --shell /sbin/nologin frr
# sudo usermod -a -G frrvty frr

# ## install FRR
# git clone https://github.com/frrouting/frr.git frr
# cd frr
# ./bootstrap.sh
# ./configure \
#     --prefix=/usr \
#     --includedir=\${prefix}/include \
#     --bindir=\${prefix}/bin \
#     --sbindir=\${prefix}/lib/frr \
#     --libdir=\${prefix}/lib/frr \
#     --libexecdir=\${prefix}/lib/frr \
#     --localstatedir=/var/run/frr \
#     --sysconfdir=/etc/frr \
#     --with-moduledir=\${prefix}/lib/frr/modules \
#     --with-libyang-pluginsdir=\${prefix}/lib/frr/libyang_plugins \
#     --enable-configfile-mask=0640 \
#     --enable-logfile-mask=0640 \
#     --enable-snmp=agentx \
#     --enable-multipath=64 \
#     --enable-user=frr \
#     --enable-group=frr \
#     --enable-vty-group=frrvty \
#     --with-pkg-git-version 
# make
# sudo make install
# cd ..
# rm -rf frr/