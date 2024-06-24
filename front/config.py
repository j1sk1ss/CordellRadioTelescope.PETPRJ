import pickle

from driver.driver import Driver


rtl_driver = Driver()
stm32_driver = Driver()
nema17_driver = Driver()

antenna_radius = 0


def save():
    data4save = {
        'rtl_driver': rtl_driver,
        'stm32_driver': stm32_driver,
        'nema17_driver': nema17_driver,
        'antenna_radius': antenna_radius
    }

    with open('config.pickle', 'wb') as handle:
        pickle.dump(data4save, handle, protocol=pickle.HIGHEST_PROTOCOL)


def load():
    with open('config.pickle', 'rb') as handle:
        loaded = pickle.load(handle)

    global rtl_driver, stm32_driver, nema17_driver, antenna_radius

    rtl_driver = loaded['rtl_driver']
    stm32_driver = loaded['stm32_driver']
    nema17_driver = loaded['nema17_driver']
    antenna_radius = loaded['antenna_radius']
