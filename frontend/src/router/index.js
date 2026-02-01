import { createRouter, createWebHistory } from 'vue-router'
import FriendIndex from "@/views/friend/FriendIndex.vue";
import CreateIndex from "@/views/create/CreateIndex.vue";
import HomepageIndex from "@/views/homepage/HomepageIndex.vue";
import NotFoundIndex from "@/views/error/NotFoundIndex.vue";
import LoginIndex from "@/views/user/account/LoginIndex.vue";
import RegisterIndex from "@/views/user/account/RegisterIndex.vue";
import SpaceIndex from "@/views/user/space/SpaceIndex.vue";
import ProfileIndex from "@/views/user/profile/ProfileIndex.vue";
import SettingIndex from "@/views/setting/SettingIndex.vue";
import NewIndex from "@/views/new/NewIndex.vue";
import {useUserStore} from "@/stores/user.js";
import Asdf from "@/views/chat/asdf.vue"

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path:'/chat/', // <-- 新增路由
      component: Asdf,
      name:'chat-index',
      meta:{
        needlogin: true,
      },
    },
    {
      path:'/',
      component: HomepageIndex,
      name:'homepage-index',
      meta:{
        needlogin: false,
      },
    },
    {
      path:'/friend/',
      component: FriendIndex,
      name:'friend-index',
      meta: {
        needlogin: true,
      },
    },
    {
      path:'/new/',
      component: NewIndex,
      name:'new-index',
      meta: {
        needlogin: true
      },
    },
    {
      path:'/create/',
      component: CreateIndex,
      name: 'create-index',
      meta: {
        needlogin: true,
      },
    },
    {
      path:'/404/',
      component: NotFoundIndex,
      name:'404',
      meta: {
        needlogin: false
      }
    },
    {
      path:'/user/account/login/',
      component: LoginIndex,
      name:'user-account-login-index',
      meta: {
        needlogin: false,
      },
    },
    {
      path:'/user/account/register/',
      component: RegisterIndex,
      name:'user-account-register-index',
      meta: {
        needlogin: false,
      },
    },
    {
      path:'/user/space/:user_id/',
      component: SpaceIndex,
      name:'user-space-index',
      meta: {
        needlogin: false
      }
    },
    {
      path:'/user/profile/',
      component: ProfileIndex,
      name:'user-profile-index',
      meta: {
        needlogin: true,
      },
    },
    {
      path:'/setting/',
      component: SettingIndex,
      name:'setting-index',
      meta: {
        needlogin: true,
      }
    },
    {
      path:'/:pathMatch(.*)*',
      component: NotFoundIndex,
      name:'not-found',
      meta: {
        needlogin: false,
      },
    },
  ],
})

router.beforeEach((to, from) => {
  const user = useUserStore()
  if (to.meta.needlogin && user.hasPulledUserInfo && !user.isLogin()) {
    return {
      name: 'user-account-login-index'
    }
  }
  return true
})


export default router
