#
# PySNMP MIB module ATM-TC-MIB (http://pysnmp.sf.net)
# ASN.1 source http://mibs.snmplabs.com:80/asn1/ATM-TC-MIB
# Produced by pysmi-0.0.7 at Sun Feb 14 00:06:16 2016
# On host bldfarm platform Linux version 4.1.13-100.fc21.x86_64 by user goose
# Using Python version 3.5.0 (default, Jan  5 2016, 17:11:52) 
#
( ObjectIdentifier, Integer, OctetString, ) = mibBuilder.importSymbols("ASN1", "ObjectIdentifier", "Integer", "OctetString")
( NamedValues, ) = mibBuilder.importSymbols("ASN1-ENUMERATION", "NamedValues")
( SingleValueConstraint, ConstraintsIntersection, ValueRangeConstraint, ConstraintsUnion, ValueSizeConstraint, ) = mibBuilder.importSymbols("ASN1-REFINEMENT", "SingleValueConstraint", "ConstraintsIntersection", "ValueRangeConstraint", "ConstraintsUnion", "ValueSizeConstraint")
( NotificationGroup, ModuleCompliance, ) = mibBuilder.importSymbols("SNMPv2-CONF", "NotificationGroup", "ModuleCompliance")
( ObjectIdentity, MibIdentifier, Gauge32, Counter32, ModuleIdentity, Integer32, Bits, Counter64, mib_2, iso, MibScalar, MibTable, MibTableRow, MibTableColumn, NotificationType, IpAddress, Unsigned32, TimeTicks, ) = mibBuilder.importSymbols("SNMPv2-SMI", "ObjectIdentity", "MibIdentifier", "Gauge32", "Counter32", "ModuleIdentity", "Integer32", "Bits", "Counter64", "mib-2", "iso", "MibScalar", "MibTable", "MibTableRow", "MibTableColumn", "NotificationType", "IpAddress", "Unsigned32", "TimeTicks")
( TextualConvention, DisplayString, ) = mibBuilder.importSymbols("SNMPv2-TC", "TextualConvention", "DisplayString")
atmTCMIB = ModuleIdentity((1, 3, 6, 1, 2, 1, 37, 3))
if mibBuilder.loadTexts: atmTCMIB.setLastUpdated('9810190200Z')
if mibBuilder.loadTexts: atmTCMIB.setOrganization('IETF AToMMIB Working Group')
if mibBuilder.loadTexts: atmTCMIB.setContactInfo('          Michael Noto\n              Postal:  3Com Corporation\n                       5400 Bayfront Plaza, M/S 3109\n                       Santa Clara, CA 95052\n                       USA\n              Tel:     +1 408 326 2218\n              E-mail:  mike_noto@3com.com\n            \n                       Ethan Mickey Spiegel\n            \n              Postal:  Cisco Systems\n                       170 W. Tasman Dr.\n                       San Jose, CA 95134\n                       USA\n              Tel:     +1 408 526 6408\n              E-mail:  mspiegel@cisco.com\n            \n                       Kaj Tesink\n              Postal:  Bellcore\n                       331 Newman Springs Road\n                       Red Bank, NJ 07701\n                       USA\n              Tel:     +1 732 758 5254\n              Fax:     +1 732 758 4177\n              E-mail:  kaj@bellcore.com')
if mibBuilder.loadTexts: atmTCMIB.setDescription('This MIB Module provides Textual Conventions\n            and OBJECT-IDENTITY Objects to be used by\n            ATM systems.')
class AtmAddr(OctetString, TextualConvention):
    displayHint = '1x'
    subtypeSpec = OctetString.subtypeSpec+ValueSizeConstraint(0,40)

class AtmConnCastType(Integer32, TextualConvention):
    subtypeSpec = Integer32.subtypeSpec+ConstraintsUnion(SingleValueConstraint(1, 2, 3,))
    namedValues = NamedValues(("p2p", 1), ("p2mpRoot", 2), ("p2mpLeaf", 3),)

