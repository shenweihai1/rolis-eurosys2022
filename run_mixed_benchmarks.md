## The benchmark 
Transaction: read 2 random keys and then update them

## How to run it
1. Since this mixed benchmark is simpler than the `micro` benchmark, it's recommended to use the batch\_size 20000, instead 10000 in the `mb0.sh`.
2. Enable the mix benchmark: uncomment `#define USING_MIX 1` in the file `benchmarks/micro_bench.cc`
3. Update the configuration on the 1 leader and 2 follower servers
```bash
# ./run.sh {leader_ip} {follower_1} {follower_2}
./run.sh "127.0.0.1" "127.0.0.1" "127.0.0.1"
```
4. Run the Rolis with `{n}` threads
```
# on the leader
sudo pkill -f dbtest
bash mb0.sh {n} 

# on the follower_1
sudo pkill -f dbtest
bash mb1.sh {n} 

# on the follower_2
sudo pkill -f dbtest
bash mb2.sh {n} 
```

## The throughput on Azure
```
threads	Silo-only	Rolis
1	1.366	1.05
4	4.13	3.15
16	12.45	9.28
20	15.36	11.01
28	20.07	13.78
```
