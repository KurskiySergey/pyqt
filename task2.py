from task1 import host_ping
from ipaddress import ip_network
from pprint import pprint


def host_range_ping(ip_address_range="192.168.0.0/30", pockets=1, show_result_info=True):
    if not isinstance(ip_address_range, ip_network.__class__):
        ip = ip_network(ip_address_range)
    else:
        ip = ip_address_range
    ip_list = list(ip.hosts())
    # print("checking ip range...\n")
    result = host_ping(
        ip_addresses=ip_list,
        pockets=pockets,
        show_info=False,
        show_console_info=False
    )
    if show_result_info:
        print()
        pprint(result)
        success_result = sum(0 if info[1] == "Узел недоступен" else 1 for info in result)
        error_result = len(result) - success_result
        total_result = f"succsess: {success_result}\nerror: {error_result}\n"
        print(total_result)

    return result


if __name__ == "__main__":

    host_range_ping(
        pockets=1,
        show_result_info=True
    )
