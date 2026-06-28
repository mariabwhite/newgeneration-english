(function () {
  "use strict";

  var loginPage = "/lingua-boost-lab/login.html";
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

  function localHasAccess() {
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

  async function serverHasAccess() {
    try {
      var response = await fetch("/api/premium-lessons", {
        credentials: "include",
        cache: "no-store",
      });

      if (response.status === 404) return null;
      if (!response.ok) return false;

      var payload = await response.json();
      if (!payload || !Array.isArray(payload.lessons)) return false;

      var here = currentPath();
      return payload.lessons.some(function (lesson) {
        return normalizePath(lesson && lesson.url) === here;
      });
    } catch (error) {
      return null;
    }
  }

  (async function () {
    var server = await serverHasAccess();
    if (server === true) return;

    if (server === false || (server === null && !localHasAccess())) {
      var target = loginPage + "?next=" + encodeURIComponent(window.location.pathname + window.location.search);
      window.location.replace(target);
    }
  })();
})();
