#
# PySNMP MIB module LANGTAG-TC-MIB (http://pysnmp.sf.net)
# ASN.1 source http://mibs.snmplabs.com:80/asn1/LANGTAG-TC-MIB
# Produced by pysmi-0.0.7 at Sun Feb 14 00:17:53 2016
# On host bldfarm platform Linux version 4.1.13-100.fc21.x86_64 by user goose
# Using Python version 3.5.0 (default, Jan  5 2016, 17:11:52) 
#
( Integer, ObjectIdentifier, OctetString, ) = mibBuilder.importSymbols("ASN1", "Integer", "ObjectIdentifier", "OctetString")
( NamedValues, ) = mibBuilder.importSymbols("ASN1-ENUMERATION", "NamedValues")
( ValueRangeConstraint, SingleValueConstraint, ValueSizeConstraint, ConstraintsIntersection, ConstraintsUnion, ) = mibBuilder.importSymbols("ASN1-REFINEMENT", "ValueRangeConstraint", "SingleValueConstraint", "ValueSizeConstraint", "ConstraintsIntersection", "ConstraintsUnion")
( ModuleCompliance, NotificationGroup, ) = mibBuilder.importSymbols("SNMPv2-CONF", "ModuleCompliance", "NotificationGroup")
( Counter32, Counter64, iso, mib_2, NotificationType, MibScalar, MibTable, MibTableRow, MibTableColumn, IpAddress, Gauge32, ObjectIdentity, Unsigned32, MibIdentifier, Integer32, ModuleIdentity, Bits, TimeTicks, ) = mibBuilder.importSymbols("SNMPv2-SMI", "Counter32", "Counter64", "iso", "mib-2", "NotificationType", "MibScalar", "MibTable", "MibTableRow", "MibTableColumn", "IpAddress", "Gauge32", "ObjectIdentity", "Unsigned32", "MibIdentifier", "Integer32", "ModuleIdentity", "Bits", "TimeTicks")
( DisplayString, TextualConvention, ) = mibBuilder.importSymbols("SNMPv2-TC", "DisplayString", "TextualConvention")
langTagTcMIB = ModuleIdentity((1, 3, 6, 1, 2, 1, 165)).setRevisions(("2007-11-09 00:00",))
if mibBuilder.loadTexts: langTagTcMIB.setLastUpdated('200711090000Z')
if mibBuilder.loadTexts: langTagTcMIB.setOrganization('IETF Operations and Management (OPS) Area')
if mibBuilder.loadTexts: langTagTcMIB.setContactInfo('EMail: ops-area@ietf.org\n                  Home page: http://www.ops.ietf.org/')
if mibBuilder.loadTexts: langTagTcMIB.setDescription('This MIB module defines a textual convention for\n            representing BCP 47 language tags.')
class LangTag(OctetString, TextualConvention):
    displayHint = '1a'
    subtypeSpec = OctetString.subtypeSpec+ConstraintsUnion(ValueSizeConstraint(0,0),ValueSizeConstraint(2,63),)
mibBuilder.exportSymbols("LANGTAG-TC-MIB", PYSNMP_MODULE_ID=langTagTcMIB, langTagTcMIB=langTagTcMIB, LangTag=LangTag)
