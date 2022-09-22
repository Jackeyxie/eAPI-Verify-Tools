# eAPI-Verify-Tools
Verify Tools use eAPI
## Install
## Requerment
```bash
 
 python3 -v
```

Use PIP install python packegs

```
pip install -r requirements.txt
```
Verify pip 
```
pip3 list
Package          Version
---------------- -------
jsonrpclib-pelix 0.4.3.2
PyYAML           6.0
```

##Usage Guide
### enable eAPI on Arista Eos Device
```
configure
management api http-commands
   protocol https port 443
   no shutdown
   vrf MGMT
      no shutdown
end
```

```
DC1_SPINE1#show management api http-commands 
Enabled:            Yes
HTTPS server:       running, set to use port 443
HTTP server:        shutdown, set to use port 80
Local HTTP server:  shutdown, no authentication, set to use port 8080
Unix Socket server: shutdown, no authentication
VRFs:               MGMT
Hits:               2440
Last hit:           4814 seconds ago
Bytes in:           387050
Bytes out:          2531922
Requests:           1981
Commands:           3541
Duration:           348.398 seconds
SSL Profile:        none
FIPS Mode:          No
QoS DSCP:           0
Log Level:          none
CSP Frame Ancestor: None
TLS Protocols:      1.0 1.1 1.2
   User        Requests       Bytes in       Bytes out    Last hit        
----------- -------------- -------------- --------------- ----------------
   admin       1981           387050         2531922      4814 seconds ago

URLs                                           
-----------------------------------------------
Management0 : https://172.100.100.2:443        
Management0 : https://[2001:172:100:100::a]:443
```

###Define the switches to check in devices.txt (multiple devices or a single device can be defined)
```
% cat device.txt
172.100.100.2
172.100.100.3
172.100.100.4
```

### The CLI commands for custom inspection are divided into summary and detail commands for processing. 
    -- summary   All commands outputs in a single text file for easy comparison before and after 
    -- detail    The commands output as a separate file for each command. Easy to check in detail

#### Example ：
```
---
# list of EOS commands to collect in summary format - qucik Diff 
cli_summary:
  - show version | grep Software
  - show module
  - show interfaces status | grep connected | wc -l
  - show ip interface brief | grep up | wc -l
  - show ip bgp summary | grep Esta | wc -l
  - show ipv6 bgp summary | grep Esta | wc -l
  - show ip bgp summary | grep -vE "Esta|Desc|Neigh|identifier|default" | wc -l
  - show ipv6 bgp summary | grep -vE "Esta|Desc|Neigh|identifier|default" | wc -l
  - show ip route vrf all summary | grep -E "VRF|Total"
  - show ipv6 route vrf all summary | grep -E "VRF|Total"
  - show platform fap ip route summary
  - show extensions
  - show boot-extensions

# list of EOS commands to collect in detail output --- to check what is happend.
cli_detail:
  - show version
  - show extensions
  - show boot-extensions
  - show inventory
  - show running-config diffs
  - show agent logs crash
  - show system coredump
  - show logging last 7 days threshold warnings
  - show uptime
  - show reload cause
  - show system environment temperature
  - show system environment temperature transceiver
  - show system environment cooling
  - show system environment power
  - show processes top once
  - show ntp status
  #- show platform trident forwarding-table partition
  - show hardware tcam profile
  - show hardware counter drop
  - show interfaces counters rates
  - show interfaces counters errors
  - show interfaces counters discards
  - show interfaces status
  - show port-channel
  - show lacp counters all-ports
  - show spanning-tree blockedports
  - show ip interface brief
  - show interfaces description
  - show ip route summary
  - show bfd peers
  - show bgp ipv4 unicast summary vrf all
  - show bgp ipv6 unicast summary vrf all
  - show bgp evpn summary
  - show bgp rt-membership summary
  - show mlag
  - show mlag config-sanity
  - show running-config
  - show lldp neighbors
  - show interfaces counters rates | nz
  - show platform sand l3 summary
  - show platform sand health
 ```
 

