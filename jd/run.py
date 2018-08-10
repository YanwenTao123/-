import pstats
from cProfile import Profile
from scrapy import cmdline


def run():
    # cmdline.execute('scrapy crawl jdSpider'.split())
    cmdline.execute('scrapy crawl HwDetailSpider'.split())

if __name__ == "__main__":
    # prof = Profile()
    # prof.enable()
    run()
    # prof.create_stats()
    # p = pstats.Stats(prof)
    # p.print_callees()
