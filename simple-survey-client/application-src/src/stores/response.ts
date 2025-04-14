import { ref } from 'vue'
import { defineStore } from 'pinia'
import axios from 'axios'

const apiEndpoint = import.meta.env.VITE_API_ENDPOINT

export const useResponseStore = defineStore('response', () => {
  const responses: any = ref([])

  async function getResponses() {
    const responses = await axios.get(`${apiEndpoint}/questions/responses`)
    
    return responses.data
  }

  return { responses, getResponses }
})
