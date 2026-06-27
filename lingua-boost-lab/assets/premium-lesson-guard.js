(function () {
  "use strict";

  var premiumPage = "/lingua-boost-lab/login.html";
  var cacheKey = "nge-vault-cache";

  function normalizePath(value) {
    try {
      var url = new URL(value, window.location.origin + "/lingua-boost-lab/");
      var path = url.pathname;
      if (path.endsWith("/index.html")) path = path.slice(0, -10);
      if (!path.endsWith("/") && !/\.[a-z0-9]+$/i.test(path)) path += "/";
      return path;
    } catch (error) {
      return "";
    }
  }

  function currentPath() {
    var path = window.location.pathname;
    if (path.endsWith("/index.html")) path = path.slice(0, -10);
    if (!path.endsWith("/") && !/\.[a-z0-9]+$/i.test(path)) path += "/";
    return path;
  }

  function hasAccess() {
    var raw = "";
    try {
      raw = localStorage.getItem(cacheKey);
    } catch (error) {
      return false;
    }
    if (!raw) return false;

    try {
      var lessons = JSON.parse(raw);
      if (!Array.isArray(lessons)) return false;
      var here = currentPath();
      return lessons.some(function (lesson) {
        return normalizePath(lesson && lesson.url) === here;
      });
    } catch (error) {
      return false;
    }
  }

  if (!hasAccess()) {
    var target = premiumPage + "?next=" + encodeURIComponent(window.location.pathname + window.location.search);
    window.location.replace(target);
  }
})();
