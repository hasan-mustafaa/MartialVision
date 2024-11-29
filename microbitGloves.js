input.onButtonPressed(Button.A, function () {
    basic.showString(control.deviceName())
})
bluetooth.startUartService()
bluetooth.startButtonService()
basic.forever(function () {
    bluetooth.uartWriteValue("x", input.acceleration(Dimension.X))
    bluetooth.uartWriteValue("y", input.acceleration(Dimension.Y))
    bluetooth.uartWriteValue("z", input.acceleration(Dimension.Z))
    bluetooth.uartWriteValue("strength", input.acceleration(Dimension.Strength))
    if (input.acceleration(Dimension.Strength) >= 3500) {
        basic.showLeds(`
            . . . . #
            . . . # #
            . . # # #
            . # # # #
            # # # # #
            `)
        basic.pause(1000)
    } else if (input.acceleration(Dimension.Strength) >= 3000) {
        basic.showLeds(`
            . . . . .
            . . . # .
            . . # # .
            . # # # .
            # # # # .
            `)
        basic.pause(1000)
    } else if (input.acceleration(Dimension.Strength) >= 2500) {
        basic.showLeds(`
            . . . . .
            . . . . .
            . . # . .
            . # # . .
            # # # . .
            `)
        basic.pause(1000)
    } else if (input.acceleration(Dimension.Strength) >= 2000) {
        basic.showLeds(`
            . . . . .
            . . . . .
            . . . . .
            . # . . .
            # # . . .
            `)
    } else if (input.acceleration(Dimension.Strength) >= 1500) {
        basic.showLeds(`
            . . . . .
            . . . . .
            . . . . .
            . . . . .
            # . . . .
            `)
    } else {
        basic.showLeds(`
            . . . . .
            . . . . .
            . . . . .
            . . . . .
            . . . . .
            `)
    }
})
