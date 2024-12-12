import React from 'react';

const ErrorMessage = ({ type, message }) => {
    const getErrorMessage = () => {
        switch (type) {
            case 'ValidationError':
                return `Validation Error: ${message}`;
            case 'NotFound':
                return `Not Found: ${message}`;
            case 'InternalError':
                return 'Something went wrong on our side. Please try again later.';
            default:
                return `Error: ${message}`;
        }
    };

    return (
        <div style={{ color: 'red', textAlign: 'center', marginTop: '20px' }}>
            {getErrorMessage()}
        </div>
    );
};

export default ErrorMessage;
