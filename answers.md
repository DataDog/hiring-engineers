This is Michael Hawley's submission for a Sales Engineer/Solutions engineer role. I decided for the sake of originality to make a sudo (hah get it?) tutorial, to help outline the steps I took for this challenge and present it in a way that a potential end user could follow easily.

## Environment

While you can use any environment really, the recommended option is use a virtual machine, linux-based. To learn a new tool for my own personal experience, I used Vagrant with an Ubuntu OS. It's highly recommended that you're on 16.04 or later to avoid any dependency issues with package management.

Follow the [Vagrant Getting Started](https://www.vagrantup.com/intro/getting-started/index.html) guides to set up the virtual machine. The [Xenial64](https://app.vagrantup.com/ubuntu/boxes/xenial64) box is the used for this guide so instead of `vagrant init hashicorp/precise64`, use `vagrant init ubuntu/xenial64`.

To install the necessary packages, copy [bootstrap.sh](./bootstrap.sh).

In your Vagrantfile, add the line: `config.vm.provision :shell, path: "bootstrap.sh"` to provision the machine with the packages you'll need for this exercise.
