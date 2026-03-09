<script setup>
import {computed, nextTick, onBeforeUnmount, onMounted, ref, useTemplateRef, watch} from "vue";
import {useRoute, useRouter} from "vue-router";
import api from "@/js/http/api.js";
import MobilePageHeader from "@/components/navbar/MobilePageHeader.vue";
import ArrowLeftIcon from "@/components/navbar/icons/ArrowLeftIcon.vue";
import ChatHistory from "@/components/character/chat_field/chat_history/ChatHistory.vue";
import InputField from "@/components/character/chat_field/input_field/InputField.vue";

const router = useRouter();
const route = useRoute();

const friends = ref([]);
const history = ref([]);
const selectedFriend = ref(null);
const loadingFriends = ref(false);
const hasMoreFriends = ref(true);
const friendsError = ref("");
const isThinking = ref(false);
const isMobile = ref(false);

const chatHistoryRef = useTemplateRef("chat-history-ref");

const selectedFriendId = computed(() => selectedFriend.value?.id ?? null);
const showListPane = computed(() => !isMobile.value || !selectedFriend.value);
const showChatPane = computed(() => !isMobile.value || !!selectedFriend.value);
const selectedBackdropStyle = computed(() => {
  const image = selectedFriend.value?.character?.background_image;
  if (!image) return {};

  return {
    backgroundImage: `url(${image})`,
    backgroundSize: "cover",
    backgroundPosition: "center",
  };
});

function normalizeFriendId(value) {
  const friendId = Number(Array.isArray(value) ? value[0] : value);
  return Number.isInteger(friendId) && friendId > 0 ? friendId : null;
}

function updateViewport() {
  isMobile.value = window.innerWidth < 768;
}

function resetConversationState() {
  history.value = [];
  isThinking.value = false;
}

function findFriendById(friendId) {
  return friends.value.find((friend) => friend.id === friendId) || null;
}

async function scrollChatToBottom() {
  await nextTick();
  chatHistoryRef.value?.scrollToBottom();
}

async function loadMoreFriends() {
  if (loadingFriends.value || !hasMoreFriends.value) return;

  loadingFriends.value = true;
  friendsError.value = "";
  let newFriends = [];

  try {
    const res = await api.get("/api/friend/get_list/", {
      params: {
        items_count: friends.value.length,
      },
    });

    if (res.data.result === "success") {
      newFriends = res.data.friends || [];
    } else {
      friendsError.value = "Failed to load conversations";
    }
  } catch {
    friendsError.value = "Failed to load conversations";
  } finally {
    loadingFriends.value = false;
    if (newFriends.length === 0) {
      hasMoreFriends.value = false;
    } else {
      friends.value.push(...newFriends);
    }
  }
}

async function ensureFriendLoaded(friendId) {
  if (!friendId) return null;

  let friend = findFriendById(friendId);
  while (!friend && hasMoreFriends.value) {
    await loadMoreFriends();
    friend = findFriendById(friendId);
  }

  return friend;
}

function syncFriendQuery(friendId) {
  const currentId = normalizeFriendId(route.query.friend_id);
  if (currentId === friendId) return;

  void router.replace({
    name: "new-index",
    query: {
      ...route.query,
      friend_id: String(friendId),
    },
  });
}

function clearFriendQuery() {
  if (!route.query.friend_id) return;

  const query = {...route.query};
  delete query.friend_id;
  void router.replace({
    name: "new-index",
    query,
  });
}

function applySelectedFriend(friend, syncRoute = true) {
  if (!friend) return;
  if (selectedFriend.value?.id === friend.id) {
    if (syncRoute) {
      syncFriendQuery(friend.id);
    }
    return;
  }

  selectedFriend.value = friend;
  resetConversationState();

  if (syncRoute) {
    syncFriendQuery(friend.id);
  }
}

function clearSelectedFriend(syncRoute = true) {
  selectedFriend.value = null;
  resetConversationState();

  if (syncRoute) {
    clearFriendQuery();
  }
}

async function syncSelectedFriendFromRoute() {
  const friendId = normalizeFriendId(route.query.friend_id);
  if (!friendId) {
    clearSelectedFriend(false);
    return;
  }

  const friend = await ensureFriendLoaded(friendId);
  if (friend) {
    applySelectedFriend(friend, false);
  } else {
    clearSelectedFriend(false);
  }
}

function openConversation(friend) {
  applySelectedFriend(friend);
}

function closeConversation() {
  clearSelectedFriend();
}

function openHomepage() {
  void router.push({name: "homepage-index"});
}

function handlePushBackMessage(msg) {
  history.value.push(msg);
  void scrollChatToBottom();
}

function handleAddToLastMessage(delta) {
  const lastMessage = history.value.at(-1);
  if (!lastMessage) return;

  lastMessage.content += delta;
  void scrollChatToBottom();
}

function handlePushFrontMessage(msg) {
  history.value.unshift(msg);
}

function handleUpdateProcessing(value) {
  isThinking.value = value;
  if (value) {
    void scrollChatToBottom();
  }
}

