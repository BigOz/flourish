S_HOME = [1214, 1185, 1155, 1185, 1214, 1244, 1274, 1303, 1274, 1244, 1214, 1185, 1155, 1126, 1096, 1155, 1214, 1274, 1303, 1363, 1422, 1333, 1274, 1214]
N_HOME = [1037, 948, 889, 859, 859, 918, 978, 1037, 1066, 1096, 1126, 1155, 1185, 1214, 1244, 1303, 1481, 1600, 1807, 1837, 1777, 1570, 1422, 1214]

class HomeProfile:
    def __init__(self):
        pass

    def get_usage(self, smart_home):
        if smart_home:
            return S_HOME
        else:
            return N_HOME

# average home use assumed at 10,812 kWh annually, divided by 365 to get daily
# usage, as taken from https://www.eia.gov/tools/faqs/faq.php?id=97&t=3
#
# Energy archetypes taken from charts "steady eddies" (for smart home use) and
# "evening peakers" (for typical home use) Typical home use quoted at ~40% of
# all homes, while smart home quoted at ~30% The goal is to make all homes the
# "smart home" type, regardless of actual usage
# Taken from http://beccconferenceorg/wp-content/uploads/2016/10/Frades_presentationpdf
# Interestingly, there are 3 additional profiles available, which might
# actually be 'better', depending on what goal a smart home actually has