#
# PySNMP MIB module ADSL2-LINE-TC-MIB (http://pysnmp.sf.net)
# ASN.1 source http://mibs.snmplabs.com:80/asn1/ADSL2-LINE-TC-MIB
# Produced by pysmi-0.0.7 at Sun Feb 14 00:03:54 2016
# On host bldfarm platform Linux version 4.1.13-100.fc21.x86_64 by user goose
# Using Python version 3.5.0 (default, Jan  5 2016, 17:11:52) 
#
( ObjectIdentifier, OctetString, Integer, ) = mibBuilder.importSymbols("ASN1", "ObjectIdentifier", "OctetString", "Integer")
( NamedValues, ) = mibBuilder.importSymbols("ASN1-ENUMERATION", "NamedValues")
( SingleValueConstraint, ValueRangeConstraint, ValueSizeConstraint, ConstraintsIntersection, ConstraintsUnion, ) = mibBuilder.importSymbols("ASN1-REFINEMENT", "SingleValueConstraint", "ValueRangeConstraint", "ValueSizeConstraint", "ConstraintsIntersection", "ConstraintsUnion")
( NotificationGroup, ModuleCompliance, ) = mibBuilder.importSymbols("SNMPv2-CONF", "NotificationGroup", "ModuleCompliance")
( Gauge32, transmission, TimeTicks, ObjectIdentity, ModuleIdentity, Bits, Counter32, IpAddress, MibIdentifier, Integer32, Counter64, Unsigned32, NotificationType, MibScalar, MibTable, MibTableRow, MibTableColumn, iso, ) = mibBuilder.importSymbols("SNMPv2-SMI", "Gauge32", "transmission", "TimeTicks", "ObjectIdentity", "ModuleIdentity", "Bits", "Counter32", "IpAddress", "MibIdentifier", "Integer32", "Counter64", "Unsigned32", "NotificationType", "MibScalar", "MibTable", "MibTableRow", "MibTableColumn", "iso")
( TextualConvention, DisplayString, ) = mibBuilder.importSymbols("SNMPv2-TC", "TextualConvention", "DisplayString")
adsl2TCMIB = ModuleIdentity((1, 3, 6, 1, 2, 1, 10, 238, 2)).setRevisions(("2006-10-04 00:00",))
if mibBuilder.loadTexts: adsl2TCMIB.setLastUpdated('200610040000Z')
if mibBuilder.loadTexts: adsl2TCMIB.setOrganization('ADSLMIB Working Group')
if mibBuilder.loadTexts: adsl2TCMIB.setContactInfo('WG-email:  adslmib@ietf.org\n   Info:      https://www1.ietf.org/mailman/listinfo/adslmib\n\n             Chair:     Mike Sneed\n                        Sand Channel Systems\n             Postal:    P.O. Box 37324\n                        Raleigh NC 27627-732\n             Email:     sneedmike@hotmail.com\n             Phone:     +1 206 600 7022\n\n             Co-Chair & Co-editor:\n                        Menachem Dodge\n                        ECI Telecom Ltd.\n             Postal:    30 Hasivim St.\n                        Petach Tikva 49517,\n                        Israel.\n             Email:     mbdodge@ieee.org\n             Phone:     +972 3 926 8421\n\n\n\n\n\n\n             Co-editor: Moti Morgenstern\n                        ECI Telecom Ltd.\n             Postal:    30 Hasivim St.\n                        Petach Tikva 49517,\n                        Israel.\n             Email:     moti.morgenstern@ecitele.com\n             Phone:     +972 3 926 6258\n\n             Co-editor: Scott Baillie\n                        NEC Australia\n             Postal:    649-655 Springvale Road,\n                        Mulgrave, Victoria 3170,\n                        Australia.\n             Email:     scott.baillie@nec.com.au\n             Phone:     +61 3 9264 3986\n\n             Co-editor: Umberto Bonollo\n                        NEC Australia\n             Postal:    649-655 Springvale Road,\n                        Mulgrave, Victoria 3170,\n                        Australia.\n             Email:     umberto.bonollo@nec.com.au\n             Phone:     +61 3 9264 3385\n            ')
if mibBuilder.loadTexts: adsl2TCMIB.setDescription('This MIB Module provides Textual Conventions to be\n         used by the ADSL2-LINE-MIB module for the purpose of\n         managing ADSL, ADSL2, and ADSL2+ lines.\n\n        Copyright (C) The Internet Society (2006).  This version of\n        this MIB module is part of RFC 4706: see the RFC itself for\n        full legal notices.')
class Adsl2Unit(Integer32, TextualConvention):
    subtypeSpec = Integer32.subtypeSpec+ConstraintsUnion(SingleValueConstraint(1, 2,))
    namedValues = NamedValues(("atuc", 1), ("atur", 2),)

