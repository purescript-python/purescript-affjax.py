"""
 var platformSpecific = { };
  if (typeof module !== "undefined" && module.require && !(typeof process !== "undefined" && process.versions["electron"])) {
    // We are on node.js
    platformSpecific.newXHR = function () {
      var XHR = module.require("xhr2");
      return new XHR();
    };

    platformSpecific.fixupUrl = function (url, xhr) {
      if (xhr.nodejsBaseUrl === null) {
        var urllib = module.require("url");
        var u = urllib.parse(url);
        u.protocol = u.protocol || "http:";
        u.hostname = u.hostname || "localhost";
        return urllib.format(u);
      } else {
        return url || "/";
      }
    };

    platformSpecific.getResponse = function (xhr) {
      return xhr.response;
    };
  } else {
    // We are in the browser
    platformSpecific.newXHR = function () {
      return new XMLHttpRequest();
    };

    platformSpecific.fixupUrl = function (url) {
      return url || "/";
    };

    platformSpecific.getResponse = function (xhr) {
      return xhr.response;
    };
  }
"""
import http.client
from urllib.parse import urlparse
from base64 import b64encode
import threading

# todo - is there an analog for withCredentials here?
def _ajax(mkHeader, options):
    def _1(errback, callback):
        if options["responseType"] in ["arraybuffer", "blob", "document"]:
            errback(
                Exception(
                    "Affjax python does not support arraybuffer, blob, or document responses yet"
                )
            )
            return

        def _toThreading():
            parsedUrl = urlparse(options["url"])
            conn = (
                http.client.HTTPConnection(parsedUrl.netloc)
                if parsedUrl.scheme == "http"
                else http.client.HTTPSConnection(parsedUrl.netloc)
            )
            headers = {}
            if options.username and options.password:
                userAndPass = b64encode(b"username:password").decode("ascii")
                headers["Authorization"] = "Basic %s" % userAndPass
            if options["headers"]:
                for header in headers:
                    headers[header["field"]] = header["value"]
            try:
                conn.request(
                    options["method"] if options["method"] else "GET",
                    parsedUrl.path,
                    body=options["content"],
                    headers=headers,
                )
                r1 = conn.getresponse()
                callback(
                    {
                        "status": r1.status,
                        "statusText": r1.reason,
                        "headers": tuple([mkHeader(k)(v) for k, v in r1.getheaders]),
                        "body": r1.read().decode("utf-8"),
                    }
                )

            except Exception as e:
                errback(e)
                return

        t = threading.Thread(target=_toThreading)
        t.start()

        def _toRet(error, cancelErrback, cancelCallback):
            try:
                t.cancel()
            except Exception as e:
                return cancelErrback(e)
            return cancelCallback()

        return _toRet

    return _1
