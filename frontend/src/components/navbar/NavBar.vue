<script setup>

import MenuIcon from "@/components/navbar/icons/MenuIcon.vue";
import HomepageIcon from "@/components/navbar/icons/HomepageIcon.vue";
import FriendIcon from "@/components/navbar/icons/FriendIcon.vue";
import CreateIcon from "@/components/navbar/icons/CreateIcon.vue";
import SettingIcon from "@/components/navbar/icons/SettingIcon.vue";
import SearchIcon from "@/components/navbar/icons/SearchIcon.vue";
import CompactIcon from "@/components/navbar/icons/CompactIcon.vue";

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

        <div class="navbar-center justify-center w-full max-w-180">
          <div class="join w-4/5 justify-center">
            <input class="input join-item rounded-l-full w-4/5" placeholder="Search" />
            <button class="btn join-item rounded-r-full">
              <SearchIcon/>
            </button>
          </div>
        </div>

        <div class="navbar-end">
          <button class="btn btn-ghost text-lg">Sign in/up</button>
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

          <li>
            <button class="is-drawer-close:tooltip is-drawer-close:tooltip-right py-3" data-tip="Homepage">
              <!-- Home icon -->
              <homepage-icon/>
              <span class="is-drawer-close:hidden text-base ml-2 whitespace-nowrap">Homepage</span>
            </button>
          </li>

          <li>
            <button class="is-drawer-close:tooltip is-drawer-close:tooltip-right py-3" data-tip="Friend">
              <friend-icon/>
              <span class="is-drawer-close:hidden text-base ml-2 whitespace-nowrap">Friends</span>
            </button>
          </li>

          <li>
            <button class="is-drawer-close:tooltip is-drawer-close:tooltip-right py-3" data-tip="Create">
              <create-icon/>
              <span class="is-drawer-close:hidden text-base ml-2 whitespace-nowrap">Create</span>
            </button>
          </li>

          <li>
            <button class="is-drawer-close:tooltip is-drawer-close:tooltip-right py-3" data-tip="Settings">
              <!-- Settings icon -->
              <setting-icon/>
            <span class="is-drawer-close:hidden text-base ml-2 whitespace-nowrap">Settings</span>
            </button>
          </li>

        </ul>
      </div>
    </div>
  </div>
</template>

<style scoped>

</style>