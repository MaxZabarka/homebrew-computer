const crossOriginIsolationConfigPlugin = require("./craco-plugin-cross-origin-isolation-config");

module.exports = {
  // webpack: {
  //   configure: (webpackConfig) => {
  //     const scopePluginIndex = webpackConfig.resolve.plugins.findIndex(
  //       ({ constructor }) =>
  //         constructor && constructor.name === "ModuleScopePlugin"
  //     );
  //     webpackConfig.resolve.plugins.splice(scopePluginIndex, 1);
  //     return webpackConfig;
  //   },
  // },
  plugins: [
    {
      plugin: crossOriginIsolationConfigPlugin,
      options: { preText: "Will log the dev server config:" },
    },
  ],
};
