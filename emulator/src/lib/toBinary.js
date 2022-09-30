export const toBinary = (n, pad = 8) => {
  return n.toString(2).padStart(pad, "0");
};
