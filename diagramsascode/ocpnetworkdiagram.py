from diagrams import Cluster, Diagram
from diagrams.aws.compute import ECS
from diagrams.aws.database import ElastiCache, RDS
from diagrams.aws.network import ELB
from diagrams.aws.network import Route53
from diagrams.onprem.network import Haproxy

with Diagram("OpenShift 4.3 with external load balancer", show=False):
    dns = Route53("dns")
    lb = ELB("F5")
    internallb = Haproxy("Internal load balancer")

    with Cluster("Masters"):
        master_group = [ECS("master1"),
                     ECS("master2"),
                     ECS("master3")]

    with Cluster("Infra nodes"):
                         infra_group = [ECS("infranode1"),
                                      ECS("infranode2")]

    with Cluster("Worker nodes"):
                         worker_group = [ECS("workernode1"),
                         ECS("workernode2")]

    with Cluster("CA bundle, http://bit.ly/marcredhatcerts"):
                        ca_bundle = ECS("CA bundle")


    with Cluster("Storage, http://bit.ly/marcredhatstorage"):
        storage = RDS("Container registry")
        storage - [RDS("Apps")]


    internallb >> master_group
    internallb >> infra_group >> storage
    dns >> lb >> worker_group >> storage
    worker_group >> ca_bundle
