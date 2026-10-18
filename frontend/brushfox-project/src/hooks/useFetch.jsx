import { useState, useEffect } from 'react';
import { getErrorMessage } from '../utils/helpers';

const EMPTY_DEPENDENCIES = [];

export const useFetch = (fetchFunction, dependencies = EMPTY_DEPENDENCIES) => {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const fetchData = async () => {
    setLoading(true);
    setError(null);
    
    try {
      const response = await fetchFunction();
      setData(response.data);
    } catch (err) {
      setError(getErrorMessage(err));
      console.error('Fetch error:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, dependencies);

  return { data, loading, error, refetch: fetchData };
};

export default useFetch;
