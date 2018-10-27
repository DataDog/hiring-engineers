#
# PySNMP MIB module SIP-MIB-SMI (http://pysnmp.sf.net)
# ASN.1 source http://mibs.snmplabs.com:80/asn1/SIP-MIB-SMI
# Produced by pysmi-0.0.7 at Sun Feb 14 00:28:08 2016
# On host bldfarm platform Linux version 4.1.13-100.fc21.x86_64 by user goose
# Using Python version 3.5.0 (default, Jan  5 2016, 17:11:52) 
#
( ObjectIdentifier, Integer, OctetString, ) = mibBuilder.importSymbols("ASN1", "ObjectIdentifier", "Integer", "OctetString")
( NamedValues, ) = mibBuilder.importSymbols("ASN1-ENUMERATION", "NamedValues")
( ConstraintsIntersection, SingleValueConstraint, ConstraintsUnion, ValueRangeConstraint, ValueSizeConstraint, ) = mibBuilder.importSymbols("ASN1-REFINEMENT", "ConstraintsIntersection", "SingleValueConstraint", "ConstraintsUnion", "ValueRangeConstraint", "ValueSizeConstraint")
( NotificationGroup, ModuleCompliance, ) = mibBuilder.importSymbols("SNMPv2-CONF", "NotificationGroup", "ModuleCompliance")
( TimeTicks, Counter32, iso, Unsigned32, Counter64, IpAddress, mib_2, ModuleIdentity, Gauge32, Integer32, Bits, ObjectIdentity, MibIdentifier, MibScalar, MibTable, MibTableRow, MibTableColumn, NotificationType, ) = mibBuilder.importSymbols("SNMPv2-SMI", "TimeTicks", "Counter32", "iso", "Unsigned32", "Counter64", "IpAddress", "mib-2", "ModuleIdentity", "Gauge32", "Integer32", "Bits", "ObjectIdentity", "MibIdentifier", "MibScalar", "MibTable", "MibTableRow", "MibTableColumn", "NotificationType")
( DisplayString, TextualConvention, ) = mibBuilder.importSymbols("SNMPv2-TC", "DisplayString", "TextualConvention")
sipMIB = ModuleIdentity((1, 3, 6, 1, 2, 1, 9998))
if mibBuilder.loadTexts: sipMIB.setLastUpdated('200007080000Z')
if mibBuilder.loadTexts: sipMIB.setOrganization('IETF SIP Working Group, SIP MIB Team')
if mibBuilder.loadTexts: sipMIB.setContactInfo('SIP MIB Team email: sip-mib@egroups.com \n\n                 Co-editor  Kevin Lingle \n                            Cisco Systems, Inc. \n                 postal:    7025 Kit Creek Road \n\nLingle/Maeng/Walker                                                  5 \nInternet Draft            SIP-MIB                          July, 2000 \n\n                            P.O. Box 14987 \n                            Research Triangle Park, NC 27709 \n                            USA \n                 email:     klingle@cisco.com \n                 phone:     +1-919-392-2029 \n\n                 Co-editor  Joon Maeng \n                            VTEL Corporation \n                 postal:    108 Wild Basin Rd. \n                            Austin, TX 78746 \n                            USA \n                 email:     joon_maeng@vtel.com \n                 phone:     +1-512-437-4567 \n\n                 Co-editor  Dave Walker \n                            SS8 Networks, Inc. \n                 postal:    80 Hines Road \n                            Kanata, ON  K2K 2T8 \n                            Canada \n                 email:     drwalker@ss8networks.com \n                 phone:     +1 613 592 2100')
if mibBuilder.loadTexts: sipMIB.setDescription('Initial version of Session Initiation Protocol (SIP) \n                 MIB module that defines base OID for all other \n                 SIP-related MIB Modules.')
mibBuilder.exportSymbols("SIP-MIB-SMI", sipMIB=sipMIB, PYSNMP_MODULE_ID=sipMIB)
