try:
    import sys
    from vpython import *
    from planet import Planet
    from satellite import Satellite
    from star import Star
except ImportError as error:
    print("Error during loading module. {}".format(error))
    sys.exit(2)


def start_flag_button(b):
    global start_flag
    start_flag = not start_flag
    if start_flag:
        b.text = "Pause"
    else:
        b.text = "<b>START</b>"


def time_scale_menu(m):
    global time_scale
    if m.selected == '1s = 1h':
        time_scale = 3600
    elif m.selected == '1s = 24h':
        time_scale = 3600 * 24
    elif m.selected == '1s = 30days':
        time_scale = 3600 * 24 * 30
    elif m.selected == '1s = 90days':
        time_scale = 3600 * 24 * 30 * 3


def camera_menu(m):
    if m.selected in solar_system:
        scene.camera.follow(solar_system[m.selected].obj)


def trail_flag_button(b):
    global trail_flag
    trail_flag = not trail_flag
    if trail_flag:
        b.text = "trail is on"
    else:
        b.text = "trail is off"


if __name__ == '__main__':
    PLANET_SCALE = 0.0001  # 0.0001
    DISTANCE_SCALE = 0.0000002  # 0.0000002
    SUN_SCALE = 0.1 * PLANET_SCALE  # 0.1
    REFRESH_RATE = 120
    time_scale = 1 * 3600
    start_flag = False
    trail_flag = False

    scene = canvas(width=1400, height=900)
    scene.title = int(0.1 * scene.width) * ' ' + 'Solar System\n',
    scene.ambient = color.gray(0.7)
    scene.autoscale = False
    scene.lights = []

    sun = Star(1392000, 27 * 24, 'textures/sunmap.jpg', 333000, time_scale, REFRESH_RATE, SUN_SCALE)
    mercury = Planet(4879, 57910000, 58.65 * 24, 87.969, 'textures/mercurymap.jpg', 0.0552, sun, PLANET_SCALE,
                     DISTANCE_SCALE, time_scale,
                     REFRESH_RATE, 47.9)
    venus = Planet(12100, 108200000, 243 * 24, 224.7, 'textures/venusmap.jpg', 0.8149, sun, PLANET_SCALE,
                   DISTANCE_SCALE,
                   time_scale,
                   REFRESH_RATE, 35)
    earth = Planet(12740, 149600000, 23.93, 365.25, 'textures/earthmap1k.jpg', 1, sun, PLANET_SCALE, DISTANCE_SCALE,
                   time_scale,
                   REFRESH_RATE, 30)
    moon = Satellite(3476, 380000, 27.3 * 24, 27.3, 'textures/moonmap4k.jpg', 0.1, earth)
    mars = Planet(6779, 227900000, 24.62, 686.738, 'textures/mars_1k_color.jpg', 0.1074, sun, PLANET_SCALE,
                  DISTANCE_SCALE,
                  time_scale,
                  REFRESH_RATE, 24.1)
    jupiter = Planet(139800, 778600000, 9.8, 11 * 365.25 + 315, 'textures/jupitermap.jpg', 317.8, sun, PLANET_SCALE,
                     DISTANCE_SCALE,
                     time_scale, REFRESH_RATE, 13.1)
    saturn = Planet(116500, 1433000000, 10.23, 29 * 365.25 + 167, 'textures/saturnmap.jpg', 95.1620, sun, PLANET_SCALE,
                    DISTANCE_SCALE,
                    time_scale, REFRESH_RATE, 9.7)
    uranus = Planet(50720, 2877000000, 10.82, 84.014 * 365.25, 'textures/uranusmap.jpg', 14.5360, sun, PLANET_SCALE,
                    DISTANCE_SCALE,
                    time_scale, REFRESH_RATE, 6.8)
    neptune = Planet(49250, 4503000000, 15.67, 167.78 * 365.25, 'textures/neptunemap.jpg', 17.1470, sun, PLANET_SCALE,
                     DISTANCE_SCALE,
                     time_scale, REFRESH_RATE, 5.4)

    solar_system = {'sun': sun, 'mercury': mercury, 'venus': venus, 'earth': earth, 'moon': moon, 'mars': mars,
                    'jupiter': jupiter, 'saturn': saturn, 'uranus': uranus, 'neptune': neptune}

    button(text='<b>START</b>', pos=scene.title_anchor, bind=start_flag_button)
    scene.caption = ''
    menu(choices=['1s = 1h', '1s = 24h', '1s = 30days', '1s = 90days'], bind=time_scale_menu, pos=scene.title_anchor)
    menu(choices=list(solar_system.keys()), bind=camera_menu, pos=scene.title_anchor)
    button(text='trail', pos=scene.title_anchor, bind=trail_flag_button)

    for obj in list(solar_system.values()):
        if type(obj) == Star:
            obj.light_on()

    while True:
        rate(REFRESH_RATE)
        for obj in list(solar_system.values()):
            obj.update(time_scale)
            if start_flag:
                obj.rotate_axis()
                if type(obj) == Planet:
                    if trail_flag:
                        obj.trail(0)
                    else:
                        obj.clear_trail()
                if type(obj) != Star:
                    obj.rotate_orbit()