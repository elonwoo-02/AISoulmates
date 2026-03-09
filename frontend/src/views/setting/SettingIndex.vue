<script setup>
import { computed, onMounted, ref } from "vue";
import { useRouter } from "vue-router";
import api from "@/js/http/api.js";
import { useUserStore } from "@/stores/user.js";
import { useSettingsStore } from "@/stores/settings.js";
import MobilePageHeader from "@/components/navbar/MobilePageHeader.vue";

const loading = ref(true);
const saving = ref(false);
const clearingConnection = ref(false);
const loggingOut = ref(false);

const errorMessage = ref("");
const successMessage = ref("");
const accountErrorMessage = ref("");

const apiKey = ref("");
const apiBase = ref("");
const apiKeyDirty = ref(false);

const apiKeyConfigured = ref(false);
const apiKeyMasked = ref("");
const usingDefaultApiBase = ref(true);

const router = useRouter();
const user = useUserStore();
const settings = useSettingsStore();
const backTarget = computed(() => {
  if (user.id) {
    return {
      name: "user-space-index",
      params: { user_id: user.id },
    };
  }

  return { name: "homepage-index" };
});

const rememberLastSearchModel = computed({
  get: () => settings.rememberLastSearch,
  set: (value) => settings.setRememberLastSearch(value),
});

const preferGridOnMobileModel = computed({
  get: () => settings.preferGridOnMobile,
  set: (value) => settings.setPreferGridOnMobile(value),
});

const compactCardLayoutModel = computed({
  get: () => settings.compactCardLayout,
  set: (value) => settings.setCompactCardLayout(value),
});

async function loadSettings() {
  loading.value = true;
  errorMessage.value = "";
  successMessage.value = "";
  try {
    const res = await api.get("/api/user/settings/ai/");
    applySettings(res.data);
  } catch {
    errorMessage.value = "Failed to load AI settings";
  } finally {
    loading.value = false;
  }
}

function applySettings(data) {
  apiKeyConfigured.value = data.api_key_configured;
  apiKeyMasked.value = data.api_key_masked || "";
  apiBase.value = data.api_base || "";
  usingDefaultApiBase.value = data.using_default_api_base;
  apiKey.value = "";
  apiKeyDirty.value = false;
}

async function saveSettings() {
  saving.value = true;
  errorMessage.value = "";
  successMessage.value = "";
  try {
    const payload = {
      api_base: apiBase.value.trim(),
    };
    if (apiKeyDirty.value) {
      payload.api_key = apiKey.value.trim();
    }
    const res = await api.post("/api/user/settings/ai/", payload);
    if (res.data.result === "success") {
      applySettings(res.data);
      successMessage.value = "Saved";
    } else {
      errorMessage.value = res.data.result || "Failed to save AI settings";
    }
  } catch {
    errorMessage.value = "Failed to save AI settings";
  } finally {
    saving.value = false;
  }
}

async function clearApiKey() {
  clearingConnection.value = true;
  errorMessage.value = "";
  successMessage.value = "";
  try {
    const res = await api.post("/api/user/settings/ai/", {
      api_key: "",
      api_base: "",
    });
    applySettings(res.data);
    successMessage.value = "Personal settings removed";
  } catch {
    errorMessage.value = "Failed to clear personal settings";
  } finally {
    clearingConnection.value = false;
  }
}

function openProfile() {
  router.push({ name: "user-profile-index" });
}

function openSpace() {
  if (!user.id) return;
  router.push({ name: "user-space-index", params: { user_id: user.id } });
}

async function handleLogout() {
  loggingOut.value = true;
  accountErrorMessage.value = "";
  try {
    const res = await api.post("/api/user/account/logout/");
    if (res.data.result === "success") {
      user.logout();
      await router.push({ name: "user-account-login-index" });
    } else {
      accountErrorMessage.value = "Failed to log out";
    }
  } catch {
    accountErrorMessage.value = "Failed to log out";
  } finally {
    loggingOut.value = false;
  }
}

onMounted(loadSettings);
</script>

