# DF::DistFabric
Distributed Fabric is a POC project in an attempt to create a minimal platform for supporting applications that can leverage distributed computing on top of it. This project is intended for understanding basics of distributing tasks among multiple nodes for performance enhancement. On top of that, it is an attempt to create a generic platform on top of which applications can be easily plugged to leverage underlying distributed environment.

## Dependencies
Distributed Fabric uses RabbitMQ for communication between master and the nodes. To install RabbitMQ in Ubuntu/Debian distributions, follow [techadmin](https://tecadmin.net/install-rabbitmq-server-on-ubuntu/) or [rabbitmq](https://www.rabbitmq.com/install-debian.html#supported-debian-distributions).

All the other dependencies are listed in `requirements.txt` and can be installed using `sh install-requirements.sh`. 

## Configuration
Configuration file `conf.json` determines the behaviour of a node. Following are important part of the configuration.
1. `whoAmI` determines if a node is a master or just a node. The value needs to be set to `MASTER` if the node is master or integer identifier of the node (e.g. 1,2..). 
2. `sync.dir` is the directory that is shared between all the nodes (master too). This is to enable the data sharing between nodes if required. `Rsync` is used internally to sync folder between the nodes. 
3. `rabbitmq` holds configuration regading the rabbitmq used. 
4. `nodes` lists all the nodes that are part of the distributed system. (Important, all the nodes should be accessible to master node via ssh without password. Also all nodes should have same user)
5. `logDir` is the directory where the results are stored if required.

## Usage
One can create their own distributed application by following the example `search` application available at `appstore/search`. This application needs to be registered to `appstore/registry.py`.

After a valid configuration is put in `conf.json`, issue the command `sh run.sh` which will bring up the node. The node will act as master or worker according the configuration. All the nodes listed in the configuration of master should be spawned and running. 

Now, the master node will enable a CLI interface from where one can invoke the distributed application using the following command (Seach example in this case).
```bash
invoke search $relative_path_to_directory_inside_shared_dir $search_file.txt
``` 
