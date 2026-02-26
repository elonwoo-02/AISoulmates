<script setup>
import { nextTick, ref, useTemplateRef } from 'vue'
import { useUserStore } from '@/stores/user.js'
import UpdateIcon from '@/components/character/icons/UpdateIcon.vue'
import RemoveIcon from '@/components/character/icons/RemoveIcon.vue'
import api from '@/js/http/api.js'
import ChatField from "@/components/character/chat_field/ChatField.vue";
import { useRouter } from "vue-router";

const props = defineProps(['character', 'canEdit', 'canRemoveFriend', 'friendId'])
const emit = defineEmits(['remove'])
const isHover = ref(false)
const user = useUserStore()
const router = useRouter()
const isClosingChat = ref(false)

async function handleRemoveCharacter() {
  try {
    const res = await api.post('/api/create/character/remove/', {
      character_id: props.character.id,
    })
    if (res.data.result === 'success') {
      emit('remove', props.character.id)
    }
  } catch {
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

const chatFieldRef = useTemplateRef('chat-field-ref')
const friend = ref(null)

async function openChatField() {
  if (isClosingChat.value) return

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
        await nextTick()
        chatFieldRef.value?.showModal()
      }
    } catch (err) {
      console.error('Error opening chat field:', err)
    }
  }
}

function guardClickFromDialog(event) {
  const target = event.target
  if (!(target instanceof HTMLElement)) return false
  return Boolean(target.closest('dialog'))
}

function onCardClick(event) {
  if (guardClickFromDialog(event)) return
  openChatField()
}

function onCardMouseDown(event) {
  const target = event.target
  if (!(target instanceof HTMLElement)) return
  if (target.closest('dialog')) {
    isClosingChat.value = true
    window.setTimeout(() => {
      isClosingChat.value = false
    }, 180)
  }
}
</script>

<template>
  <article
    class="group w-full max-w-[320px] cursor-pointer overflow-hidden rounded-2xl bg-[var(--surface)] text-[var(--text)] shadow-[var(--shadow)] transition duration-200 hover:-translate-y-0.5"
    @mouseover="isHover = true"
    @mouseleave="isHover = false"
    @click="onCardClick"
    @mousedown="onCardMouseDown"
  >
    <div class="relative aspect-[16/10] overflow-hidden bg-[var(--bg-elevated)]">
      <img
        :src="character.background_image"
        class="h-full w-full object-cover transition-transform duration-300"
        :class="{ 'scale-105': isHover }"
        alt="character background"
      />
      <div class="absolute inset-0 bg-gradient-to-t from-black/45 via-black/10 to-transparent"></div>

      <div
        v-if="canEdit && character.author.user_id === user.id"
        class="absolute right-2 top-2 flex gap-1 rounded-full bg-black/20 px-1.5 py-1 opacity-0 backdrop-blur-sm transition-opacity group-hover:opacity-100"
      >
        <RouterLink :to="{ name: 'update-character', params: { character_id: character.id } }" class="btn btn-circle btn-xs bg-transparent text-white hover:bg-white/20" aria-label="Edit character">
          <UpdateIcon />
        </RouterLink>
        <button @click.stop="handleRemoveCharacter" class="btn btn-circle btn-xs bg-transparent text-white hover:bg-white/20" aria-label="Delete character">
          <RemoveIcon />
        </button>
      </div>

      <div v-if="canRemoveFriend" class="absolute right-2 top-2">
        <button @click.stop="handleRemoveFriend" class="btn btn-circle btn-xs bg-black/35 text-white hover:bg-black/55" aria-label="Remove friend">
          <RemoveIcon />
        </button>
      </div>
    </div>

    <div class="p-4">
      <div class="flex items-start gap-3">
        <div class="avatar mt-0.5">
          <div class="h-10 w-10 rounded-full bg-[var(--bg-elevated)]">
            <img :src="character.photo" alt="character avatar" class="object-cover" />
          </div>
        </div>

        <div class="min-w-0 flex-1">
          <h3 class="line-clamp-2 break-all text-[15px] font-semibold leading-5">{{ character.name }}</h3>
          <p class="line-clamp-2 mt-1 text-sm text-[var(--muted)]">{{ character.profile }}</p>

          <RouterLink
            :to="{ name: 'user-space-index', params: { user_id: character.author.user_id } }"
            class="mt-3 inline-flex max-w-full items-center gap-2 rounded-full bg-[var(--surface-strong)] px-2.5 py-1 text-xs text-[var(--muted)] hover:text-[var(--accent)]"
          >
            <span class="avatar">
              <span class="h-5 w-5 overflow-hidden rounded-full">
                <img :src="character.author.photo" alt="author avatar" class="h-full w-full object-cover" />
              </span>
            </span>
            <span class="truncate">{{ character.author.username }}</span>
          </RouterLink>
          <ChatField ref="chat-field-ref" :friend="friend" />
        </div>
      </div>
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
