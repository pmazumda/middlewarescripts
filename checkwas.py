#----------------------------------------------------------------------
# File Name: check_was.py
#   Purpose: Display user requested information about
#            WebSphere Application Server (WSAS) resources.
#    Author: HonorGod [HG] - http://www.experts-exchange.com/M_3572595.html
#   History:
#   date    ver  who  what
# --------  ---  ---  ----------
# 10/07/15  0.0  HG   New - http://www.experts-exchange.com/Q_26328297.html
#----------------------------------------------------------------------
'''Command: %(cmdName)s\n
Purpose: wsadmin script used to display user specified information about
         WebSphere Application Server resources.\n
  Usage: %(cmdName)s [options]\n
Required switches/options:
  -i | --info       <value> = Type of information being requested
  -s | --serverName <value> = Target serverName\n
Optional switches/options:
  -n | --nodeName   <value> = Target nodeName\n
Information types/values:
  connectionpool - Display Connection Pool details
  heapsize       - Display Heap Size details
  threadpool     - Display Thread Pool details
  sessions       - Display Session Details\n
\nNotes:
- Long form option values may be separated/delimited from their associated
  identifier using either a space, or an equal sign ('=').\n
- Short form option values may be sepearated from their associated letter
  using an optional space.\n
- Text containing blanks must be enclosed in double quotes.\n
Examples:
  wsadmin -f %(cmdName)s.py -s heapeize -p server1 -n node01\n'''

import os, re, sys, getopt;

__scriptName__ = 'check_was';
__version__    = '0.0';
__updated__    = '15 July 2010';

#---------------------------------------------------------------------
# Name: localMode()
# Role: Return true (1) if AdminControl object is unavailable, false
#       (0) otherwise.
# Note: In localmode (i.e., -conntype none), this returns true (1)
#---------------------------------------------------------------------
def localMode() :
  'localMode() - Return true (1) if AdminControl object is unavailable, false (0) otherwise'
  try :
    host   = AdminControl.getCell();
    result = 0;                        # No, we're connected
  except :
    result = 1;                        # Yes, --contype none
  return result;

#---------------------------------------------------------------------
# Name: beanNameAsDict()
# Role: Parse the specified MBean and return a dictionary of the name
#       value pairs
#---------------------------------------------------------------------
def beanNameAsDict( bean ) :
  'beanNameAsDict() - Parse the specified MBean and return a dictionary of the name value pairs'
  result = {};
  for pair in bean.split( ':', 1 )[ 1 ].split( ',' ) :
    n, v = pair.split( '=', 1 );
    result[ n ] = v;
  return result;

#---------------------------------------------------------------------
# Name: callerName
# Role: Utility routine used to determine, and return the name of the
#       calling function.
# Note: Dependends on sys._getframe()
#  See: http://code.activestate.com/recipes/66062/
#---------------------------------------------------------------------
def callerName() :
  "callerName() - Returns the name of the calling routine (or '?')"
  return sys._getframe( 1 ).f_code.co_name;


#---------------------------------------------------------------------
# Name: configurable()
# Role: Return true (1) if AdminConfig object is available, false (0) otherwise
#---------------------------------------------------------------------
def configurable() :
  'configurable() - Return true (1) if AdminConfig object is available, false (0) otherwise'
  try :
    host   = AdminConfig.list( 'Server' );
    result = 1;                        # True  = AdminConfig object is available
  except :
    result = 0;                        # False = AdminConfig object not available
  return result;


#---------------------------------------------------------------------
# Name: configIdAsDict
# Role: Parse a config ID and return a dictionary of name/value pairs
# Note: Exception handler requires sys module
#       The keys in the returned dictionary come from the configID, so
#       are unlikely to match your defect expectations about exactly
#       what values are used (e.g., 'nodes' instead of "Node")
#---------------------------------------------------------------------
def configIdAsDict( configId ) :
  'configIdAsDict( configId ) - Given a configID, return a dictionary of the name/value components.'
  funName = callerName();              # Name of this function
  result  = {};                        # Result is a dictionary
  hier    = [];                        # Initialize to simplifiy checks
  try :                                # Be prepared for an error
    #-----------------------------------------------------------------
    # Does the specified configID match our RegExp pattern?
    # Note: mo == Match Object, if mo != None, a match was found
    #-----------------------------------------------------------------
    if ( configId[ 0 ] == '"' ) and ( configId[ -1 ] == '"' ) and ( configId.count( '"' ) == 2 ) :
      configId = configId[ 1:-1 ];
    mo = re.compile( r'^([\w ]+)\(([^|]+)\|[^)]+\)$' ).match( configId );
    if mo :
      Name = mo.group( 1 );
      hier = mo.group( 2 ).split( '/' );
    if mo and ( len( hier ) % 2 == 0 ) :
      #---------------------------------------------------------------
      # hier == Extracted config hierarchy string
      #---------------------------------------------------------------
      for i in range( 0, len( hier ), 2 ) :
        ( name, value ) = hier[ i ], hier[ i + 1 ];
        result[ name ]  = value;
      if result.has_key( 'Name' ) :
        print '''%s: Unexpected situation - "Name" attribute conflict,
  Name = "%s", Name prefix ignored: "%s"''' % ( funName, result[ 'Name' ], Name );
      else :
        result[ 'Name' ] = Name;
    else :
      print '''%(funName)s:
  Warning: The specified configId doesn\'t match the expected pattern,
           and is ignored.
  configId: "%(configId)s"''' % locals();
  except :
    ( kind, value ) = sys.exc_info()[ :2 ];
    print '''%(funName)s: Unexpected exception.\n
  Exception  type: %(kind)s
  Exception value: %(value)s''' % locals();
  return result;


