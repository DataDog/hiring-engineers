#
# PySNMP MIB module IANA-ADDRESS-FAMILY-NUMBERS-MIB (http://pysnmp.sf.net)
# ASN.1 source http://mibs.snmplabs.com:80/asn1/IANA-ADDRESS-FAMILY-NUMBERS-MIB
# Produced by pysmi-0.0.7 at Sun Feb 14 00:14:00 2016
# On host bldfarm platform Linux version 4.1.13-100.fc21.x86_64 by user goose
# Using Python version 3.5.0 (default, Jan  5 2016, 17:11:52) 
#
( ObjectIdentifier, OctetString, Integer, ) = mibBuilder.importSymbols("ASN1", "ObjectIdentifier", "OctetString", "Integer")
( NamedValues, ) = mibBuilder.importSymbols("ASN1-ENUMERATION", "NamedValues")
( ConstraintsIntersection, ValueSizeConstraint, SingleValueConstraint, ConstraintsUnion, ValueRangeConstraint, ) = mibBuilder.importSymbols("ASN1-REFINEMENT", "ConstraintsIntersection", "ValueSizeConstraint", "SingleValueConstraint", "ConstraintsUnion", "ValueRangeConstraint")
( NotificationGroup, ModuleCompliance, ) = mibBuilder.importSymbols("SNMPv2-CONF", "NotificationGroup", "ModuleCompliance")
( IpAddress, Unsigned32, Counter32, iso, TimeTicks, Counter64, Bits, ModuleIdentity, Gauge32, NotificationType, ObjectIdentity, MibIdentifier, mib_2, MibScalar, MibTable, MibTableRow, MibTableColumn, Integer32, ) = mibBuilder.importSymbols("SNMPv2-SMI", "IpAddress", "Unsigned32", "Counter32", "iso", "TimeTicks", "Counter64", "Bits", "ModuleIdentity", "Gauge32", "NotificationType", "ObjectIdentity", "MibIdentifier", "mib-2", "MibScalar", "MibTable", "MibTableRow", "MibTableColumn", "Integer32")
( TextualConvention, DisplayString, ) = mibBuilder.importSymbols("SNMPv2-TC", "TextualConvention", "DisplayString")
ianaAddressFamilyNumbers = ModuleIdentity((1, 3, 6, 1, 2, 1, 72)).setRevisions(("2002-03-14 00:00", "2000-09-08 00:00", "2000-03-01 00:00", "2000-02-04 00:00", "1999-08-26 00:00",))
if mibBuilder.loadTexts: ianaAddressFamilyNumbers.setLastUpdated('200203140000Z')
if mibBuilder.loadTexts: ianaAddressFamilyNumbers.setOrganization('IANA')
if mibBuilder.loadTexts: ianaAddressFamilyNumbers.setContactInfo('Postal:    Internet Assigned Numbers Authority\n                      Internet Corporation for Assigned Names\n\t\t      and Numbers\n                      4676 Admiralty Way, Suite 330\n                      Marina del Rey, CA 90292-6601\n                      USA\n\n          Tel:    +1  310-823-9358\n          E-Mail: iana@iana.org')
if mibBuilder.loadTexts: ianaAddressFamilyNumbers.setDescription('The MIB module defines the AddressFamilyNumbers\n          textual convention.')
class AddressFamilyNumbers(Integer32, TextualConvention):
    subtypeSpec = Integer32.subtypeSpec+ConstraintsUnion(SingleValueConstraint(0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 65535,))
    namedValues = NamedValues(("other", 0), ("ipV4", 1), ("ipV6", 2), ("nsap", 3), ("hdlc", 4), ("bbn1822", 5), ("all802", 6), ("e163", 7), ("e164", 8), ("f69", 9), ("x121", 10), ("ipx", 11), ("appleTalk", 12), ("decnetIV", 13), ("banyanVines", 14), ("e164withNsap", 15), ("dns", 16), ("distinguishedName", 17), ("asNumber", 18), ("xtpOverIpv4", 19), ("xtpOverIpv6", 20), ("xtpNativeModeXTP", 21), ("fibreChannelWWPN", 22), ("fibreChannelWWNN", 23), ("gwid", 24), ("reserved", 65535),)

mibBuilder.exportSymbols("IANA-ADDRESS-FAMILY-NUMBERS-MIB", AddressFamilyNumbers=AddressFamilyNumbers, PYSNMP_MODULE_ID=ianaAddressFamilyNumbers, ianaAddressFamilyNumbers=ianaAddressFamilyNumbers)
