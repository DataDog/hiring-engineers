.. _glossary:

Glossary of DataDog concepts
============================

.. glossary::

	Agent
		The current package is called `datadog-agent` and is at version 7.x https://docs.datadoghq.com/agent/#overview

	``app_key``
		Needed for READ access

	``api_key``
		Needed for WRITE access

	APM
		Application Performance Monitoring: |about_APM|

	Autodiscovery
		https://docs.datadoghq.com/agent/faq/template_variables/

	Basic
		This anomaly detection algorithm uses a simple lagging rolling quantile computation to determine the range of expected values.
		It uses very little data and adjusts quickly to changing conditions but has no knowledge of seasonal behavior or longer trends.
		See also https://docs.datadoghq.com/monitors/monitor_types/anomaly/#anomaly-detection-algorithms

	Check
		Custom agent check: https://docs.datadoghq.com/developers/write_agent_check

	Resource
		A resource is a particular action for a given service (typically an individual endpoint or query). A helpful
		mnemonic could be: *A service...provides (serves) a resource*

	Service
		Services are the building blocks of modern microservice architectures.
		Broadly speaking, a service groups together endpoints, queries, or jobs for the purposes of scaling instances

	Timeboard
		https://docs.datadoghq.com/dashboards/timeboards/#pagetitle


.. Substitutions

.. |about_APM| replace:: https://docs.datadoghq.com/tracing/visualization/#pagetitle


