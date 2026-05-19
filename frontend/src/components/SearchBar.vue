<script setup>
import { ref, watch, computed, onMounted, onBeforeUnmount } from 'vue';
import { useAuthStore } from '../stores/auth';
import apiClient from '../axios';
import CompanyInfo from './CompanyComponent/CompanyInfo.vue';
import StudentInfo from './StudentComponent/StudentInfo.vue';
import DriveInfo from './DriveComponent/DriveInfo.vue';

const authStore = useAuthStore()
const userRole  = authStore.getUserRole() // "Admin" | "Company" | "Student"
const userId    = authStore.getUserId()

// ── Tab config ────────────────────────────────────────────────────────────────
// Admin  : Drive | Student | Company
// Company: Drive  (own drives only)
// Student: Drive  (open only) | Company
const allTabs = [
  { key: 'drive',   label: 'Drive'   },
  { key: 'student', label: 'Student' },
  { key: 'company', label: 'Company' },
]

const visibleTabs = computed(() => {
  if (userRole === 'Admin')   return allTabs
  if (userRole === 'Company') return allTabs.filter(t => t.key === 'drive')
  if (userRole === 'Student') return allTabs.filter(t => t.key === 'drive' || t.key === 'company')
  return []
})

const activeTab = ref(visibleTabs.value[0]?.key ?? 'drive')

// ── Search input — the bar itself acts as the name/title field ────────────────
const searchText = ref('')

// ── Drive-only extra filters (not available to Student, status not for Company) ─
const driveJobType = ref('')
const driveStatus  = ref('')

// ── Modal visibility ──────────────────────────────────────────────────────────
const isOpen       = ref(false)
const searchBarRef = ref(null)

function openModal() { isOpen.value = true }

function handleClickOutside(e) {
  if (searchBarRef.value && !searchBarRef.value.contains(e.target)) {
    isOpen.value = false
  }
}
onMounted(()       => document.addEventListener('mousedown', handleClickOutside))
onBeforeUnmount(() => document.removeEventListener('mousedown', handleClickOutside))

// ── Results ───────────────────────────────────────────────────────────────────
const results = ref([])
const loading = ref(false)
const error   = ref(null)

// ── Info-view state ───────────────────────────────────────────────────────────
const selectedDrive   = ref(null)
const selectedStudent = ref(null)
const selectedCompany = ref(null)
const showDriveInfo   = ref(false)
const showStudentInfo = ref(false)
const showCompanyInfo = ref(false)

function openResult(item) {
  isOpen.value = false
  if (activeTab.value === 'drive') {
    selectedDrive.value = item
    showDriveInfo.value = true
  } else if (activeTab.value === 'student') {
    selectedStudent.value = item
    showStudentInfo.value = true
  } else if (activeTab.value === 'company') {
    selectedCompany.value = item
    showCompanyInfo.value = true
  }
}

// ── Fetch ─────────────────────────────────────────────────────────────────────
function buildParams(obj) {
  const p = new URLSearchParams()
  Object.entries(obj).forEach(([k, v]) => {
    if (v !== '' && v !== null && v !== undefined) p.append(k, v)
  })
  return p.toString()
}

async function fetchResults() {
  error.value   = null
  results.value = []

  let url = ''

  if (activeTab.value === 'drive') {
    const params = { title: searchText.value }
    if (userRole === 'Company') {
      // Company sees only their own drives
      params.company_id = userId
    } else if (userRole === 'Student') {
      // Student sees only open drives; no status selector exposed
      params.status = 'open'
    } else {
      // Admin can filter by job_type and status
      if (driveJobType.value) params.job_type = driveJobType.value
      if (driveStatus.value)  params.status   = driveStatus.value
    }
    const q = buildParams(params)
    url = `/api/v1/drives/${q ? '?' + q : ''}`

  } else if (activeTab.value === 'student') {
    // Admin only — name search
    const q = buildParams({ name: searchText.value })
    url = `/api/v1/students/${q ? '?' + q : ''}`

  } else if (activeTab.value === 'company') {
    // Admin + Student — name search
    const q = buildParams({ name: searchText.value })
    url = `/api/v1/company/${q ? '?' + q : ''}`
  }

  if (!url) return

  loading.value = true
  try {
    const response = await apiClient(url)
    if (!response.status === 200) throw new Error(`HTTP ${response.status}`)
    results.value = await response.data;
  } catch {
    error.value = 'Failed to fetch results.'
  } finally {
    loading.value = false
  }
}