class AtmConnKind(Integer32, TextualConvention):
    subtypeSpec = Integer32.subtypeSpec+ConstraintsUnion(SingleValueConstraint(1, 2, 3, 4, 5,))
    namedValues = NamedValues(("pvc", 1), ("svcIncoming", 2), ("svcOutgoing", 3), ("spvcInitiator", 4), ("spvcTarget", 5),)

class AtmIlmiNetworkPrefix(OctetString, TextualConvention):
    subtypeSpec = OctetString.subtypeSpec+ConstraintsUnion(ValueSizeConstraint(8,8),ValueSizeConstraint(13,13),)
class AtmInterfaceType(Integer32, TextualConvention):
    subtypeSpec = Integer32.subtypeSpec+ConstraintsUnion(SingleValueConstraint(1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13,))
    namedValues = NamedValues(("other", 1), ("autoConfig", 2), ("ituDss2", 3), ("atmfUni3Dot0", 4), ("atmfUni3Dot1", 5), ("atmfUni4Dot0", 6), ("atmfIispUni3Dot0", 7), ("atmfIispUni3Dot1", 8), ("atmfIispUni4Dot0", 9), ("atmfPnni1Dot0", 10), ("atmfBici2Dot0", 11), ("atmfUniPvcOnly", 12), ("atmfNniPvcOnly", 13),)

class AtmServiceCategory(Integer32, TextualConvention):
    subtypeSpec = Integer32.subtypeSpec+ConstraintsUnion(SingleValueConstraint(1, 2, 3, 4, 5, 6,))
    namedValues = NamedValues(("other", 1), ("cbr", 2), ("rtVbr", 3), ("nrtVbr", 4), ("abr", 5), ("ubr", 6),)

class AtmSigDescrParamIndex(Integer32, TextualConvention):
    subtypeSpec = Integer32.subtypeSpec+ValueRangeConstraint(0,2147483647)

class AtmTrafficDescrParamIndex(Integer32, TextualConvention):
    subtypeSpec = Integer32.subtypeSpec+ValueRangeConstraint(0,2147483647)

class AtmVcIdentifier(Integer32, TextualConvention):
    subtypeSpec = Integer32.subtypeSpec+ValueRangeConstraint(0,65535)

class AtmVpIdentifier(Integer32, TextualConvention):
    subtypeSpec = Integer32.subtypeSpec+ValueRangeConstraint(0,4095)

class AtmVorXAdminStatus(Integer32, TextualConvention):
    subtypeSpec = Integer32.subtypeSpec+ConstraintsUnion(SingleValueConstraint(1, 2,))
    namedValues = NamedValues(("up", 1), ("down", 2),)

class AtmVorXLastChange(TimeTicks, TextualConvention):
    pass

class AtmVorXOperStatus(Integer32, TextualConvention):
    subtypeSpec = Integer32.subtypeSpec+ConstraintsUnion(SingleValueConstraint(1, 2, 3,))
    namedValues = NamedValues(("up", 1), ("down", 2), ("unknown", 3),)

