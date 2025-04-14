<template>
  <a-page-header
    title="Survey Response"
    style="border-bottom: 1px solid rgb(235, 237, 240)"
    @back="$router.push('/responses')"
  />

  <main class="spacing">
    <div v-if="responsesLoading" class="vertical-spacing" style="text-align: center">
      <a-spin />
    </div>

    <div v-else>
      <div v-if="response" class="spacing">
        <a-row :gutter="[16, 24]">
          <a-col class="gutter-row" :xs="24" :md="12">
            <a-typography-title :level="5">Full name</a-typography-title>
            <a-typography-text type="secondary">{{ response.full_name }}</a-typography-text>
          </a-col>

          <a-col class="gutter-row" :xs="24" :md="12">
            <a-typography-title :level="5">Email Address</a-typography-title>
            <a-typography-text type="secondary">{{ response.email_address }}</a-typography-text>
          </a-col>

          <a-col class="gutter-row" :xs="24" :md="12">
            <a-typography-title :level="5">Gender</a-typography-title>
            <a-typography-text type="secondary">{{ response.gender }}</a-typography-text>
          </a-col>

          <a-col class="gutter-row" :xs="24" :md="12">
            <a-typography-title :level="5">Programming Stack</a-typography-title>
            <a-typography-text type="secondary">{{ response.programming_stack }}</a-typography-text>
          </a-col>

          <a-col class="gutter-row" :xs="24" :md="12">
            <a-typography-title :level="5">Description</a-typography-title>
            <a-typography-text type="secondary">{{ response.description }}</a-typography-text>
          </a-col>

          <a-col class="gutter-row" :xs="24" :md="12">
            <a-typography-title :level="5">Certificates</a-typography-title>
            <div v-for="certificate in response.certificates">
              <a-typography-link
                :href="`${apiEndpoint}/questions/responses/certificates/${certificate.id}`"
                target="_blank"
              >
                {{ certificate.name }}
              </a-typography-link>
            </div>
          </a-col>
        </a-row>
      </div>

      <div v-else>
        <a-alert
          message="Error"
          description="The response was not found!"
          type="error"
          show-icon
        />
      </div>
    </div>
  </main>
</template>

<script setup lang="ts">
import { useResponseStore } from '@/stores/response'
import { message } from 'ant-design-vue'
import { storeToRefs } from 'pinia'
import { onMounted, ref } from 'vue'

const responseStore = useResponseStore()
const { responses } = storeToRefs(responseStore)

const props = defineProps<{
  id: string
}>()

const apiEndpoint = import.meta.env.VITE_API_ENDPOINT

const response: any = ref(null)
const responsesLoading = ref(false)

onMounted(async () => {
  const responseId = Number(props.id)

  if (responses.value.length === 0) {
    responsesLoading.value = true

    const responsesRes = await responseStore.getResponses()

    if (responsesRes.status === 200) {
      responseStore.$patch({
        responses: responsesRes.responses,
      })    

      response.value = responses.value.find((res: any) => res.id === responseId)
    } else {
      message.error('Failed to fetch survey responses!')
    }

    responsesLoading.value = false
  } else {
    response.value = responses.value.find((res: any) => res.id === responseId)
  }
})
</script>

<style scoped></style>