// Fetch on any change
watch([searchText, activeTab, driveJobType, driveStatus], fetchResults)
watch(isOpen, (val) => { if (val) fetchResults() })

function switchTab(key) {
  activeTab.value    = key
  driveJobType.value = ''
  driveStatus.value  = ''
  results.value      = []
}

// ── Display helpers ───────────────────────────────────────────────────────────
function resultTitle(item) {
  if (activeTab.value === 'drive')   return item.title           ?? item.id
  if (activeTab.value === 'student') return `${item.first_name} ${item.last_name}`            ?? item.email ?? item.id
  if (activeTab.value === 'company') return item.registered_name ?? item.name  ?? item.id
  return item.id
}

function resultSubtitle(item) {
  if (activeTab.value === 'drive')
    return [item.job_type, item.status, item.company?.registered_name].filter(Boolean).join(' · ')
  if (activeTab.value === 'student')
    return [item.branch?.name, item.academic_degree?.name, item.year ? `Year ${item.year}` : ''].filter(Boolean).join(' · ')
  if (activeTab.value === 'company')
    return [item.industry?.name, item.status, item.location].filter(Boolean).join(' · ')
  return ''
}

const inputPlaceholder = computed(() => {
  if (activeTab.value === 'drive')   return 'Search drives by title…'
  if (activeTab.value === 'student') return 'Search students by name…'
  if (activeTab.value === 'company') return 'Search companies by name…'
  return 'Search…'
})
</script>

<template>
  <div class="search" ref="searchBarRef">

    <!-- Main search bar — name/title input -->
    <input
      v-model="searchText"
      type="text"
      :placeholder="inputPlaceholder"
      class="search-input"
      @focus="openModal"
    />

    <!-- Search modal -->
    <Transition name="fade">
      <div v-if="isOpen" class="search-modal">

        <!-- Tabs -->
        <div class="tabs">
          <button
            v-for="tab in visibleTabs"
            :key="tab.key"
            class="tab-btn"
            :class="{ active: activeTab === tab.key }"
            @click="switchTab(tab.key)"
          >
            {{ tab.label }}
          </button>
        </div>

        <!-- Drive extra filters: shown only for Admin and Company -->
        <!-- Company: only job_type, no status selector -->
        <!-- Student: no filters at all — open drives only, hint shown instead -->
        <div
          v-if="activeTab === 'drive' && userRole !== 'Student'"
          class="filters"
        >
          <select v-model="driveJobType" class="filter-select">
            <option value="">All job types</option>
            <option value="full-time">Full Time</option>
            <option value="part-time">Part Time</option>
            <option value="internship">Internship</option>
          </select>

          <select v-if="userRole === 'Admin'" v-model="driveStatus" class="filter-select">
            <option value="">All statuses</option>
            <option value="pending">Pending</option>
            <option value="open">Open</option>
            <option value="closed">Closed</option>
          </select>
        </div>

        <!-- Context hints -->
        <p v-if="activeTab === 'drive' && userRole === 'Student'" class="hint">
          Showing open drives only
        </p>
        <p v-if="activeTab === 'drive' && userRole === 'Company'" class="hint">
          Showing your company's drives
        </p>

        <!-- Results list -->
        <div class="results">
          <div v-if="loading" class="state-msg">Searching…</div>
          <div v-else-if="error" class="state-msg error-msg">{{ error }}</div>
          <div v-else-if="results.length === 0" class="state-msg muted">No results found.</div>
          <ul v-else class="result-list">
            <li
              v-for="item in results"
              :key="item.id"
              class="result-item"
              @click="openResult(item)"
            >
              <span class="result-title">{{ resultTitle(item) }}</span>
              <span class="result-sub">{{ resultSubtitle(item) }}</span>
            </li>
          </ul>
        </div>

      </div>
    </Transition>

    <!-- Info views -->
    <DriveInfo
      v-if="showDriveInfo"
      :drive-info="selectedDrive"
      :applied-drive="new Set()"
    />

    <StudentInfo
      v-if="showStudentInfo"
      :show="showStudentInfo"
      :student-data="selectedStudent"
      @close="showStudentInfo = false"
    />

    <CompanyInfo
      v-if="showCompanyInfo"
      :show="showCompanyInfo"
      :company-data="selectedCompany"
      @close="showCompanyInfo = false"
    />

  </div>
