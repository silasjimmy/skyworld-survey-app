<template>
  <a-page-header
    class="border"
    title="Sky World Survey"
    style="border-bottom: 1px solid rgb(235, 237, 240)"
    :avatar="{ src: 'https://avatars1.githubusercontent.com/u/8186664?s=460&v=4' }"
  >
  </a-page-header>

  <main>
    <a-segmented block v-model:value="currentNavButton" :options="navButtons" />

    <section v-if="currentNavButton === 'Questions'">
      <div v-if="questionsLoading" style="text-align: center">
        <a-spin />
      </div>

      <div v-else>
        <h1>Survey questions</h1>
        <span class="required-desc">required</span>

        <div class="step-content">
          <a-form
            layout="vertical"
            ref="formRef"
            :model="response"
            @finish="submitResponse"
            @finishFailed="submitFailed"
          >
            <div v-for="(question, index) in questions">
              <a-card v-if="currentStep === index">
                <a-form-item
                  :label="question.text"
                  :name="question.name"
                  :rules="[{ required: question.required, message: 'This field is required!' }]"
                >
                  <div v-if="question.description" class="question-description">
                    <a-typography-text type="secondary">
                      {{ question.description }}
                    </a-typography-text>
                  </div>

                  <a-input
                    v-if="question.type === 'short_text'"
                    type="text"
                    v-model:value="response.full_name"
                  />

                  <a-input
                    v-else-if="question.type === 'email'"
                    type="email"
                    v-model:value="response.email_address"
                  />

                  <div v-else-if="question.type === 'long_text'">
                    <a-textarea v-model:value="response.description" />
                  </div>

                  <div v-else-if="question.type === 'single_choice'">
                    <a-radio-group v-model:value="response.gender">
                      <a-radio
                        v-for="option in question.options"
                        :value="option.value"
                        :name="option.label"
                      >
                        {{ option.label }}
                      </a-radio>
                    </a-radio-group>
                  </div>

                  <div v-else-if="question.type === 'multiple_choice'">
                    <a-checkbox-group v-model:value="response.programming_stack">
                      <a-checkbox
                        v-for="option in question.options"
                        :value="option.value"
                        :name="option.label"
                      >
                        {{ option.label }}
                      </a-checkbox>
                    </a-checkbox-group>
                  </div>

                  <div v-else-if="question.type === 'file'">
                    <a-upload
                      multiple
                      accept=".pdf"
                      v-model:file-list="response.certificates"
                      :name="question.name"
                      :before-upload="uploadCertificates"
                      @remove="deleteCertificate"
                    >
                      <a-button>
                        <upload-outlined></upload-outlined>
                        Click to Upload
                      </a-button>
                    </a-upload>
                    <!-- <input multiple type="file" accept=".pdf" :name="question.name"> -->
                  </div>
                </a-form-item>
              </a-card>
            </div>

            <div v-if="currentStep === questions.length">
              <a-typography-title :level="3">Response</a-typography-title>

              <a-typography-title :level="5">Full Name</a-typography-title>
              <a-typography-text type="secondary">{{ response.full_name }}</a-typography-text>

              <a-typography-title :level="5">Email Address</a-typography-title>
              <a-typography-text type="secondary">{{ response.email_address }}</a-typography-text>

              <a-typography-title :level="5">Description</a-typography-title>
              <a-typography-text type="secondary">{{ response.description }}</a-typography-text>

              <a-typography-title :level="5">Gender</a-typography-title>
              <a-typography-text type="secondary">{{ response.gender }}</a-typography-text>

              <a-typography-title :level="5">Programming Stack</a-typography-title>
              <a-typography-text type="secondary">
                {{ response.programming_stack.toString() }}
              </a-typography-text>

              <a-typography-title :level="5">Certificates</a-typography-title>
              <div v-for="certificate in response.certificates">
                <a-typography-text type="secondary">{{ certificate.name }}</a-typography-text>
              </div>
            </div>

            <div class="step-actions">
              <a-button v-if="currentStep > 0" @click="currentStep--">Previous</a-button>

              <a-button v-if="currentStep < questions.length" type="primary" @click="validateInput">
                Next
              </a-button>

              <a-button
                v-if="currentStep === questions.length"
                type="primary"
                html-type="submit"
                :loading="submitLoading"
              >
                Submit
              </a-button>
            </div>
          </a-form>
        </div>
      </div>
    </section>

    <section v-if="currentNavButton === 'Responses'">
      <h1>Survey responses</h1>

      <a-input-search
        placeholder="Enter email address..."
        enter-button="Search"
        size="large"
        :loading="searchLoading"
        @search="onSearch"
      />

      <a-table
        :columns="columns"
        :data-source="data?.data.results"
        :pagination="pagination"
        :loading="loading"
        :expand-column-width="100"
        @change="handleTableChange"
      >
        <template #bodyCell="{ column, text }">
          <template v-if="column.dataIndex === 'name'">{{ text.first }} {{ text.last }}</template>
        </template>

        <template #expandedRowRender="{ record }">
          <p style="margin: 0">
            {{ record.name }}
          </p>
        </template>

        <template #expandColumnTitle>
          <span style="color: red">View</span>
        </template>
      </a-table>
    </section>
  </main>
</template>

<script setup lang="ts">
import { computed, onMounted, reactive, ref, watch } from 'vue'
import type { FormInstance, UploadProps } from 'ant-design-vue'
import { UploadOutlined } from '@ant-design/icons-vue'
import { usePagination } from 'vue-request'
import axios from 'axios'
import { useQuestionStore } from '@/stores/question'
import { storeToRefs } from 'pinia'
import { message } from 'ant-design-vue'

