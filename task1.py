from ipaddress import ip_address
from subprocess import Popen, PIPE
import platform
import chardet


def host_ping(ip_addresses: list = None, pockets=4, show_info=False, show_console_info=False):
    param = "-n" if platform.system().lower() == "windows" else "-c"
    base_command = f"ping {param} {pockets} "
    output = []
    # print(f"console command: {base_command}\n")
    if ip_addresses is not None and isinstance(ip_addresses, list):
        for ip in ip_addresses:
            if not isinstance(ip, ip_address.__class__):
                try:
                    ip = ip_address(ip)
                except ValueError:
                    print("using DNS name")
                finally:
                    command = f"{base_command} {ip}"
            else:
                command = f"{base_command} {ip}"

            print(f"checking ip address {ip} ...")
            process = Popen(command, stdout=PIPE)
            process.wait()
            bytes_info = process.stdout.read()
            command_info = bytes_info.decode(chardet.detect(bytes_info).get("encoding"))
            result = int(process.returncode)

            if show_console_info:
                print(command_info)

            if result == 0:
                result_info = "Узел доступен"
            else:
                result_info = "Узел недоступен"

            if show_info:
                print(result_info)
                print()

            output.append((ip, result_info))
    else:
        print("Wrong input data")

    return output


if __name__ == "__main__":
    test_ip = ip_address("192.168.10.100")
    test_addresses = [test_ip + i for i in range(0, 3)]
    info = ["yandex.ru", "google.com", "mail.ru", "localhost", "github.com"]
    info += test_addresses
    host_ping(info, pockets=2)
