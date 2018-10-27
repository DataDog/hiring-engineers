#
# PySNMP MIB module IANA-FINISHER-MIB (http://pysnmp.sf.net)
# ASN.1 source http://mibs.snmplabs.com:80/asn1/IANA-FINISHER-MIB
# Produced by pysmi-0.0.7 at Sun Feb 14 00:15:44 2016
# On host bldfarm platform Linux version 4.1.13-100.fc21.x86_64 by user goose
# Using Python version 3.5.0 (default, Jan  5 2016, 17:11:52) 
#
( ObjectIdentifier, OctetString, Integer, ) = mibBuilder.importSymbols("ASN1", "ObjectIdentifier", "OctetString", "Integer")
( NamedValues, ) = mibBuilder.importSymbols("ASN1-ENUMERATION", "NamedValues")
( ConstraintsUnion, ValueRangeConstraint, ValueSizeConstraint, ConstraintsIntersection, SingleValueConstraint, ) = mibBuilder.importSymbols("ASN1-REFINEMENT", "ConstraintsUnion", "ValueRangeConstraint", "ValueSizeConstraint", "ConstraintsIntersection", "SingleValueConstraint")
( ModuleCompliance, NotificationGroup, ) = mibBuilder.importSymbols("SNMPv2-CONF", "ModuleCompliance", "NotificationGroup")
( Integer32, Gauge32, MibScalar, MibTable, MibTableRow, MibTableColumn, Counter64, ObjectIdentity, Unsigned32, ModuleIdentity, NotificationType, MibIdentifier, IpAddress, Bits, iso, mib_2, Counter32, TimeTicks, ) = mibBuilder.importSymbols("SNMPv2-SMI", "Integer32", "Gauge32", "MibScalar", "MibTable", "MibTableRow", "MibTableColumn", "Counter64", "ObjectIdentity", "Unsigned32", "ModuleIdentity", "NotificationType", "MibIdentifier", "IpAddress", "Bits", "iso", "mib-2", "Counter32", "TimeTicks")
( TextualConvention, DisplayString, ) = mibBuilder.importSymbols("SNMPv2-TC", "TextualConvention", "DisplayString")
ianafinisherMIB = ModuleIdentity((1, 3, 6, 1, 2, 1, 110)).setRevisions(("2004-06-02 00:00",))
if mibBuilder.loadTexts: ianafinisherMIB.setLastUpdated('200406020000Z')
if mibBuilder.loadTexts: ianafinisherMIB.setOrganization('IANA')
if mibBuilder.loadTexts: ianafinisherMIB.setContactInfo('Internet Assigned Numbers Authority\n\n                  Postal: ICANN\n                          4676 Admiralty Way, Suite 330\n                          Marina del Rey, CA 90292\n\n                  Tel:    +1 310 823 9358\n                  E-Mail: iana@iana.org')
if mibBuilder.loadTexts: ianafinisherMIB.setDescription('This MIB module defines a set of finishing-related\n                  TEXTUAL-CONVENTIONs for use in Finisher MIB (RFC 3806)\n                  and other MIBs which need to specify finishing\n                  mechanism details.\n\n                  Any additions or changes to the contents of this MIB\n                  module require either publication of an RFC, or\n                  Designated Expert Review as defined in RFC 2434,\n                  Guidelines for Writing an IANA Considerations Section\n                  in RFCs.  The Designated Expert will be selected by\n                  the IESG Area Director(s) of the Applications Area.\n\n                  Copyright (C) The Internet Society (2004). The\n\n                  initial version of this MIB module was published\n                  in RFC 3806. For full legal notices see the RFC\n                  itself or see:\n                  http://www.ietf.org/copyrights/ianamib.html')
class FinDeviceTypeTC(Integer32, TextualConvention):
    subtypeSpec = Integer32.subtypeSpec+ConstraintsUnion(SingleValueConstraint(1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18,))
    namedValues = NamedValues(("other", 1), ("unknown", 2), ("stitcher", 3), ("folder", 4), ("binder", 5), ("trimmer", 6), ("dieCutter", 7), ("puncher", 8), ("perforater", 9), ("slitter", 10), ("separationCutter", 11), ("imprinter", 12), ("wrapper", 13), ("bander", 14), ("makeEnvelope", 15), ("stacker", 16), ("sheetRotator", 17), ("inserter", 18),)

class FinAttributeTypeTC(Integer32, TextualConvention):
    subtypeSpec = Integer32.subtypeSpec+ConstraintsUnion(SingleValueConstraint(1, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 30, 31, 40, 50, 80, 81, 82, 83, 100, 130, 160, 161, 162,))
    namedValues = NamedValues(("other", 1), ("deviceName", 3), ("deviceVendorName", 4), ("deviceModel", 5), ("deviceVersion", 6), ("deviceSerialNumber", 7), ("maximumSheets", 8), ("finProcessOffsetUnits", 9), ("finReferenceEdge", 10), ("finAxisOffset", 11), ("finJogEdge", 12), ("finHeadLocation", 13), ("finOperationRestrictions", 14), ("finNumberOfPositions", 15), ("namedConfiguration", 16), ("finMediaTypeRestriction", 17), ("finPrinterInputTraySupported", 18), ("finPreviousFinishingOperation", 19), ("finNextFinishingOperation", 20), ("stitchingType", 30), ("stitchingDirection", 31), ("foldingType", 40), ("bindingType", 50), ("punchHoleType", 80), ("punchHoleSizeLongDim", 81), ("punchHoleSizeShortDim", 82), ("punchPattern", 83), ("slittingType", 100), ("wrappingType", 130), ("stackOutputType", 160), ("stackOffset", 161), ("stackRotation", 162),)

