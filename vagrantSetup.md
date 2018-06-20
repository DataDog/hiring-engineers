## Vagrant Box Setup
#### __Here is my finished base box__ [KPM/miller_dd_box](https://app.vagrantup.com/KPM/boxes/miller_dd_box/versions/1.0.0)
You can download that box and continue to the next section [Collecting Metrics](answers.md#collecting-metrics). 

The following are the steps I took to set up that base box:<br>
For my base box I choose Ubuntu 's latest Build, Bionic Beaver 18.04 LTS [ubuntu/bionic64](https://app.vagrantup.com/ubuntu/boxes/bionic64)

After installing this base box and running `vagrant up` I accessed my VM via `vagrant ssh`.
While there I ran the following commands to get my machine set up with a Postgres database.
    
    # get new package updates
    sudo apt-get update
    # install general updates
    sudo apt-get upgrade
    # install postgres
    sudo apt-get install postgresql postgresql-contrib
    
Then I set up postgres...
    
     # create user postgres that also creates a superuser with your hostname
     sudo -u postgres createuser --superuser $USER
     #create a database with your host name 
     createdb $USER
     
 Next I set up the permissions in the `pg_hba.conf` file to  not require a password for localhost development.
 
cd over to `../../etc/postgresql/10/main/` and `sudo vim pg_hba.conf`. 
Change the permissions for IPv4  and IPv6 from `md5` -> `trust`

    # IPv4 local connections:
    host    all             all             127.0.0.1/32           trust
    # IPv6 local connections:
    host    all             all             ::1/128                 trust

and restart `sudo service postgresql restart`
