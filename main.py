from visual import *
from visual.graph import *
scene = display(width=1200, height=700,center=(0,5,0))

earthmass = 5.972 * 10**24 
sunmass = 1.989 * 10**30 
moonmass = 7.34767309 * 10**22

earth_iv = vector(0,0,30000)
moon_iv = vector(0,1023,30000)
sun_iv = vector(0,0,0)

earthradius = 6371000
sunradius = 695700000
moonradius = 1737000

pi = 3.141592654
eath_sun_dis = 149.6 * 10**9
eath_moon_dis = 370300000
earth_ang_speed = 2*pi/24/3600
earth_rot_axis = vector(0,1,0.1)
G = 6.67 * 10**(-11)
dt = 100000
bodies = []
scene.lights = color.gray(0.1)
local_light(pos=(0,0,0), color=color.white, ambient = color.white)
#scene.ambient = 0
def init_bodies():
    global bodies
    
    sun = body(name='Sun',pos=vector(0,0,0), radius=sunradius, vel = sun_iv, mass = sunmass, Color=color.yellow, material = materials.emissive)

    mercury = body(name='Mercury',pos=vector(-57909050000,0,0), radius=0.3829*earthradius, vel = vector(0,0,47362), mass = 3.3011*10**23 , Color=color.white,retain = .1)

    venus = body(name='Venus',pos=vector(-108939000000,0,0), radius=0.9499*earthradius, vel = vector(0,0,35020), mass = 4.867*10**24, retain=0.3)

    earth = body(name='Earth',pos=vector(-eath_sun_dis,0,0), radius=earthradius, vel = earth_iv, mass = earthmass, material = materials.earth,retain=0.4,ang_speed = earth_ang_speed,rot_axis=earth_rot_axis)
    
    moon = body(name='Moon',pos=vector(-eath_sun_dis,0,-eath_moon_dis), radius=moonradius, vel = moon_iv, mass = moonmass, Color=color.white,retain=0.2)
    
    mars = body(name='Mars',pos=vector(-249230101000,0,0), radius=3389500, vel = vector(0,0,24077), mass = 6.4171*10**23, Color=color.orange,retain = 1)

    jupiter = body(name='Jupiter',pos=vector(-778298782530,0,0), radius=69911000, vel = vector(0,0,13070), mass = 317.8*earthmass , Color=(1,0.7,0.2),retain = 4)

    saturn = body(name='Saturn',pos=vector(-1429407934000,0,0), radius=58232000, vel = vector(0,0,9690), mass = 95.159*earthmass , Color=(1,0.8,0.7),retain = 7)

    uranus = body(name='Uranus',pos=vector(-2875271638000,0,0), radius=25362000, vel = vector(0,0,6800), mass = 14.536*earthmass , Color=color.cyan,retain = 10)

    neptune = body(name='Neptune',pos=vector(-4498408853000,0,0), radius=24622000, vel = vector(0,0,5430), mass = 17.147*earthmass , Color=(0.1,0.1,1),retain = 15)
    
    bodies.append(('sun',sun))
    bodies.append(('mercury',mercury))
    bodies.append(('venus',venus))
    bodies.append(('earth',earth))
    bodies.append(('moon',moon))
    bodies.append(('mars',mars))
    bodies.append(('jupiter',jupiter))
    bodies.append(('saturn',saturn))
    bodies.append(('uranus',uranus))
    bodies.append(('neptune',neptune))
    bodies = dict(bodies)


class body():
    def __init__(self,name,pos,radius,vel,mass,Color=color.white,material = None,make_trail = True,retain = 2,ang_speed = 0,rot_axis = vector(0,0,1)):
        self.sphere = sphere(pos = pos, radius = radius, color = Color, material = material, make_trail = make_trail,retain=int(retain*50000))
        self.text = text(text=name,align='center',pos = pos+vector(0,-radius*1.5,0),height = radius/2,width = radius, depth = radius/4,color = color.white,material=materials.rough)
        self.vel = vel
        self.mass = mass
        self.ang_speed = ang_speed
        self.rot_axis = rot_axis
        self.name = name



    
def print_all_bodies():
    print "Name\t\t","Mass\t\t       ","Radius\t\t      ","Speed\t\t  ","Position"
    for body in bodies:
        print body,"\t\t",bodies[body].mass,"\t\t",bodies[body].sphere.radius,"\t\t",mag(bodies[body].vel),"\t\t",bodies[body].sphere.pos

def update_kinetics():
    global bodies
    for body in bodies:
        fg = vector(0,0,0)
        for body2 in bodies:
            if bodies[body] != bodies[body2]:
                dist = ((bodies[body].sphere.x-bodies[body2].sphere.x)**2 + (bodies[body].sphere.y-bodies[body2].sphere.y)**2 + (bodies[body].sphere.z-bodies[body2].sphere.z)**2)**.5
                RadialVector = (bodies[body].sphere.pos-bodies[body2].sphere.pos)/dist
                fg += -G*bodies[body].mass*bodies[body2].mass*RadialVector/dist**2
        bodies[body].vel += fg/bodies[body].mass*dt
        bodies[body].sphere.pos += bodies[body].vel*dt
        bodies[body].text.pos += bodies[body].vel*dt
        bodies[body].sphere.rotate(angle=bodies[body].ang_speed*dt, axis=bodies[body].rot_axis)


def main():
    init_bodies()
    center_body = bodies['sun'].sphere
    #print_all_bodies()
    while True:
        rate(dt)
        scene.center = center_body.pos
        update_kinetics()
        p = scene.mouse.pick
        if p != None:
            center_body = p

            
if __name__ == '__main__':
    main()
