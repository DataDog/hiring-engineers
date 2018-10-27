#
# PySNMP MIB module HC-PerfHist-TC-MIB (http://pysnmp.sf.net)
# ASN.1 source http://mibs.snmplabs.com:80/asn1/HC-PerfHist-TC-MIB
# Produced by pysmi-0.0.7 at Sun Feb 14 00:03:54 2016
# On host bldfarm platform Linux version 4.1.13-100.fc21.x86_64 by user goose
# Using Python version 3.5.0 (default, Jan  5 2016, 17:11:52) 
#
( ObjectIdentifier, OctetString, Integer, ) = mibBuilder.importSymbols("ASN1", "ObjectIdentifier", "OctetString", "Integer")
( NamedValues, ) = mibBuilder.importSymbols("ASN1-ENUMERATION", "NamedValues")
( SingleValueConstraint, ValueRangeConstraint, ValueSizeConstraint, ConstraintsIntersection, ConstraintsUnion, ) = mibBuilder.importSymbols("ASN1-REFINEMENT", "SingleValueConstraint", "ValueRangeConstraint", "ValueSizeConstraint", "ConstraintsIntersection", "ConstraintsUnion")
( NotificationGroup, ModuleCompliance, ) = mibBuilder.importSymbols("SNMPv2-CONF", "NotificationGroup", "ModuleCompliance")
( Gauge32, TimeTicks, ObjectIdentity, ModuleIdentity, Bits, Counter32, IpAddress, MibIdentifier, Integer32, Counter64, Unsigned32, mib_2, NotificationType, MibScalar, MibTable, MibTableRow, MibTableColumn, iso, ) = mibBuilder.importSymbols("SNMPv2-SMI", "Gauge32", "TimeTicks", "ObjectIdentity", "ModuleIdentity", "Bits", "Counter32", "IpAddress", "MibIdentifier", "Integer32", "Counter64", "Unsigned32", "mib-2", "NotificationType", "MibScalar", "MibTable", "MibTableRow", "MibTableColumn", "iso")
( TextualConvention, DisplayString, ) = mibBuilder.importSymbols("SNMPv2-TC", "TextualConvention", "DisplayString")
hcPerfHistTCMIB = ModuleIdentity((1, 3, 6, 1, 2, 1, 107)).setRevisions(("2004-02-03 00:00",))
if mibBuilder.loadTexts: hcPerfHistTCMIB.setLastUpdated('200402030000Z')
if mibBuilder.loadTexts: hcPerfHistTCMIB.setOrganization('ADSLMIB Working Group')
if mibBuilder.loadTexts: hcPerfHistTCMIB.setContactInfo('WG-email:  adslmib@ietf.org\n           Info:      https://www1.ietf.org/mailman/listinfo/adslmib\n\n           Chair:     Mike Sneed\n                      Sand Channel Systems\n           Postal:    P.O.  Box 37324\n                      Raleigh NC 27627-7324\n                      USA\n           Email:     sneedmike@hotmail.com\n           Phone:     +1 206 600 7022\n\n           Co-editor: Bob Ray\n                      PESA Switching Systems, Inc.\n           Postal:    330-A Wynn Drive\n                      Huntsville, AL 35805\n                      USA\n           Email:     rray@pesa.com\n           Phone:     +1 256 726 9200 ext.  142\n\n           Co-editor: Rajesh Abbi\n                      Alcatel USA\n           Postal:    2301 Sugar Bush Road\n                      Raleigh, NC 27612-3339\n                      USA\n           Email:     Rajesh.Abbi@alcatel.com\n           Phone:     +1 919 850 6194\n           ')
if mibBuilder.loadTexts: hcPerfHistTCMIB.setDescription('This MIB Module provides Textual Conventions to be\n            used by systems supporting 15 minute based performance\n            history counts that require high-capacity counts.\n\n            Copyright (C) The Internet Society (2004).  This version\n            of this MIB module is part of RFC 3705: see the RFC\n            itself for full legal notices.')
class HCPerfValidIntervals(Integer32, TextualConvention):
    subtypeSpec = Integer32.subtypeSpec+ValueRangeConstraint(0,96)

class HCPerfInvalidIntervals(Integer32, TextualConvention):
    subtypeSpec = Integer32.subtypeSpec+ValueRangeConstraint(0,96)

class HCPerfTimeElapsed(Integer32, TextualConvention):
    subtypeSpec = Integer32.subtypeSpec+ValueRangeConstraint(0,86399)

class HCPerfIntervalThreshold(Unsigned32, TextualConvention):
    subtypeSpec = Unsigned32.subtypeSpec+ValueRangeConstraint(0,900)

class HCPerfCurrentCount(Counter64, TextualConvention):
    pass

class HCPerfIntervalCount(Counter64, TextualConvention):
    pass

class HCPerfTotalCount(Counter64, TextualConvention):
    pass

mibBuilder.exportSymbols("HC-PerfHist-TC-MIB", HCPerfTimeElapsed=HCPerfTimeElapsed, HCPerfTotalCount=HCPerfTotalCount, HCPerfIntervalCount=HCPerfIntervalCount, HCPerfCurrentCount=HCPerfCurrentCount, HCPerfValidIntervals=HCPerfValidIntervals, hcPerfHistTCMIB=hcPerfHistTCMIB, HCPerfInvalidIntervals=HCPerfInvalidIntervals, HCPerfIntervalThreshold=HCPerfIntervalThreshold, PYSNMP_MODULE_ID=hcPerfHistTCMIB)
