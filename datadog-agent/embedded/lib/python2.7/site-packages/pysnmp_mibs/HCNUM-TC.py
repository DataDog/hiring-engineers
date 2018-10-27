#
# PySNMP MIB module HCNUM-TC (http://pysnmp.sf.net)
# ASN.1 source http://mibs.snmplabs.com:80/asn1/HCNUM-TC
# Produced by pysmi-0.0.7 at Sun Feb 14 00:10:39 2016
# On host bldfarm platform Linux version 4.1.13-100.fc21.x86_64 by user goose
# Using Python version 3.5.0 (default, Jan  5 2016, 17:11:52) 
#
( Integer, OctetString, ObjectIdentifier, ) = mibBuilder.importSymbols("ASN1", "Integer", "OctetString", "ObjectIdentifier")
( NamedValues, ) = mibBuilder.importSymbols("ASN1-ENUMERATION", "NamedValues")
( ConstraintsUnion, ValueRangeConstraint, ConstraintsIntersection, SingleValueConstraint, ValueSizeConstraint, ) = mibBuilder.importSymbols("ASN1-REFINEMENT", "ConstraintsUnion", "ValueRangeConstraint", "ConstraintsIntersection", "SingleValueConstraint", "ValueSizeConstraint")
( NotificationGroup, ModuleCompliance, ) = mibBuilder.importSymbols("SNMPv2-CONF", "NotificationGroup", "ModuleCompliance")
( Gauge32, Counter64, MibScalar, MibTable, MibTableRow, MibTableColumn, MibIdentifier, TimeTicks, ModuleIdentity, Unsigned32, IpAddress, iso, NotificationType, Bits, mib_2, ObjectIdentity, Integer32, Counter32, ) = mibBuilder.importSymbols("SNMPv2-SMI", "Gauge32", "Counter64", "MibScalar", "MibTable", "MibTableRow", "MibTableColumn", "MibIdentifier", "TimeTicks", "ModuleIdentity", "Unsigned32", "IpAddress", "iso", "NotificationType", "Bits", "mib-2", "ObjectIdentity", "Integer32", "Counter32")
( TextualConvention, DisplayString, ) = mibBuilder.importSymbols("SNMPv2-TC", "TextualConvention", "DisplayString")
hcnumTC = ModuleIdentity((1, 3, 6, 1, 2, 1, 78)).setRevisions(("2000-06-08 00:00",))
if mibBuilder.loadTexts: hcnumTC.setLastUpdated('200006080000Z')
if mibBuilder.loadTexts: hcnumTC.setOrganization('IETF OPS Area')
if mibBuilder.loadTexts: hcnumTC.setContactInfo('        E-mail: mibs@ops.ietf.org\n                    Subscribe: majordomo@psg.com\n                      with msg body: subscribe mibs\n\n                    Andy Bierman\n                    Cisco Systems Inc.\n                    170 West Tasman Drive\n                    San Jose, CA 95134 USA\n                    +1 408-527-3711\n                    abierman@cisco.com\n\n                    Keith McCloghrie\n                    Cisco Systems Inc.\n                    170 West Tasman Drive\n                    San Jose, CA 95134 USA\n                    +1 408-526-5260\n                    kzm@cisco.com\n\n                    Randy Presuhn\n                    BMC Software, Inc.\n                    Office 1-3141\n                    2141 North First Street\n                    San Jose,  California 95131 USA\n                    +1 408 546-1006\n                    rpresuhn@bmc.com')
if mibBuilder.loadTexts: hcnumTC.setDescription('A MIB module containing textual conventions\n            for high capacity data types. This module\n            addresses an immediate need for data types not directly\n            supported in the SMIv2. This short-term solution\n            is meant to be deprecated as a long-term solution\n            is deployed.')
class CounterBasedGauge64(Counter64, TextualConvention):
    pass

class ZeroBasedCounter64(Counter64, TextualConvention):
    pass

mibBuilder.exportSymbols("HCNUM-TC", ZeroBasedCounter64=ZeroBasedCounter64, CounterBasedGauge64=CounterBasedGauge64, PYSNMP_MODULE_ID=hcnumTC, hcnumTC=hcnumTC)