class Adsl2Direction(Integer32, TextualConvention):
    subtypeSpec = Integer32.subtypeSpec+ConstraintsUnion(SingleValueConstraint(1, 2,))
    namedValues = NamedValues(("upstream", 1), ("downstream", 2),)

class Adsl2TransmissionModeType(Bits, TextualConvention):
    namedValues = NamedValues(("ansit1413", 0), ("etsi", 1), ("g9921PotsNonOverlapped", 2), ("g9921PotsOverlapped", 3), ("g9921IsdnNonOverlapped", 4), ("g9921isdnOverlapped", 5), ("g9921tcmIsdnNonOverlapped", 6), ("g9921tcmIsdnOverlapped", 7), ("g9922potsNonOverlapped", 8), ("g9922potsOverlapped", 9), ("g9922tcmIsdnNonOverlapped", 10), ("g9922tcmIsdnOverlapped", 11), ("g9921tcmIsdnSymmetric", 12), ("reserved1", 13), ("reserved2", 14), ("reserved3", 15), ("reserved4", 16), ("reserved5", 17), ("g9923PotsNonOverlapped", 18), ("g9923PotsOverlapped", 19), ("g9923IsdnNonOverlapped", 20), ("g9923isdnOverlapped", 21), ("reserved6", 22), ("reserved7", 23), ("g9924potsNonOverlapped", 24), ("g9924potsOverlapped", 25), ("reserved8", 26), ("reserved9", 27), ("g9923AnnexIAllDigNonOverlapped", 28), ("g9923AnnexIAllDigOverlapped", 29), ("g9923AnnexJAllDigNonOverlapped", 30), ("g9923AnnexJAllDigOverlapped", 31), ("g9924AnnexIAllDigNonOverlapped", 32), ("g9924AnnexIAllDigOverlapped", 33), ("g9923AnnexLMode1NonOverlapped", 34), ("g9923AnnexLMode2NonOverlapped", 35), ("g9923AnnexLMode3Overlapped", 36), ("g9923AnnexLMode4Overlapped", 37), ("g9923AnnexMPotsNonOverlapped", 38), ("g9923AnnexMPotsOverlapped", 39), ("g9925PotsNonOverlapped", 40), ("g9925PotsOverlapped", 41), ("g9925IsdnNonOverlapped", 42), ("g9925isdnOverlapped", 43), ("reserved10", 44), ("reserved11", 45), ("g9925AnnexIAllDigNonOverlapped", 46), ("g9925AnnexIAllDigOverlapped", 47), ("g9925AnnexJAllDigNonOverlapped", 48), ("g9925AnnexJAllDigOverlapped", 49), ("g9925AnnexMPotsNonOverlapped", 50), ("g9925AnnexMPotsOverlapped", 51), ("reserved12", 52), ("reserved13", 53), ("reserved14", 54), ("reserved15", 55),)

class Adsl2RaMode(Integer32, TextualConvention):
    subtypeSpec = Integer32.subtypeSpec+ConstraintsUnion(SingleValueConstraint(1, 2, 3,))
    namedValues = NamedValues(("manual", 1), ("raInit", 2), ("dynamicRa", 3),)

class Adsl2InitResult(Integer32, TextualConvention):
    subtypeSpec = Integer32.subtypeSpec+ConstraintsUnion(SingleValueConstraint(0, 1, 2, 3, 4, 5,))
    namedValues = NamedValues(("noFail", 0), ("configError", 1), ("configNotFeasible", 2), ("commFail", 3), ("noPeerAtu", 4), ("otherCause", 5),)

