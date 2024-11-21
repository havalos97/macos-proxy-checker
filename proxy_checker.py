import datetime
import subprocess
import sys
import shlex


def check_proxy() -> None:
    network_devices = list_all_network_services()
    for device_name in network_devices:
        if is_proxy_bypass_domains_set(device_name) or is_auto_proxy_state_on(device_name):
            disable_proxy_state(device_name)
        else:
            write_log(f"Proxy for device {device_name} is already disabled.")


def write_log(message: str) -> None:
    print(f"{timestamp()} ---- {message}")


def disable_proxy_state(device: str) -> bool:
    print(f"Disabling proxy state for device: {device}")
    result_wifi_proxy_disabler = run_sp(
        f"sudo /Users/ksfw694/proxy_checker/proxy_disabler.sh \"{device}\"",
    )

    if result_wifi_proxy_disabler[0] == "":
        write_log("Proxy state is now disabled.")
    return result_wifi_proxy_disabler[0] == ""


def run_sp(bash_command: str) -> list[str]:
    write_log(f"Running command: {bash_command}")
    response = subprocess.run(
        shlex.split(bash_command),
        capture_output=True,
    )
    result = response.stdout.decode("utf-8").strip()
    return result.split("\n")


def is_proxy_bypass_domains_set(device: str) -> bool:
    proxy_bypass_domains = run_sp(
        f"/usr/sbin/networksetup -getproxybypassdomains \"{device}\""
    )
    eval_result = proxy_bypass_domains[0] == sys.argv[1]
    write_log(f"'{proxy_bypass_domains[0]}' == '{sys.argv[1]}' ? => {eval_result}")
    return eval_result


def is_auto_proxy_state_on(device: str) -> bool:
    _, enabled = run_sp(f"/usr/sbin/networksetup -getautoproxyurl \"{device}\"")
    eval_result = enabled == sys.argv[2]
    write_log(f"'{enabled}' == '{sys.argv[2]}' ? => {eval_result}")
    return eval_result


def list_all_network_services() -> None:
    result = run_sp("/usr/sbin/networksetup -listallnetworkservices")
    return result[1:]


def timestamp() -> str:
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


if __name__ == "__main__":
    check_proxy()