</template>

<style scoped>
.search {
  margin: 20px;
  position: relative;
  display: inline-block;
}

/* Search bar */
.search-input {
  height: 35px;
  width: 350px;
  border-radius: 25px;
  border: 1px solid rgba(20, 20, 20, 0.233);
  padding: 5px 16px;
  background-color: white;
  color: rgba(0, 0, 0, 0.6);
  font-size: 1em;
  outline: none;
  box-sizing: border-box;
  transition: border-color 0.2s;
}

.search-input:focus {
  border-color: rgba(0, 0, 0, 0.4);
}

/* Modal */
.search-modal {
  position: absolute;
  top: calc(100% + 8px);
  left: 0;
  width: 420px;
  background: #fff;
  border-radius: 12px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.15);
  z-index: 1000;
  overflow: hidden;
}

/* Tabs */
.tabs {
  display: flex;
  border-bottom: 1px solid #eee;
  padding: 8px 12px 0;
  gap: 4px;
}

.tab-btn {
  padding: 6px 14px;
  border: none;
  background: transparent;
  font-size: 0.9em;
  color: #888;
  cursor: pointer;
  border-radius: 6px 6px 0 0;
  border-bottom: 2px solid transparent;
  transition: color 0.15s, border-color 0.15s;
}

.tab-btn:hover { color: #333; }

.tab-btn.active {
  color: var(--primary-highlight-color);
  border-bottom-color: var(--accent-bar-color);
  font-weight: 600;
}

/* Extra filters row */
.filters {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  padding: 10px 14px 4px;
}

.filter-select {
  flex: 1 1 140px;
  height: 32px;
  border: 1px solid #ddd;
  border-radius: 6px;
  padding: 0 10px;
  font-size: 0.85em;
  outline: none;
  color: #333;
  background: #fafafa;
  cursor: pointer;
}

.filter-select:focus {
  border-color: #4f46e5;
  background: #fff;
}

/* Context hint */
.hint {
  font-size: 0.75em;
  color: #9b8fe0;
  padding: 6px 16px 0;
  margin: 0;
  font-style: italic;
}

/* Results */
.results {
  max-height: 320px;
  overflow-y: auto;
  padding: 8px 0 4px;
}

.state-msg {
  text-align: center;
  padding: 20px;
  font-size: 0.9em;
  color: #999;
}

.error-msg { color: #e53e3e; }
.muted { color: #bbb; }

.result-list {
  list-style: none;
  margin: 0;
  padding: 0;
}

.result-item {
  display: flex;
  flex-direction: column;
  padding: 10px 16px;
  cursor: pointer;
  transition: background 0.1s;
  border-bottom: 1px solid #f3f3f3;
}

.result-item:last-child { border-bottom: none; }

.result-item:hover { background: #f5f3ff; }

.result-title {
  font-size: 0.95em;
  font-weight: 500;
  color: #1a1a1a;
}

.result-sub {
  font-size: 0.78em;
  color: #888;
  margin-top: 2px;
}

/* Transitions */
.fade-enter-active,
.fade-leave-active { transition: opacity 0.15s, transform 0.15s; }
.fade-enter-from,
.fade-leave-to     { opacity: 0; transform: translateY(-6px); }
</style>