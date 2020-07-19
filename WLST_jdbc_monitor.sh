#!/bin/sh


#########################################################################
## Script Name: WLST_jdbc_monitor.sh                                   ##
## Usage : ./WLST_jdbc_monitor.sh                                      ##
## Author: Pinak Mazumdar                                              ##
## Place:Bangalore                                                     ## 
## Description: WLST Script to monitor JDBC Statistics                 ##
#########################################################################



JAVA_HOME=/WAS/jdk1.7.0_45/
export JAVA_HOME

echo "JAVA_HOME PATH SET IS: $JAVA_HOME"
echo 

WLST_HOME=/WAS/wasadm/Oracle/Middleware/Oracle_Home/oracle_common/common/bin
export WLST_HOME

echo "WLST HOME PATH SET IS: $WLST_HOME"
echo 


cat << EOF > wlspy.py

#!/usr/bin/python

from java.io import FileInputStream
import java.lang
import os
import string

username = 'weblogic'
password = 'welcome1'
url='t3://abc.ad.cloud.com:7001'

connect(username,password,url)
allServers=domainRuntimeService.getServerRuntimes();
if (len(allServers) > 0):
  for mServer in allServers:
    jdbcServiceRT = mServer.getJDBCServiceRuntime();
    dataSources = jdbcServiceRT.getJDBCDataSourceRuntimeMBeans();
    if (len(dataSources) > 0):
        for dataSource in dataSources:
            print 'ActiveConnectionsAverageCount      '  ,  dataSource.getActiveConnectionsAverageCount()
            print 'ActiveConnectionsCurrentCount      '  ,  dataSource.getActiveConnectionsCurrentCount()
            print 'ActiveConnectionsHighCount         '  ,  dataSource.getActiveConnectionsHighCount()
            print 'ConnectionDelayTime                '  ,  dataSource.getConnectionDelayTime()
            print 'ConnectionsTotalCount              '  ,  dataSource.getConnectionsTotalCount()
            print 'CurrCapacity                       '  ,  dataSource.getCurrCapacity()
            print 'CurrCapacityHighCount              '  ,  dataSource.getCurrCapacityHighCount()
            print 'DeploymentState                    '  ,  dataSource.getDeploymentState()
            print 'FailedReserveRequestCount          '  ,  dataSource.getFailedReserveRequestCount()
            print 'FailuresToReconnectCount           '  ,  dataSource.getFailuresToReconnectCount()
            print 'HighestNumAvailable                '  ,  dataSource.getHighestNumAvailable()
            print 'HighestNumUnavailable              '  ,  dataSource.getHighestNumUnavailable()
            print 'LeakedConnectionCount              '  ,  dataSource.getLeakedConnectionCount()
            print 'ModuleId                           '  ,  dataSource.getModuleId()
            print 'Name                               '  ,  dataSource.getName()
            print 'NumAvailable                       '  ,  dataSource.getNumAvailable()
            print 'NumUnavailable                     '  ,  dataSource.getNumUnavailable()
            print 'PrepStmtCacheAccessCount           '  ,  dataSource.getPrepStmtCacheAccessCount()
            print 'PrepStmtCacheAddCount              '  ,  dataSource.getPrepStmtCacheAddCount()
            print 'PrepStmtCacheCurrentSize           '  ,  dataSource.getPrepStmtCacheCurrentSize()
            print 'PrepStmtCacheDeleteCount           '  ,  dataSource.getPrepStmtCacheDeleteCount()
            print 'PrepStmtCacheHitCount              '  ,  dataSource.getPrepStmtCacheHitCount()
            print 'PrepStmtCacheMissCount             '  ,  dataSource.getPrepStmtCacheMissCount()
            print 'ReserveRequestCount                '  ,  dataSource.getReserveRequestCount()
            print 'State                              '  ,  dataSource.getState()
            print 'WaitingForConnectionCurrentCount   '  ,  dataSource.getWaitingForConnectionCurrentCount()
            print 'WaitingForConnectionFailureTotal   '  ,  dataSource.getWaitingForConnectionFailureTotal()
            print 'WaitingForConnectionHighCount      '  ,  dataSource.getWaitingForConnectionHighCount()
            print 'WaitingForConnectionSuccessTotal   '  ,  dataSource.getWaitingForConnectionSuccessTotal()
            print 'WaitingForConnectionTotal          '  ,  dataSource.getWaitingForConnectionTotal()
            print 'WaitSecondsHighCount               '  ,  dataSource.getWaitSecondsHighCount()
EOF



echo "************Execution Starts*****************"
echo
chmod 755 wlspy.py
$WLST_HOME/wlst.sh wlspy.py > jdbcstats.log
rm wlspy.py
echo "JDBC Statistics are logged in jdbcstats.log"

echo
echo "************Execution Ended******************"

