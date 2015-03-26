# TwTwTellMe

##Servers (Data center: SJC01)

*Mongodb: mongo1.softlayer.com (198.23.76.25/10.88.6.137)

## Import our project as packages
Add path to PYTHONPATH in order to import our project as packages: export PYTHONPATH=/path/to/project:$PYTHONPATH (on your servers)

add \_\_init\_\_.py under the directory which you want to make it a pacakge

##Protobuf
Download from https://developers.google.com/protocol-buffers/docs/downloads

tar -xzvf protobuf***

cd protobuf***

./configure

make

sudo make install

protoc --python_out=$DST_DIR $SRC_DIR/tweet.proto

