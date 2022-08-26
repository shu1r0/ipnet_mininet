# MPLS Examples

## MPLS Config
```comandline
sudo apt install linux-modules-extra-`uname -r`
sudo modprobe mpls-router
sudo modprobe mpls_gso
sudo modprobe mpls-iptunnel
```

## `sr_mpls_10.py`

![sr_mpls_10](./sr_mpls_10.drawio.png)

## MPLS (SR-MPLS) comand
* `show mpls table`
* `show ip ospf database segment-routing`