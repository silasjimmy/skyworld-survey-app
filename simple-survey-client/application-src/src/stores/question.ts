import { ref } from 'vue'
import { defineStore } from 'pinia'
import axios from 'axios'

const apiEndpoint = import.meta.env.VITE_API_ENDPOINT

export const useQuestionStore = defineStore('question', () => {
  const questions: any = ref([])

  async function getQuestions() {
    const questions = await axios.get(`${apiEndpoint}/questions`)
    
    return questions.data
  }

  return { questions, getQuestions }
})
