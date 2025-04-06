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
      <h1>Survey questions</h1>
      <span>marks required questions</span>

      <div class="step-content">
        <a-form layout="vertical" :model="response">
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

                <div v-if="question.type === 'short_text'">
                  <a-input
                    v-if="question.name === 'full_name'"
                    v-model:value="response.full_name"
                  />

                  <a-input
                    v-else-if="question.name === 'email_address'"
                    v-model:value="response.email_address"
                  />
                </div>

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
                    v-model:file-list="response.certificates"
                    :name="question.name"
                    @change="handleChange"
                  >
                    <a-button>
                      <upload-outlined></upload-outlined>
                      Click to Upload
                    </a-button>
                  </a-upload>
                </div>
              </a-form-item>
            </a-card>
          </div>
        </a-form>
      </div>

      <div class="step-actions">
        <a-button v-if="currentStep > 0" @click="currentStep--">Previous</a-button>

        <a-button v-if="currentStep < questions.length - 1" type="primary" @click="currentStep++">
          Next
        </a-button>

        <a-button v-if="currentStep === questions.length - 1" type="primary">Submit</a-button>
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
import { computed, reactive, ref } from 'vue'
import type { UploadChangeParam } from 'ant-design-vue'
import { message } from 'ant-design-vue'
import { UploadOutlined } from '@ant-design/icons-vue'
import { usePagination } from 'vue-request'
import axios from 'axios'

const navButtons = ref(['Questions', 'Responses'])
const currentNavButton = ref('Questions')
const currentStep = ref(0)

const searchLoading = ref(false)

interface Form {
  full_name: string
  email_address: string
  description: string
  gender: string
  programming_stack: Array<string>
  certificates: Array<File>
}

const response = reactive<Form>({
  full_name: '',
  email_address: '',
  description: '',
  gender: '',
  programming_stack: [],
  certificates: [],
})

const questions = ref([
  {
    id: 0,
    name: 'full_name',
    type: 'short_text',
    text: 'What is your full name?',
    required: true,
    description: '[Surname] [First Name] [Other Names]',
    options: null,
  },
  {
    id: 1,
    name: 'email_address',
    type: 'short_text',
    text: 'What is your email address?',
    required: true,
    description: null,
    options: null,
  },
  {
    id: 2,
    name: 'description',
    type: 'long_text',
    text: 'Tell us a bit more about yourself',
    required: true,
    description: null,
    options: null,
  },
  {
    id: 3,
    name: 'gender',
    type: 'single_choice',
    text: 'What is your gender?',
    required: true,
    description: null,
    options: [
      {
        id: 0,
        label: 'Male',
        value: 'MALE',
      },
      {
        id: 1,
        label: 'Female',
        value: 'FEMALE',
      },
      {
        id: 2,
        label: 'Other',
        value: 'OTHER',
      },
    ],
  },
  {
    id: 4,
    name: 'programming_stack',
    type: 'multiple_choice',
    text: 'What programming stack are you familiar with?',
    required: true,
    description: 'You can select multiple',
    options: [
      {
        id: 3,
        label: 'React JS',
        value: 'REACT',
      },
      {
        id: 4,
        label: 'Angular JS',
        value: 'ANGULAR',
      },
      {
        id: 5,
        label: 'Vue JS',
        value: 'VUE',
      },
      {
        id: 6,
        label: 'SQL',
        value: 'SQL',
      },
      {
        id: 7,
        label: 'Postgres',
        value: 'POSTGRES',
      },
      {
        id: 8,
        label: 'MySQL',
        value: 'MYSQL',
      },
      {
        id: 9,
        label: 'Microsoft SQL Server',
        value: 'MSSQL',
      },
      {
        id: 10,
        label: 'Java',
        value: 'JAVA',
      },
      {
        id: 11,
        label: 'PHP',
        value: 'PHP',
      },
      {
        id: 12,
        label: 'Go',
        value: 'GO',
      },
      {
        id: 13,
        label: 'Rust',
        value: 'RUST',
      },
    ],
  },
  {
    id: 5,
    name: 'certificates',
    type: 'file',
    text: 'Upload any of your certificates?',
    required: true,
    description: 'You can upload multiple (.pdf)',
    options: null,
  },
])

const handleChange = (info: UploadChangeParam) => {
  if (info.file.status !== 'uploading') {
    console.log(info.file, info.fileList)
  }
  if (info.file.status === 'done') {
    message.success(`${info.file.name} file uploaded successfully`)
  } else if (info.file.status === 'error') {
    message.error(`${info.file.name} file upload failed.`)
  }
}

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

.step-content {
  margin: 20px 0;
}

.question-description {
  margin-bottom: 10px;
}

.step-actions {
  display: flex;
  justify-content: space-between;
}
</style>
