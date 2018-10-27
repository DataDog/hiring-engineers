#
# PySNMP MIB module INTEGRATED-SERVICES-MIB (http://pysnmp.sf.net)
# ASN.1 source http://mibs.snmplabs.com:80/asn1/INTEGRATED-SERVICES-MIB
# Produced by pysmi-0.0.7 at Sun Feb 14 00:07:36 2016
# On host bldfarm platform Linux version 4.1.13-100.fc21.x86_64 by user goose
# Using Python version 3.5.0 (default, Jan  5 2016, 17:11:52) 
#
( OctetString, ObjectIdentifier, Integer, ) = mibBuilder.importSymbols("ASN1", "OctetString", "ObjectIdentifier", "Integer")
( NamedValues, ) = mibBuilder.importSymbols("ASN1-ENUMERATION", "NamedValues")
( ValueSizeConstraint, ConstraintsIntersection, ValueRangeConstraint, ConstraintsUnion, SingleValueConstraint, ) = mibBuilder.importSymbols("ASN1-REFINEMENT", "ValueSizeConstraint", "ConstraintsIntersection", "ValueRangeConstraint", "ConstraintsUnion", "SingleValueConstraint")
( InterfaceIndex, ifIndex, ) = mibBuilder.importSymbols("IF-MIB", "InterfaceIndex", "ifIndex")
( ObjectGroup, ModuleCompliance, NotificationGroup, ) = mibBuilder.importSymbols("SNMPv2-CONF", "ObjectGroup", "ModuleCompliance", "NotificationGroup")
( MibScalar, MibTable, MibTableRow, MibTableColumn, Bits, Counter64, ModuleIdentity, mib_2, Counter32, IpAddress, ObjectIdentity, Integer32, MibIdentifier, TimeTicks, Gauge32, Unsigned32, NotificationType, iso, ) = mibBuilder.importSymbols("SNMPv2-SMI", "MibScalar", "MibTable", "MibTableRow", "MibTableColumn", "Bits", "Counter64", "ModuleIdentity", "mib-2", "Counter32", "IpAddress", "ObjectIdentity", "Integer32", "MibIdentifier", "TimeTicks", "Gauge32", "Unsigned32", "NotificationType", "iso")
( RowStatus, TimeInterval, TextualConvention, DisplayString, TestAndIncr, TruthValue, ) = mibBuilder.importSymbols("SNMPv2-TC", "RowStatus", "TimeInterval", "TextualConvention", "DisplayString", "TestAndIncr", "TruthValue")
intSrv = ModuleIdentity((1, 3, 6, 1, 2, 1, 52))
if mibBuilder.loadTexts: intSrv.setLastUpdated('9511030500Z')
if mibBuilder.loadTexts: intSrv.setOrganization('IETF Integrated Services Working Group')
if mibBuilder.loadTexts: intSrv.setContactInfo('       Fred Baker\n            Postal: Cisco Systems\n                    519 Lado Drive\n                    Santa Barbara, California 93111\n            Tel:    +1 805 681 0115\n            E-Mail: fred@cisco.com\n            \n                    John Krawczyk\n            Postal: ArrowPoint Communications\n                    235 Littleton Road\n                    Westford, Massachusetts 01886\n            Tel:    +1 508 692 5875\n            E-Mail: jjk@tiac.net')
if mibBuilder.loadTexts: intSrv.setDescription('The MIB module to describe the Integrated Services\n            Protocol')
intSrvObjects = MibIdentifier((1, 3, 6, 1, 2, 1, 52, 1))
intSrvGenObjects = MibIdentifier((1, 3, 6, 1, 2, 1, 52, 2))
intSrvNotifications = MibIdentifier((1, 3, 6, 1, 2, 1, 52, 3))
intSrvConformance = MibIdentifier((1, 3, 6, 1, 2, 1, 52, 4))
class SessionNumber(Integer32, TextualConvention):
    subtypeSpec = Integer32.subtypeSpec+ValueRangeConstraint(0,2147483647)

