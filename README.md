# Cheapseats Utilities
This repository contains some simple tools and utilities that can be used by other CheapSeats stacks to solve a variety of different problems. At the moment, it's quite modest but will likely grow with time.

## Macros

### NetworkInfo
This macro takes a parameter (either CIDR or CIDR-export) that provides a network range in CIDR format.
**CIDR**: A network CIDR range
**CIDR-export**: The name of a Cloudformation Stack Export that contains a CIDR range
The CIDR range is processed and returned as a JSON fragment containing both the CIDR range and the equivalent subnet & netmask.
```
{
    'CIDR' : <CIDR Range>
    'ip-range' : <Subnet IP Range>
    'netmask' : <Subnet Netmask>
}
```

The primary use-case here is to feed this as parameters into a Mustache template for configuration files that may require different IP formats.