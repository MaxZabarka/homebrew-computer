const setClockHigh = () => {
    console.log("CLOCK HIGH")
}
const setClockLow = () => {
    console.log("CLOCK LOW")
}
const setDataHigh = () => {
    console.log("DATA HIGH")
}
const setDataLow = () => {
    console.log("DATA LOW")
}
const readData = () => {
    console.log("DATA READ")
}
const clockPulse = () => {
    setClockHigh()
    delay()
    setClockLow()
    delay()
}
const transmitBit = (data) => {
    if (data) {
        setDataHigh()
    } else {
        setDataLow()
    }
    clockPulse()
}
const delay = (data) => {

}
const sendStartBit = () => {
    setDataHigh()
    setClockHigh()
    delay()
    setDataLow()
    delay()
    setClockLow()
    delay()
}

const transmit = (data) => {
    for (let i = 0; i < 8; i++) {
        transmitBit(data&0b10000000)
        data = data << 1
    }
    setDataHigh(1)
    delay()
    setClockHigh(1)
    delay()
    const ack = readData()
}

sendStartBit()
transmit(0x50)