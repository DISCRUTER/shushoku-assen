import { defineStore } from 'pinia';
import { ref, watch } from 'vue';

export const useAuthStore = defineStore('auth', () => {

    const userId = ref(localStorage.getItem('userId') || null);
    const role = ref(localStorage.getItem('role') || null);
    
    watch([userId, role], ([newUserId, newRole]) => {
        if (newUserId) {
            localStorage.setItem('userId', newUserId);
        } else {
            localStorage.removeItem('userId');
        }
    
        if (newRole) {
            localStorage.setItem('role', newRole);
        } else {
            localStorage.removeItem('role');
        }
    })
    
    function setUser(id, userRole) {
        userId.value = id;
        role.value = userRole;
    }
    
    function getUserId() {
        return userId.value;
    }

    function getUserRole() {
        return role.value;
    }
    
    function logout() {
        userId.value = null;
        localStorage.removeItem('userId');
        role.value = null;
        localStorage.removeItem('role');
    }

    return { setUser, getUserId, getUserRole, logout };
});