## Check Device  
```
$ python3 ./collect-eos-commands.py --help
usage: collect-eos-commands.py [-h] -i FILE -u USERNAME -c EOS_COMMANDS -o OUTPUT_DIRECTORY

Collect output of EOS commands

optional arguments:
  -h, --help           show this help message and exit
  -i FILE              Text file containing a list of switches
  -u USERNAME          Devices username
  -c EOS_COMMANDS      YAML file containing the list of EOS commands to collect
  -o OUTPUT_DIRECTORY  Output directory
```

```
[jackey@avd-ceos-lab]$ python3 ./collect-eos-commands.py -i device.txt -c eos_command.ymal -u admin -o test
Device password: 
['172.100.100.2']
Connecting to devices .... please be patient ... 


Collecting show commands output on device 172.100.100.2
Unable to collect and save the json command show module
Unable to collect and save the json command show ip bgp summary | exclue Esta | wc -l
Unable to collect and save the json command show platform fap ip route summary
Unable to collect and save the text command bash timeout 10 ls /var/core
Unable to collect and save the text command show system environment power
Unable to collect and save the text command show platform trident forwarding-table partition
Unable to collect and save the text command show hardware tcam profile
Unable to collect and save the text command show hardware counter drop
Unable to collect and save the text command show platform sand l3 summary
Unable to collect and save the text command show platform sand health
```
####   If the platform is different（Sand & Stara）, there will be a corresponding prompt if the output cannot be obtained. As suggested above


After executing the command, the following files are generated

```
jackey@avd-ceos-lab test]$ tree -l
.
└── 172.100.100.2-2022-08-30-160819
    ├── cli_detail
    │   ├── show\ agent\ logs\ crash
    │   ├── show\ bfd\ peers
    │   ├── show\ bgp\ evpn\ summary
    │   ├── show\ bgp\ ipv4\ unicast\ summary\ vrf\ all
    │   ├── show\ bgp\ ipv6\ unicast\ summary\ vrf\ all
    │   ├── show\ bgp\ rt-membership\ summary
    │   ├── show\ boot-extensions
    │   ├── show\ extensions
    │   ├── show\ interfaces\ counters\ discards
    │   ├── show\ interfaces\ counters\ errors
    │   ├── show\ interfaces\ counters\ rates
    │   ├── show\ interfaces\ counters\ rates\ |\ nz
    │   ├── show\ interfaces\ description
    │   ├── show\ interfaces\ status
    │   ├── show\ inventory
    │   ├── show\ ip\ interface\ brief
    │   ├── show\ ip\ route\ summary
    │   ├── show\ lacp\ counters\ all-ports
    │   ├── show\ lldp\ neighbors
    │   ├── show\ logging\ last\ 7\ days\ threshold\ warnings
    │   ├── show\ mlag
    │   ├── show\ mlag\ config-sanity
    │   ├── show\ ntp\ status
    │   ├── show\ port-channel
    │   ├── show\ processes\ top\ once
    │   ├── show\ reload\ cause
    │   ├── show\ running-config
    │   ├── show\ running-config\ diffs
    │   ├── show\ spanning-tree\ blockedports
    │   ├── show\ system\ environment\ cooling
    │   ├── show\ system\ environment\ temperature
    │   ├── show\ system\ environment\ temperature\ transceiver
    │   ├── show\ uptime
    │   └── show\ version
    └── cli_summary
        └── cli_summary.txt
```
### Cli_summary Example：
```
------show version | grep Software-----------------------------------------------------------------
Software image version: 4.28.0F-26924507.4280F (engineering build)

------show interfaces status | grep connected | wc -l-----------------------------------------------------------------
5

------show ip interface brief | grep up | wc -l-----------------------------------------------------------------
6

------show ip bgp summary | grep Esta | wc -l-----------------------------------------------------------------
4

------show ipv6 bgp summary | grep Esta | wc -l-----------------------------------------------------------------
0

------show ip route vrf all summary | grep -E "VRF|Total"-----------------------------------------------------------------
VRF: default
   Total Routes                                              21
VRF: MGMT
   Total Routes                                               7

------show ipv6 route vrf all summary | grep -E "VRF|Total"-----------------------------------------------------------------
VRF: default
   Total Routes                              3
VRF: MGMT
   Total Routes                              5

------show extensions-----------------------------------------------------------------
! No extensions are available
The extensions are stored on internal flash (flash:)

------show boot-extensions-----------------------------------------------------------------
```

