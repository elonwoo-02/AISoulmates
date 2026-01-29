import {defineStore} from "pinia";
import { ref } from 'vue'

export const useUserStore= defineStore('user', ()=>{
    // const id = ref(0)
    // const username = ref('Elon')
    // const photo = ref('http://127.0.0.1:8000/media/user/photos/default.jpg')
    // const profile = ref('111')
    // const accessToken = ref('111')
    const id = ref(0)
    const username = ref('')
    const photo = ref('')
    const profile = ref('')
    const accessToken = ref('')
    const hasPulledUserInfo = ref(false)

    function isLogin() {
        return !!accessToken.value
    }

    function setAccessToken(token) {
        accessToken.value = token
    }

    function setUserInfo(data) {
        id.value = data.user_id
        username.value = data.username
        photo.value = data.photo
        profile.value = data.profile
    }

    function logout() {
        id.value = 0
        username.value = ''
        photo.value = ''
        profile.value = ''
        accessToken.value = ''
    }

    function setHasPulledUserInfo(newStatus) {
        hasPulledUserInfo.value = newStatus
    }

    return {
        id,
        username,
        photo,
        profile,
        accessToken,
        hasPulledUserInfo,

        isLogin,
        setAccessToken,
        setUserInfo,
        logout,
        setHasPulledUserInfo,
    }
})
