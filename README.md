# Module gRPC - Market 
Platform gRPC Integration Module to communicate with Market Module.

## Git
Clone this repository:
```shell
git clone https://github.com/Emb3rs-Project/m-grpc-market.git
```

Load submodules:
```shell
git submodule init
git submodule update
```

## Setup Local Environment
Create Conda environment and install packages:
```shell
conda env create -n market-grpc-module -f environment-py39.yml
conda activate market-grpc-module
```

Create environment variables config file:
```shell
cp .env.example .env
```

Run grpc server:
```shell
PYTHONPATH=$PYTHONPATH:ms_grpc/plibs:module python server.py
```

## Setup Docker Environment
Create environment variables config file:
```shell
cp .env.example .env
```

Build docker image:
```shell
DOCKER_BUILDKIT=1 docker build -t m-grpc-market .
```

Run docker image:
```shell
docker run -p 50054:50054 --name m-grpc-market --rm m-grpc-market
```

**NOTE**: *If you've run docker-dev from the Emb3rs-project repository before, I advise use the embers network 
in docker run to access PGSQL and change the database settings inside .env to Platform DB.*  

Run docker image with embers network:
```shell
docker run -p 50054:50054 --network dev_embers|platform_embers --name m-grpc-market --rm m-grpc-market
```