watch(
  () => route.query.friend_id,
  () => {
    void syncSelectedFriendFromRoute();
  }
);

onMounted(async () => {
  updateViewport();
  window.addEventListener("resize", updateViewport);

  await loadMoreFriends();
  await syncSelectedFriendFromRoute();
});

onBeforeUnmount(() => {
  window.removeEventListener("resize", updateViewport);
});
</script>

<template>
  <div class="relative px-4 py-6 pb-24 md:px-6 lg:px-8">
    <div class="pointer-events-none absolute inset-x-0 top-0 h-96 bg-[var(--cloud-dancer)]"></div>

    <section class="relative mx-auto max-w-7xl space-y-5">
      <MobilePageHeader
        title="Messages"
        :fallback-route="{ name: 'homepage-index' }"
      />

      <div class="grid gap-4 md:grid-cols-[320px_minmax(0,1fr)] xl:grid-cols-[360px_minmax(0,1fr)]">
        <aside
          v-if="showListPane"
          class="flex min-h-[68vh] flex-col overflow-hidden rounded-[2rem] border border-slate-200 bg-white/85 shadow-[0_18px_54px_rgba(15,23,42,0.08)] backdrop-blur"
        >
          <div class="border-b border-slate-200 px-5 py-5">
            <p class="text-xs font-semibold uppercase tracking-[0.22em] text-slate-400">Conversations</p>
            <h2 class="mt-2 font-['Fraunces'] text-2xl font-semibold text-slate-900">Your circle</h2>
            <p class="mt-2 text-sm text-slate-500">Pick a character to continue the thread.</p>
          </div>

          <div class="min-h-0 flex-1 overflow-y-auto px-3 py-3">
            <div v-if="friends.length" class="space-y-2">
              <button
                v-for="friend in friends"
                :key="friend.id"
                type="button"
                class="group flex w-full items-start gap-3 rounded-[1.5rem] border px-3 py-3 text-left transition"
                :class="selectedFriendId === friend.id
                  ? 'border-slate-900 bg-slate-950 text-white shadow-[0_16px_40px_rgba(15,23,42,0.18)]'
                  : 'border-slate-200 bg-slate-50/80 text-slate-900 hover:border-slate-300 hover:bg-white'"
                @click="openConversation(friend)"
              >
                <div class="h-14 w-14 shrink-0 overflow-hidden rounded-[1.25rem] bg-slate-200">
                  <img
                    v-if="friend.character.photo"
                    :src="friend.character.photo"
                    :alt="friend.character.name"
                    class="h-full w-full object-cover"
                  >
                  <div
                    v-else
                    class="flex h-full w-full items-center justify-center text-lg font-semibold"
                    :class="selectedFriendId === friend.id ? 'bg-white/10 text-white' : 'bg-slate-200 text-slate-500'"
                  >
                    {{ friend.character.name?.slice(0, 1) || "?" }}
                  </div>
                </div>

                <div class="min-w-0 flex-1">
                  <div class="flex items-start justify-between gap-3">
                    <div class="min-w-0">
                      <p class="truncate text-sm font-semibold" :class="selectedFriendId === friend.id ? 'text-white' : 'text-slate-900'">
                        {{ friend.character.name }}
                      </p>
                      <p class="mt-1 truncate text-xs uppercase tracking-[0.18em]" :class="selectedFriendId === friend.id ? 'text-white/55' : 'text-slate-400'">
                        {{ friend.character.author.username }}
                      </p>
                    </div>
                    <span
                      class="rounded-full px-2.5 py-1 text-[10px] font-semibold uppercase tracking-[0.18em]"
                      :class="selectedFriendId === friend.id ? 'bg-white/10 text-white' : 'bg-slate-200 text-slate-500'"
                    >
                      {{ selectedFriendId === friend.id ? "Open" : "Chat" }}
                    </span>
                  </div>

                  <p
                    class="conversation-summary mt-3 text-sm"
                    :class="selectedFriendId === friend.id ? 'text-white/72' : 'text-slate-500'"
                  >
                    {{ friend.character.profile || "No profile yet." }}
                  </p>
                </div>
              </button>
            </div>

            <div
              v-else-if="!loadingFriends && !friendsError"
              class="flex h-full min-h-[340px] flex-col items-center justify-center rounded-[1.75rem] border border-dashed border-slate-200 bg-slate-50/80 px-6 text-center"
            >
              <p class="font-['Fraunces'] text-2xl font-semibold text-slate-900">No conversations yet</p>
              <p class="mt-3 max-w-xs text-sm text-slate-500">Add a friend from the homepage or character cards, then come back here.</p>
              <button
                type="button"
                class="btn mt-5 rounded-full border-0 bg-slate-950 px-6 text-white hover:bg-slate-800"
                @click="openHomepage"
              >
                Go to homepage
              </button>
            </div>

            <p
              v-if="friendsError"
              class="rounded-[1.5rem] border border-red-200 bg-red-50 px-4 py-3 text-sm text-red-700"
            >
              {{ friendsError }}
            </p>
          </div>

          <div class="border-t border-slate-200 px-4 py-4">
            <div v-if="loadingFriends" class="flex items-center justify-center py-2 text-slate-500">
              <span class="loading loading-spinner loading-md"></span>
            </div>
            <button
              v-else-if="hasMoreFriends"
              type="button"
              class="btn w-full rounded-full border border-slate-200 bg-white text-slate-700 hover:border-slate-300 hover:bg-slate-50"
              @click="loadMoreFriends"
            >
              Load more
            </button>
            <p v-else-if="friends.length" class="text-center text-xs font-semibold uppercase tracking-[0.18em] text-slate-400">
              End of conversations
            </p>
          </div>
        </aside>

        <section
          v-if="showChatPane"
          class="relative flex min-h-[68vh] flex-col overflow-hidden rounded-[2rem] border border-slate-200 bg-white/78 shadow-[0_18px_54px_rgba(15,23,42,0.08)] backdrop-blur"
        >
          <div v-if="selectedFriend" class="pointer-events-none absolute inset-0 opacity-15" :style="selectedBackdropStyle"></div>
          <div class="pointer-events-none absolute inset-0 bg-[var(--cloud-dancer)] opacity-80"></div>

          <template v-if="selectedFriend">
            <div class="relative border-b border-slate-200/80 px-4 py-4 md:px-5">
              <div class="flex items-center gap-3">
                <button
                  type="button"
                  class="flex h-10 w-10 shrink-0 items-center justify-center rounded-full border border-slate-200 bg-white text-slate-600 transition hover:border-slate-300 hover:text-slate-900 md:hidden"
                  aria-label="Back to conversations"
                  @click="closeConversation"
                >
                  <ArrowLeftIcon class="h-5 w-5" />
                </button>

                <div class="h-14 w-14 shrink-0 overflow-hidden rounded-[1.25rem] border border-white/70 bg-slate-200 shadow-sm">
                  <img
                    v-if="selectedFriend.character.photo"
                    :src="selectedFriend.character.photo"
                    :alt="selectedFriend.character.name"
                    class="h-full w-full object-cover"
                  >
                  <div v-else class="flex h-full w-full items-center justify-center bg-slate-200 text-lg font-semibold text-slate-500">
                    {{ selectedFriend.character.name?.slice(0, 1) || "?" }}
                  </div>
                </div>

                <div class="min-w-0 flex-1">
                  <div class="flex flex-wrap items-center gap-2">
                    <h2 class="truncate font-['Fraunces'] text-2xl font-semibold text-slate-900">
                      {{ selectedFriend.character.name }}
                    </h2>
                    <span
                      class="rounded-full px-3 py-1 text-[10px] font-semibold uppercase tracking-[0.18em]"
                      :class="isThinking ? 'bg-amber-100 text-amber-700' : 'bg-slate-100 text-slate-500'"
                    >
                      {{ isThinking ? "Thinking" : "Ready" }}
                    </span>
                  </div>
                  <p class="mt-1 truncate text-sm text-slate-500">
                    {{ selectedFriend.character.author.username }}
                  </p>
                </div>
              </div>

              <p class="mt-4 text-sm text-slate-600">{{ selectedFriend.character.profile || "Start a new conversation." }}</p>
            </div>

            <div class="relative flex min-h-0 flex-1 flex-col px-3 pb-3 pt-3 md:px-4">
              <ChatHistory
                :key="selectedFriend.id"
                ref="chat-history-ref"
                class="rounded-[1.75rem] bg-white/55 px-2 py-3 shadow-inner backdrop-blur-sm"
                :history="history"
                :friendId="selectedFriend.id"
                :character="selectedFriend.character"
                @pushBackFrontMessage="handlePushFrontMessage"
              />

              <div class="pt-3">
                <InputField
                  :key="`input-${selectedFriend.id}`"
                  :friendId="selectedFriend.id"
                  variant="page"
                  @pushBackMessage="handlePushBackMessage"
                  @addToLastMessage="handleAddToLastMessage"
                  @updateProcessing="handleUpdateProcessing"
                />
              </div>
            </div>
          </template>

          <div v-else class="relative flex h-full min-h-[68vh] flex-col items-center justify-center px-8 text-center">
            <div class="max-w-md rounded-[2rem] border border-dashed border-slate-200 bg-white/70 px-8 py-10 shadow-inner">
              <p class="text-xs font-semibold uppercase tracking-[0.24em] text-slate-400">Workspace</p>
              <h2 class="mt-4 font-['Fraunces'] text-3xl font-semibold text-slate-900">Pick a conversation</h2>
              <p class="mt-3 text-sm text-slate-500">The chat stream will open here. History loading and live replies stay the same as the character modal.</p>
            </div>
          </div>
        </section>
      </div>
    </section>
  </div>
</template>

<style scoped>
.conversation-summary {
  display: -webkit-box;
  overflow: hidden;
  -webkit-box-orient: vertical;
  -webkit-line-clamp: 2;
}
</style>
