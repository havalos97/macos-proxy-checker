import datetime
import subprocess
import sys


def check_proxy() -> None:
    if are_proxy_bypass_domains_set() or is_auto_proxy_state_on():
        write_log("Proxy is enabled, disabling it...")
        disable_proxy_state()
    else:
        write_log("Proxy is already disabled.")


def write_log(message: str) -> None:
    print(f"{timestamp()} ---- {message}")


def disable_proxy_state() -> bool:
    result_wifi_proxy_disabler = run_sp(
        "sudo /Users/ksfw694/proxy_checker/wifi_proxy_disabler.sh",
    )

    if result_wifi_proxy_disabler[0] == "":
        write_log("Proxy state is now disabled.")
    return result_wifi_proxy_disabler[0] == ""


def run_sp(bash_command: str) -> list[str]:
    write_log(f"Running command: {bash_command}")
    response = subprocess.run(
        bash_command.split(' '),
        capture_output=True,
    )
    result = response.stdout.decode("utf-8").strip()
    return result.split("\n")


def are_proxy_bypass_domains_set() -> bool:
    proxy_bypass_domains = run_sp(
        "/usr/sbin/networksetup -getproxybypassdomains Wi-Fi"
    )
    write_log(f"'{proxy_bypass_domains[0]}' == '{sys.argv[1]}' ?")
    return proxy_bypass_domains[0] == sys.argv[1]


def is_auto_proxy_state_on() -> bool:
    _, enabled = run_sp("/usr/sbin/networksetup -getautoproxyurl Wi-Fi")
    write_log(f"'{enabled}' == '{sys.argv[2]}' ?")
    return enabled == sys.argv[2]


def timestamp() -> str:
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


if __name__ == "__main__":
    check_proxy()
