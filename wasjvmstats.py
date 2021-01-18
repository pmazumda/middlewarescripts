#!/bin/sh
echo "This script  is used to get the current heap size, used heap size."
echo "Enter the profile path"
read -a PP
PROFILE_PATH=$PP
#echo "Enter USER"
#read -a user
#USER=$user
#echo "Enter Password"
#read -a passwd
#PASSWORD=$passwd
cat << EOF > jvmstats.py
#!/usr/bin/python
serverJVM=AdminControl.completeObjectName('type=JVM,process=' + sys.argv[0] + ',*')
serverJVMObj=AdminControl.makeObjectName(serverJVM)
perf=AdminControl.completeObjectName('type=Perf,process=' + sys.argv[0] + ',*')
perfObj=AdminControl.makeObjectName(perf)
jvmObj=AdminControl.invoke_jmx(perfObj,'getStatsObject',[serverJVMObj,java.lang.Boolean('false')],['javax.management.ObjectName','java.lang.Boolean'])

currentHeapsize=jvmObj.getStatistic('HeapSize').getCurrent()
usedMemory=jvmObj.getStatistic('UsedMemory').getCount()
usage=float(usedMemory)/float(currentHeapsize)*100
print sys.argv[0] + ".> "+str(currentHeapsize)+"K .> "+str(usedMemory)+"K .> "+"Usage:%.2f" % usage+"%"
EOF

chmod 755 jvmstats.py
#$PP/bin/wsadmin.sh -user $user -password $passwd -lang jython -f jvmstats.py
$PP/bin/wsadmin.sh -lang jython -f jvmstats.py
