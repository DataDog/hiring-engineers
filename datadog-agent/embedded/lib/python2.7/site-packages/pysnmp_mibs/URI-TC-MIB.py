#
# PySNMP MIB module URI-TC-MIB (http://pysnmp.sf.net)
# ASN.1 source http://mibs.snmplabs.com:80/asn1/URI-TC-MIB
# Produced by pysmi-0.0.7 at Sun Feb 14 00:32:35 2016
# On host bldfarm platform Linux version 4.1.13-100.fc21.x86_64 by user goose
# Using Python version 3.5.0 (default, Jan  5 2016, 17:11:52) 
#
( OctetString, Integer, ObjectIdentifier, ) = mibBuilder.importSymbols("ASN1", "OctetString", "Integer", "ObjectIdentifier")
( NamedValues, ) = mibBuilder.importSymbols("ASN1-ENUMERATION", "NamedValues")
( ConstraintsIntersection, ValueSizeConstraint, SingleValueConstraint, ValueRangeConstraint, ConstraintsUnion, ) = mibBuilder.importSymbols("ASN1-REFINEMENT", "ConstraintsIntersection", "ValueSizeConstraint", "SingleValueConstraint", "ValueRangeConstraint", "ConstraintsUnion")
( ModuleCompliance, NotificationGroup, ) = mibBuilder.importSymbols("SNMPv2-CONF", "ModuleCompliance", "NotificationGroup")
( MibIdentifier, Gauge32, MibScalar, MibTable, MibTableRow, MibTableColumn, Counter64, Unsigned32, Integer32, Bits, iso, Counter32, ObjectIdentity, IpAddress, TimeTicks, mib_2, NotificationType, ModuleIdentity, ) = mibBuilder.importSymbols("SNMPv2-SMI", "MibIdentifier", "Gauge32", "MibScalar", "MibTable", "MibTableRow", "MibTableColumn", "Counter64", "Unsigned32", "Integer32", "Bits", "iso", "Counter32", "ObjectIdentity", "IpAddress", "TimeTicks", "mib-2", "NotificationType", "ModuleIdentity")
( DisplayString, TextualConvention, ) = mibBuilder.importSymbols("SNMPv2-TC", "DisplayString", "TextualConvention")
uriTcMIB = ModuleIdentity((1, 3, 6, 1, 2, 1, 164)).setRevisions(("2007-09-10 00:00",))
if mibBuilder.loadTexts: uriTcMIB.setLastUpdated('200709100000Z')
if mibBuilder.loadTexts: uriTcMIB.setOrganization('IETF Operations and Management (OPS) Area')
if mibBuilder.loadTexts: uriTcMIB.setContactInfo('EMail: ops-area@ietf.org\n                  Home page: http://www.ops.ietf.org/')
if mibBuilder.loadTexts: uriTcMIB.setDescription('This MIB module defines textual conventions for\n            representing URIs, as defined by RFC 3986 STD 66.')
class Uri(OctetString, TextualConvention):
    displayHint = '1a'

class Uri255(OctetString, TextualConvention):
    displayHint = '255a'
    subtypeSpec = OctetString.subtypeSpec+ValueSizeConstraint(0,255)

class Uri1024(OctetString, TextualConvention):
    displayHint = '1024a'
    subtypeSpec = OctetString.subtypeSpec+ValueSizeConstraint(0,1024)

mibBuilder.exportSymbols("URI-TC-MIB", PYSNMP_MODULE_ID=uriTcMIB, Uri=Uri, Uri255=Uri255, Uri1024=Uri1024, uriTcMIB=uriTcMIB)
