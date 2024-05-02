import json
import re
import requests
import socket
import whois

class RapidDNS:
    def __init__(self, domain):
        self.domain = domain
        self.subdomains = set()

    def fetch_subdomains(self):
        try:
            response = requests.get(f"https://rapiddns.io/subdomain/{self.domain}?full=1")
            if response.status_code == 200:
                content = response.text
                matches = re.findall(r'<td class="col-md-4">(.*?)</td>', content)
                for match in matches:
                    subdomain = match.strip().lower()
                    if subdomain:
                        self.subdomains.add(subdomain)
        except requests.RequestException as e:
            print(f"Error fetching subdomains from RapidDNS: {e}")

class CrtSH:
    def __init__(self, domain):
        self.domain = domain
        self.subdomains = set()

    def fetch_subdomains(self):
        try:
            response = requests.get(f"https://crt.sh/?q=%.{self.domain}&output=json")
            if response.status_code == 200:
                content = response.text
                json_data = json.loads(content)
                for entry in json_data:
                    subdomain = entry['name_value'].strip().lower()
                    if subdomain.startswith("*."):
                        subdomain = subdomain[2:]
                    self.subdomains.add(subdomain)
        except requests.RequestException as e:
            print(f"Error fetching subdomains from crt.sh: {e}")

    def fetch_subdomains_json(self):
        try:
            response = requests.get(f"https://crt.sh/?q={self.domain}&output=json")
            if response.status_code == 200:
                json_data = response.json()
                for entry in json_data:
                    subdomain = entry['name_value'].strip().lower()
                    if subdomain.startswith("*."):
                        subdomain = subdomain[2:]
                    self.subdomains.add(subdomain)
        except requests.RequestException as e:
            print(f"Error fetching subdomains from crt.sh: {e}")

class SubdomainEnumerator:
    def __init__(self, domain):
        self.domain = domain
        self.rapiddns = RapidDNS(domain)
        self.crtsh = CrtSH(domain)
        self.resolvable_subdomains = []

    def is_resolvable(self, subdomain):
        try:
            socket.gethostbyname(subdomain)
            return True
        except socket.error:
            return False

    def fetch_subdomains(self):
        self.rapiddns.fetch_subdomains()
        self.crtsh.fetch_subdomains_json()  

        subdomains = self.rapiddns.subdomains.union(self.crtsh.subdomains)

        for subdomain in subdomains:
            if self.is_resolvable(subdomain):
                self.resolvable_subdomains.append(subdomain)

    def print_subdomains(self):
        print("\nResolvable Subdomains:")
        for subdomain in self.resolvable_subdomains:
            print(f"\033[91m{subdomain}\033[0m") 

    def whois_info(self):
        try:
            w = whois.whois(self.domain)        
            print("Domain Name:", w.domain_name)
            print("Registrar:", w.registrar)
            print("Creation Date:", w.creation_date)
            print("Expiration Date:", w.expiration_date)
            print("Registrant:", w.registrant)
            print("Contact Email:", w.emails)
            print("Name Servers:", w.name_servers)

        except Exception as e:
            print("Error: ", e)

def main():
    print("If you want to run the whois code you should run the powershell as admin")
    domain = input("Enter the domain name: ")
    enumerator = SubdomainEnumerator(domain)
    enumerator.fetch_subdomains()
    enumerator.print_subdomains()
    
    print("############################ WHOIS INFO OUTPUT ##############################")
    
    enumerator.whois_info()

if __name__ == "__main__":
    main()
