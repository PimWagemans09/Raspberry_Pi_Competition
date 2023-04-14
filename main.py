#made by xant & pim
#programmed by pim

try:
    #imports
    import RPi.GPIO as gpio
    import time

    #gpio pin variables
    sensor1 = 21
    sensor2 = 20
    door_open_sensor = 16
    led = 26
    servo = 17

    #general variables
    last_triggered = 0
    last_10_triggered = [0,0,0,0,0,0,0,0,0,0]
    person_count = 0

    #gpio init
    gpio.setmode(gpio.BCM)

    gpio.setup(sensor1,gpio.IN)
    gpio.setup(sensor2,gpio.IN)
    gpio.setup(door_open_sensor,gpio.IN)
    gpio.setup(led,gpio.OUT)
    gpio.setup(servo,gpio.OUT)

    #servo init
    p = gpio.PWM(servo, 50)
    p.start(2.5)
    time.sleep(1)

    #function to convert from 1 scale to another
    def map(scale1, scale2, inputS1):
        unit_S1_For_Unit_S2 = scale1 / scale2
        return_value = inputS1 / unit_S1_For_Unit_S2
        return(return_value)

    #function to set the servo to a specific position
    def set_servo_to(degrees):
        global p
        degrees = map(180,10.5,degrees)
        degrees+=2
        print(degrees)
        p.ChangeDutyCycle(degrees)

    #mainloop
    while True:
        #get sensor statusses
        sensor1_status=gpio.input(sensor1)
        sensor2_status=gpio.input(sensor2)
        door_open_sensor_status = gpio.input(door_open_sensor)
        
        #visual output

        gpio.output(led,not door_open_sensor_status)

        if door_open_sensor_status == 1:
            door_open_sensor_status = "closed"
        else:
            door_open_sensor_status = "open"

        print(person_count,last_triggered,sensor1_status,sensor2_status,"-",door_open_sensor_status,"    ",last_10_triggered)
        last_10_triggered.append(last_triggered)
        last_10_triggered.pop(0)

        if sensor1_status == 0:
            if last_triggered == 0:
                if not 2 in last_10_triggered:
                    last_triggered = 1
            if last_triggered == 2:
                if person_count > 0:
                    person_count -= 1
                last_triggered = 0
        elif sensor2_status == 0:
            if last_triggered == 0:
                if not 1 in last_10_triggered:
                    last_triggered = 2
            if last_triggered == 1:
                person_count += 1
                last_triggered = 0
        
        #main calculations
        temp = person_count * 18 #temp is temperature not temporary
        print(temp)
        set_servo_to(temp)
        time.sleep(0.1)

finally:
    p.stop()
    gpio.cleanup()