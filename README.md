## Usage

### Step 1 - Create your inventory.yaml file

This file will be the basis for which PyATS will parse/gather outputs from so that the python script can generate the needed output CSV files.  This example shows two devices (switch1 and switch2) but it can collect as many (or little) as needed.  Note that user/pass can be supplied directly in the file or can be gathered upon execution and not stored in the file.  Just edit/comment/uncomment as required.

```
devices:
  switch1:
    connections:
      cli:
        ip: 10.10.10.10
        protocol: ssh
    os: iosxe
    type: iosxe
  switch2:
    connections:
      cli:
        ip: 10.20.20.83
        protocol: ssh
    os: iosxe
    type: iosxe
testbed:
  credentials:
    default:
      password: 'P@$$worD!'
      username: 'admin'
      #password: '%ASK{}'
      #username: '%ASK{}'
```


### Step 2 - Populate your mapping.yaml file

Fill out the mapping.yaml file with site-specific relavant inputs needed to associate legacy VLANs to new SDA IP Pool names to use for assignments.

```
sites:
  site1:
    devices:
      switch1:
        ip_pools:
          - voicevlan: 100
            voiceippool: SDA-VOICE-Pool
          - vlan2: 10
            ippool2: SDA-Data-10
          - vlan3: 963
            ippool3: SDA-Data-963
	  
```

### Step 3 - Run the script

```
python3 discovery.py site1 switch1
