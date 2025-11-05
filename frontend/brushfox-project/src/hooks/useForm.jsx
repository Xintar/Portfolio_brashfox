import { useState } from 'react';
import { getErrorMessage } from '../utils/helpers';

export const useForm = (initialValues, onSubmit, validate) => {
  const [values, setValues] = useState(initialValues);
  const [errors, setErrors] = useState({});
  const [loading, setLoading] = useState(false);
  const [submitError, setSubmitError] = useState(null);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setValues(prev => ({ ...prev, [name]: value }));
    
    // Clear error for this field
    if (errors[name]) {
      setErrors(prev => ({ ...prev, [name]: '' }));
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setSubmitError(null);

    // Validate if validation function provided
    if (validate) {
      const validationErrors = validate(values);
      if (Object.keys(validationErrors).length > 0) {
        setErrors(validationErrors);
        return;
      }
    }

    setLoading(true);
    
    try {
      await onSubmit(values);
      setValues(initialValues); // Reset form
      setErrors({});
    } catch (error) {
      setSubmitError(getErrorMessage(error));
      console.error('Form submission error:', error);
    } finally {
      setLoading(false);
    }
  };

  const reset = () => {
    setValues(initialValues);
    setErrors({});
    setSubmitError(null);
  };

  return {
    values,
    errors,
    loading,
    submitError,
    handleChange,
    handleSubmit,
    reset,
    setValues,
  };
};

export default useForm;
