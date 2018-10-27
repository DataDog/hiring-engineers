#
# PySNMP MIB module ITU-ALARM-TC-MIB (http://pysnmp.sf.net)
# ASN.1 source http://mibs.snmplabs.com:80/asn1/ITU-ALARM-TC-MIB
# Produced by pysmi-0.0.7 at Sun Feb 14 00:19:29 2016
# On host bldfarm platform Linux version 4.1.13-100.fc21.x86_64 by user goose
# Using Python version 3.5.0 (default, Jan  5 2016, 17:11:52) 
#
( Integer, OctetString, ObjectIdentifier, ) = mibBuilder.importSymbols("ASN1", "Integer", "OctetString", "ObjectIdentifier")
( NamedValues, ) = mibBuilder.importSymbols("ASN1-ENUMERATION", "NamedValues")
( SingleValueConstraint, ConstraintsIntersection, ValueSizeConstraint, ConstraintsUnion, ValueRangeConstraint, ) = mibBuilder.importSymbols("ASN1-REFINEMENT", "SingleValueConstraint", "ConstraintsIntersection", "ValueSizeConstraint", "ConstraintsUnion", "ValueRangeConstraint")
( NotificationGroup, ModuleCompliance, ) = mibBuilder.importSymbols("SNMPv2-CONF", "NotificationGroup", "ModuleCompliance")
( MibScalar, MibTable, MibTableRow, MibTableColumn, ObjectIdentity, Counter64, Gauge32, IpAddress, NotificationType, Unsigned32, ModuleIdentity, MibIdentifier, Bits, TimeTicks, mib_2, iso, Integer32, Counter32, ) = mibBuilder.importSymbols("SNMPv2-SMI", "MibScalar", "MibTable", "MibTableRow", "MibTableColumn", "ObjectIdentity", "Counter64", "Gauge32", "IpAddress", "NotificationType", "Unsigned32", "ModuleIdentity", "MibIdentifier", "Bits", "TimeTicks", "mib-2", "iso", "Integer32", "Counter32")
( TextualConvention, DisplayString, ) = mibBuilder.importSymbols("SNMPv2-TC", "TextualConvention", "DisplayString")
ituAlarmTc = ModuleIdentity((1, 3, 6, 1, 2, 1, 120)).setRevisions(("2004-09-09 00:00",))
if mibBuilder.loadTexts: ituAlarmTc.setLastUpdated('200409090000Z')
if mibBuilder.loadTexts: ituAlarmTc.setOrganization('IETF Distributed Management Working Group')
if mibBuilder.loadTexts: ituAlarmTc.setContactInfo(' WG EMail: disman@ietf.org\n           Subscribe: disman-request@ietf.org\n           http://www.ietf.org/html.charters/disman-charter.html\n\n           Chair:     Randy Presuhn\n                      randy_presuhn@mindspring.com\n\n           Editors:   Sharon Chisholm\n                      Nortel Networks\n                      PO Box 3511 Station C\n                      Ottawa, Ont.  K1Y 4H7\n                      Canada\n                      schishol@nortelnetworks.com\n\n                      Dan Romascanu\n                      Avaya\n                      Atidim Technology Park, Bldg. #3\n                      Tel Aviv, 61131\n                      Israel\n                      Tel: +972-3-645-8414\n                      Email: dromasca@avaya.com')
if mibBuilder.loadTexts: ituAlarmTc.setDescription('This MIB module defines the ITU Alarm\n         textual convention for objects not expected to require\n         regular extension.\n\n         Copyright (C) The Internet Society (2004).  The\n         initial version of this MIB module was published\n         in RFC 3877.  For full legal notices see the RFC\n         itself.  Supplementary information may be available on:\n         http://www.ietf.org/copyrights/ianamib.html')
class ItuPerceivedSeverity(Integer32, TextualConvention):
    subtypeSpec = Integer32.subtypeSpec+ConstraintsUnion(SingleValueConstraint(1, 2, 3, 4, 5, 6,))
    namedValues = NamedValues(("cleared", 1), ("indeterminate", 2), ("critical", 3), ("major", 4), ("minor", 5), ("warning", 6),)

class ItuTrendIndication(Integer32, TextualConvention):
    subtypeSpec = Integer32.subtypeSpec+ConstraintsUnion(SingleValueConstraint(1, 2, 3,))
    namedValues = NamedValues(("moreSevere", 1), ("noChange", 2), ("lessSevere", 3),)

mibBuilder.exportSymbols("ITU-ALARM-TC-MIB", ItuPerceivedSeverity=ItuPerceivedSeverity, ituAlarmTc=ituAlarmTc, PYSNMP_MODULE_ID=ituAlarmTc, ItuTrendIndication=ItuTrendIndication)
