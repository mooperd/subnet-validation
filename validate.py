import ipaddress
import itertools
import json

def open_file():
    with open("data.json", "r") as network_file:
        return json.load(network_file)

def load_network(networks, recurse, parent='0.0.0.0/0'):
    recurse += 4
    parent_ = ipaddress.ip_network(parent)
    subnets = list(map(lambda x: ipaddress.ip_network(x['cidr']), networks))
    for subnet_a, subnet_b in itertools.combinations(subnets, 2):
        if subnet_a.overlaps(subnet_b):
            print("Fail " + subnet_a.exploded + " overlaps sibling " + subnet_b.exploded + " " + str
                (subnet_a.overlaps(subnet_b)))
        if not subnet_a.overlaps(parent_):
            print("Fail " + subnet_a.exploded + "is not within parent " + parent_.exploded + " " + str
                (subnet_a.overlaps(parent_)))
    for network_dict in networks:
        if network_dict['cidr'] == parent_.exploded:
            print("Fail " + network_dict['cidr'] + " is same as parent " + parent_.exploded )
        x = ' '
        print(recurse*x+network_dict['name']+" "+network_dict['cidr'])
        load_network(network_dict['subnets'], recurse, network_dict['cidr'])

if __name__ == '__main__':
    recurse = 0
    json_data = open_file()
    foo = load_network(json_data, recurse)
