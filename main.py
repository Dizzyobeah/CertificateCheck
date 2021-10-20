from urllib.request import ssl, socket
import csv
import datetime

            
class CertificateCheck:
    def __init__(self) -> None:
        pass

    def read_csv_file(self, site_file):
        with open(site_file, "r") as file:
            file_reader = csv.DictReader(file)
            sites = list(file_reader)
            # file.close()
            return sites

    def validate_certificates(self, sites):
            for site in sites:
                host = site['Site']
                port = '443'

                try:
                    context = ssl.create_default_context()
                    with socket.create_connection((host, port)) as sock:
                        with context.wrap_socket(sock, server_hostname = host) as ssock:
                            certificate = ssock.getpeercert()
                            certExpires = datetime.datetime.strptime(certificate['notAfter'], '%b %d %H:%M:%S %Y %Z')
                            daysToExpire = (certExpires - datetime.datetime.now()).days

                    if daysToExpire == 30 or daysToExpire == 14 or daysToExpire == 7:
                        print(f"Warning certificate {host} is about to expire in {daysToExpire}")
                    else:
                        print(f"{host} has {daysToExpire} remaining before expiration.")
                except TimeoutError as err:
                    print(f"{host} did not reply {err}")
                    pass

if __name__ == '__main__':

    cc = CertificateCheck()
    sites = cc.read_csv_file("sites.csv")
    cc.validate_certificates(sites)
