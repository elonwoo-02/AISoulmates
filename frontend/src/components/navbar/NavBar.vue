<script setup>

import MenuIcon from "@/components/navbar/icons/MenuIcon.vue";
import HomepageIcon from "@/components/navbar/icons/HomepageIcon.vue";
import FriendIcon from "@/components/navbar/icons/FriendIcon.vue";
import CreateIcon from "@/components/navbar/icons/CreateIcon.vue";
import SettingIcon from "@/components/navbar/icons/SettingIcon.vue";
import SearchIcon from "@/components/navbar/icons/SearchIcon.vue";
import CompactIcon from "@/components/navbar/icons/CompactIcon.vue";
import NewIcon from "@/components/navbar/icons/NewIcon.vue";

import { ref, computed } from 'vue'
import {useUserStore} from "@/stores/user.js";
import UserMenu from "@/components/navbar/UserMenu.vue";

// 模拟数据：7列（周日~周六）× 5行（5周）
const data = ref([
  [0, 1, 3, 2, 5, 4, 6],
  [2, 4, 5, 1, 0, 3, 2],
  [3, 2, 4, 5, 1, 0, 3],
  [1, 0, 2, 3, 4, 5, 1],
  [0, 1, 2, 3, 1, 0, 2],
])

// 找出最大值，用于颜色归一化
const maxVal = computed(() => Math.max(...data.value.flat()))

// 根据数值返回 Tailwind 背景颜色
const getColor = (val) => {
  if (val === 0) return 'bg-gray-200'
  const intensity = Math.ceil((val / maxVal.value) * 4) // 1~4
  switch (intensity) {
    case 1: return 'bg-gray-200'
    case 2: return 'bg-gray-400'
    case 3: return 'bg-gray-600'
    case 4: return 'bg-gray-800'
  }
}

const user = useUserStore()

</script>

<template>
  <div class="drawer lg:drawer-open">
    <input id="my-drawer-4" type="checkbox" class="drawer-toggle" />

    <div class="drawer-content">
      <!-- Navbar -->
      <nav class="navbar w-full bg-base-100 shadow-sm">
        <div class="navbar-start">
<!--          <label for="my-drawer-4" aria-label="open sidebar" class="btn btn-square btn-ghost">-->
<!--            <MenuIcon/>-->
<!--          </label>-->
          <div class="dropdown dropdown-hover">
            <div tabindex="0" role="button" class="px-0 font-bold text-xl">AISoulmates</div>
            <ul tabindex="-1" class="dropdown-content menu bg-base-100 rounded-box z-1 w-52 p-2 shadow-sm">
              <li><a>Item 1</a></li>
              <li><a>Item 2</a></li>
            </ul>
          </div>
<!--          <div class="px-2 font-bold text-xl">AISoulmates</div>-->
        </div>

        <div class="navbar-center flex justify-center w-full max-w-150">
          <div class="join w-4/5 flex justify-center">
            <input class="input join-item rounded-l-full w-4/5" placeholder="Search" />
            <button class="btn join-item rounded-r-full">
              <SearchIcon/>
            </button>
          </div>
        </div>

        <div class="navbar-end">
          <RouterLink v-if="user.isLogin()"  :to="{name:'create-index'}"  class="btn btn-ghost text-lg hover-3d py-1">
            <CreateIcon/>
          </RouterLink>

          <RouterLink v-if="user.isLogin()" :to="{name:'new-index'}" class="btn btn-ghost text-lg hover-3d py-1">
            <NewIcon/>
          </RouterLink>

          <RouterLink v-if="user.hasPulledUserInfo && !user.isLogin()" :to="{name: 'user-account-login-index'}" active-class="btn-active" class="btn btn-ghost text-lg">
            Sign in
          </RouterLink>

          <UserMenu v-else-if="user.isLogin()"/>

        </div>
      </nav>
      <!-- Page content here -->
      <slot></slot>
    </div>

    <div class="drawer-side is-drawer-close:overflow-visible">
      <label for="my-drawer-4" aria-label="close sidebar" class="drawer-overlay"></label>

      <div class="flex min-h-full flex-col items-start bg-base-200 is-drawer-close:w-16 is-drawer-open:w-54">
        <!-- Sidebar content here -->
        <ul class="menu w-full grow">
          <li>
            <label for="my-drawer-4" aria-label="open sidebar" class="flex group">
              <CompactIcon class="is-drawer-close:ml-0 is-drawer-close:group-hover:hidden"/>
              <MenuIcon class="is-drawer-open:ml-auto is-drawer-close:hidden group-hover:inline-block" />
            </label>
          </li>
          <li></li>
          <!-- heatmap -->
          <li>
            <div class="flex flex-col gap-1 p-4 is-drawer-close:hidden">
              <div
                v-for="(week, rowIndex) in data"
                :key="rowIndex"
                class="flex gap-1"
              >
                <div
                  v-for="(dayVal, colIndex) in week"
                  :key="colIndex"
                  :class="['w-4 h-4 rounded', getColor(dayVal)]"
                  :title="`Value: ${dayVal}`"
                ></div>
              </div>
            </div>
          </li>
          <li class="is-drawer-close:hidden"></li>
          <li>
            <RouterLink :to="{name: 'homepage-index'}" active-class="menu-focus" class="is-drawer-close:tooltip is-drawer-close:tooltip-right py-3" data-tip="Homepage">
              <!-- Home icon -->
              <homepage-icon/>
              <span class="is-drawer-close:hidden text-base ml-2 whitespace-nowrap">Home</span>
            </RouterLink>
          </li>

          <li>
            <RouterLink :to="{name: 'friend-index'}" active-class="menu-focus" class="is-drawer-close:tooltip is-drawer-close:tooltip-right py-3" data-tip="Friend">
              <friend-icon/>
              <span class="is-drawer-close:hidden text-base ml-2 whitespace-nowrap">Friends</span>
            </RouterLink>
          </li>

          <li>
            <RouterLink :to="{name:'create-index'}" active-class="menu-focus" class="is-drawer-close:tooltip is-drawer-close:tooltip-right py-3" data-tip="Create">
              <create-icon/>
              <span class="is-drawer-close:hidden text-base ml-2 whitespace-nowrap">Create</span>
            </RouterLink>
          </li>

          <li>
            <RouterLink :to="{name:'setting-index'}" active-class="menu-focus" class="is-drawer-close:tooltip is-drawer-close:tooltip-right py-3" data-tip="Settings">
              <!-- Settings icon -->
              <setting-icon/>
            <span class="is-drawer-close:hidden text-base ml-2 whitespace-nowrap">Settings</span>
            </RouterLink>
          </li>

        </ul>
      </div>
    </div>
  </div>
</template>

<style scoped>

</style>