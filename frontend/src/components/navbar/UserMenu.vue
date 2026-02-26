<script setup>
import { useUserStore } from "@/stores/user.js";
import UserSpaceIcon from "@/components/navbar/icons/UserSpaceIcon.vue";
import UserProfileIcon from "@/components/navbar/icons/UserProfileIcon.vue";
import UserLogoutIcon from "@/components/navbar/icons/UserLogoutIcon.vue";
import api from "@/js/http/api.js";
import { useRouter } from "vue-router";

const user = useUserStore()
const router = useRouter()

function closeMenu() {
  const element = document.activeElement
  if (element && element instanceof HTMLElement) element.blur()
}

async function handleLogout() {
  try {
    const res = await api.post('/api/user/account/logout/')
    if (res.data.result === 'success') {
      user.logout()
      await router.push({
        name: 'homepage-index'
      })
    }
  } catch (err) {
  }
}
</script>

<template>
  <div class="dropdown dropdown-end">
    <div tabindex="0" role="button" class="avatar btn btn-circle h-10 w-10 bg-[var(--surface-strong)] p-0 ring-1 ring-black/10 dark:ring-white/15">
      <div class="h-10 w-10 rounded-full overflow-hidden">
        <img :src="user.photo" alt="user avatar">
      </div>
    </div>

    <ul tabindex="-1" class="dropdown-content layer-popover mt-2 w-56 rounded-2xl bg-[var(--surface)] p-2 text-[var(--text)] shadow-[var(--shadow)] ring-1 ring-black/10 dark:ring-white/15">
      <li class="mb-1">
        <RouterLink @click="closeMenu" :to="{name:'user-space-index', params:{ user_id: user.id }}" class="rounded-xl p-2 no-underline hover:no-underline">
          <div class="avatar">
            <div class="w-10 rounded-full overflow-hidden">
              <img :src="user.photo" alt="profile photo">
            </div>
          </div>
          <span class="line-clamp-1 break-all text-sm font-semibold">{{ user.username }}</span>
        </RouterLink>
      </li>

      <li>
        <RouterLink @click="closeMenu" :to="{name:'user-space-index', params:{user_id: user.id}}" class="rounded-xl py-2.5 text-sm no-underline hover:no-underline">
          <UserSpaceIcon />
          User Space
        </RouterLink>
      </li>

      <li>
        <RouterLink @click="closeMenu" :to="{name:'user-profile-index', params:{user_id: user.id}}" class="rounded-xl py-2.5 text-sm no-underline hover:no-underline">
          <UserProfileIcon />
          User Profile
        </RouterLink>
      </li>

      <li class="my-1 h-px bg-[var(--bg-elevated)]"></li>

      <li>
        <a @click="handleLogout" class="rounded-xl py-2.5 text-sm text-rose-500 hover:bg-rose-500/10 no-underline hover:no-underline">
          <UserLogoutIcon />
          Log out
        </a>
      </li>
    </ul>
  </div>
</template>

<style scoped>
.line-clamp-1 {
  display: -webkit-box;
  -webkit-line-clamp: 1;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

:deep(.dropdown-content a),
:deep(.dropdown-content a:hover),
:deep(.dropdown-content a:focus) {
  text-decoration: none;
}
</style>
