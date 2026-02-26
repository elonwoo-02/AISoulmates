<script setup>
import { computed, nextTick, ref, useTemplateRef } from "vue";
import { useUserStore } from "@/stores/user.js";
import UpdateIcon from "@/components/character/icons/UpdateIcon.vue";
import RemoveIcon from "@/components/character/icons/RemoveIcon.vue";
import HeartIcon from "@/components/character/icons/HeartIcon.vue";
import api from "@/js/http/api.js";
import ChatField from "@/components/character/chat_field/ChatField.vue";
import { useRouter } from "vue-router";

const props = defineProps(["character", "canEdit", "canRemoveFriend", "friendId"]);
const emit = defineEmits(["remove"]);
const isHover = ref(false);
const user = useUserStore();
const router = useRouter();
const likeCount = computed(() => props.character?.like_count ?? props.character?.likes ?? 0);

async function handleRemoveCharacter() {
  try {
    const res = await api.post('/api/create/character/remove/', {
      character_id: props.character.id,
    })
    if (res.data.result === 'success') {
      emit('remove', props.character.id)
    }
  } catch {
    // Keep silent to match current behavior.
  }
}

async function handleRemoveFriend() {
  try {
    const res = await api.post('/api/friend/remove/', {
      friend_id: props.friendId
    })
    if (res.data.result === 'success') {
      emit('remove', props.friendId)
    }
  } catch (err) {

  }
}


const chatFieldRef = useTemplateRef("chat-field-ref");
const friend = ref(null);

async function openChatField() {
  if (!user.isLogin()) {
    await router.push({
      name: 'user-account-login-index'
    })
  } else {
    try {
      const res = await api.post('/api/friend/get_or_create/', {
        character_id: props.character.id
      })
      const data = res.data
      if (data.result === 'success') {
        friend.value = data.friend
        // Use nextTick to ensure DOM is updated before showing modal
        await nextTick()
        chatFieldRef.value?.showModal()
      }
    } catch (err) {
      console.error("Error opening chat field:", err);
    }
  }
}
</script>

<template>
  <article
    class="group mb-6 cursor-pointer break-inside-avoid overflow-hidden rounded-3xl border border-black/5 bg-white shadow-[0_12px_30px_-20px_rgba(15,23,42,0.35)] transition-all duration-200 hover:-translate-y-0.5 hover:shadow-[0_18px_40px_-24px_rgba(15,23,42,0.45)]"
    @mouseover="isHover = true"
    @mouseleave="isHover = false" @click="openChatField"
  >
    <div class="relative aspect-[3/5] overflow-hidden bg-[var(--surface-muted)]">
      <img
        :src="character.background_image"
        class="h-full w-full object-cover transition-transform duration-300"
        :class="{ 'scale-105': isHover }"
        alt="character background"
        loading="lazy"
        decoding="async"
      />
      <div class="absolute inset-0 bg-gradient-to-t from-black/70 via-black/20 to-transparent"></div>

      <div
        v-if="canEdit && character.author.user_id === user.id"
        class="absolute right-2 top-2 flex gap-1 opacity-0 transition-opacity group-hover:opacity-100"
      >
        <RouterLink :to="{ name: 'update-character', params: { character_id: character.id } }" class="btn btn-circle btn-ghost btn-xs bg-black/35 text-white hover:bg-black/55">
          <UpdateIcon />
        </RouterLink>
        <button @click.stop="handleRemoveCharacter" class="btn btn-circle btn-ghost btn-xs bg-black/35 text-white hover:bg-black/55">
          <RemoveIcon />
        </button>
      </div>

      <div v-if="canRemoveFriend" class="absolute right-0 top-1">
        <button @click.stop="handleRemoveFriend" class="btn btn-circle btn-ghost btn-xs bg-black/35 text-white hover:bg-black/55">
          <RemoveIcon />
        </button>
      </div>

      <div class="absolute bottom-0 left-0 right-0 p-4 text-white">
        <h3 class="line-clamp-2 text-base font-semibold leading-5 tracking-tight">{{ character.name }}</h3>
        <p class="line-clamp-2 mt-1 text-xs text-white/80">{{ character.profile }}</p>
      </div>
    </div>

    <div class="flex items-center justify-between px-4 py-3">
      <RouterLink
        :to="{ name: 'user-space-index', params: { user_id: character.author.user_id } }"
        class="inline-flex items-center gap-2 text-xs font-medium text-[var(--text-secondary)] hover:text-[var(--text-primary)]"
        @click.stop
      >
        <span class="avatar">
          <span class="h-7 w-7 overflow-hidden rounded-full">
            <img :src="character.author.photo" alt="author avatar" class="h-full w-full object-cover" loading="lazy" decoding="async" />
          </span>
        </span>
        <span class="max-w-[120px] truncate">{{ character.author.username }}</span>
      </RouterLink>

      <div class="flex items-center gap-1 text-xs font-semibold text-[var(--accent-yellow)]">
        <HeartIcon />
        <span>{{ likeCount }}</span>
      </div>
      <ChatField ref="chat-field-ref" :friend="friend"/>
    </div>
  </article>
</template>

<style scoped>
.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>
