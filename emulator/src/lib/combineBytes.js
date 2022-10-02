export const combineBytes = (highByte, lowByte, size=8) => (highByte << size) + lowByte;