interface Form {
  full_name: string
  email_address: string
  description: string
  gender: string
  programming_stack: Array<string>
  certificates: Array<File>
}

const apiEndpoint = import.meta.env.VITE_API_ENDPOINT

const questionsStore = useQuestionStore()
const { questions } = storeToRefs(questionsStore)

const navButtons = ref(['Questions', 'Responses'])
const currentNavButton = ref('Questions')

const questionsLoading = ref(false)
const currentStep = ref(0)
const formInputNames = ref<any[]>([])
const submitLoading = ref(false)

const formRef = ref<FormInstance>()
const response = reactive<Form>({
  full_name: '',
  email_address: '',
  description: '',
  gender: '',
  programming_stack: [],
  certificates: [],
})

watch(questions, (newVal: any) => {
  formInputNames.value = Array.from(newVal).map((question: any) => question.name)
})

/**
 * Loads the questions and responses from the API and updates the store
 */
onMounted(async () => {
  if (questions.value.length === 0) {
    questionsLoading.value = true

    const res = await questionsStore.getQuestions()

    if (res.status === 200) {
      // Sort the questions based on the ID
      const sortedQuestions = res.questions.sort((q1: any, q2: any) => q1.id - q2.id)

      // Update the questions store state
      questionsStore.$patch({
        questions: sortedQuestions,
      })
    } else {
      console.log(res)
    }

    questionsLoading.value = false
  } else return
})

/**
 * Validates the form input before moving to the next question
 */
async function validateInput(): Promise<any> {
  try {
    const fieldName = formInputNames.value[currentStep.value]

    await formRef.value?.validateFields([fieldName])

    currentStep.value++
  } catch (errorInfo: any) {
    console.log('Error:', errorInfo.errorFields[0].name[0], 'is required!')
  }
}

/**
 * Updates the certificates property in the form response object
 * @param file file object
 * @param fileList file list
 * @returns false to prevent the upload component from saving the uploaded file to a server
 */
const uploadCertificates: UploadProps['beforeUpload'] = (file, fileList) => {
  response.certificates = fileList

  return false
}

/**
 * Handles the deletion of an uploaded file
 * @param file file object to delete
 */
const deleteCertificate: UploadProps['onRemove'] = (file: any) => {
  const index = response.certificates.indexOf(file)
  const newFileList = response.certificates.slice()

  newFileList.splice(index, 1)
  response.certificates = newFileList
}

/**
 * Submits the form data to the API for uploading
 */
function submitResponse() {
  submitLoading.value = true

  let certificates: Array<File> = []

  response.certificates.forEach((cert: any) => certificates.push(cert.originFileObj))

  const responseObj = {
    full_name: response.full_name,
    email_address: response.email_address,
    description: response.description,
    gender: response.gender,
    programming_stack: response.programming_stack.toString(),
    certificates: certificates,
  }

  axios
    .put(`${apiEndpoint}/questions/responses`, responseObj, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    })
    .then((res) => {
      message.success('Your response has been saved!')

      const userResponse = res.data.response

      console.log(userResponse)
    })
    .catch((error) => {
      message.error('Something went wrong! Please try again')

      console.log(error)
    })
    .finally(() => {
      submitLoading.value = false

      // Reset form
      response.full_name = ''
      response.email_address = ''
      response.description = ''
      response.gender = ''
      response.programming_stack = []
      response.certificates = []

      currentStep.value = 0
    })
}

/**
 * Checks if the form is validated
 * @param error form errors found
 */
function submitFailed(error: any): void {
  console.log('Failed:', error)
}

// Response code

const searchLoading = ref(false)

const columns = [
  {
    title: 'Name',
    dataIndex: 'name',
    sorter: true,
    width: '50%',
  },
  {
    title: 'Email',
    dataIndex: 'email',
  },
]

type APIParams = {
  results: number
  page?: number
  sortField?: string
  sortOrder?: number
  [key: string]: any
}

type APIResult = {
  results: {
    gender: 'female' | 'male'
    name: string
    email: string
  }[]
}

const queryData = (params: APIParams) => {
  return axios.get<APIResult>('https://randomuser.me/api?noinfo', { params })
}

const { data, current, loading, pageSize, changePagination } = usePagination(queryData, {
  defaultParams: [
    {
      results: 5,
    },
  ],
  pagination: {
    currentKey: 'page',
    pageSizeKey: 'results',
  },
})

const pagination = computed(() => ({
  total: 20,
  current: current.value,
  pageSize: pageSize.value,
}))

const handleTableChange = (
  pag: { pageSize: number; current: number },
  filters: any,
  sorter: any,
) => {
  changePagination(pag.current, pag.pageSize)
}

const onSearch = (emailAddress: string) => {
  searchLoading.value = true

  console.log('Search: ', emailAddress)

  setTimeout(() => {
    searchLoading.value = false
  }, 3000)
}
</script>

<style scoped>
main {
  padding: 20px 24px;
}

section {
  padding-top: 20px;
}

.step-content,
.step-actions {
  margin: 20px 0;
}

.question-description {
  margin-bottom: 10px;
}

.step-actions {
  display: flex;
  justify-content: space-between;
}

.required-desc::before {
  content: '*';
  color: red;
  margin-right: 4px;
}
</style>
