module.exports = {
  overrideDevServerConfig: ({
    devServerConfig,
    cracoConfig,
    pluginOptions,
    context: { env, paths, allowedHost },
  }) => {

    devServerConfig.headers = {
      ...devServerConfig.headers,
      "Cross-Origin-Embedder-Policy": "require-corp",
      "Cross-Origin-Opener-Policy": "same-origin",
    };

    return devServerConfig;
  },
};