<template>
  <div class="relative overflow-hidden bg-base-100 px-4 pb-6 pt-0 md:px-6 md:py-6 lg:px-8">
    <div class="pointer-events-none absolute inset-x-0 top-0 hidden h-72 bg-[radial-gradient(circle_at_top_left,rgba(255,56,79,0.14),transparent_45%),radial-gradient(circle_at_top_right,rgba(245,185,76,0.16),transparent_42%)] md:block"></div>

    <section class="relative mx-auto max-w-6xl space-y-2 md:space-y-6">
      <MobilePageHeader
        title="Settings"
        :fallback-route="backTarget"
      />

      <div class="grid gap-6 xl:grid-cols-[1.15fr_0.85fr]">
        <section class="rounded-3xl border border-base-300 bg-base-100 p-5 shadow-sm md:rounded-[2rem] md:border-slate-200 md:bg-white/85 md:p-6 md:shadow-[0_20px_60px_rgba(15,23,42,0.08)] md:backdrop-blur">
          <div class="flex items-start justify-between gap-4 border-b border-slate-200 pb-5">
            <div>
              <h2 class="font-['Fraunces'] text-2xl font-semibold text-slate-900">AI Connection</h2>
              <p class="mt-2 text-sm text-slate-500">Personal config first, server default second.</p>
            </div>
            <span class="rounded-full border border-slate-200 bg-slate-100 px-3 py-1 text-xs font-semibold uppercase tracking-[0.2em] text-slate-500">
              Private
            </span>
          </div>

          <div v-if="loading" class="py-10 text-sm text-slate-500">Loading settings...</div>

          <form v-else class="space-y-5 pt-5" @submit.prevent="saveSettings">
            <div class="grid gap-3 sm:grid-cols-2">
              <article class="rounded-2xl border border-slate-200 bg-slate-950 p-4 text-white">
                <p class="text-xs uppercase tracking-[0.24em] text-white/50">API Key</p>
                <p class="mt-2 text-sm font-semibold">{{ apiKeyConfigured ? `Saved ${apiKeyMasked}` : "Server default" }}</p>
              </article>

              <article class="rounded-2xl border border-amber-200 bg-amber-50 p-4 text-amber-950">
                <p class="text-xs uppercase tracking-[0.24em] text-amber-700">Base URL</p>
                <p class="mt-2 text-sm font-semibold">{{ usingDefaultApiBase ? "Server default" : "Personal endpoint" }}</p>
              </article>
            </div>

            <label class="block space-y-2">
              <span class="text-sm font-semibold text-slate-700">API Key</span>
              <input
                v-model="apiKey"
                type="password"
                autocomplete="off"
                class="input w-full rounded-2xl border-slate-200 bg-slate-50 text-slate-900 focus:border-slate-300 focus:outline-none"
                :placeholder="apiKeyConfigured ? `Saved key: ${apiKeyMasked}` : 'Paste a new API key'"
                @input="apiKeyDirty = true"
              />
            </label>

            <label class="block space-y-2">
              <span class="text-sm font-semibold text-slate-700">Base URL</span>
              <input
                v-model="apiBase"
                type="url"
                class="input w-full rounded-2xl border-slate-200 bg-slate-50 text-slate-900 focus:border-slate-300 focus:outline-none"
                placeholder="https://your-openai-compatible-base-url/v1"
              />
            </label>

            <p
              v-if="errorMessage"
              class="rounded-2xl border border-red-200 bg-red-50 px-4 py-3 text-sm text-red-700"
            >
              {{ errorMessage }}
            </p>

            <p
              v-if="successMessage"
              class="rounded-2xl border border-emerald-200 bg-emerald-50 px-4 py-3 text-sm text-emerald-700"
            >
              {{ successMessage }}
            </p>

            <div class="flex flex-wrap items-center gap-3 pt-2">
              <button class="btn rounded-full border-0 bg-slate-950 px-6 text-white hover:bg-slate-800" :disabled="saving">
                {{ saving ? "Saving..." : "Save" }}
              </button>
              <button
                type="button"
                class="btn rounded-full border border-slate-200 bg-white px-5 text-slate-700 hover:border-slate-300 hover:bg-slate-50"
                :disabled="clearingConnection || (!apiKeyConfigured && usingDefaultApiBase)"
                @click="clearApiKey"
              >
                {{ clearingConnection ? "Clearing..." : "Clear personal settings" }}
              </button>
            </div>
          </form>
        </section>

        <div class="space-y-6">
          <section class="rounded-3xl border border-base-300 bg-base-100 p-5 shadow-sm md:rounded-[2rem] md:border-slate-200 md:bg-white/85 md:p-6 md:shadow-[0_20px_60px_rgba(15,23,42,0.08)] md:backdrop-blur">
            <div class="border-b border-slate-200 pb-5">
              <h2 class="font-['Fraunces'] text-2xl font-semibold text-slate-900">Account</h2>
              <p class="mt-2 text-sm text-slate-500">Shortcuts and session controls.</p>
            </div>

            <div class="mt-5 flex items-center gap-4 rounded-2xl border border-slate-200 bg-slate-50 p-4">
              <div class="avatar">
                <div class="h-14 w-14 rounded-full ring ring-white ring-offset-2 ring-offset-slate-100">
                  <img :src="user.photo" alt="user avatar" />
                </div>
              </div>
              <div class="min-w-0">
                <p class="truncate text-base font-semibold text-slate-900">{{ user.username || "User" }}</p>
                <p class="mt-1 truncate text-sm text-slate-500">{{ user.profile || "No profile yet" }}</p>
              </div>
            </div>

            <div class="mt-4 space-y-3">
              <button
                type="button"
                class="flex w-full items-center justify-between rounded-2xl border border-slate-200 bg-slate-50 px-4 py-4 text-left transition hover:border-slate-300 hover:bg-white"
                @click="openProfile"
              >
                <span>
                  <span class="block text-sm font-semibold text-slate-900">Edit profile</span>
                  <span class="mt-1 block text-sm text-slate-500">Username, avatar and bio.</span>
                </span>
                <span class="text-lg text-slate-300">›</span>
              </button>

              <button
                type="button"
                class="flex w-full items-center justify-between rounded-2xl border border-slate-200 bg-slate-50 px-4 py-4 text-left transition hover:border-slate-300 hover:bg-white disabled:cursor-not-allowed disabled:opacity-60"
                :disabled="!user.id"
                @click="openSpace"
              >
                <span>
                  <span class="block text-sm font-semibold text-slate-900">My space</span>
                  <span class="mt-1 block text-sm text-slate-500">Open your public page.</span>
                </span>
                <span class="text-lg text-slate-300">›</span>
              </button>

              <button
                type="button"
                class="flex w-full items-center justify-between rounded-2xl border border-red-200 bg-red-50 px-4 py-4 text-left text-red-700 transition hover:border-red-300 hover:bg-red-100 disabled:cursor-not-allowed disabled:opacity-60"
                :disabled="loggingOut"
                @click="handleLogout"
              >
                <span>
                  <span class="block text-sm font-semibold">{{ loggingOut ? "Logging out..." : "Log out" }}</span>
                  <span class="mt-1 block text-sm text-red-500">End the current session.</span>
                </span>
                <span class="text-lg text-red-300">›</span>
              </button>
            </div>

            <p
              v-if="accountErrorMessage"
              class="mt-4 rounded-2xl border border-red-200 bg-red-50 px-4 py-3 text-sm text-red-700"
            >
              {{ accountErrorMessage }}
            </p>
          </section>

          <section class="rounded-3xl border border-base-300 bg-base-100 p-5 shadow-sm md:rounded-[2rem] md:border-slate-200 md:bg-white/85 md:p-6 md:shadow-[0_20px_60px_rgba(15,23,42,0.08)] md:backdrop-blur">
            <div class="border-b border-slate-200 pb-5">
              <h2 class="font-['Fraunces'] text-2xl font-semibold text-slate-900">Preferences</h2>
              <p class="mt-2 text-sm text-slate-500">Saved in this browser.</p>
            </div>

            <div class="mt-5 space-y-4">
              <label class="flex items-start justify-between gap-4 rounded-2xl border border-slate-200 bg-slate-50 px-4 py-4">
                <span>
                  <span class="block text-sm font-semibold text-slate-900">Remember last search</span>
                  <span class="mt-1 block text-sm text-slate-500">Reuse the last homepage keyword.</span>
                </span>
                <input v-model="rememberLastSearchModel" type="checkbox" class="toggle mt-1" />
              </label>

              <div class="rounded-2xl border border-slate-200 bg-slate-50 px-4 py-4">
                <div class="flex items-start justify-between gap-4">
                  <span>
                    <span class="block text-sm font-semibold text-slate-900">Saved keyword</span>
                    <span class="mt-1 block text-sm text-slate-500">{{ settings.lastSearchQuery || "None" }}</span>
                  </span>
                  <button
                    type="button"
                    class="btn btn-sm rounded-full border border-slate-200 bg-white px-4 text-slate-700 hover:border-slate-300 hover:bg-slate-100"
                    :disabled="!settings.lastSearchQuery"
                    @click="settings.clearLastSearchQuery()"
                  >
                    Clear
                  </button>
                </div>
              </div>

              <label class="flex items-start justify-between gap-4 rounded-2xl border border-slate-200 bg-slate-50 px-4 py-4">
                <span>
                  <span class="block text-sm font-semibold text-slate-900">Prefer grid on mobile</span>
                  <span class="mt-1 block text-sm text-slate-500">Disable homepage swipe cards.</span>
                </span>
                <input v-model="preferGridOnMobileModel" type="checkbox" class="toggle mt-1" />
              </label>

              <label class="flex items-start justify-between gap-4 rounded-2xl border border-slate-200 bg-slate-50 px-4 py-4">
                <span>
                  <span class="block text-sm font-semibold text-slate-900">Compact card layout</span>
                  <span class="mt-1 block text-sm text-slate-500">Reduce spacing in character grids.</span>
                </span>
                <input v-model="compactCardLayoutModel" type="checkbox" class="toggle mt-1" />
              </label>
            </div>
          </section>
        </div>
      </div>
    </section>
  </div>
</template>

<style scoped>
</style>
