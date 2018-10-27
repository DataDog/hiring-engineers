#
# PySNMP MIB module INET-ADDRESS-MIB (http://pysnmp.sf.net)
# ASN.1 source http://mibs.snmplabs.com:80/asn1/INET-ADDRESS-MIB
# Produced by pysmi-0.0.7 at Sun Feb 14 00:04:40 2016
# On host bldfarm platform Linux version 4.1.13-100.fc21.x86_64 by user goose
# Using Python version 3.5.0 (default, Jan  5 2016, 17:11:52) 
#
( ObjectIdentifier, Integer, OctetString, ) = mibBuilder.importSymbols("ASN1", "ObjectIdentifier", "Integer", "OctetString")
( NamedValues, ) = mibBuilder.importSymbols("ASN1-ENUMERATION", "NamedValues")
( ValueSizeConstraint, ConstraintsUnion, SingleValueConstraint, ConstraintsIntersection, ValueRangeConstraint, ) = mibBuilder.importSymbols("ASN1-REFINEMENT", "ValueSizeConstraint", "ConstraintsUnion", "SingleValueConstraint", "ConstraintsIntersection", "ValueRangeConstraint")
( NotificationGroup, ModuleCompliance, ) = mibBuilder.importSymbols("SNMPv2-CONF", "NotificationGroup", "ModuleCompliance")
( MibScalar, MibTable, MibTableRow, MibTableColumn, TimeTicks, mib_2, Counter32, ObjectIdentity, MibIdentifier, iso, IpAddress, Integer32, Unsigned32, NotificationType, Gauge32, Bits, ModuleIdentity, Counter64, ) = mibBuilder.importSymbols("SNMPv2-SMI", "MibScalar", "MibTable", "MibTableRow", "MibTableColumn", "TimeTicks", "mib-2", "Counter32", "ObjectIdentity", "MibIdentifier", "iso", "IpAddress", "Integer32", "Unsigned32", "NotificationType", "Gauge32", "Bits", "ModuleIdentity", "Counter64")
( DisplayString, TextualConvention, ) = mibBuilder.importSymbols("SNMPv2-TC", "DisplayString", "TextualConvention")
inetAddressMIB = ModuleIdentity((1, 3, 6, 1, 2, 1, 76)).setRevisions(("2005-02-04 00:00", "2002-05-09 00:00", "2000-06-08 00:00",))
if mibBuilder.loadTexts: inetAddressMIB.setLastUpdated('200502040000Z')
if mibBuilder.loadTexts: inetAddressMIB.setOrganization('IETF Operations and Management Area')
if mibBuilder.loadTexts: inetAddressMIB.setContactInfo('Juergen Schoenwaelder (Editor)\n         International University Bremen\n         P.O. Box 750 561\n         28725 Bremen, Germany\n\n         Phone: +49 421 200-3587\n         EMail: j.schoenwaelder@iu-bremen.de\n\n         Send comments to <ietfmibs@ops.ietf.org>.')
if mibBuilder.loadTexts: inetAddressMIB.setDescription('This MIB module defines textual conventions for\n         representing Internet addresses.  An Internet\n         address can be an IPv4 address, an IPv6 address,\n         or a DNS domain name.  This module also defines\n         textual conventions for Internet port numbers,\n         autonomous system numbers, and the length of an\n         Internet address prefix.\n\n         Copyright (C) The Internet Society (2005).  This version\n         of this MIB module is part of RFC 4001, see the RFC\n         itself for full legal notices.')
class InetAddressType(Integer32, TextualConvention):
    subtypeSpec = Integer32.subtypeSpec+ConstraintsUnion(SingleValueConstraint(0, 1, 2, 3, 4, 16,))
    namedValues = NamedValues(("unknown", 0), ("ipv4", 1), ("ipv6", 2), ("ipv4z", 3), ("ipv6z", 4), ("dns", 16),)

class InetAddress(OctetString, TextualConvention):
    subtypeSpec = OctetString.subtypeSpec+ValueSizeConstraint(0,255)

class InetAddressIPv4(OctetString, TextualConvention):
    displayHint = '1d.1d.1d.1d'
    subtypeSpec = OctetString.subtypeSpec+ValueSizeConstraint(4,4)
    fixedLength = 4

class InetAddressIPv6(OctetString, TextualConvention):
    displayHint = '2x:2x:2x:2x:2x:2x:2x:2x'
    subtypeSpec = OctetString.subtypeSpec+ValueSizeConstraint(16,16)
    fixedLength = 16

class InetAddressIPv4z(OctetString, TextualConvention):
    displayHint = '1d.1d.1d.1d%4d'
    subtypeSpec = OctetString.subtypeSpec+ValueSizeConstraint(8,8)
    fixedLength = 8

class InetAddressIPv6z(OctetString, TextualConvention):
    displayHint = '2x:2x:2x:2x:2x:2x:2x:2x%4d'
    subtypeSpec = OctetString.subtypeSpec+ValueSizeConstraint(20,20)
    fixedLength = 20

class InetAddressDNS(OctetString, TextualConvention):
    displayHint = '255a'
    subtypeSpec = OctetString.subtypeSpec+ValueSizeConstraint(1,255)

class InetAddressPrefixLength(Unsigned32, TextualConvention):
    displayHint = 'd'
    subtypeSpec = Unsigned32.subtypeSpec+ValueRangeConstraint(0,2040)

class InetPortNumber(Unsigned32, TextualConvention):
    displayHint = 'd'
    subtypeSpec = Unsigned32.subtypeSpec+ValueRangeConstraint(0,65535)

class InetAutonomousSystemNumber(Unsigned32, TextualConvention):
    displayHint = 'd'

class InetScopeType(Integer32, TextualConvention):
    subtypeSpec = Integer32.subtypeSpec+ConstraintsUnion(SingleValueConstraint(1, 2, 3, 4, 5, 8, 14,))
    namedValues = NamedValues(("interfaceLocal", 1), ("linkLocal", 2), ("subnetLocal", 3), ("adminLocal", 4), ("siteLocal", 5), ("organizationLocal", 8), ("global", 14),)

class InetZoneIndex(Unsigned32, TextualConvention):
    displayHint = 'd'

class InetVersion(Integer32, TextualConvention):
    subtypeSpec = Integer32.subtypeSpec+ConstraintsUnion(SingleValueConstraint(0, 1, 2,))
    namedValues = NamedValues(("unknown", 0), ("ipv4", 1), ("ipv6", 2),)

mibBuilder.exportSymbols("INET-ADDRESS-MIB", InetAddressIPv4z=InetAddressIPv4z, InetAddressDNS=InetAddressDNS, InetPortNumber=InetPortNumber, InetAddress=InetAddress, InetAutonomousSystemNumber=InetAutonomousSystemNumber, InetScopeType=InetScopeType, PYSNMP_MODULE_ID=inetAddressMIB, InetAddressIPv4=InetAddressIPv4, InetZoneIndex=InetZoneIndex, InetAddressType=InetAddressType, InetAddressIPv6=InetAddressIPv6, InetAddressPrefixLength=InetAddressPrefixLength, inetAddressMIB=inetAddressMIB, InetAddressIPv6z=InetAddressIPv6z, InetVersion=InetVersion)