### Use Diff to compare before and after any operations. cli_summary is convenient for statistical comparison. If there is an abnormality, then compare the output of cli_detail.

 No abnormality in  cli_summary  comparison
```
 diff -Naar ./test/172.100.100.2-2022-08-30-160819/cli_summary ./test/172.100.100.2-2022-08-30-161108/cli_summary/
```
As shown in the following CLI_detail comparison (note that the difference between time and Counter can be ignored)

```
[jackey@avd-ceos-lab ANTA]$ diff -Naar ./test/172.100.100.2-2022-08-30-160819/cli_detail/ ./test/172.100.100.2-2022-08-30-161108/cli_detail/
diff -Naar "./test/172.100.100.2-2022-08-30-160819/cli_detail/show bgp evpn summary" "./test/172.100.100.2-2022-08-30-161108/cli_detail/show bgp evpn summary"
5,8c5,8
<   DC1_LEAF1A               192.168.255.3 4 65101           2034      2040    0    0    1d04h Estab   7      7
<   DC1_LEAF1B               192.168.255.4 4 65101           2021      2035    0    0    1d04h Estab   7      7
<   DC1_SVC2A                192.168.255.5 4 65102           2025      2030    0    0    1d04h Estab   7      7
<   DC1_SVC2B                192.168.255.6 4 65102           2039      2040    0    0    1d04h Estab   7      7
---
>   DC1_LEAF1A               192.168.255.3 4 65101           2038      2043    0    0    1d04h Estab   7      7
>   DC1_LEAF1B               192.168.255.4 4 65101           2024      2039    0    0    1d04h Estab   7      7
>   DC1_SVC2A                192.168.255.5 4 65102           2028      2033    0    0    1d04h Estab   7      7
>   DC1_SVC2B                192.168.255.6 4 65102           2042      2043    0    0    1d04h Estab   7      7
diff -Naar "./test/172.100.100.2-2022-08-30-160819/cli_detail/show bgp ipv4 unicast summary vrf all" "./test/172.100.100.2-2022-08-30-161108/cli_detail/show bgp ipv4 unicast summary vrf all"
5,8c5,8
<   DC1_LEAF1A_Ethernet1     172.31.255.1  4 65101           2023      2034    0    0    1d04h Estab   3      3
<   DC1_LEAF1B_Ethernet1     172.31.255.5  4 65101           2031      2036    0    0    1d04h Estab   3      3
<   DC1_SVC2A_Ethernet1      172.31.255.9  4 65102           2027      2033    0    0    1d04h Estab   3      3
<   DC1_SVC2B_Ethernet1      172.31.255.13 4 65102           2033      2033    0    0    1d04h Estab   3      3
---
>   DC1_LEAF1A_Ethernet1     172.31.255.1  4 65101           2026      2037    0    0    1d04h Estab   3      3
>   DC1_LEAF1B_Ethernet1     172.31.255.5  4 65101           2034      2039    0    0    1d04h Estab   3      3
>   DC1_SVC2A_Ethernet1      172.31.255.9  4 65102           2030      2037    0    0    1d04h Estab   3      3
>   DC1_SVC2B_Ethernet1      172.31.255.13 4 65102           2037      2036    0    0    1d04h Estab   3      3
diff -Naar "./test/172.100.100.2-2022-08-30-160819/cli_detail/show interfaces counters discards" "./test/172.100.100.2-2022-08-30-161108/cli_detail/show interfaces counters discards"
7c7
< Ma0                    437773              0
---
> Ma0                    438491              0
9c9
< Totals                 437773              0
---
> Totals                 438491              0
diff -Naar "./test/172.100.100.2-2022-08-30-160819/cli_detail/show lldp neighbors" "./test/172.100.100.2-2022-08-30-161108/cli_detail/show lldp neighbors"
1c1
< Last table change time   : 23:04:59 ago
---
> Last table change time   : 23:07:49 ago
diff -Naar "./test/172.100.100.2-2022-08-30-160819/cli_detail/show processes top once" "./test/172.100.100.2-2022-08-30-161108/cli_detail/show processes top once"
1c1
< top - 08:08:23 up 1 day,  5:19,  1 user,  load average: 7.30, 6.66, 6.89
---
> top - 08:11:13 up 1 day,  5:22,  1 user,  load average: 7.66, 6.91, 6.94
3,5c3,5
< %Cpu(s): 18.3 us, 24.5 sy,  0.0 ni, 57.3 id,  0.0 wa,  0.0 hi,  0.0 si,  0.0 st
< MiB Mem :  64263.3 total,  47141.6 free,  10946.3 used,   6175.4 buff/cache
< MiB Swap:  32256.0 total,  32256.0 free,      0.0 used.  51358.4 avail Mem 
---
> %Cpu(s): 13.4 us, 20.9 sy,  0.0 ni, 65.7 id,  0.0 wa,  0.0 hi,  0.0 si,  0.0 st
> MiB Mem :  64263.3 total,  47161.5 free,  10926.2 used,   6175.7 buff/cache
> MiB Swap:  32256.0 total,  32256.0 free,      0.0 used.  51378.5 avail Mem 
8,12c8,9
<  1274 root      20   0   20904   8220   6888 S  12.5   0.0  12:01.52 AgentMonitor
< 12020 admin     20   0    9940   2696   2080 R  12.5   0.0   0:00.06 top
<   939 root      20   0   20352   7672   2248 S   6.2   0.0  14:37.56 ProcMgr-worker
<  1052 root      20   0  258980  82128  46848 S   6.2   0.1   6:10.44 Sysdb
<  1273 root      20   0 1098008 196036  17904 S   6.2   0.3  60:13.93 OpenConfig
---
>  1273 root      20   0 1098008 196036  17904 S   6.7   0.3  60:20.25 OpenConfig
>  1299 root      20   0  194704  76984  57080 S   6.7   0.1 106:28.85 Etba
22c19
<   530 dbus      20   0   10476   3020   2472 S   0.0   0.0   0:04.27 dbus-daemon
---
>   530 dbus      20   0   10476   3020   2472 S   0.0   0.0   0:04.28 dbus-daemon
27c24
<   558 root      20   0    2256    596    528 S   0.0   0.0   0:03.74 ProcMonitor
---
>   558 root      20   0    2256    596    528 S   0.0   0.0   0:03.75 ProcMonitor
29c26
<   804 root      20   0    4260   1464    884 S   0.0   0.0   0:01.43 crond
---
>   804 root      20   0    4260   1464    884 S   0.0   0.0   0:01.44 crond
34,39c31,38
<  1016 root      20   0    4140    816    664 S   0.0   0.0   0:45.13 EosOomAdjust
<  1053 root      20   0   35996  16704   9768 S   0.0   0.0   0:11.87 StageMgr
<  1054 root      20   0  626580 316420 129760 S   0.0   0.5  13:03.53 ConfigAgent
<  1055 root      20   0  111740  38024  23272 S   0.0   0.1   0:12.37 Fru
<  1056 root      20   0    4144   1076    944 S   0.0   0.0   0:20.29 SlabMonitor
<  1057 root      20   0  157784  49972  18640 S   0.0   0.1   0:13.68 Launcher
---
>   939 root      20   0   20352   7672   2248 S   0.0   0.0  14:39.02 ProcMgr-worker
>  1016 root      20   0    4140    816    664 S   0.0   0.0   0:45.19 EosOomAdjust
>  1052 root      20   0  258980  82128  46848 S   0.0   0.1   6:11.42 Sysdb
>  1053 root      20   0   35996  16704   9768 S   0.0   0.0   0:11.88 StageMgr
>  1054 root      20   0  626580 316420 129760 S   0.0   0.5  13:07.34 ConfigAgent
>  1055 root      20   0  111740  38024  23272 S   0.0   0.1   0:12.39 Fru
>  1056 root      20   0    4144   1076    944 S   0.0   0.0   0:20.33 SlabMonitor
>  1057 root      20   0  157784  49972  18640 S   0.0   0.1   0:13.69 Launcher
41,89c40,88
<  1219 root      20   0   38544   7000   3152 S   0.0   0.0   0:04.25 CliShell
<  1244 root      20   0   38544  11084   3152 S   0.0   0.0   0:04.17 CliShell
<  1269 root      20   0  105504  27944  23592 S   0.0   0.0   0:15.04 LacpTxAgent
<  1270 root      20   0  106100  30736  26148 S   0.0   0.0   0:14.77 McastCommon
<  1271 root      20   0  152712  62676  38520 S   0.0   0.1   6:46.89 SuperServer
<  1272 root      20   0  103908  39060  34320 S   0.0   0.1   0:16.71 Bfd
<  1275 root      20   0   99960  26792  22588 S   0.0   0.0   0:15.11 PortSec
<  1276 root      20   0   32240  11220   9336 S   0.0   0.0   7:19.77 rbfdu
<  1277 root      20   0  110112  40864  35748 S   0.0   0.1   0:14.84 Ira
<  1283 root      20   0  111288  28324  23664 S   0.0   0.0   0:21.97 LedPolicy
<  1284 root      20   0  106968  35512  28140 S   0.0   0.1   0:21.34 EventMgr
<  1285 root      20   0   82600  31992  20152 S   0.0   0.0   0:24.62 CapiApp
<  1286 root      20   0   99260  27312  22964 S   0.0   0.0   1:00.21 StpTxRx
<  1287 root      20   0   40116  10344   7912 S   0.0   0.0   0:11.15 StandbyCpld
<  1288 root      20   0  106900  33304  28588 S   0.0   0.1   0:40.54 Lag
<  1289 root      20   0   59912  16396  13576 S   0.0   0.0   0:12.85 FibServices
<  1290 root      20   0   48680  19112  11240 S   0.0   0.0   4:04.59 PhyEthtool
<  1291 root      20   0   21700   8812   7620 S   0.0   0.0   0:10.97 EventHistoryAge
<  1292 root      20   0  107784  27284  12676 S   0.0   0.0   3:02.70 Aaa
<  1293 root      20   0  101444  26160  21944 S   0.0   0.0   0:13.72 StpTopology
<  1294 root      20   0   59236  22456  17116 S   0.0   0.0   0:16.80 Tunnel
<  1295 root      20   0  163404  49820  42344 S   0.0   0.1   1:18.91 Acl
<  1296 root      20   0   52504  16676  13824 S   0.0   0.0   0:35.94 Stp
<  1297 root      20   0   39064  16608  14376 S   0.0   0.0   0:14.31 KernelNetworkIn
<  1298 root      20   0  105688  26764  22336 S   0.0   0.0   0:16.77 McastCommon6
<  1299 root      20   0  194704  76984  57080 S   0.0   0.1 106:18.62 Etba
<  1300 root      20   0  124460  42948  37196 S   0.0   0.1   0:33.09 Arp
<  1301 root      20   0  100356  33152  28864 S   0.0   0.1   2:57.95 Lldp
<  1302 root      20   0  110212  39908  32228 S   0.0   0.1   0:17.06 KernelFib
<  1304 root      20   0  103772  27968  23428 S   0.0   0.0   0:19.45 Qos
<  1305 root      20   0   39244  11568   9280 S   0.0   0.0   0:13.55 Thermostat
<  1306 root      20   0   45508  18032  15760 S   0.0   0.0   0:15.63 L2Rib
<  1307 root      20   0   99452  26772  22708 S   0.0   0.0   0:11.68 TopoAgent
<  1308 root      20   0   21884   9020   7812 S   0.0   0.0   0:10.80 PowerFuse
<  1309 root      20   0  109096  39928  35068 S   0.0   0.1   0:18.65 Ebra
<  1310 root      20   0   45080  18724  15376 S   0.0   0.0   0:11.67 ReloadCauseAgen
<  1311 root      20   0   23292   8352   7036 S   0.0   0.0   0:11.09 SharedSecretPro
<  1312 root      20   0  121716  37660  26956 S   0.0   0.1   0:27.82 IgmpSnooping
<  1320 root      20   0   38544  11080   3148 S   0.0   0.0   0:04.06 CliShell
<  1352 root      20   0   38544  11088   3152 S   0.0   0.0   0:04.21 CliShell
<  1383 root      20   0   86824  28200  23608 S   0.0   0.0   0:14.11 StaticRoute
<  1384 root      20   0  116236  56616  43236 S   0.0   0.1   0:30.97 IpRib
<  1385 root      20   0  102284  30220  25400 S   0.0   0.0   0:14.22 ConnectedRoute
<  1386 root      20   0   83896  28292  23900 S   0.0   0.0   0:13.93 RouteInput
<  1387 root      20   0  230528  69820  61220 S   0.0   0.1   0:14.93 BgpCliHelper
<  1388 root      20   0  273200 133132 119132 S   0.0   0.2   2:27.38 Bgp-main
<  1414 root      20   0   43644  14644   3192 S   0.0   0.0   0:04.10 CliShell
<  1585 root      20   0   56444  12820   9520 S   0.0   0.0   0:12.51 EvpnrtrEncap
<  1618 root      20   0   95564  22612  16936 S   0.0   0.0   0:34.73 AirStream
---
>  1219 root      20   0   38544   7000   3152 S   0.0   0.0   0:04.26 CliShell
>  1244 root      20   0   38544  11084   3152 S   0.0   0.0   0:04.18 CliShell
>  1269 root      20   0  105504  27944  23592 S   0.0   0.0   0:15.06 LacpTxAgent
>  1270 root      20   0  106100  30736  26148 S   0.0   0.0   0:14.79 McastCommon
>  1271 root      20   0  152712  62684  38520 S   0.0   0.1   6:47.56 SuperServer
>  1272 root      20   0  103908  39060  34320 S   0.0   0.1   0:16.73 Bfd
>  1274 root      20   0   20904   8220   6888 S   0.0   0.0  12:02.65 AgentMonitor
>  1275 root      20   0   99960  26792  22588 S   0.0   0.0   0:15.13 PortSec
>  1276 root      20   0   32240  11220   9336 S   0.0   0.0   7:20.49 rbfdu
>  1277 root      20   0  110112  40864  35748 S   0.0   0.1   0:14.87 Ira
>  1283 root      20   0  111288  28324  23664 S   0.0   0.0   0:21.99 LedPolicy
>  1284 root      20   0  106968  35512  28140 S   0.0   0.1   0:21.39 EventMgr
>  1285 root      20   0   82600  31984  20152 S   0.0   0.0   0:24.92 CapiApp
>  1286 root      20   0   99260  27312  22964 S   0.0   0.0   1:00.31 StpTxRx
>  1287 root      20   0   40116  10344   7912 S   0.0   0.0   0:11.17 StandbyCpld
>  1288 root      20   0  106900  33304  28588 S   0.0   0.1   0:40.60 Lag
>  1289 root      20   0   59912  16396  13576 S   0.0   0.0   0:12.87 FibServices
>  1290 root      20   0   48680  19112  11240 S   0.0   0.0   4:04.99 PhyEthtool
>  1291 root      20   0   21700   8812   7620 S   0.0   0.0   0:10.98 EventHistoryAge
>  1292 root      20   0  107784  27288  12676 S   0.0   0.0   3:06.36 Aaa
>  1293 root      20   0  101444  26160  21944 S   0.0   0.0   0:13.73 StpTopology
>  1294 root      20   0   59236  22456  17116 S   0.0   0.0   0:16.84 Tunnel
>  1295 root      20   0  163404  49820  42344 S   0.0   0.1   1:19.04 Acl
>  1296 root      20   0   52504  16676  13824 S   0.0   0.0   0:36.00 Stp
>  1297 root      20   0   39064  16608  14376 S   0.0   0.0   0:14.34 KernelNetworkIn
>  1298 root      20   0  105688  26764  22336 S   0.0   0.0   0:16.80 McastCommon6
>  1300 root      20   0  124460  42948  37196 S   0.0   0.1   0:33.15 Arp
>  1301 root      20   0  100356  33152  28864 S   0.0   0.1   2:58.24 Lldp
>  1302 root      20   0  110212  39908  32228 S   0.0   0.1   0:17.10 KernelFib
>  1304 root      20   0  103772  27968  23428 S   0.0   0.0   0:19.48 Qos
>  1305 root      20   0   39244  11568   9280 S   0.0   0.0   0:13.57 Thermostat
>  1306 root      20   0   45508  18032  15760 S   0.0   0.0   0:15.66 L2Rib
>  1307 root      20   0   99452  26772  22708 S   0.0   0.0   0:11.69 TopoAgent
>  1308 root      20   0   21884   9020   7812 S   0.0   0.0   0:10.82 PowerFuse
>  1309 root      20   0  109096  39928  35068 S   0.0   0.1   0:18.69 Ebra
>  1310 root      20   0   45080  18724  15376 S   0.0   0.0   0:11.69 ReloadCauseAgen
>  1311 root      20   0   23292   8352   7036 S   0.0   0.0   0:11.11 SharedSecretPro
>  1312 root      20   0  121716  37660  26956 S   0.0   0.1   0:27.86 IgmpSnooping
>  1320 root      20   0   38544  11080   3148 S   0.0   0.0   0:04.07 CliShell
>  1352 root      20   0   38544  11088   3152 S   0.0   0.0   0:04.22 CliShell
>  1383 root      20   0   86824  28200  23608 S   0.0   0.0   0:14.13 StaticRoute
>  1384 root      20   0  116236  56616  43236 S   0.0   0.1   0:31.02 IpRib
>  1385 root      20   0  102284  30220  25400 S   0.0   0.0   0:14.24 ConnectedRoute
>  1386 root      20   0   83896  28292  23900 S   0.0   0.0   0:13.95 RouteInput
>  1387 root      20   0  230528  69820  61220 S   0.0   0.1   0:14.94 BgpCliHelper
>  1388 root      20   0  273200 133128 119132 S   0.0   0.2   2:27.63 Bgp-main
>  1414 root      20   0   43644  14644   3192 S   0.0   0.0   0:04.11 CliShell
>  1585 root      20   0   56444  12820   9520 S   0.0   0.0   0:12.53 EvpnrtrEncap
>  1618 root      20   0   95564  22612  16936 S   0.0   0.0   0:34.79 AirStream
91c90
<  1832 nobody    20   0   14412   4520   3116 S   0.0   0.0   0:05.35 nginx
---
>  1832 nobody    20   0   14412   4520   3116 S   0.0   0.0   0:05.47 nginx
94c93
<  2074 ntp       20   0   14148   3708   2788 S   0.0   0.0   0:14.66 ntpd
---
>  2074 ntp       20   0   14148   3708   2788 S   0.0   0.0   0:14.68 ntpd
97a97
> 12363 admin     20   0    9940   2700   2080 R   0.0   0.0   0:00.04 top
diff -Naar "./test/172.100.100.2-2022-08-30-160819/cli_detail/show uptime" "./test/172.100.100.2-2022-08-30-161108/cli_detail/show uptime"
1c1
<  08:08:22 up 1 day,  5:19,  1 user,  load average: 7.30, 6.66, 6.89
---
>  08:11:12 up 1 day,  5:22,  1 user,  load average: 7.66, 6.91, 6.94
diff -Naar "./test/172.100.100.2-2022-08-30-160819/cli_detail/show version" "./test/172.100.100.2-2022-08-30-161108/cli_detail/show version"
17c17
< Uptime: 1 day, 4 hours and 45 minutes
---
> Uptime: 1 day, 4 hours and 48 minutes
19c19
< Free memory: 52630636 kB
---
> Free memory: 52563264 kB
```
###  eAPI  Unsupported commands

Certain commands are not permitted and will always return an error. The largest class of such commands are interactive commands; “top” and “bash” are prime examples. 
In addition, no abbreviations are allowed in commands. This is necessary because future versions of EOS may add more commands, rendering previous abbreviations ambiguous.
