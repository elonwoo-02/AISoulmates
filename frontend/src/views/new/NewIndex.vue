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
  <div class="wechat-container">
    <div class="wechat-content">
      <!-- Conversation List -->
      <div v-if="showListPane" class="conversation-list">
        <MobilePageHeader
          title="Messages"
          :fallback-route="{ name: 'homepage-index' }"
        />
        <div v-if="friends.length" class="friend-list">
          <div
            v-for="friend in friends"
            :key="friend.id"
            class="friend-item"
            :class="{ active: selectedFriendId === friend.id }"
            @click="openConversation(friend)"
          >
            <div class="friend-avatar">
              <img
                v-if="friend.character.photo"
                :src="friend.character.photo"
                :alt="friend.character.name"
                class="avatar-img"
              >
              <div v-else class="avatar-placeholder">
                {{ friend.character.name?.slice(0, 1) || "?" }}
              </div>
            </div>
            <div class="friend-info">
              <div class="friend-header">
                <span class="friend-name">{{ friend.character.name }}</span>
                <span class="friend-time">12:30</span>
              </div>
              <div class="friend-message">
                <span class="message-preview">{{ friend.character.profile || "No profile yet." }}</span>
              </div>
            </div>
          </div>
        </div>

        <div
          v-else-if="!loadingFriends && !friendsError"
          class="empty-state"
        >
          <div class="empty-icon">💬</div>
          <p class="empty-title">No conversations yet</p>
          <p class="empty-desc">Add friends to start chatting</p>
          <button
            type="button"
            class="go-home-btn"
            @click="openHomepage"
          >
            Go to homepage
          </button>
        </div>

        <div
          v-if="friendsError"
          class="error-message"
        >
          {{ friendsError }}
        </div>

        <div class="load-more">
          <div v-if="loadingFriends" class="loading">
            <span class="loading-spinner"></span>
          </div>
          <button
            v-else-if="hasMoreFriends"
            type="button"
            class="load-more-btn"
            @click="loadMoreFriends"
          >
            Load more
          </button>
        </div>
      </div>

      <!-- Chat Area -->
      <div v-if="showChatPane" class="chat-area">
        <template v-if="selectedFriend">
          <!-- Chat Header -->
          <div class="chat-header">
            <button
              v-if="isMobile"
              type="button"
              class="back-btn mobile-only"
              @click="closeConversation"
            >
              <ArrowLeftIcon class="h-5 w-5" />
            </button>
            <div class="chat-avatar">
              <img
                v-if="selectedFriend.character.photo"
                :src="selectedFriend.character.photo"
                :alt="selectedFriend.character.name"
                class="avatar-img"
              >
              <div v-else class="avatar-placeholder">
                {{ selectedFriend.character.name?.slice(0, 1) || "?" }}
              </div>
            </div>
            <div class="chat-info">
              <h3 class="chat-name">{{ selectedFriend.character.name }}</h3>
              <p class="chat-status">{{ isThinking ? "Thinking..." : "Online" }}</p>
            </div>
            <div class="chat-actions">
              <button type="button" class="action-btn">
                <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z"></path>
                </svg>
              </button>
              <button type="button" class="action-btn">
                <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 5v.01M12 12v.01M12 19v.01M12 6a1 1 0 110-2 1 1 0 010 2zm0 7a1 1 0 110-2 1 1 0 010 2zm0 7a1 1 0 110-2 1 1 0 010 2z"></path>
                </svg>
              </button>
            </div>
          </div>

          <!-- Chat Messages -->
          <div class="chat-messages">
            <ChatHistory
              :key="selectedFriend.id"
              ref="chat-history-ref"
              class="chat-history"
              :history="history"
              :friendId="selectedFriend.id"
              :character="selectedFriend.character"
              @pushBackFrontMessage="handlePushFrontMessage"
            />
          </div>

          <!-- Chat Input -->
          <div class="chat-input-container">
            <InputField
              :key="`input-${selectedFriend.id}`"
              :friendId="selectedFriend.id"
              variant="page"
              @pushBackMessage="handlePushBackMessage"
              @addToLastMessage="handleAddToLastMessage"
              @updateProcessing="handleUpdateProcessing"
            />
          </div>
        </template>

        <div v-else class="chat-placeholder">
          <div class="placeholder-content">
            <div class="placeholder-icon">💬</div>
            <h3>WeChat</h3>
            <p>Select a conversation to start chatting</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.wechat-container {
  height: 100vh;
  background: #f5f5f5;
  display: flex;
  flex-direction: column;
}

.wechat-navbar {
  height: 64px;
  background: #ededed;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 16px;
  border-bottom: 1px solid #d9d9d9;
  position: relative;
  z-index: 10;
}

.navbar-left,
.navbar-right {
  width: 60px;
  display: flex;
  align-items: center;
}

.navbar-center {
  flex: 1;
  text-align: center;
}

.navbar-title {
  font-size: 17px;
  font-weight: 600;
  color: #111;
  margin: 0;
}