class Adsl2OperationModes(Integer32, TextualConvention):
    subtypeSpec = Integer32.subtypeSpec+ConstraintsUnion(SingleValueConstraint(1, 2, 8, 9, 10, 11, 14, 15, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 36, 37, 38, 39, 40, 41,))
    namedValues = NamedValues(("defMode", 1), ("adsl", 2), ("g9923PotsNonOverlapped", 8), ("g9923PotsOverlapped", 9), ("g9923IsdnNonOverlapped", 10), ("g9923isdnOverlapped", 11), ("g9924potsNonOverlapped", 14), ("g9924potsOverlapped", 15), ("g9923AnnexIAllDigNonOverlapped", 18), ("g9923AnnexIAllDigOverlapped", 19), ("g9923AnnexJAllDigNonOverlapped", 20), ("g9923AnnexJAllDigOverlapped", 21), ("g9924AnnexIAllDigNonOverlapped", 22), ("g9924AnnexIAllDigOverlapped", 23), ("g9923AnnexLMode1NonOverlapped", 24), ("g9923AnnexLMode2NonOverlapped", 25), ("g9923AnnexLMode3Overlapped", 26), ("g9923AnnexLMode4Overlapped", 27), ("g9923AnnexMPotsNonOverlapped", 28), ("g9923AnnexMPotsOverlapped", 29), ("g9925PotsNonOverlapped", 30), ("g9925PotsOverlapped", 31), ("g9925IsdnNonOverlapped", 32), ("g9925isdnOverlapped", 33), ("g9925AnnexIAllDigNonOverlapped", 36), ("g9925AnnexIAllDigOverlapped", 37), ("g9925AnnexJAllDigNonOverlapped", 38), ("g9925AnnexJAllDigOverlapped", 39), ("g9925AnnexMPotsNonOverlapped", 40), ("g9925AnnexMPotsOverlapped", 41),)

class Adsl2PowerMngState(Integer32, TextualConvention):
    subtypeSpec = Integer32.subtypeSpec+ConstraintsUnion(SingleValueConstraint(1, 2, 3, 4,))
    namedValues = NamedValues(("l0", 1), ("l1", 2), ("l2", 3), ("l3", 4),)

class Adsl2ConfPmsForce(Integer32, TextualConvention):
    subtypeSpec = Integer32.subtypeSpec+ConstraintsUnion(SingleValueConstraint(0, 2, 3,))
    namedValues = NamedValues(("l3toL0", 0), ("l0toL2", 2), ("l0orL2toL3", 3),)

class Adsl2LConfProfPmMode(Bits, TextualConvention):
    namedValues = NamedValues(("allowTransitionsToIdle", 0), ("allowTransitionsToLowPower", 1),)

class Adsl2LineLdsf(Integer32, TextualConvention):
    subtypeSpec = Integer32.subtypeSpec+ConstraintsUnion(SingleValueConstraint(0, 1,))
    namedValues = NamedValues(("inhibit", 0), ("force", 1),)

class Adsl2LdsfResult(Integer32, TextualConvention):
    subtypeSpec = Integer32.subtypeSpec+ConstraintsUnion(SingleValueConstraint(1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11,))
    namedValues = NamedValues(("none", 1), ("success", 2), ("inProgress", 3), ("unsupported", 4), ("cannotRun", 5), ("aborted", 6), ("failed", 7), ("illegalMode", 8), ("adminUp", 9), ("tableFull", 10), ("noResources", 11),)

class Adsl2SymbolProtection(Integer32, TextualConvention):
    subtypeSpec = Integer32.subtypeSpec+ConstraintsUnion(SingleValueConstraint(1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18,))
    namedValues = NamedValues(("noProtection", 1), ("halfSymbol", 2), ("singleSymbol", 3), ("twoSymbols", 4), ("threeSymbols", 5), ("fourSymbols", 6), ("fiveSymbols", 7), ("sixSymbols", 8), ("sevenSymbols", 9), ("eightSymbols", 10), ("nineSymbols", 11), ("tenSymbols", 12), ("elevenSymbols", 13), ("twelveSymbols", 14), ("thirteeSymbols", 15), ("fourteenSymbols", 16), ("fifteenSymbols", 17), ("sixteenSymbols", 18),)

class Adsl2MaxBer(Integer32, TextualConvention):
    subtypeSpec = Integer32.subtypeSpec+ConstraintsUnion(SingleValueConstraint(1, 2, 3,))
    namedValues = NamedValues(("eminus3", 1), ("eminus5", 2), ("eminus7", 3),)

class Adsl2ScMaskDs(OctetString, TextualConvention):
    subtypeSpec = OctetString.subtypeSpec+ValueSizeConstraint(0,64)

class Adsl2ScMaskUs(OctetString, TextualConvention):
    subtypeSpec = OctetString.subtypeSpec+ValueSizeConstraint(0,8)

class Adsl2RfiDs(OctetString, TextualConvention):
    subtypeSpec = OctetString.subtypeSpec+ValueSizeConstraint(0,64)

class Adsl2PsdMaskDs(OctetString, TextualConvention):
    subtypeSpec = OctetString.subtypeSpec+ValueSizeConstraint(0,96)

class Adsl2PsdMaskUs(OctetString, TextualConvention):
    subtypeSpec = OctetString.subtypeSpec+ValueSizeConstraint(0,12)

