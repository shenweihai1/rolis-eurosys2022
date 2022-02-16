#!/bin/bash
repos="rolis-eurosys2022"  # repos name, default
workdir="~"  # we default put our repos under the root
leadrIP=$( cat ./scripts/ip_leader_replica )
p1=$( cat ./scripts/ip_p1_follower_replica )
p2=$( cat ./scripts/ip_p2_follower_replica )
ulimit -n 10000
# minimum of the number of worker threads
start=1
# maximum of the number of worker threads
end=31

setup () {
    bash ./batch_silo.sh kill
    mkdir -p results
    #rm ./results/*
}

experiment1 () {
   echo 'start experiment-1'
   sudo ./multi-silo-only.sh $start $end
   python3 scripts/extractor.py 0 silo-only-logs "agg_throughput:" "ops/sec" > results/silo-only-tpcc.log
}

experiment2 () {
    echo 'start experiment-2'
    sudo bash ./multi.sh
    bash ./batch_silo.sh kill
    bash ./batch_silo.sh scp

    eval "ulimit -n 10000; cd $workdir/$repos/ && python3 scripts/leader_b.py $start $end 1" &
    sleep 1

    ssh $p2 "ulimit -n 10000; cd $workdir/$repos/ && python3 scripts/follower_b2.py $start $end 1" &
    sleep 1

    ssh $p1 "ulimit -n 10000; cd $workdir/$repos/ && python3 scripts/follower_b1.py $start $end 1" &
    sleep 1

    echo "Wait for jobs..."
    FAIL=0

    for job in `jobs -p`
    do
        wait $job || let "FAIL+=1"
    done

    if [ "$FAIL" == "0" ];
    then
        echo "YAY!"
    else
        echo "FAIL! ($FAIL)"
    fi

    python3 scripts/extractor.py 0 xxxx15 "agg_throughput:" "ops/sec" > results/scalability-tpcc.log
}

experiment3 () {
  echo 'start experiment-3'
  sudo ./multi-silo-only-m.sh $start $end
  python3 scripts/extractor.py 0 silo-only-logs-m "agg_throughput:" "ops/sec" > results/silo-only-ycsb.log
}


experiment4 () {
    echo 'start experiment-4'
    sudo bash ./multi.sh
    bash ./batch_silo.sh kill
    bash ./batch_silo.sh scp

    eval "ulimit -n 10000; cd $workdir/$repos/ && python3 scripts/leader_b_m.py $start $end 1" &
    sleep 1

    ssh $p2 "ulimit -n 10000; cd $workdir/$repos/ && python3 scripts/follower_b2_m.py $start $end 1" &
    sleep 1

    ssh $p1 "ulimit -n 10000; cd $workdir/$repos/ && python3 scripts/follower_b1_m.py $start $end 1" &
    sleep 1

    echo "Wait for jobs..."
    FAIL=0

    for job in `jobs -p`
    do
        wait $job || let "FAIL+=1"
    done

    if [ "$FAIL" == "0" ];
    then
        echo "YAY!"
    else
        echo "FAIL! ($FAIL)"
    fi

    python3 scripts/extractor.py 0 xxxx15_micro  "agg_throughput:" "ops/sec" > results/scalability-ycsb.log
}

experiment5() {
  echo "skip experiment 5"
}

experiment6() {
  echo 'start experiment-6'
  sudo  bash ./multi-failover.sh
  bash ./batch_silo.sh kill
  bash ./batch_silo.sh scp

  sudo  bash ./multi-failover-variable.sh
  
  eval "ulimit -n 10000; cd $workdir/$repos/ && sudo ./b0.sh 16" &
  sleep 1

  ssh $p2 "ulimit -n 10000; cd $workdir/$repos/ && sudo ./b2.sh 16" &
  sleep 1

  ssh $p1 "ulimit -n 10000; cd $workdir/$repos/ && sudo ./b1.sh 16 " &
  sleep 1

  echo "Wait for jobs..."
  FAIL=0

  for job in `jobs -p`
  do
      wait $job || let "FAIL+=1"
  done

  if [ "$FAIL" == "0" ];
  then
      echo "YAY!"
  else
      echo "FAIL! ($FAIL)"
  fi


  # 30 + 16 + 10 + 30
  sleep 86
  
  ./batch_silo.sh copy_remote_file ./xxxx15/follower-16.log  && mv p1p2.log ./scripts/failure_follower && cp ./xxxx15/leader-16-1000.log ./scripts/failure_leader

  python ./scripts/failure_cal.py > ./results/failover-16-throughput.log
}

experiment7 () {
  echo "start experiment7"
  sudo  bash ./multi-latency.sh
  bash ./batch_silo.sh scp
  bash ./batch_silo.sh kill
  bash ./batch_size_exp.sh
  ag '% latency' xxxx15 > results/batch-latency.log
}

experiment8 () {
  echo "start experiment8"
  sudo  bash ./multi.sh
  bash ./batch_silo.sh scp
  bash ./batch_silo.sh kill
  bash ./batch_size_exp.sh
  ag 'agg_throughput: ' xxxx15 > results/batch-throughput.log
}


setup
experiment1
experiment2
experiment3
experiment4
experiment5
experiment6
experiment7
experiment8
