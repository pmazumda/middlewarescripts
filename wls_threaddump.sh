#!/bin/sh
###################################################################
#@@Script Name: wls_threadmonitor.sh
#@@Created and modified by Pinak Mazumdar 
#
################################################################### 
# Setting the Java Home, by giving the path where your JDK is kept
echo "Usage : sh ./wls_threadmonitor.sh <JBOSS_PID>"
export JAVA_HOME=/WAS/jdk1.7.0_45/

####Path to save thread dumps####


LOG_PATH=`pwd` 
#Process id
PID=$1

##Number of times##
N=5
## Loop##
INTERVAL=40

for ((i=1;i<=$N;i++))
do
   d=$(date +%Y%m%d-%H%M%S)
   dump="THREAD-$PID-$d.txt"
   echo $i of $N: $dump
   $JAVA_HOME/bin/jstack -l $PID > $dump
	if [ $i -lt $INTERVAL ]; then
    echo "sleeping..."
   sleep $INTERVAL
fi
done