#---------------------------------------------------------------------
# Name: heapsize()
# Role: Display information about the heap for the specified server
#---------------------------------------------------------------------
def heapsize( configID ) :
  cDict = configIdAsDict( configID );
  jvm   = AdminControl.queryNames( 'type=JVM,process=%(servers)s,node=%(nodes)s,*' % cDict );
  if jvm :
#   print '%-20s %-10s    %-8s %-8s' % ( 'nodeName', 'serverName', 'Used', 'Free' )
#   print '-' * 50
    jvmDict = beanNameAsDict( jvm );
    used    = AdminControl.getAttribute( jvm, 'heapSize' );
    free    = AdminControl.getAttribute( jvm, 'freeMemory' );
    total   = int( used ) + int( free );
    percent = float( used ) * 100.0 / float( total );
#   print '%-20s %-10s %8.2f %8.2f' % ( jvmDict[ 'node' ], jvmDict[ 'J2EEServer' ], MB( heapSize ), MB( freeMemory ) )
    print 'heapsize: node=%s  server=%s  used=%.1f MB  free=%.1f MB (%.2f%%)' % ( jvmDict[ 'node' ], jvmDict[ 'J2EEServer' ], MB( used ), MB( free ), percent );
  else :
    print 'Specified server does not appear to be active: %s' % cDict[ 'servers' ];


#---------------------------------------------------------------------
# Name: localMode()
# Role: Return true (1) if AdminControl object is unavailable, false
#       (0) otherwise.
# Note: In localmode (i.e., -conntype none), this returns true (1)
#---------------------------------------------------------------------
def localMode() :
  'localMode() - Return true (1) if AdminControl object is unavailable, false (0) otherwise'
  try :
    host   = AdminControl.getCell();
    result = 0;                        # No, we're connected
  except :
    result = 1;                        # Yes, --contype none
  return result;


#---------------------------------------------------------------------
# Name: main()
# Role: Perform the actual work of the script
#---------------------------------------------------------------------
def main( cmdName = None ) :
  missingParms = '%(cmdName)s: Insufficient parameters provided.\n';
  ambigServer  = '%(cmdName)s: Ambiguous server specified: %(serverName)s\n';
  badReqdParam = '%(cmdName)s: Invalid required parameter: %(key)s\n';
  badServer    = '%(cmdName)s: Unknown server: %(serverName)s\n';
  badNode      = '%(cmdName)s: Unknown node: %(nodeName)s\n';
  serverReqd   = '%(cmdName)s: Missing required parameter: "serverName".\n';

  if not cmdName :
    cmdName = __scriptName__;
  
  #-------------------------------------------------------------------
  # How many user command line parameters were specified?
  #-------------------------------------------------------------------
  argc = len( sys.argv );                   # Number of arguments
  if ( argc < 2 ) :                         # If too few are present,
    print missingParms % locals();          #   tell the user, and
    Usage( cmdName );                       #   provide the Usage info
  else :                                    # otherwise
    Opts = parseOpts( cmdName );            #   parse the command line

  #-------------------------------------------------------------------
  # Assign values from the user Options dictionary, to make value
  # access simplier, and easier.  For example, instead of using:
  #   Opts[ 'nodeName' ]
  # we will be able to simply use:
  #   nodeName
  # to access the value.
  #-------------------------------------------------------------------
  for key in Opts.keys() :
    val = Opts[ key ];
    cmd = '%s=Opts["%s"]' % ( key, key );
