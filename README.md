Welcome to the Rolis artifact for our Eurosys'22 submission. 

_Rolis: a software approach to efficiently replicating multi-core transactions_

## Project organization
 - `benchmarks`
   - `benchmarks/sto`: Transaction control, serialization (in `Transactions.cc`) and replay interface implementation (in `ReplayDB.cc`)
   - `benchmarks/tpcc.cc`: TPC-C benchmark implementation
   - `benchmarks/micro_bench.cc`: YCSB++ benchmark implementation
 - `docker`: the docker container
 - `scripts`: several experimental scripts and scripts to plot figures in the paper
 - `third-party`: the dependencies on MultiPaxos ported from Janus with the leader election
 - `dbtest.cc`: the `main()` portal to start the program, including replay logic

 You can find a more detailed document in [modules](./documents/code.md).

## Run the experiment locally
In this section, you can set up Rolis locally for testing and verification, which is mainly for badges `Artifacts Available` and `Artifacts Evaluated - Functional`.

### Obtain a Docker container
We run all our codes on `ubuntu 18.04` which mainly depends on several Linux libraries (i.e., boost, gcc and libyaml-cpp-dev). We provide a docker image with all required dependencies and source code for ease **so you can run on any local machine supporting Docker**. You can directly build a runnable Rolis instance with all required dependencies and source code via
```bash
cd ~
git clone https://github.com/shenweihai1/rolis-eurosys2022.git
cd ./docker
bash docker.sh
```

### Minimal working examples locally
You can start Rolis instance locally (*using different processes to mimic actual distributed environment*) to verify the functionability of the program through three minimal experiments: 
 * two running replicas without failure; 
 * Silo only;
 * three replicas with failure;

```bash
# 1. enter the docker container
docker exec -it ubuntu_eurosys2022 /bin/bash

# 2. run 3 minimal experiments (inside the container): 
make paxos
cd ./test && bash ./runner.sh
```

We should observe status "PASS" in green at the end of experiments as below
![alter](./documents/minimal_exp.PNG)

## Run the expriment in actual distributed environment
In this section, you can reproduce all results in the paper in the real environment, which is mainly for badges `Results Reproduced`. **The following `Experiment-2` are the major claim we made in the paper**. We also provide the detailed instructions to reproduce other results reported in the paper for other researchers.

### Hardware preparation
To reproduce the results in Rolis, we need
- 3 server machines, each machine has 32 CPU cores running on `Ubuntu 18.04` within a single socket. (***Please ensure that 3 machines can connect to each other via `ssh` and share the same username, because our tool depends on `scp` and `ssh` to simplify the procedure**, which means you can connect to any other two machines on any machine through `ssh ip` directly without username required*)
- obtain the IP of 3 machines.

### Download code and install dependencies
Let's assume here, `10.1.0.7` is the leader replica, `10.1.0.8` serves as the p1 follower replica and `10.1.0.9` serves as the p2 follower replica.
```bash
# on the leader replica 
cd ~
git clone https://github.com/shenweihai1/rolis-eurosys2022.git
cd rolis-eurosys2022
# install dependencies
bash ./install.sh

# config IPs for configuration 1.yml ~ 32.yml
cd ./third-party/paxos/config/1silo_1paxos_2follower

# ./run.sh {leader ip} {p1 follower ip} {p2 follower ip}
./run.sh "10.1.0.7" "10.1.0.8" "10.1.0.9"

# compile Paxos
cd ~/rolis-eurosys2022
make paxos
```

### Sync modifications to two other replicas via ssh
```bash
bash ./batch_silo.sh scp
```
At this moment, the running environment on 3 replicas is ready. 

### Experiment-1: Silo-only on TPC-C (Figure-10-a)
```bash
# on the leader replica
sudo ./multi-silo-only.sh 1 31
```
In this experiment, we run Silo solely up to 31 worker threads, it will finish the entire experiments in 25 minutes (*50 * 31/60*). Then you can obtain all performance numbers from 1 ~ 31 threads, by

```bash
python3 scripts/extractor.py 0 silo-only-logs "agg_throughput:" "ops/sec"
```

### Experiment-2: Throughput of Rolis on TPC-C benchmark (Figure-10-a)
* compile the program on the leader replica
```bash
# on the leader replica
# re-compile
bash ./multi.sh

# kill the running processes on all replicas
bash ./batch_silo.sh kill

# sync modifications
bash ./batch_silo.sh scp
```
* run the experiments on three replicas separately one by one

