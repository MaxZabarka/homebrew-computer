onmessage = (e) => {
    let sum = 1
    while (e.data[0]) {
        sum = sum + sum
        // console.log('e.data[0]', e.data[0])
    }
    console.log(sum)
}
