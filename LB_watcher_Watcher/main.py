#!/bin/env python3
from kubernetes import client, config
from kubernetes.leaderelection import leaderelection
from kubernetes.leaderelection.resourcelock.configmaplock import ConfigMapLock
from kubernetes.leaderelection import electionconfig
import threading
import logging
import socket
import os

# self-build informer this is not stable
# FIXME: rewrite it at go lang or js which has informer
# FIXME: change it to class


# init logging moudle
logging.basicConfig(level=logging.INFO)

# Authenticate using config file
config.load_kube_config(config_file=r"~/.kube/config")
# config.load_incluster_config()

# leader election setting
# leaderElectionConfig = {
#     # A unique identifier for this candidate
#     "candidate_id": socket.gethostname(),
#     # Name of the lock object to be created
#     "lock_namespace": os.environ["namespace"],           # Kubernetes namespace
#     "lock_name_prefix": os.environ["name_prefix"],
#     "lock_range_min": int(os.environ["range_min"]),
#     "lock_range_max": int(os.environ["range_max"])
# }

leaderElectionConfig = {}
leaderElectionConfig["candidate_id"] = "rtpengine-daemonset-tcqgq"
leaderElectionConfig["lock_namespace"] = "default"
leaderElectionConfig["lock_name_prefix"] = "test"
leaderElectionConfig["lock_range_min"] = int("0")
leaderElectionConfig["lock_range_max"] = int("4")

def onstarted_leading(lock_name=""):
    body = {
        "metadata": {
            "labels": {
                lock_name: "True"
            }
        }
    }
    print(body)
    client.CoreV1Api().patch_namespaced_pod(
        leaderElectionConfig["candidate_id"], "default", body)


def onstopped_leading(lock_name):
    body = {
        "metadata": {
            "labels": {
                lock_name: "False"
            }
        }
    }
    client.CoreV1Api().patch_namespaced_pod(
        leaderElectionConfig["candidate_id"], "default", body)


def leaderElectionJob(leader_number=0):
    lock_name = leaderElectionConfig["lock_name_prefix"] + str(leader_number)
    config = electionconfig.Config(ConfigMapLock(lock_name,
                                                 leaderElectionConfig["lock_namespace"],
                                                 leaderElectionConfig["candidate_id"]),
                                   lease_duration=2, renew_deadline=1.3, retry_period=1,
                                   onstarted_leading=lambda: onstarted_leading(
                                       lock_name),
                                   onstopped_leading=lambda: onstopped_leading(lock_name))
    # Enter leader election
    leaderelection.LeaderElection(config).run()


def main():
    for i in range(leaderElectionConfig["lock_range_min"], leaderElectionConfig["lock_range_max"]):
        threading.Thread(target=leaderElectionJob,args=([i])).start()


if __name__ == '__main__':
    main()
