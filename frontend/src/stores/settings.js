import { defineStore } from "pinia";
import { ref, watch } from "vue";

const STORAGE_KEY = "aisoulmates.settings";

function loadStoredSettings() {
  if (typeof window === "undefined") {
    return {};
  }

  try {
    return JSON.parse(window.localStorage.getItem(STORAGE_KEY) || "{}");
  } catch {
    return {};
  }
}

function saveStoredSettings(payload) {
  if (typeof window === "undefined") {
    return;
  }
  window.localStorage.setItem(STORAGE_KEY, JSON.stringify(payload));
}

export const useSettingsStore = defineStore("settings", () => {
  const stored = loadStoredSettings();

  const rememberLastSearch = ref(Boolean(stored.rememberLastSearch));
  const preferGridOnMobile = ref(Boolean(stored.preferGridOnMobile));
  const compactCardLayout = ref(Boolean(stored.compactCardLayout));
  const lastSearchQuery = ref(typeof stored.lastSearchQuery === "string" ? stored.lastSearchQuery : "");

  watch(
    [rememberLastSearch, preferGridOnMobile, compactCardLayout, lastSearchQuery],
    () => {
      saveStoredSettings({
        rememberLastSearch: rememberLastSearch.value,
        preferGridOnMobile: preferGridOnMobile.value,
        compactCardLayout: compactCardLayout.value,
        lastSearchQuery: lastSearchQuery.value,
      });
    },
  );

  function setRememberLastSearch(value) {
    rememberLastSearch.value = Boolean(value);
    if (!rememberLastSearch.value) {
      lastSearchQuery.value = "";
    }
  }

  function setPreferGridOnMobile(value) {
    preferGridOnMobile.value = Boolean(value);
  }

  function setCompactCardLayout(value) {
    compactCardLayout.value = Boolean(value);
  }

  function setLastSearchQuery(value) {
    lastSearchQuery.value = rememberLastSearch.value ? value.trim() : "";
  }

  function clearLastSearchQuery() {
    lastSearchQuery.value = "";
  }

  return {
    rememberLastSearch,
    preferGridOnMobile,
    compactCardLayout,
    lastSearchQuery,
    setRememberLastSearch,
    setPreferGridOnMobile,
    setCompactCardLayout,
    setLastSearchQuery,
    clearLastSearchQuery,
  };
});