.back-btn {
  background: none;
  border: none;
  padding: 8px;
  cursor: pointer;
  color: #07c160;
  display: flex;
  align-items: center;
  justify-content: center;
}

.nav-btn {
  background: none;
  border: none;
  padding: 8px;
  cursor: pointer;
  color: #333;
  display: flex;
  align-items: center;
  justify-content: center;
}

.wechat-content {
  flex: 1;
  display: flex;
  overflow: hidden;
}

.conversation-list {
  width: 100%;
  background: #f5f5f5;
  display: flex;
  flex-direction: column;
}

.friend-list {
  flex: 1;
  overflow-y: auto;
}

.friend-item {
  display: flex;
  align-items: center;
  padding: 12px 16px;
  background: white;
  border-bottom: 1px solid #e5e5e5;
  cursor: pointer;
  transition: background-color 0.2s;
}

.friend-item:hover {
  background: #f5f5f5;
}

.friend-item.active {
  background: #ebebeb;
}

.friend-avatar {
  width: 48px;
  height: 48px;
  margin-right: 12px;
  flex-shrink: 0;
}

.avatar-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  border-radius: 4px;
}

.avatar-placeholder {
  width: 100%;
  height: 100%;
  background: #ddd;
  border-radius: 4px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 18px;
  font-weight: 600;
  color: #999;
}

.friend-info {
  flex: 1;
  min-width: 0;
}

.friend-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 4px;
}

.friend-name {
  font-size: 16px;
  font-weight: 500;
  color: #111;
}

.friend-time {
  font-size: 12px;
  color: #999;
}

.friend-message {
  display: flex;
  align-items: center;
}

.message-preview {
  font-size: 14px;
  color: #999;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.empty-state {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 40px 20px;
  text-align: center;
}

.empty-icon {
  font-size: 48px;
  margin-bottom: 16px;
}

.empty-title {
  font-size: 18px;
  font-weight: 500;
  color: #333;
  margin-bottom: 8px;
}

.empty-desc {
  font-size: 14px;
  color: #999;
  margin-bottom: 20px;
}

.go-home-btn {
  background: #07c160;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 4px;
  font-size: 14px;
  cursor: pointer;
}

.error-message {
  padding: 16px;
  background: #fff2f0;
  border: 1px solid #ffccc7;
  border-radius: 4px;
  color: #ff4d4f;
  font-size: 14px;
  margin: 16px;
}

.load-more {
  padding: 16px;
  text-align: center;
}

.loading {
  display: flex;
  justify-content: center;
}

.loading-spinner {
  width: 20px;
  height: 20px;
  border: 2px solid #f3f3f3;
  border-top: 2px solid #07c160;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.load-more-btn {
  background: white;
  border: 1px solid #e5e5e5;
  padding: 8px 16px;
  border-radius: 4px;
  font-size: 14px;
  color: #333;
  cursor: pointer;
}

.chat-area {
  flex: 1;
  display: flex;
  flex-direction: column;
  background: white;
}

.chat-header {
  height: 64px;
  background: #f8f8f8;
  display: flex;
  align-items: center;
  padding: 0 16px;
  border-bottom: 1px solid #e5e5e5;
}

.chat-avatar {
  width: 40px;
  height: 40px;
  margin-right: 12px;
  flex-shrink: 0;
}

.chat-info {
  flex: 1;
  min-width: 0;
}

.chat-name {
  font-size: 16px;
  font-weight: 600;
  color: #111;
  margin: 0;
}

.chat-status {
  font-size: 12px;
  color: #07c160;
  margin: 0;
}

.chat-actions {
  display: flex;
  gap: 8px;
}

.action-btn {
  background: none;
  border: none;
  padding: 8px;
  cursor: pointer;
  color: #333;
  display: flex;
  align-items: center;
  justify-content: center;
}

.chat-messages {
  flex: 1;
  overflow-y: auto;
  background: #f5f5f5;
}

.chat-history {
  background: transparent !important;
  border-radius: 0 !important;
  box-shadow: none !important;
  backdrop-filter: none !important;
}

.chat-input-container {
  background: #f8f8f8;
  padding: 8px 16px;
  border-top: 1px solid #e5e5e5;
}

.chat-placeholder {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #f5f5f5;
}

.placeholder-content {
  text-align: center;
}

.placeholder-icon {
  font-size: 64px;
  margin-bottom: 16px;
}

.placeholder-content h3 {
  font-size: 24px;
  font-weight: 500;
  color: #333;
  margin-bottom: 8px;
}

.placeholder-content p {
  font-size: 14px;
  color: #999;
  margin: 0;
}

/* Desktop responsive */
@media (min-width: 768px) {
  .conversation-list {
    width: 320px;
    border-right: 1px solid #e5e5e5;
  }
  
  .chat-area {
    flex: 1;
  }
  
  .mobile-only {
    display: none !important;
  }
}

/* Mobile responsive */
@media (max-width: 767px) {
  .conversation-list {
    width: 100%;
  }
  
  .chat-area {
    width: 100%;
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    z-index: 5;
  }
}
</style>