atmTrafficDescriptorTypes = MibIdentifier((1, 3, 6, 1, 2, 1, 37, 1, 1))
atmObjectIdentities = MibIdentifier((1, 3, 6, 1, 2, 1, 37, 3, 1))
atmNoTrafficDescriptor = ObjectIdentity((1, 3, 6, 1, 2, 1, 37, 1, 1, 1))
if mibBuilder.loadTexts: atmNoTrafficDescriptor.setDescription('This identifies the no ATM traffic\n            descriptor type.  Parameters 1, 2, 3, 4,\n            and 5 are not used.  This traffic descriptor\n            type can be used for best effort traffic.')
atmNoClpNoScr = ObjectIdentity((1, 3, 6, 1, 2, 1, 37, 1, 1, 2))
if mibBuilder.loadTexts: atmNoClpNoScr.setDescription('This traffic descriptor type is for no CLP\n            and no Sustained Cell Rate.  The use of the\n            parameter vector for this type:\n                Parameter 1: peak cell rate in cells/second\n                             for CLP=0+1 traffic\n                Parameter 2: not used\n                Parameter 3: not used\n                Parameter 4: not used\n                Parameter 5: not used.')
atmClpNoTaggingNoScr = ObjectIdentity((1, 3, 6, 1, 2, 1, 37, 1, 1, 3))
if mibBuilder.loadTexts: atmClpNoTaggingNoScr.setDescription('This traffic descriptor is for CLP without\n            tagging and no Sustained Cell Rate.  The use\n            of the parameter vector for this type:\n                Parameter 1: peak cell rate in cells/second\n                             for CLP=0+1 traffic\n                Parameter 2: peak cell rate in cells/second\n                             for CLP=0 traffic\n                Parameter 3: not used\n                Parameter 4: not used\n                Parameter 5: not used.')
atmClpTaggingNoScr = ObjectIdentity((1, 3, 6, 1, 2, 1, 37, 1, 1, 4))
if mibBuilder.loadTexts: atmClpTaggingNoScr.setDescription('This traffic descriptor is for CLP with\n            tagging and no Sustained Cell Rate.  The use\n            of the parameter vector for this type:\n                Parameter 1: peak cell rate in cells/second\n                             for CLP=0+1 traffic\n                Parameter 2: peak cell rate in cells/second\n                             for CLP=0 traffic, excess\n                             tagged as CLP=1\n                Parameter 3: not used\n                Parameter 4: not used\n                Parameter 5: not used.')
atmNoClpScr = ObjectIdentity((1, 3, 6, 1, 2, 1, 37, 1, 1, 5))
if mibBuilder.loadTexts: atmNoClpScr.setDescription('This traffic descriptor type is for no CLP\n            with Sustained Cell Rate.  The use of the\n            parameter vector for this type:\n                Parameter 1: peak cell rate in cells/second\n                             for CLP=0+1 traffic\n                Parameter 2: sustainable cell rate in cells/second\n                             for CLP=0+1 traffic\n                Parameter 3: maximum burst size in cells\n                Parameter 4: not used\n                Parameter 5: not used.')
atmClpNoTaggingScr = ObjectIdentity((1, 3, 6, 1, 2, 1, 37, 1, 1, 6))
if mibBuilder.loadTexts: atmClpNoTaggingScr.setDescription('This traffic descriptor type is for CLP with\n            Sustained Cell Rate and no tagging.  The use\n            of the parameter vector for this type:\n                Parameter 1: peak cell rate in cells/second\n                             for CLP=0+1 traffic\n                Parameter 2: sustainable cell rate in cells/second\n                             for CLP=0 traffic\n                Parameter 3: maximum burst size in cells\n                Parameter 4: not used\n                Parameter 5: not used.')
atmClpTaggingScr = ObjectIdentity((1, 3, 6, 1, 2, 1, 37, 1, 1, 7))
if mibBuilder.loadTexts: atmClpTaggingScr.setDescription('This traffic descriptor type is for CLP with\n            tagging and Sustained Cell Rate.  The use of\n            the parameter vector for this type:\n                Parameter 1: peak cell rate in cells/second\n                             for CLP=0+1 traffic\n                Parameter 2: sustainable cell rate in cells/second\n                             for CLP=0 traffic, excess tagged as\n                             CLP=1\n                Parameter 3: maximum burst size in cells\n                Parameter 4: not used\n                Parameter 5: not used.')
atmClpNoTaggingMcr = ObjectIdentity((1, 3, 6, 1, 2, 1, 37, 1, 1, 8))
if mibBuilder.loadTexts: atmClpNoTaggingMcr.setDescription('This traffic descriptor type is for CLP with\n            Minimum Cell Rate and no tagging.  The use of\n            the parameter vector for this type:\n                Parameter 1: peak cell rate in cells/second\n                             for CLP=0+1 traffic\n                Parameter 2: CDVT in tenths of microseconds\n                Parameter 3: minimum cell rate in cells/second\n                Parameter 4: unused\n                Parameter 5: unused.')
atmClpTransparentNoScr = ObjectIdentity((1, 3, 6, 1, 2, 1, 37, 1, 1, 9))
if mibBuilder.loadTexts: atmClpTransparentNoScr.setDescription('This traffic descriptor type is for the CLP-\n            transparent model and no Sustained Cell Rate.\n            The use of the parameter vector for this type:\n                Parameter 1: peak cell rate in cells/second\n                             for CLP=0+1 traffic\n                Parameter 2: CDVT in tenths of microseconds\n                Parameter 3: not used\n                Parameter 4: not used\n                Parameter 5: not used.\n            \n            This traffic descriptor type is applicable to\n            connections following the CBR.1 conformance\n            definition.\n            \n            Connections specifying this traffic descriptor\n            type will be rejected at UNI 3.0 or UNI 3.1\n            interfaces.  For a similar traffic descriptor\n            type that can be accepted at UNI 3.0 and\n            UNI 3.1 interfaces, see atmNoClpNoScr.')
atmClpTransparentScr = ObjectIdentity((1, 3, 6, 1, 2, 1, 37, 1, 1, 10))
if mibBuilder.loadTexts: atmClpTransparentScr.setDescription('This traffic descriptor type is for the CLP-\n            transparent model with Sustained Cell Rate.\n            The use of the parameter vector for this type:\n                Parameter 1: peak cell rate in cells/second\n                             for CLP=0+1 traffic\n                Parameter 2: sustainable cell rate in cells/second\n                             for CLP=0+1 traffic\n                Parameter 3: maximum burst size in cells\n                Parameter 4: CDVT in tenths of microseconds\n                Parameter 5: not used.\n            \n            This traffic descriptor type is applicable to\n            connections following the VBR.1 conformance\n            definition.\n            Connections specifying this traffic descriptor\n            type will be rejected at UNI 3.0 or UNI 3.1\n            interfaces.  For a similar traffic descriptor\n            type that can be accepted at UNI 3.0 and\n            UNI 3.1 interfaces, see atmNoClpScr.')
atmNoClpTaggingNoScr = ObjectIdentity((1, 3, 6, 1, 2, 1, 37, 1, 1, 11))
if mibBuilder.loadTexts: atmNoClpTaggingNoScr.setDescription('This traffic descriptor type is for no CLP\n            with tagging and no Sustained Cell Rate.  The\n            use of the parameter vector for this type:\n                Parameter 1: peak cell rate in cells/second\n                             for CLP=0+1 traffic\n                Parameter 2: CDVT in tenths of microseconds\n                Parameter 3: not used\n                Parameter 4: not used\n                Parameter 5: not used.\n            \n            This traffic descriptor type is applicable to\n            connections following the UBR.2 conformance\n            definition .')
atmNoClpNoScrCdvt = ObjectIdentity((1, 3, 6, 1, 2, 1, 37, 1, 1, 12))
if mibBuilder.loadTexts: atmNoClpNoScrCdvt.setDescription('This traffic descriptor type is for no CLP\n            and no Sustained Cell Rate.  The use of the\n            parameter vector for this type:\n                Parameter 1: peak cell rate in cells/second\n                             for CLP=0+1 traffic\n                Parameter 2: CDVT in tenths of microseconds\n                Parameter 3: not used\n                Parameter 4: not used\n                Parameter 5: not used.\n        \n            This traffic descriptor type is applicable to\n            CBR connections following the UNI 3.0/3.1\n            conformance definition for PCR CLP=0+1.\n            These CBR connections differ from CBR.1\n            connections in that the CLR objective\n            applies only to the CLP=0 cell flow.\n            \n            This traffic descriptor type is also\n            applicable to connections following the UBR.1\n            conformance definition.')
atmNoClpScrCdvt = ObjectIdentity((1, 3, 6, 1, 2, 1, 37, 1, 1, 13))
if mibBuilder.loadTexts: atmNoClpScrCdvt.setDescription('This traffic descriptor type is for no CLP\n            with Sustained Cell Rate.  The use of the\n            parameter vector for this type:\n                Parameter 1: peak cell rate in cells/second\n                             for CLP=0+1 traffic\n                Parameter 2: sustainable cell rate in cells/second\n                             for CLP=0+1 traffic\n                Parameter 3: maximum burst size in cells\n                Parameter 4: CDVT in tenths of microseconds\n                Parameter 5: not used.\n            \n            This traffic descriptor type is applicable\n            to VBR connections following the UNI 3.0/3.1\n            conformance definition for PCR CLP=0+1 and\n            SCR CLP=0+1.  These VBR connections\n            differ from VBR.1 connections in that\n            the CLR objective applies only to the CLP=0\n            cell flow.')
atmClpNoTaggingScrCdvt = ObjectIdentity((1, 3, 6, 1, 2, 1, 37, 1, 1, 14))
if mibBuilder.loadTexts: atmClpNoTaggingScrCdvt.setDescription('This traffic descriptor type is for CLP with\n            Sustained Cell Rate and no tagging.  The use\n            of the parameter vector for this type:\n                Parameter 1: peak cell rate in cells/second\n                             for CLP=0+1 traffic\n                Parameter 2: sustainable cell rate in cells/second\n                             for CLP=0 traffic\n                Parameter 3: maximum burst size in cells\n                Parameter 4: CDVT in tenths of microseconds\n                Parameter 5: not used.\n            \n            This traffic descriptor type is applicable to\n            connections following the VBR.2 conformance\n            definition.')
atmClpTaggingScrCdvt = ObjectIdentity((1, 3, 6, 1, 2, 1, 37, 1, 1, 15))
if mibBuilder.loadTexts: atmClpTaggingScrCdvt.setDescription('This traffic descriptor type is for CLP with\n            tagging and Sustained Cell Rate.  The use of\n            the parameter vector for this type:\n                Parameter 1: peak cell rate in cells/second\n                             for CLP=0+1 traffic\n                Parameter 2: sustainable cell rate in cells/second\n                             for CLP=0 traffic, excess tagged as\n                             CLP=1\n                Parameter 3: maximum burst size in cells\n                Parameter 4: CDVT in tenths of microseconds\n                Parameter 5: not used.\n            \n            This traffic descriptor type is applicable to\n            connections following the VBR.3 conformance\n            definition.')
mibBuilder.exportSymbols("ATM-TC-MIB", atmNoClpNoScr=atmNoClpNoScr, atmTrafficDescriptorTypes=atmTrafficDescriptorTypes, atmObjectIdentities=atmObjectIdentities, AtmVorXAdminStatus=AtmVorXAdminStatus, atmNoClpScr=atmNoClpScr, PYSNMP_MODULE_ID=atmTCMIB, AtmAddr=AtmAddr, atmClpNoTaggingNoScr=atmClpNoTaggingNoScr, AtmIlmiNetworkPrefix=AtmIlmiNetworkPrefix, atmClpTaggingNoScr=atmClpTaggingNoScr, atmClpNoTaggingMcr=atmClpNoTaggingMcr, atmNoClpTaggingNoScr=atmNoClpTaggingNoScr, atmClpTaggingScrCdvt=atmClpTaggingScrCdvt, AtmVcIdentifier=AtmVcIdentifier, atmNoClpScrCdvt=atmNoClpScrCdvt, atmTCMIB=atmTCMIB, atmClpNoTaggingScrCdvt=atmClpNoTaggingScrCdvt, atmClpTransparentScr=atmClpTransparentScr, AtmSigDescrParamIndex=AtmSigDescrParamIndex, AtmServiceCategory=AtmServiceCategory, AtmConnCastType=AtmConnCastType, AtmTrafficDescrParamIndex=AtmTrafficDescrParamIndex, AtmVorXLastChange=AtmVorXLastChange, atmClpNoTaggingScr=atmClpNoTaggingScr, AtmVorXOperStatus=AtmVorXOperStatus, AtmVpIdentifier=AtmVpIdentifier, atmNoTrafficDescriptor=atmNoTrafficDescriptor, atmNoClpNoScrCdvt=atmNoClpNoScrCdvt, atmClpTransparentNoScr=atmClpTransparentNoScr, AtmConnKind=AtmConnKind, atmClpTaggingScr=atmClpTaggingScr, AtmInterfaceType=AtmInterfaceType)
