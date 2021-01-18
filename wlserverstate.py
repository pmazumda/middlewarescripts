connect('weblogic','weblogic1','t3://localhost:7001')
serverRuntime()
actTime = get('ActivationTime')

thisState = get('State')
cd('JVMRuntime/AdminServer')
cpuTime = get('JvmProcessorLoad')*100
disconnect()

import time
x = time.gmtime(actTime/1000)

print 
print 
print 
print "Start Time : " + str(x[0]) + "/" + str(x[1]) + "/" + str(x[2]) + " - " + str(x[3]) + ":" + str(x[4])
print "Activation Time: " + str(actTime)
print "State: " + thisState
print "CPU: " + str(cpuTime) + "%"
