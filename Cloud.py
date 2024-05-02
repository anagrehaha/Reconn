import requests
import re

class Azure:
    def __init__(self):
        self.perm_file = r"C:\Users\user\OneDrive\Desktop\python files\day4\perm.txt"

    def perm(self):
        domain = input("please enter the domain for Azure: ").split(".")[0]
        with open('storage.txt', 'w', encoding='utf-8') as f:
            pass
        with open('storage.txt', 'a', encoding='utf-8') as f:
            f.write(str(domain)+'\n')
            words = open(self.perm_file).read().splitlines()
            for w in words:
                f.write(str(domain) + w + '\n')
                f.write(w + str(domain) + '\n')
                f.write(w + str(domain) + w + '\n')
                f.write(w + w + str(domain) + '\n')
                f.write(str(domain) + w + w + '\n')

    def test_storage(self):
        with open('storage.txt', 'r', encoding='utf-8') as fs:
            storage = fs.read().splitlines()
        with open('validstorage.txt', 'w', encoding='utf-8') as fs:
            pass
        with open('validstorage.txt', 'a', encoding='utf-8') as fs:
            for s in storage:
                url_s = f"https://{s}.blob.core.windows.net"
                try:
                    requests.get(url_s)
                    print(url_s)
                    fs.write(url_s + '\n')
                except requests.ConnectionError:
                    continue
        print("----------testing containers----------")
        with open('containers.txt', 'r', encoding='utf-8') as fc:
            containers = fc.read().splitlines()
        with open('validcontainers.txt', 'w', encoding='utf-8') as fc:
            pass
        with open('xmlurls.txt', 'w', encoding='utf-8') as fx:
            pass
        with open('xmlurls.txt', 'a', encoding='utf-8') as fx:
            for v in storage:
                print("Storage:", v)
                for c in containers:
                    try:
                        url_c = f"https://{v}/{c}?restype=container&comp=list"
                        print("testing:", url_c)
                        response = requests.get(url_c)
                        if response.status_code == 200:
                            print("Container found:", url_c)
                            with open('validcontainers.txt', 'a', encoding='utf-8') as fc:
                                fc.write(url_c + '\n')
                            xml_url = re.findall(r'<Url\s*>(.*?)</Url\s*>', response.text)
                            print("urls in xml:")
                            print(xml_url)
                            for x in xml_url:
                                fx.write("Urls found in container: " + url_c + "/" + x + '\n')
                    except requests.ConnectionError:
                        continue

class AWS:
    def __init__(self):
        self.perm_file = r"C:\Users\user\OneDrive\Desktop\python files\day4\perm.txt"

    def perm(self):
        domain = input("please enter the domain for AWS: ").split(".")[0]
        with open('aws.txt', 'w', encoding='utf-8') as f:
            pass
        with open('aws.txt', 'a', encoding='utf-8') as f:
            f.write(str(domain)+'\n')
            words = open(self.perm_file).read().splitlines()
            for w in words:
                f.write(str(domain) + w + '\n')
                f.write(w + str(domain) + '\n')
                f.write(w + str(domain) + w + '\n')
                f.write(w + w + str(domain) + '\n')
                f.write(str(domain) + w + w + '\n')

    def test_aws(self):
        awsstorage = open('aws.txt', 'r', encoding='utf-8').read().splitlines()
        with open('validaws.txt', 'w', encoding='utf-8') as fa, open('validaaaaa.txt', 'w', encoding='utf-8') as fw:
            pass
        with open('validaws.txt', 'a', encoding='utf-8') as fa, open('validaaaaa.txt', 'a', encoding='utf-8') as fw:
            for a in awsstorage:
                url_a = f"https://{a}.s3.amazonaws.com"
                try:
                    response2 = requests.get(url_a)
                    print("testing:", url_a)
                    print(response2.status_code)
                    if response2.status_code == 200:
                        print("Public Bucket found:", url_a)
                        fa.write("Public Bucket found with status code 200:" + url_a + '\n')
                        aws_url = re.findall(r'<Key\s*>(.*?)</Key\s*>', response2.text)
                        for w in aws_url:
                            fw.write("Urls found in container: " + url_a + "/" + w + '\n')
                    elif response2.status_code == 403:
                        print("Protected Bucket found with status code 403:", url_a)
                    elif response2.status_code == 404:
                        print("Bucket not found with status code 404:", url_a)
                except requests.ConnectionError:
                    continue

class GCP:
    def __init__(self):
        self.perm_file = r"C:\Users\user\OneDrive\Desktop\python files\day4\perm.txt"

    def perm(self):
        domain = input("please enter the domain for GCP: ").split(".")[0]
        with open('gcp.txt', 'w', encoding='utf-8') as f:
            pass
        with open('gcp.txt', 'a', encoding='utf-8') as f:
            f.write(str(domain)+'\n')
            words = open(self.perm_file).read().splitlines()
            for w in words:
                f.write(str(domain) + w + '\n')
                f.write(str(domain) + '-' + w + '\n')
                f.write(w + '-' + str(domain) + '\n')
                f.write(w + str(domain) + '\n')
                f.write(w + str(domain) + w + '\n')
                f.write(w + w + str(domain) + '\n')
                f.write(str(domain) + w + w + '\n')

    def test_gcp(self):
        gcpstorage = open('gcp.txt', 'r', encoding='utf-8').read().splitlines()
        with open('validgcp.txt', 'w', encoding='utf-8') as fa, open('validbucket.txt', 'w', encoding='utf-8') as fw:
            pass
        with open('validgcp.txt', 'a', encoding='utf-8') as fa, open('validbucket.txt', 'a', encoding='utf-8') as fw:
            for g in gcpstorage:
                url_g = f"https://storage.googleapis.com/{g}"
                try:
                    response2 = requests.get(url_g)
                    print("testing:", url_g)
                    print(response2.status_code)
                    if response2.status_code == 200:
                        print("Public Bucket found:", url_g)
                        fa.write("Public Bucket found with status code 200:" + url_g + '\n')
                        aws_url = re.findall(r'<Key\s*>(.*?)</Key\s*>', response2.text)
                        for w in aws_url:
                            fw.write("Urls found in container: " + url_g + "/" + w + '\n')
                    elif response2.status_code == 403:
                        print("Protected Bucket found with status code 403:", url_g)
                    elif response2.status_code == 404:
                        print("Bucket not found with status code 404:", url_g)
                except requests.ConnectionError:
                    continue

def main():
    a = Azure()
    a.perm()
    a.test_storage()

    b = AWS()
    b.perm()
    b.test_aws()

    g = GCP()
    g.perm()
    g.test_gcp()

if __name__ == "__main__":
    main()
