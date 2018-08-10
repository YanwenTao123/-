import requests
import time
from lxml import etree
from storage import MysqlClient

proxies = {
    "http":"http://122.114.31.177:808",
    "https":"https://122.114.31.177:808",
}
class GetProxy():
    def __init__(self):
        self.proxies = []
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36'
        }
    def get_kuai(self,url):
        response = requests.get(url=url,headers=self.headers).text
        response = etree.HTML(response)
        ip = response.xpath('//table[@class="table table-bordered table-striped"]//td[1]/text()')
        port = response.xpath('//table[@class="table table-bordered table-striped"]//td[2]/text()')
        # print(ip)
        # print(port)
        for i in range(len(ip)):
            proxy = ip[i] + ":" + port[i]
            self.proxies.append(proxy)
        print(self.proxies)
        return self.proxies

    def get_xici(self,url):
        response = requests.get(url=url,headers=self.headers).text
        response = etree.HTML(response)
        ip = response.xpath('//table[@id="ip_list"]//tr/td[2]/text()')
        port = response.xpath('//table[@id="ip_list"]//tr/td[3]/text()')
        for i in range(len(ip)):
            proxy = ip[i] + ":" + port[i]
            self.proxies.append(proxy)
        print(self.proxies)
        return self.proxies

    def get_cool(self,url):
        response = requests.get(url=url,headers=self.headers).text
        response = etree.HTML(response)
        ip = response.xpath('//div[@id="main"]/table//tr/td[1]/text()')
        port = response.xpath('//div[@id="main"]/table//tr/td[2]/text()')
        for i in range(len(ip)):
            proxy = ip[i] + ":" + port[i]
            self.proxies.append(proxy)
        print(self.proxies)
        return self.proxies

    def get_coderbusy(self,url):
        response = requests.get(url=url,headers=self.headers).text
        response = etree.HTML(response)
        ip = response.xpath('//table[@class="table"]/tbody/tr/td[3]/@data-ip')
        port = response.xpath('//table[@class="table"]/tbody/tr/td[3]/@data-i')
        for i in range(len(ip)):
            proxy = ip[i] + ":" + port[i]
            self.proxies.append(proxy)
        print(self.proxies)
        return self.proxies

    def SaveProxy(self,proxies):
        """在写入数据时注意一次写入多条，一并存储，避免一次1条严重影响效率"""
        # print("111")
        for proxy in proxies:
            try:
                MysqlClient().add(proxy)
            except Exception:
                continue
            print("------------------")
        self.proxies = []
        return MysqlClient().all()

    def Count(self):
        return MysqlClient().count()

    def run(self):
        for offset in range(1,3000):
            url_1  = "http://www.xicidaili.com/nn/" + str(offset)
            url_2 = "https://www.kuaidaili.com/free/inha/" + str(offset)
            url_cool = 'https://www.cool-proxy.net/proxies/http_proxy_list/page:'+str(offset) + '/country_code:/port:/anonymous:'
            url_coderbusy = 'https://proxy.coderbusy.com/classical/anonymous-type/highanonymous.aspx?page=' + str(offset)
            # print(url_coderbusy)
            time.sleep(3)
            # 数据库限量存储
            # if MysqlClient().count() > 100:
            #     continue
            proxies_xici = self.get_xici(url_1)
            # proxies_kuai = self.get_kuai(url_2)
            # proxies_cool = self.get_cool(url_cool)
            # proxies_coderbusy = self.get_coderbusy(url_coderbusy)
            # print(proxies_kuai)
            # self.SaveProxy(proxies_kuai)
            self.SaveProxy(proxies_xici)
            # self.SaveProxy(proxies_coderbusy)




def main():
    p = GetProxy()
    p.run()

if __name__ == "__main__":
    main()