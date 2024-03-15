from yaml import load, dump
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper
    
class Configuration:
    def __init__(self, filepath):
        self.cfg = load(open(filepath), Loader)
        self._urls = []
        self._source_map = []

        sources_in_cfg = self.cfg["sources"]
        for index, s in enumerate(sources_in_cfg):
            self._urls.append(s["url"])
            self._source_map.append(index)

    def urls(self):
        return self._urls

    def get_source_by_index(self, index):
        # get a source object
        sources_in_cfg = self.cfg["sources"]
        index_to_cfg = self._source_map[index]
        return sources_in_cfg[index_to_cfg]

    def report_url(self):
        return self.cfg["report-url"]
