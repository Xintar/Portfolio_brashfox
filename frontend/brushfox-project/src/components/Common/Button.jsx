import './Button.css';

const Button = ({ 
  children, 
  onClick, 
  type = 'button', 
  variant = 'primary',
  disabled = false,
  fullWidth = false,
  className = ''
}) => {
  const buttonClass = `btn btn-${variant} ${fullWidth ? 'btn-full' : ''} ${className}`;
  
  return (
    <button 
      type={type} 
      onClick={onClick} 
      disabled={disabled}
      className={buttonClass}
    >
      {children}
    </button>
  );
};

export default Button;
