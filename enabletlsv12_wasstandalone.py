import time;
import os;
import shutil; 


localtime = time.asctime( time.localtime(time.time()) );

# checking FIPS-TLSv12 security status
tlsFlag= AdminTask.getFipsInfo();



tlsFlag1 = tlsFlag.split(" ");


if tlsFlag1[1] == "true]":
   print "--------------------------------------------------------------------------------";
   print "                        TLSV1.2 ALREADY ENABLED\n";
   print "           Local current time :", localtime;
   print "--------------------------------------------------------------------------------";
else:
   print "--------------------------------------------------------------------------------";
   print "                        TLSV1.2 SCRIPT STARTED\n";
   
   # getting current dir and profile dir
   binDir= os.getcwd();
   profileDir = binDir[:-4];
      
   # the below command to get the server name and path 
   test = AdminTask.listServers('[-serverType APPLICATION_SERVER ]');
   test1 = test.split("(");
   test2 = test1[1].split(")");
   SRVRpath = test2[0];
   SRVRNAME = test1[0];
   
   # the below commadn take the number
   GETID = AdminConfig.getid('/Server:'+SRVRNAME+'/');
   GETID1 = GETID.split("_");
   GETID2 = GETID1[1].split(")");
   GETNMBR = GETID2[0];

   # below commad to add the Required three tlsv12 property in jvm custom property
   AdminConfig.create('Property', '('+SRVRpath+'#JavaVirtualMachine_'+GETNMBR+')', '[[validationExpression ""] [name "com.ibm.team.repository.transport.client.protocol"] [description ""] [value "TLSv1.2"] [required "false"]]') 
   AdminConfig.create('Property', '('+SRVRpath+'#JavaVirtualMachine_'+GETNMBR+')', '[[validationExpression ""] [name "com.ibm.jsse2.sp800-131"] [description ""] [value "strict"] [required "false"]]') 
   AdminConfig.create('Property', '('+SRVRpath+'#JavaVirtualMachine_'+GETNMBR+')', '[[validationExpression ""] [name "com.ibm.rational.rpe.tls12only"] [description ""] [value "true"] [required "false"]]') 

   # below command convert existing certificate to tlsv12 strict compliance 2048 keysize certificate   
   AdminTask.convertCertForSecurityStandard('[-fipsLevel SP800-131 -signatureAlgorithm SHA256withRSA -keySize 2048 ]') 
   
   # below command enbles tlsv12 fip security in strict mode
   AdminTask.enableFips('[-enableFips true -fipsLevel SP800-131 ]')
   
    
   
   # save the configuratopm changes
   #AdminConfig.save()
   
   # the below command to get the cell and node name
   cellName = AdminControl.getCell();
   nodeName = AdminControl.getNode();
   
   #Adding JVM argument -DSSO_SSL_CIPHER_LIST=TLSv1.2
   jvmvalue = AdminTask.showJVMProperties('[-nodeName '+nodeName+' -serverName '+SRVRNAME+' -propertyName genericJvmArguments]')
   AdminTask.setJVMProperties('[-nodeName '+nodeName+' -serverName '+SRVRNAME+' -genericJvmArguments "'+jvmvalue+' -DSSO_SSL_CIPHER_LIST=TLSv1.2 -Dhttps.protocols=TLSv1.2"]')
   AdminConfig.save()
   
   # below command copy the updated WAS default trust.p12 to etc path
   frompath = profileDir+"/config/cells/"+cellName+"/nodes/"+nodeName+"/trust.p12"
   destPath = profileDir+"/etc/trust.p12";
   shutil.copyfile(frompath,destPath);
   
   # below command update ssl.client.props with required tlsv12 changes
   iFilename = '/properties/ssl.client.props';
   oFilename = '/properties/ssl.clientnew.props';
   iFile = profileDir+iFilename; 
   oFile = profileDir+oFilename; 
   inputFile=open(iFile, 'rb+')
   outptFile=open(oFile,'wb+')

   while 1:
         line=inputFile.readline()
         if line.strip() == 'com.ibm.security.useFIPS=false':
             newLine = 'com.ibm.security.useFIPS=true\ncom.ibm.websphere.security.FIPSLevel=SP800-131\n';
             outptFile.write(newLine);
         elif line.strip() == 'com.ibm.ssl.protocol=SSL_TLS':
             newLine1 = 'com.ibm.ssl.protocol=TLSv1.2\n';
             outptFile.write(newLine1);
         else:
             outptFile.write(line);
         if not line:
             break
             pass
   inputFile.close();
   outptFile.close();
   
   os.rename( profileDir+"/properties/ssl.client.props", profileDir+"/properties/ssl.client.props_SSLTLS");
   os.rename( profileDir+"/properties/ssl.clientnew.props", profileDir+"/properties/ssl.client.props");
   os.remove( profileDir+"/properties/ssl.client.props_SSLTLS");
 
   
   print "       Congrats!! Script Executed Successfully,Please do restart WAS ";
   print "Before accessing application make sure your browser JRE and JDK support TLSv1.2 ";
   print "           Local current time :", localtime;
   print "--------------------------------------------------------------------------------";

