#
# PySNMP MIB module SIP-TC-MIB (http://pysnmp.sf.net)
# ASN.1 source http://mibs.snmplabs.com:80/asn1/SIP-TC-MIB
# Produced by pysmi-0.0.7 at Sun Feb 14 00:28:00 2016
# On host bldfarm platform Linux version 4.1.13-100.fc21.x86_64 by user goose
# Using Python version 3.5.0 (default, Jan  5 2016, 17:11:52) 
#
( OctetString, ObjectIdentifier, Integer, ) = mibBuilder.importSymbols("ASN1", "OctetString", "ObjectIdentifier", "Integer")
( NamedValues, ) = mibBuilder.importSymbols("ASN1-ENUMERATION", "NamedValues")
( ValueRangeConstraint, ConstraintsUnion, ValueSizeConstraint, SingleValueConstraint, ConstraintsIntersection, ) = mibBuilder.importSymbols("ASN1-REFINEMENT", "ValueRangeConstraint", "ConstraintsUnion", "ValueSizeConstraint", "SingleValueConstraint", "ConstraintsIntersection")
( ModuleCompliance, NotificationGroup, ) = mibBuilder.importSymbols("SNMPv2-CONF", "ModuleCompliance", "NotificationGroup")
( IpAddress, TimeTicks, ObjectIdentity, Unsigned32, Integer32, Gauge32, MibScalar, MibTable, MibTableRow, MibTableColumn, iso, mib_2, Counter64, Bits, MibIdentifier, ModuleIdentity, Counter32, NotificationType, ) = mibBuilder.importSymbols("SNMPv2-SMI", "IpAddress", "TimeTicks", "ObjectIdentity", "Unsigned32", "Integer32", "Gauge32", "MibScalar", "MibTable", "MibTableRow", "MibTableColumn", "iso", "mib-2", "Counter64", "Bits", "MibIdentifier", "ModuleIdentity", "Counter32", "NotificationType")
( TextualConvention, DisplayString, ) = mibBuilder.importSymbols("SNMPv2-TC", "TextualConvention", "DisplayString")
sipTC = ModuleIdentity((1, 3, 6, 1, 2, 1, 148)).setRevisions(("2007-04-20 00:00",))
if mibBuilder.loadTexts: sipTC.setLastUpdated('200704200000Z')
if mibBuilder.loadTexts: sipTC.setOrganization('IETF Session Initiation Protocol Working Group')
if mibBuilder.loadTexts: sipTC.setContactInfo('SIP WG email: sip@ietf.org\n\n              Co-editor  Kevin Lingle\n                         Cisco Systems, Inc.\n              postal:    7025 Kit Creek Road\n                         P.O. Box 14987\n                         Research Triangle Park, NC 27709\n                         USA\n              email:     klingle@cisco.com\n              phone:     +1 919 476 2029\n\n              Co-editor  Joon Maeng\n              email:     jmaeng@austin.rr.com\n\n              Co-editor  Jean-Francois Mule\n                         CableLabs\n              postal:    858 Coal Creek Circle\n                         Louisville, CO 80027\n                         USA\n              email:     jf.mule@cablelabs.com\n              phone:     +1 303 661 9100\n\n              Co-editor  Dave Walker\n              email:     drwalker@rogers.com')
if mibBuilder.loadTexts: sipTC.setDescription('Session Initiation Protocol (SIP) MIB TEXTUAL-CONVENTION\n        module used by other SIP-related MIB Modules.\n\n        Copyright (C) The IETF Trust (2007).  This version of\n        this MIB module is part of RFC 4780; see the RFC itself for\n\n\n\n        full legal notices.')
class SipTCTransportProtocol(Bits, TextualConvention):
    namedValues = NamedValues(("other", 0), ("udp", 1), ("tcp", 2), ("sctp", 3), ("tlsTcp", 4), ("tlsSctp", 5),)

class SipTCEntityRole(Bits, TextualConvention):
    namedValues = NamedValues(("other", 0), ("userAgent", 1), ("proxyServer", 2), ("redirectServer", 3), ("registrarServer", 4),)

class SipTCOptionTagHeaders(Bits, TextualConvention):
    namedValues = NamedValues(("require", 0), ("proxyRequire", 1), ("supported", 2), ("unsupported", 3),)

class SipTCMethodName(OctetString, TextualConvention):
    subtypeSpec = OctetString.subtypeSpec+ValueSizeConstraint(1,100)

mibBuilder.exportSymbols("SIP-TC-MIB", sipTC=sipTC, SipTCOptionTagHeaders=SipTCOptionTagHeaders, SipTCEntityRole=SipTCEntityRole, PYSNMP_MODULE_ID=sipTC, SipTCTransportProtocol=SipTCTransportProtocol, SipTCMethodName=SipTCMethodName)
