#
# PySNMP MIB module DIFFSERV-DSCP-TC (http://pysnmp.sf.net)
# ASN.1 source http://mibs.snmplabs.com:80/asn1/DIFFSERV-DSCP-TC
# Produced by pysmi-0.0.7 at Sun Feb 14 00:07:28 2016
# On host bldfarm platform Linux version 4.1.13-100.fc21.x86_64 by user goose
# Using Python version 3.5.0 (default, Jan  5 2016, 17:11:52) 
#
( OctetString, Integer, ObjectIdentifier, ) = mibBuilder.importSymbols("ASN1", "OctetString", "Integer", "ObjectIdentifier")
( NamedValues, ) = mibBuilder.importSymbols("ASN1-ENUMERATION", "NamedValues")
( ConstraintsIntersection, SingleValueConstraint, ValueRangeConstraint, ValueSizeConstraint, ConstraintsUnion, ) = mibBuilder.importSymbols("ASN1-REFINEMENT", "ConstraintsIntersection", "SingleValueConstraint", "ValueRangeConstraint", "ValueSizeConstraint", "ConstraintsUnion")
( NotificationGroup, ModuleCompliance, ) = mibBuilder.importSymbols("SNMPv2-CONF", "NotificationGroup", "ModuleCompliance")
( Unsigned32, Gauge32, MibScalar, MibTable, MibTableRow, MibTableColumn, IpAddress, ModuleIdentity, ObjectIdentity, Counter64, TimeTicks, Integer32, Counter32, Bits, NotificationType, mib_2, MibIdentifier, iso, ) = mibBuilder.importSymbols("SNMPv2-SMI", "Unsigned32", "Gauge32", "MibScalar", "MibTable", "MibTableRow", "MibTableColumn", "IpAddress", "ModuleIdentity", "ObjectIdentity", "Counter64", "TimeTicks", "Integer32", "Counter32", "Bits", "NotificationType", "mib-2", "MibIdentifier", "iso")
( DisplayString, TextualConvention, ) = mibBuilder.importSymbols("SNMPv2-TC", "DisplayString", "TextualConvention")
diffServDSCPTC = ModuleIdentity((1, 3, 6, 1, 2, 1, 96)).setRevisions(("2002-05-09 00:00",))
if mibBuilder.loadTexts: diffServDSCPTC.setLastUpdated('200205090000Z')
if mibBuilder.loadTexts: diffServDSCPTC.setOrganization('IETF Differentiated Services WG')
if mibBuilder.loadTexts: diffServDSCPTC.setContactInfo('       Fred Baker\n               Cisco Systems\n               1121 Via Del Rey\n               Santa Barbara, CA 93117, USA\n               E-mail: fred@cisco.com\n\n               Kwok Ho Chan\n               Nortel Networks\n               600 Technology Park Drive\n               Billerica, MA 01821, USA\n               E-mail: khchan@nortelnetworks.com\n\n               Andrew Smith\n               Harbour Networks\n               Jiuling Building\n               21 North Xisanhuan Ave.\n               Beijing, 100089, PRC\n               E-mail: ah_smith@acm.org\n\n                 Differentiated Services Working Group:\n                 diffserv@ietf.org')
if mibBuilder.loadTexts: diffServDSCPTC.setDescription('The Textual Conventions defined in this module should be used\n       whenever a Differentiated Services Code Point is used in a MIB.')
class Dscp(Integer32, TextualConvention):
    displayHint = 'd'
    subtypeSpec = Integer32.subtypeSpec+ValueRangeConstraint(0,63)

class DscpOrAny(Integer32, TextualConvention):
    displayHint = 'd'
    subtypeSpec = Integer32.subtypeSpec+ConstraintsUnion(ValueRangeConstraint(-1,-1),ValueRangeConstraint(0,63),)
mibBuilder.exportSymbols("DIFFSERV-DSCP-TC", Dscp=Dscp, diffServDSCPTC=diffServDSCPTC, DscpOrAny=DscpOrAny, PYSNMP_MODULE_ID=diffServDSCPTC)
