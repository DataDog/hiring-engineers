<!-- Header -->
<br />
<p align="center">
  <a href="https://upload.wikimedia.org/wikipedia/en/thumb/7/7e/Datadog_logo.svg/1200px-Datadog_logo.svg.png">
    <img src="images/logo.png" alt="Logo" width="80" height="80">
  </a>

  <h3 align="center">Datadog - Sales Engineer Technical Interview</h3>

  <p align="center">
    Valentin PEREIRA
    <br />
    <a href="https://www.linkedin.com/in/valentin-pereira/"><strong>View on LinkedIn »</strong></a>
    <br />
  </p>
</p>



<!-- Table of contents -->
<details open="open">
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#setup-the-environment">Setup the environment</a>
      <ul>
        <li><a href="#installing-the-datadog-agent">Installing the Datadog agent</a></li>
      </ul>
    </li>
    <li>
      <a href="#collecting-metrics">Collecting Metrics</a>
    </li>
    <li><a href="#visualizing-data">Visualizing Data</a></li>
    <li><a href="#monitoring-data">Monitoring Data</a></li>
    <li><a href="#collecting-apm-data">Collecting APM Data</a></li>
    <li><a href="#final-question">Final Question</a></li>
  </ol>
</details>



<!-- Prerequisites -->
## Setup the environment

To ensure a proper environment for this exercise, and avoid dependency issues, we are using Vagrant to spawn an Ubuntu Virtual Machine with version 18.04.3.

Following the steps detailed on [Vagrant](https://learn.hashicorp.com/collections/vagrant/getting-started) getting-started guide, we simply installed Vagrant and [VirtualBox](https://www.virtualbox.org/), and performed the following steps:

```
vagrant init hashicorp/bionic64
vagrant up
```

Our VM is now running. We then SSH into it using:
```
vagrant ssh
```

### Installing the Datadog agent

Following the installation process after creating a [Datadog account](https://docs.datadoghq.com/), we are installing the Datadog Agent on our Ubuntu VM, using the simple following command:

```
DD_AGENT_MAJOR_VERSION=7 DD_API_KEY=aac12d08c8efaa3d00c0fb61eadfec5f DD_SITE="datadoghq.eu" bash -c "$(curl -L https://s3.amazonaws.com/dd-agent/scripts/install_script.sh)"
```

The agent is now running:
![agent running screenshot](img/screenshot_1.png)


<!-- Collecting Metrics -->
## Collecting Metrics

ToDo


<!-- Visualizing Data -->
## Visualizing Data

ToDo

<!-- Monitoring Data -->
## Monitoring Data

ToDo


<!-- Collecting APM Data -->
## Collecting APM Data

ToDo

<!-- Final Question -->
## Final Question

ToDo


