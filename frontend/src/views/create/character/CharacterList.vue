<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import api from '@/js/http/api.js'

const router = useRouter()
const characters = ref([])
const loading = ref(true)
const error = ref('')

onMounted(async () => {
  try {
    const res = await api.get('/api/create/character/list/')
    const data = res.data
    if (data.result === 'success') {
      characters.value = data.characters
    } else {
      error.value = data.result
    }
  } catch (err) {
    error.value = 'Failed to load characters'
  } finally {
    loading.value = false
  }
})

function goToUpdate(characterId) {
  router.push({
    name: 'update-character',
    params: { character_id: characterId }
  })
}

function goToCreate() {
  router.push({
    name: 'create-index'
  })
}
</script>

<template>
  <div class="flex justify-center">
    <div class="card w-120 bg-base-200 shadow-sm mt-1">
      <div class="card-body">
        <h3 class="text-lg font-bold my-4">My Characters</h3>
        
        <div v-if="loading" class="flex justify-center">
          <span class="loading loading-spinner loading-lg"></span>
        </div>
        
        <div v-else-if="error" class="alert alert-error">
          <span>{{ error }}</span>
        </div>
        
        <div v-else-if="characters.length === 0" class="text-center py-8">
          <p class="text-gray-500 mb-4">You haven't created any characters yet</p>
          <button @click="goToCreate" class="btn btn-primary">Create Your First Character</button>
        </div>
        
        <div v-else class="space-y-4">
          <div v-for="character in characters" :key="character.id" 
               class="card bg-base-100 shadow-sm cursor-pointer hover:shadow-md transition-shadow"
               @click="goToUpdate(character.id)">
            <div class="card-body p-4">
              <div class="flex items-center gap-4">
                <div class="avatar">
                  <div class="w-16 h-16 rounded-full">
                    <img :src="character.photo" :alt="character.name" />
                  </div>
                </div>
                <div class="flex-1">
                  <h4 class="font-semibold">{{ character.name }}</h4>
                  <p class="text-sm text-gray-600 line-clamp-2">{{ character.profile }}</p>
                  <p class="text-xs text-gray-400 mt-1">
                    Updated: {{ new Date(character.update_time).toLocaleDateString() }}
                  </p>
                </div>
                <div class="btn btn-ghost btn-sm">
                  Edit
                </div>
              </div>
            </div>
          </div>
          
          <div class="flex justify-center mt-6">
            <button @click="goToCreate" class="btn btn-primary">Create New Character</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>
