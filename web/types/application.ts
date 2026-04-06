export type ApplicationStatus = 'pending' | 'applied' | 'screening' | 'interview' | 'offer' | 'rejected' | 'accepted' | 'withdrawn'

export type JobPlatform = 'linkedin' | 'indeed' | 'company_site' | 'other'

export interface Application {
  id: number
  company: string
  position: string
  job_url?: string
  platform?: JobPlatform
  status: ApplicationStatus
  posted_date?: string
  applied_date?: string
  location?: string
  remote?: boolean
  salary_min?: number
  salary_max?: number
  currency?: string
  notes?: string
  created_at: string
}

export interface CreateApplication {
  company: string
  position: string
  job_url?: string
  platform?: JobPlatform
  status?: ApplicationStatus
  posted_date?: string
  applied_date?: string
  salary_min?: number
  salary_max?: number
  currency?: string
  location?: string
  remote?: boolean
  notes?: string
}