class Adsl2Tssi(OctetString, TextualConvention):
    subtypeSpec = OctetString.subtypeSpec+ValueSizeConstraint(0,96)

class Adsl2LastTransmittedState(Integer32, TextualConvention):
    subtypeSpec = Integer32.subtypeSpec+ConstraintsUnion(SingleValueConstraint(0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131,))
    namedValues = NamedValues(("atucG9941", 0), ("atucQuiet1", 1), ("atucComb1", 2), ("atucQuiet2", 3), ("atucComb2", 4), ("atucIcomb1", 5), ("atucLineprob", 6), ("atucQuiet3", 7), ("atucComb3", 8), ("atucIComb2", 9), ("atucMsgfmt", 10), ("atucMsgpcb", 11), ("atucQuiet4", 12), ("atucReverb1", 13), ("atucTref1", 14), ("atucReverb2", 15), ("atucEct", 16), ("atucReverb3", 17), ("atucTref2", 18), ("atucReverb4", 19), ("atucSegue1", 20), ("atucMsg1", 21), ("atucReverb5", 22), ("atucSegue2", 23), ("atucMedley", 24), ("atucExchmarker", 25), ("atucMsg2", 26), ("atucReverb6", 27), ("atucSegue3", 28), ("atucParams", 29), ("atucReverb7", 30), ("atucSegue4", 31), ("atucShowtime", 32), ("aturG9941", 100), ("aturQuiet1", 101), ("aturComb1", 102), ("aturQuiet2", 103), ("aturComb2", 104), ("aturIcomb1", 105), ("aturLineprob", 106), ("aturQuiet3", 107), ("aturComb3", 108), ("aturIcomb2", 109), ("aturMsgfmt", 110), ("aturMsgpcb", 111), ("aturReverb1", 112), ("aturQuiet4", 113), ("aturReverb2", 114), ("aturQuiet5", 115), ("aturReverb3", 116), ("aturEct", 117), ("aturReverb4", 118), ("aturSegue1", 119), ("aturReverb5", 120), ("aturSegue2", 121), ("aturMsg1", 122), ("aturMedley", 123), ("aturExchmarker", 124), ("aturMsg2", 125), ("aturReverb6", 126), ("aturSegue3", 127), ("aturParams", 128), ("aturReverb7", 129), ("aturSegue4", 130), ("aturShowtime", 131),)

class Adsl2LineStatus(Bits, TextualConvention):
    namedValues = NamedValues(("noDefect", 0), ("lossOfFrame", 1), ("lossOfSignal", 2), ("lossOfPower", 3), ("initFailure", 4),)

class Adsl2ChAtmStatus(Bits, TextualConvention):
    namedValues = NamedValues(("noDefect", 0), ("noCellDelineation", 1), ("lossOfCellDelineation", 2),)

class Adsl2ChPtmStatus(Bits, TextualConvention):
    namedValues = NamedValues(("noDefect", 0), ("outOfSync", 1),)

mibBuilder.exportSymbols("ADSL2-LINE-TC-MIB", Adsl2LineStatus=Adsl2LineStatus, Adsl2Tssi=Adsl2Tssi, Adsl2ScMaskUs=Adsl2ScMaskUs, PYSNMP_MODULE_ID=adsl2TCMIB, Adsl2Direction=Adsl2Direction, Adsl2ConfPmsForce=Adsl2ConfPmsForce, Adsl2OperationModes=Adsl2OperationModes, Adsl2ScMaskDs=Adsl2ScMaskDs, Adsl2ChAtmStatus=Adsl2ChAtmStatus, Adsl2ChPtmStatus=Adsl2ChPtmStatus, Adsl2PsdMaskDs=Adsl2PsdMaskDs, Adsl2Unit=Adsl2Unit, Adsl2MaxBer=Adsl2MaxBer, Adsl2PsdMaskUs=Adsl2PsdMaskUs, Adsl2LineLdsf=Adsl2LineLdsf, Adsl2RfiDs=Adsl2RfiDs, Adsl2LdsfResult=Adsl2LdsfResult, Adsl2SymbolProtection=Adsl2SymbolProtection, Adsl2InitResult=Adsl2InitResult, Adsl2LastTransmittedState=Adsl2LastTransmittedState, adsl2TCMIB=adsl2TCMIB, Adsl2PowerMngState=Adsl2PowerMngState, Adsl2RaMode=Adsl2RaMode, Adsl2LConfProfPmMode=Adsl2LConfProfPmMode, Adsl2TransmissionModeType=Adsl2TransmissionModeType)
