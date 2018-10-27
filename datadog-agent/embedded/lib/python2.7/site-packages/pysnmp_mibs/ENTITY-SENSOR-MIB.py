#
# PySNMP MIB module ENTITY-SENSOR-MIB (http://pysnmp.sf.net)
# ASN.1 source http://mibs.snmplabs.com:80/asn1/ENTITY-SENSOR-MIB
# Produced by pysmi-0.0.7 at Sun Feb 14 00:11:46 2016
# On host bldfarm platform Linux version 4.1.13-100.fc21.x86_64 by user goose
# Using Python version 3.5.0 (default, Jan  5 2016, 17:11:52) 
#
( ObjectIdentifier, OctetString, Integer, ) = mibBuilder.importSymbols("ASN1", "ObjectIdentifier", "OctetString", "Integer")
( NamedValues, ) = mibBuilder.importSymbols("ASN1-ENUMERATION", "NamedValues")
( ValueSizeConstraint, ConstraintsUnion, SingleValueConstraint, ValueRangeConstraint, ConstraintsIntersection, ) = mibBuilder.importSymbols("ASN1-REFINEMENT", "ValueSizeConstraint", "ConstraintsUnion", "SingleValueConstraint", "ValueRangeConstraint", "ConstraintsIntersection")
( entityPhysicalGroup, entPhysicalIndex, ) = mibBuilder.importSymbols("ENTITY-MIB", "entityPhysicalGroup", "entPhysicalIndex")
( SnmpAdminString, ) = mibBuilder.importSymbols("SNMP-FRAMEWORK-MIB", "SnmpAdminString")
( ObjectGroup, ModuleCompliance, NotificationGroup, ) = mibBuilder.importSymbols("SNMPv2-CONF", "ObjectGroup", "ModuleCompliance", "NotificationGroup")
( ModuleIdentity, MibScalar, MibTable, MibTableRow, MibTableColumn, Unsigned32, IpAddress, mib_2, iso, TimeTicks, Bits, Counter64, Integer32, Counter32, ObjectIdentity, MibIdentifier, Gauge32, NotificationType, ) = mibBuilder.importSymbols("SNMPv2-SMI", "ModuleIdentity", "MibScalar", "MibTable", "MibTableRow", "MibTableColumn", "Unsigned32", "IpAddress", "mib-2", "iso", "TimeTicks", "Bits", "Counter64", "Integer32", "Counter32", "ObjectIdentity", "MibIdentifier", "Gauge32", "NotificationType")
( TextualConvention, DisplayString, TimeStamp, ) = mibBuilder.importSymbols("SNMPv2-TC", "TextualConvention", "DisplayString", "TimeStamp")
entitySensorMIB = ModuleIdentity((1, 3, 6, 1, 2, 1, 99)).setRevisions(("2002-12-16 00:00",))
if mibBuilder.loadTexts: entitySensorMIB.setLastUpdated('200212160000Z')
if mibBuilder.loadTexts: entitySensorMIB.setOrganization('IETF Entity MIB Working Group')
if mibBuilder.loadTexts: entitySensorMIB.setContactInfo('        Andy Bierman\n                     Cisco Systems, Inc.\n                Tel: +1 408-527-3711\n             E-mail: abierman@cisco.com\n             Postal: 170 West Tasman Drive\n                     San Jose, CA USA 95134\n\n                     Dan Romascanu\n                     Avaya Inc.\n                Tel: +972-3-645-8414\n              Email: dromasca@avaya.com\n             Postal: Atidim technology Park, Bldg. #3\n                     Tel Aviv, Israel, 61131\n\n                     K.C. Norseth\n                     L-3 Communications\n                Tel: +1 801-594-2809\n              Email: kenyon.c.norseth@L-3com.com\n             Postal: 640 N. 2200 West.\n\n                     Salt Lake City, Utah 84116-0850\n\n             Send comments to <entmib@ietf.org>\n             Mailing list subscription info:\n               http://www.ietf.org/mailman/listinfo/entmib ')
if mibBuilder.loadTexts: entitySensorMIB.setDescription('This module defines Entity MIB extensions for physical\n             sensors.\n\n             Copyright (C) The Internet Society (2002). This version\n             of this MIB module is part of RFC 3433; see the RFC\n             itself for full legal notices.')
entitySensorObjects = MibIdentifier((1, 3, 6, 1, 2, 1, 99, 1))
entitySensorConformance = MibIdentifier((1, 3, 6, 1, 2, 1, 99, 3))
class EntitySensorDataType(Integer32, TextualConvention):
    subtypeSpec = Integer32.subtypeSpec+ConstraintsUnion(SingleValueConstraint(1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12,))
    namedValues = NamedValues(("other", 1), ("unknown", 2), ("voltsAC", 3), ("voltsDC", 4), ("amperes", 5), ("watts", 6), ("hertz", 7), ("celsius", 8), ("percentRH", 9), ("rpm", 10), ("cmm", 11), ("truthvalue", 12),)

