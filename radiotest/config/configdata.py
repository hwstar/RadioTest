import configparser

CD_FILT_AWG = "AWG"
CD_FILT_SA = "SA"

class ConfigData():
    def __init__(self, config_file):
        self.config_file = config_file
        self.instruments = [
            {"name": "AWG1","cd_filter": CD_FILT_AWG, "instrument": {"i_type": "Arbitrary Waveform Generator", "driver": "sdg1032x",
             "class_name":"Sdg1032x", "interface": "vxi", "hostname": "SDG-1032X"}},
            {"name": "SA1", "cd_filter": CD_FILT_SA, "instrument": {"i_type": "Spectrum Analyzer", "driver": "dsa815",
             "class_name": "Dsa815", "interface": "vxi", "hostname": "DSA-815"}}
        ]

    def get_instruments_of_type(self, cd_filter):
        """ Return a dictionary of instruments which match the filter specified"""
        res = None
        for instrument in self.instruments:
            if cd_filter == instrument["cd_filter"]:
                if res is None:
                    res = dict()
                res[instrument["name"]] = instrument["instrument"]
        return res

    def get_instrument_names_of_type(self, cd_filter):
        """ Return just the instrument names which match the filter"""
        res = []
        instruments = self.get_instruments_of_type(cd_filter)
        if instruments is None:
            return res
        for instrument in instruments.keys():
            res.append(instrument)
        return res


    def get_instrument_list(self):
        """ Return the complete list of instruments"""
        return self.instruments


