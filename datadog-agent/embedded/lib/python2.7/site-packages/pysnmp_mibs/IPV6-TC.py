#
# PySNMP MIB module IPV6-TC (http://pysnmp.sf.net)
# ASN.1 source http://mibs.snmplabs.com:80/asn1/IPV6-TC
# Produced by pysmi-0.0.7 at Sun Feb 14 00:18:33 2016
# On host bldfarm platform Linux version 4.1.13-100.fc21.x86_64 by user goose
# Using Python version 3.5.0 (default, Jan  5 2016, 17:11:52) 
#
( Integer, ObjectIdentifier, OctetString, ) = mibBuilder.importSymbols("ASN1", "Integer", "ObjectIdentifier", "OctetString")
( NamedValues, ) = mibBuilder.importSymbols("ASN1-ENUMERATION", "NamedValues")
( ValueRangeConstraint, ValueSizeConstraint, ConstraintsIntersection, SingleValueConstraint, ConstraintsUnion, ) = mibBuilder.importSymbols("ASN1-REFINEMENT", "ValueRangeConstraint", "ValueSizeConstraint", "ConstraintsIntersection", "SingleValueConstraint", "ConstraintsUnion")
( NotificationGroup, ModuleCompliance, ) = mibBuilder.importSymbols("SNMPv2-CONF", "NotificationGroup", "ModuleCompliance")
( TimeTicks, Counter32, iso, Bits, ObjectIdentity, NotificationType, Gauge32, MibScalar, MibTable, MibTableRow, MibTableColumn, Unsigned32, ModuleIdentity, Integer32, Counter64, IpAddress, MibIdentifier, ) = mibBuilder.importSymbols("SNMPv2-SMI", "TimeTicks", "Counter32", "iso", "Bits", "ObjectIdentity", "NotificationType", "Gauge32", "MibScalar", "MibTable", "MibTableRow", "MibTableColumn", "Unsigned32", "ModuleIdentity", "Integer32", "Counter64", "IpAddress", "MibIdentifier")
( TextualConvention, DisplayString, ) = mibBuilder.importSymbols("SNMPv2-TC", "TextualConvention", "DisplayString")
class Ipv6Address(OctetString, TextualConvention):
    displayHint = '2x:'
    subtypeSpec = OctetString.subtypeSpec+ValueSizeConstraint(16,16)
    fixedLength = 16

class Ipv6AddressPrefix(OctetString, TextualConvention):
    displayHint = '2x:'
    subtypeSpec = OctetString.subtypeSpec+ValueSizeConstraint(0,16)

class Ipv6AddressIfIdentifier(OctetString, TextualConvention):
    displayHint = '2x:'
    subtypeSpec = OctetString.subtypeSpec+ValueSizeConstraint(0,8)

class Ipv6IfIndex(Integer32, TextualConvention):
    displayHint = 'd'
    subtypeSpec = Integer32.subtypeSpec+ValueRangeConstraint(1,2147483647)

class Ipv6IfIndexOrZero(Integer32, TextualConvention):
    displayHint = 'd'
    subtypeSpec = Integer32.subtypeSpec+ValueRangeConstraint(0,2147483647)

mibBuilder.exportSymbols("IPV6-TC", Ipv6Address=Ipv6Address, Ipv6IfIndex=Ipv6IfIndex, Ipv6AddressPrefix=Ipv6AddressPrefix, Ipv6AddressIfIdentifier=Ipv6AddressIfIdentifier, Ipv6IfIndexOrZero=Ipv6IfIndexOrZero)
