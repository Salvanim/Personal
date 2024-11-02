import socket
import netifaces
import ipaddress
from scapy.all import ARP, Ether, srp

def get_local_network():
    # Get all network interfaces
    interfaces = netifaces.interfaces()

    for interface in interfaces:
        # Get the addresses for each interface
        addrs = netifaces.ifaddresses(interface)

        # Check for IPv4 addresses
        if netifaces.AF_INET in addrs:
            ipv4_info = addrs[netifaces.AF_INET][0]
            ip_address = ipv4_info['addr']
            netmask = ipv4_info['netmask']

            # Calculate the network address
            network = ipaddress.ip_network(f"{ip_address}/{netmask}", strict=False)
            return str(network)  # Return the network range
    return None  # If no suitable interface is found

def discover_ips(network):
    # Create an ARP request to discover IPs
    arp = ARP(pdst=network)
    ether = Ether(dst="ff:ff:ff:ff:ff:ff")
    packet = ether / arp

    # Send the packet and capture the responses
    result = srp(packet, timeout=3, verbose=0)[0]

    # Collect and return the IP addresses
    ips = []
    for sent, received in result:
        ips.append(received.psrc)  # Get the IP address of the responding device
    return ips

def reverse_lookup(ip):
    try:
        # Get the host name associated with the IP address
        host_name = socket.gethostbyaddr(ip)[0]
        return host_name
    except socket.herror:
        return None  # Return None if no host is found

if __name__ == "__main__":
    print("Getting local network range...")

    # Get the local network range automatically
    local_network = get_local_network()
    if local_network:
        print(f"Local network range: {local_network}")
    else:
        print("Could not determine local network range.")
        exit(1)

    print("Discovering IP addresses on the network...")

    # Discover IPs
    accessible_ips = discover_ips(local_network)
    print("Accessible IP Addresses:")
    for ip in accessible_ips:
        print(ip)

    print("\nPerforming reverse lookups...")
    for ip in accessible_ips:
        host_name = reverse_lookup(ip)
        if host_name:
            print(f"{ip} -> {host_name}")
        else:
            print(f"{ip} -> No host found")

