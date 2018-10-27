#
# PySNMP MIB module ADSL-TC-MIB (http://pysnmp.sf.net)
# ASN.1 source http://mibs.snmplabs.com:80/asn1/ADSL-TC-MIB
# Produced by pysmi-0.0.7 at Sun Feb 14 00:04:05 2016
# On host bldfarm platform Linux version 4.1.13-100.fc21.x86_64 by user goose
# Using Python version 3.5.0 (default, Jan  5 2016, 17:11:52) 
#
( ObjectIdentifier, OctetString, Integer, ) = mibBuilder.importSymbols("ASN1", "ObjectIdentifier", "OctetString", "Integer")
( NamedValues, ) = mibBuilder.importSymbols("ASN1-ENUMERATION", "NamedValues")
( ValueRangeConstraint, SingleValueConstraint, ConstraintsUnion, ValueSizeConstraint, ConstraintsIntersection, ) = mibBuilder.importSymbols("ASN1-REFINEMENT", "ValueRangeConstraint", "SingleValueConstraint", "ConstraintsUnion", "ValueSizeConstraint", "ConstraintsIntersection")
( NotificationGroup, ModuleCompliance, ) = mibBuilder.importSymbols("SNMPv2-CONF", "NotificationGroup", "ModuleCompliance")
( Counter64, NotificationType, ObjectIdentity, transmission, iso, Integer32, MibIdentifier, Gauge32, MibScalar, MibTable, MibTableRow, MibTableColumn, IpAddress, ModuleIdentity, Counter32, Unsigned32, TimeTicks, Bits, ) = mibBuilder.importSymbols("SNMPv2-SMI", "Counter64", "NotificationType", "ObjectIdentity", "transmission", "iso", "Integer32", "MibIdentifier", "Gauge32", "MibScalar", "MibTable", "MibTableRow", "MibTableColumn", "IpAddress", "ModuleIdentity", "Counter32", "Unsigned32", "TimeTicks", "Bits")
( TextualConvention, DisplayString, ) = mibBuilder.importSymbols("SNMPv2-TC", "TextualConvention", "DisplayString")
adslMIB = MibIdentifier((1, 3, 6, 1, 2, 1, 10, 94))
adsltcmib = ModuleIdentity((1, 3, 6, 1, 2, 1, 10, 94, 2)).setRevisions(("1999-08-19 00:00",))
if mibBuilder.loadTexts: adsltcmib.setLastUpdated('9908190000Z')
if mibBuilder.loadTexts: adsltcmib.setOrganization('IETF ADSL MIB Working Group')
if mibBuilder.loadTexts: adsltcmib.setContactInfo('\n       Gregory Bathrick\n       AG Communication Systems\n       A Subsidiary of Lucent Technologies\n       2500 W Utopia Rd.\n       Phoenix, AZ 85027 USA\n       Tel: +1 602-582-7679\n       Fax: +1 602-582-7697\n       E-mail: bathricg@agcs.com\n\n       Faye Ly\n       Copper Mountain Networks\n       Norcal Office\n       2470 Embarcadero Way\n       Palo Alto, CA 94303\n       Tel: +1 650-858-8500\n       Fax: +1 650-858-8085\n       E-Mail: faye@coppermountain.com\n       IETF ADSL MIB Working Group (adsl@xlist.agcs.com)\n       ')
if mibBuilder.loadTexts: adsltcmib.setDescription('The MIB module which provides a ADSL\n           Line Coding Textual Convention to be used\n           by ADSL Lines.')
class AdslLineCodingType(Integer32, TextualConvention):
    subtypeSpec = Integer32.subtypeSpec+ConstraintsUnion(SingleValueConstraint(1, 2, 3, 4,))
    namedValues = NamedValues(("other", 1), ("dmt", 2), ("cap", 3), ("qam", 4),)

class AdslPerfCurrDayCount(Gauge32, TextualConvention):
    pass

class AdslPerfPrevDayCount(Gauge32, TextualConvention):
    pass

class AdslPerfTimeElapsed(Gauge32, TextualConvention):
    pass

mibBuilder.exportSymbols("ADSL-TC-MIB", AdslLineCodingType=AdslLineCodingType, AdslPerfPrevDayCount=AdslPerfPrevDayCount, AdslPerfCurrDayCount=AdslPerfCurrDayCount, adslMIB=adslMIB, AdslPerfTimeElapsed=AdslPerfTimeElapsed, PYSNMP_MODULE_ID=adsltcmib, adsltcmib=adsltcmib)
