"use strict";

// src/vercel-request-context.ts
var SYMBOL_FOR_REQ_CONTEXT = Symbol.for("@vercel/request-context");
function getContext() {
  const fromSymbol = globalThis;
  return fromSymbol[SYMBOL_FOR_REQ_CONTEXT]?.get?.() ?? {};
}

// src/next-request-context.ts
var import_async_hooks = require("async_hooks");
var name = "@next/request-context";
var NEXT_REQUEST_CONTEXT_SYMBOL = Symbol.for(name);
var INTERNAL_STORAGE_FIELD_SYMBOL = Symbol.for("internal.storage");
function getOrCreateContextSingleton() {
  const _globalThis = globalThis;
  if (!_globalThis[NEXT_REQUEST_CONTEXT_SYMBOL]) {
    const storage = new import_async_hooks.AsyncLocalStorage();
    const Context = {
      get: () => storage.getStore(),
      [INTERNAL_STORAGE_FIELD_SYMBOL]: storage
    };
    _globalThis[NEXT_REQUEST_CONTEXT_SYMBOL] = Context;
  }
  return _globalThis[NEXT_REQUEST_CONTEXT_SYMBOL];
}
var NextRequestContext = getOrCreateContextSingleton();
function withNextRequestContext(value, callback) {
  const storage = NextRequestContext[INTERNAL_STORAGE_FIELD_SYMBOL];
  return storage.run(value, callback);
}

// src/server-launcher.ts
process.chdir(__dirname);
var region = process.env.VERCEL_REGION || process.env.NOW_REGION;
if (!process.env.NODE_ENV) {
  process.env.NODE_ENV = region === "dev1" ? "development" : "production";
}
if (process.env.NODE_ENV !== "production" && region !== "dev1") {
  console.warn(
    `Warning: NODE_ENV was incorrectly set to "${process.env.NODE_ENV}", this value is being overridden to "production"`
  );
  process.env.NODE_ENV = "production";
}
process.env.__NEXT_PRIVATE_PREBUNDLED_REACT = "next"
var NextServer = require("next/dist/server/next-server.js").default;
// @preserve next-server-preload-target
const conf = {"env":{},"webpack":null,"eslint":{"ignoreDuringBuilds":true},"typescript":{"ignoreBuildErrors":true,"tsconfigPath":"tsconfig.json"},"distDir":".next","cleanDistDir":true,"assetPrefix":"","configOrigin":"next.config.mjs","useFileSystemPublicRoutes":true,"generateEtags":true,"pageExtensions":["tsx","ts","jsx","js"],"poweredByHeader":true,"compress":false,"analyticsId":"","images":{"deviceSizes":[640,750,828,1080,1200,1920,2048,3840],"imageSizes":[16,32,48,64,96,128,256,384],"path":"/_next/image","loader":"default","loaderFile":"","domains":[],"disableStaticImages":false,"minimumCacheTTL":60,"formats":["image/webp"],"dangerouslyAllowSVG":false,"contentSecurityPolicy":"script-src 'none'; frame-src 'none'; sandbox;","contentDispositionType":"inline","remotePatterns":[{"protocol":"https","hostname":"*","port":"","pathname":"/**"}],"unoptimized":true},"devIndicators":{"buildActivity":true,"buildActivityPosition":"bottom-right"},"onDemandEntries":{"maxInactiveAge":15000,"pagesBufferLength":2},"amp":{"canonicalBase":""},"basePath":"","sassOptions":{},"trailingSlash":false,"i18n":null,"productionBrowserSourceMaps":false,"optimizeFonts":true,"excludeDefaultMomentLocales":true,"serverRuntimeConfig":{},"publicRuntimeConfig":{},"reactStrictMode":false,"httpAgentOptions":{"keepAlive":true},"outputFileTracing":true,"staticPageGenerationTimeout":60,"swcMinify":true,"experimental":{"caseSensitiveRoutes":false,"useDeploymentId":false,"useDeploymentIdServerActions":false,"clientRouterFilter":true,"clientRouterFilterRedirects":false,"fetchCacheKeyPrefix":"","middlewarePrefetch":"flexible","optimisticClientCache":true,"manualClientBasePath":false,"legacyBrowsers":false,"newNextLinkBehavior":true,"cpus":15,"memoryBasedWorkersCount":false,"sharedPool":true,"isrFlushToDisk":true,"workerThreads":false,"pageEnv":false,"optimizeCss":false,"nextScriptWorkers":false,"scrollRestoration":false,"externalDir":false,"disableOptimizedLoading":false,"gzipSize":true,"swcFileReading":true,"craCompat":false,"esmExternals":true,"appDir":true,"isrMemoryCacheSize":52428800,"fullySpecified":false,"outputFileTracingRoot":"C:\\Users\\asus\\Documents\\Testing\\devwrap\\frontend\\newrap","swcTraceProfiling":false,"forceSwcTransforms":false,"largePageDataBytes":128000,"adjustFontFallbacks":false,"adjustFontFallbacksWithSizeAdjust":false,"typedRoutes":false,"instrumentationHook":false,"trustHostHeader":true},"configFileName":"next.config.mjs"};
var nextServer = new NextServer({
  conf,
  dir: ".",
  minimalMode: true,
  customServer: false
});
var serve = (handler) => async (req, res) => {
  try {
    const vercelContext = getContext();
    await withNextRequestContext(
      { waitUntil: vercelContext.waitUntil },
      () => {
        // @preserve entryDirectory handler
        return handler(req, res);
      }
    );
  } catch (err) {
    console.error(err);
    process.exit(1);
  }
};
module.exports = serve(nextServer.getRequestHandler());
if (conf.experimental?.ppr && "getRequestHandlerWithMetadata" in nextServer && typeof nextServer.getRequestHandlerWithMetadata === "function") {
  module.exports.getRequestHandlerWithMetadata = (metadata) => serve(nextServer.getRequestHandlerWithMetadata(metadata));
}
if (process.env.NEXT_PRIVATE_PRELOAD_ENTRIES) {
  module.exports.preload = nextServer.unstable_preloadEntries.bind(nextServer);
}
