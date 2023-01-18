from resource import _read_all_resources

w, h = 500, 500
menu_h = 30
FONT = 15

RESOURCES_FOR_SAFE_PLANETS, \
    RESOURCES_FOR_MIDDLE_PLANETS, \
    RESOURCES_FOR_DANGEROUS_PLANETS = _read_all_resources()

n_planet = [1]
