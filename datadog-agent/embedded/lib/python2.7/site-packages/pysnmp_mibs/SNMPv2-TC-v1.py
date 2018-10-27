#
# PySNMP MIB module SNMPv2-TC-v1 (http://pysnmp.sf.net)
# ASN.1 source http://mibs.snmplabs.com:80/asn1/SNMPv2-TC-v1
# Produced by pysmi-0.0.7 at Sun Feb 14 00:08:56 2016
# On host bldfarm platform Linux version 4.1.13-100.fc21.x86_64 by user goose
# Using Python version 3.5.0 (default, Jan  5 2016, 17:11:52) 
#
( Integer, OctetString, ObjectIdentifier, ) = mibBuilder.importSymbols("ASN1", "Integer", "OctetString", "ObjectIdentifier")
( NamedValues, ) = mibBuilder.importSymbols("ASN1-ENUMERATION", "NamedValues")
( SingleValueConstraint, ConstraintsUnion, ValueRangeConstraint, ConstraintsIntersection, ValueSizeConstraint, ) = mibBuilder.importSymbols("ASN1-REFINEMENT", "SingleValueConstraint", "ConstraintsUnion", "ValueRangeConstraint", "ConstraintsIntersection", "ValueSizeConstraint")
( NotificationGroup, ModuleCompliance, ) = mibBuilder.importSymbols("SNMPv2-CONF", "NotificationGroup", "ModuleCompliance")
( NotificationType, Integer32, MibIdentifier, Counter64, iso, TimeTicks, MibScalar, MibTable, MibTableRow, MibTableColumn, Gauge32, ModuleIdentity, IpAddress, Bits, Unsigned32, ObjectIdentity, Counter32, ) = mibBuilder.importSymbols("SNMPv2-SMI", "NotificationType", "Integer32", "MibIdentifier", "Counter64", "iso", "TimeTicks", "MibScalar", "MibTable", "MibTableRow", "MibTableColumn", "Gauge32", "ModuleIdentity", "IpAddress", "Bits", "Unsigned32", "ObjectIdentity", "Counter32")
( DisplayString, TextualConvention, ) = mibBuilder.importSymbols("SNMPv2-TC", "DisplayString", "TextualConvention")
class DisplayString(OctetString):
    subtypeSpec = OctetString.subtypeSpec+ValueSizeConstraint(0,255)

class PhysAddress(OctetString):
    pass

class MacAddress(OctetString):
    subtypeSpec = OctetString.subtypeSpec+ValueSizeConstraint(6,6)
    fixedLength = 6

class TruthValue(Integer32):
    subtypeSpec = Integer32.subtypeSpec+ConstraintsUnion(SingleValueConstraint(1, 2,))
    namedValues = NamedValues(("true", 1), ("false", 2),)

class TestAndIncr(Integer32):
    subtypeSpec = Integer32.subtypeSpec+ValueRangeConstraint(0,2147483647)

class AutonomousType(ObjectIdentifier):
    pass

class InstancePointer(ObjectIdentifier):
    pass

class VariablePointer(ObjectIdentifier):
    pass

class RowPointer(ObjectIdentifier):
    pass

class RowStatus(Integer32):
    subtypeSpec = Integer32.subtypeSpec+ConstraintsUnion(SingleValueConstraint(1, 2, 3, 4, 5, 6,))
    namedValues = NamedValues(("active", 1), ("notInService", 2), ("notReady", 3), ("createAndGo", 4), ("createAndWait", 5), ("destroy", 6),)

class TimeStamp(TimeTicks):
    pass

class TimeInterval(Integer32):
    subtypeSpec = Integer32.subtypeSpec+ValueRangeConstraint(0,2147483647)

class DateAndTime(OctetString):
    subtypeSpec = OctetString.subtypeSpec+ValueSizeConstraint(11,11)
    fixedLength = 11

class StorageType(Integer32):
    subtypeSpec = Integer32.subtypeSpec+ConstraintsUnion(SingleValueConstraint(1, 2, 3, 4, 5,))
    namedValues = NamedValues(("other", 1), ("volatile", 2), ("nonVolatile", 3), ("permanent", 4), ("readOnly", 5),)

class TDomain(ObjectIdentifier):
    pass

class TAddress(OctetString):
    subtypeSpec = OctetString.subtypeSpec+ValueSizeConstraint(1,255)

mibBuilder.exportSymbols("SNMPv2-TC-v1", TDomain=TDomain, VariablePointer=VariablePointer, InstancePointer=InstancePointer, StorageType=StorageType, PhysAddress=PhysAddress, TestAndIncr=TestAndIncr, AutonomousType=AutonomousType, TimeStamp=TimeStamp, RowPointer=RowPointer, TAddress=TAddress, DateAndTime=DateAndTime, RowStatus=RowStatus, MacAddress=MacAddress, DisplayString=DisplayString, TimeInterval=TimeInterval, TruthValue=TruthValue)
