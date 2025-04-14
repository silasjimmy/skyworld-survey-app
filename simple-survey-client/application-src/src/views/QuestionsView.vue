<template>
  <a-page-header
    title="Survey Questions"
    style="border-bottom: 1px solid rgb(235, 237, 240)"
    @back="$router.push('/')"
  />

  <main class="spacing">
    <div v-if="questionsLoading" class="vertical-spacing" style="text-align: center">
      <a-spin />
    </div>

    <div v-else class="vertical-spacing">
      <div class="vertical-spacing">
        <span class="required-mark">required</span>
      </div>

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
              <div v-if="question.description" class="vertical-spacing">
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

        <div class="vertical-spacing">
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
  </main>
</template>

<script setup lang="ts">
import { useQuestionStore } from '@/stores/question'
import { message } from 'ant-design-vue'
import axios from 'axios'
import { storeToRefs } from 'pinia'
import { onMounted, reactive, ref, watch } from 'vue'
import type { FormInstance, UploadProps } from 'ant-design-vue'
import { UploadOutlined } from '@ant-design/icons-vue';

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
const questionsLoading = ref(false)
const submitLoading = ref(false)
const currentStep = ref(0)
const formInputNames = ref<any[]>([])
const formRef = ref<FormInstance>()

const response = reactive<Form>({
  full_name: '',
  email_address: '',
  description: '',
  gender: '',
  programming_stack: [],
  certificates: [],
})

/**
 * Watch `questions` state changes and generate an Array of form input names
 */
watch(questions as any, (newVal: any) => {
  formInputNames.value = Array.from(newVal).map((question: any) => question.name)
})

onMounted(async () => {
  if (questions.value.length === 0) {
    questionsLoading.value = true

    const questionsRes = await questionsStore.getQuestions()

    if (questionsRes.status === 200) {
      // Sort the questions based on the ID
      const sortedQuestions = questionsRes.questions.sort((q1: any, q2: any) => q1.id - q2.id)

      // Update the questions store state
      questionsStore.$patch({
        questions: sortedQuestions,
      })
    } else {
      message.error('Failed to fetch survey questions!')
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
</script>

<style scoped>
.required-mark::before {
  content: '*';
  color: red;
  margin-right: 4px;
}
</style>
