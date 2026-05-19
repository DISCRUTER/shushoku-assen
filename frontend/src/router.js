import { createWebHistory, createRouter } from 'vue-router'

import { useAuthStore } from './stores/auth'

import DashboardView from './components/DashboardPage/DashboardView.vue'
import DriveView from './components/DriveComponent/DriveView.vue'
import CompanyView from './components/CompanyComponent/CompanyView.vue'
import HomeView from './components/LandingPage/HomeView.vue'
import StudentView from './components/StudentComponent/StudentView.vue'
import UtilsView from './components/UtilsComponent/UtilsView.vue'
import ActionView from './components/ActionComponent/ActionView.vue'

const routes = [
  {
    path: '/',
    component: HomeView,
    meta: {
      guestOnly: true,
      title: 'Home'
    }
  },
  {
    path: '/dashboard',
    component: DashboardView,
    meta: {
      requiresAuth: true,
      roles: ['Admin', 'Student', 'Company'],
      title: 'Dashboard'
    }
  },
  {
    path: '/drive',
    component: DriveView,
    meta: {
      requiresAuth: true,
      roles: ['Admin', 'Student', 'Company'],
      title: 'Drive'
    }
  },
  {
    path: '/company',
    component: CompanyView,
    meta: {
      requiresAuth: true,
      roles: ['Admin', 'Student'],
      title: 'Company'
    }
  },
  {
    path: '/student',
    component: StudentView,
    meta: {
      requiresAuth: true,
      roles: ['Admin'],
      title: 'Student'
    }
  },
  {
    path: '/utils',
    component: UtilsView,
    meta: {
      requiresAuth: true,
      roles: ['Admin'],
      title: 'Utils'
    }
  },
  {
    path: '/action',
    component: ActionView,
    meta: {
      requiresAuth: true,
      roles: ['Admin', 'Student', 'Company'],
      title: 'Action Center'
    }
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
});

router.beforeEach((to, from, next) => {
  const auth = useAuthStore();

  if (to.meta.requiresAuth && !auth.getUserId()) {
    return next('/');
  }

  if (to.meta.roles && !to.meta.roles.includes(auth.getUserRole())) {
    return next('/');
  }

  if (to.meta.guestOnly && auth.getUserId()) {
    const role = auth.getUserRole();
    if (['Admin', 'Student', 'Company'].includes(role)) {
      return next('/dashboard');
    }
    return next();
  }
  document.title = to.meta.title || 'Default App Title';
  next();
});

export default router