#   print cmd;
    exec( cmd );

  #-------------------------------------------------------------------
  # Check required parameters
  #-------------------------------------------------------------------
  if info not in [ 'heapsize', 'sessions', 'connectionpool', 'threadpool' ] :
    print badInfo % locals();
    Usage( cmdName );
    
  if not serverName :
    print serverReqd % locals();
    Usage( cmdName );
  
  #-------------------------------------------------------------------
  # Was the nodeName specified, and if so, does it exist?
  #-------------------------------------------------------------------
  node = None;
  if nodeName :
    for nid in AdminConfig.list( 'Node' ).splitlines() :
       if nid.startswith( nodeName + '(' ) :
         node = nid;
    if not node :
      print badNode % locals();
  
  #-------------------------------------------------------------------
  # Does the specified serverName exist (within the scope of the
  # specified node)?
  # Note: A scope of None is identical to not specifying a scope
  #-------------------------------------------------------------------
  servers = [];
  for sid in AdminConfig.list( 'Server', node ).splitlines() :
    if sid.startswith( serverName + '(' ) :
      servers.append( sid );
  if len( servers ) < 1 :
    print badServer % locals();
    sys.exit();
  elif len( servers ) > 1 :
    print ambigServer % locals();
    nodes = [];
    for sid in servers :
      nodes.append( configIdAsDict( sid )[ 'nodes' ] );
    print 'Specify one of the following nodes using the --nodeName option: ' + ( ', '.join( nodes ) );
    sys.exit();
  server = servers[ 0 ];

  print 'Request for %s on %s' % ( info, server );
  if info == 'heapsize' :
    heapsize( server );
  else :
    print 'Not yet implemented: "%s"' % info


#---------------------------------------------------------------------
# Name: MB()
# Role: Convert the specified (integer) value [bytes] into MegaBytes
#---------------------------------------------------------------------
def MB( val ) :
  'MB() - Convert specified integer (byte) value into MegaBytes'
  return int( val ) / ( 1024.0 * 1024.0 );


#---------------------------------------------------------------------
# Name: parseOpts()
# Role: Process the user specified (command line) options
#---------------------------------------------------------------------
def parseOpts( cmdName ) :
  shortForm = 'i:n:s:';
  longForm  = 'info=,nodeName=,serverName='.split( ',' );
  badOpt    = '%(cmdName)s: Unknown/unrecognized parameter%(plural)s: %(argStr)s\n';
  optErr    = '%(cmdName)s: Error encountered processing: %(argStr)s\n';
  problem   = '%(cmdName)s: Error option processing problem: %(opt)s\n';

  try :
    opts, args = getopt.getopt( sys.argv, shortForm, longForm );
  except getopt.GetoptError :
    argStr = ' '.join( sys.argv );
    print optErr % locals();
    Usage( cmdName );

  #-------------------------------------------------------------------
  # Initialize the Opts dictionary using the longForm key identifiers
  #-------------------------------------------------------------------
  Opts = {};
  for name in longForm :
    if name[ -1 ] == '=' :
      name = name[ :-1 ]
    Opts[ name ] = None;

  #-------------------------------------------------------------------
  # Process the list of options returned by getopt()
  #-------------------------------------------------------------------
  for opt, val in opts :
    if opt in   ( '-i', '--info' )       : Opts[ 'info'       ] = val
    elif opt in ( '-n', '--nodeName' )   : Opts[ 'nodeName'   ] = val
    elif opt in ( '-s', '--serverName' ) : Opts[ 'serverName' ] = val
    else :
      print problem % locals();

  #-------------------------------------------------------------------
  # Check for unhandled/unrecognized options
  #-------------------------------------------------------------------
  if ( args != [] ) :        # If any unhandled parms exist => error
    argStr = ' '.join( args );
    plural = '';
    if ( len( args ) > 1 ) : plural = 's';
    print badOpt % locals();
    Usage( cmdName );

  #-------------------------------------------------------------------
  # Return a dictionary of the user specified command line options
  #-------------------------------------------------------------------
  return Opts;


#---------------------------------------------------------------------
# Name: Usage()
# Role: Display usage information necessary to use this script.
#---------------------------------------------------------------------
def Usage( cmdName = None ) :
  if not cmdName :
    cmdName = __scriptName__;

  print __doc__ % locals();       # Script docstring contains usage info
  sys.exit();

  
#----------------------------------------------------------------------
# Code execution begins
#----------------------------------------------------------------------
if ( __name__ == '__main__' ) or ( __name__ == 'main' ) :
  if localMode() :
    print 'A connection to WebSphere Application Server is required.\n';
    Usage();
  elif configurable() :
    main();
  else :
    print 'WebSphere Application Server scripting objects appear to be unavailable.\n';
    Usage();
else :
  print 'This script should be executed, not imported.\n';
  Usage( __name__ );
