def on_log_full():
    global logData
    logData = 0
datalogger.on_log_full(on_log_full)

def on_button_pressed_a():
    global recording
    recording = 1
    radio.send_number(1)
    basic.show_leds("""
        . # . . .
        . # # . .
        . # # # .
        . # # . .
        . # . . .
        """)
    basic.pause(500)
input.on_button_pressed(Button.A, on_button_pressed_a)

def on_button_pressed_ab():
    global logData
    logData = 1
    radio.send_number(2)
    datalogger.delete_log()
    basic.show_leds("""
        # . . . #
        . # . # .
        . . # . .
        . # . # .
        # . . . #
        """)
    basic.pause(1000)
input.on_button_pressed(Button.AB, on_button_pressed_ab)

def on_button_pressed_b():
    global recording
    recording = 0
    radio.send_number(0)
    basic.show_leds("""
        . # . . .
        . # # . .
        . # # # .
        . # # . .
        . # . . .
        """)
    basic.pause(500)
input.on_button_pressed(Button.B, on_button_pressed_b)

logData = 0
recording = 0
recording = 0
logData = 1
radio.set_group(143)

def on_every_interval():
    if recording == 1:
        datalogger.log(datalogger.create_cv("x", input.acceleration(Dimension.X)),
            datalogger.create_cv("y", input.acceleration(Dimension.Y)),
            datalogger.create_cv("z", input.acceleration(Dimension.Z)),
            datalogger.create_cv("strength", input.acceleration(Dimension.STRENGTH)))
loops.every_interval(75, on_every_interval)

def on_forever():
    if logData == 1:
        if abs(input.acceleration(Dimension.STRENGTH)) >= 3500:
            basic.show_leds("""
                . . . . #
                . . . # #
                . . # # #
                . # # # #
                # # # # #
                """)
            basic.pause(750)
        elif abs(input.acceleration(Dimension.STRENGTH)) >= 3000:
            basic.show_leds("""
                . . . . .
                . . . # .
                . . # # .
                . # # # .
                # # # # .
                """)
            basic.pause(750)
        elif abs(input.acceleration(Dimension.STRENGTH)) >= 2500:
            basic.show_leds("""
                . . . . .
                . . . . .
                . . # . .
                . # # . .
                # # # . .
                """)
            basic.pause(500)
        elif abs(input.acceleration(Dimension.STRENGTH)) >= 2000:
            basic.show_leds("""
                . . . . .
                . . . . .
                . . . . .
                . # . . .
                # # . . .
                """)
        elif abs(input.acceleration(Dimension.STRENGTH)) >= 1500:
            basic.show_leds("""
                . . . . .
                . . . . .
                . . . . .
                . . . . .
                # . . . .
                """)
        else:
            basic.show_leds("""
                . . . . .
                . . . . .
                . . . . .
                . . . . .
                . . . . .
                """)
    else:
        basic.show_leds("""
            # . . . #
            . # . # .
            . . # . .
            . # . # .
            # . . . #
            """)
basic.forever(on_forever)
