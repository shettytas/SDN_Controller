# Static Routing using SDN Controller (Ryu + Mininet)

## Problem Statement

Implement static routing paths using an SDN controller by manually installing flow rules in switches. The objective is to ensure deterministic packet forwarding and validate that the routing path remains unchanged even after rule reinstallation.

---

## Objectives

* Define fixed routing paths
* Install flow rules manually via controller
* Validate packet delivery
* Observe flow table behavior
* Perform regression testing (path stability)

---

## Network Topology

```
h1 ---- s1 ---- s2 ---- h2
```

* h1: 10.0.0.1
* h2: 10.0.0.2
* s1, s2: OpenFlow switches

---

## Technologies Used

* Mininet (network emulation)
* Ryu Controller (SDN controller)
* OpenFlow 1.3
* Wireshark (packet analysis)
* iperf / ping (performance testing)

---

## Setup & Execution Steps

### 1. Start Ryu Controller

```bash
ryu-manager controller.py
```

### 2. Run Mininet Topology

```bash
sudo mn --custom topo.py --topo static --controller=remote --switch ovsk,protocols=OpenFlow13
```

### 3. Test Connectivity

```bash
mininet> pingall
```

### 4. Run iperf Test

```bash
mininet> h1 iperf -s &
mininet> h2 iperf -c 10.0.0.1
```

---

## Expected Output

###  Ping Result

* 0% packet loss
* Successful communication between h1 and h2

###  Controller Logs

```
[INFO] Switch connected: 1
[INFO] Switch connected: 2
[PACKET_IN] Switch 1 received packet on port X
```

---

## Flow Table Verification

Run:

```bash
sudo ovs-ofctl dump-flows s1
sudo ovs-ofctl dump-flows s2
```

Expected:

* Static rules mapping port 1 ↔ port 2
* No dynamic learning behavior

---
## OUTPUT 
 ![Start](images\3.jpeg)
* Flow tables
![Flow tables](images\5.jpeg)

* ICMP packets (ping)
![ping command](images\6.jpeg)
![](images\4.jpeg)
* TCP traffic (iperf)
 ![](images\10.jpeg)

---
## Test Scenarios

### Scenario 1: Normal vs Failure

#### Failure Case
![Failure](images/failure.png)

- 100% packet loss observed
- Indicates missing/incorrect flow rules

#### Normal Case
![Success](images/success.png)

- 0% packet loss
- Static routing works correctly

---

### Scenario 2: Allowed vs Blocked Traffic

- Traffic from h1 → h2 blocked (no action)
- Traffic from h2 → h1 allowed

---

### Scenario 3: Regression Testing

Procedure:

1. Restart controller
2. Reinstall flow rules
3. Re-run ping

Expected Result:

* Path remains unchanged
* No alternate routing observed
* Confirms deterministic routing

---

## Observations

* Routing is fully controller-driven
* No MAC learning required
* Deterministic forwarding ensured

---

## References

1. OpenFlow Switch Specification v1.3
2. Ryu SDN Framework Documentation
3. Mininet Official Documentation
4. SDN Architecture (ONF White Paper)

---

##
