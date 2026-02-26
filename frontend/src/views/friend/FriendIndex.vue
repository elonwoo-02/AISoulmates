<script setup>
import {nextTick, onBeforeUnmount, onMounted, ref, useTemplateRef} from "vue";
import api from "@/js/http/api.js";
import Character from "@/components/character/Character.vue";

const friends = ref([])
const loading = ref(false)
const hasFriends = ref(true)
const sentinelRef = useTemplateRef('sentinel-ref')
const error = ref(null)

function checkSentinelVisible() {  // 判断哨兵是否能被看到
  if (!sentinelRef.value) return false

  const rect = sentinelRef.value.getBoundingClientRect()
  return rect.top < window.innerHeight && rect.bottom > 0
}

async function loadMore() {
  if (loading.value || !hasFriends.value) return
  loading.value = true

  let newFriends = []
  try {
    const res = await api.get('/api/friend/get_list/', {
      params: {
        items_count: friends.value.length
      }
    })
    const data = res.data
    if (data.result === 'success') {
      newFriends = data.friends
    }
  } catch(err) {
    console.log(err)
    error.value = 'Failed to load more friends'
  } finally {
    loading.value = false
    if (newFriends.length === 0) {
      hasFriends.value = false
    } else {
      friends.value.push(...newFriends)
      await nextTick()

      if (checkSentinelVisible()) {
        await loadMore()
      }
    }
  }
}

let observer = null
onMounted(async () => {
  await loadMore()  // 加载新元素

  observer = new IntersectionObserver(
    entries => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          loadMore()
        }
      })
    },
    {root: null, rootMargin: '2px', threshold: 0}
  )

  //监听哨兵元素， 每次哨兵被看到时，都会触发一次
  observer.observe(sentinelRef.value)
})

function removeFriend(friendId) {
  friends.value = friends.value.filter(f => f.id !== friendId)
}

onBeforeUnmount(() => {
  observer?.disconnect()  // 解绑监听器
})
</script>

<template>
  <div class="flex flex-col items-center mb-12">
    <div class="grid grid-cols-[repeat(auto-fill,minmax(240px,1fr))] gap-9 mt-12 justify-items-center w-full px-9">
      <Character
        v-for="friend in friends"
        :key="friend.id"
        :character="friend.character"
        :canRemoveFriend="removeFriend"
        :friendId="friend.id"
        @remove="removeFriend"
      />
    </div>

    <div ref="sentinel-ref" class="mt-8 hidden h-2 text-base-100"></div>

    <div v-if="loading" class="mt-4 flex justify-center text-gray-500">
      <span class="loading loading-spinner loading-lg"></span>
    </div>

    <div v-else-if="error" class="alert alert-error mt-4">
      <span>{{ error }}</span>
    </div>
  </div>
</template>

<style scoped>

</style>
