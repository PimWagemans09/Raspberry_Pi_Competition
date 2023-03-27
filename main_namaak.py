#deze code is uit mijn hoofd gemaakt omdat ik geen toegang had tot de echte code tijdens het inzenden
#dit is dus NIET de code die echt word gebruikt in ons project maar een zo accuraat mogelijke recreatie

#!!!!!!!!!!!!!!!!!!!!! mogelijk klopt niet alles !!!!!!!!!!!!!!!!!!!!!!!!

try :
    import RPi.GPIO as gpio
    import time
    
    led = 26
    sensor1 = 21
    sensor2 = 20
    door_open_closed_sensor = 16
    servo = 17

    gpio.setmode(gpio.BCM)

    gpio.setup(led,gpio.OUT)
    gpio.setup(sensor1,gpio.IN)
    gpio.setup(sensor2,gpio.IN)
    gpio.setup(door_open_closed_sensor,gpio.IN)

    gpio.setup(servo,gpio.OUT)
    servo = gpio.PWM(servo,50)
    servo.start(2.5)

    person_count = 0
    last_10_seen = [0,0,0,0,0,0,0,0,0,0,]
    last_seen = 0

    def map(s1,s2,val):
        tmp = s1/s2
        tmp = val/tmp
        return tmp
    
    def set_servo_to_(degrees):
        degrees = map(10,180,degrees) + 2.5
        servo.ChangeDutyCycle(degrees)

    while True:
        sensor1_status = gpio.input(sensor1)
        sensor2_status = gpio.input(sensor2)
        door_sensor_status = gpio.input(door_open_closed_sensor)
        print(sensor1_status,sensor2_status, door_sensor_status, last_seen, last_10_seen)
        gpio.output(led,door_sensor_status)

        #dit stukje code is niet zoals orgineel maar ik kan me niet meer herrinneren hoe het orgineel er uit zag
        # dit stukje code werkt dan ook niet zoalse bedoeld 
        if sensor1_status == 0:
            if last_seen == 2:
                last_seen = 0
                if person_count > 0:
                    person_count-=1
            elif not 1 in last_10_seen:
                last_seen = 1
        elif sensor2_status == 0:
            if last_seen == 1:
                last_seen = 0
                person_count+=1
            elif not 2 in last_10_seen:
                last_seen = 2
        #einde van het niet werkende stukje code (zie regels 47 &4 8)
        
        last_10_seen.append(last_seen)
        last_10_seen.pop(0)
        temp = person_count*18
        set_servo_to_(temp)
        time.sleep(0.1)
finally:
    gpio.cleanup()