class Protocol(Integer32, TextualConvention):
    displayHint = 'd'
    subtypeSpec = Integer32.subtypeSpec+ValueRangeConstraint(1,255)

class SessionType(Integer32, TextualConvention):
    subtypeSpec = Integer32.subtypeSpec+ValueRangeConstraint(1,255)

class Port(OctetString, TextualConvention):
    displayHint = 'd'
    subtypeSpec = OctetString.subtypeSpec+ValueSizeConstraint(2,4)

class MessageSize(Integer32, TextualConvention):
    displayHint = 'd'
    subtypeSpec = Integer32.subtypeSpec+ValueRangeConstraint(0,2147483647)

class BitRate(Integer32, TextualConvention):
    displayHint = 'd'
    subtypeSpec = Integer32.subtypeSpec+ValueRangeConstraint(0,2147483647)

class BurstSize(Integer32, TextualConvention):
    displayHint = 'd'
    subtypeSpec = Integer32.subtypeSpec+ValueRangeConstraint(0,2147483647)

class QosService(Integer32, TextualConvention):
    subtypeSpec = Integer32.subtypeSpec+ConstraintsUnion(SingleValueConstraint(1, 2, 5,))
    namedValues = NamedValues(("bestEffort", 1), ("guaranteedDelay", 2), ("controlledLoad", 5),)