class FinEdgeTC(Integer32, TextualConvention):
    subtypeSpec = Integer32.subtypeSpec+ConstraintsUnion(SingleValueConstraint(3, 4, 5, 6,))
    namedValues = NamedValues(("topEdge", 3), ("bottomEdge", 4), ("leftEdge", 5), ("rightEdge", 6),)

class FinStitchingTypeTC(Integer32, TextualConvention):
    subtypeSpec = Integer32.subtypeSpec+ConstraintsUnion(SingleValueConstraint(1, 2, 4, 5, 6, 7, 8, 9, 10,))
    namedValues = NamedValues(("other", 1), ("unknown", 2), ("stapleTopLeft", 4), ("stapleBottomLeft", 5), ("stapleTopRight", 6), ("stapleBottomRight", 7), ("saddleStitch", 8), ("edgeStitch", 9), ("stapleDual", 10),)

class FinStitchingDirTypeTC(Integer32, TextualConvention):
    subtypeSpec = Integer32.subtypeSpec+ConstraintsUnion(SingleValueConstraint(2, 3, 4,))
    namedValues = NamedValues(("unknown", 2), ("topDown", 3), ("bottomUp", 4),)

class FinStitchingAngleTypeTC(Integer32, TextualConvention):
    subtypeSpec = Integer32.subtypeSpec+ConstraintsUnion(SingleValueConstraint(2, 3, 4, 5,))
    namedValues = NamedValues(("unknown", 2), ("horizontal", 3), ("vertical", 4), ("slanted", 5),)

class FinFoldingTypeTC(Integer32, TextualConvention):
    subtypeSpec = Integer32.subtypeSpec+ConstraintsUnion(SingleValueConstraint(1, 2, 3, 4, 5,))
    namedValues = NamedValues(("other", 1), ("unknown", 2), ("zFold", 3), ("halfFold", 4), ("letterFold", 5),)

class FinBindingTypeTC(Integer32, TextualConvention):
    subtypeSpec = Integer32.subtypeSpec+ConstraintsUnion(SingleValueConstraint(1, 2, 4, 5, 6, 7, 8, 9, 10, 11,))
    namedValues = NamedValues(("other", 1), ("unknown", 2), ("tape", 4), ("plastic", 5), ("velo", 6), ("perfect", 7), ("spiral", 8), ("adhesive", 9), ("comb", 10), ("padding", 11),)

class FinPunchHoleTypeTC(Integer32, TextualConvention):
    subtypeSpec = Integer32.subtypeSpec+ConstraintsUnion(SingleValueConstraint(1, 2, 3, 4, 5, 6, 7,))
    namedValues = NamedValues(("other", 1), ("unknown", 2), ("round", 3), ("oblong", 4), ("square", 5), ("rectangular", 6), ("star", 7),)

class FinPunchPatternTC(Integer32, TextualConvention):
    subtypeSpec = Integer32.subtypeSpec+ConstraintsUnion(SingleValueConstraint(1, 2, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18,))
    namedValues = NamedValues(("other", 1), ("unknown", 2), ("twoHoleUSTop", 4), ("threeHoleUS", 5), ("twoHoleDIN", 6), ("fourHoleDIN", 7), ("twentyTwoHoleUS", 8), ("nineteenHoleUS", 9), ("twoHoleMetric", 10), ("swedish4Hole", 11), ("twoHoleUSSide", 12), ("fiveHoleUS", 13), ("sevenHoleUS", 14), ("mixed7H4S", 15), ("norweg6Hole", 16), ("metric26Hole", 17), ("metric30Hole", 18),)

class FinSlittingTypeTC(Integer32, TextualConvention):
    subtypeSpec = Integer32.subtypeSpec+ConstraintsUnion(SingleValueConstraint(1, 2, 4, 5,))
    namedValues = NamedValues(("other", 1), ("unknown", 2), ("slitAndSeparate", 4), ("slitAndMerge", 5),)

class FinWrappingTypeTC(Integer32, TextualConvention):
    subtypeSpec = Integer32.subtypeSpec+ConstraintsUnion(SingleValueConstraint(1, 2, 4, 5,))
    namedValues = NamedValues(("other", 1), ("unknown", 2), ("shrinkWrap", 4), ("paperWrap", 5),)

class FinStackOutputTypeTC(Integer32, TextualConvention):
    subtypeSpec = Integer32.subtypeSpec+ConstraintsUnion(SingleValueConstraint(1, 2, 4, 5, 6,))
    namedValues = NamedValues(("other", 1), ("unknown", 2), ("straight", 4), ("offset", 5), ("crissCross", 6),)

mibBuilder.exportSymbols("IANA-FINISHER-MIB", FinFoldingTypeTC=FinFoldingTypeTC, FinStitchingAngleTypeTC=FinStitchingAngleTypeTC, FinPunchPatternTC=FinPunchPatternTC, FinAttributeTypeTC=FinAttributeTypeTC, FinStackOutputTypeTC=FinStackOutputTypeTC, FinSlittingTypeTC=FinSlittingTypeTC, FinBindingTypeTC=FinBindingTypeTC, FinStitchingDirTypeTC=FinStitchingDirTypeTC, ianafinisherMIB=ianafinisherMIB, FinPunchHoleTypeTC=FinPunchHoleTypeTC, FinEdgeTC=FinEdgeTC, PYSNMP_MODULE_ID=ianafinisherMIB, FinWrappingTypeTC=FinWrappingTypeTC, FinDeviceTypeTC=FinDeviceTypeTC, FinStitchingTypeTC=FinStitchingTypeTC)
