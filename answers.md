Sarah Schaab - Solutions Engineer Candidate

Setup:
I set up my environment with Vagrant and VirtualBox.
I then installed the Datadog Agent for Mac OSX using the command line and the Datadog Agent Install instructions.


Collecting Metrics:

  Adding Host Tags
  
    After a bit of experimentation working with the datadog.yaml file and the datadog UI Dashboard I found the documentation for assigning Tags at https://docs.datadoghq.com/getting_started/tagging/assigning_tags/
    First, I chose to add a tag through the UI, with a key of hello and a value of world "hello:world"
    Then, I navigated to the datadog.yaml file and uncommented line 35, "tags:", and added my own tags, region:eastus, region:westus, and region:centralus.

    According to the documentation you should use the following form in the datadog.yaml file:
    tags: key_first_tag:value_1, key_second_tag:value_2, key_third_tag:value_3

    Upon trying to restart the agent, I ran into an error and went with the second form listed:
    tags:
      - key_first_tag:value_1
      - key_second_tag:value_2
      - key_third_tag:value_3