on the leader replica: 10.1.0.7 
```bash
# this process will stop after completion
ulimit -n 10000 && python3 scripts/leader_b.py 1 31 1
```
on the p2 follower replica: 10.1.0.9
```bash
# , this process will stop after completion
ulimit -n 10000 && python3 scripts/follower_b2.py 1 31 1
```
on the p1 follower replica: 10.1.0.8
```
# this process will stop after completion
ulimit -n 10000 && python3 scripts/follower_b1.py 1 31 1
```
The order of execution matters, executing the command on the p2 follower replica at first as above. In this experiment, we conduct an experiment to get the performance of Rolis on TPC-C benchmark by varying the number of CPU cores. Each run would take 1 minute, thus it will run up to 31 minutes (31 * 1 minute). We redirect all results into the folder `xxxx15`, thus you can obtain the performance numbers from 1 ~ 31 CPU cores, by
```bash
python3 scripts/extractor.py 0 xxxx15 "agg_throughput:" "ops/sec"
```
The major results would like below, Rolis can achieve about 1.259M throughput on 32 cores.
![alter](./documents/major_claim.PNG)

### Experiment-3: Silo-only on YCSB++ (Figure-10-b)
```bash
# on the leader replica
sudo ./multi-silo-only-m.sh 1 31
```
Similar to Experiment-1, get numbers by,

```bash
python3 scripts/extractor.py 0 silo-only-logs-m "agg_throughput:" "ops/sec"
```

### Experiment-4: Throughput of Rolis on YCSB++ benchmark (Figure-10-b)
Same to Experiment-2, except replacing the script names as follow,
```
leader_b.py  => leader_b_m.py
follower_b2.py  => follower_b2_m.py
follower_b1.py  => follower_b1_m.py
```
Then get the numbers by,
```bash
python3 scripts/extractor.py 0 xxxx15_micro "agg_throughput:" "ops/sec"
```

### Experiment-5 (Figure-11):
All numbers in `Figure-11` is  reciprocal of ones from `Figure-10`.

### Experiment-6: Failover (Figure-14)
In this experiment, we terminate the leader replica at the second 10, thus we manually modify variable `fail` from false to true to mimic the termination in `./benchmarks/bench.cc`. Then, we recompile it
```bash
# on the leader replica
bash ./multi.sh
```
Now, let's run the failover experiment
```bash
# on the leader replica
sudo ./b0.sh 16
tail -f ./xxxx15/*

# on the p1 follower replica
sudo ./b1.sh 16
tail -f ./xxxx15/*

# on the p2 follower replica
sudo ./b2.sh 16
tail -f ./xxxx15/*
```
Then, we can obtain numbers via
```bash
# on the leader replica
# copy logs from remote machines
./batch_silo.sh copy_remote_file ./xxxx15/follower-16.log  && mv p1p2.log ./scripts/failure_follower && cp ./xxxx15/leader-16-1000.log ./scripts/failure_leader

cd ./scripts && python failure_cal.py
```

### Experiment-7: latency ovar different batch-sizes (Figure-16)
In this experiment, we'll fix the number of worker threads while varying the batch-size of transactions. At first, compile the system
```bash
# on the leader replica
bash ./multi-latency.sh
bash ./batch_silo.sh scp
bash ./batch_silo.sh kill
```
Now, let's get the latency for all possible cases, batch-size: 50, 100, 200, 400, 800, 1600, 3200. It will take about up to 7 * 65 = 455 seconds.
```bash
bash ./batch_size_exp.sh
```
After that, you can get all the latency numbers via 
```
ag '% latency' xxxx15
```

### Experiment-8: Throughput over different batch-sizes (Figure-16)
Let's we stop tracking latency and record the throughput of Rolis over different batch-sizes. It's similar to Experiment-7. At first, compile the system
```bash
# on the leader replica
bash ./multi.sh
bash ./batch_silo.sh scp
bash ./batch_silo.sh kill
```
Then, let's get the throughput of Rolis with different batch-sizes.
```bash
bash ./batch_size_exp.sh
```
After that, you can get all latency numbers via
```
ag 'agg_throughput: ' xxxx15
```

## References
* Eurosys badges: https://sysartifacts.github.io/eurosys2022/badges