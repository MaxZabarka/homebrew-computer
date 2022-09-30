const worker = new Worker(new URL("./worker.js", import.meta.url));

// eslint-disable-next-line no-undef
const buff = new SharedArrayBuffer(1);
const shared = new Int8Array(buff);

shared[0] = 50;

worker.postMessage(shared);

setTimeout(() => {
  shared[0] = 0;
}, 2000);
