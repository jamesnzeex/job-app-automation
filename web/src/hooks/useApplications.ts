import { useState, useEffect, useCallback } from 'react';
import { applicationApi, interviewApi, Application, Interview, ApplicationFormData } from '@/lib/api';

export function useApplications() {
  const [applications, setApplications] = useState<Application[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchApplications = useCallback(async () => {
    try {
      setLoading(true);
      const data = await applicationApi.getAll();
      setApplications(data);
      setError(null);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to fetch applications');
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchApplications();
  }, [fetchApplications]);

  const addApplication = async (data: ApplicationFormData) => {
    const newApp = await applicationApi.create(data);
    setApplications(prev => [...prev, newApp]);
    return newApp;
  };

  const updateApplication = async (id: number, data: ApplicationFormData) => {
    const updated = await applicationApi.update(id, data);
    setApplications(prev => prev.map(app => app.id === id ? updated : app));
    return updated;
  };

  const removeApplication = async (id: number) => {
    await applicationApi.delete(id);
    setApplications(prev => prev.filter(app => app.id !== id));
  };

  return {
    applications,
    loading,
    error,
    refetch: fetchApplications,
    addApplication,
    updateApplication,
    removeApplication,
  };
}

export function useApplication(id: number) {
  const [application, setApplication] = useState<Application | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchApplication = async () => {
      try {
        setLoading(true);
        const data = await applicationApi.getById(id);
        setApplication(data);
        setError(null);
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Failed to fetch application');
      } finally {
        setLoading(false);
      }
    };

    fetchApplication();
  }, [id]);

  const update = async (data: ApplicationFormData) => {
    const updated = await applicationApi.update(id, data);
    setApplication(updated);
    return updated;
  };

  const deleteApp = async () => {
    await applicationApi.delete(id);
    setApplication(null);
  };

  return {
    application,
    loading,
    error,
    update,
    delete: deleteApp,
  };
}

export function useInterviews(applicationId: number) {
  const [interviews, setInterviews] = useState<Interview[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchInterviews = async () => {
      try {
        setLoading(true);
        const data = await interviewApi.getAll(applicationId);
        setInterviews(data);
        setError(null);
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Failed to fetch interviews');
      } finally {
        setLoading(false);
      }
    };

    if (applicationId) {
      fetchInterviews();
    }
  }, [applicationId]);

  const addInterview = async (data: Partial<Interview>) => {
    const interview = await interviewApi.create(applicationId, data);
    setInterviews(prev => [...prev, interview]);
    return interview;
  };

  const updateInterview = async (interviewId: number, data: Partial<Interview>) => {
    const updated = await interviewApi.update(applicationId, interviewId, data);
    setInterviews(prev => prev.map(irt => irt.id === interviewId ? updated : irt));
    return updated;
  };

  const removeInterview = async (interviewId: number) => {
    await interviewApi.delete(applicationId, interviewId);
    setInterviews(prev => prev.filter(irt => irt.id !== interviewId));
  };

  return {
    interviews,
    loading,
    error,
    addInterview,
    updateInterview,
    removeInterview,
  };
}
