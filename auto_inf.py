import argparse
import subprocess

def amass_enumeration(domains):

    subdomains = set()
    for domain in domains:
        cmd = f"amass enum -d {domain}"
        output = subprocess.check_output(cmd.split()).decode()
        subdomains.update(output.strip().split('\n'))
    return subdomains

def scan_subdomains(subdomains, output_file=None):

    choice = input("Do you want to scan the enumerated subdomains? (y/n): ").lower()
    if choice == 'y':
        selection = input("Select a scan type:\n1) Basic Scan (-sS)\n2) TCP Scan with version detection (-sTV)\n3) OS Detection (-A)\nSelection: ")
        if selection == '1':
            cmd = f"nmap -sS {' '.join(subdomains)}"
        elif selection == '2':
            cmd = f"nmap -sTV {' '.join(subdomains)}"
        elif selection == '3':
            cmd = f"nmap -A {' '.join(subdomains)}"
        else:
            print("Invalid selection")
            return
        output = subprocess.check_output(cmd.split()).decode()
        print(output)
        if output_file:
            with open(output_file, 'w') as f:
                f.write(output)

def main():
    parser = argparse.ArgumentParser(description='Amass subdomain enumeration and nmap scanning script')
    parser.add_argument('-d', '--domains', nargs='+', help='list of domains to enumerate subdomains for')
    parser.add_argument('-f', '--file', help='file containing domains to enumerate subdomains for')
    parser.add_argument('-o', '--output', help='file to write output to')
    args = parser.parse_args()

    if args.domains:
        domains = set(args.domains)
    elif args.file:
        with open(args.file, 'r') as f:
            domains = set(f.read().strip().split('\n'))
    else:
        parser.print_help()
        return

    subdomains = amass_enumeration(domains)
    print(subdomains)
    scan_subdomains(subdomains, args.output)

if __name__ == '__main__':
    main()
