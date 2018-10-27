#
# PySNMP MIB module ENTITY-STATE-TC-MIB (http://pysnmp.sf.net)
# ASN.1 source http://mibs.snmplabs.com:80/asn1/ENTITY-STATE-TC-MIB
# Produced by pysmi-0.0.7 at Sun Feb 14 00:11:52 2016
# On host bldfarm platform Linux version 4.1.13-100.fc21.x86_64 by user goose
# Using Python version 3.5.0 (default, Jan  5 2016, 17:11:52) 
#
( ObjectIdentifier, OctetString, Integer, ) = mibBuilder.importSymbols("ASN1", "ObjectIdentifier", "OctetString", "Integer")
( NamedValues, ) = mibBuilder.importSymbols("ASN1-ENUMERATION", "NamedValues")
( ConstraintsUnion, SingleValueConstraint, ConstraintsIntersection, ValueSizeConstraint, ValueRangeConstraint, ) = mibBuilder.importSymbols("ASN1-REFINEMENT", "ConstraintsUnion", "SingleValueConstraint", "ConstraintsIntersection", "ValueSizeConstraint", "ValueRangeConstraint")
( NotificationGroup, ModuleCompliance, ) = mibBuilder.importSymbols("SNMPv2-CONF", "NotificationGroup", "ModuleCompliance")
( Unsigned32, MibScalar, MibTable, MibTableRow, MibTableColumn, iso, Counter32, TimeTicks, Bits, mib_2, ObjectIdentity, IpAddress, ModuleIdentity, Integer32, Counter64, NotificationType, Gauge32, MibIdentifier, ) = mibBuilder.importSymbols("SNMPv2-SMI", "Unsigned32", "MibScalar", "MibTable", "MibTableRow", "MibTableColumn", "iso", "Counter32", "TimeTicks", "Bits", "mib-2", "ObjectIdentity", "IpAddress", "ModuleIdentity", "Integer32", "Counter64", "NotificationType", "Gauge32", "MibIdentifier")
( DisplayString, TextualConvention, ) = mibBuilder.importSymbols("SNMPv2-TC", "DisplayString", "TextualConvention")
entityStateTc = ModuleIdentity((1, 3, 6, 1, 2, 1, 130)).setRevisions(("2005-11-22 00:00",))
if mibBuilder.loadTexts: entityStateTc.setLastUpdated('200511220000Z')
if mibBuilder.loadTexts: entityStateTc.setOrganization('IETF Entity MIB Working Group')
if mibBuilder.loadTexts: entityStateTc.setContactInfo('General Discussion: entmib@ietf.org\n                 To Subscribe:\n                 http://www.ietf.org/mailman/listinfo/entmib\n\n                 http://www.ietf.org/html.charters/entmib-charter.html\n\n                 Sharon Chisholm\n                 Nortel Networks\n                 PO Box 3511 Station C\n                 Ottawa, Ont.  K1Y 4H7\n                 Canada\n                 schishol@nortel.com\n\n                 David T. Perkins\n                 548 Qualbrook Ct\n                 San Jose, CA 95110\n                 USA\n                 Phone: 408 394-8702\n                 dperkins@snmpinfo.com')
if mibBuilder.loadTexts: entityStateTc.setDescription('This MIB defines state textual conventions.\n\n                 Copyright (C) The Internet Society 2005.  This version\n                 of this MIB module is part of RFC 4268;  see the RFC\n                 itself for full legal notices.')
class EntityAdminState(Integer32, TextualConvention):
    subtypeSpec = Integer32.subtypeSpec+ConstraintsUnion(SingleValueConstraint(1, 2, 3, 4,))
    namedValues = NamedValues(("unknown", 1), ("locked", 2), ("shuttingDown", 3), ("unlocked", 4),)

class EntityOperState(Integer32, TextualConvention):
    subtypeSpec = Integer32.subtypeSpec+ConstraintsUnion(SingleValueConstraint(1, 2, 3, 4,))
    namedValues = NamedValues(("unknown", 1), ("disabled", 2), ("enabled", 3), ("testing", 4),)

class EntityUsageState(Integer32, TextualConvention):
    subtypeSpec = Integer32.subtypeSpec+ConstraintsUnion(SingleValueConstraint(1, 2, 3, 4,))
    namedValues = NamedValues(("unknown", 1), ("idle", 2), ("active", 3), ("busy", 4),)

class EntityAlarmStatus(Bits, TextualConvention):
    namedValues = NamedValues(("unknown", 0), ("underRepair", 1), ("critical", 2), ("major", 3), ("minor", 4), ("warning", 5), ("indeterminate", 6),)

class EntityStandbyStatus(Integer32, TextualConvention):
    subtypeSpec = Integer32.subtypeSpec+ConstraintsUnion(SingleValueConstraint(1, 2, 3, 4,))
    namedValues = NamedValues(("unknown", 1), ("hotStandby", 2), ("coldStandby", 3), ("providingService", 4),)

mibBuilder.exportSymbols("ENTITY-STATE-TC-MIB", EntityAdminState=EntityAdminState, EntityStandbyStatus=EntityStandbyStatus, PYSNMP_MODULE_ID=entityStateTc, EntityUsageState=EntityUsageState, entityStateTc=entityStateTc, EntityAlarmStatus=EntityAlarmStatus, EntityOperState=EntityOperState)
