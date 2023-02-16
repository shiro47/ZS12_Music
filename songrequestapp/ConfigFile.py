import configparser

class SR_config():
    
    def __init__(self) -> None:
        self.config = configparser.ConfigParser()
        self.config.read("config.cfg")
    
    def build_cfg(self):
        with open("config.cfg", 'w') as config_file:
            self.config.add_section("SongRequest")
            self.config.set("SongRequest","request_limit","0")
            self.config.set("SongRequest","request_reset_time_period","0")
            self.config.write(config_file)
        return
    
    def set_requests_limit(self, limit):
        try:
            with open("config.cfg", 'w') as config_file:
                self.config["SongRequest"]["request_limit"]=str(limit)
                self.config.write(config_file)
            return
        except KeyError:
            self.build_cfg()
            return self.set_requests_limit(limit)
        
    def set_request_time_period(self, seconds):
        try:
            with open("config.cfg", 'w') as config_file:
                self.config["SongRequest"]["request_reset_time_period"]=str(seconds)
                self.config.write(config_file)
            return
        except KeyError:
            self.build_cfg()
            return self.set_request_time_period(seconds)
        
    def check_requests_limit(self):
        try:
            return self.config.get("SongRequest","request_limit")
        except configparser.NoSectionError:
            self.build_cfg()
            return self.check_requests_limit()
        
    def check_request_time_period(self):
        try:
            return self.config.get("SongRequest","request_reset_time_period")
        except configparser.NoSectionError:
            self.build_cfg()
            return self.check_request_time_period()
        
        