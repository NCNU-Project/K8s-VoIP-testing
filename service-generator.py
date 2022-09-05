#!/bin/env python3
template = """
apiVersion: v1
kind: Service
metadata:
  name: rtpengine-163-22-22-68-p0
  annotations:
    metallb.universe.tf/allow-shared-ip: "key-to-share-163.22.22.68"
spec:
  type: LoadBalancer
  selector:
    ip: 163.22.22.68
    partition-leader-0: "True"
  ports:
{port_template}\
"""
portTemplate = """\
    - name: rtp-{port}
      protocol: UDP
      port: {port}
      targetPort: {port}
"""

tmp = []
for i in range(20000, 20020):
    tmp.append(portTemplate.format(port=i))
print(template.format(port_template="".join(tmp)))