intSrvIfAttribTable = MibTable((1, 3, 6, 1, 2, 1, 52, 1, 1), )
if mibBuilder.loadTexts: intSrvIfAttribTable.setDescription("The reservable attributes of the system's  in-\n            terfaces.")
intSrvIfAttribEntry = MibTableRow((1, 3, 6, 1, 2, 1, 52, 1, 1, 1), ).setIndexNames((0, "IF-MIB", "ifIndex"))
if mibBuilder.loadTexts: intSrvIfAttribEntry.setDescription('The reservable attributes of  a  given  inter-\n            face.')
intSrvIfAttribAllocatedBits = MibTableColumn((1, 3, 6, 1, 2, 1, 52, 1, 1, 1, 1), BitRate()).setUnits('Bits per second').setMaxAccess("readonly")
if mibBuilder.loadTexts: intSrvIfAttribAllocatedBits.setDescription('The number of bits/second currently  allocated\n            to reserved sessions on the interface.')
intSrvIfAttribMaxAllocatedBits = MibTableColumn((1, 3, 6, 1, 2, 1, 52, 1, 1, 1, 2), BitRate()).setUnits('Bits per second').setMaxAccess("readcreate")
if mibBuilder.loadTexts: intSrvIfAttribMaxAllocatedBits.setDescription('The maximum number of bits/second that may  be\n            allocated  to  reserved  sessions on the inter-\n            face.')
intSrvIfAttribAllocatedBuffer = MibTableColumn((1, 3, 6, 1, 2, 1, 52, 1, 1, 1, 3), BurstSize()).setUnits('Bytes').setMaxAccess("readonly")
if mibBuilder.loadTexts: intSrvIfAttribAllocatedBuffer.setDescription('The amount of buffer space  required  to  hold\n            the simultaneous burst of all reserved flows on\n            the interface.')
intSrvIfAttribFlows = MibTableColumn((1, 3, 6, 1, 2, 1, 52, 1, 1, 1, 4), Gauge32()).setMaxAccess("readonly")
if mibBuilder.loadTexts: intSrvIfAttribFlows.setDescription('The number of reserved flows currently  active\n            on  this  interface.  A flow can be created ei-\n            ther from a reservation protocol (such as  RSVP\n            or ST-II) or via configuration information.')
intSrvIfAttribPropagationDelay = MibTableColumn((1, 3, 6, 1, 2, 1, 52, 1, 1, 1, 5), Integer32()).setUnits('microseconds').setMaxAccess("readcreate")
if mibBuilder.loadTexts: intSrvIfAttribPropagationDelay.setDescription('The amount of propagation delay that this  in-\n            terface  introduces  in addition to that intro-\n            diced by bit propagation delays.')
intSrvIfAttribStatus = MibTableColumn((1, 3, 6, 1, 2, 1, 52, 1, 1, 1, 6), RowStatus()).setMaxAccess("readcreate")
if mibBuilder.loadTexts: intSrvIfAttribStatus.setDescription("'active' on interfaces that are configured for\n            RSVP.")
intSrvFlowTable = MibTable((1, 3, 6, 1, 2, 1, 52, 1, 2), )
if mibBuilder.loadTexts: intSrvFlowTable.setDescription("Information describing the reserved flows  us-\n            ing the system's interfaces.")
intSrvFlowEntry = MibTableRow((1, 3, 6, 1, 2, 1, 52, 1, 2, 1), ).setIndexNames((0, "INTEGRATED-SERVICES-MIB", "intSrvFlowNumber"))
if mibBuilder.loadTexts: intSrvFlowEntry.setDescription('Information describing the use of a given  in-\n            terface   by   a   given   flow.   The  counter\n            intSrvFlowPoliced starts counting  at  the  in-\n            stallation of the flow.')
intSrvFlowNumber = MibTableColumn((1, 3, 6, 1, 2, 1, 52, 1, 2, 1, 1), SessionNumber())
if mibBuilder.loadTexts: intSrvFlowNumber.setDescription('The number of this flow.  This is for SNMP In-\n            dexing purposes only and has no relation to any\n            protocol value.')
intSrvFlowType = MibTableColumn((1, 3, 6, 1, 2, 1, 52, 1, 2, 1, 2), SessionType()).setMaxAccess("readcreate")
if mibBuilder.loadTexts: intSrvFlowType.setDescription('The type of session (IP4, IP6, IP6  with  flow\n            information, etc).')
intSrvFlowOwner = MibTableColumn((1, 3, 6, 1, 2, 1, 52, 1, 2, 1, 3), Integer32().subtype(subtypeSpec=ConstraintsUnion(SingleValueConstraint(1, 2, 3,))).clone(namedValues=NamedValues(("other", 1), ("rsvp", 2), ("management", 3),))).setMaxAccess("readcreate")
if mibBuilder.loadTexts: intSrvFlowOwner.setDescription('The process that installed this  flow  in  the\n            queue policy database.')
intSrvFlowDestAddr = MibTableColumn((1, 3, 6, 1, 2, 1, 52, 1, 2, 1, 4), OctetString().subtype(subtypeSpec=ValueSizeConstraint(4,16))).setMaxAccess("readcreate")
if mibBuilder.loadTexts: intSrvFlowDestAddr.setDescription("The destination address used by all senders in\n            this  session.   This object may not be changed\n            when the value of the RowStatus object is  'ac-\n            tive'.")
intSrvFlowSenderAddr = MibTableColumn((1, 3, 6, 1, 2, 1, 52, 1, 2, 1, 5), OctetString().subtype(subtypeSpec=ValueSizeConstraint(4,16))).setMaxAccess("readcreate")
if mibBuilder.loadTexts: intSrvFlowSenderAddr.setDescription("The source address of the sender  selected  by\n            this  reservation.  The value of all zeroes in-\n            dicates 'all senders'.  This object may not  be\n            changed  when the value of the RowStatus object\n            is 'active'.")
intSrvFlowDestAddrLength = MibTableColumn((1, 3, 6, 1, 2, 1, 52, 1, 2, 1, 6), Integer32().subtype(subtypeSpec=ValueRangeConstraint(0,128))).setMaxAccess("readcreate")
if mibBuilder.loadTexts: intSrvFlowDestAddrLength.setDescription("The length of the destination address in bits.\n            This  is  the CIDR Prefix Length, which for IP4\n            hosts and multicast addresses is 32 bits.  This\n            object may not be changed when the value of the\n            RowStatus object is 'active'.")
intSrvFlowSenderAddrLength = MibTableColumn((1, 3, 6, 1, 2, 1, 52, 1, 2, 1, 7), Integer32().subtype(subtypeSpec=ValueRangeConstraint(0,128))).setMaxAccess("readcreate")
if mibBuilder.loadTexts: intSrvFlowSenderAddrLength.setDescription("The length of the sender's  address  in  bits.\n            This  is  the CIDR Prefix Length, which for IP4\n            hosts and multicast addresses is 32 bits.  This\n            object may not be changed when the value of the\n            RowStatus object is 'active'.")
intSrvFlowProtocol = MibTableColumn((1, 3, 6, 1, 2, 1, 52, 1, 2, 1, 8), Protocol()).setMaxAccess("readcreate")
if mibBuilder.loadTexts: intSrvFlowProtocol.setDescription("The IP Protocol used by a session.   This  ob-\n            ject  may  not be changed when the value of the\n            RowStatus object is 'active'.")
intSrvFlowDestPort = MibTableColumn((1, 3, 6, 1, 2, 1, 52, 1, 2, 1, 9), Port()).setMaxAccess("readcreate")
if mibBuilder.loadTexts: intSrvFlowDestPort.setDescription("The UDP or TCP port number used as a  destina-\n            tion  port for all senders in this session.  If\n            the  IP   protocol   in   use,   specified   by\n            intSrvResvFwdProtocol,  is 50 (ESP) or 51 (AH),\n            this  represents  a  virtual  destination  port\n            number.   A value of zero indicates that the IP\n            protocol in use does not have ports.  This  ob-\n            ject  may  not be changed when the value of the\n            RowStatus object is 'active'.")
intSrvFlowPort = MibTableColumn((1, 3, 6, 1, 2, 1, 52, 1, 2, 1, 10), Port()).setMaxAccess("readcreate")
if mibBuilder.loadTexts: intSrvFlowPort.setDescription("The UDP or TCP port number used  as  a  source\n            port  for  this sender in this session.  If the\n            IP    protocol    in    use,    specified    by\n            intSrvResvFwdProtocol  is  50 (ESP) or 51 (AH),\n            this represents a generalized  port  identifier\n            (GPI).   A  value of zero indicates that the IP\n            protocol in use does not have ports.  This  ob-\n            ject  may  not be changed when the value of the\n            RowStatus object is 'active'.")
intSrvFlowFlowId = MibTableColumn((1, 3, 6, 1, 2, 1, 52, 1, 2, 1, 11), Integer32().subtype(subtypeSpec=ValueRangeConstraint(0,16777215))).setMaxAccess("readonly")
if mibBuilder.loadTexts: intSrvFlowFlowId.setDescription('The flow ID that  this  sender  is  using,  if\n            this  is  an IPv6 session.')
intSrvFlowInterface = MibTableColumn((1, 3, 6, 1, 2, 1, 52, 1, 2, 1, 12), InterfaceIndex()).setMaxAccess("readcreate")
if mibBuilder.loadTexts: intSrvFlowInterface.setDescription('The ifIndex value of the  interface  on  which\n            this reservation exists.')
intSrvFlowIfAddr = MibTableColumn((1, 3, 6, 1, 2, 1, 52, 1, 2, 1, 13), OctetString().subtype(subtypeSpec=ValueSizeConstraint(4,16))).setMaxAccess("readcreate")
if mibBuilder.loadTexts: intSrvFlowIfAddr.setDescription('The IP Address on the ifEntry  on  which  this\n            reservation  exists.  This is present primarily\n            to support those interfaces which layer  multi-\n            ple IP Addresses on the interface.')
intSrvFlowRate = MibTableColumn((1, 3, 6, 1, 2, 1, 52, 1, 2, 1, 14), BitRate()).setUnits('bits per second').setMaxAccess("readcreate")
if mibBuilder.loadTexts: intSrvFlowRate.setDescription("The Reserved Rate of the sender's data stream.\n            If this is a Controlled Load service flow, this\n            rate is derived from the Tspec  rate  parameter\n            (r).   If  this  is  a Guaranteed service flow,\n            this rate is derived from  the  Rspec  clearing\n            rate parameter (R).")
intSrvFlowBurst = MibTableColumn((1, 3, 6, 1, 2, 1, 52, 1, 2, 1, 15), BurstSize()).setUnits('bytes').setMaxAccess("readcreate")
if mibBuilder.loadTexts: intSrvFlowBurst.setDescription("The size of the largest  burst  expected  from\n            the sender at a time.\n\n            If this is less than  the  sender's  advertised\n            burst  size, the receiver is asking the network\n            to provide flow pacing  beyond  what  would  be\n            provided  under normal circumstances. Such pac-\n            ing is at the network's option.")
intSrvFlowWeight = MibTableColumn((1, 3, 6, 1, 2, 1, 52, 1, 2, 1, 16), Integer32()).setMaxAccess("readcreate")
if mibBuilder.loadTexts: intSrvFlowWeight.setDescription('The weight used  to  prioritize  the  traffic.\n            Note  that the interpretation of this object is\n            implementation-specific,   as   implementations\n            vary in their use of weighting procedures.')
intSrvFlowQueue = MibTableColumn((1, 3, 6, 1, 2, 1, 52, 1, 2, 1, 17), Integer32()).setMaxAccess("readcreate")
if mibBuilder.loadTexts: intSrvFlowQueue.setDescription('The number of the queue used by this  traffic.\n            Note  that the interpretation of this object is\n            implementation-specific,   as   implementations\n            vary in their use of queue identifiers.')
intSrvFlowMinTU = MibTableColumn((1, 3, 6, 1, 2, 1, 52, 1, 2, 1, 18), MessageSize()).setMaxAccess("readcreate")
if mibBuilder.loadTexts: intSrvFlowMinTU.setDescription('The minimum message size for  this  flow.  The\n            policing  algorithm will treat smaller messages\n            as though they are this size.')
intSrvFlowMaxTU = MibTableColumn((1, 3, 6, 1, 2, 1, 52, 1, 2, 1, 19), MessageSize()).setMaxAccess("readcreate")
if mibBuilder.loadTexts: intSrvFlowMaxTU.setDescription('The maximum datagram size for this  flow  that\n            will conform to the traffic specification. This\n            value cannot exceed the MTU of the interface.')
intSrvFlowBestEffort = MibTableColumn((1, 3, 6, 1, 2, 1, 52, 1, 2, 1, 20), Counter32()).setMaxAccess("readonly")
if mibBuilder.loadTexts: intSrvFlowBestEffort.setDescription('The number of packets that  were  remanded  to\n            best effort service.')
intSrvFlowPoliced = MibTableColumn((1, 3, 6, 1, 2, 1, 52, 1, 2, 1, 21), Counter32()).setMaxAccess("readonly")
if mibBuilder.loadTexts: intSrvFlowPoliced.setDescription("The number of packets policed since the incep-\n            tion of the flow's service.")
intSrvFlowDiscard = MibTableColumn((1, 3, 6, 1, 2, 1, 52, 1, 2, 1, 22), TruthValue().clone('false')).setMaxAccess("readcreate")
if mibBuilder.loadTexts: intSrvFlowDiscard.setDescription("If 'true', the flow  is  to  incur  loss  when\n            traffic is policed.  If 'false', policed traff-\n            ic is treated as best effort traffic.")
intSrvFlowService = MibTableColumn((1, 3, 6, 1, 2, 1, 52, 1, 2, 1, 23), QosService()).setMaxAccess("readonly")
if mibBuilder.loadTexts: intSrvFlowService.setDescription('The QoS service being applied to this flow.')
intSrvFlowOrder = MibTableColumn((1, 3, 6, 1, 2, 1, 52, 1, 2, 1, 24), Integer32().subtype(subtypeSpec=ValueRangeConstraint(0,65535))).setMaxAccess("readcreate")
if mibBuilder.loadTexts: intSrvFlowOrder.setDescription('In the event of ambiguity, the order in  which\n            the  classifier  should  make  its comparisons.\n            The row with intSrvFlowOrder=0 is tried  first,\n            and  comparisons  proceed  in  the order of in-\n            creasing value.  Non-serial implementations  of\n            the classifier should emulate this behavior.')
intSrvFlowStatus = MibTableColumn((1, 3, 6, 1, 2, 1, 52, 1, 2, 1, 25), RowStatus()).setMaxAccess("readcreate")
if mibBuilder.loadTexts: intSrvFlowStatus.setDescription("'active' for all active  flows.   This  object\n            may be used to install static classifier infor-\n            mation, delete classifier information,  or  au-\n            thorize such.")
intSrvFlowNewIndex = MibScalar((1, 3, 6, 1, 2, 1, 52, 2, 1), TestAndIncr()).setMaxAccess("readwrite")
if mibBuilder.loadTexts: intSrvFlowNewIndex.setDescription("This  object  is  used  to  assign  values  to\n            intSrvFlowNumber  as described in 'Textual Con-\n            ventions  for  SNMPv2'.   The  network  manager\n            reads  the  object,  and  then writes the value\n            back in the SET that creates a new instance  of\n            intSrvFlowEntry.   If  the  SET  fails with the\n            code 'inconsistentValue', then the process must\n            be  repeated; If the SET succeeds, then the ob-\n            ject is incremented, and the  new  instance  is\n            created according to the manager's directions.")
intSrvGroups = MibIdentifier((1, 3, 6, 1, 2, 1, 52, 4, 1))
intSrvCompliances = MibIdentifier((1, 3, 6, 1, 2, 1, 52, 4, 2))
intSrvCompliance = ModuleCompliance((1, 3, 6, 1, 2, 1, 52, 4, 2, 1)).setObjects(*(("INTEGRATED-SERVICES-MIB", "intSrvIfAttribGroup"), ("INTEGRATED-SERVICES-MIB", "intSrvFlowsGroup"),))
if mibBuilder.loadTexts: intSrvCompliance.setDescription('The compliance statement ')
intSrvIfAttribGroup = ObjectGroup((1, 3, 6, 1, 2, 1, 52, 4, 1, 1)).setObjects(*(("INTEGRATED-SERVICES-MIB", "intSrvIfAttribAllocatedBits"), ("INTEGRATED-SERVICES-MIB", "intSrvIfAttribMaxAllocatedBits"), ("INTEGRATED-SERVICES-MIB", "intSrvIfAttribAllocatedBuffer"), ("INTEGRATED-SERVICES-MIB", "intSrvIfAttribFlows"), ("INTEGRATED-SERVICES-MIB", "intSrvIfAttribPropagationDelay"), ("INTEGRATED-SERVICES-MIB", "intSrvIfAttribStatus"),))
if mibBuilder.loadTexts: intSrvIfAttribGroup.setDescription('These objects are required  for  Systems  sup-\n            porting the Integrated Services Architecture.')
intSrvFlowsGroup = ObjectGroup((1, 3, 6, 1, 2, 1, 52, 4, 1, 2)).setObjects(*(("INTEGRATED-SERVICES-MIB", "intSrvFlowType"), ("INTEGRATED-SERVICES-MIB", "intSrvFlowOwner"), ("INTEGRATED-SERVICES-MIB", "intSrvFlowDestAddr"), ("INTEGRATED-SERVICES-MIB", "intSrvFlowSenderAddr"), ("INTEGRATED-SERVICES-MIB", "intSrvFlowDestAddrLength"), ("INTEGRATED-SERVICES-MIB", "intSrvFlowSenderAddrLength"), ("INTEGRATED-SERVICES-MIB", "intSrvFlowProtocol"), ("INTEGRATED-SERVICES-MIB", "intSrvFlowDestPort"), ("INTEGRATED-SERVICES-MIB", "intSrvFlowPort"), ("INTEGRATED-SERVICES-MIB", "intSrvFlowInterface"), ("INTEGRATED-SERVICES-MIB", "intSrvFlowBestEffort"), ("INTEGRATED-SERVICES-MIB", "intSrvFlowRate"), ("INTEGRATED-SERVICES-MIB", "intSrvFlowBurst"), ("INTEGRATED-SERVICES-MIB", "intSrvFlowWeight"), ("INTEGRATED-SERVICES-MIB", "intSrvFlowQueue"), ("INTEGRATED-SERVICES-MIB", "intSrvFlowMinTU"), ("INTEGRATED-SERVICES-MIB", "intSrvFlowDiscard"), ("INTEGRATED-SERVICES-MIB", "intSrvFlowPoliced"), ("INTEGRATED-SERVICES-MIB", "intSrvFlowService"), ("INTEGRATED-SERVICES-MIB", "intSrvFlowIfAddr"), ("INTEGRATED-SERVICES-MIB", "intSrvFlowOrder"), ("INTEGRATED-SERVICES-MIB", "intSrvFlowStatus"),))
if mibBuilder.loadTexts: intSrvFlowsGroup.setDescription('These objects are required  for  Systems  sup-\n            porting the Integrated Services Architecture.')
mibBuilder.exportSymbols("INTEGRATED-SERVICES-MIB", intSrvFlowDiscard=intSrvFlowDiscard, intSrvFlowInterface=intSrvFlowInterface, intSrvIfAttribMaxAllocatedBits=intSrvIfAttribMaxAllocatedBits, intSrvFlowDestAddr=intSrvFlowDestAddr, intSrvIfAttribGroup=intSrvIfAttribGroup, intSrvFlowSenderAddr=intSrvFlowSenderAddr, intSrvIfAttribTable=intSrvIfAttribTable, intSrvFlowIfAddr=intSrvFlowIfAddr, intSrvConformance=intSrvConformance, intSrvFlowNewIndex=intSrvFlowNewIndex, intSrvIfAttribEntry=intSrvIfAttribEntry, intSrvFlowSenderAddrLength=intSrvFlowSenderAddrLength, intSrvFlowProtocol=intSrvFlowProtocol, Port=Port, intSrvFlowType=intSrvFlowType, intSrvFlowService=intSrvFlowService, intSrvNotifications=intSrvNotifications, intSrvFlowDestPort=intSrvFlowDestPort, intSrvFlowStatus=intSrvFlowStatus, QosService=QosService, intSrvGenObjects=intSrvGenObjects, MessageSize=MessageSize, intSrvFlowRate=intSrvFlowRate, intSrvCompliances=intSrvCompliances, intSrvFlowsGroup=intSrvFlowsGroup, SessionType=SessionType, intSrvCompliance=intSrvCompliance, intSrvFlowBestEffort=intSrvFlowBestEffort, BurstSize=BurstSize, intSrvFlowPoliced=intSrvFlowPoliced, intSrvFlowFlowId=intSrvFlowFlowId, intSrvFlowDestAddrLength=intSrvFlowDestAddrLength, SessionNumber=SessionNumber, intSrvFlowWeight=intSrvFlowWeight, BitRate=BitRate, intSrvFlowOwner=intSrvFlowOwner, intSrvIfAttribAllocatedBits=intSrvIfAttribAllocatedBits, Protocol=Protocol, intSrv=intSrv, intSrvFlowTable=intSrvFlowTable, intSrvFlowBurst=intSrvFlowBurst, intSrvIfAttribFlows=intSrvIfAttribFlows, intSrvIfAttribPropagationDelay=intSrvIfAttribPropagationDelay, intSrvFlowMaxTU=intSrvFlowMaxTU, intSrvGroups=intSrvGroups, intSrvFlowOrder=intSrvFlowOrder, intSrvObjects=intSrvObjects, intSrvFlowPort=intSrvFlowPort, intSrvFlowQueue=intSrvFlowQueue, intSrvFlowMinTU=intSrvFlowMinTU, intSrvFlowEntry=intSrvFlowEntry, intSrvIfAttribStatus=intSrvIfAttribStatus, intSrvFlowNumber=intSrvFlowNumber, intSrvIfAttribAllocatedBuffer=intSrvIfAttribAllocatedBuffer, PYSNMP_MODULE_ID=intSrv)
