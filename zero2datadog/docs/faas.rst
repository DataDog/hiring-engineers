Arkade & OpenFaaS: serverless on the spot
===========================================

The Goal
---------

Setup serverless Kubernetes services

* on the spot
* using the same simple tools
* regardless of the infrastructure.

The Problem: so many moving parts
----------------------------------

The infrastructure might change and if (when) it does, you don't want to have to unravel your hostnames, service bindings,
TLS certificates, credentials, etc.
On the new infrastructure all of that might be different and the processes might also change, ``helm`` versions, package management,
registry names, etc.

Starting from a bare kubernetes cluster... on your laptop, in a cloud provider, home lab, it doesn't matter (that's the first benefit).
Let's say you create something in Digital Ocean, as I did for this exercise:

.. code-block::

	doctl kubernetes cluster create openfaas-arkadedog   \
	--access-token=$DO_TOKEN --region="sfo2"   --auto-upgrade="true" \
	--node-pool="name=main;size=s-1vcpu-2gb;count=2;tag=openfaas;tag=datadog"


Now, this is where the heavy lifting would start, from here you would want to create:

* a metrics server
* Add a kube-state metrics sidecar
* a certificate manager
* an ingress controller
* a local docker registry
* another ingress
* more certificates and secrets

You still don't have a way to deploy applications... the next step would be to stand up services and you would have to make decisions
about configurations, etc.

The Solution
-----------------------------

What if there was a way to automate the moving parts into a single tool?

Enter Arkade....

k8s open for business
-----------------------

Arkade handles the interaction with the package manager and config tools (``helm``, ``kubectl``, etc.)

About 500 lines of Yaml, required to get a private docker registry with metrics and certificates in place, are replaced by
a small code block that gets you to the point where you can deploy serverless functions regardless of the infrastructure:

.. code-block::

	arkade install metrics-server
	arkade install kube-state-metrics
	arkade install nginx-ingress
	arkade install cert-manager
	arkade install  docker-registry --wait
	arkade install openfaas --load-balancer --ingress-operator --wait
	arkade install openfaas-ingress \
	  --domain i.do.controlplane.info \
	  --email jitkelme@gmail.com


This process will take five to 10 minutes, which you can spend doing something useful instead of editing config files.

.. asciinema:: 327397

One click DataDog Agent
------------------------

Not only does it handle the integrated apps, :term:`Arkade` will also install custom Helm charts, so you can install the Datadog cluster agent and node agent with a single click.
No more dealing with Helm vs Tiller, RBAC, serviceaccount, clusterrole bindings, etc.

.. code-block:: bash

	arkade install chart --repo-name stable/datadog \
	--set datadog.apiKey=$DD_API_KEY \
	--set datadog.apm.enabled="true" \
	--set datadog.clusterAgent.enabled="true" \
	--set datadog.clusterAgent.token=$DD_CLUSTER_KEY

It's gratifying to sit back and watch how arkade does all the busywork for you:

.. asciinema:: 327393



