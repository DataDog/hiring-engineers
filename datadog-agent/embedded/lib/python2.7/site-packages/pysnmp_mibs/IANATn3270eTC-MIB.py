#
# PySNMP MIB module IANATn3270eTC-MIB (http://pysnmp.sf.net)
# ASN.1 source http://mibs.snmplabs.com:80/asn1/IANATn3270eTC-MIB
# Produced by pysmi-0.0.7 at Sun Feb 14 00:16:11 2016
# On host bldfarm platform Linux version 4.1.13-100.fc21.x86_64 by user goose
# Using Python version 3.5.0 (default, Jan  5 2016, 17:11:52) 
#
( Integer, OctetString, ObjectIdentifier, ) = mibBuilder.importSymbols("ASN1", "Integer", "OctetString", "ObjectIdentifier")
( NamedValues, ) = mibBuilder.importSymbols("ASN1-ENUMERATION", "NamedValues")
( ValueSizeConstraint, ConstraintsIntersection, SingleValueConstraint, ConstraintsUnion, ValueRangeConstraint, ) = mibBuilder.importSymbols("ASN1-REFINEMENT", "ValueSizeConstraint", "ConstraintsIntersection", "SingleValueConstraint", "ConstraintsUnion", "ValueRangeConstraint")
( ModuleCompliance, NotificationGroup, ) = mibBuilder.importSymbols("SNMPv2-CONF", "ModuleCompliance", "NotificationGroup")
( ObjectIdentity, TimeTicks, Gauge32, mib_2, experimental, NotificationType, iso, Integer32, Counter32, MibIdentifier, Bits, ModuleIdentity, IpAddress, Counter64, MibScalar, MibTable, MibTableRow, MibTableColumn, Unsigned32, ) = mibBuilder.importSymbols("SNMPv2-SMI", "ObjectIdentity", "TimeTicks", "Gauge32", "mib-2", "experimental", "NotificationType", "iso", "Integer32", "Counter32", "MibIdentifier", "Bits", "ModuleIdentity", "IpAddress", "Counter64", "MibScalar", "MibTable", "MibTableRow", "MibTableColumn", "Unsigned32")
( DisplayString, TextualConvention, ) = mibBuilder.importSymbols("SNMPv2-TC", "DisplayString", "TextualConvention")
ianaTn3270eTcMib = ModuleIdentity((1, 3, 6, 1, 2, 1, 61)).setRevisions(("1998-07-27 00:00",))
if mibBuilder.loadTexts: ianaTn3270eTcMib.setLastUpdated('9807270000Z')
if mibBuilder.loadTexts: ianaTn3270eTcMib.setOrganization('IANA')
if mibBuilder.loadTexts: ianaTn3270eTcMib.setContactInfo('Internet Assigned Numbers Authority\n\n             Postal: USC/Information Sciences Institute\n                     4676 Admiralty Way, Marina del Rey, CA 90292\n\n             Tel:    +1  310 822 1511\n             E-Mail: iana@isi.edu')
if mibBuilder.loadTexts: ianaTn3270eTcMib.setDescription('This module defines a set of textual conventions\n            for use by the TN3270E-MIB and the TN3270E-RT-MIB.\n\n            Any additions or changes to the contents of this\n            MIB module must first be discussed on the tn3270e\n            working group list at: tn3270e@list.nih.gov\n            and approved by one of the following TN3270E\n            working group contacts:\n\n                Ed Bailey (co-chair) - elbailey@us.ibm.com\n                Michael Boe (co-chair) - mboe@cisco.com\n                Ken White - kennethw@vnet.ibm.com\n                Robert Moore - remoore@us.ibm.com\n\n            The above list of contacts can be altered with\n            the approval of the two co-chairs.\n\n            The Textual Conventions defined within this MIB have\n            no security issues associated with them unless\n            explicitly stated in their corresponding\n            DESCRIPTION clause.')
class IANATn3270eAddrType(Integer32, TextualConvention):
    subtypeSpec = Integer32.subtypeSpec+ConstraintsUnion(SingleValueConstraint(0, 1, 2,))
    namedValues = NamedValues(("unknown", 0), ("ipv4", 1), ("ipv6", 2),)

class IANATn3270eAddress(OctetString, TextualConvention):
    subtypeSpec = OctetString.subtypeSpec+ValueSizeConstraint(0,255)

class IANATn3270eClientType(Integer32, TextualConvention):
    subtypeSpec = Integer32.subtypeSpec+ConstraintsUnion(SingleValueConstraint(1, 2, 3, 4, 5, 6, 7, 8, 9, 10,))
    namedValues = NamedValues(("none", 1), ("other", 2), ("ipv4", 3), ("ipv6", 4), ("domainName", 5), ("truncDomainName", 6), ("string", 7), ("certificate", 8), ("userId", 9), ("x509dn", 10),)

class IANATn3270Functions(Bits, TextualConvention):
    namedValues = NamedValues(("transmitBinary", 0), ("timemark", 1), ("endOfRecord", 2), ("terminalType", 3), ("tn3270Regime", 4), ("scsCtlCodes", 5), ("dataStreamCtl", 6), ("responses", 7), ("bindImage", 8), ("sysreq", 9),)

class IANATn3270ResourceType(Integer32, TextualConvention):
    subtypeSpec = Integer32.subtypeSpec+ConstraintsUnion(SingleValueConstraint(1, 2, 3, 4,))
    namedValues = NamedValues(("other", 1), ("terminal", 2), ("printer", 3), ("terminalOrPrinter", 4),)

class IANATn3270DeviceType(Integer32, TextualConvention):
    subtypeSpec = Integer32.subtypeSpec+ConstraintsUnion(SingleValueConstraint(1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 100,))
    namedValues = NamedValues(("ibm3278d2", 1), ("ibm3278d2E", 2), ("ibm3278d3", 3), ("ibm3278d3E", 4), ("ibm3278d4", 5), ("ibm3278d4E", 6), ("ibm3278d5", 7), ("ibm3278d5E", 8), ("ibmDynamic", 9), ("ibm3287d1", 10), ("unknown", 100),)

class IANATn3270eLogData(OctetString, TextualConvention):
    subtypeSpec = OctetString.subtypeSpec+ConstraintsUnion(ValueSizeConstraint(0,0),ValueSizeConstraint(6,2048),)
mibBuilder.exportSymbols("IANATn3270eTC-MIB", IANATn3270eClientType=IANATn3270eClientType, ianaTn3270eTcMib=ianaTn3270eTcMib, IANATn3270ResourceType=IANATn3270ResourceType, IANATn3270eLogData=IANATn3270eLogData, IANATn3270eAddrType=IANATn3270eAddrType, PYSNMP_MODULE_ID=ianaTn3270eTcMib, IANATn3270Functions=IANATn3270Functions, IANATn3270eAddress=IANATn3270eAddress, IANATn3270DeviceType=IANATn3270DeviceType)