class EntitySensorDataScale(Integer32, TextualConvention):
    subtypeSpec = Integer32.subtypeSpec+ConstraintsUnion(SingleValueConstraint(1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17,))
    namedValues = NamedValues(("yocto", 1), ("zepto", 2), ("atto", 3), ("femto", 4), ("pico", 5), ("nano", 6), ("micro", 7), ("milli", 8), ("units", 9), ("kilo", 10), ("mega", 11), ("giga", 12), ("tera", 13), ("exa", 14), ("peta", 15), ("zetta", 16), ("yotta", 17),)

class EntitySensorPrecision(Integer32, TextualConvention):
    subtypeSpec = Integer32.subtypeSpec+ValueRangeConstraint(-8,9)

class EntitySensorValue(Integer32, TextualConvention):
    subtypeSpec = Integer32.subtypeSpec+ValueRangeConstraint(-1000000000,1000000000)

class EntitySensorStatus(Integer32, TextualConvention):
    subtypeSpec = Integer32.subtypeSpec+ConstraintsUnion(SingleValueConstraint(1, 2, 3,))
    namedValues = NamedValues(("ok", 1), ("unavailable", 2), ("nonoperational", 3),)

entPhySensorTable = MibTable((1, 3, 6, 1, 2, 1, 99, 1, 1), )
if mibBuilder.loadTexts: entPhySensorTable.setDescription('This table contains one row per physical sensor represented\n            by an associated row in the entPhysicalTable.')
entPhySensorEntry = MibTableRow((1, 3, 6, 1, 2, 1, 99, 1, 1, 1), ).setIndexNames((0, "ENTITY-MIB", "entPhysicalIndex"))
if mibBuilder.loadTexts: entPhySensorEntry.setDescription('Information about a particular physical sensor.\n\n\n\n            An entry in this table describes the present reading of a\n            sensor, the measurement units and scale, and sensor\n            operational status.\n\n            Entries are created in this table by the agent.  An entry\n            for each physical sensor SHOULD be created at the same time\n            as the associated entPhysicalEntry.  An entry SHOULD be\n            destroyed if the associated entPhysicalEntry is destroyed.')
entPhySensorType = MibTableColumn((1, 3, 6, 1, 2, 1, 99, 1, 1, 1, 1), EntitySensorDataType()).setMaxAccess("readonly")
if mibBuilder.loadTexts: entPhySensorType.setDescription('The type of data returned by the associated\n            entPhySensorValue object.\n\n            This object SHOULD be set by the agent during entry\n            creation, and the value SHOULD NOT change during operation.')
entPhySensorScale = MibTableColumn((1, 3, 6, 1, 2, 1, 99, 1, 1, 1, 2), EntitySensorDataScale()).setMaxAccess("readonly")
if mibBuilder.loadTexts: entPhySensorScale.setDescription('The exponent to apply to values returned by the associated\n            entPhySensorValue object.\n\n            This object SHOULD be set by the agent during entry\n            creation, and the value SHOULD NOT change during operation.')
entPhySensorPrecision = MibTableColumn((1, 3, 6, 1, 2, 1, 99, 1, 1, 1, 3), EntitySensorPrecision()).setMaxAccess("readonly")
if mibBuilder.loadTexts: entPhySensorPrecision.setDescription("The number of decimal places of precision in fixed-point\n            sensor values returned by the associated entPhySensorValue\n            object.\n\n            This object SHOULD be set to '0' when the associated\n            entPhySensorType value is not a fixed-point type: e.g.,\n            'percentRH(9)', 'rpm(10)', 'cmm(11)', or 'truthvalue(12)'.\n\n            This object SHOULD be set by the agent during entry\n            creation, and the value SHOULD NOT change during operation.")
entPhySensorValue = MibTableColumn((1, 3, 6, 1, 2, 1, 99, 1, 1, 1, 4), EntitySensorValue()).setMaxAccess("readonly")
if mibBuilder.loadTexts: entPhySensorValue.setDescription('The most recent measurement obtained by the agent for this\n            sensor.\n\n            To correctly interpret the value of this object, the\n            associated entPhySensorType, entPhySensorScale, and\n            entPhySensorPrecision objects must also be examined.')
entPhySensorOperStatus = MibTableColumn((1, 3, 6, 1, 2, 1, 99, 1, 1, 1, 5), EntitySensorStatus()).setMaxAccess("readonly")
if mibBuilder.loadTexts: entPhySensorOperStatus.setDescription('The operational status of the sensor.')
entPhySensorUnitsDisplay = MibTableColumn((1, 3, 6, 1, 2, 1, 99, 1, 1, 1, 6), SnmpAdminString()).setMaxAccess("readonly")
if mibBuilder.loadTexts: entPhySensorUnitsDisplay.setDescription('A textual description of the data units that should be used\n            in the display of entPhySensorValue.')
entPhySensorValueTimeStamp = MibTableColumn((1, 3, 6, 1, 2, 1, 99, 1, 1, 1, 7), TimeStamp()).setMaxAccess("readonly")
if mibBuilder.loadTexts: entPhySensorValueTimeStamp.setDescription('The value of sysUpTime at the time the status and/or value\n            of this sensor was last obtained by the agent.')
entPhySensorValueUpdateRate = MibTableColumn((1, 3, 6, 1, 2, 1, 99, 1, 1, 1, 8), Unsigned32()).setUnits('milliseconds').setMaxAccess("readonly")
if mibBuilder.loadTexts: entPhySensorValueUpdateRate.setDescription('An indication of the frequency that the agent updates the\n            associated entPhySensorValue object, representing in\n            milliseconds.\n\n            The value zero indicates:\n\n                - the sensor value is updated on demand (e.g.,\n                  when polled by the agent for a get-request),\n                - the sensor value is updated when the sensor\n                  value changes (event-driven),\n                - the agent does not know the update rate.\n\n            ')
entitySensorCompliances = MibIdentifier((1, 3, 6, 1, 2, 1, 99, 3, 1))
entitySensorGroups = MibIdentifier((1, 3, 6, 1, 2, 1, 99, 3, 2))
entitySensorCompliance = ModuleCompliance((1, 3, 6, 1, 2, 1, 99, 3, 1, 1)).setObjects(*(("ENTITY-SENSOR-MIB", "entitySensorValueGroup"), ("ENTITY-MIB", "entityPhysicalGroup"),))
if mibBuilder.loadTexts: entitySensorCompliance.setDescription('Describes the requirements for conformance to the Entity\n            Sensor MIB module.')
entitySensorValueGroup = ObjectGroup((1, 3, 6, 1, 2, 1, 99, 3, 2, 1)).setObjects(*(("ENTITY-SENSOR-MIB", "entPhySensorType"), ("ENTITY-SENSOR-MIB", "entPhySensorScale"), ("ENTITY-SENSOR-MIB", "entPhySensorPrecision"), ("ENTITY-SENSOR-MIB", "entPhySensorValue"), ("ENTITY-SENSOR-MIB", "entPhySensorOperStatus"), ("ENTITY-SENSOR-MIB", "entPhySensorUnitsDisplay"), ("ENTITY-SENSOR-MIB", "entPhySensorValueTimeStamp"), ("ENTITY-SENSOR-MIB", "entPhySensorValueUpdateRate"),))
if mibBuilder.loadTexts: entitySensorValueGroup.setDescription('A collection of objects representing physical entity sensor\n            information.')
mibBuilder.exportSymbols("ENTITY-SENSOR-MIB", EntitySensorDataType=EntitySensorDataType, entitySensorCompliance=entitySensorCompliance, entPhySensorValueUpdateRate=entPhySensorValueUpdateRate, entPhySensorOperStatus=entPhySensorOperStatus, EntitySensorValue=EntitySensorValue, entitySensorValueGroup=entitySensorValueGroup, entitySensorConformance=entitySensorConformance, entPhySensorScale=entPhySensorScale, entPhySensorEntry=entPhySensorEntry, entPhySensorValueTimeStamp=entPhySensorValueTimeStamp, entPhySensorPrecision=entPhySensorPrecision, entPhySensorType=entPhySensorType, entPhySensorValue=entPhySensorValue, entitySensorObjects=entitySensorObjects, PYSNMP_MODULE_ID=entitySensorMIB, EntitySensorStatus=EntitySensorStatus, entitySensorCompliances=entitySensorCompliances, entitySensorGroups=entitySensorGroups, entPhySensorTable=entPhySensorTable, EntitySensorDataScale=EntitySensorDataScale, entitySensorMIB=entitySensorMIB, entPhySensorUnitsDisplay=entPhySensorUnitsDisplay, EntitySensorPrecision=EntitySensorPrecision)
