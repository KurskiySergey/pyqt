from tabulate import tabulate
from ipaddress import ip_interface
import urllib3
import socket
from task2 import host_range_ping
ENCODING = "UTF-8"


def host_range_tab_ping(ip_address_range_list=None, pockets=1, show_table_info=True, sort_by_result=True):
    if ip_address_range_list is None:
        ip_address_range_list = ["192.168.0.0/30"]
    list_result = []
    for ip_address_range in ip_address_range_list:
        result = host_range_ping(
            ip_address_range=ip_address_range,
            pockets=pockets,
            show_result_info=False
        )
        list_result += result

    if show_table_info:
        if sort_by_result:
            dict_result = {"Узел недоступен": [],
                           "Узел доступен": []}
            for line_result in list_result:
                dict_result.get(line_result[1]).append(line_result[0])
            tab_info = tabulate(dict_result, headers="keys", tablefmt="grid")
            print(tab_info)
        else:
            headers = ("IP", "RESULT")
            tab_info = tabulate(list_result, headers=headers, tablefmt="grid")
            print(tab_info)

    return list_result


def find_user_ip_network(is_public=False, mask_prefix="24"):
    if is_public:
        url_name = "ifconfig.me/ip"
        http = urllib3.PoolManager()
        request = http.request("GET", url_name)
        response = request.data
        user_ip = response.decode(ENCODING)
        http.clear()
    else:
        user_ip = socket.gethostbyname(socket.gethostname())

    ip_int = ip_interface(f"{user_ip}/{mask_prefix}")

    return ip_int.network


if __name__ == "__main__":
    user_ip_net_list = []
    user_ip_net = find_user_ip_network(is_public=True, mask_prefix='30')
    print(f"user ip public network: {user_ip_net}")
    user_ip_net_list.append(str(user_ip_net))

    user_ip_net = find_user_ip_network(is_public=False, mask_prefix='30')
    print(f"user ip local network: {user_ip_net}")
    user_ip_net_list.append(str(user_ip_net))
    print(user_ip_net_list)

    host_range_tab_ping(user_ip_net_list,
                        pockets=1,
                        show_table_info=True,
                        sort_by_result=False)
    print()
    host_range_tab_ping(user_ip_net_list,
                        pockets=1,
                        show_table_info=True,
                        sort_by_result=True)
