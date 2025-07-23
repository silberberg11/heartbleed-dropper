## Heartbleed Dropper
An advanced Golang cross compiler designed for red-teaming.

## Order of action
- User inputs path of Golang script and C2 IPv4
- Heartbleed dropper compiles a binary for each platform
- Heartbleed dropper generates a payload for all of the binaries
- Payloads generated ! You're ready to go ...

## Devices supported
This dropper is very supportive and is designed for a range of systems:
['windows/386', 'darwin/amd64', 'linux/amd64', 'linux/386', 'linux/arm', 'freebsd/amd64', 'freebsd/386', 'windows/amd64',
'linux/arm64', 'linux/arm/5', 'linux/arm/7', 'linux/mips', 'linux/mips64', 'linux/mips64le', 'linux/mipsle', 'linux/ppc64']

## Legal Notice
Unauthorized use of this tool on live systems is illegal.  
The author assumes **no responsibility for misuse**. Use responsibly and within the bounds of cybersecurity education.
