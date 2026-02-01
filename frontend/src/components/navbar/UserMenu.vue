<script setup>
import {useUserStore} from "@/stores/user.js";
import UserSpaceIcon from "@/components/navbar/icons/UserSpaceIcon.vue";
import UserProfileIcon from "@/components/navbar/icons/UserProfileIcon.vue";
import UserLogoutIcon from "@/components/navbar/icons/UserLogoutIcon.vue";
import api from "@/js/http/api.js";
import {useRouter} from "vue-router";

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
    <div tabindex="0" role="button" class="avatar btn btn-circle w-8 h-8 ml-6 mr-6">
      <div class="w-8 rounded-full">
        <img v-if="user.photo" :src="user.photo" alt="avatar">
      </div>
    </div>
    <ul tabindex="-1" class="dropdown-content menu bg-base-100 rounded-box z-1 w-52 p-2 shadow-lg">
      <li>
        <RouterLink @click="closeMenu" :to="{name:'user-space-index', params:{ user_id: user.id }}">
          <div class="avatar">
            <div class="w-10 rounded-full">
              <img
                v-if="user.photo"
                :key="user.photo"
                :src="user.photo"
                alt="avatar"
                class="w-full h-full object-cover"
              />
            </div>
          </div>
          <span class="text-base font-bold line-clamp-1"> {{ user.username }}</span>
        </RouterLink>
      </li>
      <li>
        <RouterLink @click="closeMenu" :to="{name:'user-space-index', params:{user_id: user.id}}" class="text-sm font-bold py-3">
          <UserSpaceIcon/>
          User Space
        </RouterLink>
      </li>
      <li>
        <RouterLink @click="closeMenu" :to="{name:'user-profile-index', params:{user_id: user.id}}" class="text-sm font-bold py-3">
          <UserProfileIcon/>
          User Profile
        </RouterLink>
      </li>
      <li></li>
      <li>
        <a @click="handleLogout" class="text-sm font-bold py-3">
          <UserLogoutIcon/>
          Log out
        </a>
      </li>
    </ul>
  </div>
</template>

<style scoped>

</style>