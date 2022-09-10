#!/bin/env python3
template = """
apiVersion: v1
kind: Service
metadata:
  name: rtpengine-10-22-149-230-p{partition}
  annotations:
    metallb.universe.tf/allow-shared-ip: "key-to-share-10.22.149.230"
spec:
  type: LoadBalancer
  selector:
    ip: 10.22.149.230
    rtpengine-10.22.149.230-p{partition}: "True"
  ports:
{port_template}\
"""
portTemplate = """\
    - name: rtp-{port}
      protocol: UDP
      port: {port}
      targetPort: {port}
"""

base = 20000
partition_size = 2000
for p in range(0, 3):
    tmp = []
    for i in range(0, partition_size):
        tmp.append(portTemplate.format(port=base + p * partition_size + i))
    print(template.format(port_template="".join(tmp), partition=p))
    print("---")
