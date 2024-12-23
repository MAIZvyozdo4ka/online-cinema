import React from 'react';

const ErrorMessage = ({ type, message, additionalStyles = {} }) => {
    const getErrorMessage = () => {
        switch (type) {
            case 'ValidationError':
                return `Validation Error: ${message}`;
            case 'NotFound':
                return `Not Found: ${message}`;
            case 'InternalError':
                return 'Something went wrong on our side. Please try again later.';
            case 'Unauthorized':
                return `Unauthorized: ${message}`;
            default:
                return `Error: ${message || 'An unexpected error occurred.'}`;
        }
    };

    return (
        <div
            style={{
                color: '#721c24',
                backgroundColor: '#f8d7da',
                border: '1px solid #f5c6cb',
                padding: '10px',
                borderRadius: '5px',
                margin: '20px auto',
                maxWidth: '400px',
                textAlign: 'center',
                fontSize: '14px',
                ...additionalStyles,
            }}
        >
            {getErrorMessage()}
        </div>
    );
};

export default ErrorMessage;
