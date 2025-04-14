<template>
  <a-page-header
    title="Survey Responses"
    style="border-bottom: 1px solid rgb(235, 237, 240)"
    @back="$router.push('/')"
  />

  <main class="spacing">
    <div v-if="responsesLoading" class="vertical-spacing" style="text-align: center">
      <a-spin />
    </div>

    <div class="vertical-spacing">
      <a-table :columns="columns" :data-source="responses">
        <template #bodyCell="{ column, record }">
          <template v-if="column.key === 'action'">
            <span>
              <RouterLink :to="`/responses/${record.id}`">View response</RouterLink>
            </span>
          </template>
        </template>
      </a-table>
    </div>
  </main>
</template>

<script setup lang="ts">
import { useResponseStore } from '@/stores/response'
import { message } from 'ant-design-vue'
import { storeToRefs } from 'pinia'
import { onMounted, ref } from 'vue'
import { RouterLink } from 'vue-router'

const responseStore = useResponseStore()
const { responses } = storeToRefs(responseStore)
const responsesLoading = ref(false)

const columns = [
  {
    title: 'Full name',
    dataIndex: 'full_name',
    key: 'full_name',
  },
  {
    title: 'Email address',
    dataIndex: 'email_address',
    key: 'email_address',
  },
  {
    title: 'Action',
    key: 'action',
  },
]

onMounted(async () => {
  responsesLoading.value = true

  const responsesRes = await responseStore.getResponses()

  if (responsesRes.status === 200) {
    responseStore.$patch({
      responses: responsesRes.responses,
    })
  } else {
    message.error('Failed to fetch survey responses!')
  }

  responsesLoading.value = false
})
</script>

<style scoped></style>
